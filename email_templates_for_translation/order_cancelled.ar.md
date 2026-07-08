---
template_type: order_cancelled
category: Core E-commerce
---

# Email Template: order_cancelled

## Subject
لقد تم إلغاء طلبك #{{ order_number }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}">
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          تم إلغاء الطلب
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          مرحباً {{ customer_name }},
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          تم إلغاء طلبك <strong>#{{ order_number }}</strong>.
        </mj-text>

        {% if cancellation_reason %}
        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-size="15px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>السبب:</strong> {{ cancellation_reason }}
            </mj-text>
          </mj-column>
        </mj-section>
        {% endif %}

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          إذا تم دفع قيمة الطلب، فسيتم إرجاع المبلغ وفقًا للطريقة الأصلية للدفع.
        </mj-text>

        <mj-spacer height="30px" />

        {% if order_url %}
        <mj-button href="{{ order_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          عرض تفاصيل الطلب
        </mj-button>
        {% endif %}
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
تم إلغاء الطلب

مرحباً {{ customer_name }},

تم إلغاء طلبك #{{ order_number }}.

{% if cancellation_reason %}السبب: {{ cancellation_reason }}{% endif %}

إذا تم دفع قيمة الطلب، فسيتم إرجاع المبلغ وفقًا للطريقة الأصلية للدفع.

{% if order_url %}عرض تفاصيل الطلب: {{ order_url }}{% endif %}

هل لديك أسئلة حول هذا الإلغاء؟
البريد الإلكتروني: {{ support_email }}
الهاتف: {{ support_phone }}