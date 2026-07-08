---
title: 承运商预设
---

承运商预设用于定义在没有API集成的情况下创建的运输方式（DHL、FedEx、UPS、自定义承运商）——每个预设提供承运商标志、跟踪URL模板和显示设置。系统预设（DHL、FedEx、UPS、USPS）已预先配置且无法删除，而自定义预设允许商家添加区域性或专业承运商。预设链接到手动运输，商家在此手动输入跟踪号，而不是通过提供商API购买标签。

在创建手动运输或希望使用跟踪链接但没有完整API集成时使用承运商预设。

## 系统预设与自定义预设

**系统预设**（预装）：
- DHL、FedEx、UPS、USPS、Royal Mail、Canada Post、Australia Post
- 无法删除（is_system=True）
- 可覆盖跟踪URL或标志
- 提供默认跟踪URL模板

**自定义预设**（商家创建）：
- 区域性承运商（OnTrac、LaserShip、区域性邮政）
- 专业承运商（货运、白手套配送）
- 可编辑或删除
- 需要手动输入跟踪URL模板

---

## 承运商预设配置

每个预设定义：

**基本设置**：
- **名称**：承运商显示名称（例如，"DHL快递"，"本地快递"）
- **代码**：内部标识符（例如，"dhl"，"local_courier"）
- **标志**：承运商标志图像（可选，未提供时使用图标）
- **图标**：作为备用的FontAwesome图标（例如，"fa-truck"）
- **启用**：切换可见性

**跟踪配置**：
- **跟踪URL模板**：带有{tracking_id}占位符的URL模式
- **跟踪URL覆盖**：自定义URL（覆盖默认模板）

**系统设置**（仅限系统预设）：
- **是系统**：无法删除
- **是默认**：每种承运商类型有一个默认

---

## 跟踪URL模板

跟踪URL使用{tracking_id}占位符：

**示例**：

DHL: `https://www.dhl.com/en/express/tracking.html?AWB={tracking_id}`

FedEx: `https://www.fedex.com/fedextrack/?tracknumbers={tracking_id}`

UPS: `https://www.ups.com/track?tracknum={tracking_id}`

USPS: `https://tools.usps.com/go/TrackConfirmAction?tLabels={tracking_id}`

自定义: `https://track.localcourier.com/tracking/{tracking_id}`

**工作原理**：
1. 商家创建带有跟踪号"1234567890"的运输
2. 系统将{tracking_id}替换为实际号码
3. 客户点击跟踪链接 → 跳转到承运商网站
4. 结果: `https://www.dhl.com/en/express/tracking.html?AWB=1234567890`

---

## 创建自定义承运商预设

**步骤**：

1. 导航到设置 > 配送 > 承运商预设
2. 点击"添加承运商预设"
3. 输入名称（例如，"OnTrac"）
4. 输入代码（slug: "ontrac"）
5. 可选：上传标志图像
6. 选择图标（fa-truck、fa-shipping-fast等）
7. 输入带有{tracking_id}的跟踪URL模板
8. 启用 = 是
9. 保存

**示例 - OnTrac**：
```
名称: OnTrac
代码: ontrac
跟踪URL: https://www.ontrac.com/tracking.asp?tracking_number={tracking_id}
图标: fa-truck
启用: 是
```

---

## 覆盖系统预设的跟踪URL

系统预设可以有跟踪URL覆盖：

**使用场景**：您的承运商账户有特殊跟踪门户

**如何覆盖**：
1. 编辑系统预设（例如，DHL）
2. 在"跟踪URL覆盖"字段中输入覆盖URL
3. 覆盖优先于默认模板
4. 保存

**示例**：
```
系统: DHL
默认URL: https://www.dhl.com/en/express/tracking.html?AWB={tracking_id}
覆盖URL: https://track.dhl.com/special-account/{tracking_id}
结果: 所有DHL运输使用覆盖URL
```

---

## 承运商标志

**标志指南**：
- 格式: PNG或SVG（优先使用SVG以提高可扩展性）
- 尺寸: 推荐200×60像素
- 背景: 透明或白色
- 颜色: 完全彩色的承运商标识

**备用图标**：
如果未上传标志，系统将显示FontAwesome图标：
- fa-truck（默认）
- fa-shipping-fast（快递）
- fa-plane（空运）
- fa-box（包裹）

---

## 在运输中使用承运商预设

创建手动运输时：

1. 订单 > 订单详情 > 创建运输
2. 选择"手动运输"模式
3. 从预设下拉菜单中选择承运商
4. 输入跟踪号
5. 可选: 覆盖此运输的跟踪URL
6. 保存

**运输显示**：
- 显示承运商标志（或图标）
- 显示跟踪号
- 可点击的跟踪链接（使用预设URL模板）

---

## 默认承运商

每种系统可设置一个预设为默认：

**使用场景**：最常用的承运商在创建运输时自动选择

**如何设置**：
1. 编辑承运商预设
2. 勾选"是默认"
3. 保存
4. 如果有先前的默认，会自动取消设置

**只允许一个默认** - 设置新默认会移除之前的默认标志。

---

## 小贴士

- **使用描述性名称** - "DHL快递"比"DHL"更好
- **测试跟踪URL** - 验证模板是否能与真实跟踪号一起使用
- **上传承运商标志** - 在客户电子邮件中呈现专业外观
- **不要删除系统预设** - 它们已正确预配置
- **仅在承运商更改跟踪系统时使用覆盖**
- **为主要承运商设置默认** - 在创建运输时节省时间
- **保持预设启用** - 仅在承运商停运时停用
- **记录自定义承运商** - 添加关于区域性承运商的说明

Remember: Preserve all markdown formatting, image paths, code blocks, and technical terms exactly as shown in the preservation rules.