---
template_type: component_rollback_success
category: Component Updates
---

# Email Template: component_rollback_success

## Subject
✓ {{ component_name }} ถอยกลับไปที่ v{{ previous_version }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#dbeafe">
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="#1e40af" align="center">
          ↩️ การถอยกลับสำเร็จ
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="18px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          คืนค่าส่วนประกอบ
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          {{ component_name }} ได้รับการถอยกลับไปยังเวอร์ชันก่อนหน้าอย่างสำเร็จ
        </mj-text>

        <mj-spacer height="30px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
              รายละเอียดการถอยกลับ:
            </mj-text>
            <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>ส่วนประกอบ:</strong> {{ component_name }}<br/>
              <strong>ถอยกลับจาก:</strong> v{{ failed_version }}<br/>
              <strong>คืนค่าไปที่:</strong> v{{ previous_version }}<br/>
              <strong>เสร็จสิ้น:</strong> {{ completed_at }}<br/>
              <strong>ระยะเวลา:</strong> {{ rollback_duration }}
            </mj-text>
          </mj-column>
        </mj-section>

        {% if rollback_reason %}
        <mj-spacer height="30px" />
        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          เหตุผลในการถอยกลับ:
        </mj-text>
        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}" line-height="1.8">
          {{ rollback_reason }}
        </mj-text>
        {% endif %}

        <mj-spacer height="30px" />

        <mj-section background-color="#f0fdf4" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="14px" color="#065f46" font-weight="bold">
              ✓ สถานะร้านค้า
            </mj-text>
            <mj-text font-size="14px" color="#065f46" line-height="1.6">
              ร้านค้าของคุณตอนนี้กำลังทำงานบนเวอร์ชันที่มั่นคง {{ previous_version }} ฟังก์ชันทั้งหมดควรได้รับการคืนค่าแล้ว
            </mj-text>
          </mj-column>
        </mj-section>

        {% if data_restored %}
        <mj-spacer height="20px" />
        <mj-text font-size="14px" color="{{ theme.color.text_secondary|default:'#6b7280' }}">
          <strong>การคืนค่าข้อมูล:</strong> {{ data_restoration_message }}
        </mj-text>
        {% endif %}

        {% if next_steps %}
        <mj-spacer height="30px" />
        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          ขั้นตอนต่อไป:
        </mj-text>
        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}" line-height="1.8">
          {{ next_steps }}
        </mj-text>
        {% endif %}

        <mj-spacer height="30px" />

        <mj-button href="{{ component_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          ดูรายละเอียดส่วนประกอบ
        </mj-button>

        {% if incident_report_url %}
        <mj-spacer height="10px" />
        <mj-button href="{{ incident_report_url }}" background-color="#6b7280" color="#ffffff" font-size="14px" border-radius="6px" padding="10px 25px">
          ดูรายงานเหตุการณ์
        </mj-button>
        {% endif %}

        <mj-spacer height="20px" />

        <mj-text font-size="13px" color="{{ theme.color.text_secondary|default:'#6b7280' }}" align="center">
          หากคุณยังคงประสบปัญหา กรุณาติดต่อฝ่ายสนับสนุน
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
↩️ การถอยกลับสำเร็จ

คืนค่าส่วนประกอบ

{{ component_name }} ได้รับการถอยกลับไปยังเวอร์ชันก่อนหน้าอย่างสำเร็จ

รายละเอียดการถอยกลับ:
- ส่วนประกอบ: {{ component_name }}
- ถอยกลับจาก: v{{ failed_version }}
- คืนค่าไปที่: v{{ previous_version }}
- เสร็จสิ้น: {{ completed_at }}
- ระยะเวลา: {{ rollback_duration }}

{% if rollback_reason %}
เหตุผลในการถอยกลับ:
{{ rollback_reason }}
{% endif %}

✓ สถานะร้านค้า:
ร้านค้าของคุณตอนนี้กำลังทำงานบนเวอร์ชันที่มั่นคง {{ previous_version }} ฟังก์ชันทั้งหมดควรได้รับการคืนค่าแล้ว

{% if data_restored %}
การคืนค่าข้อมูล: {{ data_restoration_message }}
{% endif %}

{% if next_steps %}
ขั้นตอนต่อไป:
{{ next_steps }}
{% endif %}

ดูรายละเอียดส่วนประกอบ: {{ component_url }}
{% if incident_report_url %}ดูรายงานเหตุการณ์: {{ incident_report_url }}{% endif %}

หากคุณยังคงประสบปัญหา กรุณาติดต่อฝ่ายสนับสนุน