---
template_type: return_request_confirmation
category: Returns
---

# Email Template: return_request_confirmation

## Subject
Permintaan Pengembalian Diterima - Pesanan #{{ order_number }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="{{ theme.color.surface|default:'#eff6ff' }}">
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="{{ theme.color.text|default:'#1e40af' }}">
          Permintaan Pengembalian Diterima
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text|default:'#1e40af' }}">
          Pesanan #{{ order_number }}
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Hi {{ customer_name }},
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Kami telah menerima permintaan pengembalian Anda untuk pesanan <strong>#{{ order_number }}</strong>.
        </mj-text>

        <mj-spacer height="20px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
              Detail Pengembalian:
            </mj-text>
            <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>Alasan:</strong> {{ return_reason }}<br/>
              <strong>Barang:</strong> {{ items_count }} item(s)<br/>
              <strong>Status:</strong> {{ return_status }}
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="20px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Apa yang terjadi selanjutnya?
        </mj-text>

        <mj-text font-size="15px" line-height="1.8" color="{{ theme.color.text|default:'#4b5563' }}">
          1. Tim kami akan meninjau permintaan pengembalian Anda dalam waktu 24-48 jam<br/>
          2. Setelah disetujui, kami akan mengirimkan label pengembalian melalui email<br/>
          3. Kemas barang dengan aman dan lampirkan label pengembalian<br/>
          4. Serahkan paket di lokasi pengiriman terdekat<br/>
          5. Refund Anda akan diproses setelah kami menerima dan memeriksa barang tersebut
        </mj-text>

        <mj-spacer height="20px" />

        <mj-text font-size="15px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Jika Anda memiliki pertanyaan, jangan ragu untuk menghubungi kami.
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
PERMINTAAN PENGEMBALIAN DITERIMA
Pesanan #{{ order_number }}

Hi {{ customer_name }},

Kami telah menerima permintaan pengembalian Anda untuk pesanan #{{ order_number }}.

DETAIL PENGEMBALIAN:
- Alasan: {{ return_reason }}
- Barang: {{ items_count }} item(s)
- Status: {{ return_status }}

APA YANG TERJADI SELANJUTNYA?
1. Tim kami akan meninjau permintaan pengembalian Anda dalam waktu 24-48 jam
2. Setelah disetujui, kami akan mengirimkan label pengembalian melalui email
3. Kemas barang dengan aman dan lampirkan label pengembalian
4. Serahkan paket di lokasi pengiriman terdekat
5. Refund Anda akan diproses setelah kami menerima dan memeriksa barang tersebut

Jika Anda memiliki pertanyaan, jangan ragu untuk menghubungi kami.