---
template_type: booking_waitlist_notification
category: Bookings
---

# Email Template: booking_waitlist_notification

## Subject
有一个名额空出来了 - {{ product_name }}

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
          有一个名额刚刚空出来了！
        </mj-text>
        <mj-text font-size="16px" color="{{ theme.color.text_muted|default:'#6b7280' }}" align="center" padding-top="10px">
          你好 {{ customer_name }}，你等待预订的名额现在有了一个空位。
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
          <strong>可用日期：</strong> {{ available_date }}
        </mj-text>
        {% endif %}
        {% if resource_name %}
        <mj-text font-size="14px" color="{{ theme.color.text|default:'#1f2937' }}">
          <strong>资源：</strong> {{ resource_name }}
        </mj-text>
        {% endif %}
      </mj-column>
    </mj-section>

    <!-- Urgency Notice -->
    <mj-section background-color="{{ theme.color.info_light|default:'#dbeafe' }}" padding="15px 20px">
      <mj-column>
        <mj-text font-size="14px" color="{{ theme.color.text|default:'#1f2937' }}" align="center">
          赶快行动！这个名额是先到先得的。
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
有一个名额刚刚空出来了！

你好 {{ customer_name }}，你等待预订的名额现在有了一个空位。

{{ product_name }}
{% if available_date %}可用日期：{{ available_date }}{% endif %}
{% if resource_name %}资源：{{ resource_name }}{% endif %}

赶快行动！这个名额是先到先得的。

{% if book_now_url %}立即预订：{{ book_now_url }}{% endif %}