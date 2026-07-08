---
template_type: return_request_rejected
category: Returns
---

# Email Template: return_request_rejected

## Subject
تحديث طلب الإرجاع - طلب #{{ order_number }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="{{ theme.color.surface|default:'#fffbeb' }}">
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="{{ theme.color.text|default:'#92400e' }}">
          تحديث طلب الإرجاع
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text|default:'#92400e' }}">
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
          لقد قمنا بمراجعة طلب الإرجاع الخاص بك لطلب <strong>#{{ order_number }}</strong> ونستحيل الموافقة عليه في الوقت الحالي.
        </mj-text>

        {% if rejection_reason %}
        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-size="15px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>السبب:</strong> {{ rejection_reason }}
            </mj-text>
          </mj-column>
        </mj-section>
        {% endif %}

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          إذا كانت لديك أسئلة حول هذا القرار أو تعتقد أن هناك خطأ، يرجى التواصل مع فريق الدعم لدينا.
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
تحديث طلب الإرجاع - طلب #{{ order_number }}

مرحباً {{ customer_name }},

لقد قمنا بمراجعة طلب الإرجاع الخاص بك لطلب #{{ order_number }} ونستحيل الموافقة عليه في الوقت الحالي.

{% if rejection_reason %}السبب: {{ rejection_reason }}{% endif %}

إذا كانت لديك أسئلة حول هذا القرار أو تعتقد أن هناك خطأ، يرجى التواصل مع فريق الدعم لدينا.