---
template_type: hosted_interval_changed
category: License
---

# Email Template: hosted_interval_changed

## Subject
Fatura Güncellendi - {{ store_name }}

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
          Fatura Güncellendi
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
          {{ store_name }} üzerindeki <strong>{{ plan_name }}</strong> planınız için fatura aralığı güncellendi.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Billing Details -->
    <mj-section background-color="{{ theme.color.background_secondary|default:'#f9fafb' }}" padding="20px" border-radius="8px">
      <mj-column>
        <mj-text font-size="16px" font-weight="bold" padding-bottom="10px">
          Fatura Detayları
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          Plan: {{ plan_name }}
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          Önceki Fatura Aralığı: {{ old_interval }}
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          Yeni Fatura Aralığı: {{ new_interval }}
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          Bir Sonraki Fatura Tarihi: {{ next_billing_date }}
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Additional Info -->
    <mj-section>
      <mj-column>
        <mj-text>
          Abonelik hâlâ aktif. Hesabınızdan herhangi bir zamanda fatura tercihlerinizi yönetebilirsiniz.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- CTA -->
    {% include 'email_system/mjml_components/cta_button.mjml' with url="https://spwig.com/account" text="Abonelik Yönet" %}

    <!-- Support -->
    {% include 'email_system/mjml_components/support_block.mjml' %}
  </mj-body>
</mjml>

## Text Content
Fatura Güncellendi - {{ store_name }}

Merhaba,

{{ store_name }} üzerindeki {{ plan_name }} planınız için fatura aralığı güncellendi.

Fatura Detayları:
- Plan: {{ plan_name }}
- Önceki Fatura Aralığı: {{ old_interval }}
- Yeni Fatura Aralığı: {{ new_interval }}
- Bir Sonraki Fatura Tarihi: {{ next_billing_date }}

Abonelik hâlâ aktif. Hesabınızdan herhangi bir zamanda fatura tercihlerinizi yönetebilirsiniz.

Abonelik Yönet: https://spwig.com/account

Yardıma mı ihtiyacınız var? {{ support_email }} adresine ulaşın.