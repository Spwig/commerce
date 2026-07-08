---
template_type: blog_subscription_confirmed
category: Blog
---

# Email Template: blog_subscription_confirmed

## Subject
Konfirmasi langganan Anda ke {{ blog_name }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section>
      <mj-column>
        <mj-text font-size="22px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Konfirmasi Langganan Anda
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Hai {{ subscriber_name }},
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Terima kasih telah berlangganan ke {{ blog_name }}! Untuk menyelesaikan langganan Anda dan mulai menerima pembaruan, silakan konfirmasi alamat email Anda.
        </mj-text>

        <mj-spacer height="30px" />

        <mj-button href="{{ confirmation_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="18px" font-weight="bold" border-radius="6px" padding="18px 50px">
          Konfirmasi Langganan
        </mj-button>

        <mj-spacer height="30px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="14px" color="{{ theme.color.text|default:'#4b5563' }}">
              Tidak bisa mengklik tombol? Salin dan tempel tautan ini ke browser Anda:<br/>
              <span style="color: {{ theme.color.primary|default:'#2563eb' }}; font-family: 'Courier New', monospace;">{{ confirmation_url }}</span>
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-size="14px" color="{{ theme.color.text_secondary|default:'#6b7280' }}">
          <strong>Mengapa harus mengonfirmasi?</strong><br/>
          Konfirmasi email membantu kami memastikan Anda ingin menerima pembaruan dan mencegah spam. Privasi Anda dan kotak masuk Anda penting bagi kami.
        </mj-text>

        <mj-spacer height="20px" />

        <mj-text font-size="13px" color="{{ theme.color.text_secondary|default:'#6b7280' }}" align="center">
          Tidak berlangganan? Anda dapat aman mengabaikan email ini.
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
KONFIRMASI LANGGANAN ANDA

Hai {{ subscriber_name }},

Terima kasih telah berlangganan ke {{ blog_name }}! Untuk menyelesaikan langganan Anda dan mulai menerima pembaruan, silakan konfirmasi alamat email Anda.

Konfirmasi langganan: {{ confirmation_url }}

MENGAPA HARUS MENGONFIRMASI?
Konfirmasi email membantu kami memastikan Anda ingin menerima pembaruan dan mencegah spam. Privasi Anda dan kotak masuk Anda penting bagi kami.

Tidak berlangganan? Anda dapat aman mengabaikan email ini.