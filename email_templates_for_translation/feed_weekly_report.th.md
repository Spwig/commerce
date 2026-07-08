---
template_type: feed_weekly_report
category: Product Feeds
---

# Email Template: feed_weekly_report

## Subject
📊 รายงานการจัดส่งผลิตภัณฑ์รายสัปดาห์ - {{ week_range }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#eff6ff">
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="#1e40af" align="center">
          📊 ผลการจัดส่งรายสัปดาห์
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="18px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          สรุปผลการจัดส่ง
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}">
          นี่คือผลการจัดส่งผลิตภัณฑ์ของคุณจาก {{ week_range }}
        </mj-text>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          สถิติโดยรวม:
        </mj-text>

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>รวมการจัดส่ง:</strong> {{ total_feeds }}<br/>
              <strong>การจัดส่งที่เปิดใช้งาน:</strong> {{ active_feeds }}<br/>
              <strong>รวมการซิงค์:</strong> {{ total_syncs }}<br/>
              <strong>การซิงค์ที่สำเร็จ:</strong> {{ successful_syncs }} ({{ success_rate }}%)<br/>
              <strong>การซิงค์ที่ล้มเหลว:</strong> {{ failed_syncs }}
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          ผลการจัดส่งตามแต่ละการจัดส่ง:
        </mj-text>

        {% for feed in feed_stats %}
        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="15px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
              {{ feed.name }}
            </mj-text>
            <mj-text font-size="14px" color="{{ theme.color.text|default:'#4b5563' }}">
              Platform: {{ feed.platform }}<br/>
              Syncs: {{ feed.sync_count }} ({{ feed.success_count }} successful)<br/>
              Products: {{ feed.product_count }}<br/>
              {% if feed.errors > 0 %}Errors: {{ feed.errors }}{% endif %}
            </mj-text>
          </mj-column>
        </mj-section>
        <mj-spacer height="10px" />
        {% endfor %}

        {% if top_errors %}
        <mj-spacer height="30px" />
        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          ปัญหาที่พบบ่อยที่สุด:
        </mj-text>
        {% for error in top_errors %}
        <mj-section background-color="#fef3c7" border-radius="8px" padding="12px">
          <mj-column>
            <mj-text font-size="14px" color="#92400e">
              <strong>{{ error.type }}:</strong> {{ error.count }} occurrences
            </mj-text>
          </mj-column>
        </mj-section>
        <mj-spacer height="8px" />
        {% endfor %}
        {% endif %}

        <mj-spacer height="30px" />

        {% if recommendations %}
        <mj-section background-color="#f0fdf4" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="15px" color="#065f46" font-weight="bold">
              💡 ข้อแนะนำ
            </mj-text>
            <mj-text font-size="14px" color="#065f46" line-height="1.6">
              {{ recommendations }}
            </mj-text>
          </mj-column>
        </mj-section>
        {% endif %}

        <mj-spacer height="30px" />

        <mj-button href="{{ feeds_dashboard_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          ดูแดชบอร์ดการจัดส่ง
        </mj-button>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
📊 ผลการจัดส่งรายสัปดาห์

สรุปผลการจัดส่ง

นี่คือผลการจัดส่งผลิตภัณฑ์ของคุณจาก {{ week_range }}

สถิติโดยรวม:
- รวมการจัดส่ง: {{ total_feeds }}
- การจัดส่งที่เปิดใช้งาน: {{ active_feeds }}
- รวมการซิงค์: {{ total_syncs }}
- การซิงค์ที่สำเร็จ: {{ successful_syncs }} ({{ success_rate }}%)
- การซิงค์ที่ล้มเหลว: {{ failed_syncs }}

ผลการจัดส่งตามแต่ละการจัดส่ง:
{% for feed in feed_stats %}
{{ feed.name }}
Platform: {{ feed.platform }}
Syncs: {{ feed.sync_count }} ({{ feed.success_count }} successful)
Products: {{ feed.product_count }}
{% if feed.errors > 0 %}Errors: {{ feed.errors }}{% endif %}

{% endfor %}

{% if top_errors %}
ปัญหาที่พบบ่อยที่สุด:
{% for error in top_errors %}
{{ error.type }}: {{ error.count }} occurrences
{% endfor %}
{% endif %}

{% if recommendations %}
💡 ข้อแนะนำ:
{{ recommendations }}
{% endif %}

ดูแดชบอร์ดการจัดส่ง: {{ feeds_dashboard_url }}