---
template_type: booking_cancelled
category: Bookings
---

# Email Template: booking_cancelled

## Subject
Pemesanan Dibatalkan - {{ product_name }}

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
          Pemesanan Dibatalkan
        </mj-text>
        <mj-text font-size="16px" color="{{ theme.color.text_muted|default:'#6b7280' }}" align="center" padding-top="10px">
          Hai {{ customer_name }}, pemesanan Anda telah dibatalkan.
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
          <strong>Waktu:</strong> {{ booking_time_start }} - {{ booking_time_end }}
        </mj-text>
        {% if cancellation_reason %}
        <mj-text font-size="14px" color="{{ theme.color.text|default:'#1f2937' }}" padding-top="10px">
          <strong>Alasan:</strong> {{ cancellation_reason }}
        </mj-text>
        {% endif %}
      </mj-column>
    </mj-section>

    <!-- Rebook CTA -->
    <mj-section background-color="{{ theme.color.background|default:'#ffffff' }}" padding="10px 20px">
      <mj-column>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}" align="center">
          Apakah Anda ingin memesan kembali? Kunjungi situs web kami untuk menjadwalkan janji temu baru.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Support Block -->
    {% include 'email_system/mjml_components/support_block.mjml' %}
  </mj-body>
</mjml>

## Text Content
Pemesanan Dibatalkan

Hai {{ customer_name }}, pemesanan Anda telah dibatalkan.

{{ product_name }}
Tanggal: {{ booking_date }}
Waktu: {{ booking_time_start }} - {{ booking_time_end }}
{% if cancellation_reason %}Alasan: {{ cancellation_reason }}{% endif %}

Apakah Anda ingin memesan kembali? Kunjungi situs web kami untuk menjadwalkan janji temu baru.