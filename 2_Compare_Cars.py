import streamlit as st
import pandas as pd
import os

st.set_page_config(page_title="Compare Cars", layout="wide")
st.title("⚖️ Filter & Compare Cars")

# --- Load Excel ---
@st.cache_data
def load_data():
    return pd.read_excel("2.xlsx")

file_path = "2.xlsx"
if not os.path.exists(file_path):
    st.error("❌ File '2.xlsx' not found in the root directory.")
    st.stop()

df = load_data()

# Drop missing Car Name
df = df[df["Car Name"].notna()]

# --- Sidebar Filters ---
st.sidebar.header("🔍 Filter Options")

fuel_options = st.sidebar.multiselect("Fuel Type", df["Fuel"].unique(), default=df["Fuel"].unique())
owner_options = st.sidebar.multiselect("Owner", df["Owner"].unique(), default=df["Owner"].unique())
drive_options = st.sidebar.multiselect("Drive", df["Drive"].unique(), default=df["Drive"].unique())
age_range = st.sidebar.slider("Car Age (Years)", int(df["Car_Age"].min()), int(df["Car_Age"].max()), (1, 15))
price_range = st.sidebar.slider("Selling Price (₹)", int(df["Selling_Price"].min()), int(df["Selling_Price"].max()), (100000, 1000000))

# --- Apply Filters ---
filtered_df = df[
    (df["Fuel"].isin(fuel_options)) &
    (df["Owner"].isin(owner_options)) &
    (df["Drive"].isin(drive_options)) &
    (df["Car_Age"].between(age_range[0], age_range[1])) &
    (df["Selling_Price"].between(price_range[0], price_range[1]))
]

# --- Car Selection ---
car_list = filtered_df["Car Name"].unique()
st.markdown("### 🚗 Choose Cars to Compare (2 or 3)")
selected_cars = st.multiselect("Select cars:", car_list, max_selections=3)

# --- Comparison Table ---
if len(selected_cars) >= 2:
    compare_df = filtered_df[filtered_df["Car Name"].isin(selected_cars)].copy()

    # Ensure unique label for transpose
    compare_df["Unique Name"] = compare_df["Car Name"] + " (" + compare_df["Distance"].astype(str) + " km)"
    compare_df.set_index("Unique Name", inplace=True)
    compare_df.drop(columns=["Car Name"], inplace=True)

    st.markdown("### 📊 Comparison Table")
    st.dataframe(compare_df.T)

elif len(selected_cars) == 1:
    st.info("ℹ️ Please select at least 2 cars to compare.")
else:
    st.warning("👆 Use filters and select cars to compare.")
