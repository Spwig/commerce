---
template_type: license_purchase_confirmation
category: License
---

# Email Template: license_purchase_confirmation

## Subject
Spwig Lisansınız - Sipariş #{{ order_number }}

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
          Alışverişınız için teşekkür ederiz!
        </mj-text>
        <mj-text font-size="16px" color="#ffffffcc" align="center" padding-top="10px">
          Sipariş #{{ order_number }}
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Greeting -->
    <mj-section>
      <mj-column>
        <mj-text font-size="16px">
          Merhaba {{ customer_name }},
        </mj-text>
        <mj-text>
          {{ product_name }} alımınız tamamlandı. Aşağıda lisans anahtarınızı ve kurulum tokenınızı bulacaksınız.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Order Summary -->
    <mj-section background-color="{{ theme.color.background_secondary|default:'#f9fafb' }}" padding="20px" border-radius="8px">
      <mj-column>
        <mj-text font-size="16px" font-weight="bold" padding-bottom="10px">
          Sipariş Özeti
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          Ürün: {{ product_name }}{% if includes_pos %} (POS içerir){% endif %}
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          Tutar: {{ price }}
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          Sipariş Numarası: {{ order_number }}
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- License Key Box -->
    <mj-section background-color="#eff6ff" padding="25px" border-radius="8px">
      <mj-column>
        <mj-text font-size="12px" color="#1e40af" font-weight="bold" align="center">
          LİSANS ANAHTARINIZ
        </mj-text>
        <mj-text font-size="18px" font-weight="bold" color="{{ theme.color.primary|default:'#2563eb' }}" align="center" font-family="'Courier New', monospace" padding="10px 0">
          {{ license_key }}
        </mj-text>
        <mj-text font-size="12px" color="{{ theme.color.text_muted|default:'#6b7280' }}" align="center">
          Bu anahtarı saklayınız - yeniden kurulum için gerekecektir
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Setup Token Box -->
    <mj-section background-color="#f0fdf4" padding="25px" border-radius="8px">
      <mj-column>
        <mj-text font-size="12px" color="#065f46" font-weight="bold" align="center">
          KURULUM TOKENINIZ
        </mj-text>
        <mj-text font-size="14px" font-weight="bold" color="#059669" align="center" font-family="'Courier New', monospace" padding="10px 0" word-break="break-all">
          {{ setup_token }}
        </mj-text>
        <mj-text font-size="12px" color="{{ theme.color.text_muted|default:'#6b7280' }}" align="center">
          Kurulum sırasında bu tokenı kullanarak mağazanızı aktifleştirebilirsiniz
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Getting Started -->
    <mj-section>
      <mj-column>
        <mj-text font-size="16px" font-weight="bold" padding-bottom="10px">
          Başlangıç
        </mj-text>
        <mj-text font-size="14px">
          1. Spwig'i sunucunuza kurmak için kurulum kılavuzunu takip edin
        </mj-text>
        <mj-text font-size="14px">
          2. Kurulum sırasında istendiğinde kurulum tokenınızı girin
        </mj-text>
        <mj-text font-size="14px">
          3. Mağazanız otomatik olarak aktif hale gelecektir
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Setup Guide CTA -->
    {% include 'email_system/mjml_components/cta_button.mjml' with url=setup_url text="Kurulum Kılavuzunu Gör" %}

    {% if activation_url %}
    <!-- Guest Account Activation -->
    <mj-section background-color="{{ theme.color.background|default:'#ffffff' }}" padding="20px 20px 10px">
      <mj-column>
        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}" align="center">
          Hesabınızı Oluşturun
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}" align="center" padding-top="5px">
          Şifre belirleyerek lisanslarınızı yönetin, indirimlere erişin ve güncellemeleri alın.
        </mj-text>
      </mj-column>
    </mj-section>
    {% include 'email_system/mjml_components/cta_button.mjml' with url=activation_url text="Hesabınızı Oluşturun" %}
    {% endif %}

    <!-- Important Notice -->
    <mj-section>
      <mj-column>
        <mj-text font-size="14px" color="{{ theme.color.warning|default:'#d97706' }}" font-weight="bold">
          Önemli:
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          Bu e-postayı koruyun - gelecekte lisans anahtarınızı ve kurulum tokenınızı içermektedir. Bu kimlik bilgilerini başkalarıyla paylaşmayın.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Support -->
    {% include 'email_system/mjml_components/support_block.mjml' %}
  </mj-body>
</mjml>

## Text Content
Alışverişınız için teşekkür ederiz!

Sipariş #{{ order_number }}

Merhaba {{ customer_name }},

{{ product_name }} alımınız tamamlandı. Aşağıda lisans anahtarınızı ve kurulum tokenınızı bulacaksınız.

Sipariş Özeti:
- Ürün: {{ product_name }}{% if includes_pos %} (POS içerir){% endif %}
- Tutar: {{ price }}
- Sipariş Numarası: {{ order_number }}

LİSANS ANAHTARINIZ:
{{ license_key }}
Bu anahtarı saklayınız - yeniden kurulum için gerekecektir.

KURULUM TOKENINIZ:
{{ setup_token }}
Kurulum sırasında bu tokenı kullanarak mağazanızı aktifleştirebilirsiniz.

Başlangıç:
1. Spwig'i sunucunuza kurmak için kurulum kılavuzunu takip edin
2. Kurulum sırasında istendiğinde kurulum tokenınızı girin
3. Mağazanız otomatik olarak aktif hale gelecektir

Kurulum Kılavuzunu Gör: {{ setup_url }}
{% if activation_url %}
Hesabınızı Oluşturun:
Şifre belirleyerek lisanslarınızı yönetin, indirimlere erişin ve güncellemeleri alın.
{{ activation_url }}
{% endif %}
Önemli:
Bu e-postayı koruyun - gelecekte lisans anahtarınızı ve kurulum tokenınızı içermektedir. Bu kimlik bilgilerini başkalarıyla paylaşmayın.

Yardıma mı ihtiyacınız var? {{ support_email }}