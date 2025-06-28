import streamlit as st
import mysql.connector

st.set_page_config(page_title="Feedback", layout="centered")
st.title("📝 We'd Love Your Feedback!")

# --- MySQL config ---
db_config = {
    "host": "localhost",
    "user": "root",
    "password": "mbng1234@@@@",  # Change if needed
    "database": "car_selling_startup"
}

# --- Feedback Form ---
with st.form("feedback_form"):
    rating = st.slider("⭐ Rate this app (1 = Poor, 5 = Excellent)", 1, 5, 3)
    comment = st.text_area("💬 Leave your comment or suggestion:")
    email = st.text_input("📧 Your Email (optional)")
    submitted = st.form_submit_button("Submit Feedback")

# --- Save to MySQL ---
if submitted:
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        query = "INSERT INTO feedback (Rating, Email, Comment) VALUES (%s, %s, %s)"
        cursor.execute(query, (rating, email, comment))
        conn.commit()
        st.success("✅ Thank you! Your feedback has been saved.")
    except Exception as e:
        st.error(f"❌ Failed to save feedback: {e}")
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()
