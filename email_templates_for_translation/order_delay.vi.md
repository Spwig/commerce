---
template_type: order_delay
category: Enhanced E-commerce
---

# Email Template: order_delay

## Subject
Cập nhật: Giao hàng chậm cho đơn hàng #{{ order_number }}

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
    <mj-section background-color="{{ theme.color.warning_light|default:'#fef3c7' }}" padding="30px 20px">
      <mj-column>
        <mj-text font-size="28px" font-weight="bold" color="#856404" align="center">
          Thông báo giao hàng chậm
        </mj-text>
        <mj-text font-size="16px" color="#856404" align="center" padding-top="10px">
          Đơn hàng #{{ order_number }}
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Apology Message -->
    <mj-section background-color="{{ theme.color.background|default:'#ffffff' }}" padding="30px 20px">
      <mj-column>
        <mj-text font-size="16px" color="{{ theme.color.text|default:'#1f2937' }}">
          Kính gửi {{ customer_name }},
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text|default:'#1f2937' }}" padding-top="15px" line-height="1.8">
          {{ delay_reason }}
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Delivery Date Update -->
    <mj-section background-color="{{ theme.color.info_light|default:'#dbeafe' }}" padding="20px">
      <mj-column>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}" align="center">
          <strong>Ngày giao hàng ban đầu:</strong>
        </mj-text>
        <mj-text font-size="16px" color="{{ theme.color.text|default:'#1f2937' }}" align="center" padding-top="5px">
          <s>{{ original_delivery_date }}</s>
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}" align="center" padding-top="15px">
          <strong>Ngày giao hàng dự kiến mới:</strong>
        </mj-text>
        <mj-text font-size="18px" color="{{ theme.color.primary|default:'#2563eb' }}" font-weight="600" align="center" padding-top="5px">
          {{ new_delivery_date }}
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Delayed Items -->
    <mj-section background-color="{{ theme.color.background|default:'#ffffff' }}" padding="20px">
      <mj-column>
        <mj-text font-size="16px" font-weight="600" color="{{ theme.color.text|default:'#1f2937' }}" padding-bottom="15px">
          Các mặt hàng bị ảnh hưởng
        </mj-text>
      </mj-column>
    </mj-section>

    {% for item in items %}
    <mj-section background-color="{{ theme.color.background|default:'#ffffff' }}" padding="10px 20px">
      <mj-column width="80px">
        <mj-image src="{{ item.product_thumbnail_url }}" alt="{{ item.name }}" width="60px" border-radius="6px" />
      </mj-column>
      <mj-column width="80%" vertical-align="middle">
        <mj-text font-size="14px" font-weight="600" color="{{ theme.color.text|default:'#1f2937' }}">
          {{ item.name }}
        </mj-text>
        <mj-text font-size="12px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          Qty: {{ item.quantity }}
        </mj-text>
      </mj-column>
    </mj-section>
    {% endfor %}

    <!-- Compensation (if offered) -->
    {% if compensation_offered %}
    <mj-section background-color="#d4edda" padding="20px">
      <mj-column>
        <mj-text font-size="16px" font-weight="600" color="#155724" align="center">
          Như một lời xin lỗi...
        </mj-text>
        <mj-text font-size="14px" color="#155724" align="center" padding-top="10px">
          {{ compensation_details }}
        </mj-text>
        {% if discount_code %}
        <mj-text font-size="18px" font-weight="bold" color="#155724" align="center" padding-top="10px">
          Mã: {{ discount_code }}
        </mj-text>
        {% endif %}
      </mj-column>
    </mj-section>
    {% endif %}

    <!-- CTA Button -->
    {% include 'email_system/mjml_components/cta_button.mjml' with url=order_url text="View Order Status" %}

    <!-- Support Block -->
    {% include 'email_system/mjml_components/support_block.mjml' %}
  </mj-body>
</mjml>

## Text Content
Thông báo giao hàng chậm

Đơn hàng #{{ order_number }}

Kính gửi {{ customer_name }},

{{ delay_reason }}

Ngày giao hàng ban đầu: {{ original_delivery_date }}
Ngày giao hàng dự kiến mới: {{ new_delivery_date }}

Các mặt hàng bị ảnh hưởng:
{% for item in items %}
- {{ item.name }} (Qty: {{ item.quantity }})
{% endfor %}

{% if compensation_offered %}
Như một lời xin lỗi...
{{ compensation_details }}
{% if discount_code %}Mã: {{ discount_code }}{% endif %}
{% endif %}

Xem trạng thái đơn hàng: {{ order_url }}

Cần hỗ trợ?
Email: {{ support_email }}
Điện thoại: {{ support_phone }}