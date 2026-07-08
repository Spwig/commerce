---
title: 고객 구독 관리
---

고객 구독 섹션은 가게에서 활성, 일시 중지, 취소된 반복 구독의 전체적인 뷰를 제공합니다. 여기서부터 청구 건강 상태를 모니터링하고, 개별 구독 세부 정보를 볼 수 있으며, 문제가 발생할 때 조치를 취할 수 있습니다.

## 고객 구독 보기

**구독 > 고객 구독**으로 이동하여 모든 고객의 구독 전체 목록을 볼 수 있습니다.

![고객 구독 목록](/static/core/admin/img/help/managing-subscriptions/subscription-list.webp)

목록은 각 구독의 고객, 계획 이름, 현재 상태, 다음 청구 날짜 및 완료된 청구 주기 수를 보여줍니다.

### 필터링 및 검색

오른쪽의 필터 패널을 사용하여 다음으로 구독을 좁힐 수 있습니다:

- **상태** — 활성, 시험, 과거 미결제, 일시 중지, 취소, 만료 상태로 필터
- **계획** — 특정 계획의 구독 보기
- **공급업체 모드** — 네이티브 (Stripe/PayPal 관리) 또는 대체 (내부 청구)

검색 바를 사용하여 고객 이메일 주소로 구독을 찾을 수 있습니다.

## 구독 상태

각 상태를 이해하면 주의가 필요한 구독을 식별할 수 있습니다:

| 상태 | 의미 |
|------|------|
| **시험** | 고객이 무료 또는 할인된 가격의 시험 기간에 있습니다 |
| **활성** | 구독이 건강합니다 — 청구가 최신이고 액세스가 활성화되어 있습니다 |
| **과거 미결제** | 결제 시도가 실패했습니다 — 시스템이 재시도하고 있습니다. 고객은 유예 기간 동안 액세스를 유지합니다 |
| **일시 중지** | 구독이 일시적으로 중단되었습니다 — 청구 없이 액세스 없음 |
| **취소** | 취소 요청이 처리되었습니다. 고객은 기간 종료 날짜까지 액세스를 계속할 수 있습니다 |
| **만료** | 구독이 완전히 종료되었습니다 — 시험 기간이 끝났거나 최대 청구 주기 수에 도달했거나, 취소 기간이 지났습니다 |

**과거 미결제** 상태의 구독은 가장 많은 주의가 필요합니다 — 결제가 계속 실패하고 유예 기간이 끝나면 구독이 일시 중지됩니다.

## 구독 세부 정보 보기

구독을 클릭하여 상세 보기 창을 엽니다.

이렇게 표시됩니다:

### 현재 요금제 기간

- **현재 기간 시작 / 종료** — 활성 요금제 기간의 날짜
- **다음 요금제 날짜** — 다음 요금이 청구될 날짜
- **최근 요금제 날짜** 및 **최근 요금제 상태** — 가장 최근의 요금 청구 시도 결과
- **요금제 주기 수** — 성공적으로 완료된 요금제 주기 수

### 구독 정보

- **Plan** 및 **Pricing Tier** — 고객이 사용 중인 요금제 및 요금 주기
- **Product / Variant** — 이 구독에 연결된 카탈로그 상품 (적용 가능한 경우)
- **Quantity** — 좌석 수 또는 단위 수 (수량 기반 요금제의 경우)
- **Payment Token** — 반복 요금제에 사용되는 저장된 결제 방법

### 시도 기간 세부 정보

구독이 시도 기간 중이라면 **시도 기간 종료일**은 고객의 시도 기간이 만료되고 전체 요금제가 시작되는 날짜를 표시합니다.

### 해지 세부 정보

해지된 구독의 경우 다음과 같은 정보를 확인할 수 있습니다:

- **해지 유형** — 해지가 즉시, 기간 종료 시, 또는 예약된 해지인지 여부
- **해지 요청일** — 해지가 요청된 날짜
- **해지 사유** — 고객이 해지한 이유에 대한 메모 (기록된 경우)
- **재등록 마감일** — 고객이 다시 등록할 수 있는 마지막 날짜 (처음부터 다시 구독하지 않고도)

