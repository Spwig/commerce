---
template_type: review_request
category: Enhanced E-commerce
---

# Email Template: review_request

## Subject
您的購買體驗如何？留下評價

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
          我們很期待您的意見！
        </mj-text>
        <mj-text font-size="16px" color="{{ theme.color.text_muted|default:'#6b7280' }}" align="center" padding-top="10px">
          訂單 #{{ order_number }}
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Personal Message -->
    <mj-section background-color="{{ theme.color.background|default:'#ffffff' }}" padding="20px">
      <mj-column>
        <mj-text font-size="14px" color="{{ theme.color.text|default:'#1f2937' }}" line-height="1.8">
          您好 {{ customer_name }}，
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text|default:'#1f2937' }}" padding-top="10px" line-height="1.8">
          希望您喜歡最近的購買！您的意見幫助我們改進，也幫助其他客戶做出明智的決定。
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Products to Review -->
    <mj-section background-color="{{ theme.color.background|default:'#ffffff' }}" padding="20px">
      <mj-column>
        <mj-text font-size="18px" font-weight="600" color="{{ theme.color.text|default:'#1f2937' }}" padding-bottom="15px">
          評價您的購買
        </mj-text>
      </mj-column>
    </mj-section>

    {% for item in items %}
    <mj-section background-color="{{ theme.color.background|default:'#ffffff' }}" padding="15px 20px" css-class="review-item">
      <mj-column width="100px">
        <mj-image src="{{ item.product_thumbnail_url }}" alt="{{ item.name }}" width="80px" border-radius="6px" />
      </mj-column>
      <mj-column width="60%" vertical-align="middle">
        <mj-text font-size="14px" font-weight="600" color="{{ theme.color.text|default:'#1f2937' }}">
          {{ item.name }}
        </mj-text>
        <mj-text font-size="12px" color="{{ theme.color.text_muted|default:'#6b7280' }}" padding-top="5px">
          數量：{{ item.quantity }}
        </mj-text>
      </mj-column>
      <mj-column width="30%" vertical-align="middle">
        <mj-button
          href="{{ item.review_url }}"
          background-color="{{ theme.color.primary|default:'#2563eb' }}"
          color="{{ theme.color.background|default:'#ffffff' }}"
          font-size="12px"
          border-radius="4px"
          padding="8px 16px"
          inner-padding="8px 16px"
        >
          寫評價
        </mj-button>
      </mj-column>
    </mj-section>
    {% endfor %}

    <!-- Incentive (if offered) -->
    {% if incentive_offered %}
    <mj-section background-color="{{ theme.color.info_light|default:'#dbeafe' }}" padding="20px">
      <mj-column>
        <mj-text font-size="16px" font-weight="600" color="{{ theme.color.text|default:'#1f2937' }}" align="center">
          🎁 優惠獎勵
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text|default:'#1f2937' }}" align="center" padding-top="10px">
          {{ incentive_details }}
        </mj-text>
        {% if incentive_code %}
        <mj-text font-size="18px" font-weight="bold" color="{{ theme.color.primary|default:'#2563eb' }}" align="center" padding-top="10px">
          訂購碼：{{ incentive_code }}
        </mj-text>
        {% endif %}
      </mj-column>
    </mj-section>
    {% endif %}

    <!-- Support Block -->
    {% include 'email_system/mjml_components/support_block.mjml' %}
  </mj-body>
</mjml>

## Text Content
我們很期待您的意見！

訂單 #{{ order_number }}

您好 {{ customer_name }}，

希望您喜歡最近的購買！您的意見幫助我們改進，也幫助其他客戶做出明智的決定。

評價您的購買：
{% for item in items %}
- {{ item.name }} (數量：{{ item.quantity }})
  寫評價：{{ item.review_url }}
{% endfor %}

{% if incentive_offered %}
🎁 優惠獎勵
{{ incentive_details }}
{% if incentive_code %}訂購碼：{{ incentive_code }}{% endif %}
{% endif %}

需要幫助嗎？
郵箱：{{ support_email }}
電話：{{ support_phone }}