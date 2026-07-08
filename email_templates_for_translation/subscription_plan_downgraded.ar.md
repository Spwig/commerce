---
template_type: subscription_plan_downgraded
category: Subscriptions
---

# Email Template: subscription_plan_downgraded

## Subject
لقد تم تغيير خطة الاشتراك الخاصة بك إلى {{ new_plan_name }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#eff6ff">
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="#1e40af" align="center">
          تم تغيير الخطة
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          تم تحديث خطة الاشتراك
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          مرحباً {{ customer_name }},
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          لقد تم تغيير خطة الاشتراك الخاصة بك إلى {{ new_plan_name }}.
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
              <strong>تم التغيير في:</strong> {{ downgrade_date }}<br/>
              <strong>ساري المفعول:</strong> {{ effective_date }}
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          ما هي التغييرات:
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}" line-height="1.8">
          {{ plan_changes }}
        </mj-text>

        {% if features_lost %}
        <mj-spacer height="20px" />
        <mj-section background-color="#fef3c7" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="14px" color="#92400e" font-weight="bold">
              الميزات غير المتاحة الآن:
            </mj-text>
            <mj-text font-size="14px" color="#92400e" line-height="1.6">
              {{ features_lost }}
            </mj-text>
          </mj-column>
        </mj-section>
        {% endif %}

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          معلومات الفاتورة:
        </mj-text>

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>السعر الجديد:</strong> {{ new_price }} / {{ billing_period }}<br/>
              <strong>تاريخ السريان:</strong> {{ effective_date }}<br/>
              <strong>تاريخ الفاتورة القادم:</strong> {{ next_billing_date }}
            </mj-text>
          </mj-column>
        </mj-section>

        {% if credit_applied %}
        <mj-spacer height="20px" />
        <mj-section background-color="#f0fdf4" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="14px" color="#065f46" line-height="1.6">
              💰 تم تطبيق رصيد قدره {{ credit_amount }} على حسابك مقابل الجزء غير المستخدم من خطةك السابقة.
            </mj-text>
          </mj-column>
        </mj-section>
        {% endif %}

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}" align="center">
          هل غيرت رأيك؟
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color_secondary|default:'#6b7280' }}" align="center">
          يمكنك الترقية مرة أخرى إلى {{ old_plan_name }} في أي وقت.
        </mj-text>

        <mj-spacer height="20px" />

        <mj-button href="{{ upgrade_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          الترقية إلى خطة
        </mj-button>

        <mj-spacer height="10px" />

        <mj-button href="{{ account_url }}" background-color="#6b7280" color="#ffffff" font-size="14px" border-radius="6px" padding="10px 25px">
          عرض اشتراكيتي
        </mj-button>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
تم تغيير الخطة

تم تحديث خطة الاشتراك

مرحباً {{ customer_name }},

لقد تم تغيير خطة الاشتراك الخاصة بك إلى {{ new_plan_name }}.

تفاصيل تغيير الخطة:
- الخطة السابقة: {{ old_plan_name }}
- الخطة الجديدة: {{ new_plan_name }}
- تم التغيير في: {{ downgrade_date }}
- ساري المفعول: {{ effective_date }}

ما هي التغييرات:
{{ plan_changes }}

{% if features_lost %}
الميزات غير المتاحة الآن:
{{ features_lost }}
{% endif %}

معلومات الفاتورة:
- السعر الجديد: {{ new_price }} / {{ billing_period }}
- تاريخ السريان: {{ effective_date }}
- تاريخ الفاتورة القادم: {{ next_billing_date }}

{% if credit_applied %}
💰 تم تطبيق رصيد قدره {{ credit_amount }} على حسابك مقابل الجزء غير المستخدم من خطةك السابقة.
{% endif %}

هل غيرت رأيك؟
يمكنك الترقية مرة أخرى إلى {{ old_plan_name }} في أي وقت.

ترقية الخطة: {{ upgrade_url }}
عرض اشتراكيتي: {{ account_url }}