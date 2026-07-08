---
template_type: pos_license_expiration_warning
category: POS
---

# Email Template: pos_license_expiration_warning

## Subject
{% if is_grace_period %}[Période de grâce] Licence POS - {{ days_remaining }} jours restants{% else %}[Bientôt expirée] Licence POS - {{ days_remaining }} jours restants{% endif %}

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="{% if is_grace_period %}#fef2f2{% else %}#fffbeb{% endif %}">
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="{% if is_grace_period %}#991b1b{% else %}#92400e{% endif %}" align="center">
          {% if is_grace_period %}Période de grâce de la licence POS{% else %}La licence POS va bientôt expirer{% endif %}
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          {% if is_grace_period %}La période de grâce de votre licence Spwig POS expire dans <strong>{{ days_remaining }} jour{{ days_remaining|pluralize }}</strong>. Une fois que la période de grâce se termine, l'accès à l'API POS sera bloqué.{% else %}Votre licence Spwig POS expire dans <strong>{{ days_remaining }} jour{{ days_remaining|pluralize }}</strong>.{% endif %}
        </mj-text>

        <mj-spacer height="20px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
              Détails de la licence :
            </mj-text>
            <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>License :</strong> {{ license_key_masked }}<br/>
              <strong>Expires :</strong> {{ expires_at }}
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-button href="{{ renewal_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          Renouveler la licence POS
        </mj-button>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
{% if is_grace_period %}PÉRIODE DE GRÂCE DE LA LICENCE POS{% else %}LA LICENCE POS VA BIENTÔT EXPIRER{% endif %}

{% if is_grace_period %}La période de grâce de votre licence Spwig POS expire dans {{ days_remaining }} jour{{ days_remaining|pluralize }}. Une fois que la période de grâce se termine, l'accès à l'API POS sera bloqué.{% else %}Votre licence Spwig POS expire dans {{ days_remaining }} jour{{ days_remaining|pluralize }}.{% endif %}

DÉTAILS DE LA LICENCE:
- License: {{ license_key_masked }}
- Expires: {{ expires_at }}

Renouveler votre licence POS: {{ renewal_url }}