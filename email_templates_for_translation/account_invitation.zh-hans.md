---
template_type: account_invitation
category: Core E-commerce
---

# Email Template: account_invitation

## Subject
在 {{ site_name }} 创建您的账户

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
          您被邀请了！
        </mj-text>
        <mj-text font-size="16px" color="#ffffffcc" align="center" padding-top="10px">
          在 {{ site_name }} 创建您的账户
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Greeting -->
    <mj-section>
      <mj-column>
        <mj-text font-size="16px">
          你好，{{ customer_name }}，
        </mj-text>
        <mj-text>
          我们注意到您之前是以访客身份在我们这里购物的。创建一个完整的账户，可以解锁诸如订单跟踪、更快结账和专属优惠等福利。
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Order History Summary -->
    <mj-section background-color="{{ theme.color.background_secondary|default:'#f9fafb' }}" padding="20px" border-radius="8px">
      <mj-column>
        <mj-text font-size="16px" font-weight="bold" padding-bottom="10px">
          您的购物历史
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          总订单数：{{ total_orders }}
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          总消费金额：{{ total_spent }}
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Benefits -->
    <mj-section>
      <mj-column>
        <mj-text font-size="16px" font-weight="bold" padding-bottom="10px">
          为什么要创建账户？
        </mj-text>
        <mj-text font-size="14px">
          - 跟踪您的订单并查看订单历史
        </mj-text>
        <mj-text font-size="14px">
          - 使用保存的详细信息更快结账
        </mj-text>
        <mj-text font-size="14px">
          - 管理您的地址和偏好
        </mj-text>
        <mj-text font-size="14px">
          - 访问专属优惠和促销活动
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- CTA Button -->
    {% include 'email_system/mjml_components/cta_button.mjml' with url=activation_url text="Create Your Account" %}

    <!-- Note -->
    <mj-section>
      <mj-column>
        <mj-text font-size="12px" color="{{ theme.color.text_muted|default:'#6b7280' }}" align="center">
          此链接将允许您为账户设置密码。您现有的订单历史将被保留。
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Support -->
    {% include 'email_system/mjml_components/support_block.mjml' %}
  </mj-body>
</mjml>

## Text Content
您被邀请创建您的账户！

你好，{{ customer_name }}，

我们注意到您之前是以访客身份在我们这里购物的。创建一个完整的账户，可以解锁诸如订单跟踪、更快结账和专属优惠等福利。

您的购物历史：
- 总订单数：{{ total_orders }}
- 总消费金额：{{ total_spent }}

为什么要创建账户？
- 跟踪您的订单并查看订单历史
- 使用保存的详细信息更快结账
- 管理您的地址和偏好
- 访问专属优惠和促销活动

创建您的账户：{{ activation_url }}

此链接将允许您为账户设置密码。您现有的订单历史将被保留。

需要帮助？请联系 {{ support_email }}