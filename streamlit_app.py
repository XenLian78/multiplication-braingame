import streamlit as st
import random
import time

# 1. Ρύθμιση σελίδας
st.set_page_config(page_title="Multiplication Brain Game", page_icon="🧠", layout="centered")

# 2. CSS για το Flip Effect και το στυλ των καρτών
st.markdown("""
<style>
    .stApp { background-color: #f0f7ff; }
    
    /* Στυλ για το μεγάλο μπλε κουμπί ΞΕΚΙΝΑΜΕ */
    div.stButton > button[kind="primary"] {
        background-color: #0077b6 !important;
        color: white !important;
        width: 100% !important;
        height: 60px !important;
        font-size: 24px !important;
        border-radius: 15px !important;
        border: none !important;
        font-weight: bold !important;
    }

    /* Στυλ για τις κάρτες-κουμπιά */
    .card-box {
        width: 100%;
        aspect-ratio: 1 / 1;
        display: flex;
        align-items: center;
        justify-content: center;
        border-radius: 15px;
        font-weight: bold;
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
        border: 3px solid;
        text-align: center;
        transition: transform 0.3s;
    }

    .card-back { background-color: #ced4da; color: #495057; border-color: #adb5bd; font-size: 35px; }
    .white-card { background-color: white; color: #495057; border-color: #a2d2ff; font-size: 20px; }
    .blue-card { background-color: #e0f2fe; color: #0369a1; border-color: #0ea5e9; font-size: 24px; }
    .matched-card { background-color: #d1ffdb !important; border-color: #4caf50 !important; color: #1b5e20 !important; }

    /* Αφαίρεση του προεπιλεγμένου στυλ των κουμπιών του Streamlit για τις κάρτες */
    div[data-testid="stColumn"] button {
        height: auto !important;
        padding: 0 !important;
        border: none !important;
        background: none !important;
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
    st.title("🧮 Multiplication Brain Game")
    st.subheader("Ποιους αριθμούς θα μάθουμε σήμερα;")
    
    cols = st.columns(5)
    selected = [i for i in range(1, 11) if cols[(i-1)%5].checkbox(str(i), key=f"sel_{i}")]
    
    st.write("")
    if not selected:
        st.info("ℹ️ Επίλεξε τουλάχιστον έναν αριθμό για να ξεκινήσεις!")
    else:
        # Μεγάλο Μπλε Κουμπί
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
    
    # Progress Bar
    st.progress(len(st.session_state.matched_indices) / 12)
    
    c1, c2 = st.columns(2)
    c1.metric("⏱️ Χρόνος", format_time(elapsed))
    c2.metric("🔄 Προσπάθειες", st.session_state.attempts)

    # Grid 4x3
    for row in range(3):
        cols = st.columns(4)
        for col in range(4):
            idx = row * 4 + col
            card = st.session_state.deck[idx]
            is_matched = idx in st.session_state.matched_indices
            is_flipped = idx in st.session_state.flipped_indices or is_matched
            
            # Δημιουργία του HTML περιεχομένου της κάρτας
            if is_matched:
                style, content = "matched-card", "✅"
            elif is_flipped:
                style = "white-card" if card['type'] == 'q' else "blue-card"
                content = card['content']
            else:
                style, content = "card-back", "❓"

            card_html = f'<div class="card-box {style}">{content}</div>'
            
            with cols[col]:
                # Χρήση του HTML ως label του κουμπιού
                if st.button(card_html, key=f"btn_{idx}", disabled=is_flipped or len(st.session_state.flipped_indices) >= 2, help=None):
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
            time.sleep(0.8)
            st.session_state.flipped_indices = []
            st.rerun()

    if len(st.session_state.matched_indices) == 12:
        st.session_state.finish_time = elapsed
        st.balloons()
        st.success(f"🎉 Μπράβο! Χρόνος: {format_time(elapsed)} | Προσπάθειες: {st.session_state.attempts}")
        if st.button("🔄 Νέο Παιχνίδι", type="primary", use_container_width=True):
            st.session_state.game_running = False
            st.rerun()
