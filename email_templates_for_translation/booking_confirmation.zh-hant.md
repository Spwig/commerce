---
template_type: booking_confirmation
category: Bookings
---

# Email Template: booking_confirmation

## Subject
預訂確認 - {{ product_name }} 於 {{ booking_date }}

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
          預訂確認！
        </mj-text>
        <mj-text font-size="16px" color="{{ theme.color.text_muted|default:'#6b7280' }}" align="center" padding-top="10px">
          Hi {{ customer_name }}, 您的預訂已確認。
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
          <strong>日期：</strong> {{ booking_date }}
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text|default:'#1f2937' }}">
          <strong>時間：</strong> {{ booking_time_start }} - {{ booking_time_end }} ({{ duration_display }})
        </mj-text>
        {% if resource_name %}
        <mj-text font-size="14px" color="{{ theme.color.text|default:'#1f2937' }}">
          <strong>資源：</strong> {{ resource_name }}
        </mj-text>
        {% endif %}
        {% if persons_display %}
        <mj-text font-size="14px" color="{{ theme.color.text|default:'#1f2937' }}">
          <strong>旅客：</strong> {{ persons_display }}
        </mj-text>
        {% endif %}
        {% if total_cost %}
        <mj-text font-size="14px" color="{{ theme.color.text|default:'#1f2937' }}" padding-top="10px">
          <strong>總計：</strong> {{ total_cost }}
        </mj-text>
        {% endif %}
        {% if deposit_amount %}
        <mj-text font-size="14px" color="{{ theme.color.text|default:'#1f2937' }}">
          <strong>已付訂金：</strong> {{ deposit_amount }}
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
          需要更改？您可以從您的帳戶 <a href="{{ reschedule_url }}" style="color: {{ theme.color.primary|default:'#2563eb' }};">重新預訂</a> 或 <a href="{{ cancel_url }}" style="color: {{ theme.color.primary|default:'#2563eb' }};">取消</a> 預訂。
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Support Block -->
    {% include 'email_system/mjml_components/support_block.mjml' %}
  </mj-body>
</mjml>

## Text Content
預訂確認！

Hi {{ customer_name }}, 您的預訂已確認。

{{ product_name }}

日期：{{ booking_date }}
時間：{{ booking_time_start }} - {{ booking_time_end }} ({{ duration_display }})
{% if resource_name %}資源：{{ resource_name }}{% endif %}
{% if persons_display %}旅客：{{ persons_display }}{% endif %}
{% if total_cost %}總計：{{ total_cost }}{% endif %}
{% if deposit_amount %}已付訂金：{{ deposit_amount }}{% endif %}

{% if ical_url %}加入日曆：{{ ical_url }}{% endif %}

需要更改？請前往您的帳戶重新預訂或取消。
{{ reschedule_url }}
{{ cancel_url }}