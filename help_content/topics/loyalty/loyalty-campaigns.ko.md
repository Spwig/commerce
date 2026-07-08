---
title: 충성도 캠페인
---

충성도 캠페인은 일시적인 프로모션과 일상적인 포인트 적립 규칙을 넘어선 자동화된 보상으로, 고객에게 제공할 수 있습니다. 이를 통해 더블 포인트 주말, 고객의 생일에 보상, 비활성화된 쇼퍼를 되찾고, 특정 그룹의 회원에게 맞춤형 보상을 제공할 수 있습니다.

각 캠페인은 트리거 또는 일정, 적용 대상 회원, 수행할 작업을 정의합니다. 활성화되면 캠페인은 자동으로 실행됩니다. 한 번 설정하면 Spwig이 나머지 작업을 처리합니다.

## 캠페인 유형

| 유형 | 실행 시점 |
|------|---------------|
| **트리거 기반** | 특정 이벤트가 발생할 때 (예: 주문이 이루어지거나, 생일이 감지됨) |
| **일정 기반** | 반복 일정에 따라 (매일, 매주, 매월) |
| **수동** | 관리자에서 명시적으로 실행할 때만 |
| **행동 기반** | 고객이 특정 행동 패턴에 부합할 때 (예: 구매 없이 둘러보기) |

## 캠페인 생성

**프로모션 > 충성도 캠페인**으로 이동하고 **+ 충성도 캠페인 추가**를 클릭합니다.

### 단계 1: 기본 정보

- **이름** — 관리자에서만 보이는 명확하고 설명적인 이름 (예: `생일 보너스 — 200 포인트`)
- **슬러그** — 이름에서 자동 생성됨; 내부적으로 사용됨
- **설명** — 캠페인 목적에 대한 선택적 메모
- **캠페인 유형** — 위 표에서 유형을 선택합니다

### 단계 2: 트리거 또는 일정

**트리거 기반 캠페인**의 경우, 캠페인을 실행하는 **트리거 이벤트**를 설정합니다. 사용 가능한 트리거는 다음과 같습니다:

트리거 조건을 JSON 객체로 추가하여 캠페인 발생 시점을 추가로 필터링할 수 있습니다. 예를 들어, 주문 금액이 $100 이상인 경우에만 트리거하도록 설정할 수 있습니다:

{
  "min_order_amount": 100
}

**예약된 캠페인**의 경우, **스케줄 유형**(일일, 주간, 월간, 또는 커스텀 크론)을 설정하고 **스케줄 설정** 필드에서 시간을 구성합니다:

{
  "hour": 9,
  "minute": 0
}

### 단계 3: actions

**Actions** 필드는 캠페인이 트리거될 때 발생하는 작업을 정의합니다. 작업 객체의 JSON 배열을 입력합니다. 가장 일반적인 작업은 보너스 포인트 부여입니다:

[
  {
    "type": "award_points",
    "points": 200,
    "description": "생일 보너스 — 멤버십을 이용해 주셔서 감사합니다!"
  }
]

다른 사용 가능한 작업에는 이메일 알림을 보내거나 배지 부여가 포함됩니다. 제공업체 구성 요소 문서를 참조하여 전체 목록을 확인하세요.

### 단계 4: targeting

타겟팅 필드를 사용하여 캠페인이 적용되는 회원을 제어합니다:

