<p align="center">
  <a href="README.md">English</a> |
  <a href="README.fr.md">Français</a> |
  <a href="README.es.md">Español</a> |
  <a href="README.de.md">Deutsch</a> |
  <a href="README.ja.md">日本語</a> |
  <a href="README.zh-Hans.md">简体中文</a> |
  <strong>繁體中文</strong> |
  <a href="README.pt.md">Português</a> |
  <a href="README.ru.md">Русский</a> |
  <a href="README.ar.md">العربية</a> |
  <a href="README.hi.md">हिन्दी</a> |
  <a href="README.id.md">Bahasa Indonesia</a> |
  <a href="README.it.md">Italiano</a> |
  <a href="README.ko.md">한국어</a> |
  <a href="README.tr.md">Türkçe</a> |
  <a href="README.vi.md">Tiếng Việt</a> |
  <a href="README.th.md">ไทย</a>
</p>

<p align="center">
  <img src="https://spwig.com/images/logo.svg" alt="Spwig" width="200">
</p>

<h1 align="center">Spwig</h1>

<p align="center">
  <strong>為想真正擁有自家商店的商家而生的自架式電子商務平台。</strong>
</p>

<p align="center">
  <a href="https://spwig.com">官方網站</a> &nbsp;•&nbsp;
  <a href="https://docs.spwig.com">技術文件</a> &nbsp;•&nbsp;
  <a href="https://community.spwig.com">社群</a> &nbsp;•&nbsp;
  <a href="https://spwig.com/zh-Hant/marketplace">Marketplace</a> &nbsp;•&nbsp;
  <a href="https://spwig.com/zh-Hant/demos">線上展示</a>
</p>

<p align="center">
  <a href="LICENSE"><img alt="Licence: AGPL v3" src="https://img.shields.io/badge/licence-AGPL--3.0-blue.svg"></a>
  <a href="https://github.com/Spwig/commerce/actions"><img alt="CI" src="https://img.shields.io/github/actions/workflow/status/Spwig/commerce/test.yml?branch=main&label=tests"></a>
  <a href="https://github.com/Spwig/commerce/releases"><img alt="Release" src="https://img.shields.io/github/v/release/Spwig/commerce"></a>
  <a href="https://github.com/Spwig/commerce/discussions"><img alt="Discussions" src="https://img.shields.io/github/discussions/Spwig/commerce"></a>
</p>

## 什麼是 Spwig?

Spwig 是一套功能完整的電子商務平台:商品目錄、購物車、結帳、訂單、顧客、金流、物流、佈景主題、頁面編輯器、管理 API、POS、訂閱、忠誠度、部落格、SEO——整個技術堆疊一應俱全。以 **Django 5**、**PostgreSQL** 和 **Redis** 打造,以一組 Docker 容器發行,可運行於每月 5 美元的 VPS,也可以架設在您自己的實體主機上。

與代管型平台不同,**您完全擁有程式碼、資料庫以及顧客資料。** 沒有交易抽成、沒有鎖定綁約。若您想 fork 走自己的路,授權條款也明確允許這麼做。

<br />

## 版本

同一份執行檔。透過已簽章的授權檔在執行時期切換功能旗標。當您執行 `docker compose up` 時,預設拿到的就是 Community 版;升級只需要在管理後台貼上一組金鑰。

| | Community | Pro | Enterprise |
|---|:---:|:---:|:---:|
| 完整電子商務、佈景主題、頁面編輯器、POS UI | ✓ | ✓ | ✓ |
| 自帶金流服務商 | ✓ | ✓ | ✓ |
| 自帶物流服務商 | ✓ | ✓ | ✓ |
| Marketplace 存取(付費佈景主題+整合套件) | ✓ | ✓ | ✓ |
| Spwig 代管地址自動補全 | 免費 · 有速率限制 | 額度更高 | 額度最高 |
| Spwig 代管 GeoIP(訪客地理位置) | 免費 · 有速率限制 | 額度更高 | 額度最高 |
| 推播通知(iOS 管理應用程式) | 免費 · 有速率限制 | 額度更高 | 額度最高 |
| 銷售終端(POS 終端機支援) | – | ✓ | ✓ |
| 附暖機 IP 與 DKIM 的代管郵件閘道 | – | ✓ | ✓ |
| 優先技術支援 | – | ✓ | ✓ |
| 企業級 SSO(Azure AD、Okta) | – | – | ✓ |

