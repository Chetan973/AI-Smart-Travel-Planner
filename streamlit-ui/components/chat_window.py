import streamlit as st


def show_chat():
    """Render the chat transcript and return one new user message, if any."""
    if "messages" not in st.session_state:
        st.session_state.messages = [
            {
                "role": "assistant",
                "content": (
                    "Hi! I’m your AI travel planner. Tell me where you would like "
                    "to go, or say ‘I want to book a trip’."
                ),
            }
        ]

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    prompt = st.chat_input("Ask me anything..." \
                        "Examples" \
                        "• Book Bangalore → Delhi tomorrow" \
                        "• Cheapest train to Mysore" \
                        "• Weekend trip to Goa" \
                        "• Find hotels in Ooty")
    if prompt:
        st.session_state.messages.append({"role": "user", "content": prompt})
    return prompt
