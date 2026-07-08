---
template_type: wishlist_item_added_confirmation
category: Wishlist
---

# Email Template: wishlist_item_added_confirmation

## Subject
✓ {{ product_name }} ditambahkan ke daftar keinginan Anda - {{ shop_name }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section>
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          ❤️ Ditambahkan ke Daftar Keinginan Anda!
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Hi {{ customer_name }},
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Anda telah berhasil menambahkan {{ product_name }} ke daftar keinginan Anda. Kami akan memantau produk ini untuk Anda!
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
            <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.primary|default:'#2563eb' }}">
              {{ product_price }}
            </mj-text>
            {% if product_in_stock %}
            <mj-text font-size="13px" color="#059669">
              ✓ Tersedia di Stok
            </mj-text>
            {% else %}
            <mj-text font-size="13px" color="#dc2626">
              ⚠️ Habis - Kami akan memberi tahu Anda ketika kembali!
            </mj-text>
            {% endif %}
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-section background-color="#f0fdf4" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="14px" color="#065f46" align="center">
              💡 <strong>Kami akan memberi tahu Anda tentang:</strong><br/>
              • Penurunan harga<br/>
              • Peringatan kembali ke stok<br/>
              • Penjualan terbatas waktu tertentu
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-button href="{{ wishlist_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          Lihat Daftar Keinginan Saya
        </mj-button>

        {% if product_in_stock %}
        <mj-spacer height="10px" />
        <mj-button href="{{ product_url }}" background-color="#059669" color="#ffffff" font-size="14px" border-radius="6px" padding="10px 25px">
          Beli Sekarang
        </mj-button>
        {% endif %}
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
❤️ DITAMBAHKAN KE DAFTAR KEINGINAN ANDA!

Hi {{ customer_name }},

Anda telah berhasil menambahkan {{ product_name }} ke daftar keinginan Anda. Kami akan memantau produk ini untuk Anda!

{{ product_name }}
Harga: {{ product_price }}
{% if product_in_stock %}✓ Tersedia di Stok{% else %}⚠️ Habis - Kami akan memberi tahu Anda ketika kembali!{% endif %}

💡 KAMI AKAN MEMBERI TAHU ANDA TENTANG:
• Penurunan harga
• Peringatan kembali ke stok
• Penjualan terbatas waktu tertentu

Lihat daftar keinginan saya: {{ wishlist_url }}
{% if product_in_stock %}Beli sekarang: {{ product_url }}{% endif %}