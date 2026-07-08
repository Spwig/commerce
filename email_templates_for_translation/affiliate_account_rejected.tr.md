---
template_type: affiliate_account_rejected
category: Affiliate Program
---

# Email Template: affiliate_account_rejected

## Subject
Ortaklık Başvurusu Güncellemesi

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
          Başvuru Güncellemesi
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
          {{ shop_name }} ortaklık programına katılmak için ilginiz için teşekkür ederiz.
        </mj-text>
        <mj-text font-size="16px" color="#212529">
          Başvuranızı inceledikten sonra şu anda ilerlemeye karar vermedik.
        </mj-text>
        <mj-text font-size="16px" color="#212529">
          Bu karar, mevcut ortaklık programımızın gereksinimlerine dayanmaktadır ve kilit bilgileriniz veya potansiyelinizi yansıtmayabilir.
        </mj-text>
        <mj-text font-size="16px" color="#212529">
          Eğer koşullarınız değişirse gelecekte tekrar başvurabilirsiniz.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Footer -->
    <mj-section background-color="#f8f9fa" padding="20px">
      <mj-column>
        <mj-text font-size="12px" color="#6c757d" align="center">
          {{ shop_name }}<br/>
          Sorularınız mı var? <a href="mailto:{{ support_email }}" style="color: #007bff;">Destek ile iletişime geçin</a>
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
Ortaklık Başvurusu Güncellemesi

Merhaba {{ affiliate_name }},

{{ shop_name }} ortaklık programına katılmak için ilginiz için teşekkür ederiz.

Başvuranızı inceledikten sonra şu anda ilerlemeye karar vermedik.

Bu karar, mevcut ortaklık programımızın gereksinimlerine dayanmaktadır ve kilit bilgileriniz veya potansiyelinizi yansıtmayabilir.

Eğer koşullarınız değişirse gelecekte tekrar başvurabilirsiniz.

{{ shop_name }}
Sorularınız mı var? {{ support_email }} ile iletişime geçin