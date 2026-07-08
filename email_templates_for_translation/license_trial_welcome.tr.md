---
template_type: license_trial_welcome
category: License
---

# Email Template: license_trial_welcome

## Subject
Spwig'a Hoş geldiniz - {{ trial_days }} Gün Ücretsiz Deneme

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
    <mj-section background-color="#059669" padding="30px 20px">
      <mj-column>
        <mj-text font-size="28px" font-weight="bold" color="#ffffff" align="center">
          Spwig'a Hoş geldiniz!
        </mj-text>
        <mj-text font-size="16px" color="#ffffffcc" align="center" padding-top="10px">
          {{ trial_days }}-gün ücretsiz denemeniz hazırdır
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
          <strong>{{ product_name }}</strong> denememiz için teşekkür ederiz! Denemeniz etkinleştirildi ve Spwig'in sunduğu tüm özellikleri {{ trial_days }} gün içinde keşfetme şansınız vardır{% if includes_pos %}, satış noktası (POS) sistemi de dahil{% endif %}.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Setup Token Box -->
    <mj-section background-color="#f0fdf4" padding="25px" border-radius="8px">
      <mj-column>
        <mj-text font-size="12px" color="#065f46" font-weight="bold" align="center">
          KURULUM TOKEN'INIZ
        </mj-text>
        <mj-text font-size="14px" font-weight="bold" color="#059669" align="center" font-family="'Courier New', monospace" padding="10px 0" word-break="break-all">
          {{ setup_token }}
        </mj-text>
        <mj-text font-size="12px" color="{{ theme.color.text_muted|default:'#6b7280' }}" align="center">
          Kurulum sırasında bu tokenı kullanarak deneme mağazanızı etkinleştirebilirsiniz
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
          1. Spwig'i sunucunuzda kurmak için kurulum kılavuzumuzu takip edin
        </mj-text>
        <mj-text font-size="14px">
          2. Kurulum sırasında istendiğinde kurulum token'ınızı girin
        </mj-text>
        <mj-text font-size="14px">
          3. Online mağazanızı inşa etmeye başlayın!
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Setup Guide CTA -->
    {% include 'email_system/mjml_components/cta_button.mjml' with url=setup_url text="Kurulum Kılavuzunu Gör" %}

    <!-- What's Included -->
    <mj-section background-color="{{ theme.color.background_secondary|default:'#f9fafb' }}" padding="20px" border-radius="8px">
      <mj-column>
        <mj-text font-size="16px" font-weight="bold" padding-bottom="10px">
          Denemenizde Ne Dahil?
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          Tüm temel özelliklere {{ trial_days }} gün boyunca tam erişim
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          Ürün kataloğu, siparişler ve müşteri yönetimi
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          Tema özelleştirmesi ve sayfa inşası
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          Ödeme ve kargo sağlayıcı entegrasyonları
        </mj-text>
        {% if includes_pos %}
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          Satış Noktası (POS) sistemi
        </mj-text>
        {% endif %}
      </mj-column>
    </mj-section>

    <!-- Trial Info -->
    <mj-section>
      <mj-column>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          Denemeniz {{ trial_days }} gün sonra sona erecektir. Hazır olduğunuzda, mağazanızı veri kaybı olmadan çalıştırabilmek için tam lisansa yükseltin.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Support -->
    {% include 'email_system/mjml_components/support_block.mjml' %}
  </mj-body>
</mjml>

## Text Content
Spwig'a Hoş geldiniz!
{{ trial_days }}-gün ücretsiz denemeniz hazırdır.

Merhaba {{ customer_name }},

{{ product_name }} denememiz için teşekkür ederiz! Denemeniz etkinleştirildi ve Spwig'in sunduğu tüm özellikleri {{ trial_days }} gün içinde keşfetme şansınız vardır{% if includes_pos %}, satış noktası (POS) sistemi de dahil{% endif %}.

KURULUM TOKEN'INIZ:
{{ setup_token }}
Kurulum sırasında bu tokenı kullanarak deneme mağazanızı etkinleştirebilirsiniz.

Başlangıç:
1. Spwig'i sunucunuzda kurmak için kurulum kılavuzumuzu takip edin
2. Kurulum sırasında istendiğinde kurulum token'ınızı girin
3. Online mağazanızı inşa etmeye başlayın!

Kurulum Kılavuzunu Gör: {{ setup_url }}

Denemenizde Ne Dahil:
- Tüm temel özelliklere {{ trial_days }} gün boyunca tam erişim
- Ürün kataloğu, siparişler ve müşteri yönetimi
- Tema özelleştirmesi ve sayfa inşası
- Ödeme ve kargo sağlayıcı entegrasyonları
{% if includes_pos %}- Satış Noktası (POS) sistemi{% endif %}

Denemeniz {{ trial_days }} gün sonra sona erecektir. Hazır olduğunuzda, mağazanızı veri kaybı olmadan çalıştırabilmek için tam lisansa yükseltin.

Yardıma mı ihtiyacınız var? {{ support_email }} ile iletişime geçin