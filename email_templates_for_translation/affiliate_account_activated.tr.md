---
template_type: affiliate_account_activated
category: Affiliate Program
---

# Email Template: affiliate_account_activated

## Subject
Hoş geldiniz! Hesabınız yeniden etkinleştirildi

## HTML Content
<mjml>
  <mj-head>
    <mj-attributes>
      <mj-text font-family="Arial, sans-serif" line-height="1.6" />
      <mj-all font-family="Arial, sans-serif" />
    </mj-attributes>
  </mj-head>
  <mj-body background-color="#f8f9fa">
    <!-- Header -->
    <mj-section background-color="#ffffff" padding="40px 20px">
      <mj-column>
        <mj-text font-size="32px" font-weight="bold" color="#212529" align="center">
          🎉 Hesabınız Yeniden Etkinleştirildi!
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Success Banner -->
    <mj-section background-color="#28a745" padding="40px 20px">
      <mj-column>
        <mj-text font-size="24px" font-weight="bold" color="#ffffff" align="center">
          Hoş Geldiniz!
        </mj-text>
        <mj-text font-size="16px" color="#ffffff" align="center" padding-top="10px">
          Affiliate hesabınız tekrar aktif
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Content -->
    <mj-section background-color="#ffffff" padding="20px">
      <mj-column>
        <mj-text font-size="16px" color="#212529">
          Merhaba {{ affiliate_name }},
        </mj-text>
        <mj-text font-size="16px" color="#212529">
          İyimser haber! {{ shop_name }} ile affiliate hesabınız yeniden etkinleştirildi.
        </mj-text>
        <mj-text font-size="16px" color="#212529">
          Ürünlerimizi tanıtma ve komisyon kazanma faaliyetlerinizi hemen yeniden başlatabilirsiniz.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- CTA -->
    <mj-section background-color="#ffffff" padding="30px 20px">
      <mj-column>
        <mj-button background-color="#007bff" color="#ffffff" href="{{ portal_url }}">
          Affiliate Paneline Giriş Yap
        </mj-button>
      </mj-column>
    </mj-section>

    <!-- Footer -->
    <mj-section background-color="#f8f9fa" padding="20px">
      <mj-column>
        <mj-text font-size="12px" color="#6c757d" align="center">
          {{ shop_name }}<br/>
          Sorularınız mı var? <a href="mailto:{{ support_email }}" style="color: #007bff;">Destek ile İletişime Geçin</a>
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
Hoş geldiniz! Hesabınız yeniden etkinleştirildi

Merhaba {{ affiliate_name }},

İyimser haber! {{ shop_name }} ile affiliate hesabınız yeniden etkinleştirildi.

Ürünlerimizi tanıtma ve komisyon kazanma faaliyetlerinizi hemen yeniden başlatabilirsiniz.

Panelinize giriş yapın: {{ portal_url }}

{{ shop_name }}
Sorularınız mı var? {{ support_email }} ile iletişime geçin
