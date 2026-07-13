import uuid
import streamlit as st
from db.database import get_cursor
from utils.cookies import cookie_manager


def render():

    st.title("관리자 로그인")

    admin_name = st.text_input(
        "아이디"
    )

    password = st.text_input(
        "비밀번호",
        type="password"
    )

    col1, col2 = st.columns(2)

    with col1:

        if st.button("로그인"):

            conn, cursor = get_cursor()

            cursor.execute("""
                SELECT *
                FROM admin
                WHERE admin_name = %s
                AND admin_pw = %s
            """, (
                admin_name,
                password
            ))

            admin = cursor.fetchone()

            if admin:
                
                # 토큰값에 하이픈(-)제거 
                token = str(uuid.uuid4().hex)

                cursor.execute("""
                    UPDATE admin
                    SET login_token = %s
                    WHERE admin_id = %s
                """, (
                    token,
                    admin["admin_id"]
                ))

                conn.commit()

                cookie_manager.set(
                    "token",
                    token
                )

                conn.close()

                st.session_state.is_admin = True
                st.session_state.page = "admin_dashboard"

                st.rerun()

            else:

                conn.close()

                st.error(
                    "아이디 또는 비밀번호가 틀렸습니다."
                )

    with col2:

        if st.button("취소"):

            st.session_state.page = "waiting"
            st.rerun()