---
title: 배송 설정
---

이 가이드는 스토어에서 배송을 구성하는 방법을 설명합니다 — 기본 배송 방법 설정부터 FedEx, UPS 및 DHL과 같은 제공업체의 실시간 요금을 위한 라이브 운송업체 통합까지.

## 배송 개요

Spwig은 두 가지 방식의 배송을 제공합니다:

- **수작업 배송 방법** — 사용자가 정의한 고정 요금 방법 (예: "표준 배송 — $5.99")
- **배송 업체 통합** — FedEx, UPS 및 DHL과 같은 제공업체에서 제공하는 실시간 요금

두 가지 방식 중 하나를 사용하거나 둘을 모두 결합할 수 있습니다.

## 배송 방법

배송 방법은 고객이 결제 시 보는 선택지입니다. 사이드바에서 **Orders > Shipments**로 이동하여 관리할 수 있습니다.

![Shipping methods](/static/core/admin/img/help/setup-shipping/shipping-methods.webp)

### 배송 방법 생성

1. **Add Shipping Method** 클릭
2. 세부 정보 입력:
   - **Name** — 고객에게 표시되는 표시 이름 (예: "Express Delivery")
   - **Description** — 서비스에 대한 간단한 설명
   - **Price** — 고정 배송 비용
   - **Estimated Delivery** — 예상 배송 시간 (예: "3-5 영업일")
3. **Save** 클릭

## 배송 지역

배송 지역은 배송 방법이 적용되는 지리적 지역을 정의합니다. **Shipping Zones** 섹션으로 이동하여 관리할 수 있습니다.

![Shipping zones](/static/core/admin/img/help/setup-shipping/shipping-zones.webp)

### 지역 생성

1. **Add Shipping Zone** 클릭
2. 지역 구성:
   - **Zone Name** — 내부 이름 (예: "US Domestic", "Europe")
   - **Countries** — 이 지역에 속하는 국가 선택
   - **States/Regions** — 특정 주로 좁히는 것을 선택적으로 사용할 수 있음
   - **Postal Code Patterns** — "9*"과 같은 패턴을 사용하여 특정 지역을 대상으로 지정
3. 이 지역에 배송 방법 할당
4. **Save** 클릭

### 지역 우선순위

고객의 주소가 여러 지역과 일치하는 경우, 가장 구체적인 지역이 우선순위를 가집니다. 주 단위 타겟팅이 있는 지역은 국가 단위 지역보다 우선순위가 높습니다.

## 배송 업체 통합

배송 업체와 연결하여 결제 시 실시간 계산된 요금을 제공합니다.

![Shipping carriers](/static/core/admin/img/help/setup-shipping/shipping-carriers.webp)

### 제공 가능한 업체

마켓플레이스에서 배송 업체를 둘러보고 설치할 수 있습니다.

![Shipping providers](/static/core/admin/img/help/setup-shipping/shipping-providers.webp)

지원되는 업체에는 다음과 같은 것이 포함됩니다:

- **FedEx** — Ground, Express, International
- **UPS** — Ground, 2-Day, Overnight, Worldwide
- **DHL** — Express, eCommerce
- **USPS** — Priority, First Class, Media Mail
- Marketplace를 통해 제공되는 다른 업체들도 있습니다.

### 업체 설정

1. 배송 업체 페이지로 이동하고 선호하는 업체에서 **Install** 클릭
2. 설정 마법사에 따라 다음 단계를 수행합니다:
   - **Step 1** — 제공업체 세부 정보 확인
   - **Step 2** — 일반 설정 구성
   - **Step 3** — API 인증 정보 입력 (계정 번호, API 키 등)
   - **Step 4** — 특정 서비스 활성화 (Ground, Express 등)
   - **Step 5** — 연결 테스트
3. 연결 후, 업체의 요금은 결제 시 자동으로 표시됩니다.

### API 인증 정보

각 업체는 API 계정이 필요합니다:

- **FedEx** — FedEx 개발자 포털에서 등록하여 앱을 생성하고 API 키 및 비밀을 복사합니다.
- **UPS** — UPS 개발자 키트에서 등록하여 액세스 키를 요청합니다.
- **DHL** — DHL의 비즈니스 포털을 통해 API 인증 정보를 요청합니다.

## 배송 규칙

고급 규칙을 생성하여 배송 방법이 제공되는 시기와 방식을 제어할 수 있습니다.

### 일반적인 규칙

- **$50 이상 무료 배송** — 무료 배송을 위한 장바구니 최소 금액 설정
- **경량 주문을 위한 고정 요금** — 주문 무게가 임계값 미만일 경우 고정 요금 적용
- **원격 지역에서 express 비활성화** — 우편 번호 기반으로 express 옵션 숨기기
- **비율 마크업** — 운송업체 요금의 비율을 기준으로 처리 비용 추가

### 규칙 생성

1. 배송 규칙 섹션으로 이동
2. **Add Rule** 클릭
3. 조건 설정 (장바구니 총액, 무게, 지역 등)
4. 동작 정의 (요금 조정, 방법 숨기기, 무료 배송 활성화)
5. 규칙 저장

규칙은 순서대로 평가됩니다 — 첫 번째 일치하는 규칙이 적용됩니다.

## 무료 배송

### 전체 스토어 무료 배송

**Settings > Store Settings**에서 전역적으로 무료 배송을 활성화합니다:

- **Free Shipping** 전환 스위치 켜기
- 선택적으로 최소 주문 금액 설정
- 자격을 갖는 지역 선택

### 프로모션 기간의 무료 배송

시간 제한된 무료 배송 제안을 생성합니다:

1. **Marketing > Sales & Promotions**으로 이동
2. 새 프로모션 생성
3. 조건 설정: "장바구니 총액이 X 이상"
4. 동작 설정: "무료 배송"
5. 시작 및 종료 날짜 설정

## 국제 배송

국제 주문을 위해 제품이 다음을 포함해야 합니다:

- **HS Code** — 조화 시스템 관세 분류
- **Country of Origin** — 제조 국가
- **Customs Value** — 관세를 위한 선언된 가치

이 필드는 각 제품의 **Inventory** 탭에 있습니다. 운송업체는 이 정보를 사용하여 관세 문서를 자동으로 생성합니다.

## 팁

- 스토어를 신속하게 시작하려면 수작업 배송 방법부터 시작한 후 나중에 운송업체 통합을 추가하세요.
- 가장 일반적인 목적지에 대한 배송 지역을 먼저 생성하세요.
- 다양한 주소로 테스트 주문을 생성하여 배송 구성이 항상 테스트하세요.
- 처리 및 포장 비용을 커버하기 위해 요금 마크업 기능을 사용하세요.
- 평균 주문 금액을 높이기 위해 무료 배송 임계값을 설정하세요.
