---
template_type: booking_pending_confirmation
category: Bookings
---

# Email Template: booking_pending_confirmation

## Subject
Pemesanan Diterima - {{ product_name }} pada {{ booking_date }}

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
          Pemesanan Diterima
        </mj-text>
        <mj-text font-size="16px" color="{{ theme.color.text_muted|default:'#6b7280' }}" align="center" padding-top="10px">
          Halo {{ customer_name }}, kami telah menerima permintaan pemesanan Anda.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Notice -->
    <mj-section background-color="{{ theme.color.info_light|default:'#dbeafe' }}" padding="15px 20px">
      <mj-column>
        <mj-text font-size="14px" color="{{ theme.color.text|default:'#1f2937' }}" align="center">
          Pemesanan Anda menunggu konfirmasi. Kami akan memberi tahu Anda setelah konfirmasi dilakukan.
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
          <strong>Tanggal:</strong> {{ booking_date }}
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text|default:'#1f2937' }}">
          <strong>Waktu:</strong> {{ booking_time_start }} - {{ booking_time_end }} ({{ duration_display }})
        </mj-text>
        {% if resource_name %}
        <mj-text font-size="14px" color="{{ theme.color.text|default:'#1f2937' }}">
          <strong>Sumber Daya:</strong> {{ resource_name }}
        </mj-text>
        {% endif %}
        {% if persons_display %}
        <mj-text font-size="14px" color="{{ theme.color.text|default:'#1f2937' }}">
          <strong>Tamu:</strong> {{ persons_display }}
        </mj-text>
        {% endif %}
        {% if total_cost %}
        <mj-text font-size="14px" color="{{ theme.color.text|default:'#1f2937' }}" padding-top="10px">
          <strong>Total:</strong> {{ total_cost }}
        </mj-text>
        {% endif %}
      </mj-column>
    </mj-section>

    <!-- Support Block -->
    {% include 'email_system/mjml_components/support_block.mjml' %}
  </mj-body>
</mjml>

## Text Content
Pemesanan Diterima

Halo {{ customer_name }}, kami telah menerima permintaan pemesanan Anda.

Pemesanan Anda menunggu konfirmasi. Kami akan memberi tahu Anda setelah konfirmasi dilakukan.

{{ product_name }}

Tanggal: {{ booking_date }}
Waktu: {{ booking_time_start }} - {{ booking_time_end }} ({{ duration_display }})
{% if resource_name %}Sumber Daya: {{ resource_name }}{% endif %}
{% if persons_display %}Tamu: {{ persons_display }}{% endif %}
{% if total_cost %}Total: {{ total_cost }}{% endif %}