---
template_type: affiliate_account_approved
category: Affiliate Program
---

# Email Template: affiliate_account_approved

## Subject
🎉 {{ shop_name }} Ortak Programına Hoş Geldiniz!

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
          🎉 Başvuru Onaylandı!
        </mj-text>
        <mj-text font-size="18px" color="#6c757d" align="center">
          Ortak programımıza hos geldiniz
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Success Banner -->
    <mj-section background-color="#28a745" padding="40px 20px">
      <mj-column>
        <mj-text font-size="24px" font-weight="bold" color="#ffffff" align="center">
          Artık Bir Ortaksınız!
        </mj-text>
        <mj-text font-size="16px" color="#ffffff" align="center" padding-top="10px">
          Bugün komisyon kazanmaya başlayın
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
          TEBRİKLER! {{ shop_name }} ortak programına katılmak için başvurunuz onaylandı.
        </mj-text>
        <mj-text font-size="16px" color="#212529">
          Artık ürünlerimizi tanıtma ve size ait her satıştan komisyon kazanmaya başlayabilirsiniz.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- How it Works -->
    <mj-section background-color="#f8f9fa" padding="30px 20px">
      <mj-column>
        <mj-text font-size="18px" font-weight="bold" color="#212529" align="center" padding-bottom="10px">
          Nasıl Çalışır
        </mj-text>
        <mj-text font-size="14px" color="#6c757d">
          1. Dashboard'dan benzersiz ortak bağlantılarınıza erişin<br/>
          2. Bu bağlantıları kitleinize paylaşın<br/>
          3. İnsanların bağlantılarınız aracılığıyla alışveriş yapması durumunda komisyon kazanın<br/>
          4. Ödeme zaman çizelgenize göre ödemeleri alın
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- CTA -->
    <mj-section background-color="#ffffff" padding="30px 20px">
      <mj-column>
        <mj-button background-color="#007bff" color="#ffffff" href="{{ portal_url }}">
          Ortak Dashboard'ına Erişim
        </mj-button>
      </mj-column>
    </mj-section>

    <!-- Footer -->
    <mj-section background-color="#f8f9fa" padding="20px">
      <mj-column>
        <mj-text font-size="12px" color="#6c757d" align="center">
          {{ shop_name }}<br/>
          Sorularınız varsa <a href="mailto:{{ support_email }}" style="color: #007bff;">Destek ile iletişime geçin</a>
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
🎉 {{ shop_name }} Ortak Programına Hoş Geldiniz!

Merhaba {{ affiliate_name }},

Tebrikler! {{ shop_name }} ortak programına katılmak için başvurunuz onaylandı.

Artık ürünlerimizi tanıtma ve size ait her satıştan komisyon kazanmaya başlayabilirsiniz.

Nasıl Çalışır:
1. Dashboard'dan benzersiz ortak bağlantılarınıza erişin
2. Bu bağlantıları kitleinize paylaşın
3. İnsanların bağlantılarınız aracılığıyla alışveriş yapması durumunda komisyon kazanın
4. Ödeme zaman çizelgenize göre ödemeleri alın

Dashboard'ınıza erişim: {{ portal_url }}

{{ shop_name }}
Sorularınız varsa {{ support_email }} ile iletişime geçin