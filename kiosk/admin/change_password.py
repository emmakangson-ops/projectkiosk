import streamlit as st
from db.database import get_cursor
from utils.cookies import cookie_manager


def render():

    if not st.session_state.get("is_admin", False):
        st.error("접근 권한이 없습니다.")
        return

    st.title("비밀번호 변경")

    current_pw = st.text_input(
        "현재 비밀번호",
        type="password"
    )

    new_pw = st.text_input(
        "새 비밀번호",
        type="password"
    )

    confirm_pw = st.text_input(
        "새 비밀번호 확인",
        type="password"
    )

    col1, col2 = st.columns(2)

    with col1:

        if st.button("변경"):

            if new_pw != confirm_pw:
                st.error("새 비밀번호가 일치하지 않습니다.")
                return

            conn, cursor = get_cursor()

            token = cookie_manager.get("token")

            cursor.execute("""
            SELECT admin_id, admin_pw
            FROM admin
            WHERE login_token=%s
            """,(token,))

            admin = cursor.fetchone()

            if not admin:
                st.error("관리자 정보를 찾을 수 없습니다.")
                return

            if current_pw != admin["admin_pw"]:
                st.error("현재 비밀번호가 일치하지 않습니다.")
                return

            cursor.execute("""
            UPDATE admin
            SET admin_pw=%s
            WHERE admin_id=%s
            """,(
                new_pw,
                admin["admin_id"]
            ))

            conn.commit()

            cursor.close()
            conn.close()

            st.success("비밀번호가 변경되었습니다.")

    with col2:

        if st.button("취소"):
            st.session_state.page = "admin_dashboard"
            st.rerun()


    st.divider()
    
    if st.button("뒤로가기"):

        st.session_state.page = (
            "admin_dashboard"
        )

        st.rerun()            