---
template_type: review_request
category: Enhanced E-commerce
---

# Email Template: review_request

## Subject
คุณพึงพอใจกับการซื้อสินค้าของคุณไหม? ให้รีวิวสินค้า

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
          เราอยากได้ความคิดเห็นจากคุณ!
        </mj-text>
        <mj-text font-size="16px" color="{{ theme.color.text_muted|default:'#6b7280' }}" align="center" padding-top="10px">
          Order #{{ order_number }}
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Personal Message -->
    <mj-section background-color="{{ theme.color.background|default:'#ffffff' }}" padding="20px">
      <mj-column>
        <mj-text font-size="14px" color="{{ theme.color.text|default:'#1f2937' }}" line-height="1.8">
          สวัสดี {{ customer_name }},
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text|default:'#1f2937' }}" padding-top="10px" line-height="1.8">
          เราหวังว่าคุณจะชอบสินค้าที่เพิ่งซื้อไป! ความคิดเห็นของคุณช่วยให้เราพัฒนาและช่วยให้ลูกค้าคนอื่นตัดสินใจอย่างมีข้อมูล
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Products to Review -->
    <mj-section background-color="{{ theme.color.background|default:'#ffffff' }}" padding="20px">
      <mj-column>
        <mj-text font-size="18px" font-weight="600" color="{{ theme.color.text|default:'#1f2937' }}" padding-bottom="15px">
          ให้รีวิวสินค้าของคุณ
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
          Qty: {{ item.quantity }}
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
          เขียนรีวิว
        </mj-button>
      </mj-column>
    </mj-section>
    {% endfor %}

    <!-- Incentive (if offered) -->
    {% if incentive_offered %}
    <mj-section background-color="{{ theme.color.info_light|default:'#dbeafe' }}" padding="20px">
      <mj-column>
        <mj-text font-size="16px" font-weight="600" color="{{ theme.color.text|default:'#1f2937' }}" align="center">
          🎁 รางวัลเพิ่มเติม
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text|default:'#1f2937' }}" align="center" padding-top="10px">
          {{ incentive_details }}
        </mj-text>
        {% if incentive_code %}
        <mj-text font-size="18px" font-weight="bold" color="{{ theme.color.primary|default:'#2563eb' }}" align="center" padding-top="10px">
          Code: {{ incentive_code }}
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
เราอยากได้ความคิดเห็นจากคุณ!

Order #{{ order_number }}

Hi {{ customer_name }},

เราหวังว่าคุณจะชอบสินค้าที่เพิ่งซื้อไป! ความคิดเห็นของคุณช่วยให้เราพัฒนาและช่วยให้ลูกค้าคนอื่นตัดสินใจอย่างมีข้อมูล

Review Your Purchase:
{% for item in items %}
- {{ item.name }} (Qty: {{ item.quantity }})
  Write review: {{ item.review_url }}
{% endfor %}

{% if incentive_offered %}
🎁 รางวัลเพิ่มเติม
{{ incentive_details }}
{% if incentive_code %}Code: {{ incentive_code }}{% endif %}
{% endif %}

Need Help?
Email: {{ support_email }}
Phone: {{ support_phone }}