import streamlit as st
from db.database import get_cursor
import time

def add_digit(num):
    phone_digits = st.session_state.get("phone_digits", "")
    if len(phone_digits) < 11:
        st.session_state.phone_digits = phone_digits + str(num)

def backspace():
    phone_digits = st.session_state.get("phone_digits", "")
    st.session_state.phone_digits = phone_digits[:-1]

def clear():
    st.session_state.phone_digits = "010"
    
def render():
    if "phone_digits" not in st.session_state:
        st.session_state.phone_digits = "010"
        
    conn, cursor = get_cursor()
    st.title("휴대폰 번호 입력")

    digits = st.session_state.get("phone_digits", "")

    phone_number = digits
    if len(digits) <= 3:
        phone = digits
    elif len(digits) <= 7:
        phone = f"{digits[:3]}-{digits[3:]}"
    else:
        phone = f"{digits[:3]}-{digits[3:7]}-{digits[7:]}"

    st.markdown(
        f"""
        <div style="
            font-size:40px;
            text-align:center;
            border:2px solid gray;
            border-radius:10px;
            padding:20px;
            margin-bottom:30px;
        ">
        {phone}
        </div>
        """,
        unsafe_allow_html=True
    )

    ## 키패드
    buttons = [
    ["1","2","3"],
    ["4","5","6"],
    ["7","8","9"],
    ["←","0","C"]
    ]

    for row in buttons:
        cols = st.columns(3)
        for i, value in enumerate(row):
            with cols[i]:
                if value == "←":
                    st.button(value,
                            use_container_width=True,
                            on_click=backspace)

                elif value == "C":
                    st.button(value,
                            use_container_width=True,
                            on_click=clear)

                else:
                    st.button(value,
                            use_container_width=True,
                            on_click=add_digit,
                            args=(value,))

    if st.button("적립하기", use_container_width=True, type="primary"):

        conn, cursor = get_cursor()

        cursor.execute("""
        SELECT member_id
        FROM member
        WHERE phone_number=%s
        """,(phone_number,))

        member = cursor.fetchone()


        # 이미 회원이면
        if member:
            st.info(f"📱 {phone} 번호로 적립되었습니다.")
            time.sleep(1)

            member_id = member["member_id"]
            st.session_state.member_id = member_id

            # 스탬프 +1
            cursor.execute("""
            UPDATE member
            SET stamp = stamp + 1
            WHERE member_id = %s
            """,(member["member_id"],))

            # 현재 스탬프 조회
            cursor.execute("""
            SELECT stamp
            FROM member
            WHERE member_id=%s
            """,(member["member_id"],))

            stamp = cursor.fetchone()["stamp"]

            # 10개 모이면 쿠폰 생성
            if stamp >= 10:

                cursor.execute("""
                UPDATE member
                SET
                    stamp = stamp - 10,
                    coupon_count = coupon_count + 1
                WHERE member_id=%s
                """,(member["member_id"],))

                st.success("🎉 쿠폰 1장이 발급되었습니다!")
                time.sleep(1)

            
            st.session_state.phone_digits = "010"
            st.session_state.phone = phone_number
            st.session_state.page = "payment"

        # 회원 아니면 신규 생성
        else:
            st.info(f"신규 📱 {phone} 번호로 적립되었습니다.")
            time.sleep(1)
            
            cursor.execute("""
            INSERT INTO member(
                phone_number,
                stamp,
                grade
            )
            VALUES(%s,1,'BRONZE')
            """,(phone_number,))

            member_id = cursor.lastrowid
            st.session_state.member_id = member_id

        conn.commit()
        cursor.close()
        conn.close()
        st.session_state.phone_digits = "010"
        st.session_state.phone = phone_number
        st.session_state.page = "payment"
        st.rerun()