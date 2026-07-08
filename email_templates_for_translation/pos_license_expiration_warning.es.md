---
template_type: pos_license_expiration_warning
category: POS
---

# Email Template: pos_license_expiration_warning

## Subject
{% if is_grace_period %}[Periodo de gracia] Licencia POS - {{ days_remaining }} días restantes{% else %}[Próximo a expirar] Licencia POS - {{ days_remaining }} días restantes{% endif %}

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="{% if is_grace_period %}#fef2f2{% else %}#fffbeb{% endif %}">
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="{% if is_grace_period %}#991b1b{% else %}#92400e{% endif %}" align="center">
          {% if is_grace_period %}Periodo de gracia de la licencia POS{% else %}Licencia POS próxima a expirar{% endif %}
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          {% if is_grace_period %}El periodo de gracia de su licencia Spwig POS expira en <strong>{{ days_remaining }} día{{ days_remaining|pluralize }}</strong>. Una vez que termine el periodo de gracia, el acceso a la API POS se bloqueará.{% else %}Su licencia Spwig POS expira en <strong>{{ days_remaining }} día{{ days_remaining|pluralize }}</strong>.{% endif %}
        </mj-text>

        <mj-spacer height="20px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
              Detalles de la licencia:
            </mj-text>
            <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>Licencia:</strong> {{ license_key_masked }}<br/>
              <strong>Expira:</strong> {{ expires_at }}
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-button href="{{ renewal_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          Renovar licencia POS
        </mj-button>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
{% if is_grace_period %}PERÍODO DE GRACIA DE LA LICENCIA POS{% else %}LICENCIA POS PRÓXIMA A EXPIRAR{% endif %}

{% if is_grace_period %}El periodo de gracia de su licencia Spwig POS expira en {{ days_remaining }} día{{ days_remaining|pluralize }}. Una vez que termine el periodo de gracia, el acceso a la API POS se bloqueará.{% else %}Su licencia Spwig POS expira en {{ days_remaining }} día{{ days_remaining|pluralize }}.{% endif %}

DETALLES DE LA LICENCIA:
- Licencia: {{ license_key_masked }}
- Expira: {{ expires_at }}

Renove su licencia POS: {{ renewal_url }}