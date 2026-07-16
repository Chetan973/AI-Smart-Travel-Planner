import streamlit as st


def render(option):

    with st.container(border=True):

        col1, col2 = st.columns([5, 2])

        with col1:

            st.subheader(option["transport_name"])
            st.caption(option["transport_number"])
            st.write(f"📍 {option['source']} ➜ {option['destination']}")
            st.write(f"🕐 {option['departure_time']} → {option['arrival_time']}")
            st.write(f"⏳ Duration : {option['duration']}")
            st.write(f"⭐ Rating : {option['rating']}")
            st.write("💺 Seats : " + str(option["available_seats"]))
            st.write("✨ " + " | ".join(option["amenities"]))

        with col2:
            price_html = (
                '<div style="text-align:center;padding-top:20px;">'
                f'<h2 style="color:#2E7D32">₹ {option["price"]}</h2>'
                '</div>'
            )
            st.markdown(price_html, unsafe_allow_html=True)

            booked = st.button(
                "🚀 Book Now",
                key=f"book_{option['option_id']}",
                use_container_width=True,
            )

    return booked