---
title: 동의어 및 리디렉션 관리
---

동의어 및 리디렉션은 등가 용어를 처리하고 특정 쿼리를 대상 페이지로 라우팅하여 검색을 더 똑똑하게 만듭니다. 동의어는 검색을 관련 용어("laptop"은 "notebook"도 포함)로 확장하고, 리디렉션은 "sale"과 같은 쿼리를 직접 판매 페이지로 보냅니다. 이 가이드는 검색 관련성과 고객 경험을 개선하기 위해 두 기능을 생성하고 관리하는 방법을 설명합니다.

동의어는 용어의 등가성을 위해 사용하고, 리디렉션은 네비게이션 단축키로 사용합니다.

![동의어 목록](/static/core/admin/img/help/managing-synonyms-redirects/synonym-list.webp)

## 동의어 이해

동의어는 검색 시스템에 특정 용어가 동등하게 처리되어야 함을 알려줍니다. 고객이 하나의 용어로 검색하면 시스템이 자동으로 동의어 용어와 일치하는 결과를 포함합니다.

**예시**: "laptop" → "notebook", "portable computer"으로의 동의어 매핑을 생성합니다. 이제 누군가 "laptop"을 검색하면 "notebook" 또는 "portable computer"이 제품 이름이나 설명에 포함된 결과도 포함됩니다.

동의어는 특히 다음 경우에 매우 유용합니다:
- 영국어 대 미국어 (jumper/sweater, trainers/sneakers)
- 브랜드 대 일반 용어 (tissues/Kleenex)
- 일반적인 오타 (accommodate/accomodate)
- 산업 용어 대 일반 용어 (CPU/processor)

## 동의어 생성

**Search > Synonyms**으로 이동하고 **+ Add Synonym**을 클릭합니다.

![동의어 추가 폼](/static/core/admin/img/help/managing-synonyms-redirects/synonym-form.webp)

**Term** - 원래 검색 용어로, 동의어 확장을 트리거합니다

**Synonyms** - 등가 용어의 JSON 배열, 예: `['sweater', 'pullover', 'jumper']`

**Bidirectional** - 기본값: 체크됨. 활성화되면 동의어 관계가 양방향으로 작동합니다:
- "laptop" 검색은 "notebook" 제품을 찾습니다
- "notebook" 검색은 "laptop" 제품을 찾습니다

체크를 해제하면 단방향 매핑이 됩니다(아래 참조).

**Language** - 선택 사항. 특정 언어의 검색에만 이 동의어를 적용합니다. 비워두면 모든 언어에 적용됩니다.

**Engine** - 선택 사항. 특정 검색 엔진에만 이 동의어를 적용합니다. 비워두면 전역적으로 적용됩니다.

**Active** - 이 동의어가 현재 사용 중인지 여부. 일시적으로 비활성화하려면 체크를 해제합니다.

## 양방향 동의어 예시

대부분의 동의어는 양방향이어야 합니다 - 양쪽 방향에서 작동하는 진짜 동의어:

| Term | Synonyms | Use Case |
|------|----------|----------|
| laptop | notebook, portable computer | 미국/영국 영어 + 일반 용어 |
| sofa | couch, settee | 지역적 차이 |
| trainers | sneakers, running shoes | 영국/미국 영어 |
| mobile | cell phone, cellular | 국제적 차이 |

양방향이 활성화되면 고객이 어떤 용어를 사용하든 이 모든 용어는 동일한 제품을 찾습니다.

## 단방향 동의어 예시

"Bidirectional"을 해제하여 단방향 관계를 만듭니다:

**일반적인 사용 사례**:
- **오타**: Term: "acco

mmodate" → Synonyms: `['accommodate']` (단방향이므로 정확한 철자가 오타를 찾지 않음)
- **구체적 → 일반적**: Term: "MacBook" → Synonyms: `['laptop']` (MacBooks는 노트북이지만 모든 노트북이 MacBook은 아님)
- **약어**: Term: "CPU" → Synonyms: `['processor']` (CPU는 프로세서 제품을 찾지만 프로세서 검색은 항상 CPU를 포함하지 않아야 함)

