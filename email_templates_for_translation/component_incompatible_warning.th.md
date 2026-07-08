---
template_type: component_incompatible_warning
category: Component Updates
---

# Email Template: component_incompatible_warning

## Subject
⚠️ ปัญหาความเข้ากันได้: {{ component_name }} และ {{ conflicting_component }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#fef3c7">
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="#92400e" align="center">
          ⚠️ คำเตือนด้านความเข้ากันได้
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="18px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          ตรวจพบความขัดแย้งของเวอร์ชัน
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          พบปัญหาความเข้ากันได้ระหว่างส่วนประกอบในร้านค้า Spwig ของคุณ
        </mj-text>

        <mj-spacer height="30px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
              รายละเอียดความขัดแย้ง:
            </mj-text>
            <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>ส่วนประกอบ 1:</strong> {{ component_name }} v{{ component_version }}<br/>
              <strong>ส่วนประกอบ 2:</strong> {{ conflicting_component }} v{{ conflicting_version }}<br/>
              <strong>ตรวจพบ:</strong> {{ detected_at }}
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          ปัญหาความเข้ากันได้:
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}" line-height="1.8">
          {{ incompatibility_description }}
        </mj-text>

        <mj-spacer height="20px" />

        <mj-section background-color="#fee2e2" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="14px" color="#991b1b" font-weight="bold">
              ผลกระทบที่อาจเกิดขึ้น
            </mj-text>
            <mj-text font-size="14px" color="#991b1b" line-height="1.6">
              {{ impact_description }}
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          การกระทำที่แนะนำ:
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}" line-height="1.8">
          {{ recommended_action }}
        </mj-text>

        {% if compatible_versions %}
        <mj-spacer height="30px" />
        <mj-section background-color="#f0fdf4" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="14px" color="#065f46" font-weight="bold">
              เวอร์ชันที่เข้ากันได้
            </mj-text>
            <mj-text font-size="14px" color="#065f46" line-height="1.6">
              {{ compatible_versions }}
            </mj-text>
          </mj-column>
        </mj-section>
        {% endif %}

        <mj-spacer height="30px" />

        {% if update_url %}
        <mj-button href="{{ update_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          แก้ไขความขัดแย้ง
        </mj-button>
        <mj-spacer height="10px" />
        {% endif %}

        <mj-button href="{{ support_url }}" background-color="#6b7280" color="#ffffff" font-size="14px" border-radius="6px" padding="10px 25px">
          ติดต่อฝ่ายสนับสนุน
        </mj-button>

        <mj-spacer height="20px" />

        <mj-text font-size="13px" color="{{ theme.color.text_secondary|default:'#6b7280' }}" align="center">
          ร้านค้าของคุณยังคงทำงานได้ตามปกติ แต่เราขอแนะนำให้คุณแก้ไขความขัดแย้งนี้เร็ว ๆ นี้
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
⚠️ คำเตือนด้านความเข้ากันได้

Version Conflict Detected

พบปัญหาความเข้ากันได้ระหว่างส่วนประกอบในร้านค้า Spwig ของคุณ

CONFLICT DETAILS:
- Component 1: {{ component_name }} v{{ component_version }}
- Component 2: {{ conflicting_component }} v{{ conflicting_version }}
- Detected: {{ detected_at }}

COMPATIBILITY ISSUE:
{{ incompatibility_description }}

POTENTIAL IMPACT:
{{ impact_description }}

RECOMMENDED ACTION:
{{ recommended_action }}

{% if compatible_versions %}COMPATIBLE VERSIONS:
{{ compatible_versions }}{% endif %}

{% if update_url %}Resolve conflict: {{ update_url }}{% endif %}
Contact support: {{ support_url }}

ร้านค้าของคุณยังคงทำงานได้ตามปกติ แต่เราขอแนะนำให้คุณแก้ไขความขัดแย้งนี้เร็ว ๆ นี้