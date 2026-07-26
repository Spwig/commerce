---
title: API 토큰
---

API 토큰은 외부 서비스 및 통합이 가게와 통신할 수 있도록 해주는 보안 키입니다. 제3자 서비스나 도구가 가게의 데이터에 접근하거나 액션을 트리거해야 할 때, 요청에 함께 API 토큰을 보내어 요청이 승인되었는지 확인합니다. 가게의 API 토큰 섹션에서 모든 토큰을 생성하고 관리하며, 각 토큰이 가게의 어떤 부분에 접근할 수 있는지 정확히 설정할 수 있습니다.

## API 토큰이 필요한 경우

가장 일반적으로 API 토큰을 생성해야 하는 경우는 다음과 같습니다:

- 외부 서비스나 자동화 도구를 연결하여 가게의 데이터를 읽거나 쓰는 경우
- 수신 웹훅이 들어오는 요청을 인증해야 하는 경우
- 설치된 Spwig 도움 시스템을 설정하는 경우
- Spwig의 API를 사용하여 커스텀 통합을 구축하는 경우
- Spwig 가게와 다른 시스템 간 데이터를 동기화하는 경우

각 통합에는 자체 토큰이 있어야 하며, 하나의 서비스에 대한 액세스를 취소해도 다른 서비스에 영향을 주지 않도록 할 수 있습니다.

## 토큰 유형

토큰을 생성할 때, 그 목적을 설명하는 유형을 선택합니다. 이 유형은 참고용이며, 각 토큰이 무엇을 수행하는지 추적하는 데 도움이 됩니다.

| 유형 | 목적 |
|------|---------|
| **Help System** | Spwig 도움 문서 시스템에서 사용됨 |
| **External Integration** | 제3자 서비스, 자동화 도구(예: Zapier), 또는 데이터 동기화 도구 |
| **Webhook** | 웹훅 수신기 또는 엔드포인트의 인증 |
| **Custom** | 위의 범주에 해당하지 않는 기타 목적 |
| **Instance Sync** | Spwig 설치 간 또는 외부 Spwig 서비스 간 동기화 |

## API 범위: 토큰이 접근할 수 있는 영역 제어

각 토큰은 **API 범위** 섹션이 있으며, 이 섹션은 토큰이 가게의 어떤 부분을 호출할 수 있는지 정확히 결정합니다. 토큰이 모든 항목에 대한 일반적인 접근 권한을 가지는 대신, 통합이 실제로 필요한 수준에서 하나씩 접근 권한을 부여합니다.

**선택된 범위가 없는 토큰은 API에 접근할 수 없으며**, 다른 모든 활성 및 유효한 상태와 관계없이 해당됩니다.

이것은 새 토큰의 기본값이므로, 액세스를 명시적으로 허용하지 않으면 통합이 작동하지 않습니다.

각 범위에 대해 세 가지 액세스 수준 중 하나를 선택합니다:

| 액세스 수준 | 허용하는 항목 |
|--------------|-----------------|
| **액세스 없음** | 이 영역의 모든 엔드포인트를 호출할 수 없습니다 |
| **읽기** | 이 영역에서 데이터를 검색할 수 있지만 변경할 수는 없습니다 |
| **읽기 및 쓰기** | 이 영역에서 데이터를 검색하고, 생성, 업데이트, 또는 삭제할 수도 있습니다 |

범위는 관리자 영역의 영역과 일치하도록 그룹화되어 있습니다:

