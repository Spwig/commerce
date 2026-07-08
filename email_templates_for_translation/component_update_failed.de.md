---
template_type: component_update_failed
category: Component Updates
---

# Email Template: component_update_failed

## Subject
❌ Aktualisierung fehlgeschlagen: {{ component_name }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#fee2e2">
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="#991b1b" align="center">
          ❌ Aktualisierung fehlgeschlagen
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="18px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Installationsfehler
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}">
          Die Aktualisierung von {{ component_name }} auf Version {{ target_version }} ist fehlgeschlagen.
        </mj-text>

        <mj-spacer height="20px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
              Fehlerdetails:
            </mj-text>
            <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>Komponente:</strong> {{ component_name }}<br/>
              <strong>Zielversion:</strong> {{ target_version }}<br/>
              <strong>Fehlschlag bei:</strong> {{ failed_at }}<br/>
              <strong>Fehlercode:</strong> {{ error_code }}
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Fehlermeldung:
        </mj-text>

        <mj-section background-color="#fee2e2" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="14px" font-family="monospace" color="#991b1b" line-height="1.6">
              {{ error_message }}
            </mj-text>
          </mj-column>
        </mj-section>

        {% if error_log %}
        <mj-spacer height="20px" />
        <mj-text font-size="14px" color="{{ theme.color.text_secondary|default:'#6b7280' }}">
          <strong>Vollständiger Fehlerprotokoll:</strong><br/>
          <code style="font-size: 12px; color: #6b7280;">{{ error_log|truncatewords:50 }}</code>
        </mj-text>
        {% endif %}

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Was tun:
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}" line-height="1.8">
          1. Systemanforderungen und Abhängigkeiten prüfen<br/>
          2. Fehlerprotokoll für Details überprüfen<br/>
          3. Erneut installieren oder Support kontaktieren<br/>
          4. Ihr Geschäft läuft weiterhin auf {{ current_version }}
        </mj-text>

        <mj-spacer height="30px" />

        <mj-button href="{{ retry_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          Installation erneut versuchen
        </mj-button>

        <mj-spacer height="10px" />

        <mj-button href="{{ support_url }}" background-color="#6b7280" color="#ffffff" font-size="14px" border-radius="6px" padding="10px 25px">
          Support kontaktieren
        </mj-button>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
❌ AKTUALISIERUNG FEHLGESCHLAGEN

Installationsfehler

Die Aktualisierung von {{ component_name }} auf Version {{ target_version }} ist fehlgeschlagen.

FEHLERDETAILS:
- Komponente: {{ component_name }}
- Zielversion: {{ target_version }}
- Fehlschlag bei: {{ failed_at }}
- Fehlercode: {{ error_code }}

FEHLERMELDUNG:
{{ error_message }}

{% if error_log %}
VOLLSTÄNDIGES FEHLERLOG:
{{ error_log|truncatewords:50 }}
{% endif %}

WAS TUN:
1. Systemanforderungen und Abhängigkeiten prüfen
2. Fehlerprotokoll für Details überprüfen
3. Erneut installieren oder Support kontaktieren
4. Ihr Geschäft läuft weiterhin auf {{ current_version }}

Installation erneut versuchen: {{ retry_url }}
Support kontaktieren: {{ support_url }}