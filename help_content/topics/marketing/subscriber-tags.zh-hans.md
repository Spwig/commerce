---
title: 订阅者标签
---

标签是您为组织您的Campaign Studio受众而定义的标签——像`VIP`、`批发`或`活动-2026`这样的简短标记，您可以根据需要定义并应用到相应的订阅者。一旦一个标签存在，您可以根据它过滤您的订阅者列表，一次对任意数量的人应用或删除它，并且——最有用的是——在构建一个Segment时使用它作为条件，这样您的活动和旅程可以精确地定位您所标记的人。

## 什么是标签

标签只是您选择的名称。Spwig没有内置的标签，它永远不会自动应用一个标签——您决定它们的名称以及谁获得一个。这使得它们非常适合任何特定于您自己的业务且不映射到Spwig已跟踪的状态的内容：忠诚度等级、批发账户、在贸易展注册的所有人，或者像`event-2026`这样的单次活动列表。

每个标签还会自动生成一个**Slug**——其名称的简化、URL安全版本——当您创建它时会自动生成。Segments和filters内部使用slug；作为商家，您几乎从不需要查看它。

## 创建一个标签

标签有其自己的管理部分。打开**Campaign Studio > Subscribers**，然后点击页面顶部的**Campaign Studio**以查看Campaign Studio的所有部分，并选择**Subscriber tags**。

1. 点击**Add subscriber tag**。
2. 输入一个**Name**——简短且具体的名称效果最好，例如`VIP`、`Wholesale`或`Event 2026`。
3. Spwig在您输入时会填充一个匹配的**Slug**。您可以保留生成的值。
4. 如果您希望记录一个十六进制颜色（例如`#2563eb`）以供参考，还可以选择**Colour**字段。
5. 点击**Save**。

您也不必离开当前工作来创建一个——在任何订阅者的编辑页面的**Tags**字段旁边有一个绿色的**+**，会弹出相同的"添加标签"表单。


And if you try to bulk-tag subscribers before you've created any tags at all, the tag picker offers a **Create a tag** shortcut that takes you straight there.

## Tagging subscribers

The most common way to apply a tag is in bulk, from the Subscribers list:

1. Open **Campaign Studio > Subscribers**.
2. Tick the checkbox on each subscriber you want to tag (or **Select all on this page**).
3. From the **Bulk actions** dropdown, choose **Add tag to selected…** (or **Remove tag from selected…** to untag people).
4. Click **Go**.
5. Pick the tag from the list and click **Add tag** (or **Remove tag**).

![The bulk tag picker after choosing "Add tag to selected..." for four subscribers](/static/core/admin/img/help/subscriber-tags/bulk-tag-picker.webp)

Once applied, a tag shows as a small chip on the subscriber's card in the list, alongside their status and source badges. A **Tag** filter also appears in the Subscribers list's filter panel once you have at least one tag, so you can narrow the list down to everyone carrying a specific tag — handy for checking who's in an audience before you build a campaign around it.

![The Subscribers list filtered to the VIP tag, with the Import CSV button and tag chips visible](/static/core/admin/img/help/subscriber-tags/subscriber-list-tag-chips.webp)

You can also add or remove a single subscriber's tags directly from their own edit page, using the same **Tags** field the bulk action manages.

## Using tags in segments

Segments are the saved, rule-based audiences you point campaigns and journeys at. Once you've created at least one tag, a **Has tag** condition becomes available in the segment rule-builder — it doesn't appear on a fresh install with no tags defined, so you won't see a dead option before it's useful to you.

To use it, open **Campaign Studio > Segments**, add (or edit) a dynamic segment, and click **+ Add condition**:

1.

Set the condition's field to **Has tag**.
2.

选择一个操作符 — **is** 用于单个标签，或者 **is any of** 用于更灵活的表达方式。
3。

从下拉菜单中选择标签。

![设置为 VIP 的“Has tag”条件，显示匹配订阅者的实时数量](/static/core/admin/img/help/subscriber-tags/segment-has-tag-rule.webp)

当你构建规则时，右上角的计数会实时更新，这样你可以在保存之前准确查看当前符合条件的订阅者数量。每个 **Has tag** 条件目前每次仅匹配一个标签 —— 如果你想要一个匹配多个标签的受众（例如，`VIP` 或 `Wholesale`），请为每个标签添加一个 **Has tag** 条件，并将 **Match** 设置为 **any**。

这就是标签在组织之外的用途：基于 **Has tag** 构建的段落可以作为受众，你可以在广播或定期活动的 **Segment** 设置中选择该受众，或者作为旅程的 **Only for segment** 设置 —— 例如，“所有标记为 VIP 的人”可以有自己的欢迎系列、自己的定期新闻通讯，或者只是你在下次发送一次性公告时所选择的人群。

## 小贴士

保留所有 markdown 格式、图片路径、代码块和术语。

- 保持标签名称简短且具体 —— 它们会作为紧凑的芯片显示在订阅者卡片上，因此 `VIP` 比 `Very Important Person - Tier 1` 更易读。
- 使用 **标签** 筛选器在您围绕它构建一个分组或发送活动之前，对实际打标签的用户进行合理性检查。
- 标签是可叠加的 —— 从订阅者身上移除一个标签不会影响他们其他任何标签，也不会影响他们的状态、来源或同意。
- 在同一分组中使用标签与其他规则构建器条件（如 **订阅营销通讯** 或 **总消费金额**）以获得更精确的受众，而不仅仅是一个单独的标签。
- 一个订阅者可以携带任意数量的标签 —— 没有数量限制，因此可以用于多个重叠用途（如忠诚度等级 *and* 事件列表 *and* 来源备注）。
- 如果一个标签不再有用，从 **订阅者标签** 中删除它会将其从所有已应用该标签的订阅者以及任何引用它的分组规则中移除 —— 使用该标签的分组将简单地停止在该条件上进行匹配。