import streamlit as st
from db.database import get_cursor
import pandas as pd


def render():

    conn = None
    cursor = None

    try:
        conn, cursor = get_cursor()

        st.title("👤 회원 관리")

        # ==============================
        # 총 회원 수
        # ==============================
        cursor.execute("""
            SELECT COUNT(*) AS cnt
            FROM member
        """)

        result = cursor.fetchone()
        total = result["cnt"] if isinstance(result, dict) else result[0]

        st.metric("총 회원 수", total)

        st.divider()

        # ==============================
        # 회원 목록
        # ==============================
        cursor.execute("""
            SELECT
                member_id,
                phone_number,
                grade,
                stamp,
                coupon_count
            FROM member
            ORDER BY member_id DESC
        """)

        members = cursor.fetchall()

        if members:

            df = pd.DataFrame(members)

            df.columns = [
                "회원번호",
                "전화번호",
                "등급",
                "스탬프",
                "쿠폰"
            ]

            st.subheader("회원 목록")

            st.dataframe(
                df,
                width='stretch',
                hide_index=True
            )

        else:
            st.info("등록된 회원이 없습니다.")

        st.divider()

        # ==============================
        # 회원 검색
        # ==============================
        st.subheader("🔍 회원 검색")

        phone = st.text_input(
            "전화번호 입력",
            placeholder="01012345678"
        )

        if st.button("검색"):

            cursor.execute("""
                SELECT
                    member_id,
                    phone_number,
                    grade,
                    stamp,
                    coupon_count
                FROM member
                WHERE phone_number=%s
            """, (phone,))

            member = cursor.fetchone()

            if member is None:
                st.warning("회원을 찾을 수 없습니다.")

            else:

                member_id = member["member_id"] if isinstance(member, dict) else member[0]
                phone_number = member["phone_number"] if isinstance(member, dict) else member[1]
                grade = member["grade"] if isinstance(member, dict) else member[2]
                stamp = member["stamp"] if isinstance(member, dict) else member[3]
                coupon = member["coupon_count"] if isinstance(member, dict) else member[4]

                st.success("회원 정보")

                c1, c2, c3 = st.columns(3)

                with c1:
                    st.metric("등급", grade if grade else "-")

                with c2:
                    st.metric("스탬프", stamp)

                with c3:
                    st.metric("쿠폰", coupon)

                st.write(f"**회원번호** : {member_id}")
                st.write(f"**전화번호** : {phone_number}")

                st.divider()

                # ==============================
                # 결제 내역
                # ==============================
                cursor.execute("""
                    SELECT
                        pay_date,
                        pay_type,
                        final_amt
                    FROM payment
                    WHERE member_id=%s
                    ORDER BY pay_date DESC
                """, (member_id,))

                payments = cursor.fetchall()

                st.subheader("📄 결제 내역")

                if payments:

                    pay_df = pd.DataFrame(payments)

                    pay_df.columns = [
                        "결제일",
                        "결제수단",
                        "결제금액"
                    ]

                    pay_df["결제금액"] = pay_df["결제금액"].astype(int)
                    pay_df["결제금액"] = pay_df["결제금액"].apply(
                        lambda x: f"{x:,}원"
                    )

                    st.dataframe(
                        pay_df,
                        width='stretch',
                        hide_index=True
                    )

                else:
                    st.info("결제 내역이 없습니다.")

        st.divider()

        if st.button("뒤로가기"):

            st.session_state.page = "admin_dashboard"
            st.rerun()

    except Exception as e:
        st.error(f"오류가 발생했습니다.\n{e}")

    finally:

        if cursor:
            cursor.close()

        if conn:
            conn.close()