### 유예 기간 및 약속

- **유예 기간 종료일** — 결제가 실패한 경우, 액세스가 중단되기 전의 마감일을 표시합니다.
- **최소 약속 종료일** — 최소 약속이 있는 요금제의 경우, 가장 빠른 해지 날짜

## 구독 일시 중지

일시 중지된 구독은 일시적으로 요금 청구를 중단하면서 액세스도 중단합니다. 이는 고객이 완전히 해지하지 않고 휴식을 취하고자 할 때 유용합니다.

일시 중지된 구독을 보려면 **상태: 일시 중지**로 필터링합니다. 상세 보기에서는 다음과 같은 정보를 확인할 수 있습니다:

- **Paused At** — When the pause began
- **Pause Reason** — Notes on why it was paused
- **Auto Resume Date** — If set, the date the subscription will automatically resume billing and access

Subscriptions resume either on the auto-resume date or when the customer manually reactivates.

## Billing cycle logs

Every billing attempt — successful or failed — is recorded in the billing cycle log. Navigate to **Subscriptions > Billing Cycle Logs** to view this history.

![Billing cycle log list](/static/core/admin/img/help/managing-subscriptions/billing-cycle-log.webp)

### Reading a billing cycle log entry

Each log entry records:

- **Subscription** — Which customer subscription this billing attempt belongs to
- **Cycle Number** — Sequential billing cycle (Cycle 1 = first charge after trial)
- **Billing Date** — When the charge was attempted
- **Status** — Pending, Processing, Successful, Failed, or Retrying
- **Amount breakdown**:
  - **Base Amount** — The plan price before any adjustments
  - **Quantity Amount** — Additional charge for the quantity of seats/units
  - **Add-ons Amount** — Total cost of active add-ons
  - **Discount Amount** — Total discounts applied
  - **Total Amount** — The final amount charged (or attempted)
- **Payment Method** — The card or payment method used
- **Provider Transaction ID** — The payment provider's reference number (useful for refund lookups)
- **Failure Reason** — If the billing failed, why it failed (e.g., card declined, insufficient funds)

### Diagnosing payment failures

If a customer contacts you about a billing issue, find their subscription and check the billing cycle logs. The **Failure Reason** field explains what went wrong. Common failure reasons include:

- **카드 거부** — 고객의 카드가 은행에 의해 거부되었습니다
- **자금 부족** — 청구 시 계좌 잔액이 너무 낮았습니다
- **만료된 카드** — 저장된 결제 수단이 만료되었습니다
- **네트워크 오류** — 일시적인 결제 제공업체 연결 문제 — 일반적으로 재시도 시 해결됩니다

지속적인 실패의 경우, 고객에게 계정 설정에서 결제 수단을 업데이트하도록 안내하세요.

## 팁

- 주간으로 **과거 미결** 필터를 확인하여 이탈 위험이 있는 구독을 확인하세요. 고객에게 빠르게 이메일을 보내면 일반적으로 유예 기간이 끝나기 전에 결제 문제를 해결할 수 있습니다.
- 청구 주기 로그는 읽기 전용입니다 — 자동으로 생성되며 수정할 수 없습니다. 이는 신뢰할 수 있는 감사 추적을 보장합니다.
- 고객의 구독이 **과거 미결** 상태이지만 이미 결제 수단을 업데이트한 경우, 다음 자동 재시도 시 새 카드가 사용됩니다. 재시도는 계획에서 구성된 유예 기간 일정에 따라 진행됩니다.
- **만료된** 구독은 삭제되지 않습니다 — 보고서에 표시된 채 유지됩니다. 날짜 필터를 사용하여 현재 활성화된 구독에 집중하세요.
- **시범 기간** 중인 구독의 경우, **시범 종료 날짜**를 확인하여 예상되는 첫 번째 청구를 예측하고 결제 수단 문제를 사전에 해결하세요.