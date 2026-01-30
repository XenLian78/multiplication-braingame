import streamlit as st
import random
import time

# 1. Ρύθμιση σελίδας
st.set_page_config(page_title="Multiplication Brain Game", page_icon="🧠", layout="centered")

# 2. Καθαρό CSS χωρίς να επηρεάζει τα κανονικά κουμπιά του Streamlit
st.markdown("""
<style>
    .stApp { background-color: #f0f7ff; }
    
    /* Container για τις κάρτες */
    .card-container {
        position: relative;
        width: 100%;
        aspect-ratio: 1 / 1;
    }

    .card-inner {
        position: absolute;
        width: 100%;
        height: 100%;
        transition: transform 0.6s;
        transform-style: preserve-3d;
    }

    .is-flipped { transform: rotateY(360deg); }

    .card-front, .card-back {
        position: absolute;
        width: 100%;
        height: 100%;
        backface-visibility: hidden;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        border-radius: 15px;
        font-weight: bold;
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
        border: 3px solid;
    }

    .card-back { background-color: #ced4da; color: #495057; border-color: #adb5bd; font-size: 35px; }
    .white-card { background-color: white; color: #495057; border-color: #a2d2ff; font-size: 20px; }
    .blue-card { background-color: #e0f2fe; color: #0369a1; border-color: #0ea5e9; font-size: 24px; }
    .matched-card { background-color: #d1ffdb !important; border-color: #4caf50 !important; color: #1b5e20 !important; }

    .hint-label { font-size: 10px; text-transform: uppercase; margin-top: 4px; opacity: 0.7; }

    /* ΜΟΝΟ τα κουμπιά μέσα στο Grid των καρτών θα είναι αόρατα */
    [data-testid="stVerticalBlock"] > div:nth-child(2) [data-testid="stButton"] button {
        height: 100% !important;
        width: 100% !important;
        position: absolute !important;
        top: 0; left: 0;
        opacity: 0;
        z-index: 10;
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
    
    st.divider()
    
    if not selected:
        st.info("ℹ️ Επίλεξε τουλάχιστον έναν αριθμό για να ξεκινήσεις!")
    else:
        # Εδώ το κουμπί είναι ΚΑΝΟΝΙΚΟ Streamlit button, χωρίς CSS tricks
        if st.button("🚀 ΞΕΚΙΝΑΜΕ!", use_container_width=True, type="primary"):
            # Αρχικοποίηση παιχνιδιού
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
    
    st.progress(len(st.session_state.matched_indices) / 12)
    
    c1, c2 = st.columns(2)
    c1.metric("⏱️ Χρόνος", format_time(elapsed))
    c2.metric("🔄 Προσπάθειες", st.session_state.attempts)

    # Grid 4x3
    grid_placeholder = st.container()
    with grid_placeholder:
        for row in range(3):
            cols = st.columns(4)
            for col in range(4):
                idx = row * 4 + col
                card = st.session_state.deck[idx]
                is_matched = idx in st.session_state.matched_indices
                is_flipped = idx in st.session_state.flipped_indices or is_matched
                
                flip_style = "is-flipped" if is_flipped else ""
                
                if is_matched:
                    card_class, content, label = "matched-card", "✅", "ΒΡΕΘΗΚΕ"
                elif is_flipped:
                    card_class = "white-card" if card['type'] == 'q' else "blue-card"
                    label = "ΠΡΑΞΗ 📝" if card['type'] == 'q' else "ΑΠΟΤΕΛΕΣΜΑ 🎯"
                    content = card['content']
                else:
                    card_class, content, label = "card-back", "❓", ""

                with cols[col]:
                    # Σχεδίαση κάρτας
                    st.markdown(f"""
                    <div class="card-container">
                        <div class="card-inner {flip_style}">
                            <div class="card-back">❓</div>
                            <div class="card-front {card_class}">
                                <div>{content}</div>
                                <div class="hint-label">{label}</div>
                            </div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # Κουμπί ελέγχου (αόρατο)
                    if not is_flipped and len(st.session_state.flipped_indices) < 2:
                        if st.button(" ", key=f"btn_{idx}"):
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
            time.sleep(0.6)
            st.session_state.flipped_indices = []
            st.rerun()

    if len(st.session_state.matched_indices) == 12:
        st.session_state.finish_time = elapsed
        st.balloons()
        st.success(f"🎉 Συγχαρητήρια! Χρόνος: {format_time(elapsed)} | Προσπάθειες: {st.session_state.attempts}")
        if st.button("🔄 Νέο Παιχνίδι", use_container_width=True):
            st.session_state.game_running = False
            st.rerun()
