---
template_type: hosted_onboarding_day7
category: License
---

# Email Template: hosted_onboarding_day7

## Subject
Satışlarınızı Artırın - {{ store_name }}

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
          Başlangıç: Pazarlama & Büyüme
        </mj-text>
        <mj-text font-size="16px" color="#ffffffcc" align="center" padding-top="10px">
          {{ store_name }}'a trafiği ve satışları artırın
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
          {{ store_name }} artık şekillenmeye başladı, şimdi trafiği artırma ve satışlarınızı büyütmeye odaklanma zamanı. Başlamak için beş pazarlama ipucu aşağıdadır.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Tip 1 -->
    <mj-section background-color="{{ theme.color.background_secondary|default:'#f9fafb' }}" padding="20px" border-radius="8px">
      <mj-column>
        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.primary|default:'#2563eb' }}" padding-bottom="5px">
          İlk İndirim Kodunu Oluştur
        </mj-text>
        <mj-text font-size="14px">
          İlk müşterilerinizi çekmek için bir lansman indirimi sunun. <strong>Pazarlama > İndirim Kodları</strong> bölümüne giderek, kullanım sınırlamaları ve son tarihlerle birlikte yüzdelik veya sabit tutarlı indirimler oluşturabilirsiniz.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Tip 2 -->
    <mj-section>
      <mj-column>
        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.primary|default:'#2563eb' }}" padding-bottom="5px">
          Bırakılan Sepet Geri Kazanımı Ayarla
        </mj-text>
        <mj-text font-size="14px">
          Kayıp satışları otomatik olarak geri kazanın. <strong>Pazarlama > Bırakılan Sepetler</strong> altında bırakılan sepet geri kazanım e-postalarını etkinleştirin.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Tip 3 -->
    <mj-section background-color="{{ theme.color.background_secondary|default:'#f9fafb' }}" padding="20px" border-radius="8px">
      <mj-column>
        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.primary|default:'#2563eb' }}" padding-bottom="5px">
          Sosyal Medya Hesaplarını Bağla
        </mj-text>
        <mj-text font-size="14px">
          Mağazanızla sosyal medya profillerinizi bağlayarak müşterilerin size ulaşabilmesini sağlayın. <strong>Ayarlar > Sosyal Medya</strong> altında sosyal bağlantıları ekleyerek onları mağaza alt bilgisinde görüntüleyebilirsiniz.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Tip 4 -->
    <mj-section>
      <mj-column>
        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.primary|default:'#2563eb' }}" padding-bottom="5px">
          Google Analytics Takibi Kur
        </mj-text>
        <mj-text font-size="14px">
          Ziyaretçilerinizin nereden geldiğini ve mağazanızla nasıl etkileşime girdiğini anlayın. <strong>Ayarlar > Analiz</strong> altında Google Analytics takip kimliğinizi ekleyerek veri toplamaya başlayın.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Tip 5 -->
    <mj-section background-color="{{ theme.color.background_secondary|default:'#f9fafb' }}" padding="20px" border-radius="8px">
      <mj-column>
        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.primary|default:'#2563eb' }}" padding-bottom="5px">
          Haberleşme Listesi Kaydı Oluştur
        </mj-text>
        <mj-text font-size="14px">
          İlk günden itibaren e-posta listesinizi oluşturun. Mağazanıza bir haberleşme listesi kaydı formu ekleyerek ziyaretçilerin e-postalarını toplayın. Bu iletişimleri kampanyalar, ürün tanıtımı ve müşteri etkileşimi için kullanın.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- CTA -->
    {% include 'email_system/mjml_components/cta_button.mjml' with url=admin_url text="Pazarlamaya Git" %}

    <!-- Support -->
    {% include 'email_system/mjml_components/support_block.mjml' %}
  </mj-body>
</mjml>

## Text Content
Başlangıç: Pazarlama & Büyüme - {{ store_name }}

Merhaba {{ name|default:'there' }},

{{ store_name }} artık şekillenmeye başladı, şimdi trafiği artırma ve satışlarınızı büyütmeye odaklanma zamanı. Başlamak için beş pazarlama ipucu aşağıdadır.

1. İlk İndirim Kodunu Oluştur
İlk müşterilerinizi çekmek için bir lansman indirimi sunun. Pazarlama > İndirim Kodları bölümüne giderek, kullanım sınırlamaları ve son tarihlerle birlikte yüzdelik veya sabit tutarlı indirimler oluşturabilirsiniz.

2. Bırakılan Sepet Geri Kazanımı Ayarla
Kayıp satışları otomatik olarak geri kazanın. Pazarlama > Bırakılan Sepetler altında bırakılan sepet geri kazanım e-postalarını etkinleştirin.

3. Sosyal Medya Hesaplarını Bağla
Mağazanızla sosyal medya profillerinizi bağlayarak müşterilerin size ulaşabilmesini sağlayın. Ayarlar > Sosyal Medya altında sosyal bağlantıları ekleyerek onları mağaza alt bilgisinde görüntüleyebilirsiniz.

4. Google Analytics Takibi Kur
Ziyaretçilerinizin nereden geldiğini ve mağazanızla nasıl etkileşime girdiğini anlayın. Ayarlar > Analiz altında Google Analytics takip kimliğinizi ekleyerek veri toplamaya başlayın.

5. Haberleşme Listesi Kaydı Oluştur
İlk günden itibaren e-posta listesinizi oluşturun. Mağazanıza bir haberleşme listesi kaydı formu ekleyerek ziyaretçilerin e-postalarını toplayın. Bu iletişimleri kampanyalar, ürün tanıtımı ve müşteri etkileşimi için kullanın.

Pazarlamaya Git: {{ admin_url }}

Yardıma mı ihtiyacınız var? {{ support_email }} ile iletişime geçin