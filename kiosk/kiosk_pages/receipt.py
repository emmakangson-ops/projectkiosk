import streamlit as st


def render():
    if "grade_upgrade_msg" in st.session_state:
        st.success(st.session_state.grade_upgrade_msg)
        del st.session_state.grade_upgrade_msg

    if "receipt_print" not in st.session_state:
        st.session_state.receipt_print = False

    if not st.session_state.receipt_print:

        st.title("🧾 영수증 발행")
        st.write("영수증을 발행하시겠습니까?")

        c1, c2 = st.columns(2)

        with c1:

            if st.button(
                "예",
                use_container_width=True
            ):

                st.session_state.receipt_print = True
                st.rerun()

                st.session_state.receipt_print = False
                st.session_state.page = "complete"

                st.rerun()

            

        with c2:

            if st.button(
                "발행 안함",
                use_container_width=True
            ):

                st.session_state.page = "complete"
                st.rerun()
    else:
            
        total_amount = sum(
            item["price"]
            for item in st.session_state.cart
        )

        discount = st.session_state.get(
            "discount",
            0
        )

        grade_discount = st.session_state.get(
            "grade_discount",
            0
        )

        total_discount = st.session_state.get(
            "total_discount",
            discount
        )

        grade = st.session_state.get(
            "grade",
            "비회원"
        )



        final_amount = st.session_state.get(
            "final_amount",
            total_amount
        )



        # 영수증 미리보기
        with st.container(border=True):

            st.markdown("### 4️⃣ NET CAFE")

            st.write(
                f"주문번호 : A-{st.session_state.order_id}"
            )

            st.write(
                f"주문유형 : {st.session_state.order_type}"
            )

            st.write(
                f"결제수단 : {st.session_state.payment}"
            )

            st.markdown("---")

            for item in st.session_state.cart:

                st.write(
                    f"{item['menu_name']}  {item['price']:,}원"
                )

                for op in item["options"]:
                    st.write(
                        f" └ {op['option_name']}"
                    )

            st.markdown("---")

            st.write(
                f"주문금액 : {total_amount:,}원"
            )
            
            if grade != "비회원":
                st.write(f"회원등급 : {grade}")

            st.write(
                f"등급할인 : {grade_discount:,}원"
            )

            st.write(
                f"쿠폰할인 : {discount:,}원"
            )

            st.write(
                f"총 할인금액 : {total_discount:,}원"
            )


            st.write(
                f"결제금액 : {final_amount:,}원"
            )


            st.markdown("---")
            st.write("이용해주셔서 감사합니다 ☕")

        if st.button("확인", use_container_width=True):

            st.session_state.receipt_print = False
            st.session_state.page = "complete"
            st.rerun()
        