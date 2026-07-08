---
title: 字体编辑器
---

字体编辑器是一个共享样式工具，可让您完全控制文本的外观。在页面构建器、页眉/页脚构建器或菜单构建器中的任何元素上编辑字体属性时，它会以浮动面板的形式打开。

![字体编辑器](/static/core/admin/img/help/typography-editor/typography-editor.webp)

## 实时预览

编辑器在面板顶部显示并排比较：

| Box | Purpose |
|-----|---------|
| **Current** | 显示现有字体样式中的 "The quick brown fox..." |
| **New** | 在您调整设置时实时更新，显示应用前的结果 |

这使您可以在应用更改之前比较更改前后的效果。

## 字体选项卡

字体选项卡是编辑器打开时的默认视图。

**字体系列** — 一个可搜索的下拉菜单，包含 70 多种按类别组织的字体。每种字体都会以自己的字体样式进行预览，以便在选择前查看其外观。需要时，字体会按需从 Google Fonts 加载。

**字体大小** — 带单位选择器的数字输入，支持 px、em、rem 和 %。默认值为 16px。

**字体粗细** — 从 100（细）到 900（黑）的滑块：

| Value | Name |
|-------|------|
| 100 | Thin |
| 200 | Extra Light |
| 300 | Light |
| 400 | Regular |
| 500 | Medium |
| 600 | Semi Bold |
| 700 | Bold |
| 800 | Extra Bold |
| 900 | Black |

并非每种字体都支持所有九种粗细。编辑器会显示所选字体系列可用的粗细。

**字体样式** — 用于 Normal、Italic 和 Oblique 的切换按钮。

## 间距选项卡

微调字符周围和之间的间距：

| Control | What It Does | Default |
|---------|-------------|---------|
| **行高** | 文本行之间的垂直间距 | normal |
| **字母间距** | 单个字符之间的水平间距 | normal |
| **单词间距** | 单词之间的水平间距 | normal |
| **文本缩进** | 段落第一行的缩进 | 0 |

每个间距控件都包含一个单位选择器（px、em、rem、%）。

## 样式选项卡

控制文本装饰和视觉效果：

- **文本装饰** — 无、下划线、上划线或删除线
- **装饰样式** — 实线、虚线、点线、双线或波浪线（当启用装饰时适用）
- **装饰颜色** — 装饰线的颜色选择器，默认为文本颜色
- **文本阴影** — 可选的阴影效果，带有偏移、模糊和颜色控制

## 变换选项卡

在不编辑内容的情况下更改文本的大小写：

| Option | Result |
|--------|--------|
| **None** | 文本按原样显示 |
| **Uppercase** | ALL LETTERS ARE CAPITALIZED |
| **Lowercase** | all letters are lowercase |
| **Capitalize** | First Letter Of Each Word Is Capitalized |

此选项卡上的其他控件包括 **文本对齐**（左对齐、居中、右对齐、两端对齐）、**垂直对齐** 和 **文本方向**（从左到右或从右到左）。

## 可用字体系列

编辑器包含一组精选的系统字体和 Google Fonts，按类别分组：

| 分类 | 字体
|----------|-------|
| **系统字体** | 系统默认, Arial, Helvetica Neue, Helvetica, Segoe UI, Roboto, Ubuntu, Verdana, Tahoma, Trebuchet MS
| **无衬线（现代）** | Inter, Montserrat, Poppins, DM Sans, Space Grotesk, Plus Jakarta Sans, Outfit, Manrope, Figtree, Josefin Sans
| **无衬线（经典）** | Open Sans, Lato, Nunito, Nunito Sans, Source Sans 3, Raleway, Rubik, Work Sans, Mulish, Cabin, Karla, Barlow, Lexend
| **衬线** | Playfair Display, Merriweather, Lora, Libre Baskerville, Cormorant Garamond, Source Serif 4, EB Garamond, Crimson Pro, Bitter, Fraunces, Spectral, Cardo, Alegreya
| **衬线（系统）** | Georgia, Times New Roman, Palatino, Book Antiqua, Garamond, Cambria
| **等宽字体** | Source Code Pro, Fira Code, JetBrains Mono, Roboto Mono, IBM Plex Mono, Space Mono, Inconsolata, Consolas, Monaco, Menlo, Courier New, SF Mono
| **显示字体** | Oswald, Bebas Neue, Anton, Archivo Black, Rajdhani, Righteous, Abril Fatface, Archivo, Impact, Arial Black |

Google Fonts 在选中后会自动加载。系统字体使用适当的 CSS 备用链，以确保在不同平台上可靠渲染。

## 出现位置

Typography Editor 在需要文本样式的地方均可使用：

- **页面构建器** — 选择任意元素，打开样式选项卡，然后点击 Typography 部分
- **页眉/页脚构建器** — 对导航链接、logo 文本、菜单项和页脚内容进行文本样式设置
- **菜单构建器** — 控制菜单标签和子菜单项的字体
- **目录管理** — 在产品描述和内容编辑器中使用，当字体控制功能可用时

无论上下文如何，编辑器始终通过相同的界面访问。

## 小贴士

- **有意搭配字体** — 使用显示字体或衬线字体作为标题，使用干净的无衬线字体作为正文文本。经典的组合如 Playfair Display + Inter 或 Montserrat + Merriweather 效果很好。
- **限制每页的字体族数量** — 每页使用两到三种字体族通常就足够了。过多的字体族可能会减慢加载时间并造成视觉混乱。
- **使用相对单位进行响应式文本** — em 和 rem 会随着基础字体大小进行缩放，使您的排版能够自动适应不同的屏幕尺寸。
- **检查权重可用性** — 如果 400 和 500 的文本看起来一样，所选字体可能不支持该权重。编辑器会显示每种字体提供的权重。
- **在所有设备上预览** — 在桌面尺寸上看起来好的文本可能在移动设备上太小或太大。使用 Page Builder 的设备预览功能进行验证。
- **使用实时预览** — 在应用更改之前，始终在预览框中比较 Current vs New，以避免出现意外更改。