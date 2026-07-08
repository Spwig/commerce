---
template_type: component_update_available
category: Component Updates
---

# Email Template: component_update_available

## Subject
تحديث متوفر: {{ component_name }} v{{ new_version }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#eff6ff">
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="#1e40af" align="center">
          📦 تحديث متوفر
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="18px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          إصدار جديد متوفر
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}">
          هناك إصدار جديد من {{ component_name }} متوفر لمحفظتك على Spwig.
        </mj-text>

        <mj-spacer height="20px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
              تفاصيل التحديث:
            </mj-text>
            <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>المكون:</strong> {{ component_name }}<br/>
              <strong>الإصدار الحالي:</strong> {{ current_version }}<br/>
              <strong>الإصدار الجديد:</strong> {{ new_version }}<br/>
              <strong>تاريخ الإصدار:</strong> {{ release_date }}
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          ما الجديد:
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}" line-height="1.8">
          {{ changelog }}
        </mj-text>

        {% if breaking_changes %}
        <mj-spacer height="20px" />
        <mj-section background-color="#fef3c7" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="14px" color="#92400e" font-weight="bold">
              ⚠️ تغييرات كسرية
            </mj-text>
            <mj-text font-size="14px" color="#92400e" line-height="1.6">
              {{ breaking_changes }}
            </mj-text>
          </mj-column>
        </mj-section>
        {% endif %}

        <mj-spacer height="30px" />

        <mj-button href="{{ update_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          تثبيت التحديث
        </mj-button>

        <mj-spacer height="20px" />

        <mj-text font-size="14px" color="{{ theme.color.text_secondary|default:'#6b7280' }}" align="center">
          <a href="{{ changelog_url }}" style="color: {{ theme.color.primary|default:'#2563eb' }};">
            عرض سجل التغييرات الكامل
          </a>
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
📦 تحديث متوفر

إصدار جديد متوفر

هناك إصدار جديد من {{ component_name }} متوفر لمحفظتك على Spwig.

تفاصيل التحديث:
- المكون: {{ component_name }}
- الإصدار الحالي: {{ current_version }}
- الإصدار الجديد: {{ new_version }}
- تاريخ الإصدار: {{ release_date }}

ما الجديد:
{{ changelog }}

{% if breaking_changes %}
⚠️ تغييرات كسرية:
{{ breaking_changes }}
{% endif %}

تثبيت التحديث: {{ update_url }}
عرض سجل التغييرات الكامل: {{ changelog_url }}