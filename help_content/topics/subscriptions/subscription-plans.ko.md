---
title: 구독 플랜
---

구독 플랜을 사용하면 제품을 정기 결제로 제공할 수 있습니다 — 소모품, 서비스, 큐레이션 박스 또는 고객이 반복적으로 구매하는 모든 제품에 이상적입니다. 이 가이드에서는 플랜을 생성하고 구성하는 방법, 가격 티어를 설정하는 방법, 시험 기간을 추가하는 방법 및 선택적 추가 항목을 연결하는 방법을 설명합니다.

## 시작하기

관리자 사이드바에서 **구독 > 구독 플랜**으로 이동하세요. 플랜 목록에는 가격 모델, 활성 구독자 수 및 가시성 상태가 포함된 모든 플랜이 표시됩니다.

![구독 플랜 목록](/static/core/admin/img/help/subscription-plans/plan-list.webp)

새 플랜을 생성하려면 **마법사로 생성** 버튼을 클릭하세요 — 이 버튼은 플랜 생성 마법사를 열어 설정을 단계별로 안내합니다. 그 옆의 **+ 플랜 추가** 버튼은 모든 것을 수동으로 구성하려는 상인을 위한 빈 양식을 엽니다.

플랜 자체만으로는 구매할 수 없습니다 — 이는 템플릿입니다. 여기서 플랜을 구축한 후, 고객이 실제로 구독할 수 있도록 제품(단일, 변수, 디지털 제품만 해당)의 **구독** 탭에서 하나 이상의 제품에 연결하세요. 해당 단계에 대해서는 [제품을 구독으로 판매하기](/help/selling-products-as-subscriptions)를 참조하세요.

## 플랜 편집기

기존 플랜을 열면(목록에서 이름 또는 연필 아이콘을 클릭) 플랜 편집기로 이동합니다. 헤더에는 플랜 이름, 가격 모델, **활성**/**비활성** 및 **공개**/**비공개** 상태 배지, 그리고 생성 날짜가 표시됩니다. 헤더 오른쪽 상단의 두 버튼은 변경 사항을 저장합니다 — 체크 원 아이콘은 저장 후 목록으로 돌아가고, 일반 체크 아이콘은 페이지에 머물러 계속 편집할 수 있도록 저장합니다.

헤더 아래에는 플랜을 한눈에 요약하는 통계 스트립이 있습니다: **활성 구독**, **가격 티어**, **추가 항목**, **총 매출**.

양식의 나머지 부분은 다섯 개의 탭으로 구성됩니다:

{"| Tab | What it contains |\n|-----|-------------------|\n| **General** | Plan Information (name, slug, description) and Status (active/public) |\n| **Pricing** | Pricing Configuration, Trial Period, and Limits & Restrictions |\n| **Tiers & Add-ons** | The Pricing Tiers and Add-ons editors |\n| **Lifecycle** | Cancellation Policy and Plan Change Behavior |\n| **Advanced** | Provider Integration and Statistics |\n|\nThe sections below walk through each tab's settings. When you create a brand-new plan directly from **+ Add Plan** (rather than the wizard), the same fields appear in a single scrollable form instead of tabs — save the plan once and reopen it to get the full tabbed editor.\n|\n## Plan information (General tab)\n|\nThe **Plan Information** card captures the core identity of your plan.\n|\n- **Plan Name** — The name customers see when subscribing. Click the globe icon to add translations for other store languages.\n- **Slug** — A URL-friendly identifier auto-generated from the name (e.g., `premium-plan`). This is used internally and in integrations.\n- **Description** — Optional text describing what the plan includes. Supports translations.\n|\nThe **Status** card on the same tab controls the **Active** and **Public** toggles — see [Visibility and status](#visibility-and-status) below.\n|\n![General tab of the plan editor](/static/core/admin/img/help/subscription-plans/edit-form-general-tab.webp)\n|\n## Pricing model (Pricing tab)\n|\nThe **Pricing Configuration** card controls how pricing is structured for this plan:\n|\n| Pricing Model | Best For |\n|---------------|----------|\n| **Tiered Pricing** | Offering monthly, quarterly, and annual commitment options with discounts for longer terms |\n| **Quantity-Based** | Per-seat or per-user pricing where the total scales with quantity (e.g., team licenses) |\n| **Flat Rate** | A single fixed price with no variations |\n|\nPreserve all markdown formatting, image paths, code blocks, and technical terms."}

**수량 기반** 플랜의 경우, **수량 허용**을 선택하고 **최소 수량**(필요한 최소 좌석 수)을 설정하며, 구독자가 구매할 수 있는 좌석 수를 제한하기 위해 선택적으로 **최대 수량**을 설정할 수 있습니다.

