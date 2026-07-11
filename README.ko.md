<p align="center">
  <a href="README.md">English</a> |
  <a href="README.fr.md">Français</a> |
  <a href="README.es.md">Español</a> |
  <a href="README.de.md">Deutsch</a> |
  <a href="README.ja.md">日本語</a> |
  <a href="README.zh-Hans.md">简体中文</a> |
  <a href="README.zh-Hant.md">繁體中文</a> |
  <a href="README.pt.md">Português</a> |
  <a href="README.ru.md">Русский</a> |
  <a href="README.ar.md">العربية</a> |
  <a href="README.hi.md">हिन्दी</a> |
  <a href="README.id.md">Bahasa Indonesia</a> |
  <a href="README.it.md">Italiano</a> |
  <strong>한국어</strong> |
  <a href="README.tr.md">Türkçe</a> |
  <a href="README.vi.md">Tiếng Việt</a> |
  <a href="README.th.md">ไทย</a>
</p>

<p align="center">
  <img src="https://spwig.com/images/logo.svg" alt="Spwig" width="200">
</p>

<h1 align="center">Spwig</h1>

<p align="center">
  <strong>스토어를 직접 소유하고자 하는 판매자를 위한 셀프 호스팅 이커머스 플랫폼입니다.</strong>
</p>

<p align="center">
  <a href="https://spwig.com">웹사이트</a> &nbsp;•&nbsp;
  <a href="https://docs.spwig.com">문서</a> &nbsp;•&nbsp;
  <a href="https://community.spwig.com">커뮤니티</a> &nbsp;•&nbsp;
  <a href="https://spwig.com/ko/marketplace">마켓플레이스</a> &nbsp;•&nbsp;
  <a href="https://spwig.com/ko/demos">라이브 데모</a>
</p>

<p align="center">
  <a href="LICENSE"><img alt="Licence: AGPL v3" src="https://img.shields.io/badge/licence-AGPL--3.0-blue.svg"></a>
  <a href="https://github.com/Spwig/commerce/actions"><img alt="CI" src="https://img.shields.io/github/actions/workflow/status/Spwig/commerce/test.yml?branch=main&label=tests"></a>
  <a href="https://github.com/Spwig/commerce/releases"><img alt="Release" src="https://img.shields.io/github/v/release/Spwig/commerce"></a>
  <a href="https://github.com/Spwig/commerce/discussions"><img alt="Discussions" src="https://img.shields.io/github/discussions/Spwig/commerce"></a>
</p>

## Spwig 는 무엇인가요?

Spwig 는 카탈로그, 장바구니, 체크아웃, 주문, 고객, 결제, 배송, 테마,
페이지 빌더, 관리자 API, POS, 정기결제, 로열티, 블로그, SEO 까지 —
스택 전체를 아우르는 풀 기능 이커머스 플랫폼입니다. **Django 5**,
**PostgreSQL**, **Redis** 로 구축되었으며, Docker 컨테이너 세트로
배포되고, 월 5달러짜리 VPS 부터 자체 서버까지 모두에서 실행됩니다.

호스팅형 플랫폼과 달리 **코드, 데이터베이스, 그리고 고객 데이터를 직접
소유하게 됩니다.** 거래당 수수료도, 락인도 없습니다. 포크하여 독자적인
길을 가고자 한다면, 라이선스가 이를 명시적으로 허용합니다.

<br />

## 에디션

동일한 바이너리입니다. 서명된 라이선스 파일이 런타임에 기능 플래그를
전환합니다. `docker compose up` 을 실행하면 기본으로 Community 를 얻게
되며, 업그레이드는 관리자에 붙여 넣는 키 한 줄이면 됩니다.

