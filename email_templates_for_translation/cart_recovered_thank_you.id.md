---
template_type: cart_recovered_thank_you
category: Cart Recovery
---

# Email Template: cart_recovered_thank_you

## Subject
Terima kasih atas pesanan #{{ order_number }} Anda! - {{ shop_name }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section>
      <mj-column>
        <mj-text font-size="24px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}" align="center">
          🎉 Terima kasih atas pesanan Anda!
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Hai {{ customer_name }},
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Kami sangat senang Anda telah menyelesaikan pembelian Anda! Pesanan Anda telah dikonfirmasi dan kami sedang mempersiapkannya untuk dikirim.
        </mj-text>

        <mj-spacer height="30px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
              Ringkasan Pesanan
            </mj-text>
            <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>Nomor Pesanan:</strong> {{ order_number }}<br/>
              <strong>Tanggal Pesanan:</strong> {{ order_date }}<br/>
              <strong>Total:</strong> {{ order_total }}
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-button href="{{ order_tracking_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          Lacak Pesanan Anda
        </mj-button>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Apa yang Terjadi Berikutnya?
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}" line-height="1.8">
          1. Kami akan mempersiapkan pesanan Anda (biasanya dalam 1-2 hari kerja)<br/>
          2. Anda akan menerima konfirmasi pengiriman dengan informasi pelacakan<br/>
          3. Pesanan Anda akan dikirim ke: {{ shipping_address }}
        </mj-text>

        <mj-spacer height="30px" />

        <mj-section background-color="#f0fdf4" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="14px" color="#065f46" align="center">
              💡 <strong>Apakah Anda tahu?</strong><br/>
              Anda dapat melacak pesanan Anda kapan saja di dashboard akun Anda.
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="20px" />

        <mj-text font-size="14px" color="{{ theme.color.text_secondary|default:'#6b7280' }}" align="center">
          Pertanyaan? <a href="{{ support_url }}" style="color: {{ theme.color.primary|default:'#2563eb' }};">Hubungi tim dukungan kami</a>
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
🎉 TERIMA KASIH ATAS PESANAN ANDA!

Hai {{ customer_name }},

Kami sangat senang Anda telah menyelesaikan pembelian Anda! Pesanan Anda telah dikonfirmasi dan kami sedang mempersiapkannya untuk dikirim.

RINGKASAN PESANAN:
- Nomor Pesanan: {{ order_number }}
- Tanggal Pesanan: {{ order_date }}
- Total: {{ order_total }}

Lacak pesanan Anda: {{ order_tracking_url }}

APA YANG TERJADI SELANJUTNYA?
1. Kami akan mempersiapkan pesanan Anda (biasanya dalam 1-2 hari kerja)
2. Anda akan menerima konfirmasi pengiriman dengan informasi pelacakan
3. Pesanan Anda akan dikirim ke: {{ shipping_address }}

💡 APAKAH ANDA TAHU?
Anda dapat melacak pesanan Anda kapan saja di dashboard akun Anda.

Pertanyaan? Hubungi tim dukungan kami: {{ support_url }}

---
Pesanan #{{ order_number }} di {{ shop_name }}