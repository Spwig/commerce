---
title: SSO设置：Microsoft Entra ID
---

本指南将引导您将Spwig连接到Microsoft Entra ID（原Azure Active Directory），以实现管理员单点登录。配置完成后，您的员工可以使用其Microsoft工作账户登录Spwig管理员面板。

**注意：** Microsoft可能会随时间更新Entra管理中心的界面。这些说明是基于2026年初的界面编写的。如果任何步骤与您看到的界面不同，请参考Microsoft官方文档中的[在Microsoft身份平台注册应用程序](https://learn.microsoft.com/en-us/entra/identity-platform/quickstart-register-app)。

## 先决条件

- 一个具有Microsoft Entra ID访问权限的Azure订阅
- 在您的Entra ID租户中具有**应用程序管理员**或**全局管理员**角色
- 您的Spwig商店URL（例如，`https://your-store.com`）
- 员工的电子邮件地址在Spwig中必须与其Microsoft账户匹配

## 第1步：注册应用程序

1. 登录到[Microsoft Entra管理中心](https://entra.microsoft.com)
2. 导航到 **Identity > Applications > App registrations**
3. 点击 **New registration**
4. 配置注册：

| 字段 | 值 |
|-------|-------|
| **名称** | `Spwig Admin SSO`（或您喜欢的任何名称） |
| **支持的账户类型** | **仅此组织目录中的账户**（单租户） |
| **重定向URI** | 平台：**Web**，URI：`https://your-store.com/oidc/callback/` |

5. 点击 **Register**

**重要：** 重定向URI必须完全匹配`https://your-store.com/oidc/callback/`——包括末尾的斜杠。将`your-store.com`替换为您的实际商店域名。

## 第2步：记录应用程序ID

注册后，您将看到应用程序的**概述**页面。记录这两个值——您稍后需要它们：

| 值 | 查找位置 | 用途 |
|-------|-----------------|---------------|
| **应用程序（客户端）ID** | 概览页面，顶部部分 | 在 Spwig 中输入为 **Client ID** |
| **目录（租户）ID** | 概览页面，顶部部分 | 用于构建发现 URL |

## 第 3 步：创建客户端密钥

1. 在应用程序注册中，导航到 **证书与密钥**
2. 点击 **新建客户端密钥**
3. 输入描述（例如，`Spwig SSO`）并选择过期时间
4. 点击 **添加**
5. **立即复制值** — 它只会显示一次。这是您将在 Spwig 中输入的客户端密钥。

**不要复制密钥 ID** — 您需要的是 **值** 列，而不是 ID 列。

**设置提醒**，在密钥过期前进行轮换。当密钥过期后，SSO 将停止工作，直到您创建新的密钥并在 Spwig 中更新它。

## 第 4 步：配置 API 权限

1. 导航到 **API 权限**
2. 确认 **Microsoft Graph > User.Read**（委托）已列出。这是默认添加的。
3. 如果未列出 `openid`、`email` 和 `profile` 权限，请点击 **添加权限 > Microsoft Graph > 委托权限** 并添加它们。
4. 如果有提示，请点击 **为 [您的组织] 授予管理员同意**。

## 第 5 步：构建发现 URL

OIDC 发现 URL 的格式如下：

```
https://login.microsoftonline.com/{tenant-id}/v2.0/.well-known/openid-configuration
```

将 `{tenant-id}` 替换为第 2 步中的 **目录（租户）ID**。

示例：如果您的租户 ID 是 `a1b2c3d4-e5f6-7890-abcd-ef1234567890`，则发现 URL 为：

```
https://login.microsoftonline.com/a1b2c3d4-e5f6-7890-abcd-ef1234567890/v2.0/.well-known/openid-configuration
```

## 第 6 步：配置组声明（可选）

如果您希望 Spwig 根据 Entra ID 组成员身份自动分配员工或超级用户状态：

1.

在应用程序注册中，导航到 **令牌配置**
2.

点击 **添加组声明**
3.



# 选择要包含的组类型（通常为 **安全组**）
4.

在 **按类型自定义令牌属性** 下，对于 **ID** 令牌，选择 **组 ID**
5.

点击 **添加**

**重要：** Entra ID 发送的是组 **对象 ID**（如 `a1b2c3d4-...` 的 UUID），而不是组显示名称。在 Spwig 中配置角色映射时，必须使用这些对象 ID。

要查找组的 Object ID：
1. 在 Entra 管理中心，转到 **身份 > 组 > 所有组**
2. 点击该组
3. 从组的概述页面复制 **Object ID**

### 组限制
Microsoft Entra ID 在令牌中最多包含 **200 个组**。如果用户属于超过 200 个组，组声明将被替换为指向 Microsoft Graph API 的链接。对于组数量较多的组织，建议创建一个专门用于 Spwig 访问的安全组，并使用 [组筛选](https://learn.microsoft.com/en-us/entra/identity-platform/optional-claims-reference) 来限制包含哪些组。

## 第 7 步：在 Spwig 中进行配置

1. 在 Spwig 管理界面中，导航到 **企业 SSO > SSO 提供商配置**
2. 将 **提供商名称** 设置为 `Microsoft Entra ID`
3. 将第 5 步中获取的 Discovery URL 粘贴到 **OIDC 发现 URL** 中
4. 点击 **自动发现** —— 这将自动填充所有端点字段
5. 输入第 2 步中的 **客户端 ID**
6. 输入 **客户端密钥**（值）来自第 3 步
7. 如果在第 6 步中配置了组声明：
   - 将 **组声明** 设置为 `groups`
   - 在 **员工组** 中，输入应为员工的组的对象 ID（逗号分隔）
   - 在 **超级用户组** 中，输入应为超级用户的组的对象 ID（逗号分隔）
8. 点击 **保存**

## 第 8 步：启用并测试

1.

导航到 **站点设置 > 安全** 选项卡
2.

勾选 **启用管理员登录的 SSO**
3.

点击 **保存**
4.

在 **隐私/无痕窗口** 中打开管理员登录页面
5.

你应该会看到 **使用 Microsoft Entra ID 登录** 按钮

# 配置 Microsoft 身份验证

点击它 —— 你应该会被重定向到 Microsoft 的登录页面
7.

使用与 Spwig 中员工用户电子邮件匹配的 Microsoft 账户登录
8.

你应该会被重定向回 Spwig 管理仪表板

## 常见问题

| 问题 | 原因 | 解决方案 |
|---------|-------|----------|
| **AADSTS50011: 重定向 URI 不匹配** | Entra 中的重定向 URI 不完全匹配 | 确认重定向 URI 是 `https://your-store.com/oidc/callback/`，并包含结尾的斜杠。检查 HTTP 和 HTTPS 是否不匹配。 |
| **AADSTS700016: 应用程序未找到** | 错误的客户端 ID 或租户 | 仔细检查客户端 ID，并确保发现 URL 使用了正确的租户 ID |
| **在 Microsoft 登录成功但在 Spwig 登录失败** | Spwig 中没有匹配的用户 | 确保 Spwig 中存在与 Microsoft 账户相同电子邮件地址的员工账户。如果启用了“仅限员工”，请检查用户是否具有员工状态。 |
| **组声明为空** | 未配置组声明 | 按照步骤 6 将组声明添加到令牌配置中 |
| **组声明返回的是 URL 而不是 ID** | 用户属于超过 200 个组 | 使用组过滤功能限制令牌中的组，或指定特定组 |
| **几个月后 SSO 停止工作** | 客户端密钥已过期 | 在 Entra 中创建新的客户端密钥，并在 Spwig 的 SSO 提供商配置中更新它 |

## 建议

- **使用安全组** 进行角色映射，而不是 Microsoft 365 组或分发列表。

安全组专为访问控制而设计，与 OIDC 声明配合使用时最为可靠。
- **建议使用单租户** —— 选择“仅此组织目录中的账户”可将 SSO 限制为您的组织用户。


# 多租户配置需要额外的验证
- **设置较长的密钥过期时间** — 创建客户端密钥时选择24个月，并在22个月时设置日历提醒以轮换它。
- **条件访问** — 您可以在Entra ID中创建条件访问策略，这些策略专门适用于Spwig应用注册。

例如，要求使用多因素认证（MFA），阻止来自不可信位置的登录，或要求使用符合标准的设备。
- **使用非管理员账户进行测试** — 在Spwig中创建一个测试员工账户，以验证SSO在全面推广到整个团队之前是否正常工作。