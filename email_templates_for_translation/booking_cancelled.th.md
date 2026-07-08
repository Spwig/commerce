---
template_type: booking_cancelled
category: Bookings
---

# Email Template: booking_cancelled

## Subject
การจองถูกยกเลิก - {{ product_name }}

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
          การจองถูกยกเลิก
        </mj-text>
        <mj-text font-size="16px" color="{{ theme.color.text_muted|default:'#6b7280' }}" align="center" padding-top="10px">
          สวัสดี {{ customer_name }}, การจองของคุณถูกยกเลิกแล้ว
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
          <strong>เวลา:</strong> {{ booking_time_start }} - {{ booking_time_end }}
        </mj-text>
        {% if cancellation_reason %}
        <mj-text font-size="14px" color="{{ theme.color.text|default:'#1f2937' }}" padding-top="10px">
          <strong>เหตุผล:</strong> {{ cancellation_reason }}
        </mj-text>
        {% endif %}
      </mj-column>
    </mj-section>

    <!-- Rebook CTA -->
    <mj-section background-color="{{ theme.color.background|default:'#ffffff' }}" padding="10px 20px">
      <mj-column>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}" align="center">
          คุณต้องการจองอีกครั้งหรือไม่? โปรดเข้าเว็บไซต์ของเราเพื่อทำการนัดหมายใหม่
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Support Block -->
    {% include 'email_system/mjml_components/support_block.mjml' %}
  </mj-body>
</mjml>

## Text Content
การจองถูกยกเลิก

สวัสดี {{ customer_name }}, การจองของคุณถูกยกเลิกแล้ว

{{ product_name }}

วันที่: {{ booking_date }}
เวลา: {{ booking_time_start }} - {{ booking_time_end }}
{% if cancellation_reason %}เหตุผล: {{ cancellation_reason }}{% endif %}

คุณต้องการจองอีกครั้งหรือไม่? โปรดเข้าเว็บไซต์ของเราเพื่อทำการนัดหมายใหม่