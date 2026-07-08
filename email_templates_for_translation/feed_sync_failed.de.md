---
template_type: feed_sync_failed
category: Product Feeds
---

# Email Template: feed_sync_failed

## Subject
❌ Der Sync von {{ feed_name }} zu {{ platform_name }} ist fehlgeschlagen

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#fee2e2">
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="#991b1b" align="center">
          ❌ Sync fehlgeschlagen
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="18px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Sync-Fehler
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}">
          Der Sync von {{ feed_name }} zu {{ platform_name }} ist fehlgeschlagen.
        </mj-text>

        <mj-spacer height="20px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
              Details zum Fehler:
            </mj-text>
            <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>Feed:</strong> {{ feed_name }}<br/>
              <strong>Plattform:</strong> {{ platform_name }}<br/>
              <strong>Fehlgeschlagen um:</strong> {{ failed_at }}<br/>
              <strong>Fehler-Code:</strong> {{ error_code }}
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

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Häufige Ursachen:
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}" line-height="1.8">
          • Ungültige API-Anmeldeinformationen oder abgelaufener Token<br/>
          • Netzwerkverbindungsprobleme<br/>
          • Die API-Rate-Limits der Plattform sind überschritten worden<br/>
          • Das Feed-Format erfüllt die Plattformanforderungen nicht
        </mj-text>

        {% if recommended_action %}
        <mj-spacer height="30px" />
        <mj-section background-color="#fef3c7" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="14px" color="#92400e" font-weight="bold">
              Empfohlene Aktion
            </mj-text>
            <mj-text font-size="14px" color="#92400e" line-height="1.6">
              {{ recommended_action }}
            </mj-text>
          </mj-column>
        </mj-section>
        {% endif %}

        <mj-spacer height="30px" />

        <mj-button href="{{ retry_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          Sync erneut versuchen
        </mj-button>

        <mj-spacer height="10px" />

        <mj-button href="{{ admin_feed_url }}" background-color="#6b7280" color="#ffffff" font-size="14px" border-radius="6px" padding="10px 25px">
          Feed-Einstellungen prüfen
        </mj-button>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
❌ SYNC FEHLGESCHLAGEN

Sync-Fehler

Der Sync von {{ feed_name }} zu {{ platform_name }} ist fehlgeschlagen.

FEHLER DETAILS:
- Feed: {{ feed_name }}
- Plattform: {{ platform_name }}
- Fehlgeschlagen um: {{ failed_at }}
- Fehler-Code: {{ error_code }}

FEHLERMELDUNG:
{{ error_message }}

HÄUFIGE URSACHEN:
• Ungültige API-Anmeldeinformationen oder abgelaufener Token
• Netzwerkverbindungsprobleme
• Die API-Rate-Limits der Plattform sind überschritten worden
• Das Feed-Format erfüllt die Plattformanforderungen nicht

{% if recommended_action %}
EMPFOHLENE Aktion:
{{ recommended_action }}
{% endif %}

Sync erneut versuchen: {{ retry_url }}
Feed-Einstellungen prüfen: {{ admin_feed_url }}