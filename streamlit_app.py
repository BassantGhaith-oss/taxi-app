import streamlit as st
import pandas as pd
import numpy as np
import joblib


# ----------------- Title -----------------
st.title('The Survivors')
st.info('Welcome to Survivors Team App')

# ----------------- Sidebar Menu -----------------
page = st.sidebar.radio(
    "Navigation",
    ["Taxi Model", "Credit Model"]
)

model1 = load_model("taxi_model.pkl")


# 🚕 Taxi Model Page

if page == "Taxi Model":
    st.header("Pick up Trip")
    model1 = joblib.load("taxi_model.pkl")
    

# 💳 Credit Model Page

elif page == "Credit Model":
    model2 = joblib.load("best_random_forest_model.pkl")



