import streamlit as st
import mysql.connector
import requests
import pandas as pd

st.set_page_config(page_title="Ask Car AI", layout="centered")
st.title("🧠 Ask Anything About Used Cars (via LLaMA 3.2)")

# --- MySQL Configuration ---
db_config = {
    "host": "localhost",
    "user": "root",
    "password": "mbng1234@@@@",  # Change this if needed
    "database": "car_selling_startup"   # Make sure this matches your MySQL DB
}

# --- Ask Input ---
user_query = st.text_input("💬 Enter your car-related question:")

if st.button("Ask LLaMA"):
    if not user_query.strip():
        st.warning("Please enter a question.")
        st.stop()

    # --- Build LLaMA Prompt ---
    prompt = f"""
You are a helpful assistant that converts user questions into MySQL SELECT queries.

Table: car_startup  
Columns: car_name , Distance , Owner , Fuel , Drive , Car_Age , Selling_Price , Location

User question: "{user_query}"

Provide only a valid MySQL SELECT query.
    """

    # --- Call LLaMA 3.2 locally ---
    with st.spinner("🧠 Thinking with LLaMA 3.2..."):
        try:
            response = requests.post(
                "http://localhost:11434/api/generate",
                json={"model": "llama3.2:latest", "prompt": prompt, "stream": False}
            )
            generated_sql = response.json()["response"].strip()
            st.code(generated_sql, language="sql")
        except Exception as e:
            st.error(f"❌ Failed to parse LLaMA output: {e}")
            st.stop()

    # --- Run SQL ---
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        cursor.execute(generated_sql)
        rows = cursor.fetchall()
        columns = [desc[0] for desc in cursor.description]

        df = pd.DataFrame(rows, columns=columns)
        if df.empty:
            st.info("No results found.")
        else:
            st.success("✅ Query executed successfully!")
            st.dataframe(df)

    except mysql.connector.Error as err:
        st.error(f"MySQL Error: {err}")
    except Exception as e:
        st.error(f"⚠️ Unexpected Error: {e}")
    finally:
        if 'conn' in locals() and conn.is_connected():
            cursor.close()
            conn.close()