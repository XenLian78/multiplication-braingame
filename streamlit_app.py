import streamlit as st
import random
import time

# 1. Ρύθμιση σελίδας
st.set_page_config(page_title="Brain Game: Προπαίδεια", page_icon="🧠", layout="centered")

# 2. CSS για την τελική εμφάνιση
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Fredoka+One&display=swap');

    .stApp { background-color: #f0f7ff; }
    
    /* Μεγάλα Κουμπιά (Full Width) */
    div.stButton > button {
        width: 100% !important;
    }
    
    div.stButton > button[kind="primary"] {
        background-color: #0077b6 !important;
        color: white !important;
        height: 80px !important;
        font-size: 30px !important;
        border-radius: 20px !important;
        font-weight: bold !important;
        box-shadow: 0 4px 15px rgba(0,119,182,0.3) !important;
    }

    /* Σταθερό Κοντέινερ Καρτών */
    [data-testid="stColumn"] {
        min-height: 220px !important;
        display: flex;
        flex-direction: column;
        justify-content: flex-start;
    }

    /* Στυλ Κάρτας */
    .big-card {
        width: 100%;
        height: 140px;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        border-radius: 20px;
        font-weight: bold;
        box-shadow: 0 6px 12px rgba(0,0,0,0.1);
        border: 4px solid;
        text-align: center;
        margin-bottom: 10px;
    }

    .card-closed { 
        background: linear-gradient(135deg, #0077b6 0%, #00b4d8 100%); 
        color: white; 
        border-color: #023e8a; 
    }
    
    .brain-text {
        font-family: 'Fredoka One', cursive;
        font-size: 22px;
        letter-spacing: 2px;
        text-shadow: 2px 2px #023e8a;
    }

    .card-question { background-color: white; color: #495057; border-color: #a2d2ff; font-size: 28px; }
    .card-answer { background-color: #e0f2fe; color: #0369a1; border-color: #0ea5e9; font-size: 32px; }
    .card-matched { background-color: #d1ffdb; color: #1b5e20; border-color: #4caf50; font-size: 28px; }

    .card-label { font-size: 12px; text-transform: uppercase; margin-top: 10px; font-weight: normal; opacity: 0.8; }

    /* Το Μεγάλο Γαλάζιο Πλαίσιο Τέλους */
    .finish-box {
        background-color: #e0f2fe;
        border: 5px solid #0077b6;
        border-radius: 30px;
        padding: 40px;
        text-align: center;
        margin: 20px 0px;
        color: #0077b6;
        font-family: 'Fredoka One', cursive;
    }
</style>
""", unsafe_allow_html=True)

def format_time(seconds):
    mins, secs = divmod(int(seconds), 60)
    return f"{mins:02d}:{secs:02d}"

if 'game_running' not in st.session_state:
    st.session_state.game_running = False

# --- ΑΡΧΙΚΗ ΟΘΟΝΗ ---
if not st.session_state.game_running:
    st.title("🧠 Brain Game: Προπαίδεια")
    st.subheader("Ποιους αριθμούς θα μάθουμε σήμερα;")
    
    cols = st.columns(5)
    selected = [i for i in range(1, 11) if cols[(i-1)%5].checkbox(str(i), key=f"sel_{i}")]
    
    st.write("") # Κενό
    if not selected:
        st.info("ℹ️ Επίλεξε αριθμούς για να ξεκινήσεις!")
    else:
        # Μεγάλο κουμπί που πιάνει όλο το πλάτος
        if st.button("🚀 ΞΕΚΙΝΑΜΕ!", type="primary", use_container_width=True):
            all_pairs = []
            for n in selected:
                for i in range(1, 11):
                    all_pairs.append((f"{n} x {i}", n * i))
