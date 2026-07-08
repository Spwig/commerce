---
title: Tax Configuration
---

가게의 세금 규칙을 구성하여 고객의 위치에 따라 주문에 올바른 세금이 자동으로 적용되도록 설정합니다. 한 번의 클릭으로 지역별 사전 설정을 불러오거나, 특정 국가, 주, 도시 또는 우편 번호에 대한 사용자 정의 규칙을 만들 수 있습니다.

![Tax Dashboard](/static/core/admin/img/help/tax-configuration/tax-dashboard.webp)

## Tax Dashboard

**Orders > Shipments > Tax Rates**로 이동하여 세금 대시보드를 엽니다. 이 페이지는 다음과 같은 항목을 표시합니다:

- **Statistics panel** — 총 규칙, 활성 규칙, 커버된 국가, 사용 중인 세금 유형을 표시하는 네 개의 카드
- **Filters** — 이름, 국가 또는 주에 따라 검색하고, 국가, 세금 유형(Sales Tax, VAT, GST, Custom) 또는 상태(Active/Inactive)에 따라 필터링할 수 있습니다.
- **Tax rule cards** — 각 카드는 국가 깃발, 규칙 이름, 위치, 세율 퍼센트, 세금 유형 배지, 상태 배지, 우선순위, 면제 수를 표시합니다.

## Loading Tax Presets

**Load Presets**을 클릭하여 사전 설정 모달을 엽니다. 사전 설정은 지역별 표준 세금율의 집합으로, 한 번의 클릭으로 가게에 로드할 준비가 되어 있습니다.

![Load Presets](/static/core/admin/img/help/tax-configuration/tax-presets-modal.webp)

사전 설정은 세계 지역별로 구성되어 있습니다:

| Region | Preset Groups |
|--------|--------------|
| **Africa** | Africa VAT (25 rates) |
| **Asia Pacific** | Asia-Pacific VAT/GST (24 rates), Central Asia VAT (6 rates) |
| **Europe** | EU VAT Rates, UK VAT, Other European VAT |
| **Latin America** | Latin America VAT |
| **Middle East** | Middle East VAT |
| **North America** | US State Sales Tax, Canadian GST/HST |
| **Oceania** | Oceania GST/VAT |

### How Presets Work

1. 원하는 사전 설정 그룹에서 **Load**을 클릭합니다
2. 시스템은 그 그룹에 있는 모든 국가 또는 주에 대한 세금 규칙을 생성합니다
3. 동일한 국가, 주 및 세금 유형을 가진 기존 규칙은 중복을 방지하기 위해 자동으로 건너뜁니다
4. 로드 후 각 규칙은 완전히 편집 가능합니다 — 필요 없는 규칙을 제외하거나 세율을 조정하거나 면제를 추가할 수 있습니다

여러 사전 설정 그룹을 로드할 수 있습니다. 예를 들어, 유럽 전역에 고객을 판매하는 경우 EU VAT 및 UK VAT 모두를 로드할 수 있습니다.

## Creating Tax Rules Manually

**Add Tax Rate**를 클릭하여 사용자 정의 규칙을 생성합니다. 폼에는 다음과 같은 네 섹션이 있습니다:

![Tax Rate Form](/static/core/admin/img/help/tax-configuration/tax-rate-form.webp)

### Basic Information

| Field | Description |
|-------|-------------|
| **Name** | 규칙의 표시 이름 (예: "California Sales Tax") |
| **Is Active** | 규칙을 활성화하거나 비활성화하는 전환 스위치 |
| **Tax Type** | Sales Tax, VAT, GST 또는 Custom Tax |
| **Rate (%)** | 퍼센트로 표시되는 세율 (예: 8.25%를 입력하려면 8.25를 입력합니다) |
| **Priority** | 여러 규칙이 동일한 위치에 일치할 때 더 높은 숫자가 우선권을 가집니다 |

### Geographic Scope

| Field | Description |
|-------|-------------|
| **Country** | ISO 3166-1 alpha-2 코드 (예: US, GB, DE) |
| **State** | 주 또는 성 (빈칸을 남겨두면 전체 국가에 적용됩니다) |
| **City** | 도시 이름 (선택 사항, 도시 수준 세금 규칙에 사용) |
| **Postal Codes** | 특정 우편 번호 목록 (선택 사항, 우편 번호 수준 규칙에 사용) |

규칙은 가장 구체적인 것부터 가장 덜 구체적인 것까지 일치합니다. 특정 우편 번호에 대한 규칙은 동일한 주에 대한 규칙보다 우선권을 가지며, 이는 전체 국가에 대한 규칙보다 우선권을 가집니다.

