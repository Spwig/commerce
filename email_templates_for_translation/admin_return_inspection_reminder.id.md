---
template_type: admin_return_inspection_reminder
category: Admin Notifications
---

# Email Template: admin_return_inspection_reminder

## Subject
Pengembalian Diterima - Pemeriksaan Diperlukan untuk Pesanan #{{ order_number }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}">
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Pemeriksaan Pengembalian Diperlukan
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Paket pengembalian telah diterima dan memerlukan pemeriksaan.
        </mj-text>

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-size="15px" line-height="1.8" color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>Pesanan:</strong> #{{ order_number }}<br/>
              <strong>Diterima:</strong> {{ received_at }}<br/>
              <strong>Barang yang Perlu Diperiksa:</strong> {{ items_count }}
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="20px" />

        {% if admin_url %}
        <mj-button href="{{ admin_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          Lihat Pengembalian di Admin
        </mj-button>
        {% endif %}
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
Pemeriksaan Pengembalian Diperlukan

Paket pengembalian telah diterima dan memerlukan pemeriksaan.

Pesanan: #{{ order_number }}
Diterima: {{ received_at }}
Barang yang Perlu Diperiksa: {{ items_count }}

{% if admin_url %}Lihat di admin: {{ admin_url }}{% endif %}