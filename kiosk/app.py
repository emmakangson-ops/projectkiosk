from db.database import get_cursor
import streamlit as st
from utils.session import init_session
from utils.cookies import cookie_manager

from kiosk_pages.waiting import render as waiting_page
from kiosk_pages.order_type import render as order_type_page
from kiosk_pages.menu import render as menu_page
from kiosk_pages.option import render as option_page
from kiosk_pages.summary import render as summary_page
from kiosk_pages.payment import render as payment_page
from kiosk_pages.membership import render as membership_page
from kiosk_pages.phone import render as phone_page
from kiosk_pages.receipt import render as receipt_page
from kiosk_pages.complete import render as complete_page
from kiosk_pages.admin_login import render as admin_login_page
from kiosk_pages.admin_dashboard import render as admin_dashboard_page

from admin.menu_manage import render as menu_manage_page
from admin.sales import render as sales_page
from admin.option_manage import render as option_manage_page
from admin.change_password import render as change_password
from admin.category_manage import render as category_manage_page
from admin.member_manage import render as member_manage_page   # 추가

st.set_page_config(
    page_title="키오스크",
    layout="wide"
)

# st.set_page_config(
#     page_title="키오스크",
#     layout="centered"
# )


init_session()

# --------------------------
# 관리자 자동 로그인
# --------------------------

try:

    token = cookie_manager.get("token")

    if token and not st.session_state.is_admin:

        conn, cursor = get_cursor()

        cursor.execute("""
            SELECT *
            FROM admin
            WHERE login_token = %s
        """, (token,))

        admin = cursor.fetchone()

        conn.close()

        if admin:

            st.session_state.is_admin = True

            if st.session_state.page == "waiting":
                st.session_state.page = "admin_dashboard"

except Exception as e:
    print("Cookie Error:", e)

# --------------------------
# 페이지 매핑
# --------------------------

PAGE_MAP = {
    "waiting": waiting_page,
    "order_type": order_type_page,
    "menu": menu_page,
    "option": option_page,
    "summary": summary_page,
    "payment": payment_page,
    "membership": membership_page,
    "phone": phone_page,
    "receipt": receipt_page,
    "complete": complete_page,
    "admin_login": admin_login_page,
    "admin_dashboard": admin_dashboard_page,
    "change_password": change_password,
    "menu_manage": menu_manage_page,
    "sales": sales_page,
    "option_manage": option_manage_page,
    "category_manage": category_manage_page,
    "member_manage": member_manage_page,   # 추가
}

# --------------------------
# 페이지 실행
# --------------------------

current_page = st.session_state.page

if current_page in PAGE_MAP:
    PAGE_MAP[current_page]()
else:
    st.error(f"존재하지 않는 페이지: {current_page}")