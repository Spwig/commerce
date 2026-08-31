---
title: 電子メールの設定
---

電子メールの設定は、ストアが送信するトランザクションメール（注文確認、配送通知、パスワードリセットなど）の送信方法を制御します。Spwigには、組み込みのSMTPサーバーが含まれており、より高い配信性のための外部電子メールプロバイダーもサポートしています。

![電子メールアカウント](/static/core/admin/img/help/email-configuration/email-accounts.webp)

## 利用可能なプロバイダー

| プロバイダー | 説明 |
|----------|-------------|
| **組み込みSMTP** | Spwigに含まれる無料で自己ホストされた電子メールサーバー。自動的なDKIM署名。 |
| **Gmail API** | OAuth認証を使用して、GmailまたはGoogle Workspaceアカウント経由で電子メールを送信します。 |
| **汎用SMTP** | 任意のSMTPサーバー（SendGrid、Mailgun、Amazon SES、または独自のメールサーバー）に接続します。 |

## 電子メールの設定

**設定 > 電子メールアカウント**に移動し、セットアップウィザードを起動するには**電子メールアカウントの追加**をクリックしてください。

### ステップ1: プロバイダーの選択

電子メールプロバイダーを選択してください。組み込みSMTPサーバーは、始めに使用する最も簡単なオプションです。外部アカウントは必要ありません。

### ステップ2: 認証情報の構成

選択したプロバイダーの認証情報を入力してください：

- **組み込みSMTP** — 認証情報は必要ありません。サーバーはSpwigインストールで動作します。
- **Gmail API** — Google OAuth経由で認証します。Googleアカウントでサインインするようリダイレクトされます。
- **汎用SMTP** — SMTPサーバーアドレス、ポート、ユーザー名、パスワードを入力してください。

### ステップ3: 送信者設定

送信メールの送信者情報を設定してください：

- **送信元メールアドレス** — メールの「送信元」フィールドに表示されるメールアドレス（例: orders@yourstore.com）
- **送信者名** — メールアドレスの隣に表示される表示名（例: "Your Store Name"）
- **返信先メールアドレス** — 顧客が返信する先（送信元アドレスと異なる場合があります）

### ステップ4: DNS検証

ドメインの電子メール認証レコードを検証してください。ウィザードは3つのDNSレコードをチェックします：

{"| Record | Purpose |\n|--------|---------|\n| **SPF** | あなたのドメインのメールを送信するサーバーを認証します |\n| **DKIM** | メールをデジタル署名して、改ざんされていないことを証明します |\n| **DMARC** | 送信サーバーがSPF/DKIMチェックに合格しないメールに対して何をすべきかを指示します |\n|\nFor each record, the wizard shows: |\n- **Current status** — Whether the record is correctly configured |\n- **Required value** — The exact DNS record to add at your domain registrar |\n- **Propagation status** — Whether recent changes have taken effect (DNS changes can take up to 48 hours) |\n|\nThe built-in SMTP server automatically generates DKIM keys for your domain. |\n|\n### Step 5: Send Test Email |\n|\nSend a test email to verify everything works: |\n1. Enter a recipient email address |\n2. Click **Send Test** |\n3. Check your inbox for the test message |\n4. Verify the email arrives without spam warnings |\n|\n### Step 6: Save and Activate |\n|\nSave the configuration and set the account as active. Mark it as **Default** if it should be the primary email account. |\n|\n## Email Templates |\n|\nSpwig includes 30+ email templates for every transactional event. Navigate to **Settings > Email Templates** to manage them. |\n|\n### Template Types |\n|\nTemplates cover all store events including: |\n- **Order Lifecycle** — Confirmation, processing, shipped, delivered, cancelled |\n- **Payment** — Receipt, refund confirmation, failed payment |\n- **Customer Account** — Welcome, password reset, email verification |\n- **Gift Cards** — Delivery, balance notification |\n- **Shipping** — Tracking updates, delivery confirmation |\n- **Digital Products** — Download links, license keys |\n- **Marketing** — Abandoned cart recovery, review requests |\n|\n### Customizing Templates |\n|\n1. navigate to the template list |\n2. click a template to edit |\n3. modify the subject line, header, body content, and footer |\n4. use template variables (e.g., `{{ order.number }}`, `{{ customer.name }}`) for dynamic content |\n5. preview the email before saving |\n|\n### Multi-Language Support |\n|\nPreserve all markdown formatting, image paths, code blocks, and technical terms."}

