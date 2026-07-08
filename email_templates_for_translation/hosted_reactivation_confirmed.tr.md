---
template_type: hosted_reactivation_confirmed
category: License
---

# Email Template: hosted_reactivation_confirmed

## Subject
Hoş geldiniz! {{ store_name }} tekrar aktif

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
          Hoş geldiniz!
        </mj-text>
        <mj-text font-size="16px" color="#ffffffcc" align="center" padding-top="10px">
          {{ store_name }} tekrar aktif
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
          Harika haber! {{ store_name }} mağazanız tekrar aktif hale getirildi. {{ plan_name }} abonelik hizmetiniz artık aktif ve mağazanız çevrimiçi hale gelecek.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Reactivation Details -->
    <mj-section background-color="{{ theme.color.background_secondary|default:'#f9fafb' }}" padding="20px" border-radius="8px">
      <mj-column>
        <mj-text font-size="16px" font-weight="bold" padding-bottom="10px">
          Aktifleştirme Detayları
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          Plan: {{ plan_name }}
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          İşlem Gözden Geçirildi: {{ currency }}{{ amount }}
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          Bir Sonraki Fatura Tarihi: {{ next_billing_date }}
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- What Happens Now -->
    <mj-section>
      <mj-column>
        <mj-text>
          Mağazanız şu anda çevrimiçi hale geliyor. Her şeyin tamamen geri dönmesi birkaç dakika sürebilir. Aktif hale geldikten sonra mağazanız {{ store_url }} adresinden erişilebilir olacak.
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
Hoş geldiniz! {{ store_name }} tekrar aktif

Merhaba,

Harika haber! {{ store_name }} mağazanız tekrar aktif hale getirildi. {{ plan_name }} abonelik hizmetiniz artık aktif ve mağazanız çevrimiçi hale gelecek.

Aktifleştirme Detayları:
- Plan: {{ plan_name }}
- İşlem Gözden Geçirildi: {{ currency }}{{ amount }}
- Bir Sonraki Fatura Tarihi: {{ next_billing_date }}

Mağazanız şu anda çevrimiçi hale geliyor. Her şeyin tamamen geri dönmesi birkaç dakika sürebilir. Aktif hale geldikten sonra mağazanız {{ store_url }} adresinden erişilebilir olacak.

Mağazanıza Git: {{ admin_url }}

Yardım mı istiyorsunuz? {{ support_email }} adresine ulaşın.