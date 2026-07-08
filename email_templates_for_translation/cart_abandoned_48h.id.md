---
template_type: cart_abandoned_48h
category: Cart Recovery
---

# Email Template: cart_abandoned_48h

## Subject
Terakhir! Keranjang belanja Anda akan kedaluwarsa dalam 24 jam - {{ shop_name }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#fef3c7">
      <mj-column>
        <mj-text font-size="18px" font-weight="bold" color="#92400e" align="center">
          ⏰ Terakhir - Keranjang Belanja Anda Akan Kedaluwarsa dalam 24 Jam
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Jangan lewatkan, {{ customer_name }}!
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Ini adalah pengingat terakhir. Keranjang belanja Anda akan kedaluwarsa dalam 24 jam dan kami tidak dapat menahan barang-barang ini lebih lama.
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
              {{ item.quantity }} × {{ item.price }}
            </mj-text>
          </mj-column>
        </mj-section>
        <mj-spacer height="10px" />
        {% endfor %}

        <mj-spacer height="20px" />

        <mj-text font-size="20px" font-weight="bold" align="right" color="{{ theme.color.text|default:'#1f2937' }}">
          Total: {{ cart_total }}
        </mj-text>

        <mj-spacer height="30px" />

        <mj-button href="{{ cart_url }}" background-color="#dc2626" color="#ffffff" font-size="18px" font-weight="bold" border-radius="6px" padding="18px 50px">
          Selesaikan Pesanan Sebelum Terlambat
        </mj-button>

        <mj-spacer height="20px" />

        <mj-text font-size="14px" color="{{ theme.color.text_secondary|default:'#6b7280' }}" align="center">
          Pertanyaan? Tim kami siap membantu: <a href="{{ support_url }}">Hubungi Dukungan</a>
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
⏰ TERAKHIR - KERANJANG BELANJA ANDA AKAN KEDALUWARSAA DALAM 24 JAM

Jangan lewatkan, {{ customer_name }}!

Ini adalah pengingat terakhir. Keranjang belanja Anda akan kedaluwarsa dalam 24 jam dan kami tidak dapat menahan barang-barang ini lebih lama.

KERANJANG BELANJA ANDA:
{% for item in cart_items %}
- {{ item.product_name }}
  {{ item.quantity }} × {{ item.price }}
{% endfor %}

Total: {{ cart_total }}

Selesaikan pesanan Anda sebelum terlambat: {{ cart_url }}

Pertanyaan? Tim kami siap membantu: {{ support_url }}

---
Ini adalah pengingat terakhir untuk keranjang #{{ cart_id }}.