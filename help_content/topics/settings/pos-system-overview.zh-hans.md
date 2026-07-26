---
title: POS系统概述
---

Spwig POS系统通过现代的销售终端将您的商店转变为完整的零售解决方案。它包含在所有版本中——社区版、专业版和企业版——无需额外费用即可在无限数量的地点使用无限数量的终端。每个终端都是一个渐进式网络应用（PWA），支持离线工作、自动同步，并与您的库存、客户数据和支付处理无缝集成。通过管理仪表板管理一切——终端配置、班次结算、收据自定义和硬件集成。

在您拥有实体零售地点、快闪店、贸易展览或任何顾客亲自购买而非在线购买的环境中使用POS系统。

![POS仪表板](/static/core/admin/img/help/pos-system-overview/dashboard.webp)

## 什么是Spwig POS？

Spwig POS是一个完全集成的销售点系统，专为同时在线和实体销售的商家设计。与需要复杂集成的第三方POS系统不同，Spwig POS直接构建在您的平台中，确保所有销售渠道的数据完全同步。

**关键特性**：
- **无限终端** - 无需额外费用即可部署所需数量的终端
- **离线优先架构** - 即使在失去互联网连接时也能继续处理销售
- **渐进式网络应用** - 无需应用商店安装；通过浏览器在任何设备上访问（平板电脑、计算机、专用终端）
- **实时库存同步** - 库存预订（15分钟TTL）防止跨渠道超卖
- **分账支付支持** - 每笔交易可接受多种支付方式（现金+银行卡+礼品卡）
- **硬件集成** - ESC/POS热敏打印机、条码扫描器、收银机、客户显示屏
- **班次管理** - 通过开/关账数和差异跟踪进行现金结算
- **多地点就绪** - 带有设置继承的商店组，适用于特许经营和区域管理

## 版本

POS 包含在 Spwig 的每个版本中 —— 社区版、专业版和企业版 —— 自 Spwig 1.5.8 起。

没有单独的 POS 许可证，无需激活步骤，也没有每终端费用。

**每个版本包含的内容**:
- 无限终端注册
- 无限员工分配
- 所有 POS 功能（班次、现金管理、收据自定义、客户显示屏）
- 支付提供商集成（Stripe Terminal 和其他支持的提供商）
- 硬件集成支持

运行 Spwig 托管商店或支付专业版/企业版许可证的商家将在可选的 Spwig 托管服务（GeoIP、地理编码器、推送通知）上获得更高的限制，并享有优先支持，但 POS 功能集本身在所有版本中是相同的。

## 系统架构

**前端** - React 18 进步式网络应用:
- 首次离线，使用 Service Worker 缓存（无需互联网连接即可工作）
- Vite 构建系统以实现快速加载
- CSS Modules + 设计令牌（与您的商店主题一致）
- IndexedDB 用于本地数据持久化
- 10 种支持的语言（英语、简体/繁体中文、法语、德语、西班牙语、葡萄牙语、日语、俄语、阿拉伯语）

**后端** - 后端集成:
- 13 个 POS 模型（POSTerminal、POSShift、CashMovement、ReceiptTemplate、PromoSlide 等）
- 43+ 个 REST API 端点用于终端操作
- 带 TTL 管理的库存预留系统
- Celery 任务用于后台同步
- 支付提供商的加密凭证存储

**安全性**:
- 通过 8 个字符的代码进行终端配对（服务器端生成，使用后过期）
- 员工分配控制哪些用户可以访问哪些终端
- 管理员紧急情况下的远程锁定/解锁功能
- 加密的支付提供商凭证
- 基于会话的认证，支持生物识别解锁（取决于浏览器）

## 开始使用工作流程

按照以下 4 个步骤部署您的第一个 POS 终端。

有关包括员工设置、支付提供商和完成第一笔销售的完整逐步检查清单，请参阅[POS入门](getting-started-with-pos)。

**步骤 1：创建仓库**
- 导航到 **目录 > 仓库**
- 创建代表您零售地点的仓库
- 配置地址和联系信息
- 该仓库将跟踪POS销售的实物库存

**步骤 2：注册终端**
- 导航到 **POS > 终端**
- 点击 **+ 添加终端**
- 设置终端名称（例如，"主收银台"，"结账1"）
- 从步骤 2 中分配仓库
- 配置硬件设置（打印机、扫描仪、钱箱）
- 保存以生成 8 个字符的配对代码

**步骤 3：分配员工**
- 在终端配置中，滚动到 **已分配用户**
- 选择被授权使用此终端的员工
- 仅已分配用户可以登录到终端
- 用户必须在其员工角色中具有适当的POS权限

