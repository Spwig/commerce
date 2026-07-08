---
template_type: back_in_stock_low_stock_warning
category: Stock Notifications
---

# Email Template: back_in_stock_low_stock_warning

## Subject
⚠️ {{ product_name }} kembali tetapi laku cepat! - {{ shop_name }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#fef3c7">
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="#92400e" align="center">
          ⚠️ Stok Terbatas - Bertindak Cepat!
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          {{ product_name }} Kembali Tersedia!
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Hi {{ customer_name }},
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Berita baik! Barang yang Anda tunggu kembali tersedia. Tapi segera - kami hanya memiliki {{ stock_remaining }} unit{{ stock_remaining|pluralize }} tersisa!
        </mj-text>

        <mj-spacer height="30px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column width="35%">
            <mj-image src="{{ product_image }}" alt="{{ product_name }}" border-radius="8px" />
          </mj-column>
          <mj-column width="65%">
            <mj-text font-weight="bold" font-size="18px" color="{{ theme.color.text|default:'#1f2937' }}">
              {{ product_name }}
            </mj-text>
            <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}">
              {{ product_description }}
            </mj-text>
            <mj-text font-size="18px" font-weight="bold" color="{{ theme.color.primary|default:'#2563eb' }}">
              {{ product_price }}
            </mj-text>
            {% if variant_name %}
            <mj-text font-size="14px" color="{{ theme.color.text_secondary|default:'#6b7280' }}">
              Variasi: {{ variant_name }}
            </mj-text>
            {% endif %}
            <mj-spacer height="10px" />
            <mj-text font-size="14px" color="#dc2626" font-weight="bold">
              ⚠️ Hanya {{ stock_remaining }} tersisa di stok!
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-button href="{{ product_url }}" background-color="#dc2626" color="#ffffff" font-size="18px" font-weight="bold" border-radius="6px" padding="18px 50px">
          Beli Sekarang Sebelum Habis
        </mj-button>

        <mj-spacer height="20px" />

        <mj-section background-color="#fee2e2" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="14px" color="#991b1b" align="center">
              🔥 <strong>Produk ini habis terjual {{ times_sold_out }} kali{{ times_sold_out|pluralize }} dalam sebulan terakhir!</strong><br/>
              Jangan lewatkan lagi - pesan sekarang selagi masih ada stok.
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-size="13px" color="{{ theme.color.text_secondary|default:'#6b7280' }}" align="center">
          Tidak tertarik lagi? <a href="{{ unsubscribe_url }}" style="color: {{ theme.color.primary|default:'#2563eb' }};">Batal langganan notifikasi ini</a>
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
⚠️ STOK TERBATAS - BERTINDAK CEPAT!

{{ product_name }} Kembali Tersedia!

Hi {{ customer_name }},

Berita baik! Barang yang Anda tunggu kembali tersedia. Tapi segera - kami hanya memiliki {{ stock_remaining }} unit{{ stock_remaining|pluralize }} tersisa!

PRODUK:
{{ product_name }}
{{ product_description }}
Harga: {{ product_price }}
{% if variant_name %}Variasi: {{ variant_name }}{% endif %}

⚠️ HANYA {{ stock_remaining }} TERSISA DI STOK!

Beli sekarang sebelum habis: {{ product_url }}

🔥 Produk ini habis terjual {{ times_sold_out }} kali{{ times_sold_out|pluralize }} dalam sebulan terakhir!
Jangan lewatkan lagi - pesan sekarang selagi masih ada stok.

Tidak tertarik lagi? Batal langganan: {{ unsubscribe_url }}