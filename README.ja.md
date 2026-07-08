<p align="center">
  <a href="README.md">English</a> |
  <a href="README.fr.md">Français</a> |
  <a href="README.es.md">Español</a> |
  <a href="README.de.md">Deutsch</a> |
  <strong>日本語</strong> |
  <a href="README.zh-Hans.md">简体中文</a> |
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
  <strong>自分の店舗を自ら所有したいマーチャントのためのセルフホスト型 e コマース。</strong>
</p>

<p align="center">
  <a href="https://spwig.com">ウェブサイト</a> &nbsp;•&nbsp;
  <a href="https://docs.spwig.com">ドキュメント</a> &nbsp;•&nbsp;
  <a href="https://community.spwig.com">コミュニティ</a> &nbsp;•&nbsp;
  <a href="https://spwig.com/ja/marketplace">マーケットプレイス</a> &nbsp;•&nbsp;
  <a href="https://spwig.com/ja/demos">ライブデモ</a>
</p>

<p align="center">
  <a href="LICENSE"><img alt="Licence: AGPL v3" src="https://img.shields.io/badge/licence-AGPL--3.0-blue.svg"></a>
  <a href="https://github.com/Spwig/commerce/actions"><img alt="CI" src="https://img.shields.io/github/actions/workflow/status/Spwig/commerce/test.yml?branch=main&label=tests"></a>
  <a href="https://github.com/Spwig/commerce/releases"><img alt="Release" src="https://img.shields.io/github/v/release/Spwig/commerce"></a>
  <a href="https://github.com/Spwig/commerce/discussions"><img alt="Discussions" src="https://img.shields.io/github/discussions/Spwig/commerce"></a>
</p>

## Spwig とは

Spwig はフル機能の e コマースプラットフォームです。カタログ、カート、チェックアウト、注文、顧客、決済、配送、テーマ、ページビルダー、管理 API、POS、サブスクリプション、ロイヤルティ、ブログ、SEO まで、スタック全体を備えています。**Django 5**、**PostgreSQL**、**Redis** で構築されており、一連の Docker コンテナとして提供され、月 5 ドルの VPS でも自前のハードウェアでも動作します。

ホスト型プラットフォームとは異なり、**コード、データベース、顧客データはすべてあなたのものです**。取引ごとの手数料はありません。ロックインもありません。フォークして独自の道を進みたい場合、ライセンスがそれを明示的に許可しています。

<br />

## エディション

同じバイナリです。署名済みのライセンスファイルが実行時に機能フラグを切り替えます。`docker compose up` した際にデフォルトで得られるのは Community 版です。アップグレードは管理画面に貼り付けるキーひとつで行えます。

| | Community | Pro | Enterprise |
|---|:---:|:---:|:---:|
| フル e コマース、テーマ、ページビルダー、POS UI | ✓ | ✓ | ✓ |
| 独自の決済プロバイダーを持ち込み可能 | ✓ | ✓ | ✓ |
| 独自の配送プロバイダーを持ち込み可能 | ✓ | ✓ | ✓ |
| マーケットプレイスへのアクセス（プレミアムテーマ + 連携機能） | ✓ | ✓ | ✓ |
| Spwig ホストの住所オートコンプリート | 無料・レート制限あり | より高い上限 | 最上位の上限 |
| Spwig ホストの GeoIP（訪問者の位置情報） | 無料・レート制限あり | より高い上限 | 最上位の上限 |
| プッシュ通知（iOS 管理アプリ） | 無料・レート制限あり | より高い上限 | 最上位の上限 |
| POS（POS 端末サポート） | – | ✓ | ✓ |
| 温めた IP と DKIM を備えたホスト型メールゲートウェイ | – | ✓ | ✓ |
| 優先サポート | – | ✓ | ✓ |
| エンタープライズ SSO（Azure AD、Okta） | – | – | ✓ |

<br />

## クイックスタート

### 方法 1 — ワンラインインストール（推奨）

