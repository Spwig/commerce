---
template_type: dev_new_review
category: Developer Portal
---

# Email Template: dev_new_review

## Subject
关于 {{ component_name }} 的新 {{ rating }} 星评价

## HTML Content
<mjml>
  <mj-head>
    <mj-attributes>
      <mj-text font-family="Arial, sans-serif" line-height="1.6" />
      <mj-all font-family="Arial, sans-serif" />
    </mj-attributes>
  </mj-head>
  <mj-body background-color="{{ theme.color.background_secondaryondary|default:'#f9fafb' }}">
    <!-- Header -->
    <mj-section background-color="{{ theme.color.background|default:'#ffffff' }}" padding="40px 20px">
      <mj-column>
        <mj-text font-size="28px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}" align="center">
          新评价已收到
        </mj-text>
        <mj-text font-size="16px" color="{{ theme.color.text_muted|default:'#6b7280' }}" align="center" padding-top="10px">
          一位商家已评价 {{ component_name }}
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
          一位商家已对你的组件 <strong>{{ component_name }}</strong> 留下评价。
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Review Details -->
    <mj-section background-color="{{ theme.color.background_secondaryondary|default:'#f9fafb' }}" padding="30px 25px">
      <mj-column>
        <mj-text font-size="24px" color="{{ theme.color.warning|default:'#f59e0b' }}" align="center" padding-bottom="10px">
          {{ rating_stars }}
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}" align="center" padding-bottom="15px">
          {{ rating }}/5 星
        </mj-text>
        {% if review_title %}
        <mj-text font-size="18px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}" align="center" padding-bottom="15px">
          {{ review_title }}
        </mj-text>
        {% endif %}
        <mj-text font-size="15px" color="{{ theme.color.text|default:'#1f2937' }}" padding="20px" background-color="{{ theme.color.background|default:'#ffffff' }}" border-left="3px solid {{ theme.color.primary|default:'#2563eb' }}">
          "{{ review_comment }}"
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}" align="right" padding-top="15px">
          — {{ reviewer_name }}{% if is_verified_purchase %} <span style="color: {{ theme.color.success|default:'#10b981' }};">✓ 已验证购买</span>{% endif %}
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Action Info -->
    <mj-section background-color="{{ theme.color.background|default:'#ffffff' }}" padding="25px 20px">
      <mj-column>
        <mj-text font-size="16px" color="{{ theme.color.text|default:'#1f2937' }}">
          你可以从开发者门户回复此评价。
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- CTA Button -->
    <mj-section background-color="{{ theme.color.background|default:'#ffffff' }}" padding="20px">
      <mj-column>
        <mj-button background-color="{{ theme.color.primary|default:'#2563eb' }}" color="{{ theme.color.background|default:'#ffffff' }}" href="{{ reviews_url }}" border-radius="6px" font-size="16px" font-weight="bold" padding="15px 30px">
          查看并回复
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

一位商家已对你的组件 {{ component_name }} 留下评价。

{{ rating_stars }} ({{ rating }}/5)
{% if review_title %}{{ review_title }}{% endif %}

{{ review_comment }}

— {{ reviewer_name }}{% if is_verified_purchase %} (已验证购买){% endif %}

你可以从开发者门户回复此评价。

查看并回复：{{ reviews_url }}

---
Spwig 开发者门户