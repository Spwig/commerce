---
template_type: pos_license_expiration_warning
category: POS
---

# Email Template: pos_license_expiration_warning

## Subject
{% if is_grace_period %}[İndirim Periyodu] POS Lisansı - {{ days_remaining }} gün kalmış{% else %}[Yakında Bitiyor] POS Lisansı - {{ days_remaining }} gün kalmış{% endif %}

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="{% if is_grace_period %}#fef2f2{% else %}#fffbeb{% endif %}">
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="{% if is_grace_period %}#991b1b{% else %}#92400e{% endif %}" align="center">
          {% if is_grace_period %}POS Lisansı İndirim Periyodu{% else %}POS Lisansı Yakında Bitiyor{% endif %}
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          {% if is_grace_period %}Spwig POS lisansınızın indirim periyodu <strong>{{ days_remaining }} gün{{ days_remaining|pluralize }}</strong> sonra sona erecek. İndirim periyodu bittikten sonra POS API erişimi engellenecektir.{% else %}Spwig POS lisansınız <strong>{{ days_remaining }} gün{{ days_remaining|pluralize }}</strong> sonra sona erecek.{% endif %}
        </mj-text>

        <mj-spacer height="20px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
              Lisans Detayları:
            </mj-text>
            <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>Lisans:</strong> {{ license_key_masked }}<br/>
              <strong>Sona Eren Tarih:</strong> {{ expires_at }}
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-button href="{{ renewal_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          POS Lisansını Yenile
        </mj-button>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
{% if is_grace_period %}POS LISANS İNDİRİM PERİYODU{% else %}POS LISANS YAKINDA BİTECEK{% endif %}

{% if is_grace_period %}Spwig POS lisansınızın indirim periyodu {{ days_remaining }} gün{{ days_remaining|pluralize }} sonra sona erecek. İndirim periyodu bittikten sonra POS API erişimi engellenecektir.{% else %}Spwig POS lisansınız {{ days_remaining }} gün{{ days_remaining|pluralize }} sonra sona erecek.{% endif %}

LİSANS DETAYLARI:
- Lisans: {{ license_key_masked }}
- Sona Eren Tarih: {{ expires_at }}

POS lisansınızı yenileyin: {{ renewal_url }}