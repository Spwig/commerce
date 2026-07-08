<p align="center">
  <a href="README.md">English</a> |
  <a href="README.fr.md">Français</a> |
  <a href="README.es.md">Español</a> |
  <a href="README.de.md">Deutsch</a> |
  <a href="README.ja.md">日本語</a> |
  <strong>简体中文</strong> |
  <a href="README.zh-Hant.md">繁體中文</a> |
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
  <strong>面向希望真正掌控自己商店的商家的自托管电商平台。</strong>
</p>

<p align="center">
  <a href="https://spwig.com">官网</a> &nbsp;•&nbsp;
  <a href="https://docs.spwig.com">文档</a> &nbsp;•&nbsp;
  <a href="https://community.spwig.com">社区</a> &nbsp;•&nbsp;
  <a href="https://spwig.com/zh-Hans/marketplace">应用市场</a> &nbsp;•&nbsp;
  <a href="https://spwig.com/zh-Hans/demos">在线演示</a>
</p>

<p align="center">
  <a href="LICENSE"><img alt="Licence: AGPL v3" src="https://img.shields.io/badge/licence-AGPL--3.0-blue.svg"></a>
  <a href="https://github.com/Spwig/commerce/actions"><img alt="CI" src="https://img.shields.io/github/actions/workflow/status/Spwig/commerce/test.yml?branch=main&label=tests"></a>
  <a href="https://github.com/Spwig/commerce/releases"><img alt="Release" src="https://img.shields.io/github/v/release/Spwig/commerce"></a>
  <a href="https://github.com/Spwig/commerce/discussions"><img alt="Discussions" src="https://img.shields.io/github/discussions/Spwig/commerce"></a>
</p>

## Spwig 是什么？

Spwig 是一款功能齐全的电商平台：商品目录、购物车、结账、订单、客户、支付、物流、主题、页面构建器、后台 API、POS、订阅、会员、博客、SEO——全套齐备。基于 **Django 5**、**PostgreSQL** 与 **Redis** 构建，以一组 Docker 容器的形式发布，可运行在 5 美元的 VPS 上，也可以部署在您自己的物理服务器上。

与托管平台不同，**代码、数据库以及客户数据都归您所有。** 没有按笔交易的抽成，没有厂商锁定。如果您想 fork 一份并走自己的路，许可证也明确允许这样做。

<br />

## 版本

同一份二进制。一个签名的许可证文件在运行时切换功能开关。执行 `docker compose up` 时默认得到的就是 Community 版；升级只需将一个密钥粘贴进后台。

| | Community | Pro | Enterprise |
|---|:---:|:---:|:---:|
| 完整电商、主题、页面构建器、POS 界面 | ✓ | ✓ | ✓ |
| 自带支付服务商 | ✓ | ✓ | ✓ |
| 自带物流服务商 | ✓ | ✓ | ✓ |
| 应用市场访问（付费主题 + 集成） | ✓ | ✓ | ✓ |
| Spwig 托管的地址自动补全 | 免费 · 有速率限制 | 更高上限 | 最高上限 |
| Spwig 托管的 GeoIP（访客位置） | 免费 · 有速率限制 | 更高上限 | 最高上限 |
| 推送通知（iOS 后台应用） | 免费 · 有速率限制 | 更高上限 | 最高上限 |
| 销售点（POS 终端支持） | – | ✓ | ✓ |
| 带有预热 IP 与 DKIM 的托管邮件网关 | – | ✓ | ✓ |
| 优先技术支持 | – | ✓ | ✓ |
| 企业级 SSO（Azure AD、Okta） | – | – | ✓ |

<br />

## 快速开始

### 方式一 —— 一行命令安装（推荐）