<br />

## 快速上手

### 選項 1 — 一行指令安裝(推薦)

[Spwig 安裝程式](https://github.com/Spwig/spwig) 用一道指令搞定所有事情:Docker、PostgreSQL、Redis、MinIO、透過 Cloudflare 或自簽的 TLS、首次啟動精靈、管理員帳號。所使用的映像檔均為經過簽章、由 `registry.spwig.com` 拉取的版本。

```bash
curl -fsSL https://spwig.com/install.sh | sudo bash
```

升級透過管理後台進行——詳見 [UPGRADING.md](UPGRADING.md)。

### 選項 2 — 從原始碼建置

若您想從本 repo 建置、動手改造,或發行自己的 fork:

```bash
git clone https://github.com/Spwig/commerce.git spwig
cd spwig
cp .env.example .env
docker compose up -d
docker compose exec web ./manage.py migrate --noinput
docker compose exec web ./manage.py createsuperuser
```

商店前台位於 `http://localhost`,管理後台位於 `http://localhost/zh-Hant/admin/`。Community 版於首次啟動時會自動啟用——無需向授權伺服器往返、無需輸入金鑰。日後可透過 `git pull` 與 `docker compose build` 升級。

<br />

## 功能特色

<table>
  <tr>
    <td width="50%" valign="top">
      <h3>商店前台與結帳</h3>
      <p>預設為伺服器端渲染——首位元組時間快速、無需 JavaScript 也能運作、以行動裝置為優先(80% 的流量來自小螢幕)。可透過
      <a href="https://github.com/Spwig/headless-sdk">Spwig headless
      SDK</a> 與 <a href="https://github.com/Spwig/react">React
      元件庫</a> 選擇性地切換為 headless 模式。</p>
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
      <h3>頁面編輯器</h3>
      <p>商家可使用可重複利用的元件——首屏橫幅、商品清單、顧客見證、嵌入區塊——建構商店前台頁面,並於管理後台即時預覽。元件可自 marketplace 安裝,或從您自己的元件儲存庫載入。</p>
    </td>
  </tr>
  <tr>
    <td width="50%" valign="top">
      <h3>訂單與顧客管理</h3>
      <p>每一筆訂單、退款、訂閱續約、數位下載,以及每一個顧客互動點,都集中在同一處。支援批次操作、按權限劃分的員工角色、可匯出為 CSV/XLSX,並提供支援推播通知的 iOS 管理應用程式。</p>
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
      <h3>佈景主題與品牌識別</h3>
      <p>設計代幣(顏色、字體、間距)驅動每一個介面——包含商店前台與管理後台。更改一個代幣,所有介面同步更新。佈景主題存放於
      <a href="https://github.com/Spwig/components">Spwig/components</a>,並透過 marketplace 安裝;您也可以使用
      <a href="https://github.com/Spwig/theme-sdk">theme SDK</a> 撰寫自己的主題。</p>
    </td>
  </tr>
  <tr>
    <td width="50%" valign="top">
      <h3>銷售終端(Pro 以上)</h3>
      <p>為實體店面商家打造的完整 POS 終端:條碼掃描、分次付款、發票列印、錢櫃整合、面客顯示器,以及離線模式。Community 版仍包含這部分程式碼,但管理後台介面會顯示升級提示——若您 fork 走並修掉那段提示,我們沒意見。</p>
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
      <h3>服務商生態系</h3>
      <p>任何與外部系統對接的元件——金流、物流、匯率、翻譯、GeoIP、簡訊、電子郵件——都是可插拔的服務商。您可以透過
      <a href="https://github.com/Spwig/provider-sdks">provider SDK</a> 自行開發,發布到 marketplace,或自架私有的元件註冊表。</p>
    </td>
  </tr>
</table>

<br />

## 架構

- **單租戶。** 每一份安裝對應一家商店、一位商家、一個 Django Site。經營多店的商家可為每一家店各自運行一份 Spwig。
- **模組化單體。** 這不是微服務網格。單一 Django 行程即可處理商店前台+管理後台+REST API+Celery worker。易於部署、易於推理、也易於 fork。
- **執行時期功能開關。** Community/Pro/Enterprise 均執行同一份執行檔。已簽章的授權檔控制旗標——不會抽掉任何程式碼。

完整導覽:[ARCHITECTURE.md](ARCHITECTURE.md)。

<br />

## 社群與支援

- **Discussions。** 開放式提問、想法交流、成果分享:
  [github.com/Spwig/commerce/discussions](https://github.com/Spwig/commerce/discussions)。
- **社群論壇。** [community.spwig.com](https://community.spwig.com)——長篇討論串、最佳實務、擴充展示。
- **臭蟲回報。** 附上重現步驟的 [Issues](https://github.com/Spwig/commerce/issues)。安全漏洞揭露請見 [SECURITY.md](SECURITY.md)。
- **商業支援。** 提供給 Pro 及 Enterprise 授權使用者。

<br />

## 貢獻

我們採用 **DCO**(Developer Certificate of Origin)——每一次提交都以 `git commit -s` 簽署。沒有繁文縟節,也沒有 CLA。完整指南請見 [CONTRIBUTING.md](CONTRIBUTING.md)。

給 AI 程式助理在本 repo 工作時的注意事項,請見 [CLAUDE.md](CLAUDE.md)。

<br />

## 生態系

[Spwig 組織](https://github.com/Spwig) 底下相關的開源專案:

| Repo | 用途 |
|---|---|
| [Spwig/commerce](https://github.com/Spwig/commerce) | 本 repo——核心平台(AGPL-3.0-or-later) |
| [Spwig/spwig](https://github.com/Spwig/spwig) | 一行指令安裝程式 |
| [Spwig/components](https://github.com/Spwig/components) | 佈景主題、整合套件與工具程式(AGPL-3.0-or-later) |
| [Spwig/theme-sdk](https://github.com/Spwig/theme-sdk) | 建構佈景主題的 SDK(Apache-2.0) |
| [Spwig/provider-sdks](https://github.com/Spwig/provider-sdks) | 開發金流/物流/等等服務商的 SDK(Apache-2.0) |
| [Spwig/headless-sdk](https://github.com/Spwig/headless-sdk) | Headless / API 客戶端 SDK(Apache-2.0) |
| [Spwig/react](https://github.com/Spwig/react) | React 元件庫(Apache-2.0) |

<br />

## 授權

Spwig 採用 [AGPL-3.0-or-later](LICENSE) 授權。您可以運行、修改、散布,或作為代管服務對外提供——皆為允許行為。透過網路對外提供的修改版本,必須將原始碼公開給其使用者。這正是 AGPL 相較於 GPL 存在的意義所在。

以 SDK 建置的服務商整合以 Apache-2.0 授權,因此在 SDK 之上開發私有的金流/物流/簡訊整合,並不會觸發 AGPL。這是刻意的設計——我們希望看到一個蓬勃發展的服務商生態系。

<br />

## 隱私與遙測

Spwig 每天會向 `updates.spwig.com/api/v1/telemetry/` 發送一次匿名 ping:

- 安裝 UUID(首次啟動時產生,本地保存)
- Spwig 版本
- 版本別(community / pro / enterprise / trial / dev)
- 國家/地區(由入口 IP 解析而得;IP 本身不會被儲存)
- 功能旗標的分桶計數(已設定的金流服務商、已安裝的佈景主題)——絕不包含原始的顧客或訂單資料

**選擇不參與**:在環境變數中設定 `SPWIG_TELEMETRY=0`。這會將 `settings.SPWIG_TELEMETRY_ENABLED` 反向切換,每日的 beat 任務即成為空操作。

<br />

<p align="center">
  <sub>
    於新加坡用心打造。
    <br />
    <a href="https://spwig.com">spwig.com</a> — <a href="https://docs.spwig.com">docs</a> — <a href="https://community.spwig.com">community</a>
  </sub>
</p>
