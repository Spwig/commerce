---
template_type: booking_recurring_created
category: Bookings
---

# Email Template: booking_recurring_created

## Subject
Seri Pemesanan Berulang Dibuat - {{ product_name }}

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
          Pemesanan Berulang Dibuat
        </mj-text>
        <mj-text font-size="16px" color="{{ theme.color.text_muted|default:'#6b7280' }}" align="center" padding-top="10px">
          Halo {{ customer_name }}, seri pemesanan berulang Anda telah dibuat.
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
          <strong>Jadwal:</strong> {{ recurrence_description }}
        </mj-text>
        {% endif %}
        {% if first_date %}
        <mj-text font-size="14px" color="{{ theme.color.text|default:'#1f2937' }}">
          <strong>Pemesanan Pertama:</strong> {{ first_date }}
        </mj-text>
        {% endif %}
        {% if total_bookings %}
        <mj-text font-size="14px" color="{{ theme.color.text|default:'#1f2937' }}">
          <strong>Total Pemesanan:</strong> {{ total_bookings }}
        </mj-text>
        {% endif %}
        {% if resource_name %}
        <mj-text font-size="14px" color="{{ theme.color.text|default:'#1f2937' }}">
          <strong>Sumber Daya:</strong> {{ resource_name }}
        </mj-text>
        {% endif %}
        {% if total_cost %}
        <mj-text font-size="14px" color="{{ theme.color.text|default:'#1f2937' }}" padding-top="10px">
          <strong>Biaya per Pemesanan:</strong> {{ total_cost }}
        </mj-text>
        {% endif %}
      </mj-column>
    </mj-section>

    <!-- Manage -->
    <mj-section background-color="{{ theme.color.background|default:'#ffffff' }}" padding="10px 20px">
      <mj-column>
        <mj-text font-size="13px" color="{{ theme.color.text_muted|default:'#6b7280' }}" align="center">
          Anda dapat mengelola pemesanan individu dalam seri ini dari akun Anda.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Support Block -->
    {% include 'email_system/mjml_components/support_block.mjml' %}
  </mj-body>
</mjml>

## Text Content
Pemesanan Berulang Dibuat

Halo {{ customer_name }}, seri pemesanan berulang Anda telah dibuat.

{{ product_name }}

{% if recurrence_description %}Jadwal: {{ recurrence_description }}{% endif %}
{% if first_date %}Pemesanan Pertama: {{ first_date }}{% endif %}
{% if total_bookings %}Total Pemesanan: {{ total_bookings }}{% endif %}
{% if resource_name %}Sumber Daya: {{ resource_name }}{% endif %}
{% if total_cost %}Biaya per Pemesanan: {{ total_cost }}{% endif %}

Anda dapat mengelola pemesanan individu dalam seri ini dari akun Anda.