---
template_type: translation_job_started
category: Translation Service
---

# Email Template: translation_job_started

## Subject
🌐 งานแปลเริ่มต้นแล้ว: {{ content_type }} ({{ source_language }} → {{ target_languages }})

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#eff6ff">
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="#1e40af" align="center">
          🌐 งานแปลเริ่มต้นแล้ว
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="18px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          งานแปลแบบจำนวนมากกำลังดำเนินการอยู่
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}">
          งานแปลแบบจำนวนมากของคุณได้เริ่มต้นแล้วและกำลังประมวลผลอยู่
        </mj-text>

        <mj-spacer height="20px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
              รายละเอียดงาน:
            </mj-text>
            <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>Job ID:</strong> {{ job_id }}<br/>
              <strong>Content Type:</strong> {{ content_type }}<br/>
              <strong>Source Language:</strong> {{ source_language }}<br/>
              <strong>Target Languages:</strong> {{ target_languages }}<br/>
              <strong>Items to Translate:</strong> {{ item_count }}<br/>
              <strong>Started:</strong> {{ started_at }}
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          ระยะเวลาการดำเนินการที่คาดการณ์:
        </mj-text>

        <mj-section background-color="#f0fdf4" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="15px" color="#065f46" font-weight="bold" align="center">
              {{ estimated_completion }}
            </mj-text>
            <mj-text font-size="14px" color="#065f46" align="center">
              (ตามจำนวน {{ word_count }} คำ)
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          สิ่งที่จะเกิดขึ้นต่อไป:
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}" line-height="1.8">
          1. บริการแปลโดย AI กำลังประมวลผลเนื้อหาของคุณ<br/>
          2. การแปลจะถูกบันทึกเป็นร่างเพื่อให้คุณตรวจสอบ<br/>
          3. คุณจะได้รับอีเมลเมื่องานเสร็จสิ้น<br/>
          4. ตรวจสอบและเผยแพร่การแปลจากแดชบอร์ดผู้ดูแลระบบของคุณ
        </mj-text>

        <mj-spacer height="30px" />

        <mj-button href="{{ job_status_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          ดูสถานะงาน
        </mj-button>

        <mj-spacer height="20px" />

        <mj-text font-size="13px" color="{{ theme.color.text_secondary|default:'#6b7280' }}" align="center">
          คุณสามารถปิดอีเมลนี้ได้ เรากำลังแจ้งให้คุณทราบเมื่อการแปลเสร็จสิ้น
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
🌐 งานแปลเริ่มต้นแล้ว

งานแปลแบบจำนวนมากกำลังดำเนินการอยู่

งานแปลแบบจำนวนมากของคุณได้เริ่มต้นแล้วและกำลังประมวลผลอยู่

รายละเอียดงาน:
- Job ID: {{ job_id }}
- Content Type: {{ content_type }}
- Source Language: {{ source_language }}
- Target Languages: {{ target_languages }}
- Items to Translate: {{ item_count }}
- Started: {{ started_at }}

ระยะเวลาการดำเนินการที่คาดการณ์:
{{ estimated_completion }}
(ตามจำนวน {{ word_count }} คำ)

สิ่งที่จะเกิดขึ้นต่อไป:
1. AI translation service processes your content
2. Translations are saved as drafts for review
3. You'll receive an email when the job is complete
4. Review and publish translations from your admin panel

View job status: {{ job_status_url }}

You can close this email. We'll notify you when the translation is complete.