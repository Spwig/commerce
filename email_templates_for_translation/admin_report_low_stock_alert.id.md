---
template_type: admin_report_low_stock_alert
category: Admin Reports
---

# Email Template: admin_report_low_stock_alert

## Subject
📦 Peringatan Stok Rendah - {{ product_count }} produk memerlukan pemesanan ulang

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#fef3c7">
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="#92400e" align="center">
          📦 Peringatan Stok Rendah
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="18px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Pemesanan Ulang Diperlukan
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}">
          {{ product_count }} produk berada di bawah titik pemesanan ulang.
        </mj-text>

        <mj-spacer height="20px" />

        {% for item in low_stock_items %}
        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="15px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
              {{ item.product_name }}
            </mj-text>
            <mj-text font-size="14px" color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>Stok:</strong> <span style="color: #dc2626;">{{ item.current_stock }}</span> / Pemesanan ulang di: {{ item.reorder_point }}<br/>
              <strong>SKU:</strong> {{ item.sku }}
            </mj-text>
          </mj-column>
        </mj-section>
        <mj-spacer height="10px" />
        {% endfor %}

        <mj-spacer height="20px" />

        <mj-button href="{{ inventory_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          Lihat Stok
        </mj-button>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
📦 PERINGATAN STOK RENDAH

Pemesanan Ulang Diperlukan

{{ product_count }} produk berada di bawah titik pemesanan ulang.

PRODUK STOK RENDAH:
{% for item in low_stock_items %}
{{ item.product_name }}
Stok: {{ item.current_stock }} / Pemesanan ulang di: {{ item.reorder_point }}
SKU: {{ item.sku }}

{% endfor %}

Lihat stok: {{ inventory_url }}