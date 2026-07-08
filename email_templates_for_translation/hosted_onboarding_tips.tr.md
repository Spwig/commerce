---
template_type: hosted_onboarding_tips
category: License
---

# Email Template: hosted_onboarding_tips

## Subject
{{ store_name }}'den En Çok Yararlanma İpuçları

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
          Başlangıç İpuçları
        </mj-text>
        <mj-text font-size="16px" color="#ffffffcc" align="center" padding-top="10px">
          Spwig mağazanızdan en çok yararlanın
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
          Artık <strong>{{ store_name }}</strong> çalışıyor. Mağazanızdan en çok yararlanmanıza yardımcı olmak için bazı ipuçları aşağıdadır.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Tip 1: Theme -->
    <mj-section background-color="{{ theme.color.background_secondary|default:'#f9fafb' }}" padding="20px" border-radius="8px">
      <mj-column>
        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.primary|default:'#2563eb' }}" padding-bottom="5px">
          Görünümünüzü Özelleştirin
        </mj-text>
        <mj-text font-size="14px">
          <strong>Tasarım > Tema Ayarları</strong> bölümüne giderek bir tema seçin, logonuzu yükleyin ve marka renklerinizi ayarlayın. Mağazanız anında güncellenir ve değişiklikleri anlık olarak önizleyebilirsiniz.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Tip 2: Products -->
    <mj-section>
      <mj-column>
        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.primary|default:'#2563eb' }}" padding-bottom="5px">
          Ürünlerinizi Ekleyin
        </mj-text>
        <mj-text font-size="14px">
          <strong>Katalog > Ürünler</strong> bölümüne giderek ürün eklemeye başlayın. Boyut, renk gibi ürün varyasyyonları oluşturabilir, fiyatlandırabilir, stokları yönetebilir ve yüksek kaliteli görseller yükleyebilirsiniz.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Tip 3: Payments -->
    <mj-section background-color="{{ theme.color.background_secondary|default:'#f9fafb' }}" padding="20px" border-radius="8px">
      <mj-column>
        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.primary|default:'#2563eb' }}" padding-bottom="5px">
          Ödeme Yöntemlerini Ayarlayın
        </mj-text>
        <mj-text font-size="14px">
          <strong>Ayarlar > Ödeme Sağlayıcıları</strong> bölümüne giderek Stripe, PayPal veya başka bir ödeme yöntemiyle bağlanın. Birden fazla sağlayıcıyı etkinleştirebilirsiniz ve müşterilerinize tercihlerine göre ödeme yapma imkanı tanıyabilirsiniz.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Tip 4: Shipping -->
    <mj-section>
      <mj-column>
        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.primary|default:'#2563eb' }}" padding-bottom="5px">
          Kargo Ayarlarını Yapılandırın
        </mj-text>
        <mj-text font-size="14px">
          <strong>Ayarlar > Kargo</strong> bölümüne giderek farklı bölgeler için kargo bölgelerinizi ve ücretlerinizi ayarlayın.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Tip 5: SEO -->
    <mj-section background-color="{{ theme.color.background_secondary|default:'#f9fafb' }}" padding="20px" border-radius="8px">
      <mj-column>
        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.primary|default:'#2563eb' }}" padding-bottom="5px">
          SEO'nuzu Geliştirin
        </mj-text>
        <mj-text font-size="14px">
          Spwig, sitemap ve meta etiketlerini otomatik olarak oluşturur. <strong>Ayarlar > SEO</strong> bölümüne giderek sayfa başlıklarını, açıklamalarını ve sosyal paylaşım görsellerinizi özelleştirerek müşterilerin mağazanızı bulmasını kolaylaştırabilirsiniz.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- CTA -->
    {% include 'email_system/mjml_components/cta_button.mjml' with url=admin_url text="Admin Paneline Git" %}

    <!-- Support -->
    {% include 'email_system/mjml_components/support_block.mjml' %}
  </mj-body>
</mjml>

## Text Content
Başlangıç İpuçları - {{ store_name }}

Merhaba {{ name|default:'there' }},

Artık {{ store_name }} çalışıyor. Mağazanızdan en çok yararlanmanıza yardımcı olmak için bazı ipuçları aşağıdadır.

1. Görünümünüzü Özelleştirin
Tasarım > Tema Ayarları bölümüne giderek bir tema seçin, logonuzu yükleyin ve marka renklerinizi ayarlayın.

2. Ürünlerinizi Ekleyin
Katalog > Ürünler bölümüne giderek ürün eklemeye başlayın. Boyut, renk gibi ürün varyasyyonları oluşturabilir, fiyatlandırabilir, stokları yönetebilir ve yüksek kaliteli görseller yükleyebilirsiniz.

3. Ödeme Yöntemlerini Ayarlayın
Ayarlar > Ödeme Sağlayıcıları bölümüne giderek Stripe, PayPal veya başka bir ödeme yöntemiyle bağlanın.

4. Kargo Ayarlarını Yapılandırın
Ayarlar > Kargo bölümüne giderek farklı bölgeler için kargo bölgelerinizi ve ücretlerinizi ayarlayın.

5. SEO'nuzu Geliştirin
Ayarlar > SEO bölümüne giderek sayfa başlıklarını, açıklamalarını ve sosyal paylaşım görsellerinizi özelleştirerek müşterilerin mağazanızı bulmasını kolaylaştırabilirsiniz.

Admin Paneline Git: {{ admin_url }}

Yardıma mı ihtiyacınız var? {{ support_email }} adresine ulaşın.