| 그룹 | 범위 | 읽기 및 쓰기 가능? | 액세스 권한 부여 영역 |
|-------|-------|:---:|-------------------|
| 분석 | **판매 분석** | 읽기 전용 | 판매 대시보드, KPI, 제품/고객/카테고리 분석, 비교 및 내보내기 |
| 분석 | **웹 분석** | 읽기 전용 | 방문자 및 트래픽 분석: 개요, 추세, 상위 페이지, 지리 및 추천자 |
| 카탈로그 | **제품** | 예 | 제품, 변형, 이미지, 재고 조정 및 속성 할당 |
| 카탈로그 | **카테고리** | 예 | 제품 카테고리, 이미지 및 배너 포함 |
| 카탈로그 | **브랜드** | 예 | 제품 브랜드 |
| 카탈로그 | **속성** | 예 | 제품 속성 정의 |
| 카탈로그 | **재고** | 예 | 재고 대시보드, 재고 속도, 이동, 재주문 제안 및 재고 설정 |
| 주문 | **주문** | 예 | 주문, 주문 메모, 상태/추적 업데이트, 취소, 환불 및 주문 문서 |
| 고객 | **고객 메시지** | 예 | 연락처 양식 및 주문 메모에서의 고객 메시지, 상태 업데이트 및 답변 포함 |
| 가게 및 설정 | **가게 설정** | 예 | 가게 설정, 사용 가능한 언어 및 브랜딩(이름, 색상, 로고) |
| 사용자 및 액세스 | **직원 및 역할** | 예 | 직원 계정, 초대, 역할 및 권한 카탈로그 |

두 개의 **분석** 범위는 항상 읽기 전용입니다 — 보고 데이터에는 "쓰기" 개념이 없기 때문에, 선택기에서는 이 범위에 대해 **액세스 없음** 또는 **읽기**만 제공합니다.

[![API 범위 선택기, Analytics 및 Catalog 범위 그룹 위에 액세스 참고 사항](/static/core/admin/img/help/api-tokens/api-token-scope-picker.webp)]

범위 선택기 아래에는 읽기 전용 **"이 토큰은 다음을 액세스할 수 있습니다":** 요약이 나타나며, 이 요약은 사용자가 부여한 모든 범위와 그 수준을 나열하여 토큰의 액세스 권한을 한눈에 확인할 수 있도록 합니다.

[!["이 토큰은 다음을 액세스할 수 있습니다" 요약, 부여된 각 범위와 그 Read 또는 Read & Write 수준을 나열](/static/core/admin/img/help/api-tokens/api-token-scope-summary.webp)]

### 토큰이 실제로 사용하는 권한

토큰의 범위는 그것이 할 수 있는 것의 *상한선*을 설명합니다. 하지만 토큰은 그것을 생성한 직원의 실제 세계 권한을 상속합니다:

- 토큰은 생성한 직원이 슈퍼유저이더라도 **슈퍼유저** 권한으로 행동할 수 없습니다.
- 범위에 **Read & Write**이 적용되려면 생성한 직원의 역할이 해당 영역에 대한 쓰기 액세스를 허용해야 합니다. 예를 들어, Products에 대해 보기 전용 역할을 가진 직원이 "Products: Read & Write"로 토큰을 생성하면, 그 토큰은 여전히 읽기만 가능합니다. 역할은 범위의 위에 두 번째 게이트 역할을 합니다.
- 토큰을 생성한 직원이 삭제되거나 계정이 비활성화되면, 토큰은 즉시 API 액세스를 잃게 됩니다. 범위와 무관하게, 더 이상 토큰이 대신 행동할 수 있는 허용된 사용자가 없습니다.

이러한 의미에서, 토큰의 범위를 엄격하게 설정하는 가장 안전한 방법은, 토큰이 가진 액세스 권한과 동일한 역할을 가진 직원으로 로그인한 상태에서 토큰을 생성하는 것입니다.

## API 토큰 생성

1.

**설정 > API 토큰**으로 이동
2.

**+ API 토큰 추가**를 클릭
3.

토큰의 용도를 명확히 설명하는 **이름**을 입력하세요 (예: `Zapier Product Sync` 또는 `Help System API`)
4.

적절한 **토큰 유형**을 선택하세요
5.

통합에 대한 추가 정보를 포함하는 **설명**을 선택적으로 추가하세요
6.

**API 범위**에서 통합이 필요한 각 영역에 대해 **No access**, **Read**, 또는 **Read & Write**을 선택하세요 — 다른 모든 범위는 **No access**로 남겨두세요
7.

