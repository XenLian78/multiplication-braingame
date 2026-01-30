import streamlit as st
import random
import time
import os

# 1. Ρύθμιση σελίδας
st.set_page_config(page_title="Brain Game: Προπαίδεια", page_icon="🧠", layout="centered")

# 2. CSS για την τελική εμφάνιση
st.markdown("""
<style>
    .stApp { background-color: #f0f7ff; }
    
    /* Μεγάλο Μπλε Κουμπί ΞΕΚΙΝΑΜΕ */
    div.stButton > button[kind="primary"] {
        background-color: #0077b6 !important;
        color: white !important;
        height: 65px !important;
        font-size: 26px !important;
        border-radius: 15px !important;
        font-weight: bold !important;
    }

    /* Στυλ Κάρτας */
    .big-card {
        width: 100%;
        height: 140px;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        border-radius: 15px;
        font-weight: bold;
        box-shadow: 0 6px 12px rgba(0,0,0,0.1);
        border: 4px solid;
        text-align: center;
        margin-bottom: 8px;
        transition: transform 0.2s;
    }

    /* Πίσω μεριά κάρτας με την εικόνα μας */
    .card-closed { 
        background-image: url('https://raw.githubusercontent.com/YOUR_USERNAME/YOUR_REPO/master/card_back.png');
        background-size: cover;
        background-position: center;
        border-color: #0077b6;
    }

    /* Ανοιχτές κάρτες */
    .card-question { background-color: white; color: #495057; border-color: #a2d2ff; font-size: 24px; }
    .card-answer { background-color: #e0f2fe; color: #0369a1; border-color: #0ea5e9; font-size: 28px; }
    
    /* Σωστές κάρτες: Πράσινες αλλά με το περιεχόμενο ορατό */
    .card-matched { background-color: #d1ffdb; color: #1b5e20; border-color: #4caf50; font-size: 24px; }

    .card-hint { font-size: 11px; text-transform: uppercase; margin-top: 8px; opacity: 0.8; }
</style>
""", unsafe_allow_html=True)
