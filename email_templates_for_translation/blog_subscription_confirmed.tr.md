---
template_type: blog_subscription_confirmed
category: Blog
---

# Email Template: blog_subscription_confirmed

## Subject
Lütfen {{ blog_name }} aboneliğinizi onaylayın

## HTML Content
<mjml>
  <mj-body>
    <mj-section>
      <mj-column>
        <mj-text font-size="22px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Aboneliğinizi Onaylayın
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Merhaba {{ subscriber_name }},
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          {{ blog_name }}'a aboneliğiniz için teşekkür ederiz! Aboneliğinizi tamamlamak ve güncellemeleri almaya başlamak için e-posta adresinizi onaylayın.
        </mj-text>

        <mj-spacer height="30px" />

        <mj-button href="{{ confirmation_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="18px" font-weight="bold" border-radius="6px" padding="18px 50px">
          Aboneliği Onayla
        </mj-button>

        <mj-spacer height="30px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="14px" color="{{ theme.color.text|default:'#4b5563' }}">
              Butonu tıklayamazsanız, bu bağlantıyı tarayıcınıza kopyalayıp yapıştırın:<br/>
              <span style="color: {{ theme.color.primary|default:'#2563eb' }}; font-family: 'Courier New', monospace;">{{ confirmation_url }}</span>
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-size="14px" color="{{ theme.color.text_secondary|default:'#6b7280' }}">
          <strong>Neden onaylamalıyız?</strong><br/>
          E-posta onayı, sizin güncellemeler almak istiyorsanızdan emin olmamızı ve spam önleme konusunda yardımcı olur. Gizlilik ve e-posta kutusu sizin için önemlidir.
        </mj-text>

        <mj-spacer height="20px" />

        <mj-text font-size="13px" color="{{ theme.color.text_secondary|default:'#6b7280' }}" align="center">
          Aboneliğe kaydolmadınız mı? Bu e-postayı güvenli bir şekilde ihmal edebilirsiniz.
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
ABONELİĞİNİZİ ONAYLAYIN

Merhaba {{ subscriber_name }},

{{ blog_name }}'a aboneliğiniz için teşekkür ederiz! Aboneliğinizi tamamlamak ve güncellemeleri almaya başlamak için e-posta adresinizi onaylayın.

Aboneliği onayla: {{ confirmation_url }}

Neden onaylamalıyız?
E-posta onayı, sizin güncellemeler almak istiyorsanızdan emin olmamızı ve spam önleme konusunda yardımcı olur. Gizlilik ve e-posta kutusu sizin için önemlidir.

Aboneliğe kaydolmadınız mı? Bu e-postayı güvenli bir şekilde ihmal edebilirsiniz.