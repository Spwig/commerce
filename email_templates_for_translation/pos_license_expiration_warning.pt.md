---
template_type: pos_license_expiration_warning
category: POS
---

# Email Template: pos_license_expiration_warning

## Subject
{% if is_grace_period %}[Período de Graça] Licença POS - {{ days_remaining }} dias restantes{% else %}[Expirando em Breve] Licença POS - {{ days_remaining }} dias restantes{% endif %}

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="{% if is_grace_period %}#fef2f2{% else %}#fffbeb{% endif %}">
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="{% if is_grace_period %}#991b1b{% else %}#92400e{% endif %}" align="center">
          {% if is_grace_period %}Período de Graça da Licença POS{% else %}Licença POS Expirando em Breve{% endif %}
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          {% if is_grace_period %}O período de graça da sua licença Spwig POS expira em <strong>{{ days_remaining }} dia{{ days_remaining|pluralize }}</strong>. Após o término do período de graça, o acesso à API POS será bloqueado.{% else %}Sua licença Spwig POS expira em <strong>{{ days_remaining }} dia{{ days_remaining|pluralize }}</strong>.{% endif %}
        </mj-text>

        <mj-spacer height="20px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
              Detalhes da Licença:
            </mj-text>
            <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>Licença:</strong> {{ license_key_masked }}<br/>
              <strong>Expira:</strong> {{ expires_at }}
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-button href="{{ renewal_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          Renovar Licença POS
        </mj-button>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
{% if is_grace_period %}PERÍODO DE GRAÇA DA LICENÇA POS{% else %}LICENÇA POS EXPIRANDO EM BREVE{% endif %}

{% if is_grace_period %}O período de graça da sua licença Spwig POS expira em {{ days_remaining }} dia{{ days_remaining|pluralize }}. Após o término do período de graça, o acesso à API POS será bloqueado.{% else %}Sua licença Spwig POS expira em {{ days_remaining }} dia{{ days_remaining|pluralize }}.{% endif %}

DETALHES DA LICENÇA:
- Licença: {{ license_key_masked }}
- Expira: {{ expires_at }}

Renove sua licença POS: {{ renewal_url }}