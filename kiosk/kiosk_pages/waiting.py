import streamlit as st
import base64
import os


def render():

    # MP4 읽기
    with open(
        "in_charge/image/PixVerse_V6_Image_Text_720P_Luxury_iced_coffee.mp4",
        "rb"
    ) as video_file:
        video_base64 = base64.b64encode(
            video_file.read()
        ).decode()

    # 폰트 읽기 (Pretendard 통일)
    with open(
        "fonts/PretendardVariable.ttf",
        "rb"
    ) as font_file:
        pretendard_base64 = base64.b64encode(
            font_file.read()
        ).decode()

    with open(
        "fonts/GmarketSansTTFBold.ttf",
        "rb"
    ) as font_file:
        gmarket_base64 = base64.b64encode(
            font_file.read()
        ).decode()  

    st.markdown(
        f"""
        <style>

        @font-face {{
            font-family: 'PretendardVariable';
            src: url(data:font/ttf;base64,{pretendard_base64}) format('truetype');
        }}

        @keyframes glow {{
            0% {{
                opacity: 0.4;
                text-shadow: 0 0 5px rgba(255,255,255,0.3);
            }}
            50% {{
                opacity: 1;
                text-shadow: 0 0 20px rgba(255,255,255,0.8);
            }}
            100% {{
                opacity: 0.4;
                text-shadow: 0 0 5px rgba(255,255,255,0.3);
            }}
        }}

        .glow-text {{
            animation: glow 1.5s infinite ease-in-out;
        }}

        /* 타이핑 효과 효과를 위한 keyframes */
        @keyframes typing {{
            from {{ max-width: 0; }}
            to {{ max-width: 100%; }}
        }}

        @keyframes fadeIn {{
            from {{ opacity: 0; }}
            to {{ opacity: 1; }}
        }}

        /* 공통 타이핑 컨테이너 */
        .typing-container {{
            display: inline-block;
            white-space: nowrap;
            overflow: hidden;
            vertical-align: bottom;
        }}

       
        .coffee {{
            font-family: 'PretendardVariable' !important;
            font-weight: 700 !important;
            opacity: 0;
            max-width: 0;
            animation: 
                fadeIn 0.1s ease forwards,
                typing 1.8s steps(20) forwards;
            animation-delay: 0.5s; 
        }}

    
        .net {{
            font-family: 'PretendardVariable' !important;
            font-weight: 700 !important;
            display: inline-block;
            white-space: nowrap;
            opacity: 0;
            max-width: 0;
            overflow: hidden;
            backface-visibility: hidden;
            animation: 
                fadeIn 0.1s ease forwards,
                typing 0.8s steps(10) forwards;
            animation-delay: 2.0s; 
        }}

        /* 비디오 백그라운드 설정 (기존 레이아웃 보존) */
        .video-background {{
            position: fixed;
            top: 0;
            left: 0;
            width: 100vw;
            height: 100vh;
            z-index: -1;
            overflow: hidden;
        }}

        .video-background video {{
            width: 100%;
            height: 100%;
            object-fit: contain;
        }}

        .block-container {{
            padding-top: 0rem !important;
            padding-bottom: 0rem !important;
            padding-left: 0rem !important;
            padding-right: 0rem !important;
            max-width: 100% !important;
        }}

        [data-testid="stHeader"] {{
            display: none;
        }}

        [data-testid="stToolbar"] {{
            display: none;
        }}

        .stApp {{
            background: transparent !important;
        }}

        /* 버튼 기본 스타일 */
        div.stButton > button {{
            background-color: rgba(195,170,145,0.60);
            color: #5C4033;
            height: 120px;
            border-radius: 15px;
            border: none;
            box-shadow: 0px 4px 15px rgba(0,0,0,0.35);
            transition: all 0.3s ease;
        }}

        div.stButton > button:hover {{
            transform: scale(1.05);
            box-shadow: 0px 8px 25px rgba(255,255,255,0.25);
        }}

        /* 하단 매장/포장 버튼 내부 텍스트 PretendardVariable 700 오타 수정 적용 */
        div.stButton > button * {{
            font-family: 'PretendardVariable' !important;
            font-size: 25px !important;
            font-weight: 700 !important;
        }}

        </style>
        """,
        unsafe_allow_html=True
    )

    # 비디오 백그라운드 출력
    st.markdown(
        f"""
        <div class="video-background">
            <video autoplay muted loop playsinline>
                <source
                    src="data:video/mp4;base64,{video_base64}"
                    type="video/mp4">
            </video>
        </div>
        """,
        unsafe_allow_html=True
    )

    # 기존 여백 완벽 유지
    st.markdown(
        "<div style='height:25vh'></div>",
        unsafe_allow_html=True
    )

    # 순차 타이핑용 h2 태그 구조 복원
    st.markdown("""
    <h2 style="
        text-align:center;
        color:#F8F1E6;
        font-size:180px;
        font-family:'PretendardVariable';
        text-shadow:2px 2px 5px rgba(0,0,0,0.5);
        margin: 0;
    ">
        <span class="typing-container coffee">Coffee?</span>
        <span class="typing-container net">&nbsp;NET.</span>
    </h2>
    """, unsafe_allow_html=True)

    st.markdown("""
    <p class="glow-text" style="
        text-align:center;
        color:#FFE8A3;
        font-size:40px;
        margin-top:170px;
        margin-bottom:70px;
        font-family:'PretendardVariable';
    ">
    원하시는 주문방식을 선택하세요
    </p>
    """, unsafe_allow_html=True)           

    left, center, right = st.columns([1, 3, 1])

    with center:

        col1, gap1, col2 = st.columns([1, 0.2, 1])

        # 기존 버튼 내부 이동 로직 및 세션 연결 보존
        with col1:
            if st.button("FOR HERE [ 매장 ]", use_container_width=True):
                st.session_state.order_type = "매장"
                st.session_state.page = "menu"
                st.rerun()

        with col2:
            if st.button("TAKE OUT [ 포장 ]", use_container_width=True):
                st.session_state.order_type = "포장"
                st.session_state.page = "menu"
                st.rerun()

    st.markdown(
        "<div style='height:60px'></div>",
        unsafe_allow_html=True
    )

    admin_space, admin = st.columns([7, 0.7])

    with admin:
        if st.button("⚙️"):
            st.session_state.page = "admin_login"
            st.rerun()