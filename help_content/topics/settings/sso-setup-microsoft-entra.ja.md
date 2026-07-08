---
title: 'SSO設定: Microsoft Entra ID'
---

このガイドでは、SpwigをMicrosoft Entra ID（旧Azure Active Directory）に接続して、管理者用のシングルサインオン（SSO）を設定する手順を説明します。設定が完了すると、スタッフはMicrosoftのワークアカウントを使用してSpwigの管理者パネルにログインできます。

**注意:** Microsoftは時折Entra管理センターのインターフェースを更新する可能性があります。これらの手順は、2026年初頭のインターフェースに基づいて作成されています。表示されている手順と異なっている場合は、Microsoftの公式ドキュメントにある[Microsoft IDプラットフォームでアプリケーションを登録する](https://learn.microsoft.com/en-us/entra/identity-platform/quickstart-register-app)に関する情報を参照してください。

## 事前条件

- Microsoft Entra IDへのアクセスがあるAzureサブスクリプション
- Entra IDテナント内での**アプリケーション管理者**または**グローバル管理者**ロール
- SpwigストアURL（例: `https://your-store.com`）
- スタッフのメールアドレスは、Spwig内での登録がMicrosoftアカウントと一致している必要があります

## ステップ1: アプリケーションを登録する

1. [Microsoft Entra管理センター](https://entra.microsoft.com)にログインします
2. **Identity > Applications > App registrations** に移動します
3. **New registration** をクリックします
4. 登録を設定します:

| Field | Value |
|-------|-------|
| **Name** | `Spwig Admin SSO`（またはご希望の名前） |
| **Supported account types** | **Accounts in this organizational directory only**（単一テナント） |
| **Redirect URI** | Platform: **Web**, URI: `https://your-store.com/oidc/callback/` |

5. **Register** をクリックします

**重要:** リダイレクトURIは`https://your-store.com/oidc/callback/`と完全に一致する必要があります — 末尾のスラッシュも含めて。`your-store.com`を実際のストアドメインに置き換えてください。

## ステップ2: アプリケーションIDをメモする

登録後、アプリケーションの**Overview**ページが表示されます。これらの2つの値をメモしておいてください — あとで必要になります:

| 値 | 見つける場所 | 用途 |
|-------|-----------------|---------------|
| **アプリケーション (クライアント) ID** | 概要ページ、上部セクション | Spwig で **Client ID** として入力 |
| **ディレクトリ (テナント) ID** | 概要ページ、上部セクション | Discovery URL を構築するために使用 |

## ステップ 3: クライアントシークレットの作成

1. アプリ登録で **証明書とシークレット** に移動
2. **新しいクライアントシークレット** をクリック
3. 説明を入力 (例: `Spwig SSO`) し、有効期限を選択
4. **追加** をクリック
5. **値をすぐにコピー** してください — これは一度だけ表示されます。これは Spwig に入力するクライアントシークレットです。

**Secret ID をコピーしないでください** — **値** の列が必要で、**ID** の列ではありません。

**有効期限が切れる前にシークレットを再発行する** ことを覚えておいてください。シークレットが有効期限切れになると、SSO は新しいシークレットを作成し、Spwig で更新するまで動作しなくなります。

## ステップ 4: API パーミッションの設定

1. **API パーミッション** に移動
2. **Microsoft Graph > User.Read** (委任) が一覧されていることを確認してください。これはデフォルトで追加されます。
3. `openid`、`email`、および `profile` のパーミッションが一覧されていない場合は、**Add a permission > Microsoft Graph > Delegated permissions** をクリックし、それらを追加してください。
4. プロンプトが表示された場合は **Grant admin consent for [your organization]** をクリックしてください。

## ステップ 5: Discovery URL の作成

OIDC Discovery URL は次の形式に従います:

```
https://login.microsoftonline.com/{tenant-id}/v2.0/.well-known/openid-configuration
```

`{tenant-id}` をステップ 2 で得た **Directory (tenant) ID** に置き換えてください。

例: テナント ID が `a1b2c3d4-e5f6-7890-abcd-ef1234567890` の場合、Discovery URL は次のようになります:

```
https://login.microsoftonline.com/a1b2c3d4-e5f6-7890-abcd-ef1234567890/v2.0/.well-known/openid-configuration
```

## ステップ 6: グループクレームの設定 (オプション)

Spwig が Entra ID グループメンバーシップに基づいてスタッフまたはスーパーユーザーのステータスを自動的に割り当てたい場合:

1.

アプリ登録で **Token configuration** に移動
2.

**Add groups claim** をクリック
3.

すべてのマークダウンフォーマット、画像パス、コードブロック、および技術用語を保持してください。

# ステップ 3: グループタイプの選択

含めるグループタイプを選択する（通常は **セキュリティグループ**）
4.

**カスタムトークンプロパティのタイプごとに**、**ID** トークンに対して **Group ID** を選択します
5.

**追加** をクリックします

**重要:** Entra ID はグループの **Object ID**（`a1b2c3d4-...` のような UUID）を送信し、グループの表示名ではありません。Spwig でロールマッピングを構成する際には、これらの Object ID を使用する必要があります。

グループの Object ID を見つけるには:
1. Entra 管理センターで **Identity > Groups > All groups** に移動します
2. グループをクリックします
3. グループの概要ページから **Object ID** をコピーします

### グループの上限

Microsoft Entra ID はトークンに最大 **200 グループ** を含めます。ユーザーが 200 グループ以上に所属している場合、グループのクレームは Microsoft Graph API へのリンクに置き換えられます。多くのグループを持つ組織では、Spwig アクセス用の専用セキュリティグループを作成し、[グループフィルタリング](https://learn.microsoft.com/en-us/entra/identity-platform/optional-claims-reference)を使用して、含まれるグループを制限することを検討してください。

## ステップ 7: Spwig での構成

1. Spwig 管理画面で **Enterprise SSO > SSO プロバイダ構成** に移動します
2. **プロバイダ名** を `Microsoft Entra ID` に設定します
3. ステップ 5 で取得した Discovery URL を **OIDC Discovery URL** に貼り付けます
4. **Auto-Discover** をクリックします — これにより、すべてのエンドポイントフィールドが自動的に埋め込まれます
5. ステップ 2 で取得した **Client ID** を入力します
6. ステップ 3 で取得した **Client Secret**（値）を入力します
7. ステップ 6 でグループクレームを構成した場合:
   - **Groups Claim** を `groups` に設定します
   - **Staff Groups** に、スタッフとして指定するグループの Object ID をカンマ区切りで入力します
   - **Superuser Groups** に、スーパーユーザーとして指定するグループの Object ID をカンマ区切りで入力します
8. **保存** をクリックします

## ステップ 8: 有効化とテスト

1.

**サイト設定 > Security** タブに移動します
2.

**管理者ログイン用の SSO を有効にする** をチェックします
3.

**保存** をクリックします
4.

**プライベート/インコグニトウィンドウ** で管理者ログインページを開きます
5.

**Microsoft Entra ID でサインイン** ボタンが表示されるはずです
6.


# 4. Microsoftアカウントでサインイン

クリックしてください — Microsoftのログインページにリダイレクトされるはずです
7.

Spwigのスタッフユーザーとメールアドレスが一致するMicrosoftアカウントでサインインしてください
8.

Spwigの管理ダッシュボードに戻るはずです

## 一般的な問題

| 問題 | 原因 | 解決策 |
|---------|-------|----------|
| **AADSTS50011: リダイレクトURIが一致しません** | EntraのリダイレクトURIが完全に一致していません | リダイレクトURIが`https://your-store.com/oidc/callback/`で、末尾のスラッシュが含まれていることを確認してください。HTTPとHTTPSの不一致を確認してください。 |
| **AADSTS700016: アプリケーションが見つかりません** | 間違ったクライアントIDまたはテナント | クライアントIDを再確認し、Discovery URLが正しいテナントIDを使用しているか確認してください |
| Microsoftでのログインは成功するがSpwigで失敗する | Spwigに一致するユーザーがいない | SpwigにMicrosoftアカウントと同じメールアドレスを持つスタッフアカウントが存在することを確認してください。Restrict to Staffが有効な場合は、ユーザーがスタッフステータスを持っていることを確認してください。 |
| Groups claimが空 | グループクレームが設定されていない | ステップ6に従って、トークン構成にgroups claimを追加してください |
| Groups claimがURLではなくIDを返す | ユーザーが200以上のグループに所属している | トークン内のグループを制限するグループフィルタリングを使用するか、特定のグループを割り当ててください |
| SSOが数か月後に動作しなくなる | クライアントシークレットが期限切れ | Entraで新しいクライアントシークレットを作成し、SpwigのSSOプロバイダ構成で更新してください |

## ヒント

- **セキュリティグループ**を使用してロールマッピングを行い、Microsoft 365グループや配布リストではなく。

セキュリティグループはアクセス制御のために設計されており、OIDCクレームと最も信頼性高く動作します。
- **単一テナントが推奨されます** — 「この組織のディレクトリ内のアカウントのみ」を選択すると、SSOを組織のユーザーに限定します。


# 多租户構成
多租户構成は追加の検証が必要です。
- **長いシークレットの有効期限を設定する** — クライアントシークレットを作成する際、24か月を選択し、22か月後にローテーションするカレンダーリマインダーを設定してください。
- **条件付きアクセス** — Entra IDでSpwigアプリ登録に適用する条件付きアクセスポリシーを作成できます。

例えば、MFAを必須とし、信頼できない場所からのサインインをブロックするか、準拠したデバイスを必須とすることができます。
- **非管理者アカウントでテストする** — Spwigでテスト用のスタッフアカウントを作成し、全チームに展開する前にSSOが正常に動作することを確認してください。