| | Community | Pro | Enterprise |
|---|:---:|:---:|:---:|
| 풀 이커머스, 테마, 페이지 빌더, POS UI | ✓ | ✓ | ✓ |
| 자체 결제 프로바이더 연동 | ✓ | ✓ | ✓ |
| 자체 배송 프로바이더 연동 | ✓ | ✓ | ✓ |
| 마켓플레이스 접근 (프리미엄 테마 + 통합) | ✓ | ✓ | ✓ |
| Spwig 호스팅 주소 자동완성 | 무료 · 요청 제한 | 상향 제한 | 최고 제한 |
| Spwig 호스팅 GeoIP (방문자 위치) | 무료 · 요청 제한 | 상향 제한 | 최고 제한 |
| 푸시 알림 (iOS 관리자 앱) | 무료 · 요청 제한 | 상향 제한 | 최고 제한 |
| POS (POS 단말기 지원) | ✓ | ✓ | ✓ |
| 웜 IP + DKIM 이 적용된 호스팅 이메일 게이트웨이 | – | ✓ | ✓ |
| 우선 지원 | – | ✓ | ✓ |
| 엔터프라이즈 SSO (Azure AD, Okta) | – | – | ✓ |

<br />

## 빠른 시작

### 옵션 1 — 원 라인 설치 (권장)

