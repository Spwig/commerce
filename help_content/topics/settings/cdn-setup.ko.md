---
title: CDN 설정
---

A Content Delivery Network (CDN) stores copies of your store's images, stylesheets, and scripts on servers around the world. When a customer visits your store, these files are served from the server closest to them rather than from your main hosting server. This reduces page load times, especially for customers located far from where your store is hosted.

Spwig already optimizes static asset delivery out of the box with Brotli and gzip pre-compression, fingerprinted asset caching with 1-year immutable headers, and proper content negotiation. Adding a CDN is optional, but it can further improve speed for stores with an international customer base.

## Does Your Store Need a CDN?

Not every store benefits equally from a CDN. Use these guidelines to decide:

**A CDN is recommended if**:
- Your customers are spread across multiple countries or continents
- Your store features many product images or media-heavy pages
- You want the fastest possible page load times worldwide
- You sell to regions far from your hosting server (e.g., server in Europe, customers in Asia)

**A CDN is likely unnecessary if**:
- Your customers are mostly local or within the same country as your server
- Your store has a small catalog with few images
- Your hosting provider already includes a built-in CDN

When in doubt, a CDN does not hurt performance. Services like Cloudflare offer free tiers, so there is no cost to try.

## How Spwig Works with CDNs

Spwig is CDN-ready by default. You do not need to change any code or settings inside your Spwig admin panel. Here is what Spwig already does for you:

- **Fingerprinted static files** -- Every CSS, JavaScript, and image file includes a unique version hash in its filename. This means CDNs can safely cache these files for a long time without serving outdated content.
- **Long-lived cache headers** -- Static assets are served with 1-year immutable cache headers, telling CDNs and browsers to cache them aggressively.
- **Pre-compressed files** -- Spwig pre-compresses assets using Brotli and gzip, so your CDN can deliver smaller files without extra processing.
- **Proper content negotiation** -- Spwig sends the correct content-type and encoding headers that CDNs rely on for proper caching.

All you need to do is point your domain's DNS to the CDN provider, and everything works automatically.

## Setting Up Cloudflare

Cloudflare is the most popular CDN and offers a free tier that works well for most stores. Follow these steps:

**Step 1: Create a Cloudflare Account**
- Visit cloudflare.com and sign up for a free account

**Step 2: Add Your Domain**
- Click **Add a Site** and enter your store's domain name
- Select the **Free** plan (sufficient for most stores)

**Step 3: Update Your DNS Nameservers**
- Cloudflare will show you two nameservers (e.g., `anna.ns.cloudflare.com`)
- Log in to your domain registrar (where you purchased your domain)
- Replace your current nameservers with the Cloudflare nameservers
- DNS changes can take up to 24 hours to take effect

**Step 4: Configure SSL/TLS**
- In the Cloudflare dashboard, go to **SSL/TLS**
- Set the encryption mode to **Full (strict)**
- This ensures all traffic between Cloudflare and your server stays encrypted

**Step 5: Verify It Is Working**
- Once DNS propagates, visit your store and check for the `cf-cache-status` header in your browser (see Verifying Your CDN below)

## Setting Up AWS CloudFront

If you already use Amazon Web Services, CloudFront integrates naturally with your infrastructure:

1. Open the **CloudFront** console in your AWS account
2. Create a new **Distribution** with your store's domain as the origin
3. Set the **Origin Protocol Policy** to "HTTPS Only"
4. Under **Cache Behavior**, set **Cache Policy** to "CachingOptimized" for static assets
5. Add your store's domain as an **Alternate Domain Name (CNAME)**
6. Attach an SSL certificate from AWS Certificate Manager
7. Update your domain's DNS to point to the CloudFront distribution URL

CloudFront 가격은 사용량에 따라 결정됩니다.

대부분의 가게에서는 비용이 최소한으로 유지되며, Spwig의 지문화된 자산은 오랜 기간 동안 캐시됩니다.

## 권장된 CDN 설정

최상의 결과를 위해 CDN을 올바른 콘텐츠를 캐시하고 나머지는 건너뛰도록 구성하세요.

**캐시할 항목** (정적 자산):
- `/static/` -- 모든 스타일시트, 스크립트, 폰트 및 테마 자산
- `/media/` -- 제품 이미지 및 업로드된 미디어 파일
- 이미지 파일 (`.jpg`, `.png`, `.webp`, `.svg`, `.gif`)
- 폰트 파일 (`.woff`, `.woff2`)

**캐시하지 않을 항목** (동적 페이지):
- `/admin/` -- 관리자 패널은 항상 신선한 콘텐츠를 제공해야 합니다
- `/cart/` -- 쇼핑 카트 페이지는 세션별 데이터를 포함합니다
- `/checkout/` -- 결제 페이지는 보안상 캐시되어서는 안 됩니다
- `/accounts/` -- 고객 계정 페이지는 개인 정보를 포함합니다
- 로그인 또는 개인화된 콘텐츠를 표시하는 모든 페이지

**일반적인 캐시 규칙**:
- **원본 캐시 헤더를 존중하세요** -- Spwig은 각 콘텐츠 유형에 맞는 올바른 캐시-제어 헤더를 전송합니다. CDN을 구성할 때 이러한 헤더를 존중하도록 설정하고, 이를 덮어쓰지 않도록 하세요.
- **Brotli 압축을 활성화하세요** -- Cloudflare 및 CloudFront 모두 Brotli를 지원합니다. 이를 활성화하여 Spwig의 사전 압축된 자산을 활용하세요.
- **브라우저 캐시 TTL을 "기존 헤더 존중"으로 설정하세요** -- 이는 Spwig의 내장 캐시 정책이 동작하도록 합니다.

