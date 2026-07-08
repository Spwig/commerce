---
template_type: subscription_addon_added
category: Subscriptions
---

# Email Template: subscription_addon_added

## Subject
✓ تم إضافة {{ addon_name }} إلى اشتراكك

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#dcfce7">
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="#065f46" align="center">
          ✓ تم تفعيل الملحق
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          تم إضافة الملحق بنجاح
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Hi {{ customer_name }},
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          تم إضافة {{ addon_name }} إلى اشتراكك في {{ plan_name }} الآن ويعمل بشكل نشط!
        </mj-text>

        <mj-spacer height="30px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
              تفاصيل الملحق:
            </mj-text>
            <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>الملحق:</strong> {{ addon_name }}<br/>
              <strong>الاشتراك:</strong> {{ plan_name }}<br/>
              <strong>تمت الإضافة في:</strong> {{ added_date }}<br/>
              <strong>الحالة:</strong> نشط
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          ما يمكنك الحصول عليه:
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}" line-height="1.8">
          {{ addon_description }}
        </mj-text>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          معلومات الفاتورة:
        </mj-text>

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>سعر الملحق:</strong> {{ addon_price }} / {{ billing_period }}<br/>
              <strong>الخطة الخاصة بك:</strong> {{ plan_price }} / {{ billing_period }}<br/>
              <strong>الإجمالي الجديد:</strong> {{ new_total }} / {{ billing_period }}<br/>
              {% if prorated_charge %}<strong>الرسوم المقدرة اليوم:</strong> {{ prorated_charge }}{% endif %}
            </mj-text>
          </mj-column>
        </mj-section>

        {% if prorated_charge %}
        <mj-spacer height="20px" />
        <mj-section background-color="#eff6ff" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="14px" color="#1e40af" line-height="1.6">
              💡 تم فرض رسوم {{ prorated_charge }} اليوم على باقي فترة الفاتورة الخاصة بك الحالية.
            </mj-text>
          </mj-column>
        </mj-section>
        {% endif %}

        <mj-spacer height="30px" />

        <mj-button href="{{ account_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          عرض اشتراكي
        </mj-button>

        {% if addon_setup_url %}
        <mj-spacer height="10px" />
        <mj-button href="{{ addon_setup_url }}" background-color="#6b7280" color="#ffffff" font-size="14px" border-radius="6px" padding="10px 25px">
          تكوين {{ addon_name }}
        </mj-button>
        {% endif %}
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
✓ تم تفعيل الملحق

تم إضافة الملحق بنجاح

Hi {{ customer_name }},

تم إضافة {{ addon_name }} إلى اشتراكك في {{ plan_name }} الآن ويعمل بشكل نشط!

تفاصيل الملحق:
- الملحق: {{ addon_name }}
- الاشتراك: {{ plan_name }}
- تم إضافته في: {{ added_date }}
- الحالة: نشط

ما يمكنك الحصول عليه:
{{ addon_description }}

معلومات الفاتورة:
- سعر الملحق: {{ addon_price }} / {{ billing_period }}
- خطةك: {{ plan_price }} / {{ billing_period }}
- الإجمالي الجديد: {{ new_total }} / {{ billing_period }}
{% if prorated_charge %}- الرسوم المقدرة اليوم: {{ prorated_charge }}{% endif %}

{% if prorated_charge %}
💡 تم فرض رسوم {{ prorated_charge }} اليوم على باقي فترة الفاتورة الخاصة بك الحالية.
{% endif %}

عرض اشتراكي: {{ account_url }}
{% if addon_setup_url %}تكوين {{ addon_name }}: {{ addon_setup_url }}{% endif %}