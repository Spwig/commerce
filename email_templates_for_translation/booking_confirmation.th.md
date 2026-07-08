---
template_type: booking_confirmation
category: Bookings
---

# Email Template: booking_confirmation

## Subject
ยืนยันการจอง - {{ product_name }} เมื่อวันที่ {{ booking_date }}

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
          ยืนยันการจอง!
        </mj-text>
        <mj-text font-size="16px" color="{{ theme.color.text_muted|default:'#6b7280' }}" align="center" padding-top="10px">
          สวัสดี {{ customer_name }}, การจองของคุณได้รับการยืนยันแล้ว。
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Booking Details -->
    <mj-section background-color="{{ theme.color.background|default:'#ffffff' }}" padding="20px">
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}" padding-bottom="15px">
          {{ product_name }}
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text|default:'#1f2937' }}">
          <strong>วันที่:</strong> {{ booking_date }}
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text|default:'#1f2937' }}">
          <strong>เวลา:</strong> {{ booking_time_start }} - {{ booking_time_end }} ({{ duration_display }})
        </mj-text>
        {% if resource_name %}
        <mj-text font-size="14px" color="{{ theme.color.text|default:'#1f2937' }}">
          <strong>ทรัพยากร:</strong> {{ resource_name }}
        </mj-text>
        {% endif %}
        {% if persons_display %}
        <mj-text font-size="14px" color="{{ theme.color.text|default:'#1f2937' }}">
          <strong>ผู้เข้าพัก:</strong> {{ persons_display }}
        </mj-text>
        {% endif %}
        {% if total_cost %}
        <mj-text font-size="14px" color="{{ theme.color.text|default:'#1f2937' }}" padding-top="10px">
          <strong>รวม:</strong> {{ total_cost }}
        </mj-text>
        {% endif %}
        {% if deposit_amount %}
        <mj-text font-size="14px" color="{{ theme.color.text|default:'#1f2937' }}">
          <strong>ค่ามัดจำที่จ่ายแล้ว:</strong> {{ deposit_amount }}
        </mj-text>
        {% endif %}
      </mj-column>
    </mj-section>

    <!-- Add to Calendar -->
    {% if ical_url %}
    {% include 'email_system/mjml_components/cta_button.mjml' with url=ical_url text="Add to Calendar" %}
    {% endif %}

    <!-- Manage Booking -->
    <mj-section background-color="{{ theme.color.background|default:'#ffffff' }}" padding="10px 20px">
      <mj-column>
        <mj-text font-size="13px" color="{{ theme.color.text_muted|default:'#6b7280' }}" align="center">
          ต้องการเปลี่ยนแปลง? คุณสามารถ <a href="{{ reschedule_url }}" style="color: {{ theme.color.primary|default:'#2563eb' }};">จัดตารางใหม่</a> หรือ <a href="{{ cancel_url }}" style="color: {{ theme.color.primary|default:'#2563eb' }};">ยกเลิก</a> การจองของคุณได้จากบัญชีของคุณ。
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Support Block -->
    {% include 'email_system/mjml_components/support_block.mjml' %}
  </mj-body>
</mjml>

## Text Content
ยืนยันการจอง!

สวัสดี {{ customer_name }}, การจองของคุณได้รับการยืนยันแล้ว。

{{ product_name }}

วันที่: {{ booking_date }}
เวลา: {{ booking_time_start }} - {{ booking_time_end }} ({{ duration_display }})
{% if resource_name %}ทรัพยากร: {{ resource_name }}{% endif %}
{% if persons_display %}ผู้เข้าพัก: {{ persons_display }}{% endif %}
{% if total_cost %}รวม: {{ total_cost }}{% endif %}
{% if deposit_amount %}ค่ามัดจำที่จ่ายแล้ว: {{ deposit_amount }}{% endif %}

{% if ical_url %}เพิ่มลงในปฏิทิน: {{ ical_url }}{% endif %}

ต้องการเปลี่ยนแปลง? ไปที่บัญชีของคุณเพื่อจัดตารางใหม่หรือยกเลิก。
{{ reschedule_url }}
{{ cancel_url }}