---
title: SSO设置：Google Workspace
---

本指南将引导您将Spwig连接到Google Workspace，以实现管理员单点登录。配置完成后，您的员工可以使用其Google Workspace账户登录Spwig管理面板。

**注意：** Google可能会随时间更新Cloud Console界面。这些说明是基于2026年初的界面编写的。如果任何步骤与您看到的界面不同，请参考Google官方文档中的[设置OAuth 2.0](https://support.google.com/cloud/answer/6158849)。

## 先决条件

- Google Workspace订阅（Google Workspace Business、Enterprise或Education）
- 对[Google Cloud Console](https://console.cloud.google.com)的管理员访问权限
- 您的Spwig商店URL（例如，`https://your-store.com`）
- 员工的电子邮件地址必须与他们的Google Workspace账户匹配

## 第1步：创建或选择一个Google Cloud项目

1. 访问[Google Cloud Console](https://console.cloud.google.com)
2. 点击顶部栏中的项目选择器
3. 点击**新建项目**（或选择现有项目，如果您更喜欢的话）
4. 输入项目名称（例如，`Spwig SSO`）
5. 选择您的组织
6. 点击**创建**

## 第2步：配置OAuth同意屏幕

1. 在Cloud Console中，导航到**API和服务 > OAuth同意屏幕**
2. 选择**内部**作为用户类型——这将限制登录仅限于您的Google Workspace组织内的用户
3. 点击**创建**
4. 填写所需的字段：

| 字段 | 值 |
|-------|-------|
| **应用名称** | `Spwig Admin`（或您的商店名称） |
| **用户支持电子邮件** | 您的管理员电子邮件地址 |
| **授权域名** | `your-store.com`（您的商店域名，不带`https://`） |
| **开发人员联系电子邮件** | 您的管理员电子邮件地址 |

5. 点击**保存并继续**
6. 在**范围**页面上，点击**添加或删除范围**，并添加以下内容：
   - `openid`
   - `email`
   - `profile`
7. 点击**保存并继续**
8. 查看摘要，然后点击**返回仪表板**

## 第 3 步：创建 OAuth 凭据

1. 导航到 **APIs & Services > Credentials**
2. 点击 **Create Credentials > OAuth client ID**
3. 配置客户端：

| 字段 | 值 |
|-------|-------|
| **应用类型** | Web 应用 |
| **名称** | `Spwig SSO` |
| **授权重定向 URI** | `https://your-store.com/oidc/callback/` |

4. 点击 **创建**
5. 弹出对话框显示您的 **客户端 ID** 和 **客户端密钥** — 请复制这两个值。您也可以将它们下载为 JSON 以进行安全存储。

**重要：** 重定向 URI 必须完全匹配 `https://your-store.com/oidc/callback/` — 包括末尾的斜杠和 `https://` 协议。请将 `your-store.com` 替换为您的实际商店域名。

## 第 4 步：获取发现 URL

Google 为所有 Workspace 租户使用一个标准的发现 URL：

```
https://accounts.google.com/.well-known/openid-configuration
```

此 URL 对每个 Google Workspace 组织都是一样的 — 您不需要用租户或域名对其进行自定义。

## 第 5 步：在 Spwig 中进行配置

1. 在 Spwig 管理界面中，导航到 **Enterprise SSO > SSO Provider Configuration**
2. 将 **Provider Name** 设置为 `Google Workspace`。
3. 输入发现 URL：`https://accounts.google.com/.well-known/openid-configuration`。
4. 点击 **Auto-Discover** — 这会自动填充所有端点字段。
5. 输入第 3 步中的 **Client ID**。
6. 输入第 3 步中的 **Client Secret**。
7. 点击 **保存**。

### 声明映射

Google 使用标准的 OIDC 声明名称，因此默认的 Spwig 配置可以直接使用：

| Spwig 设置 | Google 声明 | 默认值 |
|---------------|-------------|---------------|
| 电子邮件声明 | `email` | `email` |
| 名字声明 | `given_name` | `given_name` |
| 姓氏声明 | `family_name` | `family_name` |

不需要对声明映射进行任何更改。

## 第 6 步：启用并测试

1.

导航到 **Site Settings > Security** 选项卡
2.

勾选 **启用 SSO 用于管理员登录**
3.

点击 **保存**
4.


在 **隐私/无痕模式** 窗口中打开管理员登录页面
5.

你应该会看到一个 **使用 Google Workspace 登录** 按钮
6.

点击它 —— 你应该会被重定向到 Google 的登录页面
7.

使用一个电子邮件地址与 Spwig 中员工用户匹配的 Google Workspace 账户进行登录
8.

你应该会被重定向回 Spwig 管理面板

## 基于组的角色映射

与 Microsoft Entra ID 或 Okta 不同，Google 默认情况下不会在标准 OIDC 令牌中包含组成员资格。要在 Google 中实现组声明，需要使用 Google Workspace 目录 API 并进行超出基本 OIDC 的额外配置。

对于大多数 Google Workspace 部署，我们建议直接在 Spwig 中管理员工和超级用户状态，而不是通过自动角色映射：

1. 在 Spwig 中创建具有适当权限的员工账户
2. 使用 Spwig 的员工角色系统来控制访问级别
3. 员工通过 SSO 登录，Spwig 会使用他们现有的权限

如果你需要基于组的自动角色映射，请参考 [Google Workspace 管理员 SDK 目录 API 文档](https://developers.google.com/admin-sdk/directory) 来配置自定义声明。

## 常见问题

| 问题 | 原因 | 解决方案 |
|---------|-------|----------|
| **错误 400: redirect_uri_mismatch** | Google Cloud 中的重定向 URI 不完全匹配 | 验证重定向 URI 是 `https://your-store.com/oidc/callback/`，并带有结尾斜杠。检查 HTTP 和 HTTPS 的区别。 |
| **错误 403: access_denied** | 用户不在 Google Workspace 组织中 | 使用 "Internal" 用户类型时，只有您组织中的用户才能登录。验证用户的账户是否属于您的 Workspace 域。 |
| **OAuth 许可屏幕显示 "此应用未经过验证"** | 对于 Internal 应用是正常的 | 此警告对于 Internal 应用是预期的，不会影响功能。您组织中的用户仍然可以登录。 |
| **在 Google 登录成功但在 Spwig 登录失败** | Spwig 中没有匹配的用户 | 确保 Spwig 中存在一个与 Google Workspace 账户具有相同电子邮件的工作人员账户。检查是否已正确配置 "仅限工作人员"。 |
| **"访问被阻止：此应用的请求无效"** | 范围未正确配置 | 验证是否已将 `openid`、`email` 和 `profile` 范围添加到 OAuth 许可屏幕中。 |

## 提示

- **使用 "Internal" 用户类型** — 这会将登录限制为您的 Google Workspace 组织，并且不需要 Google 的应用验证流程。
- **Google 客户端密钥不会过期** — 与 Microsoft Entra ID 不同，Google OAuth 客户端密钥没有过期日期。不过，您可以随时从凭据页面轮换它们。
- **一个项目用于多个应用** — 如果您有多个 Spwig 安装，可以在同一个 Google Cloud 项目中创建多个 OAuth 客户端 ID。
- **使用非管理员账户进行测试** — 在 Spwig 中创建一个测试工作人员账户，并使用一个常规的 Google Workspace 用户（非超级管理员）来验证 SSO 是否按预期工作。