import streamlit as st
import random

# =========================
# APP TITLE
# =========================

st.set_page_config(page_title="Fault Finding Game", layout="centered")

st.title("🎮 Fault Finding Game")
st.write("Find the fault in electrical / logic situations and test your skills ⚡")

# =========================
# QUESTIONS DATABASE
# =========================

questions = [
    {
        "question": "A circuit has no output voltage. What is the most likely fault?",
        "options": ["Open circuit", "Short circuit", "High resistance load", "Wrong color wire"],
        "answer": "Open circuit"
    },
    {
        "question": "A voltage divider output is 0V. What is the possible issue?",
        "options": ["R1 broken", "R2 shorted to ground", "Both resistors fine", "Battery overcharged"],
        "answer": "R1 broken"
    },
    {
        "question": "LED is not glowing in a simple circuit. What is likely fault?",
        "options": ["Wrong polarity", "Too bright LED", "High voltage only", "Extra resistor missing"],
        "answer": "Wrong polarity"
    },
    {
        "question": "Motor is not spinning even with power ON. Reason?",
        "options": ["Loose connection", "High RPM", "Extra voltage", "Good wiring"],
        "answer": "Loose connection"
    },
    {
        "question": "Sensor is giving constant 0 reading. Fault?",
        "options": ["Sensor disconnected", "Perfect calibration", "Extra power", "High accuracy"],
        "answer": "Sensor disconnected"
    }
]

# =========================
# SESSION STATE
# =========================

if "score" not in st.session_state:
    st.session_state.score = 0

if "current_q" not in st.session_state:
    st.session_state.current_q = random.choice(questions)

# =========================
# SHOW QUESTION
# =========================

q = st.session_state.current_q

st.subheader("🧠 Question:")
st.write(q["question"])

choice = st.radio("Select correct fault:", q["options"])

# =========================
# CHECK ANSWER
# =========================

if st.button("✅ Submit Answer"):

    if choice == q["answer"]:
        st.success("🎉 Correct! You found the fault.")
        st.session_state.score += 1
    else:
        st.error(f"❌ Wrong! Correct answer is: {q['answer']}")

# =========================
# NEXT QUESTION
# =========================

if st.button("➡ Next Question"):
    st.session_state.current_q = random.choice(questions)
    st.rerun()

# =========================
# SCORE DISPLAY
# =========================

st.markdown("---")
st.subheader(f"🏆 Score: {st.session_state.score}")
