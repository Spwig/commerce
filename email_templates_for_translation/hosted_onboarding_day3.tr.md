---
template_type: hosted_onboarding_day3
category: License
---

# Email Template: hosted_onboarding_day3

## Subject
Kataloğunuzu Oluşturun - {{ store_name }}

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
          Başlangıç: Ürünleriniz
        </mj-text>
        <mj-text font-size="16px" color="#ffffffcc" align="center" padding-top="10px">
          {{ store_name }} için harika bir katalog oluşturun
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
          {{ store_name }} mağazanız tamamen kuruldu. Artık ürün kataloğunuza başlamak zamanı. Başlamak için beş ipucu aşağıdadır.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Tip 1 -->
    <mj-section background-color="{{ theme.color.background_secondary|default:'#f9fafb' }}" padding="20px" border-radius="8px">
      <mj-column>
        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.primary|default:'#2563eb' }}" padding-bottom="5px">
          CSV Dosyasından Ürünleri İçe Aktarın
        </mj-text>
        <mj-text font-size="14px">
          Zaten bir ürün listesi var mı? <strong>Yönetim > Katalog > İçe Aktar</strong> bölümüne giderek CSV dosyasından ürünleri toplu olarak içe aktarabilirsiniz. Bu, mağazanızı doldurmanın en hızlı yolu olacaktır.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Tip 2 -->
    <mj-section>
      <mj-column>
        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.primary|default:'#2563eb' }}" padding-bottom="5px">
          Kategoriler ve Filtrelerle Düzenleyin
        </mj-text>
        <mj-text font-size="14px">
          Müşterilerin kolayca taraması ve ihtiyaçlarını bulması için kategoriler ve öznitelik filtreleri oluşturun. İyi düzenlenmiş kataloglar daha yüksek dönüşüm oranlarına neden olur.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Tip 3 -->
    <mj-section background-color="{{ theme.color.background_secondary|default:'#f9fafb' }}" padding="20px" border-radius="8px">
      <mj-column>
        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.primary|default:'#2563eb' }}" padding-bottom="5px">
          Çekici Ürün Açıklamaları Yazın
        </mj-text>
        <mj-text font-size="14px">
          Harika açıklamalar ürünleri satar. Özellikler değil faydalar üzerine odaklanın. Müşterilere ürününüz neden gerekebilir ve sorunlarını nasıl çözebilir onları anlatın.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Tip 4 -->
    <mj-section>
      <mj-column>
        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.primary|default:'#2563eb' }}" padding-bottom="5px">
          Yüksek Kaliteli Ürün Görselleri Yükleme
        </mj-text>
        <mj-text font-size="14px">
          Net ve profesyonel görseller büyük fark yaratır. Farklı açıları yükleyin ve tutarlı aydınlatma kullanın. Spwig, görselleri hızlı yükleme için otomatik olarak optimize eder.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Tip 5 -->
    <mj-section background-color="{{ theme.color.background_secondary|default:'#f9fafb' }}" padding="20px" border-radius="8px">
      <mj-column>
        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.primary|default:'#2563eb' }}" padding-bottom="5px">
          Ürün Variantlarını Kurun
        </mj-text>
        <mj-text font-size="14px">
          Ürünleriniz farklı boyutlarda, renklerde veya stillerde gelirse, müşterilerin tam olarak istediğini seçebilmesi için variantlar oluşturun. Her variant kendi fiyatına, stok seviyesine ve görsellerine sahip olabilir.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- CTA -->
    {% include 'email_system/mjml_components/cta_button.mjml' with url=admin_url text="Ürünlerinizi Yönetin" %}

    <!-- Support -->
    {% include 'email_system/mjml_components/support_block.mjml' %}
  </mj-body>
</mjml>

## Text Content
Başlangıç: Ürünleriniz - {{ store_name }}

Merhaba {{ name|default:'there' }},

{{ store_name }} mağazanız tamamen kuruldu. Artık ürün kataloğunuza başlamak zamanı. Başlamak için beş ipucu aşağıdadır.

1. CSV Dosyasından Ürünleri İçe Aktarın
Zaten bir ürün listesi var mı? <strong>Yönetim > Katalog > İçe Aktar</strong> bölümüne giderek CSV dosyasından ürünleri toplu olarak içe aktarabilirsiniz.

2. Kategoriler ve Filtrelerle Düzenleyin
Müşterilerin kolayca taraması ve ihtiyaçlarını bulması için kategoriler ve öznitelik filtreleri oluşturun.

3. Çekici Ürün Açıklamaları Yazın
Harika açıklamalar ürünleri satar. Özellikler değil faydalar üzerine odaklanın. Müşterilere ürününüz neden gerekebilir onları anlatın.

4. Yüksek Kaliteli Ürün Görselleri Yükleme
Net ve profesyonel görseller büyük fark yaratır. Farklı açıları yükleyin ve tutarlı aydınlatma kullanın.

5. Ürün Variantlarını Kurun
Ürünleriniz farklı boyutlarda, renklerde veya stillerde gelirse, müşterilerin tam olarak istediğini seçebilmesi için variantlar oluşturun.

Ürünlerinizi Yönetin: {{ admin_url }}

Yardıma mı ihtiyacınız var? {{ support_email }} ile iletişime geçin