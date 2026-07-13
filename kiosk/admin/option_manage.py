import streamlit as st
from db.database import get_cursor
import pandas as pd


def render():

    st.title("옵션 관리")

    conn, cursor = get_cursor()

    # -----------------
    # 옵션 그룹 조회
    # -----------------

    cursor.execute("""
        SELECT *
        FROM option_group
        ORDER BY group_id
    """)

    groups = cursor.fetchall()

    # -----------------
    # 옵션 그룹 관리
    # -----------------

    st.subheader("현재 옵션 그룹")

    group_df = pd.DataFrame(groups)

    edited_group_df = st.data_editor(
        group_df,
        hide_index=True,
        width="stretch",
        disabled=["group_id"],
        column_config={
            "group_id": "번호",
            "group_name": "그룹명"
        }
    )

    if st.button("그룹 수정 저장"):

        try:

            for _, row in edited_group_df.iterrows():

                cursor.execute("""
                    UPDATE option_group
                    SET group_name=%s
                    WHERE group_id=%s
                """, (
                    row["group_name"],
                    row["group_id"]
                ))

            conn.commit()

            st.success("그룹 수정 완료")
            st.rerun()

        except Exception as e:

            conn.rollback()
            st.error(e)

    st.divider()

    # -----------------
    # 옵션 그룹 추가
    # -----------------

    st.subheader("옵션 그룹 추가")

    group_name = st.text_input("그룹명")

    if st.button("그룹 추가"):

        cursor.execute("""
            INSERT INTO option_group
            (
                group_name
            )
            VALUES (%s)
        """, (
            group_name,
        ))

        conn.commit()

        st.success("등록 완료")
        st.rerun()

    # -----------------
    # 옵션 그룹 삭제
    # -----------------

    if groups:

        st.subheader("옵션 그룹 삭제")

        group_delete_map = {
            g["group_name"]: g["group_id"]
            for g in groups
        }

        selected_group_delete = st.selectbox(
            "삭제할 그룹",
            list(group_delete_map.keys())
        )

        if st.button("그룹 삭제"):

            cursor.execute("""
                SELECT COUNT(*) AS cnt
                FROM option
                WHERE group_id=%s
            """, (
                group_delete_map[selected_group_delete],
            ))

            count = cursor.fetchone()["cnt"]

            if count > 0:

                st.error(
                    "해당 그룹에 옵션이 존재하여 삭제할 수 없습니다."
                )

            else:

                cursor.execute("""
                    DELETE FROM option_group
                    WHERE group_id=%s
                """, (
                    group_delete_map[selected_group_delete],
                ))

                conn.commit()

                st.success("삭제 완료")
                st.rerun()

    st.divider()

    # -----------------
    # 옵션 추가
    # -----------------

    st.subheader("옵션 추가")

    group_map = {
        g["group_name"]: g["group_id"]
        for g in groups
    }

    if group_map:

        selected_group = st.selectbox(
            "옵션 그룹",
            list(group_map.keys())
        )

        option_name = st.text_input(
            "옵션명"
        )

        extra_price = st.number_input(
            "추가금액",
            min_value=0,
            step=500
        )

        if st.button("옵션 등록"):

            cursor.execute("""
                INSERT INTO option
                (
                    group_id,
                    option_name,
                    extra_price
                )
                VALUES (%s,%s,%s)
            """, (
                group_map[selected_group],
                option_name,
                extra_price
            ))

            conn.commit()

            st.success("등록 완료")
            st.rerun()

    st.divider()

    # -----------------
    # 현재 옵션
    # -----------------

    st.subheader("현재 옵션")

    cursor.execute("""
        SELECT
            o.option_id,
            g.group_name,
            o.option_name,
            o.extra_price
        FROM option o
        LEFT JOIN option_group g
            ON o.group_id = g.group_id
        ORDER BY o.option_id
    """)

    options = cursor.fetchall()

    if options:

        option_df = pd.DataFrame(options)

        edited_option_df = st.data_editor(
            option_df,
            hide_index=True,
            width="stretch",
            disabled=["option_id"],
            column_config={
                "option_id": "번호",

                "group_name": st.column_config.SelectboxColumn(
                    "옵션그룹",
                    options=list(group_map.keys()),
                    required=True
                ),

                "option_name": "옵션명",

                "extra_price": st.column_config.NumberColumn(
                    "추가금액",
                    format="%d원",
                    min_value=0
                )
            }
        )

        if st.button("옵션 수정 저장"):

            try:

                for _, row in edited_option_df.iterrows():

                    cursor.execute("""
                        UPDATE option
                        SET
                            group_id=%s,
                            option_name=%s,
                            extra_price=%s
                        WHERE option_id=%s
                    """, (
                        group_map[row["group_name"]],
                        row["option_name"],
                        int(row["extra_price"]),
                        row["option_id"]
                    ))

                conn.commit()

                st.success("수정 완료")
                st.rerun()

            except Exception as e:

                conn.rollback()
                st.error(e)

        st.divider()

        # -----------------
        # 옵션 삭제
        # -----------------

        st.subheader("옵션 삭제")

        option_map = {
            f"{row['group_name']} - {row['option_name']}":
            row["option_id"]
            for row in options
        }

        selected_option = st.selectbox(
            "삭제할 옵션",
            list(option_map.keys())
        )

        if st.button("옵션 삭제"):

            cursor.execute("""
                DELETE FROM option
                WHERE option_id=%s
            """, (
                option_map[selected_option],
            ))

            conn.commit()

            st.success("삭제 완료")
            st.rerun()

    else:

        st.info("등록된 옵션이 없습니다.")

    st.divider()

    if st.button("뒤로가기"):

        st.session_state.page = (
            "admin_dashboard"
        )

        st.rerun()

    conn.close()