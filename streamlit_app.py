import streamlit as st
import random
import time

# 1. Ρύθμιση σελίδας
st.set_page_config(page_title="Brain Game: Προπαίδεια", page_icon="🧠", layout="centered")

# 2. CSS για την εξάλειψη των κενών (margins/paddings)
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Fredoka+One&display=swap');

    /* 1. Μηδενισμός κενού στην κορυφή της σελίδας */
    .block-container {
        padding-top: 0rem !important;
        padding-bottom: 0rem !important;
        margin-top: -30px !important;
    }
    
    /* 2. Εξαφάνιση του Header του Streamlit */
    header {visibility: hidden;}
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}

    /* 3. Μείωση κενού ανάμεσα στα widgets (αυτό που κύκλωσες με κόκκινο) */
    [data-testid="stVerticalBlock"] {
        gap: 0rem !important;
    }
    
    /* 4. Μείωση κενού ανάμεσα σε κείμενο και κουμπί */
    div.stMarkdown {
        margin-bottom: -10px !important;
    }

    .stApp { background-color: #f0f7ff; }
    
    /* 5. Μεγάλα Μπλε Κουμπιά (Full Width) */
    div.stButton > button[kind="primary"] {
        background-color: #0077b6 !important;
        color: white !important;
        height: 70px !important;
        font-size: 28px !important;
        border-radius: 15px !important;
        font-weight: bold !important;
        width: 100% !important;
        margin-top: 5px !important;
    }

    /* Σταθερό Κοντέινερ Καρτών */
    [data-testid="stColumn"] {
        min-height: 160px !important; /* Μειώθηκε για να χωράει */
        gap: 0rem !important;
    }

    /* Στυλ Κάρτας - Πιο compact */
    .big-card {
        width: 100%;
        height: 110px; /* Μειώθηκε το ύψος */
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        border-radius: 15px;
        font-weight: bold;
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
        border: 3px solid;
        text-align: center;
        margin-bottom: 2px !important;
    }

    .card-closed { 
        background: linear-gradient(135deg, #0077b6 0%, #00b4d8 100%); 
        color: white; 
        border-color: #023e8a; 
    }
    
    .brain-text {
        font-family: 'Fredoka One', cursive;
        font-size: 18px;
        line-height: 1;
    }

    .card-question { background-color: white; color: #495057; border-color: #a2d2ff; font-size: 24px; }
    .card-answer { background-color: #e0f2fe; color: #0369a1; border-color: #0ea5e9; font-size: 28px; }
    .card-matched { background-color: #d1ffdb; color: #1b5e20; border-color: #4caf50; font-size: 24px; }
    
    /* Μικρότερα κουμπιά "ΠΑΤΑ ΕΔΩ" για εξοικονόμηση χώρου */
    div.stButton > button:not([kind="primary"]) {
        padding-top: 0px !important;
        padding-bottom: 0px !important;
        height: 30px !important;
        font-size: 12px !important;
    }

    /* Το Μεγάλο Γαλάζιο Πλαίσιο Τέλους */
    .finish-box {
        background-color: #e0f2fe;
        border: 5px solid #0077b6;
        border-radius: 25px;
        padding: 20px;
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

if 'game_running' not in st.session_state:
    st.session_state.game_running = False

# --- ΑΡΧΙΚΗ ΟΘΟΝΗ ---
if not st.session_state.game_running:
    st.markdown("## 🧠 Brain Game: Προπαίδεια")
    st.markdown("#### Ποιους αριθμούς θα μάθουμε σήμερα;")
    
    cols = st.columns(5)
    selected = [i for i in range(1, 11) if cols[(i-1)%5].checkbox(str(i), key=f"sel_{i}")]
    
    if not selected:
        st.info("ℹ️ Επίλεξε αριθμούς!")
    else:
        if st.button("🚀 ΞΕΚΙΝΑΜΕ!", type="primary"):
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
                    style, content = "card-matched", f'<div>{card["content"]}</div>'
                elif is_flipped:
                    style = "card-question" if card['type'] == 'q' else "card-answer"
                    content = f'<div>{card["content"]}</div>'
                else:
                    style, content = "card-closed", '<div class="brain-text">BRAIN<br>GAME</div>'

                with cols[col]:
                    st.markdown(f'<div class="big-card {style}">{content}</div>', unsafe_allow_html=True)
                    btn_label = "ΚΛΙΚ" if not is_flipped else "---"
                    if st.button(btn_label, key=f"btn_{idx}", disabled=is_flipped or len(st.session_state.flipped_indices) >= 2, use_container_width=True):
                        st.session_state.flipped_indices.append(idx)
                        st.rerun()

        if len(st.session_state.flipped_indices) == 2:
            st.session_state.attempts += 1
            i1, i2 = st.session_state.flipped_indices
            if st.session_state.deck[i1]['value'] == st.session_state.deck[i2]['value'] and st.session_state.deck[i1]['type'] != st.session_state.deck[i2]['type']:
                st.session_state.matched_indices.extend([i1, i2])
                st.session_state.flipped_indices = []
                st.rerun()
            else:
                time.sleep(1.0)
                st.session_state.flipped_indices = []
                st.rerun()
    else:
        st.balloons()
        st.markdown(f"""
            <div class="finish-box">
                <h1 style='font-size: 40px;'>🎉 ΤΕΛΟΣ!</h1>
                <p style='font-size: 25px;'>Χρόνος: {format_time(elapsed)}<br>Προσπάθειες: {st.session_state.attempts}</p>
            </div>
        """, unsafe_allow_html=True)
        
        if st.button("🔄 ΠΑΙΞΕ ΞΑΝΑ", type="primary"):
            st.session_state.game_running = False
            st.rerun()
