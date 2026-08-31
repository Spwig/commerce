---
template_type: newsletter_signup_confirm
category: Newsletter
---

# Email Template: newsletter_signup_confirm

## Subject
Lütfen {{ store_name }} aboneliklerini onaylayın

## HTML Content
<mjml>
  <mj-body>
    <mj-section>
      <mj-column>
        <mj-text font-size="22px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Abonelik onaylayın
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          {{ store_name }}'dan haber almak için kaydolduğunuz için teşekkür ederiz! Güncellemelerimizi ve kampanyalarımızı almaya başlamak için e-posta adresinizi onaylayın.
        </mj-text>

        <mj-spacer height="30px" />

        <mj-button href="{{ confirmation_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="18px" font-weight="bold" border-radius="6px" padding="18px 50px">
          Abonelik onaylayın
        </mj-button>

        <mj-spacer height="30px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="14px" color="{{ theme.color.text|default:'#4b5563' }}">
              Butona tıklayamazsanız, bu bağlantıyı tarayıcınıza kopyalayabilirsiniz:<br/>
              <span style="color: {{ theme.color.primary|default:'#2563eb' }}; font-family: 'Courier New', monospace;">{{ confirmation_url }}</span>
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-size="14px" color="{{ theme.color.text_secondary|default:'#6b7280' }}">
          <strong>Neden onaylamalısınız?</strong><br/>
          E-posta adresinizi onaylamak, güncellemelerimizi gerçekten istiyorsanız bize yardımcı olur ve gelen kutunuzda spam olmaz.
        </mj-text>

        <mj-spacer height="20px" />

        <mj-text font-size="13px" color="{{ theme.color.text_secondary|default:'#6b7280' }}" align="center">
          Kayıt olmazsanız, bu e-postayı güvenle yok sayabilirsiniz.
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
Lütfen {{ store_name }} aboneliklerini onaylayın

{{ store_name }}'dan haber almak için kaydolduğunuz için teşekkür ederiz! Güncellemelerimizi ve kampanyalarımızı almaya başlamak için e-posta adresinizi onaylayın:

{{ confirmation_url }}

E-posta adresinizi onaylamak, güncellemelerimizi gerçekten istiyorsanız bize yardımcı olur ve gelen kutunuzda spam olmaz.

Kayıt olmazsanız, bu e-postayı güvenle yok sayabilirsiniz.