---
template_type: booking_recurring_created
category: Bookings
---

# Email Template: booking_recurring_created

## Subject
สร้างชุดการจองซ้ำแล้ว - {{ product_name }}

## HTML Content
<mjml>
  <mj-head>
    <mj-attributes>
      <mj-text font-family="Arial, sans-serif" line-height="1.6" />
      <mj-all font-family="Arial, sans-serif" />
    </mj-attributes>
  </mj-head>
  <mj-body background-color="{{ theme.color.background_secondary|default:'#f9fafb' }}">
    <!-- Header -->
    <mj-section background-color="{{ theme.color.background|default:'#ffffff' }}" padding="30px 20px">
      <mj-column>
        <mj-text font-size="28px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}" align="center">
          สร้างการจองซ้ำแล้ว
        </mj-text>
        <mj-text font-size="16px" color="{{ theme.color.text_muted|default:'#6b7280' }}" align="center" padding-top="10px">
          สวัสดี {{ customer_name }}, ชุดการจองซ้ำของคุณได้ถูกตั้งค่าเรียบร้อยแล้ว
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Series Details -->
    <mj-section background-color="{{ theme.color.background|default:'#ffffff' }}" padding="20px">
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}" padding-bottom="15px">
          {{ product_name }}
        </mj-text>
        {% if recurrence_description %}
        <mj-text font-size="14px" color="{{ theme.color.text|default:'#1f2937' }}">
          <strong>ตาราง:</strong> {{ recurrence_description }}
        </mj-text>
        {% endif %}
        {% if first_date %}
        <mj-text font-size="14px" color="{{ theme.color.text|default:'#1f2937' }}">
          <strong>การจองครั้งแรก:</strong> {{ first_date }}
        </mj-text>
        {% endif %}
        {% if total_bookings %}
        <mj-text font-size="14px" color="{{ theme.color.text|default:'#1f2937' }}">
          <strong>จำนวนการจองทั้งหมด:</strong> {{ total_bookings }}
        </mj-text>
        {% endif %}
        {% if resource_name %}
        <mj-text font-size="14px" color="{{ theme.color.text|default:'#1f2937' }}">
          <strong>ทรัพยากร:</strong> {{ resource_name }}
        </mj-text>
        {% endif %}
        {% if total_cost %}
        <mj-text font-size="14px" color="{{ theme.color.text|default:'#1f2937' }}" padding-top="10px">
          <strong>ค่าใช้จ่ายต่อการจอง:</strong> {{ total_cost }}
        </mj-text>
        {% endif %}
      </mj-column>
    </mj-section>

    <!-- Manage -->
    <mj-section background-color="{{ theme.color.background|default:'#ffffff' }}" padding="10px 20px">
      <mj-column>
        <mj-text font-size="13px" color="{{ theme.color.text_muted|default:'#6b7280' }}" align="center">
          คุณสามารถจัดการการจองแต่ละรายการในชุดนี้ได้จากบัญชีของคุณ
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Support Block -->
    {% include 'email_system/mjml_components/support_block.mjml' %}
  </mj-body>
</mjml>

## Text Content
สร้างการจองซ้ำแล้ว

สวัสดี {{ customer_name }}, ชุดการจองซ้ำของคุณได้ถูกตั้งค่าเรียบร้อยแล้ว

{{ product_name }}

{% if recurrence_description %}ตาราง: {{ recurrence_description }}{% endif %}
{% if first_date %}การจองครั้งแรก: {{ first_date }}{% endif %}
{% if total_bookings %}จำนวนการจองทั้งหมด: {{ total_bookings }}{% endif %}
{% if resource_name %}ทรัพยากร: {{ resource_name }}{% endif %}
{% if total_cost %}ค่าใช้จ่ายต่อการจอง: {{ total_cost }}{% endif %}

คุณสามารถจัดการการจองแต่ละรายการในชุดนี้ได้จากบัญชีของคุณ