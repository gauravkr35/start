import streamlit as st

st.set_page_config(page_title="Used Car Dashboard", layout="centered")
st.title("🚗 Used Car ML App")

st.markdown("Welcome! Choose what you'd like to do:")

st.page_link("pages/1_Predict_Price.py", label="💰 Predict Car Price", icon="💰")
st.page_link("pages/2_Compare_Cars.py", label="🆚 Compare Cars", icon="🆚")
st.page_link("pages/3_Ask_AI.py", label="🧠 Ask AI About Cars", icon="💬")
st.page_link("pages/4_Feedback.py", label="📝 Feedback", icon="✍️")