## CDN 확인

설치 후 CDN이 콘텐츠를 올바르게 제공하는지 확인하세요:

**단계 1: 브라우저 개발자 도구 열기**
- Chrome 또는 Firefox에서 **F12**를 누르면 개발자 도구가 열립니다
- **Network** 탭을 클릭하세요

**단계 2: 가게 로드**
- 개발자 도구가 열린 상태에서 가게의 홈페이지를 방문하세요
- 어떤 정적 파일 요청(예: `.css` 또는 `.js` 파일)을 클릭하세요

**단계 3: 응답 헤더 확인**
- **Cloudflare**: `cf-cache-status` 헤더를 확인하세요. 값이 `HIT`이면 파일이 CDN 캐시에서 제공된 것입니다. `MISS`이면 서버에서 가져온 것입니다(처음 요청만 해당).
- **CloudFront**: `x-cache` 헤더를 확인하세요. 값이 `Hit from cloudfront`이면 CDN 제공을 확인할 수 있습니다.

**단계 4: 다른 위치에서 테스트**
- gtmetrix.com 또는 webpagetest.org 같은 무료 도구를 사용하여 가게를 다른 지리적 위치에서 테스트하세요
- CDN 설정 전후의 로드 시간을 비교하세요

## 일반적인 문제

### 테마 변경 후 오래된 콘텐츠

**문제**: 테마를 업데이트하거나 디자인 변경을 수행한 후 고객이 여전히 이전 버전을 보고 있습니다.

**해결책**: CDN 캐시를 지우세요. Cloudflare에서는 **Caching > Configuration > Purge Everything**으로 이동하세요. CloudFront에서는 `/*`에 대한 **Invalidation**을 생성하세요. Spwig의 지문화된 자산은 일반적으로 이 문제를 방지합니다. 업데이트된 파일은 자동으로 새 파일명을 받기 때문입니다. 이 문제는 일반적으로 지문화되지 않은 자산(예: 사용자 정의 업로드)에 영향을 미칩니다.

---

### 혼합 콘텐츠 경고

**문제**: CDN을 활성화한 후 브라우저에서 "혼합 콘텐츠"에 대한 보안 경고가 표시됩니다.

**해결책**: CDN의 SSL 모드가 **Full (strict)**로 설정되어 있는지 확인하세요. "Flexible" 모드는 서버가 HTTPS 대신 HTTP 요청을 받을 수 있게 하며, 이는 혼합 콘텐츠 경고를 유발할 수 있습니다. Cloudflare에서는 **SSL/TLS > Overview**를 확인하고 모드를 확인하세요.

---

### 관리자 패널이 느리게 작동함

**문제**: CDN을 추가한 후 관리자 패널이 느리게 느껴집니다.

**해결책**: CDN은 관리자 페이지를 캐시해서는 안 됩니다. Cloudflare에서는 **Page Rule** 또는 CloudFront에서는 **Cache Behavior**를 생성하여 `/admin/*`에 일치하는 모든 URL에 대해 캐시를 "Bypass"로 설정하세요. 이는 관리자 요청이 CDN 오버헤드 없이 직접 서버로 전달되도록 합니다.

---

### 이미지가 로드되지 않음

**문제**: CDN 설정 후 제품 이미지 또는 미디어 파일이 오류를 반환합니다.

**해결책**: CDN의 원본이 올바른 프로토콜 (HTTPS) 및 포트로 구성되어 있는지 확인하세요. 또한 서버의 방화벽이 CDN의 IP 범위에서의 연결을 허용하는지 확인하세요.

## 팁

모든 마크다운 포맷, 이미지 경로, 코드 블록 및 기술 용어를 유지하세요.

- **Cloudflare의 무료 계층부터 시작하세요** -- 대부분의 매장 요구사항을 충족하며, 설정에는 단지 몇 분만 걸립니다
- **항상 Full (엄격) SSL 모드를 사용하세요** -- Flexible 모드는 보안 취약점을 만들 수 있으며, 결제 흐름을 손상시킬 수 있습니다
- **대규모 테마 업데이트 후 CDN 캐시를 지우세요** -- Spwig의 지문 처리된 파일은 대부분의 경우를 처리하지만, 전체 캐시 정리가 필요합니다. 이는 오래된 콘텐츠가 남지 않도록 보장합니다
- **체크아웃 또는 장바구니 페이지를 캐시하지 마세요** -- 이러한 페이지를 캐시하면 한 고객의 데이터가 다른 고객에게 노출될 수 있습니다
- **고객의 위치에서 테스트하세요** -- webpagetest.org와 같은 무료 도구를 사용하여 고객이 쇼핑하는 지역에서 실제 성능을 측정하세요
- **CDN 분석을 모니터링하세요** -- Cloudflare 및 CloudFront 모두 캐시 히트율, 절약된 대역폭, 국가별 트래픽을 보여주는 대시보드를 제공합니다
- **설치 중 DNS TTL을 낮게 유지하세요** -- CDN으로 전환하는 동안 DNS TTL을 300초(5분)로 설정한 후 모든 것이 정상적으로 작동하는 것을 확인한 후 증가시켜야 합니다
- **CDN은 좋은 호스팅을 대체하지 않습니다** -- 체크아웃, 장바구니 및 관리와 같은 동적 페이지에 있어 원본 서버는 여전히 중요합니다

품질이 높은 호스팅을 CDN과 함께 선택하세요