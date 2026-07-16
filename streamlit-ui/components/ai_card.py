import streamlit as st


CARD_HTML = """
<div style="background:#E8F5E9;padding:20px;border-radius:15px;border-left:8px solid #4CAF50;margin-bottom:20px;">
<h2>🤖 AI Recommendation</h2>
</div>
"""


def render(recommendation):
    st.markdown(CARD_HTML, unsafe_allow_html=True)
    st.success(recommendation)