import streamlit as st
import random
import time

# 1. Ρύθμιση σελίδας
st.set_page_config(page_title="Multiplication Brain Game", page_icon="🧠", layout="centered")

# 2. CSS για Επαγγελματική Εμφάνιση Καρτών και Κουμπιών
st.markdown("""
<style>
    .stApp { background-color: #f0f7ff; }
    
    /* Στυλ για το κουμπί ΞΕΚΙΝΑΜΕ (Μπλε και Μεγάλο) */
    div.stButton > button[kind="primary"] {
        background-color: #0077b6 !important;
        color: white !important;
        height: 60px !important;
        font-size: 24px !important;
        border-radius: 15px !important;
        font-weight: bold !important;
    }

    /* Στυλ για τις Κάρτες του Παιχνιδιού */
    /* Κάνουμε τα κουμπιά να μοιάζουν με μεγάλες τετράγωνες κάρτες */
    div.stButton > button:not([kind="primary"]) {
        width: 100% !important;
        aspect-ratio: 1 / 1 !important;
        height: auto !important;
        border-radius: 15px !important;
        border: 3px solid #adb5bd !important;
        background-color: #ced4da !important; /* Κλειστή κάρτα */
        color: #495057 !important;
        font-size: 30px !important;
        font-weight: bold !important;
        transition: all 0.3s ease;
    }

    /* Όταν η κάρτα είναι ανοιχτή (λευκή ή γαλάζια) θα αλλάζουμε το στυλ μέσω κώδικα */
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
        st.info("ℹ️ Επίλεξε αριθμούς για να ξεκινήσεις!")
    else:
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
            
            # Περιεχόμενο κάρτας
            if is_matched:
                label, icon = "✅", ""
            elif is_flipped:
                label = card['content']
                icon = "📝" if card['type'] == 'q' else "🎯"
            else:
                label, icon = "❓", ""

            with cols[col]:
                # Χρησιμοποιούμε κανονικό κουμπί χωρίς HTML μέσα στο label
                if st.button(f"{label}\n{icon}", key=f"btn_{idx}", disabled=is_flipped or len(st.session_state.flipped_indices) >= 2):
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
        st.success(f"🎉 Μπράβο! Το ολοκλήρωσες σε {format_time(elapsed)}!")
        if st.button("🔄 Παίξε Ξανά", type="primary", use_container_width=True):
            st.session_state.game_running = False
            st.rerun()
