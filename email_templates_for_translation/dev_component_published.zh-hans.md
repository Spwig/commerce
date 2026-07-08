---
template_type: dev_component_published
category: Developer Portal
---

# Email Template: dev_component_published

## Subject
{{ component_name }} v{{ version }} 现已在 Spwig 市场上线！

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
    <mj-section background-color="{{ theme.color.success|default:'#10b981' }}" padding="50px 20px">
      <mj-column>
        <mj-text font-size="36px" font-weight="bold" color="{{ theme.color.background|default:'#ffffff' }}" align="center">
          现已上线！
        </mj-text>
        <mj-text font-size="18px" color="{{ theme.color.background|default:'#ffffff' }}" align="center" padding-top="15px">
          您的组件已在 Spwig 市场上线
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Content -->
    <mj-section background-color="{{ theme.color.background|default:'#ffffff' }}" padding="30px 20px">
      <mj-column>
        <mj-text font-size="16px" color="{{ theme.color.text|default:'#1f2937' }}">
          你好，{{ developer_name }}，
        </mj-text>
        <mj-text font-size="16px" color="{{ theme.color.text|default:'#1f2937' }}" padding-top="20px">
          您的组件现已上线，并可供所有 Spwig 商家在市场中使用！
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Component Details -->
    <mj-section background-color="{{ theme.color.background_secondaryondary|default:'#f9fafb' }}" padding="25px 20px">
      <mj-column>
        <mj-text font-size="16px" color="{{ theme.color.text|default:'#1f2937' }}" padding-bottom="8px">
          <strong>组件：</strong> {{ component_name }}
        </mj-text>
        <mj-text font-size="16px" color="{{ theme.color.text|default:'#1f2937' }}" padding-bottom="8px">
          <strong>类型：</strong> {{ component_type }}
        </mj-text>
        <mj-text font-size="16px" color="{{ theme.color.text|default:'#1f2937' }}">
          <strong>版本：</strong> v{{ version }}
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Analytics Info -->
    <mj-section background-color="{{ theme.color.background|default:'#ffffff' }}" padding="25px 20px">
      <mj-column>
        <mj-text font-size="16px" color="{{ theme.color.text|default:'#1f2937' }}">
          在分析仪表板上跟踪您的组件表现 —— 当商家开始使用时，下载量、评分和评论将会显示出来。
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- CTA Button -->
    <mj-section background-color="{{ theme.color.background|default:'#ffffff' }}" padding="30px 20px">
      <mj-column>
        <mj-button background-color="{{ theme.color.success|default:'#10b981' }}" color="{{ theme.color.background|default:'#ffffff' }}" href="{{ dashboard_url }}" border-radius="6px" font-size="16px" font-weight="bold" padding="15px 30px">
          查看分析
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

您的组件现已上线，并可供所有 Spwig 商家在市场中使用！

组件：{{ component_name }}
类型：{{ component_type }}
版本：v{{ version }}

在分析仪表板上跟踪您的组件表现 —— 当商家开始使用时，下载量、评分和评论将会显示出来。

查看分析：{{ dashboard_url }}

---
Spwig 开发者门户