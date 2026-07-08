---
template_type: pos_license_expiration_warning
category: POS
---

# Email Template: pos_license_expiration_warning

## Subject
{% if is_grace_period %}[Gnadezeit] POS-Lizenz - {{ days_remaining }} Tage verbleiben{% else %}[Bald abgelaufen] POS-Lizenz - {{ days_remaining }} Tage verbleiben{% endif %}

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="{% if is_grace_period %}#fef2f2{% else %}#fffbeb{% endif %}">
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="{% if is_grace_period %}#991b1b{% else %}#92400e{% endif %}" align="center">
          {% if is_grace_period %}POS-Lizenz Gnadezeit{% else %}POS-Lizenz Bald abgelaufen{% endif %}
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          {% if is_grace_period %}Ihre Spwig POS-Lizenz Gnadezeit endet in <strong>{{ days_remaining }} Tag{{ days_remaining|pluralize }}</strong>. Nachdem die Gnadezeit endet, wird der Zugriff auf die POS-API blockiert.{% else %}Ihre Spwig POS-Lizenz endet in <strong>{{ days_remaining }} Tag{{ days_remaining|pluralize }}</strong>.{% endif %}
        </mj-text>

        <mj-spacer height="20px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
              Lizenzdetails:
            </mj-text>
            <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>Lizenz:</strong> {{ license_key_masked }}<br/>
              <strong>Ablaufdatum:</strong> {{ expires_at }}
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-button href="{{ renewal_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          POS-Lizenz verlängern
        </mj-button>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
{% if is_grace_period %}POS-LIZENZ GNADENZEIT{% else %}POS-LIZENZ BALD ABLAUFEN{% endif %}

{% if is_grace_period %}Ihre Spwig POS-Lizenz Gnadezeit endet in {{ days_remaining }} Tag{{ days_remaining|pluralize }}. Nachdem die Gnadezeit endet, wird der Zugriff auf die POS-API blockiert.{% else %}Ihre Spwig POS-Lizenz endet in {{ days_remaining }} Tag{{ days_remaining|pluralize }}.{% endif %}

LIZENZDETAILS:
- Lizenz: {{ license_key_masked }}
- Ablaufdatum: {{ expires_at }}

Verlängern Sie Ihre POS-Lizenz: {{ renewal_url }}