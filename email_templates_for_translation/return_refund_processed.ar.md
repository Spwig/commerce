---
template_type: return_refund_processed
category: Returns
---

# Email Template: return_refund_processed

## Subject
تم معالجة الاسترجاع - طلب #{{ order_number }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="{{ theme.color.surface|default:'#f0fdf4' }}">
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="{{ theme.color.text|default:'#166534' }}">
          تم معالجة الاسترجاع
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text|default:'#166534' }}">
          طلب #{{ order_number }}
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          مرحباً {{ customer_name }},
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          تم فحص استرجاع طلبك <strong>#{{ order_number }}</strong>، وتم معالجة استرجاعك.
        </mj-text>

        <mj-section background-color="{{ theme.color.surface|default:'#f0fdf4' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#166534' }}">
              تفاصيل الاسترجاع
            </mj-text>
            <mj-text font-size="15px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>مبلغ الاسترجاع:</strong> {{ refund_currency }} {{ refund_amount }}
            </mj-text>
            {% if restocking_fee %}
            <mj-text font-size="15px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>رسوم إعادة المخزون:</strong> {{ restocking_fee_currency }} {{ restocking_fee }}
            </mj-text>
            {% endif %}
          </mj-column>
        </mj-section>

        <mj-section background-color="{{ theme.color.surface|default:'#fffbeb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-size="15px" line-height="1.6" color="{{ theme.color.text|default:'#92400e' }}">
              <strong>ملاحظة:</strong> قد يستغرق الأمر من 5 إلى 10 أيام عمل لظهور الاسترجاع في حسابك، حسب مزود الدفع الخاص بك.
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          إذا كانت لديك أي أسئلة حول استرجاعك، يرجى التواصل مع فريق الدعم لدينا.
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
تم معالجة الاسترجاع - طلب #{{ order_number }}

مرحباً {{ customer_name }},

تم فحص استرجاع طلبك #{{ order_number }}، وتم معالجة استرجاعك.

تفاصيل الاسترجاع:
- مبلغ الاسترجاع: {{ refund_currency }} {{ refund_amount }}
{% if restocking_fee %}- رسوم إعادة المخزون: {{ restocking_fee_currency }} {{ restocking_fee }}{% endif %}

ملاحظة: قد يستغرق الأمر من 5 إلى 10 أيام عمل لظهور الاسترجاع في حسابك، حسب مزود الدفع الخاص بك.

إذا كانت لديك أي أسئلة حول استرجاعك، يرجى التواصل مع فريق الدعم لدينا.