![플랜 편집기의 가격 탭](/static/core/admin/img/help/subscription-plans/edit-form-pricing-tab.webp)

## 가격 등급 (등급 및 추가 항목 탭)

가격 등급은 이 플랜에서 고객이 사용할 수 있는 청구 주기 및 할인 옵션을 정의합니다. **등급 및 추가 항목** 탭의 **가격 등급** 카드에서 추가 항목 편집기 옆에 추가하십시오.

각 등급에는 다음 필드가 있습니다:

- **등급 이름** — 고객에게 표시되는 라벨(예: `월간`, `연간 — 20% 절약`). 번역을 지원합니다.
- **청구 주기** — 고객이 청구되는 빈도: 일간, 주간, 월간, 분기별, 반기별 또는 연간.
- **청구 간격** — 청구 주기의 배수. 월간으로 `2`를 설정하면 2개월마다 청구됩니다.
- **할인율** — 이 등급에 적용되는 제품 가격 할인율. 정가인 경우 `0`으로, 20% 할인인 경우 `20`으로 설정합니다. 이 할인은 제품 자체의 세일 가격 위에 중첩됩니다.
- **기본 등급** — 고객이 구독 옵션을 볼 때 미리 선택되도록 한 등급을 기본으로 표시합니다.

할인은 갱신 시에만 적용되는 것이 아니라 고객의 첫 번째 청구 주기부터 적용됩니다 — 20% 할인 등급은 첫날부터(또는 플랜에 시험 기간이 있는 경우 시험 기간 후 첫 청구부터) 20% 할인된 금액으로 청구됩니다.

### 예시: 세 가지 옵션이 있는 등급별 플랜

"커피 클럽" 구독 플랜의 경우:

| 등급 이름 | 청구 주기 | 할인 |
|-----------|---------------|----------|
| 월간 | 월간 | 0% |
| 분기별 — 10% 절약 | 분기별 | 10% |
| 연간 — 20% 절약 | 연간 | 20% |

## 플랜 추가 항목 (등급 및 추가 항목 탭)

추가 항목은 구독자가 플랜에 연결할 수 있는 선택적 부가 기능입니다. 같은 탭에서 가격 등급 바로 아래에 있는 **추가 항목** 카드에 추가하십시오:

- **추가 항목 이름** — 고객에게 표시되는 이름.

번역을 지원합니다.
- **설명** — 추가 기능이 제공하는 내용.
- **가격** — 추가 기능의 비용.
- **청구 주기** — 추가 기능이 구독 시작 시 **청구 주기별**(정기) 또는 **일시불**로 청구되는지 여부.
- **수량 허용** — 고객이 추가 기능의 여러 단위를 구매할 수 있도록 활성화합니다.
- **필수** — 이 항목을 선택하면 모든 신규 구독에 추가 기능이 자동으로 포함됩니다.

필수 추가 기능은 고객이 제거할 수 없습니다.

![플랜 편집기의 티어 및 추가 기능 탭](/static/core/admin/img/help/subscription-plans/edit-form-tiers-addons-tab.webp)

## 시험 기간 (가격 탭)

시험 기간은 고객이 첫 번째 전체 청구 전에 구독을 사용해 볼 수 있게 합니다. 가격 구성 아래에 있는 **시험 기간** 카드에서 이 내용을 구성합니다:

- **시험 기간 (일)** — 무료 시험 기간의 일수. `0`으로 설정하면 시험 기간을 비활성화합니다. 최대 365일입니다.
- **시험 가격** — 시험 기간 동안 적용되는 선택적 할인 가격(예: 첫 달 $1). 완전히 무료 시험 기간을 원하면 비워 두세요.

## 제한 및 규정 (가격 탭)

**제한 및 규정** 카드도 가격 탭에 있으며 다음 내용을 포함합니다:

- **최대 청구 주기** — 구독이 자동으로 종료되기 전의 총 청구 주기 수. 무제한 정기 청구를 원하면 비워 두세요. 할부 결제 플랜이나 기간이 정해진 구독에 유용합니다.

**설정 수수료**와 **정렬 순서**는 이 카드의 일부가 아닙니다. **마법사로 생성** 플로우를 통해 플랜을 처음 만들 때 한 번만 설정되며, 이후 편집 화면에서 변경할 수 없습니다. 이 값 중 하나를 조정해야 하는 경우, 기존 플랜을 편집하는 대신 플랜을 비활성화하고 마법사로 다시 생성하세요. 이 릴리스에서는 설정 수수료가 체크아웃 시 자동으로 청구되지 않으므로, 해당 필드를 작동하는 청구가 아닌 향후 업데이트를 위해 예약된 필드로 간주하세요.

