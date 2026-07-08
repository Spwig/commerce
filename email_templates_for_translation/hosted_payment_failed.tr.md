---
template_type: hosted_payment_failed
category: License
---

# Email Template: hosted_payment_failed

## Subject
Ödeme Başarısız - {{ store_name }}

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
    <mj-section background-color="#d97706" padding="30px 20px">
      <mj-column>
        <mj-text font-size="28px" font-weight="bold" color="#ffffff" align="center">
          Ödeme Sorunu
        </mj-text>
        <mj-text font-size="16px" color="#ffffffcc" align="center" padding-top="10px">
          {{ store_name }} için eylem gerekli
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
          {{ plan_name }} için ödeme işlemini gerçekleştiremeyiz.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Payment Details -->
    <mj-section background-color="{{ theme.color.background_secondary|default:'#f9fafb' }}" padding="20px" border-radius="8px">
      <mj-column>
        <mj-text font-size="16px" font-weight="bold" padding-bottom="10px">
          Ödeme Detayları
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          Tutar: {{ currency }}{{ amount }}
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          Plan: {{ plan_name }}
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Next Steps -->
    <mj-section>
      <mj-column>
        <mj-text>
          {{ retry_info }}. Hizmet kesilmemesi için lütfen ödeme yönteminizi güncelleyin.
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
Ödeme Sorunu - {{ store_name }}

Merhaba {{ name|default:'there' }},

{{ plan_name }} için ödeme işlemini gerçekleştiremeyiz.

Ödeme Detayları:
- Tutar: {{ currency }}{{ amount }}
- Plan: {{ plan_name }}

{{ retry_info }}. Hizmet kesilmemesi için lütfen ödeme yönteminizi güncelleyin.

Ödeme Yöntemini Güncelle: https://spwig.com/account

Yardıma mı ihtiyacınız var? {{ support_email }} ile iletişime geçin.