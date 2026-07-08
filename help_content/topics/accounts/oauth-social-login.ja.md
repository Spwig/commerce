---
title: OAuthとソーシャルログインの設定
---

OAuthとソーシャルログインは、顧客が既存のGoogle、Apple、またはMicrosoftアカウントを使用してストアにログインできるようにします。別のパスワードを新たに作成して覚える必要はありません。

![OAuth設定](/static/core/admin/img/help/oauth-social-login/oauth-settings.webp)

## OAuth / ソーシャルログインとは？

OAuthは、Google、Apple、Microsoftなどの信頼できるプロバイダーの資格情報を使用して顧客がログインできるセキュアな認証基準です。

### ベネフィット

- **より速いチェックアウト** — 顧客は登録フォームをスキップし、1クリックでログインできます
- **摩擦の減少** — パスワードの作成、確認メール、忘れられたパスワードのフローが不要になります
- **より良いコンバージョン** — 調査では、ソーシャルログインがコンバージョン率を20〜40％向上させることを示しています
- **セキュリティの向上** — 資格情報はあなたのストアを通じて送信されません。認証はプロバイダーによって処理されます
- **顧客の信頼** — 顧客は既存のプロバイダーにログイン資格情報を信頼しています

### 仕組み

1. 顧客がログインページで"Googleでログイン"（またはApple/Microsoft）をクリックします
2. 顧客はプロバイダーのセキュアなログインページにリダイレクトされます
3. 顧客はプロバイダーの資格情報を使用して認証します
4. プロバイダーは検証されたID情報をストアに戻します
5. 顧客は自動的にログインされます

初めてのログイン時、プロバイダーのメールとプロフィール情報を使って新しい顧客アカウントが自動的に作成されます。

## サポートされているプロバイダー

Spwigは3つの主要なOAuthプロバイダーをサポートしています：

| プロバイダー | 用途 | 資格情報の要件 |
|----------|----------|------------------------|
| **Google** | 最も人気があり、設定が最も簡単 | クライアントID、クライアントシークレット |
| **Apple** | iOSアプリに必要、プライバシーに重きを置いている | クライアントID、チームID、キーID、プライベートキー |
| **Microsoft** | 企業顧客、Office 365ユーザー | クライアントID、クライアントシークレット、テナントID |

1つ、2つ、または3つのプロバイダーを有効にできます。それぞれは独立して動作します。

## Google OAuthの設定

Google OAuthは最も人気があり、設定が最も簡単です。

### 事前条件

- Googleアカウント
- Google Cloud Consoleへのアクセス

### 設定手順

1. **OAuth設定に移動**
   - 管理パネルで **Settings > Store Settings** に移動
   - **OAuth Providers** セクションにスクロール
   - **Configure Google** をクリック

