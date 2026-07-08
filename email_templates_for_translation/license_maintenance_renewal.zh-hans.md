---
template_type: license_maintenance_renewal
category: License
---

# Email Template: license_maintenance_renewal

## Subject
维护续订 - 订单 #{{ order_number }}

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
    <mj-section background-color="{{ theme.color.success|default:'#10b981' }}" padding="30px 20px">
      <mj-column>
        <mj-text font-size="28px" font-weight="bold" color="#ffffff" align="center">
          维护续订！
        </mj-text>
        <mj-text font-size="16px" color="#ffffffcc" align="center" padding-top="10px">
          订单 #{{ order_number }}
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
          您的 Spwig 维护订阅已成功续订。您将继续收到平台更新、安全补丁和新功能。
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Renewal Summary -->
    <mj-section background-color="{{ theme.color.background_secondary|default:'#f9fafb' }}" padding="20px" border-radius="8px">
      <mj-column>
        <mj-text font-size="16px" font-weight="bold" padding-bottom="10px">
          续订摘要
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          许可证密钥: {{ license_key }}
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          维护有效期至: {{ renewal_expires_at }}
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          订单号: {{ order_number }}
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- What's Included -->
    <mj-section>
      <mj-column>
        <mj-text font-size="16px" font-weight="bold" padding-bottom="10px">
          包含内容
        </mj-text>
        <mj-text font-size="14px">
          您的维护订阅可让您访问以下内容:
        </mj-text>
        <mj-text font-size="14px" padding-top="5px">
          - 平台功能更新和改进
        </mj-text>
        <mj-text font-size="14px">
          - 安全补丁和错误修复
        </mj-text>
        <mj-text font-size="14px">
          - 通过升级服务器发布的新组件
        </mj-text>
        <mj-text font-size="14px">
          - 技术支持
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Next Steps -->
    <mj-section>
      <mj-column>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          您无需采取任何操作。更新将继续通过您管理面板的组件更新系统提供。
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Support -->
    {% include 'email_system/mjml_components/support_block.mjml' %}
  </mj-body>
</mjml>

## Text Content
维护续订！

订单 #{{ order_number }}

你好 {{ customer_name }}，

您的 Spwig 维护订阅已成功续订。您将继续收到平台更新、安全补丁和新功能。

续订摘要：
- 许可证密钥: {{ license_key }}
- 维护有效期至: {{ renewal_expires_at }}
- 订单号: {{ order_number }}

包含内容：
- 平台功能更新和改进
- 安全补丁和错误修复
- 通过升级服务器发布的新组件
- 技术支持

您无需采取任何操作。更新将继续通过您管理面板的组件更新系统提供。

需要帮助？请联系 {{ support_email }}