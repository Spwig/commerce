---
template_type: affiliate_program_rejected
category: Affiliate Program
---

# Email Template: affiliate_program_rejected

## Subject
Program Başvurusu Güncellemesi

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
          Uygulama Güncellemesi
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
          {{ program_name }}'i tanıtma başvurusunuz için teşekkür ederiz.
        </mj-text>
        <mj-text font-size="16px" color="#212529">
          Başvurunuzu inceledikten sonra şu anda onaylamaya karar verdik.
        </mj-text>
        <mj-text font-size="16px" color="#212529">
          Affiliate ağımdaki diğer programları hâlâ tanıtabilirsiniz.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- CTA -->
    <mj-section background-color="#ffffff" padding="30px 20px">
      <mj-column>
        <mj-button background-color="#6c757d" color="#ffffff" href="{{ portal_url }}">
          Diğer Programları Görüntüle
        </mj-button>
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
Program Başvurusu Güncellemesi

Merhaba {{ affiliate_name }},

{{ program_name }}'i tanıtma başvurusunuz için teşekkür ederiz.

Başvurunuzu inceledikten sonra şu anda onaylamaya karar verdik.

Affiliate ağımdaki diğer programları hâlâ tanıtabilirsiniz.

Diğer programları görüntüleyin: {{ portal_url }}

{{ shop_name }}
Sorularınız mı var? {{ support_email }} ile iletişime geçin