import streamlit as st
import time


def reset_session():

    st.session_state.page = "waiting"

    st.session_state.cart = []

    st.session_state.order_type = ""

    st.session_state.selected_menu = None

    st.session_state.order_id = None

    st.session_state.phone = ""

    st.session_state.payment = ""


def render():

    st.success("주문이 완료되었습니다.")

    st.markdown(
        f"""
        ## 주문번호

        # A-{st.session_state.order_id}
        """
    )

    countdown_text = st.empty()

    progress = st.progress(0)

    for sec in range(10, 0, -1):

        countdown_text.info(
            f"{sec}초 후 초기 화면으로 이동합니다."
        )

        progress.progress(
            (11 - sec) * 10
        )

        time.sleep(1)

    reset_session()

    st.rerun()