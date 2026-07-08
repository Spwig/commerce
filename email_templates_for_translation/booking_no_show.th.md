---
template_type: booking_no_show
category: Bookings
---

# Email Template: booking_no_show

## Subject
การจองที่พลาดไป - {{ product_name }}

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
          เราพลาดคุณไป
        </mj-text>
        <mj-text font-size="16px" color="{{ theme.color.text_muted|default:'#6b7280' }}" align="center" padding-top="10px">
          สวัสดี {{ customer_name }}, ดูเหมือนคุณพลาดการจองของคุณ
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
          <strong>Date:</strong> {{ booking_date }}
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text|default:'#1f2937' }}">
          <strong>Time:</strong> {{ booking_time_start }} - {{ booking_time_end }}
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Rebook -->
    <mj-section background-color="{{ theme.color.background|default:'#ffffff' }}" padding="10px 20px">
      <mj-column>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}" align="center">
          คุณต้องการจองใหม่หรือไม่? โปรดเข้าเว็บไซต์ของเราเพื่อทำการจองนัดหมายใหม่ในเวลาที่สะดวกสำหรับคุณ
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Support Block -->
    {% include 'email_system/mjml_components/support_block.mjml' %}
  </mj-body>
</mjml>

## Text Content
เราพลาดคุณไป

สวัสดี {{ customer_name }}, ดูเหมือนคุณพลาดการจองของคุณ

{{ product_name }}

Date: {{ booking_date }}
Time: {{ booking_time_start }} - {{ booking_time_end }}

คุณต้องการจองใหม่หรือไม่? โปรดเข้าเว็บไซต์ของเราเพื่อทำการจองนัดหมายใหม่ในเวลาที่สะดวกสำหรับคุณ