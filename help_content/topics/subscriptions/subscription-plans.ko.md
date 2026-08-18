---
title: 구독 요금제
---

구독 요금제를 통해 제품에 대해 반복 결제를 제공할 수 있습니다. 소모품, 서비스, 정해진 상자, 또는 고객이 반복적으로 구매하는 제품에 이상적입니다. 이 가이드는 요금제를 생성하고 구성하는 방법, 가격 대역 설정, 체험 기간 추가, 선택적인 추가 요금제를 첨부하는 방법을 설명합니다.

## 시작하기

관리자 사이드바에서 **구독 > 구독 요금제**로 이동하세요. 요금제 목록은 현재 활성 상태인 구독자 수와 표시 상태를 포함하여 모든 요금제를 보여줍니다.

![구독 요금제 목록](/static/core/admin/img/help/subscription-plans/plan-list.webp)

새로운 요금제를 만들려면 **마법사로 생성** 버튼을 클릭하세요 — 이는 단계별로 설정을 안내하는 요금제 생성 마법사를 여는 버튼입니다. 그 옆에 있는 **+ 요금제 추가** 버튼은 직접 모든 설정을 구성하려는 상인을 위해 빈 폼을 여는 버튼입니다.

단독으로 존재하는 요금제는 구매할 수 없습니다. 이는 템플릿일 뿐입니다. 여기서 이 요금제를 생성한 후 제품의 **구독** 탭에서 하나 이상의 제품에 연결해야 합니다 (단순, 변수형, 디지털 제품만 해당됨). 고객이 실제로 구독할 수 있도록 하기 위해요. 그 다음 단계는 [제품을 구독으로 판매하는 방법](/help/selling-products-as-subscriptions)을 참조하십시오.

## 요금제 편집기

기존 요금제를 여는 방법은 목록에서 이름을 클릭하거나铅笔 아이콘을 클릭하는 것입니다. 헤더에는 요금제 이름, 가격 모델, **활성**/**비활성**, **공개**/**비공개** 상태 표시줄, 그리고 생성 날짜가 표시됩니다. 헤더의 상단 오른쪽 모서리에 있는 두 개의 버튼은 변경 사항을 저장합니다. 체크-원(circle) 아이콘은 목록으로 돌아가서 저장하고, 일반 체크 아이콘은 페이지에 머무르며 계속 편집할 수 있도록 합니다.

헤더 아래에는 요금제의 요약 정보를 보여주는 통계 스트립이 있습니다: **활성 구독**, **가격 대역**, **추가 요금**, **총 수익**.

나머지 폼은 다섯 개의 탭으로 구성되어 있습니다.

| 탭 | 포함 내용 |
|-----|-------------------|
| **일반** | 플랜 정보 (이름, 슬러그, 설명) 및 상태 (활성/공개) |
| **가격** | 가격 구성, 무료 체험 기간 및 제한 및 제약 |
| **단계 및 추가 요금** | 가격 단계 및 추가 요금 편집기 |
| **수명 주기** | 취소 정책 및 플랜 변경 행동 |
| **고급** | 공급자 통합 및 통계 |

아래 섹션에서는 각 탭의 설정을 단계별로 안내합니다. **+ Add Plan**에서 새 플랜을 직접 생성할 때 (마법사 대신), 동일한 필드가 탭 대신 단일 스크롤 가능한 폼에 표시됩니다. 플랜을 저장한 후 다시 열면 전체 탭 기반 편집기를 얻을 수 있습니다.

## 플랜 정보 (일반 탭)

**플랜 정보** 카드는 플랜의 핵심 정체성을 포착합니다.

- **플랜 이름** — 구독 시 고객이 보는 이름입니다. 다른 스토어 언어에 대한 번역을 추가하려면 세계 지도 아이콘을 클릭하십시오.
- **슬러그** — 이름에서 자동 생성된 URL 친화적인 식별자 (예: `premium-plan`). 이는 내부에서 사용되며 통합에도 사용됩니다.
- **설명** — 플랜에 포함된 내용을 설명하는 선택적 텍스트입니다. 번역을 지원합니다.

