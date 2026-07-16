import streamlit as st


HERO_HTML = """
<style>
.hero{
background: linear-gradient(135deg,#0F2027,#203A43,#2C5364);
border-radius:20px;
padding:45px;
color:white;
text-align:center;
box-shadow:0 8px 25px rgba(0,0,0,.25);
margin-bottom:25px;
}
.hero h1{
font-size:42px;
font-weight:700;
}
.hero h3{
color:#A5D6FF;
}
.feature{
display:inline-block;
background:#ffffff22;
padding:10px 18px;
margin:8px;
border-radius:30px;
font-size:16px;
}
</style>

<div class="hero">
<h1>🌍 AI Smart Travel Planner</h1>
<h3>Multi-Agent Travel Planning & Booking System</h3>
<br>
<span class="feature">✈ Flights</span>
<span class="feature">🚆 Trains</span>
<span class="feature">🏨 Hotels</span>
<span class="feature">🌤 Weather</span>
<span class="feature">🤖 Gemini AI</span>
<span class="feature">🧠 LangGraph</span>
<span class="feature">💳 Razorpay</span>
</div>
"""


def hero():
    st.markdown(HERO_HTML, unsafe_allow_html=True)