[Spwig 인스톨러](https://github.com/Spwig/spwig)가 한 번의 명령으로
모든 것을 설정합니다: Docker, PostgreSQL, Redis, MinIO, Cloudflare 또는
자체 서명을 통한 TLS, 최초 부팅 마법사, 관리자 계정까지.
`registry.spwig.com` 에서 서명된 이미지가 받아집니다.

```bash
curl -fsSL https://spwig.com/install.sh | sudo bash
```

업그레이드는 관리자에서 수행합니다 — [UPGRADING.md](UPGRADING.md) 를
참고하세요.

### 옵션 2 — 소스에서 빌드

이 저장소에서 직접 빌드하거나, 코드를 손보거나, 포크를 배포하고 싶다면:

```bash
git clone https://github.com/Spwig/commerce.git spwig
cd spwig
cp .env.example .env
docker compose up -d
docker compose exec web ./manage.py migrate --noinput
docker compose exec web ./manage.py createsuperuser
```

스토어프론트는 `http://localhost`, 관리자는
`http://localhost/ko/admin/` 에 있습니다. Community 에디션은 최초
부팅 시 자동으로 활성화됩니다 — 라이선스 서버 왕복도, 키도 필요
없습니다. 이후 업그레이드는 `git pull` 과 `docker compose build` 로
진행합니다.

<br />

## 기능

<table>
  <tr>
    <td width="50%" valign="top">
      <h3>스토어프론트 & 체크아웃</h3>
      <p>기본으로 서버에서 렌더링됩니다 — 빠른 첫 바이트 응답 시간,
      JavaScript 없이도 동작, 모바일 우선 (트래픽의 80% 는 작은
      화면입니다). 헤드리스 모드는
      <a href="https://github.com/Spwig/headless-sdk">Spwig 헤드리스
      SDK</a> 와 <a href="https://github.com/Spwig/react">React
      컴포넌트</a> 를 통해 선택적으로 사용할 수 있습니다.</p>
    </td>
    <td width="50%" valign="top">
      <img src="https://spwig.com/images/screenshots/storefront-product.webp" alt="Storefront product page">
    </td>
  </tr>
  <tr>
    <td width="50%" valign="top">
      <img src="https://spwig.com/images/screenshots/page-builder.webp" alt="Page builder">
    </td>
    <td width="50%" valign="top">
      <h3>페이지 빌더</h3>
      <p>판매자는 재사용 가능한 위젯 — 히어로 섹션, 상품 그리드,
      추천사, 임베드 — 으로 스토어프론트 페이지를 조립하고, 관리자에서
      실시간으로 미리보기를 할 수 있습니다. 위젯은 마켓플레이스에서
      또는 자체 컴포넌트 저장소에서 설치합니다.</p>
    </td>
  </tr>
  <tr>
    <td width="50%" valign="top">
      <h3>주문 & 고객 관리</h3>
      <p>모든 주문, 환불, 정기결제 갱신, 디지털 다운로드, 그리고
      고객 접점을 한곳에서 관리합니다. 일괄 작업, 권한 범위가 지정된
      스태프 역할, CSV/XLSX 내보내기, 푸시 알림이 지원되는 모바일
      관리자 앱 (iOS) 을 제공합니다.</p>
    </td>
    <td width="50%" valign="top">
      <img src="https://spwig.com/images/screenshots/order-management.webp" alt="Order management">
    </td>
  </tr>
  <tr>
    <td width="50%" valign="top">
      <img src="https://spwig.com/images/screenshots/branding-builder.webp" alt="Branding builder">
    </td>
    <td width="50%" valign="top">
      <h3>테마 & 브랜딩</h3>
      <p>디자인 토큰 (색상, 타이포그래피, 간격) 이 스토어프론트와
      관리자를 포함한 모든 표면을 구동합니다. 토큰 하나만 바꾸면
      전체가 업데이트됩니다. 테마는
      <a href="https://github.com/Spwig/components">Spwig/components</a>
      에 있으며 마켓플레이스를 통해 설치됩니다. 직접 만들고 싶다면
      <a href="https://github.com/Spwig/theme-sdk">테마 SDK</a> 를
      사용하세요.</p>
    </td>
  </tr>
  <tr>
    <td width="50%" valign="top">
      <h3>POS (Pro 이상)</h3>
      <p>오프라인 매장 판매자를 위한 완전한 POS 단말기 기능: 바코드
      스캔, 분할 결제, 영수증 인쇄, 캐시 드로어 연동, 고객용 디스플레이,
      오프라인 모드까지. Community 에디션에도 코드가 포함되어 있지만
      관리자 화면에는 업그레이드 안내가 표시됩니다 — 포크한다면 그
      부분을 패치해서 없애도 괜찮습니다.</p>
    </td>
    <td width="50%" valign="top">
      <img src="https://spwig.com/images/screenshots/pos-terminal.webp" alt="POS terminal">
    </td>
  </tr>
  <tr>
    <td width="50%" valign="top">
      <img src="https://spwig.com/images/screenshots/developer-portal.webp" alt="Developer portal">
    </td>
    <td width="50%" valign="top">
      <h3>프로바이더 생태계</h3>
      <p>외부 시스템과 통신하는 모든 것 — 결제, 배송, 환율, 번역,
      GeoIP, SMS, 이메일 — 은 플러그인 형태의 프로바이더입니다.
      <a href="https://github.com/Spwig/provider-sdks">프로바이더 SDK</a>
      로 직접 만들어 마켓플레이스에 게시하거나, 비공개 레지스트리를
      자체 호스팅할 수 있습니다.</p>
    </td>
  </tr>
</table>

<br />

## 아키텍처

- **싱글 테넌트.** 각 설치는 하나의 스토어, 하나의 판매자, 하나의
  Django Site 로 구성됩니다. 여러 스토어를 운영하는 판매자는 스토어
  하나당 Spwig 하나를 설치합니다.
- **모듈식 모놀리스.** 마이크로서비스 메쉬가 아닙니다. 단일 Django
  프로세스가 스토어프론트 + 관리자 + REST API + Celery 워커를 모두
  담당합니다. 배포, 이해, 포크가 간단합니다.
- **런타임 기능 게이트.** Community/Pro/Enterprise 모두 동일한
  바이너리로 동작합니다. 서명된 라이선스가 플래그만 전환할 뿐, 코드
  스트리핑은 없습니다.

전체 안내: [ARCHITECTURE.md](ARCHITECTURE.md).

<br />

## 커뮤니티 & 지원

- **Discussions.** 자유로운 질문, 아이디어, 자랑거리 공유:
  [github.com/Spwig/commerce/discussions](https://github.com/Spwig/commerce/discussions).
- **커뮤니티 포럼.** [community.spwig.com](https://community.spwig.com)
  — 심층 스레드, 모범 사례 레시피, 확장 기능 쇼케이스가 있습니다.
- **버그 리포트.** 재현 단계와 함께
  [Issues](https://github.com/Spwig/commerce/issues) 에 남겨 주세요.
  취약점 공개는 [SECURITY.md](SECURITY.md) 를 참고하세요.
- **상용 지원.** Pro 및 Enterprise 라이선스에서 이용 가능합니다.

<br />

## 기여하기

저희는 **DCO** (Developer Certificate of Origin) 를 사용합니다 — 모든
커밋은 `git commit -s` 로 사인오프됩니다. 서류 작업이나 CLA 는
없습니다. 자세한 내용은 [CONTRIBUTING.md](CONTRIBUTING.md) 를
확인하세요.

이 저장소에서 작업하는 AI 코딩 어시스턴트를 위한 안내는
[CLAUDE.md](CLAUDE.md) 에 있습니다.

<br />

## 생태계

[Spwig 조직](https://github.com/Spwig) 아래의 관련 오픈소스
프로젝트들입니다:

| Repo | 설명 |
|---|---|
| [Spwig/commerce](https://github.com/Spwig/commerce) | 이 저장소 — 핵심 플랫폼 (AGPL-3.0-or-later) |
| [Spwig/spwig](https://github.com/Spwig/spwig) | 원 라인 인스톨러 |
| [Spwig/components](https://github.com/Spwig/components) | 테마, 통합, 유틸리티 (AGPL-3.0-or-later) |
| [Spwig/theme-sdk](https://github.com/Spwig/theme-sdk) | 테마 구축용 SDK (Apache-2.0) |
| [Spwig/provider-sdks](https://github.com/Spwig/provider-sdks) | 결제 / 배송 등 프로바이더 구축용 SDK (Apache-2.0) |
| [Spwig/headless-sdk](https://github.com/Spwig/headless-sdk) | 헤드리스 / API 클라이언트 SDK (Apache-2.0) |
| [Spwig/react](https://github.com/Spwig/react) | React 컴포넌트 라이브러리 (Apache-2.0) |

<br />

## 라이선스

Spwig 는 [AGPL-3.0-or-later](LICENSE) 로 배포됩니다. 실행, 수정, 재배포,
호스팅형 서비스로 제공 — 모두 허용됩니다. 네트워크를 통해 제공되는 수정
버전은 사용자에게 소스를 공개해야 합니다. 이것이 GPL 대비 AGPL 의 존재
이유입니다.

SDK 로 구축된 프로바이더 통합은 Apache-2.0 이므로, SDK 위에서 독점적인
결제 / 배송 / SMS 통합을 만들어도 AGPL 이 트리거되지 않습니다. 이는
의도된 설계입니다 — 저희는 활발한 프로바이더 생태계를 원합니다.

<br />

## 프라이버시 & 텔레메트리

Spwig 는 `updates.spwig.com/api/v1/telemetry/` 로 하루 한 번 익명 핑을
전송합니다:

- 설치 UUID (최초 부팅 시 생성되어 로컬에 저장)
- Spwig 버전
- 에디션 (community / pro / enterprise / trial / dev)
- 국가 (수신 시점의 IP 에서 확인되며, IP 자체는 저장되지 않습니다)
- 기능 플래그의 버킷 카운트 (설정된 결제 프로바이더, 설치된 테마 등) —
  원시 고객 또는 주문 데이터는 절대 포함되지 않습니다

환경 변수에 `SPWIG_TELEMETRY=0` 을 설정하면 **비활성화** 됩니다. 이
설정은 `settings.SPWIG_TELEMETRY_ENABLED` 를 뒤집으며, 일일 비트 작업은
아무 동작도 하지 않습니다.

<br />

<p align="center">
  <sub>
    싱가포르에서 정성껏 만들었습니다.
    <br />
    <a href="https://spwig.com">spwig.com</a> — <a href="https://docs.spwig.com">docs</a> — <a href="https://community.spwig.com">community</a>
  </sub>
</p>
