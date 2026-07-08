---
template_type: component_update_available
category: Component Updates
---

# Email Template: component_update_available

## Subject
มีการอัปเดต: {{ component_name }} v{{ new_version }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#eff6ff">
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="#1e40af" align="center">
          📦 มีการอัปเดต
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="18px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          มีเวอร์ชันใหม่ให้อัปเดต
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}">
          มีเวอร์ชันใหม่ของ {{ component_name }} สำหรับร้านค้า Spwig ของคุณ
        </mj-text>

        <mj-spacer height="20px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
              รายละเอียดการอัปเดต:
            </mj-text>
            <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>Component:</strong> {{ component_name }}<br/>
              <strong>Current Version:</strong> {{ current_version }}<br/>
              <strong>New Version:</strong> {{ new_version }}<br/>
              <strong>Release Date:</strong> {{ release_date }}
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          อะไรใหม่:
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}" line-height="1.8">
          {{ changelog }}
        </mj-text>

        {% if breaking_changes %}
        <mj-spacer height="20px" />
        <mj-section background-color="#fef3c7" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="14px" color="#92400e" font-weight="bold">
              ⚠️ การเปลี่ยนแปลงที่กระทบการทำงาน
            </mj-text>
            <mj-text font-size="14px" color="#92400e" line-height="1.6">
              {{ breaking_changes }}
            </mj-text>
          </mj-column>
        </mj-section>
        {% endif %}

        <mj-spacer height="30px" />

        <mj-button href="{{ update_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          ติดตั้งการอัปเดต
        </mj-button>

        <mj-spacer height="20px" />

        <mj-text font-size="14px" color="{{ theme.color.text_secondary|default:'#6b7280' }}" align="center">
          <a href="{{ changelog_url }}" style="color: {{ theme.color.primary|default:'#2563eb' }};">
            ดูรายละเอียดการเปลี่ยนแปลงทั้งหมด
          </a>
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
📦 มีการอัปเดต

มีเวอร์ชันใหม่ให้อัปเดต

มีเวอร์ชันใหม่ของ {{ component_name }} สำหรับร้านค้า Spwig ของคุณ

รายละเอียดการอัปเดต:
- Component: {{ component_name }}
- Current Version: {{ current_version }}
- New Version: {{ new_version }}
- Release Date: {{ release_date }}

WHAT'S NEW:
{{ changelog }}

{% if breaking_changes %}
⚠️ BREAKING CHANGES:
{{ breaking_changes }}
{% endif %}

Install update: {{ update_url }}
View full changelog: {{ changelog_url }}