メールテンプレートは複数言語をサポートしています：
- 各テンプレートは、ストアで有効なすべての言語の翻訳を持つことができます
- システムは、顧客が希望する言語でメールを送信します
- **言語フォールバックチェーン** — 翻訳が利用できない場合、システムはストアのデフォルト言語にフォールバックします
- **AI翻訳** 機能を使用して、テンプレートを他の言語に自動的に翻訳できます

### テンプレートのクローン作成

システムテンプレートのカスタマイズされたバージョンを作成するには：
1. 変更したいテンプレートを開く
2. **テンプレートをクローン** をクリックする
3. クローンされたバージョンを編集する
4. クローンは元のシステムテンプレートよりも優先されます

## メールキュー

**設定 > メールキュー** で送信予定のメールを監視できます：

- **キューイング中** — 送信待ちのメール
- **送信中** — 現在送信されているメール
- **送信済み** — 正常に配信されたメール
- **失敗** — 配信できなかったメール（エラー詳細付き）
- **バウンス** — 受信者のメールサーバーによって拒否されたメール

メールをクリックすると、受信者、件名、送信時刻、配信ステータスを含む詳細を表示できます。

## 配信トラッキング

メールのエンゲージメントをトラッキングします：
- **開封数** — メールを開いた受信者の数
- **クリック数** — メール内のリンクのクリック数
- **バウンス** — ハードバウンスとソフトバウンスのトラッキング
- **苦情** — 受信者からのスパム報告

## 複数アカウント

複数のメールアカウントを設定できます：
- **デフォルトアカウント** — 上書きされない限り、すべての送信メールに使用されます
- **フォールバック** — デフォルトアカウントが失敗した場合、メールは再試行のためにキューに追加されます
- 異なる目的に異なるアカウントを使用できます（例：トランザクションメール用とマーケティングメール用）

## メール配信モード

**設定 > ストア設定** に移動して、ストアが送信メールをどのように処理するかを制御します。これらの設定は開発およびテスト中に便利です。

| モード | 説明 |
|------|-------------|
| **ライブ** | メールは通常通り実際の受信者に送信されます |
| **一時停止** | メールはキューに保持され、再びライブモードに切り替えるまで送信されません |
| **ログのみ** | メールはアウトボックスに記録されますが、決して送信されません |

### テストリダイレクトメール

すべての送信メールをインターセプトし、単一のアドレスにリダイレクトするための**テストリダイレクトメール**アドレスを設定してください。この設定を行うと、実際の受信者に関係なく、すべてのメールがそのアドレスに送信されます。これは、実際の顧客に誤って送信することなくメールテンプレートのテストに役立ちます。実際の受信者にメールを送信するには空にしておいてください。

### サンドボックスメールホワイトリスト

サンドボックスまたは開発モードでは、承認されたアドレスのホワイトリストに制限してメール配信を制限できます。ホワイトリストに追加されたアドレスへのみメールが配信されます。他のすべてのメールはログに記録されますが、決して送信されません。管理アドレスは常に自動的に含められます。最大で10件のアドレスを追加できます。

## トipp

- すぐに設定を完了できる**組み込みのSMTP**サーバーを使用してください。その後、送信ボリュームや配信性を向上させるために外部の提供元に切り替えてください。
- **SPF、DKIM、DMARC**レコードを常に構成してください。これらがないと、メールがスパムフォルダに届く可能性がはるかに高くなります。
- すべての構成変更の後に**テストメール**を送信して、配信が動作することを確認してください。
- メールキュー内の**失敗**や**バウンス**メールを定期的にモニタリングしてください。これは配信性の問題を示しています。
- **プロフェッショナルな送信アドレス**（例: orders@yourstore.com）を使用してください。無料メールアドレスよりも信頼性や配信性が向上します。
- テンプレートを簡潔に保ってください。トランザクションメールは情報を素早く提供するものであり、マーケティングニュースレターになってはなりません。