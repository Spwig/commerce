---
template_type: hosted_provision_complete
category: License
---

# Email Template: hosted_provision_complete

## Subject
您的商店已准备就绪 - {{ store_name }}

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
    <mj-section background-color="{{ theme.color.primary|default:'#2563eb' }}" padding="30px 20px">
      <mj-column>
        <mj-text font-size="28px" font-weight="bold" color="#ffffff" align="center">
          您的商店已上线！
        </mj-text>
        <mj-text font-size="16px" color="#ffffffcc" align="center" padding-top="10px">
          {{ store_name }} 已为您准备就绪
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Greeting -->
    <mj-section>
      <mj-column>
        <mj-text font-size="16px">
          你好 {{ name|default:'there' }}，
        </mj-text>
        <mj-text>
          好消息！您的 Spwig 商店 <strong>{{ store_name }}</strong> 已完成配置并正式上线。您可以立即开始设置产品、品牌和支付方式。
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Store Details -->
    <mj-section background-color="{{ theme.color.background_secondary|default:'#f9fafb' }}" padding="20px" border-radius="8px">
      <mj-column>
        <mj-text font-size="16px" font-weight="bold" padding-bottom="10px">
          您的商店详情
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          商店网址：{{ store_url }}
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          管理面板：{{ admin_url }}
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          区域：{{ region }}
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Getting Started -->
    <mj-section>
      <mj-column>
        <mj-text font-size="16px" font-weight="bold" padding-bottom="10px">
          快速入门
        </mj-text>
        <mj-text font-size="14px">
          1. 使用结账时设置的电子邮件和密码登录管理面板
        </mj-text>
        <mj-text font-size="14px">
          2. 在 设计 > 主题设置 中添加商店标志和品牌信息
        </mj-text>
        <mj-text font-size="14px">
          3. 在 目录 > 产品 中添加您的第一个产品
        </mj-text>
        <mj-text font-size="14px">
          4. 在 设置 > 支付提供商 中设置支付方式
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- CTA -->
    {% include 'email_system/mjml_components/cta_button.mjml' with url=admin_url text="Go to Admin Panel" %}

    <!-- Support -->
    {% include 'email_system/mjml_components/support_block.mjml' %}
  </mj-body>
</mjml>

## Text Content
您的商店已上线！

{{ store_name }} 已为您准备就绪。

你好 {{ name|default:'there' }}，

好消息！您的 Spwig 商店 {{ store_name }} 已完成配置并正式上线。您可以立即开始设置产品、品牌和支付方式。

您的商店详情：
- 商店网址：{{ store_url }}
- 管理面板：{{ admin_url }}
- 区域：{{ region }}

快速入门：
1. 使用结账时设置的电子邮件和密码登录管理面板
2. 在 设计 > 主题设置 中添加商店标志和品牌信息
3. 在 目录 > 产品 中添加您的第一个产品
4. 在 设置 > 支付提供商 中设置支付方式

前往管理面板：{{ admin_url }}

需要帮助？请联系 {{ support_email }}