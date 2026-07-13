# pages/menu.py
import streamlit as st
import base64
from db.database import get_cursor

def render():
   
    try:
        with open("fonts/PretendardVariable.ttf", "rb") as font_file:
            pretendard_base64 = base64.b64encode(font_file.read()).decode()
    except FileNotFoundError:
        pretendard_base64 = ""

    if "cart" not in st.session_state:
        st.session_state.cart = []

    # 2. UI 스타일 주입 
    st.markdown(f"""
    <style>
    @font-face {{
        font-family: "Pretendard";
        src: url(data:font/ttf;base64,{pretendard_base64}) format("truetype");
    }}
    
    /* 전체 기본 서체 지정 (기본 글씨는 Regular 유지) */
    html, body, [class*="st-"], div, p, h1, h2, h3, button, a {{
        font-family: "Pretendard", sans-serif !important;
    }}
    
    h1 {{
        font-weight: 800 !important;
        letter-spacing: -0.5px;
        margin: 0 !important;
        display: inline-block !important;
    }}

    h3 {{
        margin: 16px 0 0 0 !important;
        color: #666666 !important;
        font-weight: 500 !important;
        font-size: 18px !important;
    }}
                
    .stApp {{
        background:
            radial-gradient(circle at top left, #FFF8F0 0%, transparent 35%),               
            radial-gradient(circle at bottom right, #F5EFE7 0%, transparent 30%),
            linear-gradient(180deg, #FCFBF8 0%, #F8F4EE 50%, #FCFBF8 100%);
    }}

    .block-container {{
        max-width: 1200px !important; 
        margin: 0 auto !important;    
        padding-left: 2rem !important;
        padding-right: 2rem !important;
    }}
                                
    /* 일반 카테고리 탭 버튼 스타일 */
    div[data-testid="stButton"] > button {{
        background-color: white !important;
        color: #222 !important;
        border: none !important;
        border-bottom: 3px solid transparent !important;
        border-radius: 0px !important;
        font-size: 24px;
        font-weight: 800 !important; /* [강조] 카테고리 폰트 두껍게 */
        height: 58px;
    }}

    div[data-testid="stButton"] > button p {{
         font-size: 18px !important;
         font-weight: 800 !important; /* [강조] 카테고리 내부 텍스트 폰트 두껍게 */
    }}
                                                       
    div[data-testid="stVerticalBlock"] {{
        gap: 0px !important;
    }}                        
                
    /* 선택된 카테고리 탭 버튼 스타일 */
    div[data-testid="stButton"] > button[kind="primary"] {{
        background-color: #f2f2f2 !important;
        color: #222 !important;
        border-bottom: 3px solid #222 !important;
        border-radius: 0px !important;
        box-shadow: none !important;
    }}
                
    div[data-testid="stButton"] > button:hover {{
        border-bottom: 3px solid #222 !important;
    }}

    /* 카테고리 박스 컨테이너 */
    [class*="st-key-category_box"] {{
        background: #ffffff !important;
        border-radius: 18px !important;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.10) !important;
        padding: 16px 24px !important; 
        margin-top: 35px !important;    
        margin-bottom: 50px !important; 
        border: none !important; 
        overflow: hidden !important;        
    }}
                
    /* 메뉴 카드 컴포넌트 디자인 */
    [class*="st-key-card_"] {{
        background: #ffffff !important;
        border: none !important; 
        border-radius: 18px !important;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.10) !important;  
        padding: 12px !important; 
        transition: transform 0.2s ease, box-shadow 0.2s ease;
        margin-bottom: 50px !important; 
        overflow: hidden !important; 
    }}            

    [class*="st-key-card_"]:hover {{
        transform: translateY(-6px);  
        box-shadow: 0 12px 30px rgba(0, 0, 0, 0.15) !important;
    }}

    div[data-testid="stColumnsHorizontal"] {{
        gap: 50px !important; 
    }}

    /* 상단 배지 스타일 */
    .order-badge-style {{
        display: inline-block !important;
        white-space: nowrap !important;
        background-color: #5E5049 !important; 
        color: #ffffff !important;
        padding: 10px 28px !important; 
        border-radius: 50px !important;
        font-size: 26px !important;
        font-weight: 800 !important;
        letter-spacing: -0.5px !important;
        box-shadow: 0 8px 24px rgba(94, 80, 73, 0.25), 0 2px 6px rgba(94, 80, 73, 0.15) !important;
    }}
    </style>
    """, unsafe_allow_html=True)                

    # 3. 데이터베이스 데이터 조회
    conn, cursor = get_cursor()    

    cursor.execute("SELECT category_name FROM category ORDER BY category_code")
    categories = [row["category_name"] for row in cursor.fetchall()]

    cursor.execute("""
    SELECT
        c.category_name,
        m.menu_id,
        m.menu_name,
        m.menu_price,
        m.menu_image,
        m.sale_yn,
        m.is_active
    FROM menu m
    JOIN category c
        ON m.category_code = c.category_code
    WHERE m.is_active = 1
    ORDER BY
        c.category_code,
        m.menu_id
    """)
    menu_rows = cursor.fetchall()
    
    menu_dict = {}
    for row in menu_rows:
        category_name = row["category_name"]
        if category_name not in menu_dict:
            menu_dict[category_name] = []
        menu_dict[category_name].append(dict(row))

    order_type = st.session_state.get("order_type", "매장")

    # 상단 주문 방식 안내 구역
    st.markdown(f"""
    <div style="margin-top: 35px; margin-bottom: 30px;">
        <span class="order-badge-style">{order_type} 주문</span>
        <h3>원하시는 메뉴를 선택해 주세요</h3>
    </div>
    """, unsafe_allow_html=True)
    
    # 4. 카테고리 탭 UI 구현
    if "selected_category" not in st.session_state:
        st.session_state.selected_category = categories[0] if categories else None

    with st.container(border=True, key="category_box"):
        tab_cols = st.columns(len(categories))
        for idx, category_name in enumerate(categories):
            is_selected = (category_name == st.session_state.selected_category)
            with tab_cols[idx]:
                if st.button(category_name, key=f"tab_{idx}", width='stretch', type="primary" if is_selected else "secondary"): 
                    st.session_state.selected_category = category_name
                    st.rerun()       
                
    selected_category = st.session_state.selected_category
    filtered_menu = menu_dict.get(selected_category, [])

    # 5. 메뉴 리스트 UI 구현
    menu_cols = st.columns(2)
    for idx, menu in enumerate(filtered_menu):
        with menu_cols[idx % 2]:
            with st.container(border=True, key=f"card_{menu['menu_id']}"):
                image_path = menu.get("menu_image")
                if not image_path:
                    image_path = "images/default.png"

                st.image(image_path, width='stretch')     

             
                # st.markdown(f"""
                #     <div style="text-align: center; margin-top: 20px; margin-bottom: 16px;">
                #         <p style="margin: 0 0 8px 0; font-size: 26px; font-weight: 700; color: #222222;">{menu['menu_name']}</p>
                #         <p style="margin: 0; font-size: 22px; font-weight: 800; color: #222222;">{menu['menu_price']:,}원</p>
                #     </div>
                # """, unsafe_allow_html=True)
                st.markdown(f"""
                <div style="text-align: center; margin-top: 20px;">
                    <p style="margin:0 0 8px 0; font-size:26px; font-weight:700;">
                        {menu['menu_name']}
                    </p>
                </div>
                """, unsafe_allow_html=True)

                # if menu["sale_yn"] == "N":
                #     st.markdown("""
                #     <p style="
                #         color:red;
                #         font-size:20px;
                #         font-weight:bold;
                #         text-align:center;
                #         margin:5px 0;
                #     ">
                #         🚫 품절
                #     </p>
                #     """, unsafe_allow_html=True)

                st.markdown(f"""
                <p style="
                    text-align:center;
                    font-size:22px;
                    font-weight:800;
                ">
                    {menu['menu_price']:,}원
                </p>
                """, unsafe_allow_html=True)

                sold_out = menu["sale_yn"] == "N"
                if st.button(
                    "🚫 품절" if sold_out else "🛒 주문하기",
                    key=f"menu_{menu['menu_id']}",
                    use_container_width=True,
                    type="primary",
                    disabled=sold_out
                ):
                    st.session_state.selected_menu = dict(menu)
                    st.session_state.page = "option"
                    conn.close()
                    st.rerun()
             
    # 6. 하단 장바구니 바 구역
    st.markdown("<br><br>", unsafe_allow_html=True)
    st.divider()

    cart_count = len(st.session_state.get("cart", []))
    col1, col2 = st.columns([2, 1])

    with col1:
       
        st.markdown(f"### 🛒 **장바구니 {cart_count}개**")
        
    with col2:
     
        if st.button("**장바구니 보기**", key="go_to_summary_btn", width='stretch', type="primary"):
            st.session_state.page = "summary"
            conn.close()
            st.rerun()
            
    conn.close()