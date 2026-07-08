---
template_type: return_request_approved
category: Returns
---

# Email Template: return_request_approved

## Subject
Pengembalian Anda Telah Disetujui - Pesanan #{{ order_number }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="{{ theme.color.surface|default:'#f0fdf4' }}">
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="{{ theme.color.text|default:'#166534' }}">
          Pengembalian Disetujui
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text|default:'#166534' }}">
          Pesanan #{{ order_number }}
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Hai {{ customer_name }},
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Permintaan pengembalian untuk pesanan <strong>#{{ order_number }}</strong> telah disetujui.
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          <strong>Tahap selanjutnya:</strong>
        </mj-text>

        <mj-text font-size="15px" line-height="1.8" color="{{ theme.color.text|default:'#4b5563' }}">
          1. Unduh dan cetak label pengembalian di bawah ini<br/>
          2. Kemas barang secara aman dalam kemasan aslinya jika memungkinkan<br/>
          3. Tempelkan label pengembalian di luar paket<br/>
          4. Serahkan ke lokasi pengiriman terdekat Anda
        </mj-text>

        {% if return_label_url %}
        <mj-spacer height="20px" />
        <mj-button href="{{ return_label_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          Unduh Label Pengembalian
        </mj-button>
        {% endif %}

        {% if return_tracking_number %}
        <mj-text font-size="15px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          <strong>Nomor Pelacakan Pengembalian:</strong> {{ return_tracking_number }}
        </mj-text>
        {% endif %}

        <mj-section background-color="{{ theme.color.surface|default:'#fffbeb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-size="15px" line-height="1.6" color="{{ theme.color.text|default:'#92400e' }}">
              <strong>Penting:</strong> Silakan kirimkan pengembalian dalam 7 hari untuk memastikan proses pengembalian Anda diproses dengan cepat.
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Setelah kami menerima dan memeriksa pengembalian Anda, kami akan memproses pengembalian ke metode pembayaran asli.
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
Pengembalian Disetujui - Pesanan #{{ order_number }}

Hai {{ customer_name }},

Permintaan pengembalian untuk pesanan #{{ order_number }} telah disetujui.

Tahap selanjutnya:
1. Unduh dan cetak label pengembalian
2. Kemas barang secara aman dalam kemasan aslinya jika memungkinkan
3. Tempelkan label pengembalian di luar paket
4. Serahkan ke lokasi pengiriman terdekat Anda

{% if return_label_url %}Unduh label pengembalian Anda: {{ return_label_url }}{% endif %}
{% if return_tracking_number %}Nomor Pelacakan Pengembalian: {{ return_tracking_number }}{% endif %}

Penting: Silakan kirimkan pengembalian dalam 7 hari untuk memastikan proses pengembalian Anda diproses dengan cepat.

Setelah kami menerima dan memeriksa pengembalian Anda, kami akan memproses pengembalian ke metode pembayaran asli.