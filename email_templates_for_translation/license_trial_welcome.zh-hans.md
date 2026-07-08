---
template_type: license_trial_welcome
category: License
---

# Email Template: license_trial_welcome

## Subject
欢迎使用 Spwig - 您的 {{ trial_days }} 天免费试用

## HTML Content
<mjml>
  <mj-head>
    <mj-attributes>
      <mj-all font-family="'Helvetica Neue', Helvetica, Arial, sans-serif" />
      <mj-text font-size="14px" color="#333333" line-height="20px" />
      <mj-section background-color="{{ theme.color.background|default:'#ffffff' }}" padding="20px" />
    </mj-attributes>
  </mj-head>
  <mj-body background-color="{{ theme.color.background_secondary|default:'#f9fafb' }}">
    <!-- Header -->
    <mj-section background-color="#059669" padding="30px 20px">
      <mj-column>
        <mj-text font-size="28px" font-weight="bold" color="#ffffff" align="center">
          欢迎来到 Spwig！
        </mj-text>
        <mj-text font-size="16px" color="#ffffffcc" align="center" padding-top="10px">
          您的 {{ trial_days }} 天免费试用已准备就绪
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Greeting -->
    <mj-section>
      <mj-column>
        <mj-text font-size="16px">
          你好 {{ customer_name }}，
        </mj-text>
        <mj-text>
          感谢您试用 <strong>{{ product_name }}</strong>！您的试用已激活，您有 <strong>{{ trial_days }} 天</strong> 的时间来探索 Spwig 提供的所有功能{% if includes_pos %}，包括我们的收银系统{% endif %}。
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Setup Token Box -->
    <mj-section background-color="#f0fdf4" padding="25px" border-radius="8px">
      <mj-column>
        <mj-text font-size="12px" color="#065f46" font-weight="bold" align="center">
          您的安装令牌
        </mj-text>
        <mj-text font-size="14px" font-weight="bold" color="#059669" align="center" font-family="'Courier New', monospace" padding="10px 0" word-break="break-all">
          {{ setup_token }}
        </mj-text>
        <mj-text font-size="12px" color="{{ theme.color.text_muted|default:'#6b7280' }}" align="center">
          安装时使用此令牌以激活您的试用商店
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Getting Started -->
    <mj-section>
      <mj-column>
        <mj-text font-size="16px" font-weight="bold" padding-bottom="10px">
          入门指南
        </mj-text>
        <mj-text font-size="14px">
          1. 按照我们的安装指南将 Spwig 安装到您的服务器上
        </mj-text>
        <mj-text font-size="14px">
          2. 安装过程中提示时输入您的安装令牌
        </mj-text>
        <mj-text font-size="14px">
          3. 开始构建您的在线商店！
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Setup Guide CTA -->
    {% include 'email_system/mjml_components/cta_button.mjml' with url=setup_url text="查看安装指南" %}

    <!-- What's Included -->
    <mj-section background-color="{{ theme.color.background_secondary|default:'#f9fafb' }}" padding="20px" border-radius="8px">
      <mj-column>
        <mj-text font-size="16px" font-weight="bold" padding-bottom="10px">
          您的试用包含以下内容
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          {{ trial_days }} 天内可完全访问所有核心功能
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          产品目录、订单和客户管理
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          主题自定义和页面构建器
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          支付和物流提供商集成
        </mj-text>
        {% if includes_pos %}
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          收银系统（POS）
        </mj-text>
        {% endif %}
      </mj-column>
    </mj-section>

    <!-- Trial Info -->
    <mj-section>
      <mj-column>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          您的试用将在 {{ trial_days }} 天后到期。准备好后，升级为完整许可证以继续运行您的商店，不会丢失任何数据。
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Support -->
    {% include 'email_system/mjml_components/support_block.mjml' %}
  </mj-body>
</mjml>

## Text Content
欢迎使用 Spwig！
您的 {{ trial_days }} 天免费试用已准备就绪。

你好 {{ customer_name }}，

感谢您试用 {{ product_name }}！您的试用已激活，您有 {{ trial_days }} 天的时间来探索 Spwig 提供的所有功能{% if includes_pos %}，包括我们的收银系统{% endif %}。

您的安装令牌：
{{ setup_token }}
安装时使用此令牌以激活您的试用商店。

入门指南：
1. 按照我们的安装指南将 Spwig 安装到您的服务器上
2. 安装过程中提示时输入您的安装令牌
3. 开始构建您的在线商店！

查看安装指南：{{ setup_url }}

您的试用包含以下内容：
- {{ trial_days }} 天内可完全访问所有核心功能
- 产品目录、订单和客户管理
- 主题自定义和页面构建器
- 支付和物流提供商集成
{% if includes_pos %}- 收银系统（POS）{% endif %}

您的试用将在 {{ trial_days }} 天后到期。准备好后，升级为完整许可证以继续运行您的商店，不会丢失任何数据。

需要帮助？请联系 {{ support_email }}