[Spwig 安装器](https://github.com/Spwig/spwig)通过一条命令搞定全部环境：Docker、PostgreSQL、Redis、MinIO、通过 Cloudflare 签发或自签名的 TLS、首次启动向导、管理员账号。已签名的镜像从 `registry.spwig.com` 拉取。

```bash
curl -fsSL https://spwig.com/install.sh | sudo bash
```

升级在后台中完成——参见 [UPGRADING.md](UPGRADING.md)。

### 方式二 —— 从源码构建

如果您想从本仓库自行构建、进行二次开发或发布 fork：

```bash
git clone https://github.com/Spwig/commerce.git spwig
cd spwig
cp .env.example .env
docker compose up -d
docker compose exec web ./manage.py migrate --noinput
docker compose exec web ./manage.py createsuperuser
```

店铺前台在 `http://localhost`，后台在 `http://localhost/zh-Hans/admin/`。Community 版会在首次启动时自动激活——无需与许可证服务器往返通信，也无需任何密钥。之后通过 `git pull` 与 `docker compose build` 升级即可。

<br />

## 功能特性

<table>
  <tr>
    <td width="50%" valign="top">
      <h3>店铺前台与结账</h3>
      <p>默认服务端渲染——首字节响应时间快，无 JavaScript 也能工作，移动优先（80% 的流量来自小屏设备）。可选的无头模式通过
      <a href="https://github.com/Spwig/headless-sdk">Spwig headless
      SDK</a> 与 <a href="https://github.com/Spwig/react">React
      组件库</a>接入。</p>
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
      <h3>页面构建器</h3>
      <p>商家用可复用的小组件搭建店铺页面——头图区块、商品网格、用户评价、外部嵌入——并在后台实时预览。小组件可以从应用市场安装，也可以来自您自己的组件仓库。</p>
    </td>
  </tr>
  <tr>
    <td width="50%" valign="top">
      <h3>订单与客户管理</h3>
      <p>每一笔订单、退款、订阅续费、数字下载以及客户触点都汇总到一处。支持批量操作、按权限划分的员工角色、导出 CSV/XLSX，以及带推送通知的移动后台应用（iOS）。</p>
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
      <h3>主题与品牌</h3>
      <p>设计令牌（颜色、字体、间距）驱动每一个界面——店铺前台与后台皆然。修改一个令牌，所有地方随之更新。主题存放于
      <a href="https://github.com/Spwig/components">Spwig/components</a>，通过应用市场安装；也可以使用
      <a href="https://github.com/Spwig/theme-sdk">主题 SDK</a>编写您自己的主题。</p>
    </td>
  </tr>
  <tr>
    <td width="50%" valign="top">
      <h3>销售点（Pro 及以上）</h3>
      <p>面向实体门店的完整 POS 终端：条码扫描、拆分支付、小票打印、钱箱联动、面向顾客的显示屏、离线模式。Community 版附带了这部分代码，但后台入口会显示升级提示——如果您 fork 后想把它去掉，也完全可以。</p>
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
      <h3>服务商生态</h3>
      <p>凡是需要与外部系统对接的部分——支付、物流、汇率、翻译、GeoIP、短信、邮件——都是可插拔的服务商。您可以用
      <a href="https://github.com/Spwig/provider-sdks">服务商 SDK</a>自行构建，发布到应用市场，或自托管一个私有仓库。</p>
    </td>
  </tr>
</table>

<br />

## 架构

- **单租户。** 每一次安装对应一家店铺、一位商家、一个 Django Site。经营多家店铺的商家为每家店铺各部署一套 Spwig。
- **模块化单体。** 不是微服务网格。单个 Django 进程同时处理店铺前台、后台、REST API 与 Celery 任务队列。部署、理解与 fork 都很简单。
- **运行时特性开关。** Community/Pro/Enterprise 运行的是同一份二进制。签名的许可证切换开关——不做代码裁剪。

完整介绍：[ARCHITECTURE.md](ARCHITECTURE.md)。

<br />

## 社区与支持

- **Discussions。** 开放式提问、创意分享、成果展示：
  [github.com/Spwig/commerce/discussions](https://github.com/Spwig/commerce/discussions)。
- **社区论坛。** [community.spwig.com](https://community.spwig.com)——长篇讨论、最佳实践、扩展展示。
- **缺陷反馈。** 提交带复现步骤的 [Issues](https://github.com/Spwig/commerce/issues)。安全漏洞披露请参见 [SECURITY.md](SECURITY.md)。
- **商业支持。** 提供给 Pro 与 Enterprise 授权用户。

<br />

## 参与贡献

我们采用 **DCO**（Developer Certificate of Origin，开发者原创声明）——每一次提交都用 `git commit -s` 附上签署。无需签署纸质文件，也没有 CLA。完整指南请见 [CONTRIBUTING.md](CONTRIBUTING.md)。

面向在本仓库工作的 AI 编码助手的说明请见 [CLAUDE.md](CLAUDE.md)。

<br />

## 生态

[Spwig 组织](https://github.com/Spwig)下的相关开源项目：

| 仓库 | 简介 |
|---|---|
| [Spwig/commerce](https://github.com/Spwig/commerce) | 本仓库——核心平台（AGPL-3.0-or-later） |
| [Spwig/spwig](https://github.com/Spwig/spwig) | 一行命令安装器 |
| [Spwig/components](https://github.com/Spwig/components) | 主题、集成与工具组件（AGPL-3.0-or-later） |
| [Spwig/theme-sdk](https://github.com/Spwig/theme-sdk) | 构建主题的 SDK（Apache-2.0） |
| [Spwig/provider-sdks](https://github.com/Spwig/provider-sdks) | 构建支付 / 物流等服务商的 SDK（Apache-2.0） |
| [Spwig/headless-sdk](https://github.com/Spwig/headless-sdk) | 无头 / API 客户端 SDK（Apache-2.0） |
| [Spwig/react](https://github.com/Spwig/react) | React 组件库（Apache-2.0） |

<br />

## 许可证

Spwig 采用 [AGPL-3.0-or-later](LICENSE) 授权。您可以运行、修改、分发它，也可以以托管服务的形式对外提供——这些都被允许。通过网络对外提供的修改版本，必须向其用户开放源代码。这正是 AGPL 相对 GPL 存在的意义。

基于 SDK 构建的服务商集成使用 Apache-2.0 授权，因此在 SDK 之上构建一个专有的支付 / 物流 / 短信集成不会触发 AGPL。这是有意为之——我们希望看到一个繁荣的服务商生态。

<br />

## 隐私与遥测

Spwig 每天向 `updates.spwig.com/api/v1/telemetry/` 发送一次匿名心跳，内容包括：

- 安装 UUID（首次启动时生成，在本地保存）
- Spwig 版本
- 版本类型（community / pro / enterprise / trial / dev）
- 国家/地区（在接入侧根据 IP 解析得到；IP 本身不会被保存）
- 特性开关的分桶计数（已配置的支付服务商数量、已安装的主题数量）——绝不包含客户或订单原始数据

**关闭遥测**只需在环境变量中设置 `SPWIG_TELEMETRY=0`。这会切换 `settings.SPWIG_TELEMETRY_ENABLED`，让每日的 beat 任务变为空操作。

<br />

<p align="center">
  <sub>
    用心打造于新加坡。
    <br />
    <a href="https://spwig.com">spwig.com</a> — <a href="https://docs.spwig.com">文档</a> — <a href="https://community.spwig.com">社区</a>
  </sub>
</p>
