---
template_type: order_delay
category: Enhanced E-commerce
---

# Email Template: order_delay

## Subject
تحديث: تأخير في طلبك #{{ order_number }}

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
          إشعار بتأخير الطلب
        </mj-text>
        <mj-text font-size="16px" color="#856404" align="center" padding-top="10px">
          طلب #{{ order_number }}
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Apology Message -->
    <mj-section background-color="{{ theme.color.background|default:'#ffffff' }}" padding="30px 20px">
      <mj-column>
        <mj-text font-size="16px" color="{{ theme.color.text|default:'#1f2937' }}">
          العزيز {{ customer_name }},
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
          <strong>تاريخ التسليم الأصلي:</strong>
        </mj-text>
        <mj-text font-size="16px" color="{{ theme.color.text|default:'#1f2937' }}" align="center" padding-top="5px">
          <s>{{ original_delivery_date }}</s>
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}" align="center" padding-top="15px">
          <strong>التاريخ المقدر الجديد للتسليم:</strong>
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
          العناصر المتضررة
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
          الكمية: {{ item.quantity }}
        </mj-text>
      </mj-column>
    </mj-section>
    {% endfor %}

    <!-- Compensation (if offered) -->
    {% if compensation_offered %}
    <mj-section background-color="#d4edda" padding="20px">
      <mj-column>
        <mj-text font-size="16px" font-weight="600" color="#155724" align="center">
          كتعويض...
        </mj-text>
        <mj-text font-size="14px" color="#155724" align="center" padding-top="10px">
          {{ compensation_details }}
        </mj-text>
        {% if discount_code %}
        <mj-text font-size="18px" font-weight="bold" color="#155724" align="center" padding-top="10px">
          الكود: {{ discount_code }}
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
إشعار بتأخير الطلب

طلب #{{ order_number }}

العزيز {{ customer_name }},

{{ delay_reason }}

تاريخ التسليم الأصلي: {{ original_delivery_date }}
التاريخ المقدر الجديد للتسليم: {{ new_delivery_date }}

العناصر المتضررة:
{% for item in items %}
- {{ item.name }} (الكمية: {{ item.quantity }})
{% endfor %}

{% if compensation_offered %}
كتعويض...
{{ compensation_details }}
{% if discount_code %}الكود: {{ discount_code }}{% endif %}
{% endif %}

عرض حالة الطلب: {{ order_url }}

هل تحتاج إلى مساعدة؟
البريد الإلكتروني: {{ support_email }}
الهاتف: {{ support_phone }}