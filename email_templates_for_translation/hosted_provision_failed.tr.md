---
template_type: hosted_provision_failed
category: License
---

# Email Template: hosted_provision_failed

## Subject
Gerekli Eylem - {{ store_name }} Mağaza Kurulumu Sorunu

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
    <mj-section background-color="{{ theme.color.error|default:'#dc2626' }}" padding="30px 20px">
      <mj-column>
        <mj-text font-size="28px" font-weight="bold" color="#ffffff" align="center">
          Mağaza Kurulumu Sorunu
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
          {{ store_name }} mağazanızın kurulumu sırasında bir sorunla karşılaştık. Ekibimiz haberdar edildi ve bununla ilgileniyor.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Error Details -->
    <mj-section background-color="#fef2f2" padding="20px" border-radius="8px">
      <mj-column>
        <mj-text font-size="14px" font-weight="bold" color="#991b1b" padding-bottom="10px">
          Ne oldu
        </mj-text>
        <mj-text font-size="14px" color="#7f1d1d">
          {{ provision_error }}
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- What's Next -->
    <mj-section>
      <mj-column>
        <mj-text font-size="16px" font-weight="bold" padding-bottom="10px">
          Sonra ne olur?
        </mj-text>
        <mj-text font-size="14px">
          Bu sorunla ilgili destek ekibimiz otomatik olarak haberdar edildi. Herhangi bir eylem gerekmez - sorun çözüldüğünde size ulaşacağız.
        </mj-text>
        <mj-text font-size="14px" padding-top="10px">
          Bu arada sorularınız olursa, lütfen bize ulaşmaktan çekinmeyin.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Support -->
    {% include 'email_system/mjml_components/support_block.mjml' %}
  </mj-body>
</mjml>

## Text Content
Mağaza Kurulumu Sorunu - {{ store_name }}

Merhaba {{ name|default:'there' }},

{{ store_name }} mağazanızın kurulumu sırasında bir sorunla karşılaştık. Ekibimiz haberdar edildi ve bununla ilgileniyor.

Ne oldu:
{{ provision_error }}

Sonra ne olur?
Bu sorunla ilgili destek ekibimiz otomatik olarak haberdar edildi. Herhangi bir eylem gerekmez - sorun çözüldüğünde size ulaşacağız.

Bu arada sorularınız olursa, lütfen bize ulaşmaktan çekinmeyin.

Yardıma mı ihtiyacınız var? {{ support_email }} adresine ulaşın