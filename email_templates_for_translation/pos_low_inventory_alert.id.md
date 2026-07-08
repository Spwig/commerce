---
template_type: pos_low_inventory_alert
category: POS
---

# Email Template: pos_low_inventory_alert

## Subject
📦 Peringatan Persediaan Rendah: {{ product_count }} produk{{ product_count|pluralize }} sedang habis di {{ location_name }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#fef3c7">
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="#92400e" align="center">
          📦 Peringatan Persediaan Rendah
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="18px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Persediaan Sedang Rendah
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}">
          {{ product_count }} produk{{ product_count|pluralize }} {{ product_count|pluralize:'is,are' }} sedang habis di {{ location_name }}.
        </mj-text>

        <mj-spacer height="20px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
              Detail Peringatan:
            </mj-text>
            <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>Lokasi:</strong> {{ location_name }}<br/>
              <strong>Produk yang Terkena Dampak:</strong> {{ product_count }}<br/>
              <strong>Detected:</strong> {{ detected_at }}
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Barang dengan Persediaan Rendah:
        </mj-text>

        {% for item in low_stock_items %}
        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="15px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
              {{ item.product_name }}
            </mj-text>
            <mj-text font-size="14px" color="{{ theme.color.text|default:'#4b5563' }}">
              {% if item.variant_name %}<strong>Variasi:</strong> {{ item.variant_name }}<br/>{% endif %}
              <strong>Stok Saat Ini:</strong> <span style="color: #dc2626; font-weight: bold;">{{ item.current_stock }}</span><br/>
              <strong>Titik Pesan Ulang:</strong> {{ item.reorder_point }}<br/>
              <strong>SKU:</strong> {{ item.sku }}
            </mj-text>
          </mj-column>
        </mj-section>
        <mj-spacer height="10px" />
        {% endfor %}

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Tindakan yang Direkomendasikan:
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}" line-height="1.8">
          • Buat pesanan pembelian untuk barang dengan persediaan rendah<br/>
          • Pindahkan stok dari lokasi lain<br/>
          • Perbarui titik pesan ulang jika diperlukan<br/>
          • Pertimbangkan untuk menyesuaikan tingkat par
        </mj-text>

        <mj-spacer height="30px" />

        <mj-button href="{{ inventory_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          Lihat Persediaan
        </mj-button>

        <mj-spacer height="10px" />

        <mj-button href="{{ purchase_orders_url }}" background-color="#6b7280" color="#ffffff" font-size="14px" border-radius="6px" padding="10px 25px">
          Buat Pesanan Pembelian
        </mj-button>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
📦 PERINGATAN PERSEDIAAN RENDAH

Persediaan Sedang Rendah

{{ product_count }} produk{{ product_count|pluralize }} {{ product_count|pluralize:'is,are' }} sedang habis di {{ location_name }}.

DETAIL PERINGATAN:
- Lokasi: {{ location_name }}
- Produk yang Terkena Dampak: {{ product_count }}
- Detected: {{ detected_at }}

BARANG DENGAN PERSEDIAAN RENDAH:
{% for item in low_stock_items %}
{{ item.product_name }}
{% if item.variant_name %}Variasi: {{ item.variant_name }}{% endif %}
Stok Saat Ini: {{ item.current_stock }}
Titik Pesan Ulang: {{ item.reorder_point }}
SKU: {{ item.sku }}

{% endfor %}

TINDAKAN YANG DIREKOMENDASIKAN:
• Buat pesanan pembelian untuk barang dengan persediaan rendah
• Pindahkan stok dari lokasi lain
• Perbarui titik pesan ulang jika diperlukan
• Pertimbangkan untuk menyesuaikan tingkat par

Lihat persediaan: {{ inventory_url }}
Buat pesanan pembelian: {{ purchase_orders_url }}