### Application Rules

| Field | Description |
|-------|-------------|
| **Applies to Shipping** | 선택 시 이 세금은 배송 비용에도 적용됩니다 |
| **Compound Tax** | 선택 시 이 세금은 다른 세금 위에 계산됩니다 (기본 금액에 이전에 적용된 세금을 더한 금액) |

### Product Exemptions

| Field | Description |
|-------|-------------|
| **Exempt Product Types** | 이 세금에서 면제되는 제품 유형 (예: 디지털, 서비스) |
| **Exempt Categories** | 이 세금에서 면제되는 특정 제품 카테고리 |

## Tax Types

| Type | Used For | Examples |
|------|----------|---------|
| **Sales Tax** | US, Canada | 주 및 성별 세금 |
| **VAT** | Europe, UK, much of Asia and Africa | 부가가치세 |
| **GST** | Australia, New Zealand, India, Singapore | 물품 및 서비스세 |
| **Custom Tax** | Special cases | 지역별 추가세, 환경세, 과소비세 |

## How Tax Calculation Works

고객이 결제 화면에 도달하면 시스템은 고객의 배송 주소에 따라 자동으로 세금을 계산합니다:

1. **지리적 일치** — 고객의 국가에 일치하는 모든 활성 규칙을 찾고, 이후 주, 도시 및 우편 번호로 좁혀갑니다
2. **구체성 점수** — 더 구체적인 규칙(우편 번호 > 도시 > 주 > 국가)은 더 높은 순위를 받습니다
3. **우선순위 정렬** — 동일한 구체성 수준 내에서 더 높은 우선순위 규칙이 우선권을 가집니다
4. **제품 면제** — 면제된 제품은 각 적용 가능한 규칙에서 제외됩니다
5. **비복합 세금** — 각 항목의 기본 가격에 대해 먼저 계산됩니다
6. **복합 세금** — 기본 가격에 이미 적용된 모든 비복합 세금을 더한 금액에 대해 계산됩니다
7. **배송 세금** — 규칙에 "Applies to Shipping"이 활성화되어 있는 경우, 배송 비용은 과세 금액에 포함됩니다

세금 세부 정보는 주문과 함께 저장되어 해당 규칙이 적용되었고 각 규칙이 기여한 금액을 확인할 수 있습니다.

## Common Setups

### EU Store

1. **Load Presets**을 클릭하고 **EU VAT Rates** 그룹을 로드합니다
2. 이는 모든 유럽 연합 회원국에 현재 표준 세율을 적용한 VAT 규칙을 생성합니다
3. UK에도 판매하는 경우 **UK VAT**를 선택적으로 로드할 수 있습니다

### US Store

1. **Load Presets**을 클릭하고 **US State Sales Tax** 그룹을 로드합니다
2. 이는 모든 미국 주에서 세금을 징수하는 주에 대한 세금 규칙을 생성합니다
3. 도시 수준 세금이 필요한 경우, 도시 필드를 채우고 우선순위를 더 높인 규칙을 수동으로 추가합니다

### Multi-Region Store

1. 판매하는 각 시장에 대한 여러 사전 설정 그룹을 로드합니다
2. 시스템은 고객이 위치한 곳에 따라 올바른 세금을 적용합니다
3. 특정 비즈니스 요구 사항에 따라 필요한 경우 개별 규칙을 조정합니다

## Tips

- **사전 설정부터 시작하세요** — 목표 시장의 사전 설정 그룹을 로드한 후, 모든 규칙을 처음부터 만드는 대신 개별 세율을 조정하세요.
- **우선순위를 신중하게 설정하세요** — 더 구체적인 지역 규칙에 더 높은 우선순위 값을 설정하여 더 넓은 지역 규칙을 올바르게 덮어쓸 수 있도록 합니다.
- **복합 세금을 신중하게 확인하세요** — 복합 세금은 드뭅니다. 대부분의 지역은 단순(비복합) 세금을 사용합니다. 지역 규정이 명확히 세금에 세금을 계산하도록 요구하는 경우에만 복합 세금을 활성화하세요.
- **규칙을 활성/비활성 상태로 유지하세요** — 계절적 또는 일시적인 변경 사항을 위해 세금 규칙을 삭제하는 대신, 비활성 상태로 전환하고 필요할 때 다시 활성화하세요.
- **실제 운영 전에 테스트하세요** — 세금 규칙을 설정한 후, 다른 주소에서 테스트 주문을 내어 올바른 세금이 적용되는지 확인하세요.

기억하세요: 마크다운 포맷, 이미지 경로, 코드 블록 및 기술 용어는 보존 규칙에 따라 정확히 유지하세요.