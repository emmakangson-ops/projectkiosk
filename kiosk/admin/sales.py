import streamlit as st
from db.database import get_cursor
import pandas as pd


def render():
    conn, cursor = get_cursor()
    st.title("📊 매출 통계")

    tab_day, tab_month, tab_year, tab_search = st.tabs([
    "일별",
    "월별",
    "연도별",
    "기간검색"
    ])
    with tab_day:

        cursor.execute("""
            SELECT
                DATE(order_date) AS day,
                SUM(total_amount) AS sales,
                COUNT(*) AS orders
            FROM orders
            GROUP BY DATE(order_date)
            ORDER BY day DESC
        """)

        day_sales = cursor.fetchall()
        df = pd.DataFrame(day_sales)

        df.columns = [
            "날짜",
            "매출액",
            "주문수"
        ]
        df["매출액"] = df["매출액"].apply(
            lambda x: f"{int(x or 0):,}원"
        )
        st.dataframe(
            df,
            width='stretch'
        )

    with tab_month:

        cursor.execute("""
            SELECT
                DATE_FORMAT(order_date, '%Y-%m') AS month,
                SUM(total_amount) AS sales,
                COUNT(*) AS orders
            FROM orders
            GROUP BY DATE_FORMAT(order_date, '%Y-%m')
            ORDER BY month DESC
        """)

        month_sales = cursor.fetchall()
        df = pd.DataFrame(month_sales)
        df.columns = [
            "월",
            "매출액",
            "주문수"
        ]

        df["매출액"] = df["매출액"].apply(
            lambda x: f"{int(x or 0):,}원"
        )


        st.dataframe(
            df,
            width='stretch'
        )

    with tab_year:

        cursor.execute("""
            SELECT
                YEAR(order_date) AS year,
                SUM(total_amount) AS sales,
                COUNT(*) AS orders
            FROM orders
            GROUP BY YEAR(order_date)
            ORDER BY year DESC
        """)

        year_sales = cursor.fetchall()
        df = pd.DataFrame(year_sales)
        df.columns = [
            "연도",
            "매출액",
            "주문수"
        ]

        df["매출액"] = df["매출액"].apply(
            lambda x: f"{int(x or 0):,}원"
        )
        
        st.dataframe(
            df,
            width='stretch'
        )

    with tab_search:

        st.subheader("기간별 매출 조회")

        start_date = st.date_input(
            "시작일"
        )

        end_date = st.date_input(
            "종료일"
        )
        
        
        if st.button("검색"):   

            # 총 매출
            cursor.execute("""
                SELECT
                        SUM(total_amount) AS sales,
                        COUNT(*) AS orders
                    FROM orders
                    WHERE DATE(order_date)
                        BETWEEN %s AND %s
            """, (start_date, end_date))

            result = cursor.fetchone()

            col1, col2 = st.columns(2)

            with col1:
                st.metric(
                    "총매출",
                    f"{int(result['sales'] or 0):,}원"
                )

            with col2:
                st.metric(
                    "주문수",
                    result['orders']
                )


            cursor.execute("""
                SELECT
                    c.category_name,
                    SUM(od.amount) AS sales
                FROM order_detail od

                JOIN menu m
                    ON od.menu_id = m.menu_id

                JOIN category c
                    ON m.category_code = c.category_code

                JOIN orders o
                    ON od.order_id = o.order_id

                WHERE DATE(o.order_date)
                    BETWEEN %s AND %s

                GROUP BY c.category_name
                ORDER BY sales DESC
            """,(start_date,end_date))
            category_sales = cursor.fetchall()

            if category_sales:
                df = pd.DataFrame(category_sales)
                df.columns = ["카테고리", "매출액"]

                df["매출액"] = df["매출액"].apply(
                    lambda x: f"{int(x or 0):,}원"
                )

                st.subheader("카테고리별 매출") 

                st.dataframe(
                    df,
                    width='stretch'
                )
            else:
                st.info("조회된 카테고리 매출이 없습니다.")




        # 메뉴별 판매량
            cursor.execute("""
                SELECT
                    m.menu_name,
                    SUM(od.quantity) AS qty,
                    SUM(od.amount) AS sales
                FROM order_detail od

                JOIN menu m
                    ON od.menu_id = m.menu_id

                JOIN orders o
                    ON od.order_id = o.order_id

                WHERE DATE(o.order_date)
                    BETWEEN %s AND %s

                GROUP BY m.menu_name
                ORDER BY qty DESC
            """,(start_date,end_date))

            menu_sales = cursor.fetchall()

            if menu_sales:
                df = pd.DataFrame(menu_sales)
                df.columns = ["메뉴", "판매수량", "매출액"]

                df["매출액"] = df["매출액"].apply(
                    lambda x: f"{int(x or 0):,}원"
                )

                st.subheader(
                    "메뉴별 판매 현황"
                )
            
                st.dataframe(
                    df,
                    width='stretch'
                )
            else:
                st.info("조회된 메뉴 판매 내역이 없습니다.")


        # 인기 메뉴 TOP 5
        cursor.execute("""
            SELECT
                m.menu_name,
                SUM(od.quantity) AS total_qty
            FROM order_detail od
            JOIN menu m
                ON od.menu_id = m.menu_id
            GROUP BY m.menu_name
            ORDER BY total_qty DESC
            LIMIT 5
        """)

        top_menus = cursor.fetchall()



        st.subheader("🔥 인기 메뉴 TOP 5")

        for idx, menu in enumerate(top_menus, start=1):

            st.write(
                f"{idx}. {menu['menu_name']} "
                f"({menu['total_qty']}개)"
            )

        st.divider()

    if st.button("뒤로가기"):
        st.session_state.page = "admin_dashboard"
        st.rerun()

    conn.close()
