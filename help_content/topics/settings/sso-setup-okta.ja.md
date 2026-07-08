---
title: 'SSO設定: Okta'
---

このガイドでは、SpwigをOktaに接続して管理者用のシングルサインオン（SSO）を設定する手順を説明します。設定が完了すると、スタッフはOktaアカウントを使用してSpwigの管理者パネルにサインインできます。

**注意:** Oktaは時折管理コンソールのインターフェースを更新している可能性があります。これらの手順は、2026年初頭時点のOkta管理コンソールに基づいて作成されています。表示されている手順と異なっている場合は、Oktaの公式ドキュメントの[OIDCアプリ統合の作成](https://developer.okta.com/docs/guides/sign-into-web-app-redirect/main/)を参照してください。

## 事前条件

- Okta組織（どのレベルでも可 — テスト用には無料の開発者アカウントが使用可能です）
- Oktaにおける**Super Administrator**または**Application Administrator**のロール
- あなたのSpwigストアURL（例: `https://your-store.com`）
- スタッフメンバーのSpwig内でのメールアドレスが、Oktaアカウントと一致している必要があります

## ステップ1: アプリケーションの作成

1. [Okta管理コンソール](https://your-org-admin.okta.com)にサインインします
2. **Applications > Applications** に移動します
3. **Create App Integration** をクリックします
4. 以下のオプションを選択します:

| Field | Value |
|-------|-------|
| **Sign-in method** | OIDC - OpenID Connect |
| **Application type** | Web Application |

5. **Next** をクリックします

## ステップ2: アプリケーションの設定

アプリケーション設定を入力します:

| Field | Value |
|-------|-------|
| **App integration name** | `Spwig Admin SSO`（またはご希望の名前） |
| **Grant type** | Authorization Code（デフォルトで選択されているはずです） |
| **Sign-in redirect URIs** | `https://your-store.com/oidc/callback/` |
| **Sign-out redirect URIs** | `https://your-store.com/en/admin/login/` |
| **Controlled access** | ご要望に応じて選択してください（下記を参照） |

**Controlled access** では、以下のいずれかを選択してください:

- **Allow everyone in your organization to access** — Oktaのすべてのユーザーがサインインできます（SpwigへのアクセスはRestrict to Staff設定で制御可能です）
- **Limit access to selected groups** — 特定のOktaグループに所属するユーザーのみがサインインできます
- **Skip group assignment for now** — 後で手動でユーザーまたはグループを割り当てます

保存をクリックしてください。

**重要:** サインインリダイレクトURIは`https://your-store.com/oidc/callback/`と完全に一致する必要があります — 末尾のスラッシュも含めてください。

## ステップ3: クライアント資格情報を取得する

保存した後、アプリケーションの**General**タブに資格情報が表示されます:

| Value | Where to Find It |
|-------|-----------------|
| **Client ID** | Generalタブ、Client Credentialsセクション |
| **Client Secret** | Generalタブ、Client Credentialsセクション（アイコンをクリックして表示） |

両方の値をコピーしてください — Spwigで必要になります。

## ステップ4: Discovery URLを構築する

Discovery URLは、あなたのOkta組織と認証サーバーに依存します:

**デフォルトの認証サーバー（最も一般的な場合）:**
```
https://your-org.okta.com/.well-known/openid-configuration
```

**カスタム認証サーバー（設定されている場合）:**
```
https://your-org.okta.com/oauth2/{authorization-server-id}/.well-known/openid-configuration
```

`your-org.okta.com`を実際のOktaドメインに置き換えてください。Oktaドメインは、管理者コンソールのURLバーまたは**Settings > Account**で確認できます。

**ヒント:** 多くの組織はOrg Authorization Server（デフォルト）を使用しています。カスタム認証サーバーURLを使用する必要があるのは、Okta管理者が特別に設定している場合だけです。

## ステップ5: ユーザーまたはグループを割り当てる

ステップ2で「Skip group assignment（グループ割り当てをスキップ）」を選択した場合、ユーザーがサインインできるようになるまでユーザーを割り当てなければなりません:

1. アプリケーションの**Assignments**タブで**Assign**をクリックします
2. **Assign to People**または**Assign to Groups**を選択します
3. ユーザーまたはグループを選択し、**Assign**をクリックします
4. **Done**をクリックします

アプリケーションに割り当てられていないユーザーは、SSOを試みるとエラーを表示します。

## ステップ6: グループクレームを構成する（オプション）

SpwigがOktaグループメンバーシップに基づいてスタッフまたはスーパーユーザーのステータスを自動的に設定したい場合:

1.

管理者コンソールで**Security > API**に移動します
2.

**Authorization Server**を選択します（カスタムサーバーを作成していない場合は「default」、またはOrg Authorization Serverを使用してください）
3.

**Claims**タブに移動します
4.



クリックして **Add Claim** を選択
5.

クレームを構成します:

| フィールド | 値 |
|-------|-------|
| **名前** | `groups` |
| **トークンタイプに含める** | ID Token, Always |
| **値の種類** | Groups |
| **フィルター** | Matches regex: `.*` (すべてのグループを含めるため) |
| **含める場所** | Any scope (または `openid` で制限したい場合) |

6. クリックして **Create** を選択

**ヒント:** Microsoft Entra ID は Object ID を送信する一方で、Okta はデフォルトで **グループ名** を送信します。これにより、ロールマッピングがより直感的になります — Okta グループの表示名を Spwig の Staff Groups および Superuser Groups フィールドに直接使用できます。

### グループのフィルタリング

ユーザーが多くの Okta グループに所属しており、トークンに含まれるグループを特定のものだけにしたい場合:

- `.*` からより具体的な正規表現に変更し、たとえば `^Spwig.*` に変更して、"Spwig" で始まるグループのみを含める
- または正規表現の代わりに **Starts with**、**Equals**、または **Contains** フィルタを使用します

## ステップ 7: Spwig で構成

1. Spwig 管理画面で、**Enterprise SSO > SSO Provider Configuration** に移動
2. **Provider Name** を `Okta` に設定
3. ステップ 4 で取得した Discovery URL を入力
4. **Auto-Discover** をクリック — これにより、すべてのエンドポイントフィールドが自動的に埋め込まれます
5. ステップ 3 で取得した **Client ID** を入力
6. ステップ 3 で取得した **Client Secret** を入力
7. ステップ 6 でグループクレームを構成した場合:
   - **Groups Claim** を `groups` に設定
   - **Staff Groups** に、スタッフとして指定したい Okta グループの名前を入力 (カンマで区切る)
   - **Superuser Groups** に、スーパーユーザーとして指定したい Okta グループの名前を入力 (カンマで区切る)
8. **Save** をクリック

## ステップ 8: 有効化およびテスト

1.

**Site Settings > Security** タブに移動
2.

**Enable SSO for admin login** をチェック
3.

**Save** をクリック
4.

**プライベート/インコグニトウィンドウ** で管理ログインページを開く
5.

**Sign in with Okta** ボタンが表示されるはずです
6.

クリックしてください — Okta のログインページにリダイレクトされるはずです
7.



Oktaのアカウントでサインインしてください。そのアカウントはアプリケーションに割り当てられており、Spwigのスタッフユーザーのメールアドレスと一致している必要があります

# SSO 設定のベストプラクティス

このようにすることで、意図したスタッフのみがサインインできます。
- **Okta クライアントシークレットはデフォルトで期限切れにならない** — ただし、セキュリティのベストプラクティスとして、アプリケーションの「一般」タブからいつでもローテーションできます。
- **非管理者アカウントでテストする** — アプリケーションに割り当てられた通常の Okta ユーザー（スーパーアドミンではない）を使用して、SSO が予期通りに動作することを確認してください。
- **Okta 内のMFA** — Okta のグローバルセッションポリシーや認証ポリシーを構成して、MFA を必須とします。

これにより、Spwig へのすべての SSO ログインに MFA を個別に Spwig 内で構成する必要なく、適用されます。