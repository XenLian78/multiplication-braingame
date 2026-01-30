import streamlit as st
import random
import time

st.set_page_config(page_title="Brain Game: Προπαίδεια", page_icon="🧠", layout="centered")

# CSS - Καθαρό και χωρίς σφάλματα
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Fredoka+One&display=swap');
    
    .block-container { padding-top: 0.5rem !important; padding-bottom: 0rem !important; }
    [data-testid="stHeader"] { height: 0px !important; display: none !important; }
    .stApp { background-color: #f0f7ff; }
    
    [data-testid="stMetricContainer"] { 
        margin-top: -10px !important;
        margin-bottom: -35px !important; 
    }

    .reset-btn div.stButton > button {
        background-color: #ffb703 !important;
        color: #023e8a !important;
        height: 40px !important;
        font-size: 14px !important;
        margin-top: 5px !important;
        border-radius: 10px !important;
        border: 2px solid #fb8500 !important;
    }
    
    div.stButton > button[kind="primary"] { 
        background-color: #0077b6 !important; 
        color: white !important; 
        height: 60px !important; 
        font-size: 24px !important; 
        border-radius: 15px !important; 
        font-weight: bold !important;
    }

    .big-card { 
        width: 100%; 
        height: 120px; 
        display: flex; 
        flex-direction: column; 
        align-items: center; 
        justify-content: center; 
        border-radius: 18px; 
        font-weight: bold; 
        box-shadow: 0 4px 8px rgba(0,0,0,0.1); 
        border: 4px solid; 
        text-align: center; 
        margin-bottom: 2px; 
    }
    
    .card-closed { background: linear-gradient(135deg, #0077b6 0%, #00b4d8 100%); color: white; border-color: #023e8a; }
    .brain-text { font-family: 'Fredoka One', cursive; font-size: 19px; letter-spacing: 1px; text-shadow: 2px 2px #
