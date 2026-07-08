---
template_type: hosted_payment_method_updated
category: License
---

# Email Template: hosted_payment_method_updated

## Subject
Ödeme Yöntemi Güncellendi - {{ store_name }}

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
    <mj-section background-color="#16a34a" padding="30px 20px">
      <mj-column>
        <mj-text font-size="28px" font-weight="bold" color="#ffffff" align="center">
          Ödeme Yöntemi Güncellendi
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
          Merhaba,
        </mj-text>
        <mj-text>
          {{ store_name }} üzerindeki <strong>{{ plan_name }}</strong> planınız için ödeme yöntemi başarıyla güncellendi.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Security Notice -->
    <mj-section background-color="{{ theme.color.background_secondary|default:'#f9fafb' }}" padding="20px" border-radius="8px">
      <mj-column>
        <mj-text font-size="16px" font-weight="bold" padding-bottom="10px">
          Bu Değişikliği Yapmadınız mı?
        </mj-text>
        <mj-text font-size="14px">
          Ödeme yönteminizi güncellememişseniz, hesabınızı güvence altına alabilmemiz için hemen destek ekibimizle iletişime geçiniz.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- CTA -->
    {% include 'email_system/mjml_components/cta_button.mjml' with url=admin_url text="Go to Your Store" %}

    <!-- Support -->
    {% include 'email_system/mjml_components/support_block.mjml' %}
  </mj-body>
</mjml>

## Text Content
Ödeme Yöntemi Güncellendi - {{ store_name }}

Merhaba,

{{ store_name }} üzerindeki {{ plan_name }} planınız için ödeme yöntemi başarıyla güncellendi.

Bu Değişikliği Yapmadınız mı?
Eğer ödeme yönteminizi güncellememişseniz, hesabınızı güvence altına alabilmemiz için hemen destek ekibimizle iletişime geçiniz.

Mağazanıza Git: {{ admin_url }}

Yardıma mı ihtiyacınız var? {{ support_email }} ile iletişime geçin.