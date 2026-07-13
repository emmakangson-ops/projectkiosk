import streamlit as st
def render(): st.write('옵션 페이지')
import streamlit as st
from db.database import get_cursor


def render():

    menu = st.session_state.selected_menu

    if menu is None:

        st.warning("선택된 메뉴가 없습니다.")

        if st.button("메뉴로 이동"):
            st.session_state.page = "menu"
            st.rerun()

        return

    conn, cursor = get_cursor()

    st.title("옵션 선택")

    st.subheader(menu["menu_name"])

    cursor.execute("""
    SELECT
        og.group_name,
        o.option_id,
        o.option_name,
        o.extra_price
    FROM option o
    JOIN option_group og
        ON o.group_id = og.group_id
    JOIN menu_option_group mog
        ON og.group_id = mog.group_id
    WHERE mog.menu_id=%s
    """, (menu["menu_id"],))

    options = cursor.fetchall()

    grouped_options = {}

    for op in options:

        group_name = op["group_name"]

        if group_name not in grouped_options:
            grouped_options[group_name] = []

        grouped_options[group_name].append(op)

    selected_options = []

    total_price = menu["menu_price"]

    for group_name, option_list in grouped_options.items():

        st.subheader(group_name)

        option_names = [
            f"{op['option_name']} (+{op['extra_price']}원)"
            for op in option_list
        ]

        default_idx = 0

        for i, op in enumerate(option_list):
            if op["extra_price"] == 0:
                default_idx = i
                break

        selected = st.radio(
            label=group_name,
            options=option_names,
            key=f"radio_{group_name}",
            index=default_idx
        )

        selected_op = option_list[
            option_names.index(selected)
        ]

        selected_options.append(selected_op)

        total_price += selected_op["extra_price"]

    st.metric(
        "금액",
        f"{total_price:,}원"
    )

    col1, col2 = st.columns(2)

    with col1:

        if st.button("취소"):

            conn.close()

            st.session_state.page = "menu"

            st.rerun()

    with col2:

        if st.button("장바구니 담기"):

            
            st.session_state.cart.append({
                "menu_id": menu["menu_id"],
                "menu_name": menu["menu_name"],
                "price": total_price,
                "options": selected_options
            })

            conn.close()

            st.session_state.page = "menu"

            st.rerun()

    conn.close()