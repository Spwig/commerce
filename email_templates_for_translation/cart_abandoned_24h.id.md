---
template_type: cart_abandoned_24h
category: Cart Recovery
---

# Email Template: cart_abandoned_24h

## Subject
Masih tertarik? Keranjang belanja Anda akan segera habis - {{ shop_name }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section>
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Keranjang belanja Anda {{ cart_item_count }} barang{{ cart_item_count|pluralize }} {{ cart_item_count|pluralize:'is,are' }} masih menunggu
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Halo {{ customer_name }},
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Kami menyimpan keranjang belanja Anda, tetapi barang-barang ini tidak akan bertahan selamanya. Selesaikan pembelian Anda sebelum habis!
        </mj-text>

        <mj-spacer height="20px" />

        {% for item in cart_items %}
        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="15px">
          <mj-column width="30%">
            <mj-image src="{{ item.product_image }}" alt="{{ item.product_name }}" border-radius="4px" />
          </mj-column>
          <mj-column width="70%">
            <mj-text font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
              {{ item.product_name }}
            </mj-text>
            <mj-text color="{{ theme.color.text_secondary|default:'#6b7280' }}">
              Qty: {{ item.quantity }} × {{ item.price }}
            </mj-text>
            {% if item.low_stock %}
            <mj-text color="#dc2626" font-size="13px">
              ⚠️ Hanya tersisa {{ item.stock_remaining }}!
            </mj-text>
            {% endif %}
          </mj-column>
        </mj-section>
        <mj-spacer height="10px" />
        {% endfor %}

        <mj-spacer height="20px" />

        <mj-text font-size="18px" font-weight="bold" align="right" color="{{ theme.color.text|default:'#1f2937' }}">
          Total: {{ cart_total }}
        </mj-text>

        <mj-spacer height="30px" />

        <mj-button href="{{ cart_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          Selesaikan Pesanan Anda Sekarang
        </mj-button>

        <mj-spacer height="30px" />

        <mj-section background-color="#f0fdf4" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="14px" color="#065f46" align="center">
              ✓ Pengiriman gratis untuk pesanan di atas {{ free_shipping_threshold }}<br/>
              ✓ Jaminan pengembalian uang dalam 30 hari<br/>
              ✓ Checkout aman
            </mj-text>
          </mj-column>
        </mj-section>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
Keranjang belanja Anda {{ cart_item_count }} barang{{ cart_item_count|pluralize }} {{ cart_item_count|pluralize:'is,are' }} masih menunggu

Halo {{ customer_name }},

Kami menyimpan keranjang belanja Anda, tetapi barang-barang ini tidak akan bertahan selamanya. Selesaikan pembelian Anda sebelum habis!

KERANJANG BELANJA:
{% for item in cart_items %}
- {{ item.product_name }}
  Qty: {{ item.quantity }} × {{ item.price }}
  {% if item.low_stock %}⚠️ Hanya tersisa {{ item.stock_remaining }}!{% endif %}
{% endfor %}

Total: {{ cart_total }}

Selesaikan pesanan Anda sekarang: {{ cart_url }}

MENGAPA BERBELANJA DENGAN KAMI:
✓ Pengiriman gratis untuk pesanan di atas {{ free_shipping_threshold }}
✓ Jaminan pengembalian uang dalam 30 hari
✓ Checkout aman

---
Untuk menghentikan penerimaan pengingat keranjang, kunjungi: {{ preferences_url }}