## 언어별 동의어

Language 필드를 사용하여 지역에 맞는 동의어를 생성합니다:

**예시**: 영국 영어 스토어
- Term: "jumper", Synonyms: `['sweater', 'pullover']`, Language: English (UK)
- Term: "trainers", Synonyms: `['sneakers']`, Language: English (UK)

**예시**: 다국어 스토어
- Term: "ordinateur portable", Synonyms: `['laptop', 'notebook']`, Language: French
- Term: "zapatos", Synonyms: `['shoes']`, Language: Spanish

언어별 동의어는 고객이 해당 언어로 브라우징할 때만 적용됩니다.

## 엔진별 동의어

대부분의 동의어는 전역적으로 적용되어야 합니다(엔진 필드를 비워두세요). 엔진별 동의어는 다른 검색 컨텍스트가 다른 용어 매핑이 필요한 경우에만 사용하세요:

**예시**: 별도의 "shop" 및 "blog" 엔진이 있습니다
- 블로그 동의어: Term: "tutorial" → Synonyms: `['guide', 'how-to']`, Engine: blog
- 이 동의어는 블로그 검색에만 적용되고 제품 검색에는 적용되지 않습니다

## 리디렉션 이해

검색 리디렉션은 특정 쿼리를 지정된 페이지로 직접 보냅니다. 일반적인 검색 결과를 우회합니다. 고객이 정확히 어디로 가야 하는지 알고 있을 때 리디렉션을 사용합니다.

**예시**: "sale" → "/products/sale/"으로 리디렉션을 생성합니다. 이제 누군가 "sale"을 검색하면 검색 결과를 건너뛰고 직접 판매 페이지로 이동합니다.

리디렉션은 다음과 같은 경우에 이상적입니다:
- 일반적인 네비게이션 단축키("returns" → 반품 정책 페이지)
- 계절별 프로모션("summer sale" → 여름 컬렉션)
- 인기 있는 카테고리("laptops" → 노트북 카테고리 페이지)
- 정책 페이지("shipping" → 배송 정보)

![리디렉션 목록](/static/core/admin/img/help/managing-synonyms-redirects/redirect-list.webp)

## 일치 유형

리디렉션은 검색 쿼리가 얼마나 엄격하게 일치해야 하는지를 제어하는 네 가지 일치 유형을 지원합니다:

**Exact** - 대소문자 구분 없이 정확한 일치. 쿼리가 용어와 정확히 일치해야 합니다(대소문자는 무시됨).
- Term: "sale"
- Matches: "sale", "SALE", "Sale"
- Does NOT match: "summer sale", "on sale"

**Contains** - 쿼리가 용어를 포함하는 경우.
- Term: "sizing"
- Matches: "sizing guide", "help with sizing", "what sizing"
- Does NOT match: "size chart" (다른 단어)

**Starts With** - 쿼리가 용어로 시작하는 경우.
- Term: "return"
- Matches: "returns", "return policy", "returning items"
- Does NOT match: "how to return" (용어로 시작하지 않음)

**Regex** - 정규 표현식을 사용한 패턴 일치. **⚠️ 성능 주의** - 복잡한 정규 표현식은 검색 속도를 느리게 합니다. 사용은 제한하세요.
- Pattern: `^(laptop|notebook)s?$`
- Matches: "laptop", "laptops", "notebook", "notebooks"
- 다른 일치 유형이 작동하지 않을 때만 사용하세요

## 리디렉션 생성

**Search > Redirects**으로 이동하고 **+ Add Redirect**을 클릭합니다.

![리디렉션 추가 폼](/static/core/admin/img/help/managing-synonyms-redirects/redirect-form.webp)

**Term** - 일치할 검색 쿼리

**Match Type** - Exact, Contains, Starts With, 또는 Regex (위 참조)

**Redirect URL** - 고객을 보낼 위치. 상대 경로(`/products/sale/`) 또는 절대 경로(`https://example.com/page/`)일 수 있습니다.