이 탭의 **상태** 카드는 **활성** 및 **공개** 토글을 제어합니다. 아래의 [보기 및 상태](#visibility-and-status)를 참조하십시오.

![플랜 편집기의 일반 탭](/static/core/admin/img/help/subscription-plans/edit-form-general-tab.webp)

## 가격 모델 (가격 탭)

**가격 구성** 카드는 이 플랜에 대한 가격 구조를 제어합니다:

| 가격 모델 | 최적의 경우 |
|---------------|----------|
| **단계별 가격** | 더 긴 기간에 대한 할인을 제공하는 월간, 분기별, 연간 구독 옵션 제공 |
| **양 기반** | 사용자당 또는 사용자당 가격으로, 총액이 수량에 따라 증가합니다 (예: 팀 라이선스) |
| **고정 요금** | 변형이 없는 단일 고정 가격 |

모든 마크다운 포맷, 이미지 경로, 코드 블록, 기술 용어를 보존하십시오.

For **Quantity-Based** plans, check **Allow Quantity** and set the **Minimum Quantity** (minimum seats required) and optionally a **Maximum Quantity** to cap how many seats a subscriber can purchase.

![Pricing tab of the plan editor](/static/core/admin/img/help/subscription-plans/edit-form-pricing-tab.webp)

## Pricing tiers (Tiers & Add-ons tab)

Pricing tiers define the billing frequency and discount options available to customers on this plan. Add them in the **Pricing Tiers** card on the **Tiers & Add-ons** tab, alongside the Add-ons editor.

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

## Plan add-ons (Tiers & Add-ons tab)

Add-ons are optional extras that subscribers can attach to their plan. Add them in the **Add-ons** card, directly below Pricing Tiers on the same tab:

- **Add-on Name** — The name shown to customers.

번역을 지원합니다.
- **설명** — 애드온이 제공하는 내용입니다.
- **가격** — 애드온의 비용입니다.
- **청구 주기** — 애드온이 **청구 주기별** (재발)로 청구되는지, 구독 시작 시 **일회성**으로 청구되는지를 나타냅니다.
- **수량 허용** — 고객이 애드온을 여러 단위로 구매할 수 있도록 합니다.
- **필수** — 모든 새 구독에 자동으로 애드온을 포함시킵니다.

필수 애드온은 고객이 제거할 수 없습니다.

![구독 계획 편집기의 레이어 및 애드온 탭](/static/core/admin/img/help/subscription-plans/edit-form-tiers-addons-tab.webp)

## 체험 기간 (가격 설정 탭)

체험 기간은 고객이 첫 번째 정상 청구 전에 구독을 시도할 수 있도록 합니다. 이 설정은 **체험 기간** 카드에 아래에 있는 가격 설정 구성에서 구성할 수 있습니다:

- **체험 기간 (일)** — 무료 체험 기간 일수입니다. 체험을 비활성화하려면 `0`으로 설정하십시오. 최대 365일까지 설정할 수 있습니다.
- **체험 가격** — 체험 기간 동안 선택적으로 낮은 가격을 설정합니다 (예: 첫 달에 $1). 완전히 무료 체험을 원한다면 비워 두세요.

## 제한 및 제약 조건 (가격 설정 탭)

**제한 및 제약 조건** 카드는 가격 설정 탭에 있으며 다음을 포함합니다:

- **최대 청구 주기** — 구독이 자동으로 종료되는 청구 주기의 총 수입니다. 무제한 재발 청구를 원하시면 비워 두세요. 할부 계획이나 시간 제한이 있는 구독에 유용합니다.

**설치 비용** 및 **정렬 순서**는 이 카드의 일부가 아닙니다. 이는 **마법사로 생성** 흐름을 통해 처음으로 계획을 생성할 때 설정되며, 이후 편집 화면에서 변경할 수 없습니다. 이 값을 조정해야 하는 경우, 기존 계획을 편집하는 대신 계획을 비활성화하고 마법사를 사용하여 다시 생성해야 합니다. 이 버전에서는 설치 비용이 체크아웃 시 자동으로 청구되지 않으므로, 이 필드는 작업 중인 청구가 아닌 미래 업데이트를 위한 예약 필드로 간주해야 합니다.

## 취소 정책 (라이프사이클 탭)

**취소 정책** 카드에서 고객이 구독을 어떻게 취소할 수 있는지 제어할 수 있습니다.

| 정책 | 설명 |
|--------|-------------|
| **언제든 취소** | 고객은 언제든 즉시 취소할 수 있습니다 |
| **기간 종료 시 취소** | 취소는 지불 기간의 끝에서 적용됩니다. -- 고객은 만료 시점까지 액세스를 유지합니다 |
| **최소 결제 기간 필요** | 고객은 취소하기 전에 최소한의 결제 주기를 완료해야 합니다 |

추가 설정:

- **최소 결제 기간 (주기)** — 결제 정책을 사용할 때, 결제 주기의 수를 설정합니다 (예: 3개월 최소 기간에 대해 `3`). 
- **유예 기간 (일)** — 구독이 중단되기 전에 결제 실패 후 계속 액세스할 수 있는 일수입니다. 즉시 중단을 원할 경우 `0`으로 설정합니다. 
- **재활성화 기간 (일)** — 고객이 구독을 다시 활성화할 수 있는 취소 후 일수입니다. 다시 구독하지 않고도 구독을 재활성화할 수 있습니다. 

## 구독 변경 행동 (라이프사이클 탭)

**구독 변경 행동** 카드는 아래에 있는 **취소 정책** 다음에 위치합니다. 고객이 구독 계획을 업그레이드하거나 다운그레이드할 때 발생하는 행동을 제어합니다:

- **업그레이드 행동** — **즉시** (지금 프로 레이티드 금액을 청구) 또는 **만료 시** (다음 결제 날짜에 전환)로 설정합니다.
- **다운그레이드 행동** — **즉시** (다음 청구에 크레딧 적용) 또는 **만료 시** (다음 결제 날짜에 전환)로 설정합니다.

![구독 계획 편집기의 라이프사이클 탭](/static/core/admin/img/help/subscription-plans/edit-form-lifecycle-tab.webp)

## 고급 탭

**고급** 탭은 일상적으로 사용하지 않는 설정이 포함되어 있습니다:

- **결제 제공업체 통합** — 이 계획을 결제 제공업체에서 제공하는 계획/가격 ID와 매핑합니다 (예: `"stripe": "price_xxx", "paypal": "P-xxx"`). 제공업체를 통해 자체적으로 구독을 관리하는 스토어에 적합합니다. Spwig의 자체 결제 엔진을 사용하지 않고요.
- **통계** — 읽기 전용 값: **활성 구독**, **총 수입**, 그리고 이 계획의 **생성일** / **수정일** 타임스탬프입니다. 이는 페이지 상단의 통계 스트립과 동일합니다.

모든 마크다운 포맷, 이미지 경로, 코드 블록, 기술 용어를 보존합니다.

[/static/core/admin/img/help/subscription-plans/edit-form-advanced-tab.webp] 대체 텍스트

## 노출 및 상태 (일반 탭)

- **활성** — 새 구독을 생성할 수 없도록 하려면 체크를 해제하십시오. 기존 구독에는 영향을 주지 않습니다.
- **공개** — 고객이 보는 페이지에서 이 플랜을 숨기려면 체크를 해제하십시오 (기존 구독자들이 여전히 있는 내부 또는 구식 플랜에 유용합니다).

## 팁

- 구독 제품에서 구매 결정을 줄이려면 **체험 기간**을 사용하십시오 — 짧은 7일 무료 체험도 전환율을 크게 높일 수 있습니다.
- **세 가지 가격 대** (월간, 분기별, 연간)를 설정하여 할인을 증가시켜 연간 계약을 장려하고 현금 흐름을 개선하십시오.
- 서비스 기반 구독의 경우, **해지 정책**을 **기간 종료 시 해지**로 설정하십시오. 고객이 지불 기간 동안 액세스를 유지하게 하면 공정하게 느끼게 하고 청구서 반환을 줄입니다.
- 결제 실패 시 **유예 기간**을 3~7일로 유지하십시오. 액세스를 잃기 전에 고객이 결제 방법을 업데이트할 시간을 줍니다.
- 추가 기능에 **필수** 플래그를 사용할 때는 신중하게 사용하십시오. 이는 진정으로 필수적인 것(예: 서비스 계약)에만 사용하고 가격을 높이려는 수단으로 사용하지 마십시오.
- 구독자가 없는 플랜을 삭제하는 대신 비활성화하십시오 — 이는 이전에 구독했던 고객을 위한 역사적 데이터를 보존합니다.