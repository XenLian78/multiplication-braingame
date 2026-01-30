import streamlit as st
import random
import time

st.set_page_config(page_title="Brain Game: Προπαίδεια", page_icon="🧠", layout="centered")

# CSS ΓΙΑ ΜΕΓΙΣΤΗ ΑΞΙΟΠΟΙΗΣΗ ΥΨΟΥΣ & ΤΟ ΝΕΟ ΚΟΥΜΠΙ
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Fredoka+One&display=swap');
    
    .block-container { padding-top: 0.5rem !important; padding-bottom: 0rem !important; }
    [data-testid="stHeader"] { height: 0px !important; display: none !important; }
    .stApp { background-color: #f0f7ff; }
    
    /* Σύμπτυξη στατιστικών */
    [data-testid="stMetricContainer"] { 
        margin-top: -10px !important;
        margin-bottom: -35px !important; 
    }

    /* Στυλ για το κουμπί ΑΛΛΑΓΗ */
    .reset-btn div.stButton > button {
        background-color: #ffb703 !important;
        color: #023e8a !important;
        height: 40px !important;
        font-size: 14px !important;
        margin-top: 5px !important;
        border-radius: 10px !important;
        border: 2px solid #fb8500 !important;
    }
    
    .main-game-container { margin-top: -15px !important; }

    /* Κύρια κουμπιά */
    div.stButton > button[kind="primary"] { 
        background-color: #0077b6 !important; 
        color: white !important; 
        height: 60px !important; 
        font-size: 24px !important; 
        border-radius: 15px !important; 
        font-weight: bold !important;
    }

    [data-testid="stColumn"] { min-height: 175px !important; display: flex; flex-direction: column; justify-content: flex-start; }
    
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
    .brain-text { font-family: 'Fredoka One', cursive; font-size: 19px; letter-spacing: 1px; text-shadow: 2px 2px #023e8a; }
    .card-question { background-color: white; color: #495057; border-color: #a2d2ff; font-size: 26px; }
    .card-answer { background-color: #e0f2fe; color: #0369a1; border-color: #0ea5e9; font-size: 30px; }
    .card-matched { background-color: #d1ffdb; color: #1b5e20; border-color: #4caf50; font-size: 26px; }
    .card-label { font-size: 10px; text-transform: uppercase; margin-top: 2px; font-weight: normal; opacity: 0.8; }

    .countdown-box {
        text-align: center;
        color: #d62828;
        font-family: 'Fredoka One', cursive;
        font-size: 22px;
        margin-bottom: 15px;
        padding: 5px;
        background-color: #ff000010;
        border-radius: 10px;
    }

    .finish-box {
        background-color: #e0f2fe;
        border: 6px solid #0077b6;
        border-radius: 30px;
        padding: 40px;
        text-align: center;
        margin-top: 10px;
        color: #0077b6;
        font-family: 'Fredoka One', cursive;
    }
</style>
""", unsafe_allow_html=True)

def format_time(seconds):
    mins, secs = divmod(int(seconds), 60)
    return f"{mins:02d}:{secs:02d}"

if 'game_running' not in st.session_state: st.session_state.game_running = False
if 'show_finish' not in st.session_state: st.session_state.show_finish = False
if 'memory_mode' not in st.session_state: st.session_state.memory_mode = False

# --- ΑΡΧΙΚΗ ΟΘΟΝΗ ---
if not st.session_state.game_running and not st.session_state.show_finish:
    st.title("🧠 Brain Game: Προπαίδεια")
    st.subheader("Ποιους αριθμού