모든 마크다운 포맷, 이미지 경로, 코드 블록 및 기술 용어를 유지하세요.

필요한 경우 **Active** 상태, **Expiry Date**, 및 **Allowed IPs**를 설정하세요 (아래 참조)
8.

**Save**를 클릭하세요

저장 후, 전체 토큰 값은 상세 페이지에서 표시됩니다. **즉시 복사**하세요 — 보안상 목록 뷰에서는 토큰이 마스킹되어 있으며, 이 페이지를 떠나면 다시 전체 토큰 값을 얻을 수 없습니다.

![API Token Detail](/static/core/admin/img/help/api-tokens/api-token-detail.webp)

## Token value security

Spwig은 새 토큰을 저장한 직후에만 전체 토큰 값을 표시합니다. 이후 목록 뷰에서는 마스킹된 버전만 표시됩니다 (예: `spw_••••••••••••••••••••3f8a`).

토큰 값을 잃어버리면 복구할 수 없습니다. 이전 토큰을 삭제하고 새 토큰을 생성한 후, 해당 토큰을 사용하던 통합을 업데이트해야 합니다.

**이메일, 채팅 메시지, 또는 소스 코드에 토큰 값을 공유하지 마세요.** 비밀번호처럼 대우하세요.

## Setting an expiry date

**Expires At** 필드는 토큰이 더 이상 작동하지 않도록 자동으로 설정할 날짜 및 시간을 지정합니다. 토큰이 만료되어야 하지 않는 경우 이 필드를 비워두세요.

만료 날짜는 다음과 같은 경우에 유용합니다:

- 특정 종료 날짜가 있는 일시적인 통합
- 제3자에게 제공하는 토큰에서 자동으로 접근을 제거하고 싶은 경우
- 고권한 통합에 추가 보안 층을 제공하는 경우

토큰이 만료되면 해당 토큰을 사용한 요청은 거부됩니다. **Expires At** 날짜를 업데이트하거나 대체 토큰을 생성하여 접근을 연장할 수 있습니다.

## Restricting to specific IP addresses

**Allowed IPs** 필드는 IP 주소 목록을 입력할 수 있습니다. 목록이 비어 있지 않은 경우, 토큰은 해당 주소 중 하나에서 요청이 올 경우에만 작동합니다.

예를 들어, 분석 도구가 `203.0.113.42` 서버에서 실행된다면, 해당 IP를 추가하면 토큰이 유출되어도 다른 위치에서 악용될 수 없습니다.

**Allowed IPs**를 비워두면 모든 IP 주소에서의 요청을 허용합니다.

**Expiry and IP restrictions are checked independently of scopes.** An expired or off-allowlist token is rejected before its scopes are even considered, and a token with generous scopes is still rejected the moment it expires or is called from an unlisted IP.

## Calling the API with a token

Integrations authenticate to Spwig's admin API by sending the token in an `Authorization` header:

```
Authorization: Bearer <your-token-value>
```

Every admin API endpoint lives under `/api/admin/...`. The developer building your integration decides which endpoints to call — your job as the merchant is to make sure the token's **API Scopes** cover those endpoints. If a request is rejected with a permissions error, the first thing to check is whether the token has been granted the right scope at the right access level.

### Example: reading web traffic analytics

Spwig exposes a `GET /api/admin/analytics/traffic/` endpoint that returns visitor and traffic analytics for your store — an overview of visits and unique visitors, trends over time, top pages, visitor geography, and referrer sources. To let a reporting tool or dashboard read this data:

1. Create a token (or edit an existing one) for that integration
2. In **API Scopes**, set **Web Analytics** to **Read**
3. Save the token and provide it to the integration

Because **Web Analytics** is a read-only scope, there is no "Read & Write" option to choose — the integration can only retrieve analytics data, never change your store's configuration.

## Monitoring token usage

The token list shows:

- **Usage Count** — total number of times the token has been used
- **Last Used** — when the token was last used to make a request

