import streamlit as st


def init_session():

    if "page" not in st.session_state:
        st.session_state.page = "waiting"

    if "cart" not in st.session_state:
        st.session_state.cart = []
    

    if "order_type" not in st.session_state:
        st.session_state.order_type = ""

    if "membership" not in st.session_state:
        st.session_state.membership = False

    if "order_id" not in st.session_state:
        st.session_state.order_id = None

    if "selected_menu" not in st.session_state:
        st.session_state.selected_menu = None

    if "phone" not in st.session_state:
        st.session_state.phone = ""

    if "payment" not in st.session_state:
        st.session_state.payment = ""

    if "is_admin" not in st.session_state:
        st.session_state.is_admin = False