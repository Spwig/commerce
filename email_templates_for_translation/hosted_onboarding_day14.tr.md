---
template_type: hosted_onboarding_day14
category: License
---

# Email Template: hosted_onboarding_day14

## Subject
Daha İleri Git - {{ store_name }}

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
          Başlangıç: Gelişmiş Özellikler
        </mj-text>
        <mj-text font-size="16px" color="#ffffffcc" align="center" padding-top="10px">
          {{ store_name }}'in tam potansiyelini serbest bırakın
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
          {{ store_name }}'i birkaç hafta boyunca işletiyorsunuz. Mağazanızı bir sonraki seviyeye çıkarmak için size yardımcı olabilecek bazı gelişmiş özellikleri burada bulabilirsiniz.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Tip 1 -->
    <mj-section background-color="{{ theme.color.background_secondary|default:'#f9fafb' }}" padding="20px" border-radius="8px">
      <mj-column>
        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.primary|default:'#2563eb' }}" padding-bottom="5px">
          Otomatik E-posta Akışlarını Kurun
        </mj-text>
        <mj-text font-size="14px">
          Müşteri iletişiminizi otomatikleştirin. Hoş geldiniz akışlarını, satın alma sonrası takip kampanyalarını ve yeniden etkileşim kampanyalarını <strong>Marketing > E-posta Akışları</strong> altında kurun.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Tip 2 -->
    <mj-section>
      <mj-column>
        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.primary|default:'#2563eb' }}" padding-bottom="5px">
          Bölgeniz İçin Vergi Kurallarını Yapılandırın
        </mj-text>
        <mj-text font-size="14px">
          Doğru vergi oranlarını tahsil ettiğinizden emin olun. <strong>Ayarlar > Vergi</strong> bölümüne giderek satışı yaptığınız her bölge için vergi kurallarını yapılandırabilirsiniz. Vergi dahil veya vergi hariç fiyatlandırma ayarlayabilirsiniz.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Tip 3 -->
    <mj-section background-color="{{ theme.color.background_secondary|default:'#f9fafb' }}" padding="20px" border-radius="8px">
      <mj-column>
        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.primary|default:'#2563eb' }}" padding-bottom="5px">
          Entegrasyonlar İçin API'yi Keşfedin
        </mj-text>
        <mj-text font-size="14px">
          Planınız API erişimini içeriyorsa, mağazanızı harici araçlar ve hizmetlerle entegre edebilirsiniz. <strong>Ayarlar > API</strong> bölümüne giderek API anahtarları oluşturun ve belgeleri inceleyin.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Tip 4 -->
    <mj-section>
      <mj-column>
        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.primary|default:'#2563eb' }}" padding-bottom="5px">
          Analitik Dashboard'ınızı İnceleyin
        </mj-text>
        <mj-text font-size="14px">
          Mağazanızın performansını takip edin. <strong>Dashboard</strong> size gelir, siparişler, en iyi satan ürünler ve müşteri analizleri gibi ana metrikleri gösterir ve veri odaklı kararlar almanıza yardımcı olur.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Tip 5 -->
    <mj-section background-color="{{ theme.color.background_secondary|default:'#f9fafb' }}" padding="20px" border-radius="8px">
      <mj-column>
        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.primary|default:'#2563eb' }}" padding-bottom="5px">
          Mağaza Satışları İçin POS Ekleyin
        </mj-text>
        <mj-text font-size="14px">
          Kişisel satışlar da yapmak istiyorsanız? Spwig'in POS özelliği, mağaza satış işlemlerini çevrimiçi stok ve sipariş yönetimiyle senkronize eder. Daha fazla bilgi için <strong>Ayarlar > Satış Noktası</strong> bölümüne bakın.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- CTA -->
    {% include 'email_system/mjml_components/cta_button.mjml' with url=admin_url text="Dashboard'ınızı Keşfedin" %}

    <!-- Support -->
    {% include 'email_system/mjml_components/support_block.mjml' %}
  </mj-body>
</mjml>

## Text Content
Başlangıç: Gelişmiş Özellikler - {{ store_name }}

Merhaba {{ name|default:'there' }},

{{ store_name }}'i birkaç hafta boyunca işletiyorsunuz. Mağazanızı bir sonraki seviyeye çıkarmak için size yardımcı olabilecek bazı gelişmiş özellikleri burada bulabilirsiniz.

1. Otomatik E-posta Akışlarını Kurun
Hoş geldiniz akışlarını, satın alma sonrası takip kampanyalarını ve yeniden etkileşim kampanyalarını otomatikleştirin.

2. Bölgeniz İçin Vergi Kurallarını Yapılandırın
Doğru vergi oranlarını tahsil ettiğinizden emin olun. Ayarlar > Vergi bölümüne giderek her bölge için kuralları yapılandırın.

3. Entegrasyonlar İçin API'yi Keşfedin
Planınız API erişimini içeriyorsa, mağazanızı harici araçlarla entegre edin. Ayarlar > API bölümüne giderek başlayın.

4. Analitik Dashboard'ınızı İnceleyin
Dashboard, gelir, siparişler, en iyi satan ürünler ve müşteri analizleri gibi ana metrikleri gösterir.

5. Mağaza Satışları İçin POS Ekleyin
Kişisel satışlar da yapmak istiyorsanız? Spwig'in POS özelliği, mağaza satış işlemlerini çevrimiçi stokla senkronize eder.

Dashboard'ınızı Keşfedin: {{ admin_url }}

Yardıma mı ihtiyacınız var? {{ support_email }} ile iletişime geçin