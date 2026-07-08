---
template_type: license_maintenance_renewal
category: License
---

# Email Template: license_maintenance_renewal

## Subject
Bakım Yenilenmiş - Sipariş #{{ order_number }}

## HTML Content
<mjml>
  <mj-head>
    <mj-attributes>
      <mj-all font-family="'Helvetica Neue', Helvetica, Arial, sans-serif" />
      <mj-text font-size="14px" color="#333333" line-height="20px" />
      <mj-section background-color="{{ theme.color.background|default:'#ffffff' }}" padding="20px" />
    </mj-attributes>
  </mj-head>
  <mj-body background-color="{{ theme.color.background_secondary|default:'#f9fafb' }}">
    <!-- Header -->
    <mj-section background-color="{{ theme.color.success|default:'#10b981' }}" padding="30px 20px">
      <mj-column>
        <mj-text font-size="28px" font-weight="bold" color="#ffffff" align="center">
          Bakım Yenilenmiş!
        </mj-text>
        <mj-text font-size="16px" color="#ffffffcc" align="center" padding-top="10px">
          Sipariş #{{ order_number }}
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Greeting -->
    <mj-section>
      <mj-column>
        <mj-text font-size="16px">
          Merhaba {{ customer_name }},
        </mj-text>
        <mj-text>
          Spwig bakım abonemeniniz başarıyla yenilendi. Platform güncellemeleri, güvenlik yamaları ve yeni özellikler hala alacağınızdan emin olabilirsiniz.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Renewal Summary -->
    <mj-section background-color="{{ theme.color.background_secondary|default:'#f9fafb' }}" padding="20px" border-radius="8px">
      <mj-column>
        <mj-text font-size="16px" font-weight="bold" padding-bottom="10px">
          Yenileme Özeti
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          Lisans Anahtarı: {{ license_key }}
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          Bakımın Geçerliliği: {{ renewal_expires_at }}
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          Sipariş Numarası: {{ order_number }}
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- What's Included -->
    <mj-section>
      <mj-column>
        <mj-text font-size="16px" font-weight="bold" padding-bottom="10px">
          İçerikler
        </mj-text>
        <mj-text font-size="14px">
          Aktif bakım abonemeniniz sayesinde erişiminiz olanlar:
        </mj-text>
        <mj-text font-size="14px" padding-top="5px">
          - Platform özellikleri güncellemeleri ve iyileştirmeleri
        </mj-text>
        <mj-text font-size="14px">
          - Güvenlik yamaları ve hata düzeltmeleri
        </mj-text>
        <mj-text font-size="14px">
          - Upgrade sunucusu üzerinden yeni bileşen sürümleri
        </mj-text>
        <mj-text font-size="14px">
          - Teknik destek
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Next Steps -->
    <mj-section>
      <mj-column>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          Tarafınızdan herhangi bir eylem gerekmez. Güncellemeler hala yönetici panelinizdeki bileşen güncelleme sistemi üzerinden erişilebilir olacak.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Support -->
    {% include 'email_system/mjml_components/support_block.mjml' %}
  </mj-body>
</mjml>

## Text Content
Bakım Yenilenmiş!

Sipariş #{{ order_number }}

Merhaba {{ customer_name }},

Spwig bakım abonemeniniz başarıyla yenilendi. Platform güncellemeleri, güvenlik yamaları ve yeni özellikler hala alacağınızdan emin olabilirsiniz.

Yenileme Özeti:
- Lisans Anahtarı: {{ license_key }}
- Bakımın Geçerliliği: {{ renewal_expires_at }}
- Sipariş Numarası: {{ order_number }}

İçerikler:
- Platform özellikleri güncellemeleri ve iyileştirmeleri
- Güvenlik yamaları ve hata düzeltmeleri
- Upgrade sunucusu üzerinden yeni bileşen sürümleri
- Teknik destek

Tarafınızdan herhangi bir eylem gerekmez. Güncellemeler hala yönetici panelinizdeki bileşen güncelleme sistemi üzerinden erişilebilir olacak.

Yardıma mı ihtiyacınız var? {{ support_email }} adresini kullanın.