---
title: 구독 요금제
---

구독 요금제를 통해 제품에 대해 반복 결제를 제공할 수 있습니다. 소모품, 서비스, 정성스럽게 구성된 박스, 또는 고객이 반복적으로 구매하는 기타 제품에 이상적입니다. 이 가이드는 요금제를 생성하고 구성하는 방법, 가격 대상을 설정하고, 체험 기간을 추가하며, 선택적인 추가 요금을 첨부하는 방법을 설명합니다.

## 시작하기
관리자 사이드바에서 **구독 > 구독 요금제**로 이동하세요. 요금제 목록은 현재 활성 상태인 구독자 수와 표시 상태와 함께 모든 요금제를 보여줍니다.

새로운 요금제를 만들려면 **+ 구독 요금제 추가** 버튼을 클릭하세요 — 이는 단계별로 설정을 안내하는 요금제 생성 마법사로 이어집니다.

![구독 요금제 목록](/static/core/admin/img/help/subscription-plans/plan-list.webp)

자체적으로 구매할 수 없는 요금제는 템플릿일 뿐입니다. 여기서 생성한 후 제품의 **구독** 탭(단순, 변수형, 디지털 제품만 해당됨)에서 하나 이상의 제품에 첨부하여 고객이 실제로 구독할 수 있도록 해야 합니다. 해당 단계에 대해 [제품을 구독으로 판매하는 방법](/help/selling-products-as-subscriptions)을 참조하십시오.

## 요금제 정보

첫 번째 섹션은 요금제의 핵심 정체성을 담고 있습니다.

- **요금제 이름** — 구독 시 고객이 보는 이름입니다. 다른 스토어 언어에 대한 번역을 추가하려면 세계 지도 아이콘을 클릭하세요.
- **Slug** — 이름에서 자동으로 생성된 URL 친화적인 식별자(예: `premium-plan`)입니다. 이는 내부에서 사용되며 통합에도 사용됩니다.
- **설명** — 요금제에 포함된 내용을 설명하는 선택적 텍스트입니다. 번역을 지원합니다.

## 가격 모델

이 요금제에 대한 가격 구조를 선택하십시오:

| 가격 모델 | 최적의 경우 |
|---------------|----------|
| **계층형 가격** | 장기 계약 옵션을 제공하여 월간, 분기별, 연간 결제 옵션을 제공하고 더 긴 기간에 대해 할인을 제공합니다 |
| **양 기반** | 사용자 또는 좌석당 가격으로, 총액이 수량에 따라 증가합니다(예: 팀 라이선스) |
| **고정 요금** | 변동 없이 단일 고정 가격 |

모든 마크다운 포맷, 이미지 경로, 코드 블록, 기술 용어를 보존하십시오.

For **Quantity-Based** plans, set the **Minimum Quantity** (minimum seats required) and optionally a **Maximum Quantity** to cap how many seats a subscriber can purchase.

## Pricing tiers

Pricing tiers define the billing frequency and discount options available to customers on this plan. Add them in the **Pricing Tiers** section below the main form.

Each tier has these fields:

- **Tier Name** — The label shown to customers (e.g., `Monthly`, `Annual — Save 20%`). Supports translations.
- **Billing Cycle** — How often the customer is charged: Daily, Weekly, Monthly, Quarterly, Semi-Annual, or Annual.
- **Billing Interval** — The multiplier for the billing cycle. Set to `2` with Monthly to bill every 2 months.
- **Discount Percentage** — The discount applied to the product price for this tier. Set to `0` for full price, or `20` to give 20% off. This discount stacks on top of any sale pricing on the product itself.
- **Default Tier** — Mark one tier as the default to pre-select it for customers when they view the subscription options.

The discount applies starting from the customer's very first billing cycle, not just on renewals — a tier with a 20% discount charges 20% off from day one (or from the first charge after a trial, if the plan has one).

### Example: tiered plan with three options

For a "Coffee Club" subscription plan:

| Tier Name | Billing Cycle | Discount |
|-----------|---------------|----------|
| Monthly | Monthly | 0% |
| Quarterly — Save 10% | Quarterly | 10% |
| Annual — Save 20% | Annual | 20% |

## Trial period

A trial period lets customers try your subscription before their first full charge. Configure this in the **Trial Period** section:

- **Trial Period (Days)** — Number of free trial days. Set to `0` to disable trials. Maximum is 365 days.
- **Trial Price** — Optional reduced price during the trial (e.g., $1 for the first month). Leave empty for a completely free trial.

## Cancellation policy

Preserve all markdown formatting, image paths, code blocks, and technical terms.

구독 취소 방법을 **취소 정책** 섹션에서 제어합니다:

