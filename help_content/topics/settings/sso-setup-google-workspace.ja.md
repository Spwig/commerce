---
title: 'SSO設定: Google Workspace'
---

このガイドでは、SpwigをGoogle Workspaceに接続して管理者用のシングルサインオン（SSO）を設定する手順を説明します。設定が完了すると、スタッフはGoogle Workspaceアカウントを使用してSpwigの管理者パネルにログインできます。

**注意:** Googleは時折Cloud Consoleのインターフェースを更新する可能性があります。これらの手順は2026年初頭のインターフェースに基づいて作成されています。表示されている手順と異なっている場合は、Googleの公式ドキュメントの[OAuth 2.0の設定](https://support.google.com/cloud/answer/6158849)を参照してください。

## 事前条件

- Google Workspaceのサブスクリプション（Google Workspace Business、Enterprise、またはEducation）
- [Google Cloud Console](https://console.cloud.google.com)への管理者アクセス権
- あなたのSpwigストアURL（例: `https://your-store.com`）
- スタッフのメールアドレスは、Spwig内でのアカウントとGoogle Workspaceアカウントが一致している必要があります

## ステップ1: Google Cloudプロジェクトの作成または選択

1. [Google Cloud Console](https://console.cloud.google.com)にアクセスします
2. バーの上部にあるプロジェクトセレクターをクリックします
3. **新規プロジェクト**をクリックします（既存のプロジェクトを選択することも可能です）
4. プロジェクト名を入力します（例: `Spwig SSO`）
5. あなたの組織を選択します
6. **作成**をクリックします

## ステップ2: OAuth同意画面の設定

1. Cloud Consoleで **APIs & Services > OAuth同意画面** に移動します
2. ユーザータイプとして **Internal** を選択します — これにより、ログインはあなたのGoogle Workspace組織内のユーザーに限定されます
3. **作成**をクリックします
4. 必要なフィールドを入力します:

| フィールド | 値 |
|-------|-------|
| **アプリ名** | `Spwig Admin`（またはあなたのストア名） |
| **ユーザーサポートメール** | あなたの管理者メールアドレス |
| **認可されたドメイン** | `your-store.com`（あなたのストアのドメイン、`https://`は除く） |
| **開発者連絡メール** | あなたの管理者メールアドレス |

5. **保存して次へ**をクリックします
6. **スコープ**ページで **スコープの追加または削除** をクリックし、以下を追加します:
   - `openid`
   - `email`
   - `profile`
7. **保存して次へ**をクリックします
8. まとめを確認し、**ダッシュボードに戻る**をクリックします

## ステップ 3: OAuth 認証情報を作成する

1. **APIs & Services > Credentials** に移動します
2. **Create Credentials > OAuth client ID** をクリックします
3. クライアントを構成します:

| フィールド | 値 |
|-------|-------|
| **アプリケーションタイプ** | Web アプリケーション |
| **名前** | `Spwig SSO` |
| **認可されたリダイレクト URI** | `https://your-store.com/oidc/callback/` |

4. **作成** をクリックします
5. ダイアログに **クライアント ID** と **クライアントシークレット** が表示されます — 両方の値をコピーしてください。JSON として保存して安全に保管することもできます。

**重要:** リダイレクト URI は `https://your-store.com/oidc/callback/` と完全に一致する必要があります — 末尾のスラッシュと `https://` スキーマを含めて。`your-store.com` を実際のストアドメインに置き換えてください。

## ステップ 4: Discovery URL を取得する

Google はすべての Workspace テナントに対して単一の標準 Discovery URL を使用します:

```
https://accounts.google.com/.well-known/openid-configuration
```

この URL はすべての Google Workspace 組織で同じです — テナントやドメインでカスタマイズする必要はありません。

## ステップ 5: Spwig で構成する

1. Spwig 管理画面で **Enterprise SSO > SSO Provider Configuration** に移動します
2. **Provider Name** を `Google Workspace` に設定します
3. Discovery URL を入力: `https://accounts.google.com/.well-known/openid-configuration`
4. **Auto-Discover** をクリックします — これにより、すべてのエンドポイントフィールドが自動的に埋め込まれます
5. ステップ 3 から取得した **Client ID** を入力します
6. ステップ 3 から取得した **Client Secret** を入力します
7. **保存** をクリックします

### クレームマッピング

Google は標準の OIDC クレーム名を使用しているため、Spwig のデフォルト構成はすぐに使用できます:

| Spwig 設定 | Google クレーム | デフォルト値 |
|---------------|-------------|---------------|
| Email クレーム | `email` | `email` |
| 名前（ファーストネーム）クレーム | `given_name` | `given_name` |
| 姓（ラストネーム）クレーム | `family_name` | `family_name` |

クレームマッピングの変更は必要ありません。

## ステップ 6: 有効化およびテスト

1.

**Site Settings > Security** タブに移動します
2.

**Enable SSO for admin login** をチェックします
3.

**保存** をクリックします
4.


管理者ログインページを **プライベート/インコグニトウィンドウ** で開きます

| 問題 | 原因 | 解決策 |
|---------|-------|----------|
| **エラー 400: redirect_uri_mismatch** | Google Cloud でのリダイレクト URI が完全に一致していない | リダイレクト URI が `https://your-store.com/oidc/callback/` で、末尾のスラッシュが含まれていることを確認してください。HTTP と HTTPS を確認してください。 |
| **エラー 403: access_denied** | ユーザーが Google Workspace 組織に所属していない | "Internal" ユーザータイプを使用している場合、あなたの組織に所属するユーザーのみがサインインできます。ユーザーのアカウントが Workspace ドメインに所属していることを確認してください。 |
| **OAuth 承認画面に "このアプリは認証されていません" と表示される** | Internal アプリでは正常 | Internal アプリではこの警告が表示されるのは通常であり、機能に影響はありません。あなたの組織のユーザーはサインインできます。 |
| **Google でのログインは成功するが Spwig で失敗する** | Spwig に一致するユーザーがいない | Spwig に Google Workspace アカウントと同じメールアドレスを持つスタッフアカウントが存在することを確認してください。Restrict to Staff が正しく設定されているか確認してください。 |
| **"Access blocked: This app's request is invalid"** | スコープが正しく設定されていない | OAuth 承認画面に `openid`、`email`、`profile` スコープが追加されていることを確認してください。 |

## Tips

- **"Internal" ユーザータイプを使用する** — これにより、サインインはあなたの Google Workspace 組織に限定され、Google のアプリ認証プロセスは必要ありません。
- **Google クライアントシークレットは期限切れにならない** — Microsoft Entra ID と異なり、Google OAuth クライアントシークレットには有効期限がありません。ただし、Credentials ページからいつでもローテーションできます。
- **複数のアプリ用に1つのプロジェクトを使用する** — 複数の Spwig インストールがある場合、同じ Google Cloud プロジェクト内で複数の OAuth クライアント ID を作成できます。
- **非管理者アカウントでテストする** — Spwig でテスト用のスタッフアカウントを作成し、通常の Google Workspace ユーザー（スーパーアドミンでないユーザー）を使用して SSO が予期通りに動作することを確認してください。