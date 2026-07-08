---
template_type: pos_license_expiration_warning
category: POS
---

# Email Template: pos_license_expiration_warning

## Subject
{% if is_grace_period %}[Periodo di grazia] Licenza POS - {{ days_remaining }} giorni rimanenti{% else %}[Prossima scadenza] Licenza POS - {{ days_remaining }} giorni rimanenti{% endif %}

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="{% if is_grace_period %}#fef2f2{% else %}#fffbeb{% endif %}">
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="{% if is_grace_period %}#991b1b{% else %}#92400e{% endif %}" align="center">
          {% if is_grace_period %}Periodo di grazia per la licenza POS{% else %}Prossima scadenza della licenza POS{% endif %}
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          {% if is_grace_period %}Il periodo di grazia per la licenza Spwig POS scadrà tra <strong>{{ days_remaining }} giorno{{ days_remaining|pluralize }}</strong>. Una volta terminato il periodo di grazia, l'accesso all'API POS verrà bloccato.{% else %}La licenza Spwig POS scadrà tra <strong>{{ days_remaining }} giorno{{ days_remaining|pluralize }}</strong>.{% endif %}
        </mj-text>

        <mj-spacer height="20px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
              Dettagli della licenza:
            </mj-text>
            <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>Licenza:</strong> {{ license_key_masked }}<br/>
              <strong>Scade:</strong> {{ expires_at }}
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-button href="{{ renewal_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          Rinnova la licenza POS
        </mj-button>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
{% if is_grace_period %}PERIODO DI GRAZIA PER LA LICENZA POS{% else %}LICENZA POS PROSSIMA SCADENZA{% endif %}

{% if is_grace_period %}Il periodo di grazia per la licenza Spwig POS scadrà tra {{ days_remaining }} giorno{{ days_remaining|pluralize }}. Una volta terminato il periodo di grazia, l'accesso all'API POS verrà bloccato.{% else %}La licenza Spwig POS scadrà tra {{ days_remaining }} giorno{{ days_remaining|pluralize }}.{% endif %}

DETTAGLI DELLA LICENZA:
- Licenza: {{ license_key_masked }}
- Scade: {{ expires_at }}

Rinnova la tua licenza POS: {{ renewal_url }}