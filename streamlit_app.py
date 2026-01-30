import streamlit as st
import random
import time

# 1. Ρύθμιση σελίδας
st.set_page_config(page_title="Brain Game: Προπαίδεια", page_icon="🧠", layout="centered")

# 2. CSS για Σταθερότητα, Μείωση Κενών και Εμφάνιση
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Fredoka+One&display=swap');

    /* 1. Αφαίρεση περιττών κενών από την κορυφή και το πλάι */
    .block-container {
        padding-top: 1rem !important;
        padding-bottom: 0rem !important;
        max-width: 800px !important;
    }
    
    /* 2. Μείωση κενού ανάμεσα στα widgets */
    [data-testid="stVerticalBlock"] {
        gap: 0.3rem !important;
    }

    .stApp { background-color: #f0f7ff; }
    
    /* 3. Μεγάλα Μπλε Κουμπιά (Full Width) */
    div.stButton > button[kind="primary"] {
        background-color: #0077b6 !important;
        color: white !important;
        height: 80px !important;
        font-size: 32px !important;
        border-radius: 20px !important;
        font-weight: bold !important;
        width: 100% !important;
        box-shadow: 0 4px 15px rgba(0,119,182,0.3) !important;
        border: none !important;
    }

    /* Σταθερό Κοντέινερ Καρτών */
    [data-testid="stColumn"] {
        min-height: 190px !important;
        display: flex;
        flex-direction: column;
        justify-content: flex-start;
    }

    /* Στυλ Κάρτας */
    .big-card {
        width: 100%;
        height: 130px;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        border-radius: 20px;
        font-weight: bold;
        box-shadow: 0 6px 12px rgba(0,0,0,0.1);
        border: 4px solid;
        text-align: center;
        margin-bottom: 5px;
    }

    .card-closed { 
        background: linear-gradient(135deg, #0077b6 0%, #00b4d8 100%); 
        color: white; 
        border-color: #023e8a; 
    }
    
    .brain-text {
        font-family: 'Fredoka One', cursive;
        font-size: 20px;
        letter-spacing: 1px;
        text-shadow: 2px 2px #023e8a;
    }

    .card-question { background-color: white; color: #495057; border-color: #a2d2ff; font-size: 26px; }
    .card-answer { background-color: #e0f2fe; color: #0369a1; border-color: #0ea5e9; font-size: 30px; }
    .card-matched { background-color: #d1ffdb; color: #1b5e20; border-color: #4caf50; font-size: 26px; }
    .card-label { font-size: 11px; text-transform: uppercase; margin-top: 5px; font-weight: normal; opacity: 0.8; }

    /* 4. Το Μεγάλο Γαλάζιο Πλαίσιο Τέλους */
    .finish-box {
        background-color: #e0f2fe;
        border: 6px solid #0077b6;
        border-radius: 30px;
        padding: 40px;
        text-align: center;
        margin: 10px 0px;
        color: #0077b6;
        font-family: 'Fredoka One', cursive;
        box-shadow: 0 10px 25px rgba(0,0,0,0.1);
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
    st.markdown("### Ποιους αριθμούς θα μάθουμε σήμερα;")
    
    # Πιο μαζεμένο grid για τα checkboxes
    cols = st.columns(5)
    selected = [i for i in range(1, 11) if cols[(i-1)%5].checkbox(str(i), key=f"sel_{i}")]
    
    if not selected:
        st.info("ℹ️ Επίλεξε αριθμούς για να ξεκινήσεις!")
    else:
        # Το κουμπί πιάνει όλο το πλάτος και είναι κολλημένο στους αριθμούς
        if st.button("🚀 ΞΕΚΙΝΑΜΕ!", type="primary", use_container_width=True):
            all_pairs = []
            for n in selected:
                for i in range(1, 11):
                    all_pairs.append((f"{n} x {i}", n * i))
            
            selected_pairs = random.sample(all_pairs, 6)
            deck = []
            for pair in selected_pairs:
                deck.append({'content': pair[0], 'value': pair[1], 'type': 'q'})
                deck.append({'content': str(pair[1]), 'value': pair[1], 'type': 'a'})
            
            random.shuffle(deck)
            st.session_state.deck = deck
            st.session_state.matched_indices = []
            st.session_state.flipped_indices = []
            st.session_state.attempts = 0
            st.session_state.start_time = time.time()
            st.session_state.finish_time = None
            st.session_state.game_running = True
            st.rerun()

# --- ΚΥΡΙΟ ΠΑΙΧΝΙΔΙ ---
else:
    elapsed = time.time() - st.session_state.start_time if not st.session_state.finish_time else st.session_state.finish_time
    
    # Αν το παιχνίδι ΔΕΝ έχει τελειώσει
    if len(st.session_state.matched_indices) < 12:
        c1, c2 = st.columns(2)
        c1.metric("⏱️ Χρόνος", format_time(elapsed))
        c2.metric("🔄 Προσπάθειες", st.session_state.attempts)

        for row in range(3):
            cols = st.columns(4)
            for col in range(4):
                idx = row * 4 + col
                card = st.session_state.deck[idx]
                is_matched = idx in st.session_state.matched_indices
                is_flipped = idx in st.session_state.flipped_indices or is_matched
                
                if is_matched:
                    style = "card-matched"
                    content = f'<div>{card["content"]}</div><div class="card-label">ΣΩΣΤΟ! ✅</div>'
                elif is_flipped:
                    style = "card-question" if card['type'] == 'q' else "card-answer"
                    label = "ΠΡΑΞΗ" if card['type'] == 'q' else "ΑΠΟΤΕΛΕΣΜΑ"
                    content = f'<div>{card["content"]}</div><div class="card-label">{label}</div>'
                else:
                    style = "card-closed"
                    content = '<div class="brain-text">BRAIN<br>GAME</div>'

                with cols[col]:
                    st.markdown(f'<div class="big-card {style}">{content}</div>', unsafe_allow_html=True)
                    btn_label = "ΠΑΤΑ ΕΔΩ" if not is_flipped else "---"
                    if st.button(btn_label, key=f"btn_{idx}", disabled=is_flipped or len(st.session_state.flipped_indices) >= 2, use_container_width=True):
                        st.session_state.flipped_indices.append(idx)
                        st.rerun()

        # Match Logic
        if len(st.session_state.flipped_indices) == 2:
            st.session_state.attempts += 1
            i1, i2 = st.session_state.flipped_indices
            if st.session_state.deck[i1]['value'] == st.session_state.deck[i2]['value'] and st.session_state.deck[i1]['type'] != st.session_state.deck[i2]['type']:
                st.session_state.matched_indices.extend([i1, i2])
                st.session_state.flipped_indices = []
                st.rerun()
            else:
                time.sleep(1.2)
                st.session_state.flipped_indices = []
                st.rerun()

    # --- ΦΙΝΑΛΕ ---
    else:
        st.session_state.finish_time = elapsed
        st.balloons()
        
        # Το εντυπωσιακό γαλάζιο πλαίσιο
        st.markdown(f"""
            <div class="finish-box">
                <h1 style='font-size: 50px; margin-bottom: 0px;'>🎉 Μπράβο!</h1>
                <h2 style='font-size: 35px; margin-top: 0px;'>Τα κατάφερες.</h2>
                <hr style='border: 1px solid #0077b6; opacity: 0.2; margin: 20px 0;'>
                <p style='font-size: 35px;'>⏱️ Χρόνος: {format_time(elapsed)}</p>
            </div>
        """, unsafe_allow_html=True)
        
        if st.button("🔄 ΠΑΙΞΕ ΞΑΝΑ", type="primary", use_container_width=True):
            st.session_state.game_running = False
            st.rerun()
