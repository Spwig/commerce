---
template_type: affiliate_account_suspended
category: Affiliate Program
---

# Email Template: affiliate_account_suspended

## Subject
Önemli: Hesabınız Askıya Alındı

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
        <mj-text font-size="32px" font-weight="bold" color="#dc3545" align="center">
          Hesabınız Askıya Alındı
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
          {{ shop_name }} ile olan ortaklık hesabınız askıya alınmıştır.
        </mj-text>
        <mj-text font-size="16px" color="#212529">
          Bu, genellikle ortaklık programımızın koşulları ve şartları ile ilgili bir ihlal nedeniyle olur.
        </mj-text>
        <mj-text font-size="16px" color="#212529">
          Bu durumun bir hata olduğunu düşünüyorsanız veya bu karar hakkında konuşmak istiyorsanız, lütfen destek ekibimize ulaşın.
        </mj-text>
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
Önemli: Hesabınız Askıya Alındı

Merhaba {{ affiliate_name }},

{{ shop_name }} ile olan ortaklık hesabınız askıya alınmıştır.

Bu, genellikle ortaklık programımızın koşulları ve şartları ile ilgili bir ihlal nedeniyle olur.

Bu durumun bir hata olduğunu düşünüyorsanız veya bu karar hakkında konuşmak istiyorsanız, lütfen destek ekibimize ulaşın.

{{ shop_name }}
Sorularınız mı var? {{ support_email }} ile iletişime geçin