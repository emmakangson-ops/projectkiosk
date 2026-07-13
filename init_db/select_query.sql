-- mysql -u kiosk -p
-- use kiosk 

-- =====================================
-- <1> 메뉴 관리
-- =====================================
# 판매되는 메뉴는 카테고리별로 구분하여 관리

SELECT c.category_name,
       m.menu_name,
       m.menu_price
FROM CATEGORY c
JOIN MENU m
ON c.category_code = m.category_code
ORDER BY c.category_code;


-- =====================================
-- <2> 메뉴 관리
-- =====================================
# 특정 메뉴 상세조회

SELECT m.menu_name,
       og.group_name,
       o.option_name,
       o.extra_price
FROM MENU m
JOIN MENU_OPTION_GROUP mog
ON m.menu_id = mog.menu_id
JOIN OPTION_GROUP og
ON mog.group_id = og.group_id
JOIN OPTION o
ON og.group_id = o.group_id
WHERE m.menu_id = 1;

-- =====================================
-- <3> 메뉴 옵션 관리
-- =====================================
# 옵션그룹 및 추가금액 조회

SELECT og.group_name,
       o.option_name,
       o.extra_price
FROM OPTION_GROUP og
JOIN OPTION o
ON og.group_id = o.group_id;

-- =====================================
-- <4> 메뉴 옵션 관리
-- =====================================
# 메뉴별 옵션그룹 조회

SELECT m.menu_name,
       og.group_name
FROM MENU m
JOIN MENU_OPTION_GROUP mog
ON m.menu_id = mog.menu_id
JOIN OPTION_GROUP og
ON mog.group_id = og.group_id
WHERE m.menu_id = 1;

-- =====================================
-- <5> 주문 관리
-- =====================================
# 주문번호 기준 주문 조회

SELECT *
FROM ORDERS
WHERE order_id = 1001;


-- =====================================
-- <6> 주문 관리
-- =====================================
# 주문 메뉴 / 수량 / 금액 / 옵션 조회
SELECT o.order_id,
       m.menu_name,
       od.quantity,
       od.amount
FROM ORDERS o
JOIN ORDER_DETAIL od
ON o.order_id = od.order_id
JOIN MENU m
ON od.menu_id = m.menu_id
WHERE o.order_id = 1001;

# 옵션
SELECT od.detail_id,
       op.option_name,
       oo.option_price
FROM ORDER_OPTION oo
JOIN OPTION op
ON oo.option_id = op.option_id
JOIN ORDER_DETAIL od
ON oo.detail_id = od.detail_id
WHERE od.order_id = 1001;

-- =====================================
-- <7> 주문 관리
-- =====================================
# 매장/포장 주문 조회

#포장
SELECT *
FROM ORDERS
WHERE takeout_type='Y';

#매장
SELECT *
FROM ORDERS
WHERE takeout_type='N';

-- =====================================
-- <8> 회원 관리
-- =====================================
# 회원정보 조회
SELECT member_id,
       phone_number,
       stamp,
       grade
FROM MEMBER;

-- =====================================
-- <9> 회원 관리
-- =====================================
# 스탬프 조회
SELECT member_id,
       phone_number,
       stamp
FROM MEMBER;

# 특정 회원
SELECT *
FROM MEMBER
WHERE phone_number='01012341234';


-- =====================================
-- <10> 결제 관리
-- =====================================
# 결제정보 조회
SELECT pay_id,
       final_amt,
       pay_type,
       pay_date
FROM PAYMENT;

-- =====================================
-- <11> 결제 관리
-- =====================================
# 결제정보 조회
SELECT m.member_id,
       m.phone_number,
       p.pay_id,
       p.final_amt,
       p.pay_date
FROM MEMBER m
JOIN PAYMENT p
ON m.member_id = p.member_id;

-- =====================================
-- <12> 통계 관리
-- =====================================
# 메뉴별 판매수량
SELECT m.menu_name,
       SUM(od.quantity) AS total_qty
FROM ORDER_DETAIL od
JOIN MENU m
ON od.menu_id = m.menu_id
GROUP BY m.menu_name;


# 메뉴별 판매금액
SELECT m.menu_name,
       SUM(od.amount) AS total_sales
FROM ORDER_DETAIL od
JOIN MENU m
ON od.menu_id = m.menu_id
GROUP BY m.menu_name;

-- =====================================
-- <13> 통계 관리
-- =====================================
# 인기메뉴 순위 top3

SELECT m.menu_name,
       SUM(od.quantity) AS total_qty
FROM ORDER_DETAIL od
JOIN MENU m
ON od.menu_id = m.menu_id
GROUP BY m.menu_name
ORDER BY total_qty DESC
LIMIT 3;

-- =====================================
-- <14> 통계 관리
-- =====================================
# 일별 매출
SELECT DATE(order_date) AS sales_day,
       SUM(total_amount) AS sales
FROM ORDERS
GROUP BY DATE(order_date);

# 월별 매출
SELECT DATE_FORMAT(order_date,'%Y-%m') AS sales_month,
       SUM(total_amount) AS sales
FROM ORDERS
GROUP BY DATE_FORMAT(order_date,'%Y-%m');

# 연도별 매출
SELECT YEAR(order_date) AS sales_year,
       SUM(total_amount) AS sales
FROM ORDERS
GROUP BY YEAR(order_date);

-- =====================================
-- <15> 통계 관리
-- =====================================
# 카테고리별 판매현황

SELECT c.category_name,
       SUM(od.quantity) AS qty,
       SUM(od.amount) AS sales
FROM CATEGORY c
JOIN MENU m
ON c.category_code = m.category_code
JOIN ORDER_DETAIL od
ON m.menu_id = od.menu_id
GROUP BY c.category_name;

# 회원별 구매현황
SELECT m.member_id,
       m.phone_number,
       COUNT(p.pay_id) AS purchase_count,
       SUM(p.final_amt) AS purchase_amount
FROM MEMBER m
JOIN PAYMENT p
ON m.member_id = p.member_id
GROUP BY m.member_id,
         m.phone_number;