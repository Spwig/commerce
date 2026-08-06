---
title: プラットフォームの更新
---

Your Spwig installation is built from a collection of components — themes, widgets, integrations, page builder elements, and provider connections — each with its own version that can be updated independently. The Component Registry gives you a central view of everything installed, shows which components have updates waiting, and lets you install or roll back updates at any time.

![Component Registry Overview](/static/core/admin/img/help/platform-updates/component-registry-overview.webp)

## Understanding the component registry

Navigate to **System Dashboard > Component Updates** to see every component installed on your store. Each row shows:

- **Name** — the component's display name
- **Type** — what kind of component it is (theme, widget, integration, etc.)
- **Current version** — the version currently running on your store
- **Update status** — whether an update is available
- **Channel** — which update channel the component follows
- **Auto Update** — whether updates install automatically
- **Locked** — whether the component is frozen at its current version

The dashboard at the top of the page shows summary counts: total components installed, how many have updates available, and how many are up to date.

### Component types

| Type | What it is |
|------|------------|
| Theme | Your store's visual design |
| Widget | Reusable page builder blocks |
| Page Builder Element | Custom elements for the page builder |
| Page Builder Utility | Editor tools and utilities |
| Header / Footer Template | Header and footer layouts |
| Shipping Provider | Carrier integrations (FedEx, UPS, etc.) |
| Email Provider | Email delivery services |
| Payment Provider | Payment gateway integrations |
| Exchange Rate Provider | Currency rate data sources |
| Translation Provider | AI translation services |
| Language Pack | Interface translation files |

## Update channels

Every component follows an update channel that controls which releases it receives.

各コンポーネントを、ご自身が受け入れ可能なリスクレベルに応じて異なるチャネルに割り当てることができます。

| チャネル | 説明 | 最適な用途 |
|---------|-------------|----------|
| **Stable** | 本番環境で使用可能な、完全にテストされたリリース | ライブストア上のすべてのコンポーネント |
| **Beta** | 本番リリースになる前に新機能をテストするためのプレリリースビルド | プレビューしたい非クリティカルなコンポーネント |
| **Development** | 最新の機能、不安定な可能性あり | テスト環境でのみ使用 |
| **Security** | 重要なセキュリティパッチのみ、最も高い優先度で配信 | 安定性が最優先のコンポーネント |

コンポーネントのチャネルを変更するには、その名前をクリックして詳細ビューを開き、**Update Channel**フィールドで新しい値を選択し、保存してください。

## 更新の確認

Spwigは、更新サーバー設定で構成された間隔（デフォルト: 24時間ごと）で自動的に更新を確認します。すぐに確認するには:

1. **System Dashboard > Component Updates** に移動します
2. ページ上部の **Check for Updates** ボタンをクリックします
3. システムはSpwigの更新サーバーに接続し、すべてのコンポーネントの更新ステータスを更新します
4. 更新が利用可能なコンポーネントはハイライトされ、**Updates Available** のカウントが更新されます

リストのアクションメニューから **Check for Updates** アクションを使用して、個々のコンポーネントの更新確認をトリガーすることもできます。

## 更新のインストール

### 単一のコンポーネントの更新

1. **System Dashboard > Component Updates** に移動します
2. 更新したいコンポーネントを検索します — 更新が利用可能なコンポーネントはバージョンの隣に更新インジケーターが表示されます
3. そのコンポーネントの行にある **Install Update** ボタンをクリックします
4. プロンプトが表示されたら更新を確認します
5. 更新がダウンロードされ、検証され、インストールされます — 各段階の進行状況インジケーターが表示されます
6. 完了すると、コンポーネントの **Current Version** が新しいバージョン番号に更新されます

### 複数のコンポーネントの更新

1.

更新したいコンポーネントの横のチェックボックスを選びます
2.


アクションドロップダウンから **Install updates** を選択します
3.

**Go** をクリックして続行します
4.

更新は依存関係の順序でインストールされます — 他のコンポーネントに依存しているコンポーネントは最初に更新されます

### 更新中に何が起こるか

更新プロセスは次のステージを通って実行されます:

1. **Checking** — 更新が利用可能であり、ライセンスが有効であることを確認します
2. **Downloading** — Spwig 更新サーバーからパッケージを取得します
3. **Verifying** — SHA-256 チェックサムに対してパッケージの整合性を確認します
4. **Extracting** — 新しいファイルを展開します
5. **Deploying** — 新しいバージョンを有効にします
6. **Health check** — 更新後、コンポーネントが正常に動作していることを確認します

どのステージでも失敗した場合、システムは自動的に以前のバージョンへの復元を試みます。

## プラットフォームレベルの更新

個々のコンポーネントに加えて、Spwig はコアストアエンジン自体を更新するプラットフォームレベルの更新を受けることができます。これらの更新は、データベースマイグレーションや短時間のメンテナンスウィンドウを含むより厳密なプロセスを通って行われます。

