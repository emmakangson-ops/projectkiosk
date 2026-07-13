import streamlit as st
import pandas as pd
from db.database import get_cursor


def render():

    st.title("카테고리 관리")

    conn, cursor = get_cursor()

    # ------------------------
    # 카테고리 조회
    # ------------------------
    cursor.execute("""
        SELECT
            category_code,
            category_name
        FROM category
        ORDER BY category_code
    """)

    categories = cursor.fetchall()

    st.subheader("현재 카테고리")

    df = pd.DataFrame(categories)

    edited_df = st.data_editor(
        df,
        hide_index=True,
        width="stretch",
        disabled=["category_code"],
        column_config={
            "category_code": st.column_config.NumberColumn(
                "번호",
                disabled=True
            ),
            "category_name": st.column_config.TextColumn(
                "카테고리명"
            )
        }
    )

    # ------------------------
    # 수정
    # ------------------------
    if st.button("수정사항 저장"):

        try:

            for _, row in edited_df.iterrows():

                cursor.execute("""
                    UPDATE category
                    SET category_name=%s
                    WHERE category_code=%s
                """, (
                    row["category_name"],
                    row["category_code"]
                ))

            conn.commit()

            st.success("카테고리가 수정되었습니다.")
            st.rerun()

        except Exception as e:

            conn.rollback()
            st.error(e)

    st.divider()

    # ------------------------
    # 카테고리 추가
    # ------------------------
    st.subheader("카테고리 추가")

    new_category = st.text_input("카테고리명")

    if st.button("카테고리 추가"):

        if new_category.strip() == "":
            st.warning("카테고리명을 입력하세요.")

        else:

            try:

                # 중복 확인
                cursor.execute("""
                    SELECT COUNT(*) AS cnt
                    FROM category
                    WHERE category_name=%s
                """, (new_category,))

                result = cursor.fetchone()

                cnt = result["cnt"] if isinstance(result, dict) else result[0]

                if cnt > 0:
                    st.error("이미 존재하는 카테고리입니다.")

                else:

                    cursor.execute("""
                        INSERT INTO category
                        (
                            category_name
                        )
                        VALUES
                        (%s)
                    """, (new_category,))

                    conn.commit()

                    st.success("카테고리가 추가되었습니다.")
                    st.rerun()

            except Exception as e:

                conn.rollback()
                st.error(e)

    st.divider()

    # ------------------------
    # 카테고리 삭제
    # ------------------------
    st.subheader("카테고리 삭제")

    if categories:

        category_map = {
            f"{row['category_code']} - {row['category_name']}":
            row["category_code"]
            for row in categories
        }

        selected_category = st.selectbox(
            "삭제할 카테고리",
            list(category_map.keys())
        )

        if st.button("카테고리 삭제"):

            category_code = category_map[selected_category]

            try:

                # 해당 카테고리를 사용하는 메뉴가 있는지 확인
                cursor.execute("""
                    SELECT COUNT(*) AS cnt
                    FROM menu
                    WHERE category_code=%s
                """, (category_code,))

                result = cursor.fetchone()
                cnt = result["cnt"] if isinstance(result, dict) else result[0]

                if cnt > 0:

                    st.error(
                        "이 카테고리를 사용하는 메뉴가 있어 삭제할 수 없습니다."
                    )

                else:

                    cursor.execute("""
                        DELETE FROM category
                        WHERE category_code=%s
                    """, (category_code,))

                    conn.commit()

                    st.success("카테고리가 삭제되었습니다.")
                    st.rerun()

            except Exception as e:

                conn.rollback()
                st.error(e)

    else:

        st.info("삭제할 카테고리가 없습니다.")

    # ------------------------
    # 뒤로가기
    # ------------------------
    if st.button("뒤로가기"):

        st.session_state.page = "admin_dashboard"
        st.rerun()

    conn.close()