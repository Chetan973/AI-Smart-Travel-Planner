# streamlit-ui/streamlit_app.py
import uuid
import streamlit as st
from components.hero import hero
from components.navbar import show
from services.api_client import APIClient

st.set_page_config(page_title="AI Smart Travel Planner", page_icon="✈️", layout="wide")

if "session_id" not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())
if "messages" not in st.session_state:
    st.session_state.messages = []

show()

with st.sidebar:
    st.markdown("### ⚙️ Session Controls")
    if st.button("🔄 Start New Booking", type="primary", use_container_width=True):
        st.session_state.session_id = str(uuid.uuid4())
        st.session_state.messages = []
        st.rerun()

hero()
st.markdown("## AI Travel Assistant")

# Render chat history with HTML enabled for buttons
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"], unsafe_allow_html=True)

prompt = st.chat_input("Ask me anything, e.g., 'Book a train from Bangalore to Delhi tomorrow under 1500'")

if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
        
    with st.spinner("Processing..."):
        try:
            reply = APIClient.send_chat_message(st.session_state.session_id, prompt)
            ai_text = reply.get("ai_response", "Error processing request.")
        except Exception as exc:
            ai_text = f"Backend Connection Error: {exc}"

    st.session_state.messages.append({"role": "assistant", "content": ai_text})
    with st.chat_message("assistant"):
        st.markdown(ai_text, unsafe_allow_html=True)
        
    st.rerun()