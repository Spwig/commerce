---
template_type: dev_new_review
category: Developer Portal
---

# Email Template: dev_new_review

## Subject
新 {{ rating }} 星評價在 {{ component_name }}

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
          新評價已收到
        </mj-text>
        <mj-text font-size="16px" color="{{ theme.color.text_muted|default:'#6b7280' }}" align="center" padding-top="10px">
          一位商家評價了 {{ component_name }}
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Content -->
    <mj-section background-color="{{ theme.color.background|default:'#ffffff' }}" padding="30px 20px">
      <mj-column>
        <mj-text font-size="16px" color="{{ theme.color.text|default:'#1f2937' }}">
          Hi {{ developer_name }},
        </mj-text>
        <mj-text font-size="16px" color="{{ theme.color.text|default:'#1f2937' }}" padding-top="20px">
          一位商家在您的元件 <strong>{{ component_name }}</strong> 上留下了評價。
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
          — {{ reviewer_name }}{% if is_verified_purchase %} <span style="color: {{ theme.color.success|default:'#10b981' }};">✓ 已驗證購買</span>{% endif %}
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Action Info -->
    <mj-section background-color="{{ theme.color.background|default:'#ffffff' }}" padding="25px 20px">
      <mj-column>
        <mj-text font-size="16px" color="{{ theme.color.text|default:'#1f2937' }}">
          您可以從開發者專用門戶回應這則評價。
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- CTA Button -->
    <mj-section background-color="{{ theme.color.background|default:'#ffffff' }}" padding="20px">
      <mj-column>
        <mj-button background-color="{{ theme.color.primary|default:'#2563eb' }}" color="{{ theme.color.background|default:'#ffffff' }}" href="{{ reviews_url }}" border-radius="6px" font-size="16px" font-weight="bold" padding="15px 30px">
          查看並回應
        </mj-button>
      </mj-column>
    </mj-section>

    <!-- Footer -->
    <mj-section background-color="{{ theme.color.background_secondaryondary|default:'#f9fafb' }}" padding="30px 20px">
      <mj-column>
        <mj-divider border-color="{{ theme.color.border|default:'#e5e7eb' }}" padding-bottom="20px"></mj-divider>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}" align="center">
          <strong>Spwig 開發者專用門戶</strong>
        </mj-text>
        <mj-text font-size="12px" color="{{ theme.color.text_muted|default:'#6b7280' }}" align="center" padding-top="10px">
          有問題嗎？請聯繫開發者支援
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
Hi {{ developer_name }},

一位商家在您的元件 {{ component_name }} 上留下了評價。

{{ rating_stars }} ({{ rating }}/5)
{% if review_title %}{{ review_title }}{% endif %}

{{ review_comment }}

— {{ reviewer_name }}{% if is_verified_purchase %} (已驗證購買){% endif %}

您可以從開發者專用門戶回應這則評價。

查看並回應：{{ reviews_url }}

---
Spwig 開發者專用門戶