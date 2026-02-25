import streamlit as st
from chat_logic import model
import os
import re

st.set_page_config(page_title="SRH Assist", layout="wide")

with st.sidebar:
    st.header("Controls")
    if st.button("Clear conversation"):
        st.session_state.messages = []
        st.rerun()



st.title("SRH Assist")
st.caption("Educational information on sexual & reproductive health • Not medical advice")

DISCLAIMER = """
**Important**: I am **not** a doctor or healthcare provider.  
All information here is general and educational only — **not** a substitute for professional medical advice, diagnosis, or treatment.  
For personal concerns, please speak to a qualified healthcare professional or trusted clinic.
"""

st.info(DISCLAIMER, icon="⚠️")

# ── Session state for chat history ──
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Hello! I'm here to provide factual, educational information about sexual and reproductive health topics such as puberty, periods, contraception, STIs, consent, and more.\n\n" + DISCLAIMER}
    ]
print(os.getenv("GEMINI_API_KEY"))

# Display chat history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# quick‑ask topic buttons below the chat history
cols   = st.columns(3)
topics = [
    "Puberty & body changes",
    "Menstrual health",
    "Contraception options",
]
for col, topic in zip(cols, topics):
    if col.button(topic):
        st.session_state.messages.append(
            {
                "role": "user",
                "content": f"Tell me educational facts about {topic.lower()}.",
            }
        )
        st.rerun()

# User input
if prompt := st.chat_input("Ask a question about sexual and reproductive health…"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        
        with st.spinner("Thinking…"):
            # basic blacklist to catch explicit follow‑ups
            unsafe = [r"sex toy", r"porn", r"fuck", r"explicit"]
            if any(re.search(rf"\b{k}\b", prompt, re.I) for k in unsafe):
                full_response = (
                    "Sorry, I can't engage on that topic. "
                    "Let's keep questions educational and age‑appropriate."
                )
            else:
                chat = model.start_chat(history=[
                    {"role": m["role"], "parts": [m["content"]]}
                    for m in st.session_state.messages[:-1]
                ])
                try:
                    response = chat.send_message(prompt, stream=False)
                    full_response = response.text
                except Exception as e:
                    full_response = f"Sorry, I encountered an issue: {e}\nPlease try rephrasing or ask another question."
        st.markdown(full_response)

    st.session_state.messages.append({"role": "assistant", "content": full_response})
