---
template_type: translation_job_completed
category: Translation Service
---

# Email Template: translation_job_completed

## Subject
✓ การแปลเสร็จสิ้นแล้ว: {{ content_type }} ({{ language_count }} ภาษา)

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#dcfce7">
      <mj-column>
        <mj-text font-size="24px" font-weight="bold" color="#065f46" align="center">
          ✓ การแปลเสร็จสิ้นแล้ว!
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          การแปลของคุณพร้อมใช้งานแล้ว
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          ข่าวดี! งานแปลจำนวนมากของคุณเสร็จสมบูรณ์แล้ว
        </mj-text>

        <mj-spacer height="30px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
              สรุปงาน:
            </mj-text>
            <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>Job ID:</strong> {{ job_id }}<br/>
              <strong>Content Type:</strong> {{ content_type }}<br/>
              <strong>Languages:</strong> {{ target_languages }}<br/>
              <strong>Items Translated:</strong> {{ items_translated }}<br/>
              <strong>Total Words:</strong> {{ word_count }}<br/>
              <strong>Completed:</strong> {{ completed_at }}<br/>
              <strong>Duration:</strong> {{ job_duration }}
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          คุณภาพของการแปล:
        </mj-text>

        <mj-section background-color="#f0fdf4" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="15px" color="#065f46">
              <strong>Average Quality Score:</strong> {{ quality_score }}%<br/>
              <strong>High Quality:</strong> {{ high_quality_count }} items<br/>
              <strong>Review Recommended:</strong> {{ review_needed_count }} items
            </mj-text>
          </mj-column>
        </mj-section>

        {% if review_needed_count > 0 %}
        <mj-spacer height="20px" />
        <mj-section background-color="#fef3c7" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="14px" color="#92400e" font-weight="bold">
              ⚠️ แนะนำให้ตรวจสอบ
            </mj-text>
            <mj-text font-size="14px" color="#92400e" line-height="1.6">
              {{ review_needed_count }} การแปลได้คะแนนต่ำกว่า 85% และควรตรวจสอบก่อนเผยแพร่
            </mj-text>
          </mj-column>
        </mj-section>
        {% endif %}

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          ขั้นตอนต่อไป:
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}" line-height="1.8">
          1. ตรวจสอบการแปลในแดชบอร์ดผู้ดูแลระบบของคุณ<br/>
          2. แก้ไขการแปลใด ๆ ที่ต้องการปรับปรุง<br/>
          3. เผยแพร่การแปลเพื่อให้เป็นที่ใช้งานได้<br/>
          4. ข้อมูลหลายภาษาของคุณจะพร้อมให้ลูกค้าใช้งาน
        </mj-text>

        <mj-spacer height="30px" />

        <mj-button href="{{ review_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          ตรวจสอบการแปล
        </mj-button>

        {% if can_publish_all %}
        <mj-spacer height="10px" />
        <mj-button href="{{ publish_all_url }}" background-color="#059669" color="#ffffff" font-size="14px" border-radius="6px" padding="10px 25px">
          เผยแพร่ทั้งหมด
        </mj-button>
        {% endif %}
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
✓ การแปลเสร็จสิ้นแล้ว!

การแปลของคุณพร้อมใช้งานแล้ว

ข่าวดี! งานแปลจำนวนมากของคุณเสร็จสมบูรณ์แล้ว

สรุปงาน:
- Job ID: {{ job_id }}
- Content Type: {{ content_type }}
- Languages: {{ target_languages }}
- Items Translated: {{ items_translated }}
- Total Words: {{ word_count }}
- Completed: {{ completed_at }}
- Duration: {{ job_duration }}

คุณภาพของการแปล:
- Average Quality Score: {{ quality_score }}%
- High Quality: {{ high_quality_count }} items
- Review Recommended: {{ review_needed_count }} items

{% if review_needed_count > 0 %}
⚠️ REVIEW RECOMMENDED:
{{ review_needed_count }} การแปลได้คะแนนต่ำกว่า 85% และควรตรวจสอบก่อนเผยแพร่
{% endif %}

NEXT STEPS:
1. ตรวจสอบการแปลในแดชบอร์ดผู้ดูแลระบบของคุณ
2. แก้ไขการแปลใด ๆ ที่ต้องการปรับปรุง
3. เผยแพร่การแปลเพื่อให้เป็นที่ใช้งานได้
4. ข้อมูลหลายภาษาของคุณจะพร้อมให้ลูกค้าใช้งาน

Review translations: {{ review_url }}
{% if can_publish_all %}Publish all: {{ publish_all_url }}{% endif %}