---
title: Tax Configuration
---

配置商店的税务规则，以便根据客户的所在地自动将正确的税款应用于订单。您可以通过单击一次加载区域预设，或者为任何国家、州、城市或邮政编码创建自定义规则。

![Tax Dashboard](/static/core/admin/img/help/tax-configuration/tax-dashboard.webp)

## Tax Dashboard

导航到 **Orders > Shipments > Tax Rates** 以打开税务仪表板。该页面显示：

- **Statistics panel** — 四个卡片显示总规则数、活动规则数、覆盖的国家以及使用的税种
- **Filters** — 按名称、国家或州搜索，并按国家、税种（销售税、增值税、商品及服务税、自定义）或状态（活动/非活动）进行筛选
- **Tax rule cards** — 每个卡片显示国家旗帜、规则名称、位置、税率百分比、税种徽章、状态徽章、优先级和豁免数量

## Loading Tax Presets

点击 **Load Presets** 打开预设模态框。预设是为一个地区准备的标准税率集合，只需单击即可加载到您的商店中。

![Load Presets](/static/core/admin/img/help/tax-configuration/tax-presets-modal.webp)

预设按世界地区组织：

| Region | Preset Groups |
|--------|--------------|
| **Africa** | Africa VAT (25 rates) |
| **Asia Pacific** | Asia-Pacific VAT/GST (24 rates), Central Asia VAT (6 rates) |
| **Europe** | EU VAT Rates, UK VAT, Other European VAT |
| **Latin America** | Latin America VAT |
| **Middle East** | Middle East VAT |
| **North America** | US State Sales Tax, Canadian GST/HST |
| **Oceania** | Oceania GST/VAT |

### How Presets Work

1. 点击您想要的预设组的 **Load**
2. 系统为该组中的每个国家或州创建税务规则
3. 已有规则如果具有相同的国家、州和税种，将自动跳过以防止重复
4. 加载后，每条规则都可以完全编辑 — 调整税率、添加豁免或停用不需要的规则

您可以加载多个预设组。例如，如果您向欧洲各地的客户销售，可以同时加载 EU VAT 和 UK VAT。

## Creating Tax Rules Manually

点击 **Add Tax Rate** 创建自定义规则。表单有四个部分：

![Tax Rate Form](/static/core/admin/img/help/tax-configuration/tax-rate-form.webp)

### Basic Information

| Field | Description |
|-------|-------------|
| **Name** | 规则的显示名称（例如，"California Sales Tax"） |
| **Is Active** | 开关以启用或停用规则 |
| **Tax Type** | 销售税、增值税、商品及服务税或自定义税 |
| **Rate (%)** | 税率以百分比表示（例如，输入 8.25 表示 8.25%） |
| **Priority** | 当多个规则匹配同一位置时，数字越大优先级越高 |

### Geographic Scope

| Field | Description |
|-------|-------------|
| **Country** | ISO 3166-1 alpha-2 代码（例如，US、GB、DE） |
| **State** | 州或省（留空以适用于整个国家） |
| **City** | 城市名称（可选，用于城市级别的税务规则） |
| **Postal Codes** | 具体邮政编码列表（可选，用于邮政编码级别的税务规则） |

规则是按从最具体到最不具体的顺序匹配的。特定邮政编码的规则优先于同一州的规则，而同一州的规则又优先于国家范围的规则。

### Application Rules

| Field | Description |
|-------|-------------|
| **Applies to Shipping** | 勾选后，此税也适用于运费 |
| **Compound Tax** | 勾选后，此税是在其他税的基础上计算（基数金额加上已应用的税） |

### Product Exemptions

| Field | Description |
|-------|-------------|
| **Exempt Product Types** | 免税的产品类型（例如，数字产品、服务） |
| **Exempt Categories** | 免税的具体产品类别 |

## Tax Types

| Type | Used For | Examples |
|------|----------|---------|
| **Sales Tax** | US, Canada | 州和省级销售税 |
| **VAT** | Europe, UK, much of Asia and Africa | 增值税 |
| **GST** | Australia, New Zealand, India, Singapore | 商品及服务税 |
| **Custom Tax** | Special cases | 本地附加税、环境税、奢侈品税 |

## How Tax Calculation Works

当客户到达结账页面时，系统会根据他们的送货地址自动计算税款：

1. **Geographic matching** — 找到所有与客户国家匹配的活动规则，然后按州、城市和邮政编码进一步缩小范围
2. **Specificity scoring** — 更具体的规则（邮政编码 > 城市 > 州 > 国家）排名更高
3. **Priority ordering** — 在同一具体性级别内，优先级更高的规则优先
4. **Product exemptions** — 免税产品从每个适用规则中排除
5. **Non-compound taxes** — 首先根据每个商品的基准价格计算
6. **Compound taxes** — 根据基准价格加上已应用的所有非复合税计算
7. **Shipping tax** — 如果规则启用了 "Applies to Shipping"，则运费包含在应税金额中

税款明细会与订单一起存储，因此您可以确切地看到哪些规则适用以及每条规则贡献了多少。

## Common Setups

### EU Store

1. 点击 **Load Presets** 并加载 **EU VAT Rates** 组
2. 这会为所有欧盟成员国创建增值税规则，使用当前的标准税率
3. 如果您还向英国客户销售，可选择加载 **UK VAT**

### US Store

1. 点击 **Load Presets** 并加载 **US State Sales Tax** 组
2. 这会为所有征收销售税的美国州创建销售税规则
3. 对于城市级别的税，手动添加带有城市字段和更高优先级的规则

### Multi-Region Store

1. 为每个销售市场加载多个预设组
2. 系统会根据客户所在的位置应用正确的税款
3. 根据您的具体业务需求调整个别规则

## Tips

- **从预设开始** — 加载目标市场的预设组，然后自定义单个税率，而不是从头开始创建每条规则。
- **明智地使用优先级** — 为更具体的本地规则设置更高的优先级值，以确保它们正确地覆盖更广泛的区域规则。
- **仔细检查复合税** — 复合税很少见。大多数司法管辖区使用简单的（非复合）税。只有在本地法规明确要求计算税款时才启用复合税。
- **保持规则启用/停用** — 对于季节性或临时性的更改，不要删除税务规则，而是将其停用并在需要时重新启用。
- **上线前进行测试** — 设置好税务规则后，从不同地址下测试订单，以验证正确的税款是否被应用。

记住：保留所有Markdown格式、图片路径、代码块和技术术语，严格按照保存规则所示。