import streamlit as st


def render():

    if st.button("←"):
        st.session_state.page = "menu"
        st.rerun()

    st.title("주문 내역")
    if len(st.session_state.cart) == 0:
        st.info("장바구니가 비어 있습니다.")

        if st.button("메뉴 선택"):
            st.session_state.page = "menu"
            st.rerun()

        return

    total = 0

    for idx, item in enumerate(
        st.session_state.cart
    ):

        with st.container():
            col1, col2, col3 = st.columns(
                [4, 2, 1]
            )

            with col1:
                st.write(
                    item["menu_name"]
                )
                if item["options"]:
                    option_names = [
                        op["option_name"]
                        for op in item["options"]
                    ]
                    st.caption(
                        ", ".join(option_names)
                    )
            with col2:
                st.write(
                    f"{item['price']:,}원"
                )
            with col3:
                if st.button(
                    "삭제",
                    key=f"delete_{idx}"
                ):
                    st.session_state.cart.pop(
                        idx
                    )
                    st.rerun()

        total += item["price"]

    st.divider()
    st.subheader(
        f"총 금액 : {total:,}원"
    )

    col1, col2 = st.columns(2)

    with col1:

        if st.button(
            "메뉴 추가",
            use_container_width=True
        ):

            st.session_state.page = "menu"
            st.rerun()

    with col2:

        if st.button(
            "결제하기",
            use_container_width=True
        ):

            st.session_state.page = "membership"
            st.rerun() 