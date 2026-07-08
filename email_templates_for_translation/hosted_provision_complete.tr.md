---
template_type: hosted_provision_complete
category: License
---

# Email Template: hosted_provision_complete

## Subject
Mağazanız Hazır - {{ store_name }}

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
    <mj-section background-color="{{ theme.color.primary|default:'#2563eb' }}" padding="30px 20px">
      <mj-column>
        <mj-text font-size="28px" font-weight="bold" color="#ffffff" align="center">
          Mağazanız Aktif!
        </mj-text>
        <mj-text font-size="16px" color="#ffffffcc" align="center" padding-top="10px">
          {{ store_name }} siz için hazırdır
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Greeting -->
    <mj-section>
      <mj-column>
        <mj-text font-size="16px">
          Merhaba {{ name|default:'there' }},
        </mj-text>
        <mj-text>
          Harika haber! Spwig mağazanız <strong>{{ store_name }}</strong> hazırlanmış ve artık aktif. Ürünlerinizi, markanızı ve ödeme yöntemlerinizi hemen ayarlamaya başlayabilirsiniz.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Store Details -->
    <mj-section background-color="{{ theme.color.background_secondary|default:'#f9fafb' }}" padding="20px" border-radius="8px">
      <mj-column>
        <mj-text font-size="16px" font-weight="bold" padding-bottom="10px">
          Mağaza Detayları
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          Mağaza URL'si: {{ store_url }}
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          Yönetici Paneli: {{ admin_url }}
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          Bölge: {{ region }}
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Getting Started -->
    <mj-section>
      <mj-column>
        <mj-text font-size="16px" font-weight="bold" padding-bottom="10px">
          Hızlı Başlangıç
        </mj-text>
        <mj-text font-size="14px">
          1. Satın alma sırasında ayarladığınız e-posta ve şifreyle yönetici paneline giriş yapın
        </mj-text>
        <mj-text font-size="14px">
          2. Tasarım > Tema Ayarları altında mağaza logonuzu ve markanızı ekleyin
        </mj-text>
        <mj-text font-size="14px">
          3. Katalog > Ürünler altında ilk ürünleri ekleyin
        </mj-text>
        <mj-text font-size="14px">
          4. Ayarlar > Ödeme Sağlayıcıları altında bir ödeme sağlayıcısı kurun
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- CTA -->
    {% include 'email_system/mjml_components/cta_button.mjml' with url=admin_url text="Yönetici Paneline Git" %}

    <!-- Support -->
    {% include 'email_system/mjml_components/support_block.mjml' %}
  </mj-body>
</mjml>

## Text Content
Mağazanız Aktif!

{{ store_name }} siz için hazırdır.

Merhaba {{ name|default:'there' }},

Harika haber! Spwig mağazanız {{ store_name }} hazırlanmış ve artık aktif. Ürünlerinizi, markanızı ve ödeme yöntemlerinizi hemen ayarlamaya başlayabilirsiniz.

Mağaza Detayları:
- Mağaza URL'si: {{ store_url }}
- Yönetici Paneli: {{ admin_url }}
- Bölge: {{ region }}

Hızlı Başlangıç:
1. Satın alma sırasında ayarladığınız e-posta ve şifreyle yönetici paneline giriş yapın
2. Tasarım > Tema Ayarları altında mağaza logonuzu ve markanızı ekleyin
3. Katalog > Ürünler altında ilk ürünleri ekleyin
4. Ayarlar > Ödeme Sağlayıcıları altında bir ödeme sağlayıcısı kurun

Yönetici Paneline Git: {{ admin_url }}

Yardıma mı ihtiyacınız var? {{ support_email }} ile iletişime geçin