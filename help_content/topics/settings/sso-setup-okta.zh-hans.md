---
title: SSO设置：Okta
---

本指南将引导您将Spwig连接到Okta，以实现管理员单点登录。配置完成后，您的员工可以使用其Okta账户登录Spwig管理面板。

**注意：** Okta可能会随时间更新其管理控制台界面。这些说明是基于2026年初的Okta管理控制台编写的。如果任何步骤与您看到的界面不同，请参考Okta的官方文档[创建OIDC应用集成](https://developer.okta.com/docs/guides/sign-into-web-app-redirect/main/)。

## 先决条件

- 一个Okta组织（任何层级——免费开发人员账户可用于测试）
- Okta中的**超级管理员**或**应用程序管理员**角色
- 您的Spwig商店URL（例如，`https://your-store.com`）
- 员工的电子邮件地址必须与他们的Okta账户匹配

## 第1步：创建应用程序

1. 登录到[Okta管理控制台](https://your-org-admin.okta.com)
2. 导航到 **Applications > Applications**
3. 点击 **Create App Integration**
4. 选择：

| 字段 | 值 |
|-------|-------|
| **登录方法** | OIDC - OpenID Connect |
| **应用程序类型** | Web Application |

5. 点击 **Next**

## 第2步：配置应用程序

填写应用程序设置：

| 字段 | 值 |
|-------|-------|
| **应用程序集成名称** | `Spwig Admin SSO`（或您喜欢的任何名称） |
| **授权类型** | 授权码（默认应已选中） |
| **登录重定向URI** | `https://your-store.com/oidc/callback/` |
| **注销重定向URI** | `https://your-store.com/en/admin/login/` |
| **受控访问** | 根据您的需求选择（见下文） |

对于 **受控访问**，选择以下之一：

- **允许组织中的所有人访问** — 所有Okta用户都可以登录（您仍然可以使用限制为员工的设置来控制Spwig的访问）
- **限制访问到选定的组** — 仅特定Okta组中的用户可以登录
- **暂时跳过组分配** — 您稍后将手动分配用户或组

点击 **保存**。

**重要：** 登录重定向 URI 必须完全匹配 `https://your-store.com/oidc/callback/` — 包括末尾的斜杠。

## 第 3 步：获取客户端凭证

保存后，应用程序的 **General** 选项卡会显示您的凭证：

| 值 | 查找位置 |
|-------|-----------------|
| **客户端 ID** | General 选项卡，客户端凭证部分 |
| **客户端密钥** | General 选项卡，客户端凭证部分（点击眼睛图标以显示） |

复制这两个值 — 您需要它们用于 Spwig。

## 第 4 步：构建发现 URL

发现 URL 依赖于您的 Okta 组织和授权服务器：

**默认授权服务器（最常见）：**
```
https://your-org.okta.com/.well-known/openid-configuration
```

**自定义授权服务器（如果已配置）：**
```
https://your-org.okta.com/oauth2/{authorization-server-id}/.well-known/openid-configuration
```

将 `your-org.okta.com` 替换为您的实际 Okta 域名。您可以在管理员控制台的 URL 栏中或在 **Settings > Account** 下找到您的 Okta 域名。

**提示：** 大多数组织使用 Org 授权服务器（默认）。只有在 Okta 管理员已特别设置自定义授权服务器时，才使用自定义授权服务器 URL。

## 第 5 步：分配用户或组

如果您在第 2 步中选择了“跳过组分配”，则需要在用户能够登录之前分配用户：

1. 在应用程序的 **Assignments** 选项卡中，点击 **Assign**
2. 选择 **Assign to People** 或 **Assign to Groups**
3. 选择用户或组，然后点击 **Assign**
4. 点击 **Done**

未分配给应用程序的用户在尝试 SSO 时会看到错误。

## 第 6 步：配置组声明（可选）

如果您希望 Spwig 根据 Okta 组成员身份自动设置工作人员或超级用户状态：

1.

在管理员控制台中导航到 **Security > API**
2.

选择您的 **Authorization Server**（如果没有创建自定义服务器，请使用 "default" 或 Org 授权服务器）
3.

转到 **Claims** 选项卡
4.



点击 **添加声明**
5.

配置声明：

| 字段 | 值 |
|-------|-------|
| **名称** | `groups` |
| **包含在令牌类型中** | ID Token, Always |
| **值类型** | Groups |
| **过滤器** | 匹配正则表达式：`.*`（用于包含所有组） |
| **包含在** | 任何作用域（或 `openid` 如果您希望限制） |

6. 点击 **创建**

**提示：** 与 Microsoft Entra ID 发送对象 ID 不同，Okta 默认发送 **组名称**。这使得角色映射更加直观 —— 您可以直接在 Spwig 的 Staff Groups 和 Superuser Groups 字段中使用 Okta 组的显示名称。

### 过滤组

如果您的用户属于许多 Okta 组，但您只想在令牌中包含特定的组：

- 将过滤器从 `.*` 更改为更具体的正则表达式，例如 `^Spwig.*` 以仅包含以 "Spwig" 开头的组
- 或使用 **以...开头**、**等于** 或 **包含** 过滤器，而不是正则表达式

## 第 7 步：在 Spwig 中进行配置

1. 在 Spwig 管理界面中，导航到 **Enterprise SSO > SSO Provider Configuration**
2. 将 **Provider Name** 设置为 `Okta`。
3. 输入第 4 步中的 Discovery URL。
4. 点击 **Auto-Discover** —— 这将自动填充所有端点字段。
5. 输入第 3 步中的 **Client ID**。
6. 输入第 3 步中的 **Client Secret**。
7. 如果您在第 6 步中配置了组声明：
   - 将 **Groups Claim** 设置为 `groups`。
   - 在 **Staff Groups** 中，输入应为工作人员的 Okta 组的名称（用逗号分隔）。
   - 在 **Superuser Groups** 中，输入应为超级用户的 Okta 组的名称（用逗号分隔）。
8. 点击 **保存**。

## 第 8 步：启用并测试

1.

导航到 **Site Settings > Security** 选项卡
2.

勾选 **Enable SSO for admin login**
3.

点击 **保存**
4.

在 **私人/无痕窗口** 中打开管理员登录页面
5.

您应该看到 **使用 Okta 登录** 按钮
6.

点击它 —— 您应该会被重定向到 Okta 的登录页面
7.

保留所有 markdown 格式、图片路径、代码块和技术术语。

使用分配到该应用且其电子邮件与Spwig中的员工用户匹配的Okta账户登录
8.

你应该会被重定向回Spwig管理仪表板

## 常见问题

| 问题 | 原因 | 解决方案 |
|---------|-------|----------|
| **重定向URI不允许** | 重定向URI与应用配置不匹配 | 验证登录重定向URI正好是 `https://your-store.com/oidc/callback/`，并包含末尾的斜杠 |
| **用户未分配到客户端应用** | 用户未分配到Okta应用 | 在分配选项卡中将用户或其组分配到应用 |
| **在Okta登录成功但在Spwig失败** | Spwig中没有匹配的用户 | 确保Spwig中存在与电子邮件相同的员工账户。检查限制为员工的设置。 |
| **组声明为空** | 授权服务器上未配置组声明 | 按照步骤6添加组声明。确保你将其添加到正确的授权服务器。 |
| **错误的授权服务器** | 发现URL使用了与配置组声明的授权服务器不同的服务器 | 验证发现URL与配置组声明的授权服务器匹配 |
| **"提供的client_id无效"** | client_id不匹配或应用未激活 | 检查client_id是否正确，并确保Okta中的应用状态为激活 |

## 提示

- **Okta发送的是组名称，而不是ID** —— 这使得角色映射变得简单。

在Spwig的员工组或超级用户组字段中输入确切的组显示名称（例如，`Spwig Admins`）。
- **使用组分配进行访问控制** —— 将特定的Okta组分配给Spwig应用，而不是允许所有用户。

# 配置 Okta SSO

通过这种方式，只有指定的员工才能登录。
- **Okta 客户端密钥默认不会过期** — 但为了遵循最佳安全实践，你可以随时从应用程序的 General 选项卡中轮换它们。
- **使用非管理员账户进行测试** — 使用一个普通 Okta 用户（而非超级管理员）分配给应用程序，以验证 SSO 是否按预期工作。
- **Okta 中的 MFA** — 配置 Okta 的全局会话策略或认证策略以要求 MFA。

这将适用于所有对 Spwig 的 SSO 登录，无需在 Spwig 中单独配置 MFA。