**Redirect Type** - HTTP 상태 코드:
- **302 (임시)**: 권장. 브라우저는 캐시하지 않으며 나중에 대상 위치를 변경할 수 있습니다
- **301 (영구)**: 브라우저 및 검색 엔진이 캐시합니다. 영구 리디렉션이 필요한 경우에만 사용하세요

**Engine** - 선택 사항. 특정 검색 엔진에 제한

**Hit Count** - 이 리디렉션이 사용될 때마다 자동으로 증가합니다. 인기 있는 단축키를 식별하는 데 도움이 됩니다.

**Active** - 이 리디렉션을 활성화/비활성화

## 리디렉션 예시

| Term | Match Type | URL | Use Case |
|------|-----------|-----|----------|
| sale | Exact | `/products/sale/` | "sale" 검색을 직접 판매 페이지로 리디렉션 |
| clearance | Exact | `/clearance/` | 정리 상품 검색을 건너뛰고 |
| sizing | Contains | `/pages/size-guide/` | 사이즈 관련 쿼리는 가이드로 이동 |
| return | Starts With | `/pages/returns/` | 반품 관련 쿼리는 정책으로 이동 |

모두 302 (임시) 리디렉션을 사용하여 유연성을 유지합니다.

## 리디렉션 유형: 302 대 301

**302 (임시)** - 대부분의 리디렉션에 권장
- 브라우저는 매번 새로운 요청을 합니다
- 언제든지 대상 URL을 변경할 수 있습니다
- 확신이 없을 경우 더 안전한 선택

**301 (영구)** - 제한적으로 사용
- 브라우저가 리디렉션을 캐시합니다
- 검색 엔진이 인덱스를 업데이트합니다
- 나중에 변경하기 어렵습니다

**추천**: 리디렉션이 절대 변경되지 않을 것이라고 확신하지 않는 한 302를 사용하세요.

## Hit Count 분석

Hit Count 필드는 리디렉션이 실행될 때마다 자동으로 증가합니다. 이를 통해 다음과 같은 작업을 수행할 수 있습니다:
- 가장 많이 사용되는 네비게이션 단축키 식별
- 사용되지 않는 리디렉션 식별(삭제 고려)
- 인기 있는 검색 패턴 발견

매달 Hit Count를 검토하여 리디렉션 전략을 최적화하세요.

## 동의어 기회 찾기

**Zero-Results 쿼리 사용**: **Search > Search Analytics**으로 이동하고 zero-result 쿼리를 필터링합니다. 이는 다음과 같은 것을 드러냅니다:
- 고객이 사용하는 제품 설명과 일치하지 않는 용어
- 고려하지 못한 지역적 차이
- 일반적인 오타

**워크플로**:
1. 매주 zero-result 쿼리를 검토합니다
2. 패턴을 식별합니다(같은 용어가 반복적으로 나타나는 경우)
3. 고객 언어를 제품 이름으로 매핑하는 동의어를 추가합니다
4. zero-results가 감소하는지 모니터링합니다

## 팁

- **매주 zero-result 쿼리를 통해 동의어 아이디어를 모니터링하세요** - 고객 언어와 제품 설명 사이의 격차를 드러냅니다
- **일반적인 동의어부터 시작하고 데이터에 따라 확장하세요** - 지역적 차이부터 시작하고 실제 검색 행동에 따라 추가하세요
- **진짜 동의어에는 양방향을 사용하세요** - 대부분의 동의어는 양방향으로 작동해야 합니다(laptop ↔ notebook)
- **복잡한 정규 표현식은 피하세요** - 정규 표현식 일치는 다른 일치 유형보다 느리므로 필요할 때만 사용하세요
- **302 리디렉션(임시)을 기본값으로 사용하세요** - 나중에 대상 위치를 변경할 수 있는 유연성을 제공합니다
- **실제 쿼리로 동의어를 테스트하세요** - 동의어 용어를 검색하여 예상 결과가 반환되는지 확인하세요
- **다국어 스토어에는 언어별 동의어를 사용하세요** - 지원하는 각 언어에 대해 지역에 맞는 용어 매핑을 생성하세요

기억하세요: 마크다운 포맷, 이미지 경로, 코드 블록 및 기술 용어는 보존 규칙에 따라 정확히 유지하세요.