import streamlit as st
from db.database import get_cursor
from utils.cookies import cookie_manager


def render():

    if not st.session_state.get("is_admin", False):
        st.error("접근 권한이 없습니다.")
        return

    st.title("관리자 페이지")

    col1, col2 = st.columns([8, 2])

    with col2:
        if st.button("🔑 비밀번호 변경"):
            st.session_state.page = "change_password"
            st.rerun()

    st.subheader("관리 메뉴")

    # 버튼 4개로 변경
    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        if st.button("메뉴 관리"):
            st.session_state.page = "menu_manage"
            st.rerun()

    with col2:
        if st.button("옵션 관리"):
            st.session_state.page = "option_manage"
            st.rerun()

    with col3:
        if st.button("카테고리 관리"):
            st.session_state.page = "category_manage"
            st.rerun()

    with col4:
        if st.button("매출 통계"):
            st.session_state.page = "sales"
            st.rerun()

    with col5:
        if st.button("회원 관리"):
            st.session_state.page = "member_manage"
            st.rerun()

    st.divider()

    if st.button("로그아웃"):

        token = cookie_manager.get("token")

        if token:

            conn, cursor = get_cursor()

            # admin 로그아웃 시 token 삭제
            cursor.execute("""
                UPDATE admin
                SET login_token = NULL
                WHERE login_token = %s
            """, (token,))

            conn.commit()
            conn.close()

        cookie_manager.delete("token")

        st.session_state.is_admin = False
        st.session_state.page = "waiting"

        st.rerun()