## 취소 정책 (라이프사이클 탭)

**취소 정책** 카드에서 고객이 구독을 취소하는 방법을 제어합니다:

| 정책 | 설명 |
|--------|-------------|
| **언제든 취소** | 고객은 언제든 즉시 취소할 수 있습니다 |
| **기간 종료 시 취소** | 취소는 지불 기간의 끝에서 적용됩니다. -- 고객은 만료 시점까지 액세스를 유지합니다 |
| **최소 결제 기간 필요** | 고객은 취소하기 전에 최소한의 결제 주기를 완료해야 합니다 |

추가 설정:

- **최소 결제 기간 (주기)** — 결제 정책을 사용할 때, 결제 주기의 수를 설정합니다 (예: 3개월 최소 기간에 대해 `3`). 
- **유예 기간 (일)** — 구독이 중단되기 전에 결제 실패 후 계속 액세스할 수 있는 일수입니다. 즉시 중단을 원할 경우 `0`으로 설정합니다. 
- **재활성화 기간 (일)** — 고객이 구독을 다시 활성화할 수 있는 취소 후 기간입니다. 다시 구독하지 않고도 시작할 수 있습니다. 

## 구독 변경 행동 (라이프사이클 탭)

**구독 변경 행동** 카드는 고객이 구독 계획을 업그레이드하거나 다운그레이드할 때 발생하는 행동을 제어합니다:

- **업그레이드 행동** — **즉시** (지금 프로 레이티드 금액을 청구) 또는 **만료 시** (다음 결제 날짜에 전환)로 설정합니다.
- **다운그레이드 행동** — **즉시** (다음 청구에 크레딧 적용) 또는 **만료 시** (다음 결제 날짜에 전환)로 설정합니다.

![구독 계획 편집기의 라이프사이클 탭](/static/core/admin/img/help/subscription-plans/edit-form-lifecycle-tab.webp)

## 고급 탭

**고급** 탭은 일상적으로 사용하지 않는 설정이 포함되어 있습니다:

- **결제 제공업체 통합** — 이 계획을 결제 제공업체의 계획/가격 ID와 매핑합니다 (예: `"stripe": "price_xxx", "paypal": "P-xxx"`). 제공업체를 통해 자체적으로 구독을 관리하는 스토어에 적합합니다. Spwig의 자체 청구 엔진을 사용하지 않습니다.
- **통계** — 읽기 전용 값: **활성 구독**, **총 수입**, 그리고 계획의 **생성일** / **수정일** 타임스탬프입니다. 이는 페이지 상단의 통계 스트립과 동일합니다.

[/static/core/admin/img/help/subscription-plans/edit-form-advanced-tab.webp] 대체 텍스트

## 노출 및 상태 (일반 탭)

- **활성** — 새 구독을 생성할 수 없도록 하려면 체크를 해제하십시오. 기존 구독에는 영향을 주지 않습니다.
- **공개** — 고객이 보는 페이지에서 이 플랜을 숨기려면 체크를 해제하십시오 (기존 구독자들이 여전히 있는 내부 또는 구식 플랜에 유용합니다).

## 팁

- 구독 제품에서 구매 결정을 줄이려면 **체험 기간**을 사용하십시오 — 짧은 7일 무료 체험도 전환율을 크게 높일 수 있습니다.
- **세 가지 가격 대** (월간, 분기별, 연간)를 설정하여 할인을 증가시켜 연간 계약을 장려하고 수익 흐름을 개선하십시오.
- 서비스 기반 구독의 경우, **해지 정책**을 **기간 종료 시 해지**로 설정하십시오. 고객이 지불 기간 동안 액세스를 유지하게 하면 공정하게 느끼게 하고 청구서 반환을 줄입니다.
- 결제 실패 시 **유예 기간**을 3~7일로 유지하십시오. 액세스를 잃기 전에 고객이 결제 방법을 업데이트할 시간을 줍니다.
- 추가 기능에 **필수** 플래그를 사용할 때는 신중하게 사용하십시오. 이는 진짜로 필수적인 것들(예: 서비스 계약)에만 사용하되, 가격을 높이려는 수단으로 사용하지 마십시오.
- 구독자가 없는 플랜을 삭제하는 대신 비활성화하십시오 — 이는 이전에 구독했던 고객을 위한 역사적 데이터를 보존합니다.