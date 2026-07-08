---
template_type: translation_quality_review_needed
category: Translation Service
---

# Email Template: translation_quality_review_needed

## Subject
⚠️ ตรวจพบการแปลคุณภาพต่ำ: {{ content_type }} - {{ low_quality_count }} รายการต้องตรวจสอบ

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#fef3c7">
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="#92400e" align="center">
          ⚠️ แจ้งเตือนคุณภาพการแปล
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="18px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          แนะนำให้ตรวจสอบ
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}">
          การแปลของคุณเสร็จสมบูรณ์แล้ว แต่มี {{ low_quality_count }} การแปลที่คะแนนต่ำกว่าเกณฑ์คุณภาพ และควรตรวจสอบก่อนเผยแพร่
        </mj-text>

        <mj-spacer height="20px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
              สรุปงาน:
            </mj-text>
            <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>Job ID:</strong> {{ job_id }}<br/>
              <strong>Content Type:</strong> {{ content_type }}<br/>
              <strong>Total Items:</strong> {{ total_items }}<br/>
              <strong>Average Quality:</strong> {{ average_quality }}%<br/>
              <strong>Low Quality:</strong> {{ low_quality_count }} items ({{ low_quality_percentage }}%)
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          การวิเคราะห์คุณภาพ:
        </mj-text>

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="14px" color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>Excellent (95-100%):</strong> {{ excellent_count }} items<br/>
              <strong>Good (85-94%):</strong> {{ good_count }} items<br/>
              <strong>Fair (70-84%):</strong> {{ fair_count }} items<br/>
              <strong>Poor (&lt;70%):</strong> <span style="color: #dc2626; font-weight: bold;">{{ poor_count }} items</span>
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          ปัญหาคุณภาพที่พบบ่อย:
        </mj-text>

        {% for issue in quality_issues %}
        <mj-section background-color="#fef3c7" border-radius="8px" padding="12px">
          <mj-column>
            <mj-text font-size="14px" color="#92400e">
              <strong>{{ issue.type }}:</strong> {{ issue.count }} occurrences
            </mj-text>
          </mj-column>
        </mj-section>
        <mj-spacer height="8px" />
        {% endfor %}

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          การกระทำที่แนะนำ:
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}" line-height="1.8">
          1. ตรวจสอบการแปลที่มีปัญหาในแดชบอร์ดผู้ดูแลระบบ<br/>
          2. แก้ไขการแปลที่มีคุณภาพต่ำด้วยตนเอง<br/>
          3. พิจารณาแปลใหม่สำหรับรายการที่มีคุณภาพต่ำ<br/>
          4. ตีพิมพ์เฉพาะเมื่อการตรวจสอบเสร็จสิ้น
        </mj-text>

        <mj-spacer height="30px" />

        <mj-button href="{{ review_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          ตรวจสอบการแปล
        </mj-button>

        <mj-spacer height="10px" />

        <mj-button href="{{ low_quality_url }}" background-color="#dc2626" color="#ffffff" font-size="14px" border-radius="6px" padding="10px 25px">
          ดูรายการคุณภาพต่ำ
        </mj-button>

        <mj-spacer height="30px" />

        <mj-section background-color="#eff6ff" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="14px" color="#1e40af" line-height="1.6">
              💡 คำแนะนำ: คะแนนคุณภาพต่ำกว่า 85% บ่งบอกถึงปัญหาที่อาจเกิดขึ้นในด้านไวยากรณ์ บริบท หรือความถูกต้อง ขอแนะนำให้ตรวจสอบโดยมนุษย์ก่อนเผยแพร่
            </mj-text>
          </mj-column>
        </mj-section>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
⚠️ แจ้งเตือนคุณภาพการแปล

แนะนำให้ตรวจสอบ

การแปลของคุณเสร็จสมบูรณ์แล้ว แต่มี {{ low_quality_count }} การแปลที่คะแนนต่ำกว่าเกณฑ์คุณภาพ และควรตรวจสอบก่อนเผยแพร่

สรุปงาน:
- Job ID: {{ job_id }}
- Content Type: {{ content_type }}
- Total Items: {{ total_items }}
- Average Quality: {{ average_quality }}%
- Low Quality: {{ low_quality_count }} items ({{ low_quality_percentage }}%)

การวิเคราะห์คุณภาพ:
- Excellent (95-100%): {{ excellent_count }} items
- Good (85-94%): {{ good_count }} items
- Fair (70-84%): {{ fair_count }} items
- Poor (<70%): {{ poor_count }} items

ปัญหาคุณภาพที่พบบ่อย:
{% for issue in quality_issues %}
{{ issue.type }}: {{ issue.count }} occurrences
{% endfor %}

การกระทำที่แนะนำ:
1. ตรวจสอบการแปลที่มีปัญหาในแดชบอร์ดผู้ดูแลระบบ
2. แก้ไขการแปลที่มีคุณภาพต่ำด้วยตนเอง
3. พิจารณาแปลใหม่สำหรับรายการที่มีคุณภาพต่ำ
4. ตีพิมพ์เฉพาะเมื่อการตรวจสอบเสร็จสิ้น

Review translations: {{ review_url }}
View low quality items: {{ low_quality_url }}

💡 คำแนะนำ: คะแนนคุณภาพต่ำกว่า 85% บ่งบอกถึงปัญหาที่อาจเกิดขึ้นในด้านไวยากรณ์ บริบท หรือความถูกต้อง ขอแนะนำให้ตรวจสอบโดยมนุษย์ก่อนเผยแพร่