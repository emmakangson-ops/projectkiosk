import streamlit as st


def render():

    st.title("멤버십 적립")

    c1, c2 = st.columns(2)

    with c1:

        if st.button(
            "적립 안함",
            use_container_width=True
        ):

            st.session_state.member_id = None

            st.session_state.page = "payment"


            st.rerun()

    with c2:

        if st.button(
            "적립하기",
            use_container_width=True
        ):

            st.session_state.page = "phone"

            st.rerun()