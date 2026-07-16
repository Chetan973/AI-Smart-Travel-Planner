import streamlit as st


TITLE_HTML = """
<div style="text-align:center;font-size:32px;font-weight:700;color:#1565C0;">
Smart AI Travel Planner
</div>
<div style="text-align:center;color:gray;">
Powered by Gemini • LangGraph • FastAPI
</div>
"""

RIGHT_HTML = """
<div style="text-align:right;font-size:18px;">
🔔 &nbsp;&nbsp; 👤 Chetan
</div>
"""


def show():
    col1, col2, col3 = st.columns([2, 6, 2])

    with col1:
        st.markdown("# ✈ AI Travel")

    with col2:
        st.markdown(TITLE_HTML, unsafe_allow_html=True)

    with col3:
        st.markdown(RIGHT_HTML, unsafe_allow_html=True)

    st.divider()