- **모든 회원 대상** — 기본적으로 선택됨; 캠페인은 모든 활성 충성도 회원에게 적용됩니다
- **세그먼트 대상** — 특정 세그먼트에 속한 회원만 캠페인에 적용합니다(아래 [Segments](#managing-member-segments)을 참조하세요)
- **등급 대상** — 특정 충성도 등급에 속한 회원만 캠페인에 적용합니다

### 단계 5: 제한 및 쿨다운

- **회원당 최대 트리거 수** — 동일한 회원이 이 캠페인에서 혜택을 받을 수 있는 횟수. 생일 보너스와 같은 일회성 보상은 `1`로 설정하세요. 무제한으로 설정하려면 빈칸으로 두세요.
- **쿨다운 일수** — 동일한 회원의 캠페인 트리거 간 최소 일수. 예를 들어, `365`로 설정하여 한 해에 생일 캠페인을 한 번만 실행하도록 방지할 수 있습니다.

### 단계 6: 캠페인 날짜

**시작 날짜**와 **종료 날짜**를 설정하여 캠페인을 시간 제한으로 만듭니다. 두 날짜 모두를 빈칸으로 두면 캠페인은 지속됩니다.

캠페인은 다음 상태 중 하나일 수 있습니다:

| 상태 | 설명 |
|------|------|
| **초안** | 생성되었지만 아직 활성화되지 않았음; 구성 및 테스트에 안전 |
| **활성** | 실행 중이며 조건이 충족되면 트리거 됨 |
| **일시 중지** | 구성 내용을 잃지 않고 일시 중지됨 |
| **종료됨** | 종료 날짜를 지났음; 더 이상 트리거되지 않음 |
| **보관됨** | 활성 목록에서 숨겨졌지만 기록을 위해 보존됨 |

모든 필드를 입력한 후 **저장**을 클릭하세요. 그런 다음 상태를 **활성**으로 변경하여 캠페인을 시작합니다.

## 실용적인 예시

### 예시: 주말 이중 포인트

**시나리오:** 특정 주말 동안 이루어진 모든 구매에 대해 2배의 포인트를 부여합니다.

| 필드 | 값 |
|------|----|
| 이름 | `Double Points Weekend — March` |
| 캠페인 유형 | 트리거 기반 |
| 트리거 이벤트 | 주문 생성 |
| 액션 | `["{\"type\": \"award_points_multiplier\", \"multiplier\": 2.0}"]` |
| 시작 날짜 | 금요일 저녁 |
| 종료 날짜 | 일요일 자정 |
| 모든 회원 대상 | 체크됨 |

### 예시: 생일 보너스

**시나리오:** 충성도 회원에게 생일에 200개의 보너스 포인트를 제공합니다.

| 필드 | 값 |
|------|----|
| 이름 | `Birthday Bonus` |
| 캠페인 유형 | 트리거 기반 |
| 트리거 이벤트 | 고객 생일 |
| 액션 | `["{\"type\": \"award_points\", \"points\": 200, \"description\": \"Happy birthday from us!\"}"]` |
| 회원당 최대 트리거 수 | 1 |
| 쿨다운 일수 | 365 |
| 모든 회원 대상 | 체크됨 |

### 예시: 고객 복귀 캠페인


**시나리오:** 90일 이상 구매하지 않은 회원에게 100포인트 보너스 제공

| 필드 | 값 |
|-------|-------|
| 이름 | `90-Day Win-Back Bonus` |
| 캠페인 유형 | 트리거 기반 |
| 트리거 이벤트 | 90일 비활동 |
| 액션 | `["{\"type\": \"award_points\", \"points\": 100, \"description\": \"We miss you — here are some bonus points\"}"]` |
| 회원당 최대 트리거 수 | 1 |
| 쿨다운 일수 | 180 |
| 모든 회원 대상 | 체크됨 |

## 회원 세그먼트 관리

세그먼트는 특정 충성도 회원 그룹에 캠페인을 대상으로 설정할 수 있습니다. **프로모션 > 충성도 세그먼트**로 이동하여 관리합니다.

### 세그먼트 유형

| 유형 | 설명 |
|------|-------------|
| **규칙 기반** | 규칙에 따라 멤버십이 결정됨 (예: 1,000 포인트 이상인 회원) |
| **동적 계산** | 실시간 기준에서 즉시 계산하여 멤버십이 결정됨 |
| **수동 할당** | 멤버를 수동으로 세그먼트에 추가함 |

### 세그먼트 생성

1. **프로모션 > 충성도 세그먼트**로 이동하고 **+ Add Loyalty Segment**를 클릭합니다.
2. 다음을 입력합니다:
   - **이름** — 설명적인 이름 (예: `High-Value Customers`, `Silver Tier Members`)
   - **Slug** — 자동 생성됨
   - **기준 유형** — 멤버십이 어떻게 결정되는지
   - **기준 구성** — 멤버십 규칙을 정의하는 JSON 객체
3. **저장**을 클릭합니다.

#### 예시: 500포인트 이상인 회원을 위한 세그먼트

```json
{
  "min_available_points": 500
}
```

#### 예시: 금 등급 회원만을 위한 세그먼트

```json
{
  "tier_slugs": ["gold"]
}
```

세그먼트 목록의 **회원 수** 열은 현재 일치하는 회원 수를 표시합니다. 세그먼트를 클릭하고 **Refresh Member Count** 액션을 사용하여 데이터가 변경된 경우 다시 계산합니다.

## 캠페인 성과 추적

### 캠페인 실행 기록

**프로모션 > Campaign Executions**로 이동하여 모든 회원을 위한 캠페인 실행 기록을 확인합니다. 각 실행 기록은 어떤 캠페인을 실행했는지, 어떤 회원을 대상으로 했는지, 결과를 표시합니다.

### 캠페인 범위 검토

Open any campaign record to see the **Times Triggered** count and when the campaign last fired.

This gives you a quick view of how many members have benefited from the campaign.

## Tips

- Create campaigns in **Draft** status first so you can review all settings before they go live
- Use **Max Triggers Per Member** on all one-time bonus campaigns (birthday, first purchase, sign-up) to prevent customers from earning the bonus more than once
- Combine a **Target Segment** with a trigger-based campaign to run tier-exclusive promotions — for example, double points on purchases only for Gold and Platinum members
- Set a **Cooldown Days** value on win-back campaigns so members are not bombarded if they make a small purchase and then go inactive again shortly after
- The campaign list is your best tool for keeping track of what promotions are currently active — review it before launching new offers to ensure campaigns don't stack unintentionally
- Archive ended campaigns rather than deleting them so you have a historical record of what promotions you ran and when