2. **Google Cloudプロジェクトの作成**
   - [Google Cloud Console](https://console.cloud.google.com/) にアクセス
   - **Create Project** をクリック
   - プロジェクト名を入力（例: "My Store OAuth"）
   - **Create** をクリック

3. **Google+ APIの有効化**
   - 左のサイドバーで **APIs & Services > Library** に移動
   - "Google+ API" を検索
   - **Enable** をクリック

4. **OAuth資格情報の作成**
   - **APIs & Services > Credentials** に移動
   - **Create Credentials > OAuth client ID** をクリック
   - アプリケーションタイプを選択: **Web application**
   - 名前を入力（例: "Store Login"）

5. **リダイレクトURIの設定**
   - **Authorized redirect URIs** で以下を追加：
     ```
     https://yourdomain.com/accounts/google/login/callback/
     ```
   - `yourdomain.com` を実際のドメインに置き換えます
   - **Create** をクリック

6. **資格情報のコピー**
   - ポップアップから **Client ID** と **Client Secret** をコピーします

7. **Spwigに資格情報を入力**
   - Spwigの管理パネルのOAuth設定に戻ります
   - Client IDとClient Secretを貼り付けます
   - **Save** をクリック
   - **Enable Google OAuth** を有効にするスイッチをオンにします

### テスト

- ストアフロントのログインページにアクセスします
- "Googleでログイン"ボタンを探します
- それをクリックしてGoogleアカウントで認証します
- ログインし、顧客ダッシュボードにリダイレクトされるはずです

## Apple OAuthの設定

Apple OAuthは、キーベースの認証システムのため、Googleよりも複雑です。

### 事前条件

- Apple Developerアカウント（有料メンバーシップが必要）
- Apple Developerポータルへのアクセス

### 設定手順

1. **OAuth設定に移動**
   - **Settings > Store Settings > OAuth Providers** に移動
   - **Configure Apple** をクリック

2. **サービスIDの作成**
   - [Apple Developer](https://developer.apple.com/account/) にログイン
   - **Certificates, Identifiers & Profiles** に移動
   - **Identifiers** をクリックし、その後 **+** ボタンをクリック
   - **Services IDs** を選択し、**Continue** をクリック
   - 説明を入力（例: "Store Login"）
   - 識別子を入力（例: `com.yourstore.login`）
   - **Continue** をクリックし、その後 **Register** をクリック

3. **サービスIDの設定**
   - 新しく作成したサービスIDをクリックします
   - **Sign In with Apple** をチェックします
   - **Configure** をクリックします
   - ドメインとリターンURLを追加します：
     - **Domains**: `yourdomain.com`
     - **Return URLs**: `https://yourdomain.com/accounts/apple/login/callback/`
   - **Save** をクリックし、その後 **Continue** と **Save** を再度クリックします

4. **キーの作成**
   - 左のサイドバーで **Keys** をクリックし、その後 **+** ボタンをクリックします
   - キー名を入力（例: "Store OAuth Key"）
   - **Sign In with Apple** をチェックします
   - **Configure** をクリックし、プライマリアプリIDを選択します
   - **Save** をクリックし、その後 **Continue** と **Register** をクリックします
   - **.p8ファイルのキーをダウンロード** — 再度ダウンロードすることはできません

5. **必要な情報を集める**
   あなたは以下を必要とします：
   - **Client ID**（サービスID）: 作成した識別子（例: `com.yourstore.login`）
   - **Team ID**: Apple Developerポータルの右上に表示されます
   - **Key ID**: キーを作成したときに表示されます
   - **Private Key**: ダウンロードした.p8ファイルの内容

6. **Spwigに資格情報を入力**
   - SpwigのOAuth設定に戻ります
   - Client ID、Team ID、Key IDを貼り付けます
   - .p8ファイルをテキストエディタで開き、その内容をコピーします
   - ヘッダーを含むすべてのキーをPrivate Keyフィールドに貼り付けます
   - **Save** をクリックします
   - **Enable Apple OAuth** を有効にするスイッチをオンにします

### テスト

- Apple IDを持つデバイスでストアフロントのログインページにアクセスします
- "Appleでログイン"をクリックします
- Apple IDで認証します
- 成功裏にログインするはずです

## Microsoft OAuthの設定

Microsoft OAuthは、Office 365またはAzure ADを使用するビジネス顧客を対象とするストアに最適です。

### 事前条件

- Microsoftアカウント
- Azureポータルへのアクセス

### 設定手順

1. **OAuth設定に移動**
   - **Settings > Store Settings > OAuth Providers** に移動
   - **Configure Microsoft** をクリック

2. **Azureでアプリケーションの登録**
   - [Azureポータル](https://portal.azure.com/) にアクセス
   - **Azure Active Directory > App registrations** に移動
   - **New registration** をクリックします
   - 名前を入力（例: "Store OAuth"）
   - **Accounts in any organizational directory and personal Microsoft accounts** を選択します
   - **Redirect URI** で **Web** を選択し、以下を入力：
     ```
     https://yourdomain.com/accounts/microsoft/login/callback/
     ```
   - **Register** をクリックします

3. **アプリケーションIDのコピー**
   - アプリの概要ページで、**Application (client) ID** をコピーします

4. **クライアントシークレットの作成**
   - 左のサイドバーで **Certificates & secrets** をクリックします
   - **New client secret** をクリックします
   - 説明を入力（例: "OAuth Secret"）
   - 有効期限を選択（推奨: 24か月）
   - **Add** をクリックします
   - **すぐにシークレット値をコピー** — 再度表示されません

5. **Spwigに資格情報を入力**
   - SpwigのOAuth設定に戻ります
   - Application (client) IDをClient IDとして貼り付けます
   - シークレット値をClient Secretとして貼り付けます
   - オプションでテナントIDを入力（単一テナントアプリ用；マルチテナントの場合は空白）
   - **Save** をクリックします
   - **Enable Microsoft OAuth** を有効にするスイッチをオンにします

### テスト

- ストアフロントのログインページにアクセスします
- "Microsoftでログイン"をクリックします
- Microsoftアカウントで認証します
- 成功裏にログインするはずです

## OAuth接続の管理

### 顧客視点

顧客はアカウントダッシュボードから接続されたOAuthプロバイダーを表示および管理できます：

- **My Account > Connected Accounts** に移動します
- どのプロバイダーが接続されているかを確認します（Google、Apple、Microsoft）
- **Disconnect** をクリックしてプロバイダーを切断します
- 再接続するには、そのプロバイダーで再度ログインします

### 複数のプロバイダー

1つの顧客アカウントは複数のOAuthプロバイダーに接続できます。例えば、顧客は同じアカウントにGoogleとAppleを接続できます。

顧客が同じメールアドレスを使用して別のOAuthプロバイダーでログインを試みると、Spwigは既存のアカウントに自動的に接続します。

### 管理者管理

管理者として、顧客のOAuth接続を確認できます：

- **Customers > Customers** に移動します
- 顧客レコードを開きます
- **Connected Accounts** セクションにスクロールします
- 接続されているプロバイダーと接続日時を確認します

顧客の代わりにプロバイダーを切断することはできません — セキュリティ上の理由から、顧客自身がそれを実行する必要があります。

## トラブルシューティング

### リダイレクトURIの不一致

**エラー**: "Redirect URI mismatch" または "Invalid redirect_uri"

**解決策**:
- プロバイダー設定内のリダイレクトURIがSpwig内のものと完全に一致していることを確認してください
- 末尾のスラッシュを確認してください — これらは一致する必要があります
- `https://`を使用していることを確認してください（`http://`ではない）
- ブラウザのキャッシュをクリアして再度試してください

### 無効な資格情報

**エラー**: "Invalid client ID" または "Authentication failed"

**解決策**:
- Client IDとClient Secretが正しくコピーされていることを再度確認してください
- 余分なスペースや改行がないか確認してください
- 資格情報が正しいプロジェクト/アプリから取得されていることを確認してください
- Appleの場合、Private Keyが.p8ファイルの完全な内容を含んでいることを確認してください

### プロバイダーAPIが有効になっていない

**エラー**: "API not enabled" または "Access not configured"

**解決策**:
- Googleの場合: Google CloudプロジェクトでGoogle+ APIを有効にしていることを確認してください
- Microsoftの場合: アプリ登録が承認され、アクティブになっていることを確認してください
- Appleの場合: Service IDで"Sign In with Apple"が有効になっていることを確認してください

### SSLが必要

**エラー**: "OAuth requires HTTPS" または "Insecure redirect URI"

**解決策**:
- OAuthプロバイダーはセキュリティのためにSSL/TLS（HTTPS）を必要とします
- ストアに有効なSSL証明書がインストールされていることを確認してください
- リダイレクトURIを`https://`ではなく`http://`を使用して更新してください
- ローカルでテストしている場合、ngrokなどのサービスを使用してHTTPSトンネルを作成してください

### ボタンが表示されない

**問題**: "Sign in with Google/Apple/Microsoft"ボタンがログインページに表示されません

**解決策**:
- OAuth設定でプロバイダーが有効になっていることを確認してください
- ブラウザのキャッシュをクリアし、ページを再読み込みしてください
- お使いのテーマがソーシャルログインテンプレートを含んでいることを確認してください
- ブラウザコンソールでJavaScriptエラーを確認してください

## Tips & Best Practices

### セキュリティ

- **定期的にシークレットを回転** — Client Secretsを12〜24か月ごとに更新してください
- **失敗したログイン試行を監視** — 異常な認証パターンを確認してください
- **環境ごとに別々の資格情報を使用** — ステージング環境と本番環境で異なる資格情報を使用してください
- **リダイレクトURIを制限** — 必要なURIのみを追加してください

### ユーザー体験

- **3つのプロバイダーすべてを有効に** — 顧客に選択肢を提供し、異なるデモグラフィックが異なるプロバイダーを好む場合があります
- **ボタンを顕著に配置** — ソーシャルログインボタンは、メール/パスワードフォームの上に配置してください
- **認識可能なブランドを使用** — Google/Apple/Microsoftの標準的なボタンスタイルを保持してください
- **モバイルでのテスト** — OAuthフローはモバイルブラウザで異なります

### 合規性

- **プライバシーポリシー** — OAuthプロバイダーを使用していることを開示し、取得するデータについて説明してください
- **利用規約** — プロバイダーの利用規約に準拠してください（Google、Apple、Microsoftそれぞれに要件があります）
- **データ最小化** — 実際に必要なプロフィール情報をのみ要求してください

### テストチェックリスト

本番環境に移行する前にテストしてください：

- [ ] デスクトップで各プロバイダーでログイン
- [ ] モバイルで各プロバイダーでログイン
- [ ] 初回ログイン（アカウント作成）
- [ ] 2回目以降のログイン（アカウント接続）
- [ ] 同じメールアドレスで異なるプロバイダーでログイン
- [ ] プロバイダーを切断し、再接続
- [ ] 非OAuthユーザーのパスワードリセットフローがまだ動作していることを確認