These fields help you identify unused tokens (candidates for revocation) and spot unexpected activity. A sudden spike in usage count may indicate a token is being used by someone other than the intended integration.

## Revoking a token

To immediately stop a token from working without deleting it:

1.

토큰 이름을 클릭합니다.
2.

**활성화**를 선택 해제합니다.
3.

저장합니다.

토큰은 참조용으로 목록에 남아 있지만, 이후의 요청에서는 거부됩니다. 이는 문제를 조사하는 동안 통합을 일시적으로 중단해야 할 때 유용합니다.

토큰을 영구적으로 삭제하려면:

1. 목록에서 해당 토큰의 체크박스를 선택합니다.
2. 액션 메뉴에서 **선택한 API 토큰 삭제**를 선택합니다.
3. 삭제를 확인합니다.

한 번 삭제된 토큰은 복구할 수 없습니다. 통합이 여전히 액세스가 필요하다면, 새 토큰을 생성하고 통합의 설정을 업데이트합니다.

## 예시: Zapier 통합 설정

**시나리오:** 스토어를 Zapier에 연결하여 주문 알림을 자동화하고 싶습니다.

| 필드 | 값 |
|-------|-------|
| 이름 | `Zapier 주문 자동화` |
| 토큰 유형 | 외부 통합 |
| 설명 | Zapier이 새 주문을 읽고 알림을 트리거하는 데 사용됨 |
| API 범위 | **주문**: 읽기 및 쓰기 |
| 활성화 | 예 |
| 만료 시간 | *(빈칸으로 남김)* |
| 허용된 IP 주소 | *(빈칸으로 남김 — Zapier은 동적 IP를 사용함)* |

**주문** 범위만 부여되었기 때문에, 이 토큰이 노출되더라도 제품, 고객 메시지, 직원 계정 또는 스토어의 다른 부분을 조작할 수 없습니다. 저장 후 전체 토큰 값을 복사하여 Zapier의 Spwig 통합 설정에 붙여넣습니다.

## 팁

모든 마크다운 포맷, 이미지 경로, 코드 블록 및 기술 용어를 유지합니다.

- 각 토큰에 명확하고 구체적인 이름을 부여하세요 — 몇 달 후 문제를 해결할 때 `Shopify Sync v2`는 `Token 3`보다 훨씬 유용합니다
- 통합 작업당 하나의 토큰을 생성하세요 — 통합이 해킹된 경우 다른 토큰에 영향을 주지 않고 해당 토큰만 취소할 수 있습니다
- **통합이 실제로 필요한 범위만 부여하세요** — 보고 도구는 Sales Analytics 또는 Web Analytics에 대한 읽기 권한만 필요하며, Products 또는 Staff & Roles에 대한 읽기 및 쓰기 권한은 필요하지 않습니다
- 토큰을 제3자에게 전달하기 전에 변경 양식에서 **"이 토큰은 다음을 액세스할 수 있습니다:"** 요약을 확인하세요 — 이는 의도치 않게 더 많은 권한을 부여하지 않았는지 확인하는 가장 빠른 방법입니다
- 쓰기 권한은 생성한 직원의 역할에도 의존합니다 — 범위가 Read & Write로 표시되어 있지만 쓰기 작업이 여전히 실패하는 경우 해당 사용자의 역할 권한도 확인해야 합니다
- 일회성 프로젝트나 임시 통합에 사용되는 토큰에 만료 날짜를 설정하세요 — 이는 잊혀진 토큰이 영원히 활성 상태로 남아 있는 위험을 줄입니다
- 몇 달에 한 번 토큰 목록을 검토하고 **Last Used** 날짜가 예상보다 오래된 토큰을 비활성화하세요 — 이는 더 이상 실행되지 않는 통합에 속할 수 있습니다
- 토큰이 노출되었을 가능성이 있다고 생각되면 즉시 비활성화하고 대체 토큰을 생성한 후 영향을 받은 통합을 업데이트한 후 다시 액세스를 활성화하세요