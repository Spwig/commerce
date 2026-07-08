---
title: 상품 브랜드
---

브랜드는 제품을 제조사 또는 라벨과 연결하고 고객이 브랜드별로 가게를 탐색할 수 있는 방법을 제공합니다. 각 브랜드는 고객이 해당 브랜드의 모든 제품을 발견하고 브랜드 이야기를 읽고 브랜드 웹사이트로 이동할 수 있는 고유한 페이지를 가진 가상 매장에 있습니다.

**카탈로그 > 브랜드**로 이동하여 브랜드를 관리하세요.

## 브랜드를 사용하는 이유

Spwig에서 브랜드는 두 가지 목적을 수행합니다:

1. **조직화** — 제품은 브랜드로 태그되어 특정 라벨에 충성한 고객이 원하는 항목을 쉽게 찾을 수 있도록 합니다.
2. **상품 판매** — 브랜드 페이지는 브랜드의 이야기, 로고 및 전체 제품 범위를 전시할 수 있는 전용 공간으로, 브랜드에 민감한 고객의 전환율을 높일 수 있습니다.

브랜드는 프로모션 시스템과도 함께 작동합니다 — 특정 브랜드의 모든 제품에 적용되는 할인을 개별 제품을 선택하지 않고 실행할 수 있습니다.

## 브랜드 생성

1.

**카탈로그 > 브랜드**로 이동하세요
2.

**+ 브랜드 추가**를 클릭하세요
3.

**기본 정보** 섹션을 작성하세요:
   - **이름** — 가상 매장에 표시될 브랜드 이름(유일해야 함)
   - **슬러그** — 브랜드 페이지의 URL 경로(이름에서 자동으로 채워짐; 사용자가 커스터마이징 가능)
   - **설명** — 브랜드 페이지에 표시되는 브랜드의 짧은 설명
   - **웹사이트** — 브랜드의 공식 웹사이트 URL(선택 사항 — 브랜드 페이지에 링크로 표시됨)
4.

브랜드 자산을 추가하세요:
   - **로고** — 브랜드의 로고 이미지, 브랜드 목록 및 브랜드 페이지에 사용됨
   - **배너 이미지** — 브랜드 페이지 상단에 표시되는 넓은 배너 이미지
5.

**브랜드 이야기**를 작성하세요(선택 사항) — 브랜드의 역사, 가치 또는 특별한 점에 대한 더 긴 편집 기사입니다.

이 내용은 브랜드의 가상 매장 페이지에 표시되며, 관심 있는 고객에게 브랜드의 이야기를 전달하는 효과적인 방법이 될 수 있습니다.
6.

모든 마크다운 포맷, 이미지 경로, 코드 블록 및 기술 용어를 유지하세요.

Configure **SEO** fields:
   - **Meta Title** — the page title shown in search engine results
   - **Meta Description** — the short description shown below the title in search results
7.

Set display options:
   - **Show Brand Page** — controls whether the brand has a publicly accessible page.

Uncheck to hide a brand from the storefront while keeping it in the system.
   - **Is Active** — controls whether the brand is available to assign to products and visible in the store
   - **Is Featured** — marks the brand for featured placement in your theme (e.g., a homepage row of brand logos)
8.

Click **Save**

## Assigning products to a brand

Brands are assigned on individual product records, not from the brand management page. To assign a brand to a product:

1. Navigate to **Catalog > Products** and open the product
2. In the product form, find the **Brand** field
3. Search for and select the appropriate brand
4. Save the product

Once a brand is assigned, the product will appear on that brand's storefront page automatically.

## Brand pages on your storefront

Each brand with **Show Brand Page** enabled gets its own page at `/brand/{slug}/`. The page displays:

- The brand logo and banner image
- The brand name and description
- The brand story (if provided)
- A link to the brand's website (if provided)
- All active products assigned to that brand

Customers can reach brand pages by clicking a brand name on a product page, or through links you create in your navigation or page builder.

## SEO for brand pages

Filling in the **Meta Title** and **Meta Description** fields for each brand helps your brand pages appear well in search results. Effective brand SEO titles typically combine the brand name with what the brand sells:

| Brand | Good Meta Title |
|---|---|
| Levi's | "Levi's Jeans & Clothing — Official Store" |
| KitchenAid | "KitchenAid Stand Mixers & Kitchen Appliances" |
| Patagonia | "Patagonia Outdoor Clothing & Gear" |

SEO 필드을 비워두면 테마는 브랜드 이름으로 자동으로 대체됩니다.

### 자동 SEO 생성

브랜드에 **SEO 자동 생성**이 활성화되어 있으면 Spwig은 브랜드를 저장할 때 메타 제목과 설명 내용을 자동으로 생성합니다. 이는 많은 브랜드를 가진 가게에 편리하지만, 정확한 문구에 대한 통제는 줄어듭니다. 언제든지 직접 필드에 입력하여 생성된 내용을 덮어쓸 수 있으며, 자동 생성 토글을 비활성화할 수 있습니다.

## 추천 브랜드

**추천** 플래그는 테마에서 브랜드 로고의 큐레이션된 행 또는 그리드를 표시하는 데 사용됩니다 — 일반적으로 홈페이지에 표시됩니다. 한 번에 표시되는 추천 브랜드 수는 작아야 합니다; 테마 문서를 참조하여 최적의 추천 브랜드 수를 확인하세요.

## 팁

- 투명한 배경을 가진 PNG 또는 WebP 형식의 브랜드 로고를 업로드하세요 — 테마의 모든 배경 색상에서 깔끔하게 표시됩니다
- 잘 알려지지 않은 브랜드에도 매력적인 브랜드 이야기를 작성하세요; 브랜드에 익숙하지 않은 고객은 제품이 자신에게 맞는지 결정하는 데 도움이 되는 맥락을 좋아합니다
- 특정 브랜드를 대상으로 한 프로모션을 진행할 경우, Spwig에 있는 브랜드 이름이 정확히 일치하도록 해야 합니다 — 프로모션은 제품에 있는 브랜드 관계를 기반으로 자격을 결정합니다
- 제품을 더 이상 취급하지 않게 되었을 때 브랜드를 비활성화하는 것이 좋습니다 — 삭제는 모든 관련된 제품에서 브랜드 참조를 제거하지만, 비활성화는 기록을 유지합니다
- **추천** 플래그는 적게 사용하세요; 홈페이지에 20개의 브랜드 로고를 보여주는 것보다 6~8개의 신중하게 선택된 브랜드로 보여주는 것이 더 효과적입니다