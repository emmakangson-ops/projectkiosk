import streamlit as st


def render():

    st.title("이용 방법 선택")

    c1, c2 = st.columns(2)

    with c1:

        if st.button(
            "매장",
            use_container_width=True
        ):
            st.session_state.order_type = "매장"
            st.session_state.page = "menu"
            st.rerun()

    with c2:

        if st.button(
            "포장",
            use_container_width=True
        ):
            st.session_state.order_type = "포장"
            st.session_state.page = "menu"
            st.rerun()