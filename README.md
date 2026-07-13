2026년 교육 과정 팀01 프로젝트01
===
1. 주제 선정
2. 밴치 마킹
3. 요구 사항 ( 가상 시나리오  )
4. 개념적 -> 논리적(LERD) -> 물리적(PERD)모델링
5. SQL 작성
   - ( DDL, DML, DQL )
6. DBMS에  install
   - 생성 ( 새 계정 , 새 DB , 권한부여 )
   - DDL, DML 실행
   - DQL 실행하여 모델링 검증
7. Python와 연동
--------
> 프로젝트 흐름
```
app.py
   │
   ▼
order_type
   │
   ▼
menu
   │
   ▼
option
   │
   ▼
summary
   │
   ▼
membership
   │
   ▼
phone
   │
   ▼
payment
   │
   ▼
waiting
   │
   ▼
complete
   │
   ▼
receipt
```
--------
> 프로젝트 구조
```
kiosk/
│
├── app.py                     # 프로그램 시작점
├── .env                       # 환경변수
├── requirements.txt           # 설치 라이브러리
├── 실행방법.md
│
├── db/
│   └── database.py            # MySQL 연결
│
├── utils/
│   ├── cookies.py             # 쿠키 관리
│   └── session.py             # SessionState 관리
│
├── kiosk_pages/               # 사용자(키오스크) 화면
│   ├── order_type.py          # 포장/매장 선택
│   ├── menu.py                # 메뉴 선택
│   ├── option.py              # 옵션 선택
│   ├── summary.py             # 주문 내역
│   ├── membership.py          # 적립 여부
│   ├── phone.py               # 전화번호 입력
│   ├── payment.py             # 결제
│   ├── waiting.py             # 제조 대기
│   ├── complete.py            # 주문 완료
│   ├── receipt.py             # 영수증
│   ├── admin_login.py         # 관리자 로그인
│   └── admin_dashboard.py     # 관리자 메인
│
├── admin/                     # 관리자 기능
│   ├── category_manage.py     # 카테고리 관리
│   ├── menu_manage.py         # 메뉴 관리
│   ├── option_manage.py       # 옵션 관리
│   ├── member_manage.py       # 회원 관리
│   ├── sales.py               # 매출 통계
│   └── change_password.py     # 관리자 비밀번호 변경
│
├── images/                    # 메뉴 및 UI 이미지
│   ├── americano.png
│   ├── latte.png
│   ├── cake.png
│   ├── ...
│
├── fonts/
│   ├── GmarketSansTTFBold.ttf
│   └── PretendardVariable.ttf
│
└── in_charge/                 # 테스트/시안 파일
    ├── menu2.py
    └── image/
```
---
## 멤버 역할

> 강유진
- DB 모델링 
- 결제 기능 
- 스탬프 적립, 사용 기능
- 멤버십 등급 관리 및 등급별 할인 적용 기능 
- 영수증(상세내역) 출력 기능 
- 메뉴별 옵션 선택 기능 
- 관리자 화면 매출 통계 기능 


> 서지윤
- 전체 UI & UX 구성
- 관리자 대시 보드 
- 관리자 로그인 및 세션 유지 기능 
- 관리자 메뉴, 옵션 등록 및 수정 관리 기능
- 주문 내역, 장바구니 기능


> 강재환
- 팀 매니징
- DB 스키마, 데이터 관리 
- 관리자 비밀번호 변경 기능 
- 관리자 메뉴 관리 
- 메뉴 화면 구성 


> 박소연
- 요구사항 분석 및 정의 
- 프로젝트 산출물 관리 작성
- 전체 UI & UX 구성
- 키오스크 대기 화면 구성
- 키오스크 이용 방법(매장,포장) 선택 기능 


> 박종민 
- 요구사항 분석 및 정의
- 결제 화면 구성
- 주문 완료 구성
- Q/A 테스트