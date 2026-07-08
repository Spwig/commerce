---
template_type: wishlist_price_drop
category: Wishlist
---

# Email Template: wishlist_price_drop

## Subject
🔥 Peringatan Harga Turun: {{ product_name }} sekarang {{ discount_percentage }}% off!

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#dcfce7">
      <mj-column>
        <mj-text font-size="24px" font-weight="bold" color="#065f46" align="center">
          🔥 Peringatan Harga Turun!
        </mj-text>
        <mj-text font-size="18px" color="#047857" align="center">
          Hemat {{ discount_percentage }}% pada Item Daftar Keinginan Anda
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Berita Baik, {{ customer_name }}!
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Sebuah produk di daftar keinginan Anda baru saja turun harganya! Jangan lewatkan kesempatan ini untuk menghemat.
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
            <mj-spacer height="10px" />
            <mj-text font-size="14px" color="{{ theme.color.text_secondary|default:'#6b7280' }}">
              Was: <span style="text-decoration: line-through;">{{ original_price }}</span>
            </mj-text>
            <mj-text font-size="24px" font-weight="bold" color="#059669">
              Now: {{ new_price }}
            </mj-text>
            <mj-text font-size="16px" font-weight="bold" color="#dc2626">
              Save {{ savings_amount }} ({{ discount_percentage }}% OFF)
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-button href="{{ product_url }}" background-color="#059669" color="#ffffff" font-size="18px" font-weight="bold" border-radius="6px" padding="18px 50px">
          Beli Sekarang & Hemat {{ discount_percentage }}%
        </mj-button>

        <mj-spacer height="30px" />

        <mj-section background-color="#fee2e2" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="14px" color="#991b1b" align="center">
              ⏰ <strong>Limited Time:</strong> Penjualan ini tidak akan berlangsung selamanya. Harga bisa kembali naik kapan saja!
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="20px" />

        <mj-text font-size="13px" color="{{ theme.color.text_secondary|default:'#6b7280' }}" align="center">
          Hapus dari daftar keinginan: <a href="{{ remove_wishlist_url }}">Klik di sini</a>
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
🔥 PERINGATAN HARGA TURUN!
Hemat {{ discount_percentage }}% pada Item Daftar Keinginan Anda

Berita Baik, {{ customer_name }}!

Sebuah produk di daftar keinginan Anda baru saja turun harganya! Jangan lewatkan kesempatan ini untuk menghemat.

{{ product_name }}
Was: {{ original_price }}
NOW: {{ new_price }}
SAVE {{ savings_amount }} ({{ discount_percentage }}% OFF)

Beli sekarang & hemat {{ discount_percentage }}%: {{ product_url }}

⏰ WAKTU TERBATAS: Penjualan ini tidak akan berlangsung selamanya. Harga bisa kembali naik kapan saja!

Hapus dari daftar keinginan: {{ remove_wishlist_url }}