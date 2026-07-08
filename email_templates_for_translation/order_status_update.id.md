---
template_type: order_status_update
category: Core E-commerce
---

# Email Template: order_status_update

## Subject
Pemesanan #{{ order_number }} - Pembaruan Status: {{ new_status_display }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}">
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Pembaruan Status Pemesanan
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text|default:'#6b7280' }}">
          Pemesanan #{{ order_number }}
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Hai {{ customer_name }},
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Status pemesanan <strong>#{{ order_number }}</strong> telah diperbarui.
        </mj-text>

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-size="15px" line-height="1.8" color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>Status Sebelumnya:</strong> {{ old_status_display }}<br/>
              <strong>Status Baru:</strong> {{ new_status_display }}
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="20px" />

        {% if order_url %}
        <mj-button href="{{ order_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          Lihat Detail Pemesanan
        </mj-button>
        {% endif %}
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
Pembaruan Status Pemesanan - Pemesanan #{{ order_number }}

Hai {{ customer_name }},

Status pemesanan #{{ order_number }} telah diperbarui.

Status Sebelumnya: {{ old_status_display }}
Status Baru: {{ new_status_display }}

{% if order_url %}Lihat detail pemesanan: {{ order_url }}{% endif %}