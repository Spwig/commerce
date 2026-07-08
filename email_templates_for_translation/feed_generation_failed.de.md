---
template_type: feed_generation_failed
category: Product Feeds
---

# Email Template: feed_generation_failed

## Subject
❌ Feed-Generierung fehlgeschlagen: {{ feed_name }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#fee2e2">
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="#991b1b" align="center">
          ❌ Feed-Generierung fehlgeschlagen
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="18px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Generation Fehler
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}">
          Die {{ feed_name }} Produkt-Feed-Generierung ist aufgrund eines Fehlers fehlgeschlagen.
        </mj-text>

        <mj-spacer height="20px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
              Fehlerdetails:
            </mj-text>
            <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>Feed:</strong> {{ feed_name }}<br/>
              <strong>Fehlgeschlagen um:</strong> {{ failed_at }}<br/>
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
          <strong>Fehlerprotokoll:</strong><br/>
          <code style="font-size: 12px; color: #6b7280;">{{ error_log|truncatewords:30 }}</code>
        </mj-text>
        {% endif %}

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Häufige Ursachen:
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}" line-height="1.8">
          • Fehlende erforderliche Produktinformationen (Titel, Preis, Bild)<br/>
          • Ungültiges Format der Produktinformationen<br/>
          • Datenbankverbindungsprobleme<br/>
          • Unzureichender Speicherplatz oder Arbeitsspeicher
        </mj-text>

        <mj-spacer height="30px" />

        <mj-button href="{{ retry_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          Generierung erneut versuchen
        </mj-button>

        <mj-spacer height="10px" />

        <mj-button href="{{ admin_feed_url }}" background-color="#6b7280" color="#ffffff" font-size="14px" border-radius="6px" padding="10px 25px">
          Feed-Einstellungen ansehen
        </mj-button>

        <mj-spacer height="20px" />

        <mj-text font-size="13px" color="{{ theme.color.text_secondary|default:'#6b7280' }}" align="center">
          Wenn das Problem besteht, wenden Sie sich an den Support mit dem Fehlercode {{ error_code }}.
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
❌ FEED-GENERIERUNG FEHLGESCHLAGEN

Generation Fehler

Die {{ feed_name }} Produkt-Feed-Generierung ist aufgrund eines Fehlers fehlgeschlagen.

FEHLERDETAILS:
- Feed: {{ feed_name }}
- Fehlgeschlagen um: {{ failed_at }}
- Fehlercode: {{ error_code }}

FEHLERMELDUNG:
{{ error_message }}

{% if error_log %}
FEHLERLOG:
{{ error_log|truncatewords:30 }}
{% endif %}

HÄUFIGE URSACHEN:
• Fehlende erforderliche Produktinformationen (Titel, Preis, Bild)
• Ungültiges Format der Produktinformationen
• Datenbankverbindungsprobleme
• Unzureichender Speicherplatz oder Arbeitsspeicher

Generierung erneut versuchen: {{ retry_url }}
Feed-Einstellungen ansehen: {{ admin_feed_url }}

Wenn das Problem besteht, wenden Sie sich an den Support mit dem Fehlercode {{ error_code }}.