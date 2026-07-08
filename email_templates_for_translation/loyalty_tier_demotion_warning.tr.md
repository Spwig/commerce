---
template_type: loyalty_tier_demotion_warning
category: Loyalty Program
---

# Email Template: loyalty_tier_demotion_warning

## Subject
⚠️ {{ current_tier }} Durumu Yakında Bitiyor - {{ shop_name }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#fef3c7">
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="#92400e" align="center">
          ⚠️ Tier Durumu Bitmek Üzere
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          {{ current_tier }} Faydalarınızı Kaybetmeyin!
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Merhaba {{ customer_name }},
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          {{ current_tier }} seviyeniz, {{ expiry_date }} tarihine kadar aktif kalacaktır, ancak aktivite seviyenizi korumayınca bu tarihte sona erecektir.
        </mj-text>

        <mj-spacer height="30px" />

        <mj-section background-color="#fee2e2" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="#991b1b">
              Mevcut Durum:
            </mj-text>
            <mj-text color="#7f1d1d">
              <strong>Mevcut Tier:</strong> {{ current_tier }}<br/>
              <strong>Sona Erecektir:</strong> {{ expiry_date }} ({{ days_remaining }} gün)<br/>
              <strong>Bir Sonraki Tier:</strong> {{ next_tier }}
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          {{ current_tier }} Durumunu Nasıl Koruyabilirsiniz:
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}" line-height="1.8">
          {{ expiry_date }} tarihinden önce {{ requirement_type }} yapmanız gerekir:
        </mj-text>

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-size="18px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}" align="center">
              {{ requirement_description }}
            </mj-text>
            <mj-text font-size="14px" color="{{ theme.color.text_secondary|default:'#6b7280' }}" align="center">
              Mevcut: {{ current_progress }} | Gerekli: {{ required_amount }}
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Kaybedeceğiniz Faydalar:
        </mj-text>

        <mj-text font-size="14px" color="{{ theme.color.text|default:'#4b5563' }}" line-height="1.8">
          {% for benefit in tier_benefits %}
          • {{ benefit }}<br/>
          {% endfor %}
        </mj-text>

        <mj-spacer height="30px" />

        <mj-button href="{{ shop_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          Şimdi Alışveriş Yapın & Durumunuzu Koruyun
        </mj-button>

        <mj-spacer height="20px" />

        <mj-button href="{{ loyalty_dashboard_url }}" background-color="#6b7280" color="#ffffff" font-size="14px" border-radius="6px" padding="10px 25px">
          Tam Bilgiyi Görüntüleyin
        </mj-button>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
⚠️ TIER DURUMU SONA ERMELİYOR

{{ current_tier }} Faydalarınızı Kaybetmeyin!

Merhaba {{ customer_name }},

{{ current_tier }} seviyeniz, {{ expiry_date }} tarihine kadar aktif kalacaktır, ancak aktivite seviyenizi korumayınca bu tarihte sona erecektir.

MEVCUT DURUM:
- Mevcut Tier: {{ current_tier }}
- Sona Erecektir: {{ expiry_date }} ({{ days_remaining }} gün)
- Bir Sonraki Tier: {{ next_tier }}

{{ current_tier }} DURUMUNU NASIL KORUYABİLİRSİNİZ:
{{ expiry_date }} tarihinden önce {{ requirement_type }} yapmanız gerekir:

{{ requirement_description }}
Mevcut: {{ current_progress }} | Gerekli: {{ required_amount }}

KAYBEDECEĞİNİZ FAYDALAR:
{% for benefit in tier_benefits %}
• {{ benefit }}
{% endfor %}

Şimdi alışveriş yapın & durumunuzu koruyun: {{ shop_url }}
Tam bilgiyi görüntüleyin: {{ loyalty_dashboard_url }}