**System Dashboard > Platform Updates** に移動して、個々のコンポーネントとは別にプラットフォームレベルの更新を表示および管理します。

### インストールする前に変更内容を確認する

**Check for Updates** をクリックして、新しいプラットフォームバージョンが利用可能かどうかを確認します。新しいバージョンが見つかると、**Update Available** カードにバージョン変更（例: `v1.7.0 → v1.7.1`）、**Package Size**、**Est. Time**、更新の **Channel** — そして、インストールする前に変更内容を確認できる **What's New** プレビューが表示されます:

- リリースを説明する短いサマリーライン
- そのバージョンで最も重要な変更点の箇条書きリスト（最大5つ、さらに変更点がある場合はメモが表示されます）

更新がデータベーススキーマを変更する場合、**Requires database migration** の通知が表示され、推定時間が表示されます。

セキュリティリリースでは、**Security update** のバッジが表示され、すぐにインストールすることをお勧めします。

インストールする前にWhat's Newのプレビューを確認してください — これは、リリースがアップグレード後に特別な手順が必要かどうかを確認する最も速い方法です。

プラットフォームの更新履歴は、ページの下部に表示されます。各エントリには、バージョンの変遷（例: `v1.3.2 → v1.3.3`）、ステータス、および更新プロセスの所要時間が表示されます。

セキュリティ更新は個別にマークされ、**Auto Install Security Updates** が更新サーバーの設定で有効になっている場合、手動操作なしに自動的にインストールされます。

## バージョン履歴の確認

コンポーネントの以前にインストールされたすべてのバージョンを確認するには:

1. コンポーネント名をクリックして詳細ビューを開きます
2. ページの下部にある **Component Versions** セクションにスクロールします
3. 各バージョンエントリには、バージョン番号、インストールされた日時、インストール方法、および健康状態が表示されます

システムは、ロールバック可能な最後の3つのインストール済みバージョンを保持します。それ以降のバージョンは自動的に削除されます。

## コンポーネントのロールバック

更新が問題を引き起こした場合、以前のバージョンにロールバックできます:

1. コンポーネントの詳細ビューを開きます
2. ページ下部の **Rollback** セクションにスクロールします
3. ロールバックしたいバージョンを選択します
4. **Roll Back to this Version** をクリックします

**Rollback Available** とマークされたバージョンのみが復元可能です。ロールバックログエントリには、ロールバックを開始した人物と時刻が記録されます。

## コンポーネントのロック

コンポーネントをロックすると、自動的な更新を含め、すべての更新のインストールが防止されます。これは、特定のバージョンに依存するカスタマイズや統合がある場合に役立ちます。

1. コンポーネントの詳細ビューを開きます
2. **Lock & Freeze** セクションの **Locked** チェックボックスをチェックします
3. **Lock Reason** に理由を入力して、チームがなぜ凍結されているのか理解できるようにします
4. レコードを保存します

ロックされたコンポーネントは、レジストリリストでロックアイコンで表示されます。ロックを解除するには、**Locked** を外して保存します。

## 更新ログの閲覧

アップデートログは、すべてのインストール、更新、ロールバック、およびヘルスチェック操作を記録します：

1. コンポーネントの詳細ビューを開きます
2. **アップデートログ**は、ページの下部にインラインで表示されます
3. 各エントリには、実施されたアクション、開始および終了時間、古いバージョンと新しいバージョン、自動または手動の有無、および操作が失敗した場合のエラーメッセージが表示されます

**失敗**ステータスのログエントリには、トラブルシューティングを助けるために完全なエラーメッセージが含まれています。

## 自動更新の有効化

Spwigが更新を自動でインストールできるように許可できます：

1. コンポーネントの詳細ビューを開きます
2. **バージョン & 更新ステータス**セクションで**自動更新**をチェックします
3. レコードを保存します

自動更新が有効になっている場合、システムは次のスケジュールされたチェックサイクル中に更新をインストールします。セキュリティ更新は、個々のコンポーネント設定に関係なく、グローバルな**セキュリティ更新の自動インストール**設定に従います。

## ヒント

- テーマや支払いプロバイダーは常に**Stable**チャネルで更新してください — これらは最も顧客に直接関係するコンポーネントであり、安定性が最も重要です
- コンポーネントをカスタム変更する前にロックし、理由を明確に記録して、将来的なチームメンバーが更新しないようにする必要があります
- メジャーバージョンアップをインストールする前に、コンポーネントのバージョンエントリで**リリースノート**を確認してください — ブレイキング変更はそこにフラグされます
- プラットフォーム更新をインストールする前に、**Platform Updates**ページの**What's New**プレビューを確認してください — リリースノートの詳細を確認するには、**System Upgrade**ページに進んでください
- 更新後は、ストアの影響を受けたエリアにアクセスして、すべてが予期通り表示され、動作していることを確認した後で、更新が完了したと宣言してください
- コンポーネントで自動更新が有効になっている場合、**Update Logs**を定期的に確認して、自動更新が正常に完了していることを確認してください