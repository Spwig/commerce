---
template_type: shipping_exception
category: Shipping
---

# Email Template: shipping_exception

## Subject
استثناء الشحن - تتطلب طلبك #{{ order_number }} انتباهًا

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#fef3c7">
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="#92400e" align="center">
          ⚠️ استثناء الشحن
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          مرحباً {{ customer_name }},
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          نحن نكتب لك لإعلامك باستثناء في شحنك. نحن نعمل على حل هذه المشكلة بأسرع ما يمكن.
        </mj-text>

        <mj-spacer height="20px" />

        <mj-section background-color="#fef3c7" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="#92400e">
              تفاصيل الاستثناء:
            </mj-text>
            <mj-text color="#92400e">
              <strong>نوع الاستثناء:</strong> {{ exception_type }}<br/>
              <strong>الوصف:</strong> {{ exception_description }}<br/>
              <strong>وقت الحدوث:</strong> {{ exception_date }}
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="20px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
              معلومات الطلب:
            </mj-text>
            <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>رقم الطلب:</strong> {{ order_number }}<br/>
              <strong>رقم التتبع:</strong> {{ tracking_number }}<br/>
              <strong>الشركة الناقلة:</strong> {{ carrier_name }}<br/>
              <strong>الموقع الحالي:</strong> {{ current_location }}
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          ماذا يحدث بعد ذلك؟
        </mj-text>

        <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
          {{ resolution_steps }}
        </mj-text>

        <mj-spacer height="20px" />

        {% if action_required %}
        <mj-section background-color="#fee2e2" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-weight="bold" color="#991b1b">
              ⚠️ يتطلب إجراء:
            </mj-text>
            <mj-text color="#7f1d1d">
              {{ action_required_description }}
            </mj-text>
          </mj-column>
        </mj-section>
        <mj-spacer height="20px" />
        {% endif %}

        <mj-button href="{{ tracking_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          تتبع طلبك
        </mj-button>

        <mj-spacer height="10px" />

        <mj-button href="{{ support_url }}" background-color="#6b7280" color="#ffffff" font-size="14px" border-radius="6px" padding="10px 25px">
          تواصل مع الدعم
        </mj-button>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
⚠️ استثناء الشحن

مرحباً {{ customer_name }},

نحن نكتب لك لإعلامك باستثناء في شحنك. نحن نعمل على حل هذه المشكلة بأسرع ما يمكن.

تفاصيل الاستثناء:
- نوع الاستثناء: {{ exception_type }}
- الوصف: {{ exception_description }}
- وقت الحدوث: {{ exception_date }}

معلومات الطلب:
- رقم الطلب: {{ order_number }}
- رقم التتبع: {{ tracking_number }}
- الشركة الناقلة: {{ carrier_name }}
- الموقع الحالي: {{ current_location }}

ماذا يحدث بعد ذلك؟
{{ resolution_steps }}

{% if action_required %}
⚠️ يتطلب إجراء:
{{ action_required_description }}
{% endif %}

تتبع طلبك: {{ tracking_url }}
تواصل مع الدعم: {{ support_url }}