[Spwig インストーラー](https://github.com/Spwig/spwig) はすべてを一つのコマンドでセットアップします。Docker、PostgreSQL、Redis、MinIO、Cloudflare もしくは自己署名による TLS、初回起動ウィザード、管理者ユーザーまで含まれます。署名済みイメージは `registry.spwig.com` から取得されます。

```bash
curl -fsSL https://spwig.com/install.sh | sudo bash
```

アップグレードは管理画面から行います。[UPGRADING.md](UPGRADING.md) を参照してください。

### 方法 2 — ソースから

このリポジトリからビルドしたり、いじったり、フォークを配布したい場合はこちらです。

```bash
git clone https://github.com/Spwig/commerce.git spwig
cd spwig
cp .env.example .env
docker compose up -d
docker compose exec web ./manage.py migrate --noinput
docker compose exec web ./manage.py createsuperuser
```

ストアフロントは `http://localhost` に、管理画面は `http://localhost/ja/admin/` にあります。Community 版は初回起動時に自動的にアクティベートされます。ライセンスサーバーへの往復も、キーの入力も不要です。あとから `git pull` と `docker compose build` でアップグレードできます。

<br />

## 機能

<table>
  <tr>
    <td width="50%" valign="top">
      <h3>ストアフロントとチェックアウト</h3>
      <p>デフォルトでサーバーレンダリング。TTFB が速く、JavaScript なしでも動作し、モバイルファースト（トラフィックの 80% は小さな画面から）です。<a href="https://github.com/Spwig/headless-sdk">Spwig ヘッドレス SDK</a> と <a href="https://github.com/Spwig/react">React コンポーネント</a> によるヘッドレスモードもオプションで利用できます。</p>
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
      <h3>ページビルダー</h3>
      <p>マーチャントは再利用可能なウィジェット（ヒーローセクション、商品グリッド、お客様の声、埋め込みなど）を組み合わせてストアフロントのページを構築し、管理画面でライブプレビューできます。ウィジェットはマーケットプレイスまたは自前のコンポーネントリポジトリからインストールできます。</p>
    </td>
  </tr>
  <tr>
    <td width="50%" valign="top">
      <h3>注文と顧客の管理</h3>
      <p>すべての注文、返金、サブスクリプションの更新、デジタルダウンロード、顧客との接点を一箇所に集約します。一括操作、権限スコープ付きのスタッフロール、CSV/XLSX へのエクスポート、プッシュ通知対応のモバイル管理アプリ（iOS）を備えています。</p>
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
      <h3>テーマとブランディング</h3>
      <p>デザイントークン（色、タイポグラフィ、余白）がストアフロントと管理画面のすべてのサーフェスを駆動します。トークンを一つ変更すれば、すべてが更新されます。テーマは <a href="https://github.com/Spwig/components">Spwig/components</a> にあり、マーケットプレイス経由でインストールできます。<a href="https://github.com/Spwig/theme-sdk">テーマ SDK</a> を使って自作することもできます。</p>
    </td>
  </tr>
  <tr>
    <td width="50%" valign="top">
      <h3>POS（Pro 以上）</h3>
      <p>実店舗のマーチャント向けのフル機能 POS 端末です。バーコードスキャン、分割決済、レシート印刷、キャッシュドロワー連携、顧客向けディスプレイ、オフラインモードを備えています。Community 版にもコードは同梱されていますが、管理画面にはアップグレードの CTA が表示されます。フォークしてパッチを当てて外すのは自由です。</p>
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
      <h3>プロバイダーエコシステム</h3>
      <p>外部システムと連携するものすべて（決済、配送、為替レート、翻訳、GeoIP、SMS、メール）はプラグイン可能なプロバイダーです。<a href="https://github.com/Spwig/provider-sdks">プロバイダー SDK</a> を使って独自に構築し、マーケットプレイスに公開したり、プライベートレジストリをセルフホストしたりできます。</p>
    </td>
  </tr>
</table>

<br />

## アーキテクチャ

- **シングルテナント。** 各インストールは 1 つのストア、1 人のマーチャント、1 つの Django Site です。複数店舗を運営するマーチャントは、店舗ごとに 1 つの Spwig インストールを立ち上げます。
- **モジュラーモノリス。** マイクロサービスメッシュではありません。単一の Django プロセスがストアフロント + 管理画面 + REST API + Celery ワーカーを処理します。デプロイも、把握も、フォークもシンプルです。
- **実行時の機能ゲート。** Community/Pro/Enterprise はすべて同じバイナリを実行します。署名済みのライセンスがフラグを切り替え、コードの削ぎ落としは行いません。

詳しくは [ARCHITECTURE.md](ARCHITECTURE.md) をご覧ください。

<br />

## コミュニティとサポート

- **Discussions。** 自由な質問、アイデア、成果の共有はこちら：[github.com/Spwig/commerce/discussions](https://github.com/Spwig/commerce/discussions)。
- **コミュニティフォーラム。** [community.spwig.com](https://community.spwig.com) — 長文のスレッド、ベストプラクティスのレシピ、拡張機能のショーケース。
- **バグ報告。** 再現手順を添えた [Issues](https://github.com/Spwig/commerce/issues) までお願いします。脆弱性の開示については [SECURITY.md](SECURITY.md) をご覧ください。
- **商用サポート。** Pro および Enterprise ライセンス向けにご利用いただけます。

<br />

## コントリビュート

**DCO**（Developer Certificate of Origin）を採用しています。すべてのコミットは `git commit -s` でサインオフします。書類仕事も CLA もありません。詳しいガイドは [CONTRIBUTING.md](CONTRIBUTING.md) にあります。

リポジトリで作業する AI コーディングアシスタント向けのメモは [CLAUDE.md](CLAUDE.md) にあります。

<br />

## エコシステム

[Spwig org](https://github.com/Spwig) 配下の関連オープンソースプロジェクトです。

| リポジトリ | 内容 |
|---|---|
| [Spwig/commerce](https://github.com/Spwig/commerce) | このリポジトリ — コアプラットフォーム（AGPL-3.0-or-later） |
| [Spwig/spwig](https://github.com/Spwig/spwig) | ワンラインインストーラー |
| [Spwig/components](https://github.com/Spwig/components) | テーマ、連携機能、ユーティリティ（AGPL-3.0-or-later） |
| [Spwig/theme-sdk](https://github.com/Spwig/theme-sdk) | テーマを構築するための SDK（Apache-2.0） |
| [Spwig/provider-sdks](https://github.com/Spwig/provider-sdks) | 決済 / 配送などのプロバイダーを構築するための SDK（Apache-2.0） |
| [Spwig/headless-sdk](https://github.com/Spwig/headless-sdk) | ヘッドレス / API クライアント SDK（Apache-2.0） |
| [Spwig/react](https://github.com/Spwig/react) | React コンポーネントライブラリ（Apache-2.0） |

<br />

## ライセンス

Spwig は [AGPL-3.0-or-later](LICENSE) です。実行、改変、配布、ホスト型サービスとしての提供、いずれも許可されています。ネットワーク越しに提供される改変版は、そのユーザーにソースを提供しなければなりません。それこそが GPL に対する AGPL の眼目です。

SDK を使って構築されたプロバイダー連携は Apache-2.0 です。したがって、SDK の上にプロプライエタリな決済 / 配送 / SMS 連携を構築しても AGPL は発火しません。これは意図的な設計です。私たちは繁栄したプロバイダーエコシステムを望んでいます。

<br />

## プライバシーとテレメトリー

Spwig は 1 日 1 回、匿名の ping を `updates.spwig.com/api/v1/telemetry/` に送信します。

- インストール UUID（初回起動時に生成され、ローカルに保存されます）
- Spwig のバージョン
- エディション（community / pro / enterprise / trial / dev）
- 国（送信元の IP から解決されますが、IP そのものは保存されません）
- 機能フラグのバケットカウント（設定された決済プロバイダー数、インストールされたテーマ数など） — 顧客データや注文データの生データは含まれません

環境変数で `SPWIG_TELEMETRY=0` を指定すれば **オプトアウト** できます。これで `settings.SPWIG_TELEMETRY_ENABLED` が切り替わり、日次のビートタスクは何もしなくなります。

<br />

<p align="center">
  <sub>
    シンガポールにて心を込めて構築しました。
    <br />
    <a href="https://spwig.com">spwig.com</a> — <a href="https://docs.spwig.com">docs</a> — <a href="https://community.spwig.com">community</a>
  </sub>
</p>
