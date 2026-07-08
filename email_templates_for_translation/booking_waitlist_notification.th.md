---
template_type: booking_waitlist_notification
category: Bookings
---

# Email Template: booking_waitlist_notification

## Subject
มีที่ว่างแล้ว - {{ product_name }}

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
          มีที่ว่างเพิ่มขึ้นแล้ว!
        </mj-text>
        <mj-text font-size="16px" color="{{ theme.color.text_muted|default:'#6b7280' }}" align="center" padding-top="10px">
          สวัสดี {{ customer_name }}, มีที่ว่างสำหรับการจองที่คุณเคยต่อคิวรอไว้
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Booking Details -->
    <mj-section background-color="{{ theme.color.background|default:'#ffffff' }}" padding="20px">
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}" padding-bottom="15px">
          {{ product_name }}
        </mj-text>
        {% if available_date %}
        <mj-text font-size="14px" color="{{ theme.color.text|default:'#1f2937' }}">
          <strong>วันที่สามารถจองได้:</strong> {{ available_date }}
        </mj-text>
        {% endif %}
        {% if resource_name %}
        <mj-text font-size="14px" color="{{ theme.color.text|default:'#1f2937' }}">
          <strong>ทรัพยากร:</strong> {{ resource_name }}
        </mj-text>
        {% endif %}
      </mj-column>
    </mj-section>

    <!-- Urgency Notice -->
    <mj-section background-color="{{ theme.color.info_light|default:'#dbeafe' }}" padding="15px 20px">
      <mj-column>
        <mj-text font-size="14px" color="{{ theme.color.text|default:'#1f2937' }}" align="center">
          ดำเนินการเร็วๆ นะ! ที่ว่างนี้มีให้จองตามลำดับก่อนหลัง
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Book Now CTA -->
    {% if book_now_url %}
    {% include 'email_system/mjml_components/cta_button.mjml' with url=book_now_url text="Book Now" %}
    {% endif %}

    <!-- Support Block -->
    {% include 'email_system/mjml_components/support_block.mjml' %}
  </mj-body>
</mjml>

## Text Content
มีที่ว่างเพิ่มขึ้นแล้ว!

สวัสดี {{ customer_name }}, มีที่ว่างสำหรับการจองที่คุณเคยต่อคิวรอไว้

{{ product_name }}
{% if available_date %}วันที่สามารถจองได้: {{ available_date }}{% endif %}
{% if resource_name %}ทรัพยากร: {{ resource_name }}{% endif %}

ดำเนินการเร็วๆ นะ! ที่ว่างนี้มีให้จองตามลำดับก่อนหลัง

{% if book_now_url %}Book Now: {{ book_now_url }}{% endif %}