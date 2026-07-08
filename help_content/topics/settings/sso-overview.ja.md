---
title: 管理者用シングルサインオン（SSO）
---

シングルサインオン（SSO）は、スタッフがSpwigの管理者パネルにログインするために、組織のアイデンティティプロバイダーを使用して、個別のユーザー名とパスワードではなくログインできるようにします。Spwigは、OpenID Connect（OIDC）プロトコルを使用する任意のアイデンティティプロバイダーをサポートしており、Microsoft Entra ID、Google Workspace、Okta、Auth0、Keycloak、その他のプロバイダーも含みます。

| SSO Enabled | Password Login | Result |
|-------------|---------------|--------|
| Off | On | Standard login page with username/password form only |
| On | On | SSO button at the top, "or" divider, then password form below |
| On | Off | SSO button only. Password form is behind a "Sign in with local account" toggle |
| Off | Off | Not possible — password login is automatically re-enabled if SSO is disabled or not configured |

## User Matching

When a staff member signs in via SSO, Spwig matches them to an existing user account by **email address** (case-insensitive). The email from the identity provider's claims must match the email on the staff member's Spwig account.

If no matching user is found:

- **Auto-Create Users disabled** (default) — the login is denied. You must create the staff account in Spwig first with a matching email address.
- **Auto-Create Users enabled** — a new user account is created automatically with the name and email from the identity provider's claims.

The **Restrict to Staff** setting (enabled by default) adds an additional check: even if a user account exists, the login is denied unless the user has staff status. This prevents non-staff accounts from accessing the admin panel via SSO.

## Role Mapping

If your identity provider sends group membership information in the OIDC claims, Spwig can automatically set staff and superuser status based on group membership.

To configure role mapping:

1. In the SSO Provider Configuration, set the **Groups Claim** field to the claim name your provider uses (default: `groups`)
2. In **Staff Groups**, enter comma-separated group names or IDs. Users in any of these groups are granted staff status.
3. In **Superuser Groups**, enter comma-separated group names or IDs. Users in any of these groups are granted superuser status.

Role mapping is evaluated each time a user signs in via SSO. If a user is removed from a group in the identity provider, their staff or superuser status is updated on their next SSO login.

**Important:** Microsoft Entra ID sends group **Object IDs** (UUIDs) by default, not group names. Copy the Object ID from the Azure portal when configuring role mapping. Other providers like Okta typically send group names.

## Claims Mapping

Spwig reads user information from standard OIDC claims. The defaults work with most providers, but you can customize the claim field names in the SSO Provider Configuration:

| Setting | Default | Description |
|---------|---------|-------------|
| **Email Claim** | `email` | The claim containing the user's email address |
| **First Name Claim** | `given_name` | The claim containing the user's first name |
| **Last Name Claim** | `family_name` | The claim containing the user's last name |
| **Groups Claim** | `groups` | The claim containing group memberships (leave blank to disable role mapping) |

## MFA Behavior

When a staff member signs in via SSO, Spwig's built-in two-factor authentication (2FA) requirement is automatically bypassed. This is because the identity provider is responsible for enforcing MFA as part of the SSO login flow.

If your organization requires MFA, configure it in your identity provider's conditional access policies rather than in Spwig's 2FA settings. This gives you centralized MFA management across all your applications.

## Recovery Access

If your identity provider experiences an outage or misconfiguration, you can still access the admin login form:

- **Click the toggle** — If password login is disabled, click "Sign in with local account" on the login page to reveal the password form
- **URL parameter** — Append `?password=1` to the admin login URL (e.g., `https://your-store.com/en/admin/login/?password=1`) to show the password form directly
- **Password login is always available** — Even when hidden from the UI, the password authentication backend remains active. Only the visibility of the form is affected.

Spwig は、SSO が有効かつ正しく構成されている限り、パスワードログインを無効にすることを防ぎます — たった一度のミスで自分自身をロックアウトしてしまうことはありません。

## サポートされているプロバイダ

Spwig は、OpenID Connect (OIDC) プロトコルをサポートする任意のアイデンティティプロバイダと連携して動作します。詳細な設定ガイドは以下が利用可能です:

- **Microsoft Entra ID** (旧 Azure Active Directory)
- **Google Workspace** (Google Cloud Identity)
- **Okta**

他の OIDC 準拠プロバイダ (Auth0, Keycloak, OneLogin, Ping Identity, JumpCloud など) についても、Spwig の設定手順は同じです — プロバイダの OIDC ディスカバリURL、クライアントID、クライアントシークレットが必要です。これらの資格情報を取得するために、プロバイダのドキュメントを参照してください。使用するリダイレクトURIは常に `https://your-store.com/oidc/callback/` です。

## ヒント

- **パスワードログインを最初に有効にしておく** — パスワードログインとSSOを同時に有効にします。チーム内でSSOが正常に動作することを確認した後、パスワードログインをオプションで無効にできます。
- **インコグニトウィンドウでテストする** — 現在の管理者セッションに影響を与えることなく、SSOをテストするためにプライベート/インコグニトブラウザウィンドウを使用してください。
- **スタッフアカウントを最初に作成する** — Auto-Create Users を有効にしていない限り、スタッフメンバーはSSOを通じてログインする前に、既存のSpwigアカウントと一致するメールアドレスを持つ必要があります。
- **Auto-Discover ボタンを使用する** — プロバイダの OIDC ディスカバリURLを入力し、Auto-Discover をクリックしてすべてのエンドポイントフィールドを自動的に埋めます。これにより、エンドポイントを手動で入力するよりもはやく、エラーが少なくなります。
- **ローカル管理者アカウントを保持する** — 身分プロバイダの問題が発生した場合の復旧オプションとして、常に少なくとも1つのパスワード付きローカル管理者アカウントを保持してください。
- **クライアントシークレットの期限切れを監視する** — 一部のプロバイダ (特に Microsoft Entra ID) は、クライアントシークレットに期限を設定します。シークレットが期限切れになる前にローテーションするように、カレンダーリマインダーを設定してください。