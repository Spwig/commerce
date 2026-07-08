---
template_type: hosted_suspension_warning
category: License
---

# Email Template: hosted_suspension_warning

## Subject
Gerekli Eylem - {{ store_name }}

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
    <mj-section background-color="#ea580c" padding="30px 20px">
      <mj-column>
        <mj-text font-size="28px" font-weight="bold" color="#ffffff" align="center">
          Askı Uyarısı
        </mj-text>
        <mj-text font-size="16px" color="#ffffffcc" align="center" padding-top="10px">
          {{ store_name }} için gerekli eylem
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
          {{ plan_name }} ödemenniz gecikmiş. Eğer <strong>{{ grace_end_date }}</strong> tarihine kadar çözülmezse mağazanız sadece okunabilir modda olacak.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- What Suspension Means -->
    <mj-section background-color="{{ theme.color.background_secondary|default:'#f9fafb' }}" padding="20px" border-radius="8px">
      <mj-column>
        <mj-text font-size="16px" font-weight="bold" padding-bottom="10px">
          Askı Ne Anlama Geliyor
        </mj-text>
        <mj-text font-size="14px">
          Mağazanız askıya alınırsa ziyaretçiler tarafından görülebilir olmaya devam edecek ancak değişiklikler yapamayacaksınız. Kalan borcunuz ödenene kadar yeni siparişler duraklatılacaktır.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Resolve -->
    <mj-section>
      <mj-column>
        <mj-text>
          Mağazanızda herhangi bir kesinti olmaması için lütfen ödeme yönteminizi güncelleyin.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- CTA -->
    {% include 'email_system/mjml_components/cta_button.mjml' with url="https://spwig.com/account" text="Ödeme Yöntemini Güncelle" %}

    <!-- Support -->
    {% include 'email_system/mjml_components/support_block.mjml' %}
  </mj-body>
</mjml>

## Text Content
Askı Uyarısı - {{ store_name }}

Merhaba {{ name|default:'there' }},

{{ plan_name }} ödemenniz gecikmiş. Eğer {{ grace_end_date }} tarihine kadar çözülmezse mağazanız sadece okunabilir modda olacak.

Askı Ne Anlama Geliyor:
Mağazanız askıya alınırsa ziyaretçiler tarafından görülebilir olmaya devam edecek ancak değişiklikler yapamayacaksınız. Kalan borcunuz ödenene kadar yeni siparişler duraklatılacaktır.

Mağazanızda herhangi bir kesinti olmaması için lütfen ödeme yönteminizi güncelleyin.

Ödeme Yöntemini Güncelle: https://spwig.com/account

Yardıma mı ihtiyacınız var? {{ support_email }} ile iletişime geçin.