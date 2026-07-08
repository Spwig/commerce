---
template_type: return_request_approved
category: Returns
---

# Email Template: return_request_approved

## Subject
Ihr Rücksendeantrag wurde genehmigt - Bestellung #{{ order_number }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="{{ theme.color.surface|default:'#f0fdf4' }}">
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="{{ theme.color.text|default:'#166534' }}">
          Rücksendeantrag genehmigt
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text|default:'#166534' }}">
          Bestellung #{{ order_number }}
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Hallo {{ customer_name }},
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Ihr Rücksendeantrag für die Bestellung <strong>#{{ order_number }}</strong> wurde genehmigt.
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          <strong>Nächste Schritte:</strong>
        </mj-text>

        <mj-text font-size="15px" line-height="1.8" color="{{ theme.color.text|default:'#4b5563' }}">
          1. Laden Sie das Rücksendeschild unten herunter und drucken Sie es aus<br/>
          2. Packen Sie die Artikel so sicher wie möglich in ihre ursprüngliche Verpackung<br/>
          3. Heften Sie das Rücksendeschild an die Außenseite des Pakets<br/>
          4. Geben Sie es bei der nächstgelegenen Versandstelle ab
        </mj-text>

        {% if return_label_url %}
        <mj-spacer height="20px" />
        <mj-button href="{{ return_label_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          Rücksendeschild herunterladen
        </mj-button>
        {% endif %}

        {% if return_tracking_number %}
        <mj-text font-size="15px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          <strong>Rücksende-Tracking-Nummer:</strong> {{ return_tracking_number }}
        </mj-text>
        {% endif %}

        <mj-section background-color="{{ theme.color.surface|default:'#fffbeb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-size="15px" line-height="1.6" color="{{ theme.color.text|default:'#92400e' }}">
              <strong>Wichtig:</strong> Bitte senden Sie die Rücksendung innerhalb von 7 Tagen, um eine schnelle Verarbeitung Ihres Rückzahlungsantrags zu gewährleisten.
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Sobald wir Ihre Rücksendung erhalten und geprüft haben, verarbeiten wir Ihre Rückzahlung auf die ursprüngliche Zahlungsmethode.
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
Rücksendeantrag genehmigt - Bestellung #{{ order_number }}

Hallo {{ customer_name }},

Ihr Rücksendeantrag für die Bestellung #{{ order_number }} wurde genehmigt.

Nächste Schritte:
1. Laden Sie das Rücksendeschild herunter und drucken Sie es aus
2. Packen Sie die Artikel so sicher wie möglich in ihre ursprüngliche Verpackung
3. Heften Sie das Rücksendeschild an die Außenseite des Pakets
4. Geben Sie es bei der nächstgelegenen Versandstelle ab

{% if return_label_url %}Rücksendeschild herunterladen: {{ return_label_url }}{% endif %}
{% if return_tracking_number %}Rücksende-Tracking-Nummer: {{ return_tracking_number }}{% endif %}

Wichtig: Bitte senden Sie die Rücksendung innerhalb von 7 Tagen, um eine schnelle Verarbeitung Ihres Rückzahlungsantrags zu gewährleisten.

Sobald wir Ihre Rücksendung erhalten und geprüft haben, verarbeiten wir Ihre Rückzahlung auf die ursprüngliche Zahlungsmethode.