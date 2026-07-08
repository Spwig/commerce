---
template_type: dev_license_approved
category: Developer Portal
---

# Email Template: dev_license_approved

## Subject
您的 Spwig 开发者许可证已准备就绪！

## HTML Content
<mjml>
  <mj-head>
    <mj-attributes>
      <mj-text font-family="Arial, sans-serif" line-height="1.6" />
      <mj-all font-family="Arial, sans-serif" />
    </mj-attributes>
  </mj-head>
  <mj-body background-color="{{ theme.color.background_secondaryondary|default:'#f9fafb' }}">
    <!-- Header with Success Accent -->
    <mj-section background-color="{{ theme.color.success|default:'#10b981' }}" padding="40px 20px">
      <mj-column>
        <mj-text font-size="32px" font-weight="bold" color="{{ theme.color.background|default:'#ffffff' }}" align="center">
          许可证已批准！
        </mj-text>
        <mj-text font-size="16px" color="{{ theme.color.background|default:'#ffffff' }}" align="center" padding-top="10px">
          您的开发许可证已准备就绪
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Content -->
    <mj-section background-color="{{ theme.color.background|default:'#ffffff' }}" padding="30px 20px">
      <mj-column>
        <mj-text font-size="16px" color="{{ theme.color.text|default:'#1f2937' }}">
          你好 {{ developer_name }}，
        </mj-text>
        <mj-text font-size="16px" color="{{ theme.color.text|default:'#1f2937' }}" padding-top="20px">
          您的开发者许可证请求已获批准。您可以使用此许可证运行本地 Spwig 安装，用于开发和测试。
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- License Key Section -->
    <mj-section background-color="{{ theme.color.background_secondaryondary|default:'#f9fafb' }}" padding="30px 20px">
      <mj-column>
        <mj-text font-size="14px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}" align="center" padding-bottom="15px">
          您的许可证密钥
        </mj-text>
        <mj-text font-size="18px" font-family="monospace" color="{{ theme.color.text|default:'#1f2937' }}" align="center" padding="20px" background-color="{{ theme.color.background|default:'#ffffff' }}" border="2px solid {{ theme.color.success|default:'#10b981' }}">
          {{ license_key }}
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- License Details -->
    <mj-section background-color="{{ theme.color.background|default:'#ffffff' }}" padding="25px 20px">
      <mj-column>
        <mj-text font-size="16px" color="{{ theme.color.text|default:'#1f2937' }}" padding-bottom="8px">
          <strong>许可证类型：</strong> {{ license_type }}
        </mj-text>
        {% if expires_at %}
        <mj-text font-size="16px" color="{{ theme.color.text|default:'#1f2937' }}">
          <strong>过期时间：</strong> {{ expires_at }}
        </mj-text>
        {% endif %}
      </mj-column>
    </mj-section>

    <!-- Important Notice -->
    <mj-section background-color="{{ theme.color.background_secondaryondary|default:'#f9fafb' }}" padding="25px 20px">
      <mj-column>
        <mj-text font-size="14px" color="{{ theme.color.text|default:'#1f2937' }}" padding="15px" background-color="{{ theme.color.background|default:'#ffffff' }}" border-left="3px solid {{ theme.color.warning|default:'#f59e0b' }}">
          <strong>重要：</strong> 此许可证仅用于开发目的。请勿用于生产环境或与他人共享。
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- CTA Button -->
    <mj-section background-color="{{ theme.color.background|default:'#ffffff' }}" padding="30px 20px">
      <mj-column>
        <mj-button background-color="{{ theme.color.success|default:'#10b981' }}" color="{{ theme.color.background|default:'#ffffff' }}" href="{{ dashboard_url }}" border-radius="6px" font-size="16px" font-weight="bold" padding="15px 30px">
          前往仪表板
        </mj-button>
      </mj-column>
    </mj-section>

    <!-- Footer -->
    <mj-section background-color="{{ theme.color.background_secondaryondary|default:'#f9fafb' }}" padding="30px 20px">
      <mj-column>
        <mj-divider border-color="{{ theme.color.border|default:'#e5e7eb' }}" padding-bottom="20px"></mj-divider>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}" align="center">
          <strong>Spwig 开发者门户</strong>
        </mj-text>
        <mj-text font-size="12px" color="{{ theme.color.text_muted|default:'#6b7280' }}" align="center" padding-top="10px">
          有问题？请联系开发者支持
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
你好 {{ developer_name }}，

您的开发者许可证请求已获批准。您可以使用此许可证运行本地 Spwig 安装，用于开发和测试。

您的许可证密钥：
{{ license_key }}

许可证类型：{{ license_type }}{% if expires_at %}
过期时间：{{ expires_at }}{% endif %}

重要：此许可证仅用于开发目的。请勿用于生产环境或与他人共享。

前往仪表板：{{ dashboard_url }}

---
Spwig 开发者门户