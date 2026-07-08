---
template_type: booking_reminder
category: Bookings
---

# Email Template: booking_reminder

## Subject
기억하세요: {{ product_name }} - {{ booking_date }}

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
          예약 알림
        </mj-text>
        <mj-text font-size="16px" color="{{ theme.color.text_muted|default:'#6b7280' }}" align="center" padding-top="10px">
          안녕하세요 {{ customer_name }}, 귀하의 예약에 대한 알림입니다.
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
          <strong>날짜:</strong> {{ booking_date }}
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text|default:'#1f2937' }}">
          <strong>시간:</strong> {{ booking_time_start }} - {{ booking_time_end }} ({{ duration_display }})
        </mj-text>
        {% if resource_name %}
        <mj-text font-size="14px" color="{{ theme.color.text|default:'#1f2937' }}">
          <strong>자원:</strong> {{ resource_name }}
        </mj-text>
        {% endif %}
        {% if persons_display %}
        <mj-text font-size="14px" color="{{ theme.color.text|default:'#1f2937' }}">
          <strong>손님:</strong> {{ persons_display }}
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
          변경이 필요하신가요? 계정에서 <a href="{{ reschedule_url }}" style="color: {{ theme.color.primary|default:'#2563eb' }};">예약을 다시 설정</a>하거나 <a href="{{ cancel_url }}" style="color: {{ theme.color.primary|default:'#2563eb' }};">예약을 취소</a>하실 수 있습니다.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Support Block -->
    {% include 'email_system/mjml_components/support_block.mjml' %}
  </mj-body>
</mjml>

## Text Content
예약 알림

안녕하세요 {{ customer_name }}, 귀하의 예약에 대한 알림입니다.

{{ product_name }}

날짜: {{ booking_date }}
시간: {{ booking_time_start }} - {{ booking_time_end }} ({{ duration_display }})
{% if resource_name %}자원: {{ resource_name }}{% endif %}
{% if persons_display %}손님: {{ persons_display }}{% endif %}

{% if ical_url %}달력에 추가: {{ ical_url }}{% endif %}

변경이 필요하신가요? 계정에서 예약을 다시 설정하거나 예약을 취소하려면 다음 링크를 방문하세요.
{{ reschedule_url }}
{{ cancel_url }}