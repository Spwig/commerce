---
template_type: subscription_plan_upgraded
category: Subscriptions
---

# Email Template: subscription_plan_upgraded

## Subject
✓ تم ترقية خطة الاشتراك الخاصة بك!

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#dcfce7">
      <mj-column>
        <mj-text font-size="24px" font-weight="bold" color="#065f46" align="center">
          ✓ تم ترقية الخطة!
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          مرحبًا بكم في {{ new_plan_name }}
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Hi {{ customer_name }},
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          تم ترقية خطة الاشتراك الخاصة بك بنجاح. الآن يمكنك الاستمتاع بجميع مزايا {{ new_plan_name }}!
        </mj-text>

        <mj-spacer height="30px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
              تفاصيل تغيير الخطة:
            </mj-text>
            <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>الخطة السابقة:</strong> {{ old_plan_name }}<br/>
              <strong>الخطة الجديدة:</strong> {{ new_plan_name }}<br/>
              <strong>تم الترقية في:</strong> {{ upgrade_date }}<br/>
              <strong>مباشرة</strong>
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          ما الجديد:
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}" line-height="1.8">
          {{ new_features }}
        </mj-text>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          معلومات الفاتورة:
        </mj-text>

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>السعر الجديد:</strong> {{ new_price }} / {{ billing_period }}<br/>
              <strong>تاريخ الفاتورة التالي:</strong> {{ next_billing_date }}<br/>
              {% if prorated_charge %}<strong>الرسوم المحسوبة مسبقًا اليوم:</strong> {{ prorated_charge }}{% endif %}
            </mj-text>
          </mj-column>
        </mj-section>

        {% if prorated_charge %}
        <mj-spacer height="20px" />
        <mj-section background-color="#eff6ff" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="14px" color="#1e40af" line-height="1.6">
              💡 تم فرض رسوم قدرها {{ prorated_charge }} اليوم على باقي فترة الفاتورة الحالية الخاصة بك.
            </mj-text>
          </mj-column>
        </mj-section>
        {% endif %}

        <mj-spacer height="30px" />

        <mj-button href="{{ account_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          عرض اشتراكي
        </mj-button>

        <mj-spacer height="20px" />

        <mj-text font-size="14px" color="{{ theme.color.text_secondary|default:'#6b7280' }}" align="center">
          هل لديك أسئلة؟ <a href="{{ support_url }}" style="color: {{ theme.color.primary|default:'#2563eb' }};">اتصل بالدعم</a>
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
✓ تم ترقية الخطة!

مرحبًا بكم في {{ new_plan_name }}

Hi {{ customer_name }},

تم ترقية خطة الاشتراك الخاصة بك بنجاح. الآن يمكنك الاستمتاع بجميع مزايا {{ new_plan_name }}!

تفاصيل تغيير الخطة:
- الخطة السابقة: {{ old_plan_name }}
- الخطة الجديدة: {{ new_plan_name }}
- تم الترقية في: {{ upgrade_date }}
- مباشرة

ما الجديد:
{{ new_features }}

معلومات الفاتورة:
- السعر الجديد: {{ new_price }} / {{ billing_period }}
- تاريخ الفاتورة التالي: {{ next_billing_date }}
{% if prorated_charge %}- الرسوم المحسوبة مسبقًا اليوم: {{ prorated_charge }}{% endif %}

{% if prorated_charge %}
💡 تم فرض رسوم قدرها {{ prorated_charge }} اليوم على باقي فترة الفاتورة الحالية الخاصة بك.
{% endif %}

عرض اشتراكي: {{ account_url }}
هل لديك أسئلة؟ اتصل بالدعم: {{ support_url }}