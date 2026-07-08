---
template_type: dev_review_digest
category: Developer Portal
---

# Email Template: dev_review_digest

## Subject
{{ review_count }} 条新评论（{{ period }} 汇总）

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
    <mj-section background-color="{{ theme.color.primary|default:'#2563eb' }}" padding="40px 20px">
      <mj-column>
        <mj-text font-size="32px" font-weight="bold" color="{{ theme.color.background|default:'#ffffff' }}" align="center">
          {{ review_count }} 条新评论
        </mj-text>
        <mj-text font-size="16px" color="{{ theme.color.background|default:'#ffffff' }}" align="center" padding-top="10px">
          您的 {{ period }} 汇总
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
          自您上次 {{ period }} 汇总以来，您有 {{ review_count }} 条新评论。
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Reviews List -->
    {% for review in reviews %}
    <mj-section background-color="{{ theme.color.background_secondaryondary|default:'#f9fafb' }}" padding="20px">
      <mj-column>
        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}" padding-bottom="8px">
          {{ review.component_name }}
        </mj-text>
        <mj-text font-size="20px" color="{{ theme.color.warning|default:'#f59e0b' }}" padding-bottom="10px">
          {{ review.rating_stars }}
        </mj-text>
        {% if review.title %}
        <mj-text font-size="15px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}" padding-bottom="8px">
          {{ review.title }}
        </mj-text>
        {% endif %}
        <mj-text font-size="14px" color="{{ theme.color.text|default:'#1f2937' }}" padding="15px" background-color="{{ theme.color.background|default:'#ffffff' }}" border-left="3px solid {{ theme.color.primary|default:'#2563eb' }}">
          {{ review.comment|truncatewords:40 }}
        </mj-text>
        <mj-text font-size="13px" color="{{ theme.color.text_muted|default:'#6b7280' }}" padding-top="10px">
          — {{ review.reviewer_name }}
        </mj-text>
      </mj-column>
    </mj-section>

    {% if not forloop.last %}
    <mj-section background-color="{{ theme.color.background|default:'#ffffff' }}" padding="0px">
      <mj-column>
        <mj-divider border-color="{{ theme.color.border|default:'#e5e7eb' }}"></mj-divider>
      </mj-column>
    </mj-section>
    {% endif %}
    {% endfor %}

    <!-- CTA Button -->
    <mj-section background-color="{{ theme.color.background|default:'#ffffff' }}" padding="30px 20px">
      <mj-column>
        <mj-button background-color="{{ theme.color.primary|default:'#2563eb' }}" color="{{ theme.color.background|default:'#ffffff' }}" href="{{ reviews_url }}" border-radius="6px" font-size="16px" font-weight="bold" padding="15px 30px">
          查看所有评论
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

自您上次 {{ period }} 汇总以来，您有 {{ review_count }} 条新评论。

{% for review in reviews %}---
{{ review.component_name }} — {{ review.rating_stars }}
{% if review.title %}{{ review.title }}{% endif %}
{{ review.comment|truncatewords:40 }}
— {{ review.reviewer_name }}
{% endfor %}

查看所有评论：{{ reviews_url }}

---
Spwig 开发者门户