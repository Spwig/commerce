---
template_type: newsletter_signup_confirm
category: Newsletter
---

# Email Template: newsletter_signup_confirm

## Subject
Silakan konfirmasi langganan Anda ke {{ store_name }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section>
      <mj-column>
        <mj-text font-size="22px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Konfirmasi langganan Anda
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Terima kasih telah mendaftar untuk mendapatkan informasi dari {{ store_name }}! Silakan konfirmasi alamat email Anda untuk memulai menerima pembaruan dan tawaran kami.
        </mj-text>

        <mj-spacer height="30px" />

        <mj-button href="{{ confirmation_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="18px" font-weight="bold" border-radius="6px" padding="18px 50px">
          Konfirmasi langganan
        </mj-button>

        <mj-spacer height="30px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="14px" color="{{ theme.color.text|default:'#4b5563' }}">
              Tidak bisa mengklik tombolnya? Salin dan tempel tautan ini ke browser Anda:<br/>
              <span style="color: {{ theme.color.primary|default:'#2563eb' }}; font-family: 'Courier New', monospace;">{{ confirmation_url }}</span>
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-size="14px" color="{{ theme.color.text_secondary|default:'#6b7280' }}">
          <strong>Mengapa perlu mengkonfirmasi?</strong><br/>
          Mengonfirmasi email Anda membantu kami memastikan Anda benar-benar ingin menerima pembaruan kami, dan menjaga kotak masuk Anda tetap bebas dari spam.
        </mj-text>

        <mj-spacer height="20px" />

        <mj-text font-size="13px" color="{{ theme.color.text_secondary|default:'#6b7280' }}" align="center">
          Tidak mendaftar? Anda dapat dengan aman mengabaikan email ini.
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
Konfirmasi langganan Anda ke {{ store_name }}

Terima kasih telah mendaftar untuk mendapatkan informasi dari {{ store_name }}! Silakan konfirmasi alamat email Anda untuk memulai menerima pembaruan dan tawaran kami:

{{ confirmation_url }}

Mengonfirmasi email Anda membantu kami memastikan Anda benar-benar ingin menerima pembaruan kami, dan menjaga kotak masuk Anda tetap bebas dari spam.

Tidak mendaftar? Anda dapat dengan aman mengabaikan email ini.