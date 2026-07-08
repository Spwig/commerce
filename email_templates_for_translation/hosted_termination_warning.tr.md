---
template_type: hosted_termination_warning
category: License
---

# Email Template: hosted_termination_warning

## Subject
Önemli: 7 Günde Veri Silme - {{ store_name }}

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
    <mj-section background-color="#dc2626" padding="30px 20px">
      <mj-column>
        <mj-text font-size="28px" font-weight="bold" color="#ffffff" align="center">
          Veri Silme Uyarısı
        </mj-text>
        <mj-text font-size="16px" color="#ffffffcc" align="center" padding-top="10px">
          {{ store_name }}
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
          Mağazanız <strong>{{ store_name }}</strong> ve tüm ilişkili verileriniz <strong>{{ termination_date }}</strong> tarihinde kalıcı olarak silinecektir. Bu işlem geri alınamaz.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- What You Can Do -->
    <mj-section background-color="{{ theme.color.background_secondary|default:'#f9fafb' }}" padding="20px" border-radius="8px">
      <mj-column>
        <mj-text font-size="16px" font-weight="bold" padding-bottom="10px">
          Yapabileceğinizler
        </mj-text>
        <mj-text font-size="14px">
          Verilerinizi korumak istiyorsanız, bu tarih önce verilerinizi dışa aktarın veya aboneliğinizi yeniden etkinleştirebilirsiniz.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- CTA -->
    {% include 'email_system/mjml_components/cta_button.mjml' with url="https://spwig.com/account" text="Aboneliği Yeniden Etkinleştir" %}

    <!-- Support -->
    {% include 'email_system/mjml_components/support_block.mjml' %}
  </mj-body>
</mjml>

## Text Content
Veri Silme Uyarısı - {{ store_name }}

Merhaba {{ name|default:'there' }},

Mağazanız {{ store_name }} ve tüm ilişkili verileriniz {{ termination_date }} tarihinde kalıcı olarak silinecektir. Bu işlem geri alınamaz.

Yapabileceğinizler:
Eğer verilerinizi korumak istiyorsanız, bu tarih önce verilerinizi dışa aktarın veya aboneliğinizi yeniden etkinleştirebilirsiniz.

Aboneliği Yeniden Etkinleştir: https://spwig.com/account

Yardıma mı ihtiyacınız var? {{ support_email }} adresine ulaşın