**步骤 4：配对设备**
- 在您的终端设备（平板电脑/计算机）上，导航到 `/pos/` URL
- 输入来自步骤 3 的 8 个字符配对代码
- 终端下载配置并同步初始数据
- 使用分配的员工凭据登录
- 终端已准备好进行销售

配对后，终端会自动每 5 分钟同步一次（可配置）。离线模式允许在互联网不可用时继续操作——当连接恢复时，销售会自动同步。

## 核心POS功能

**销售处理**：
- 通过名称、SKU 或条形码搜索产品
- 分散支付（每笔订单使用多种支付方式）
- 暂存购物车（保存未完成的交易）
- 退款和作废并跟踪原因
- 应用折扣（优惠券、礼品卡、促销）
- 客户查找和积分兑换

- Shift opening with starting cash count

- Shift closing with expected vs actual reconciliation

- Cash movements (float adds, petty cash withdrawals with reasons)

- Automatic expected cash calculation based on cash sales

- Discrepancy tracking and reporting

- ESC/POS thermal receipt printers (network or serial)

- USB barcode scanners

- Cash drawer trigger via printer pulse

- Customer-facing displays (promotional carousel during idle)

- Stripe Terminal card readers (S700, WisePOS E, P400)

- Service Worker caches all terminal assets

- IndexedDB stores recent orders (configurable: 7-30 days, 200-1000 orders)

- Stock reservations with 15-minute TTL prevent overselling

- Queue sales for sync when connectivity returns

- Automatic reconnection detection

Access these admin pages to manage all aspects of your POS deployment:

- System overview and quick stats

- Recent terminal activity

- Active shifts summary

- Hosted-service usage tiles (GeoIP, geocoder, push — see [Spwig Hosted Services](hosted-services))

- Register and configure terminals

- Assign staff and warehouses

- Monitor online/offline status (heartbeat tracking)

- Remote unlock terminals

- [Learn more: Managing POS Terminals](managing-pos-terminals)

- View all shifts (open, closed, historical)

- Review cash reconciliation reports

- Track cash movements and discrepancies

- Audit shift activity

- [Learn more: POS Shifts and Cash Management](pos-shifts-cash-management)

- Organize terminals by location/region

- Configure group-level settings (currency, language, timezone)

- Implement settings inheritance hierarchy

- [Learn more: POS Store Groups](pos-store-groups)

**收据模板** (`/admin/pos_app/receipttemplate/`)
- 自定义打印收据（纸张宽度、标志、页眉/页脚）
- 配置合规字段（税号、商业注册）
- 添加促销的二维码
- 将模板作用域限定到特定商店或组
- [了解更多：收据模板自定义](receipt-template-customization)

**促销幻灯片** (`/admin/pos_app/promoslide/`)
- 创建客户显示轮播内容
- 将幻灯片定向到特定商店或组
- 安排季节性促销
- [了解更多：客户显示促销幻灯片](customer-display-promo-slides)

**支付提供商** (`/admin/pos_app/posterminalprovider/`)
- 配置Stripe终端集成
- 管理支付提供商凭证
- 监控连接状态
- [了解更多：支付终端提供商](payment-terminal-providers)

**卡片读取器** (`/admin/pos_app/posterminalreader/`)
- 注册物理卡片读取器
- 将读取器分配给终端
- 自定义启动画面（面向客户的显示品牌）
- 监控读取器状态（在线/离线/忙碌）
- [了解更多：卡片读取器管理](card-reader-management)

## 多地点部署

对于拥有多个零售地点的商家，Spwig POS支持分层设置继承：

**设置层次结构**（从最高优先级到最低）：
1. 终端特定设置（覆盖所有）
2. 商店特定设置（覆盖组和站点）
3. 组设置（覆盖站点默认值）
4. 站点默认值（所有情况的回退）

在组级别配置共享设置（例如区域货币、语言），并根据需要覆盖特定商店或终端的设置。有关详细配置指南，请参阅[POS商店组](pos-store-groups)。

## 小贴士

保留所有markdown格式、图片路径、代码块和技术术语。

- **从一个终端开始** - 在全面部署之前，先使用单个终端测试 POS 设置和工作流程
- **配对前分配仓库** - 未分配仓库的终端无法处理销售
- **提前配置收据模板** - 合规字段（税号）因地区而异；在上线前进行设置
- **测试离线模式** - 断开互联网连接并验证销售是否继续；重新连接时确认同步
- **使用商店组进行多地点管理** - 简化特许经营或区域部署的配置管理
- **监控心跳状态** - 终端每 5 分钟向服务器发送一次心跳；离线终端会显示在管理员仪表板中
- **为性能配置同步限制** - 网络连接较慢的终端可以从较低的 sync_days/sync_limit 设置中受益
- **备份硬件配置** - 记录打印机 IP、扫描仪设置、钱箱配置以进行灾难恢复