| 정책 | 설명 |
|--------|-------------|
| **언제든 취소** | 고객이 언제든 즉시 취소할 수 있습니다 |
| **기간 종료 시 취소** | 취소는 지불 기간의 끝에서 적용됩니다. 고객은 만료 시점까지 액세스를 유지합니다 |
| **최소 계약 기간 필요** | 고객은 취소하기 전에 최소한의 요금 청구 주기를 완료해야 합니다 |

추가 설정:

- **최소 계약 기간 (회차)** — 계약 정책을 사용할 때, 요금 청구 주기의 수를 설정합니다 (예: 3개월 최소 기간에 `3`을 입력합니다).
- **유예 기간 (일)** — 결제 실패 후 구독이 중단되기 전까지의 추가 액세스 기간입니다. 즉시 중단을 원할 경우 `0`을 설정합니다.
- **재활성화 기간 (일)** — 고객이 구독을 다시 활성화할 수 있는 취소 후 기간입니다. 다시 구독하지 않고도 재활성화할 수 있습니다.

## 플랜 변경 행동

고객이 플랜 간에 업그레이드 또는 다운그레이드할 때, 변경 사항이 적용되는 시점을 제어할 수 있습니다:

- **업그레이드 행동** — **즉시** (지연된 금액을 현재 청구) 또는 **만료 시** (다음 요금 납부일에 전환)로 설정합니다.
- **다운그레이드 행동** — **즉시** (다음 청구에 크레딧 적용) 또는 **만료 시** (다음 요금 납부일에 전환)로 설정합니다.

## 제한 및 제약 조건

- **최대 요금 청구 주기** — 구독이 자동으로 종료되기 전까지의 총 요금 청구 주기 수입니다. 무제한 반복 요금을 원할 경우 비워 두세요. 일시적인 계획 또는 시간 제한 구독에 유용합니다.
- **설치 비용** — 구독이 처음 생성될 때 청구되는 일회성 비용입니다 (예: 온boarding 또는 활성화 비용). 설치 비용이 없는 경우 `0.00`을 설정합니다.

## 플랜 추가 요금

추가 요금은 구독자가 플랜에 첨부할 수 있는 선택적 추가 요금입니다. **플랜 추가 요금** 섹션에서 추가합니다:

- **추가 요금 이름** — 고객에게 표시되는 이름입니다.

모든 마크다운 포맷, 이미지 경로, 코드 블록, 기술 용어를 보존합니다.

번역을 지원합니다.
- **설명** — 애드온이 제공하는 내용입니다.
- **가격** — 애드온의 비용입니다.
- **청구 주기** — 애드온이 **청구 주기별** (정기)로 청구되는지, 구독 시작 시 **일회성**으로 청구되는지를 나타냅니다.
- **수량 허용** — 고객이 애드온을 여러 단위로 구매할 수 있도록 합니다.
- **필수** — 새 구독에 항상 애드온이 포함되도록 체크합니다.

필수 애드온은 고객이 제거할 수 없습니다.

## 보기 및 상태

- **활성** — 새 구독을 생성할 수 없도록 계획을 비활성화하려면 체크를 해제하십시오. 기존 구독에는 영향을 주지 않습니다.
- **공개** — 고객이 보는 페이지에서 계획을 숨기려면 체크를 해제하십시오 (기존 구독자들이 여전히 사용하는 내부 또는 구형 계획에 유용합니다).
- **정렬 순서** — 구독 선택 페이지에서 표시 순서를 제어합니다. 낮은 숫자가 먼저 표시됩니다.

## 팁

- **체험 기간**을 설정하여 고객의 망설임을 줄이십시오 — 구독 제품에서 7일 무료 체험과 같은 짧은 기간이라도 전환율을 크게 높일 수 있습니다.
- **세 가지 가격 대** (월간, 분기별, 연간)를 설정하여 연간 계약을 유도하고 현금 흐름을 개선하십시오.
- 서비스 기반 구독의 경우, **해지 정책**을 **기간 종료 시 해지**로 설정하여 고객이 지불 기간 동안 접근 권한을 유지하도록 하십시오. 이는 공정하게 느끼게 하고 청구서 반환을 줄입니다.
- 결제 실패 시 **이 Jaco 기간**을 3~7일로 유지하십시오. 고객이 접근을 잃기 전에 결제 방법을 업데이트할 시간을 줍니다.
- **필수** 플래그는 애드온에 대해 신중하게 사용하십시오. 진정한 필수 항목(예: 서비스 계약)에만 사용하고, 가격을 높이려는 수단으로 사용하지 마십시오.
- 구독자가 없는 계획은 삭제 대신 비활성화하십시오 — 이는 이전에 구독한 고객을 위한 역사적 데이터를 보존합니다.