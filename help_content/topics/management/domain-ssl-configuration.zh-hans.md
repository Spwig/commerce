---
title: 域名与SSL配置
---

本指南介绍了如何将自定义域名连接到您的Spwig商店，并设置SSL证书以实现安全的HTTPS访问。您可以在安装期间配置域名，也可以稍后添加一个。

## 安装后添加域名

如果您在没有域名的情况下安装了Spwig（使用服务器的IP地址），您可以随时添加一个。

### 第1步：设置DNS

通过您的域名注册商或DNS提供商：

1. 创建一个指向您的服务器IP地址的**A记录**，用于您的域名（或子域名）
2. 如果使用类似`shop.example.com`的子域名，请为`shop`创建A记录
3. 等待DNS传播——这通常需要5–60分钟

验证DNS记录是否生效：

```bash
dig +short shop.example.com
```

这应该返回您的服务器IP地址。

### 第2步：运行域名配置脚本

通过SSH连接到您的服务器，并导航到您的Spwig安装目录：

```bash
./configure-domain.sh
```

该脚本将：

1. 要求您输入域名名称
2. 验证DNS是否指向您的服务器
3. 更新商店的配置
4. 从Let's Encrypt获取免费SSL证书
5. 配置Web服务器以使用HTTPS
6. 重新启动相关服务

您的商店现在可以通过`https://yourdomain.com`访问。

### 第3步：更新商店设置

添加域名后，登录到您的管理面板，进入**商店设置**。验证**商店URL**是否与您的新域名匹配。这确保电子邮件、发票和链接使用正确的地址。

## SSL证书

### 自动SSL（Let's Encrypt）

在**独立模式**下，安装程序会自动从Let's Encrypt获取免费SSL证书。这些证书：

- 被所有主要浏览器信任
- 有效期为90天
- 自动续期——每天运行续期检查，当证书剩余时间少于30天时会自动续期
- 覆盖您的确切域名（例如`shop.example.com`）

您无需手动管理续期。

### 自签名证书

保留所有Markdown格式、图片路径、代码块和专业术语。

在某些情况下，Spwig 会使用自签名证书代替：

- **本地模式** 安装（开发/测试）
- 当 Let's Encrypt 无法访问您的服务器时（防火墙阻止了 80 端口，DNS 尚未传播）
- 当未配置域名（仅通过 IP 访问）

自签名证书可以加密流量，但不受浏览器信任 — 访问者会看到安全警告。这适用于测试，但不应在生产环境中使用。

### Sidecar 模式 SSL

在 **sidecar 模式** 中，您现有的 Web 服务器（Apache、Nginx、Caddy 等）负责处理 SSL 终止。Spwig 在您的代理后面运行在 HTTP 端口上。按照正常方式在您的主 Web 服务器上配置 SSL。

安装程序会生成一个代理配置块，您可以将其添加到您的 Web 服务器中。对于 Nginx，它看起来类似：

```nginx
location / {
    proxy_pass http://127.0.0.1:8080;
    proxy_set_header Host $host;
    proxy_set_header X-Real-IP $remote_addr;
    proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    proxy_set_header X-Forwarded-Proto $scheme;
}
```

## 更改您的域名

要切换到不同的域名：

1. 为新域名设置 DNS（A 记录指向您的服务器）
2. 使用新域名再次运行 `./configure-domain.sh`
3. 脚本将更新所有配置，获取新证书并重新启动服务
4. 在管理面板中更新 **商店设置** 中的新 URL

一旦配置更新，您的旧域名将停止工作。

## 故障排除

### "DNS 验证失败"

configure-domain 脚本会在请求证书前检查您的域名是否指向您的服务器。如果此检查失败：

- 使用 `dig +short yourdomain.com` 验证 A 记录是否正确
- 等待几分钟以允许 DNS 传播
- 检查您是否配置了确切的域名或子域名（而不是通配符）

### "Let's Encrypt 速率限制已达到"

Let's Encrypt 将证书请求限制为每个域名每周 5 次。如果您达到此限制：

- 等待 7 天后再尝试
- 在此期间使用不同的子域名
- 等待期间可通过 HTTP 或使用自签名证书访问商店

### "端口 80 无法访问"

Let's Encrypt 必须通过端口 80 连接到您的服务器以验证域名所有权。请确保：

- 防火墙允许入站 TCP 端口 80
- 没有其他应用程序阻止端口 80
- 您的云提供商的安全组或网络防火墙允许端口 80

### 证书续订失败

如果自动续订失败，证书将在 90 天后过期。要手动续订：

```bash
docker exec spwig_nginx certbot renew
docker exec spwig_nginx nginx -s reload
```

如果此操作失败，请检查续订日志以获取详细信息。最常见的原因是初始安装后防火墙更改导致端口 80 被阻止。