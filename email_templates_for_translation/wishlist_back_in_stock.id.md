---
template_type: wishlist_back_in_stock
category: Wishlist
---

# Email Template: wishlist_back_in_stock

## Subject
✓ {{ product_name }} kembali tersedia! - {{ shop_name }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#f0fdf4">
      <mj-column>
        <mj-text font-size="22px" font-weight="bold" color="#059669" align="center">
          ✓ Kembali Tersedia!
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Berita Baik, {{ customer_name }}!
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Sebuah produk di daftar keinginan Anda kembali tersedia. Dapatkan sebelum habis lagi!
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
            <mj-text font-size="18px" font-weight="bold" color="{{ theme.color.primary|default:'#2563eb' }}">
              {{ product_price }}
            </mj-text>
            <mj-text font-size="14px" color="#059669" font-weight="bold">
              ✓ Sekarang Tersedia
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-button href="{{ product_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="18px" font-weight="bold" border-radius="6px" padding="18px 50px">
          Beli Sekarang
        </mj-button>

        <mj-spacer height="20px" />

        <mj-text font-size="13px" color="{{ theme.color.text_secondary|default:'#6b7280' }}" align="center">
          Hapus dari daftar keinginan: <a href="{{ remove_wishlist_url }}">Klik di sini</a>
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
✓ KEMBALI TERSEDIA!

Berita Baik, {{ customer_name }}!

Sebuah produk di daftar keinginan Anda kembali tersedia. Dapatkan sebelum habis lagi!

{{ product_name }}
Harga: {{ product_price }}
✓ Sekarang Tersedia

Beli sekarang: {{ product_url }}

Hapus dari daftar keinginan: {{ remove_wishlist_url }}