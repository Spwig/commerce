---
template_type: loyalty_tier_demotion_warning
category: Loyalty Program
---

# Email Template: loyalty_tier_demotion_warning

## Subject
⚠️ سيتم انتهاء صلاحية مستوى {{ current_tier }} قريبًا - {{ shop_name }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#fef3c7">
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="#92400e" align="center">
          ⚠️ انتهاء صلاحية مستوى الترقية
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          لا تفقد فوائد مستوى {{ current_tier }}!
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          مرحبًا {{ customer_name }},
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          سيتم انتهاء صلاحية مستوى {{ current_tier }} الخاص بك في {{ expiry_date }} ما لم تواصل الحفاظ على مستوى نشاطك.
        </mj-text>

        <mj-spacer height="30px" />

        <mj-section background-color="#fee2e2" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="#991b1b">
              الحالة الحالية:
            </mj-text>
            <mj-text color="#7f1d1d">
              <strong>الدرجة الحالية:</strong> {{ current_tier }}<br/>
              <strong>تنتهي الصلاحية في:</strong> {{ expiry_date }} ({{ days_remaining }} يومًا)<br/>
              <strong>الدرجة التالية:</strong> {{ next_tier }}
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          كيفية الحفاظ على مستوى {{ current_tier }}:
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}" line-height="1.8">
          تحتاج إلى {{ requirement_type }} قبل {{ expiry_date }}:
        </mj-text>

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-size="18px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}" align="center">
              {{ requirement_description }}
            </mj-text>
            <mj-text font-size="14px" color="{{ theme.color.text_secondary|default:'#6b7280' }}" align="center">
              الحالي: {{ current_progress }} | المطلوب: {{ required_amount }}
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          الفوائد التي ستخسرها:
        </mj-text>

        <mj-text font-size="14px" color="{{ theme.color.text|default:'#4b5563' }}" line-height="1.8">
          {% for benefit in tier_benefits %}
          • {{ benefit }}<br/>
          {% endfor %}
        </mj-text>

        <mj-spacer height="30px" />

        <mj-button href="{{ shop_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          اشopper الآن واحتفظ بمستواك
        </mj-button>

        <mj-spacer height="20px" />

        <mj-button href="{{ loyalty_dashboard_url }}" background-color="#6b7280" color="#ffffff" font-size="14px" border-radius="6px" padding="10px 25px">
          عرض التفاصيل الكاملة
        </mj-button>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
⚠️ انتهاء صلاحية مستوى الترقية

لا تفقد فوائد مستوى {{ current_tier }}!

مرحبًا {{ customer_name }},

سيتم انتهاء صلاحية مستوى {{ current_tier }} الخاص بك في {{ expiry_date }} ما لم تواصل الحفاظ على مستوى نشاطك.

الحالة الحالية:
- الدرجة الحالية: {{ current_tier }}
- تنتهي الصلاحية في: {{ expiry_date }} ({{ days_remaining }} يومًا)
- الدرجة التالية: {{ next_tier }}

كيفية الحفاظ على مستوى {{ current_tier }}:
تحتاج إلى {{ requirement_type }} قبل {{ expiry_date }}:

{{ requirement_description }}
الحالي: {{ current_progress }} | المطلوب: {{ required_amount }}

الفوائد التي ستخسرها:
{% for benefit in tier_benefits %}
• {{ benefit }}
{% endfor %}

اشopper الآن واحتفظ بمستواك: {{ shop_url }}
عرض التفاصيل الكاملة: {{ loyalty_dashboard_url }}