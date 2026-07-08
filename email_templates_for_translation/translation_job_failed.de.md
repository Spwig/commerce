---
template_type: translation_job_failed
category: Translation Service
---

# Email Template: translation_job_failed

## Subject
❌ Übersetzungsauftrag fehlgeschlagen: {{ content_type }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#fee2e2">
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="#991b1b" align="center">
          ❌ Übersetzungsauftrag fehlgeschlagen
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="18px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Übersetzungsfehler
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}">
          Ihr Massen-Übersetzungsauftrag ist auf einen Fehler gestoßen und konnte nicht abgeschlossen werden.
        </mj-text>

        <mj-spacer height="20px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
              Auftragsdetails:
            </mj-text>
            <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>Auftrags-ID:</strong> {{ job_id }}<br/>
              <strong>Inhaltstyp:</strong> {{ content_type }}<br/>
              <strong>Zielsprachen:</strong> {{ target_languages }}<br/>
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

        {% if partial_completion %}
        <mj-spacer height="30px" />
        <mj-section background-color="#fef3c7" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="14px" color="#92400e" font-weight="bold">
              Teilweise Ausführung
            </mj-text>
            <mj-text font-size="14px" color="#92400e" line-height="1.6">
              {{ items_completed }} von {{ total_items }} Elementen wurden erfolgreich übersetzt, bevor der Fehler auftrat.
            </mj-text>
          </mj-column>
        </mj-section>
        {% endif %}

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Häufige Ursachen:
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}" line-height="1.8">
          • Probleme mit der Verbindung zur Übersetzungsdienstleister-API<br/>
          • Unzureichende Übersetzungspunkte<br/>
          • Ungültiger oder beschädigter Quellinhalt<br/>
          • Nicht unterstützte Sprachkombination
        </mj-text>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Empfohlene Maßnahmen:
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}" line-height="1.8">
          1. Prüfen Sie die Einstellungen Ihres Übersetzungsdienstleisters<br/>
          2. Stellen Sie sicher, dass Übersetzungspunkte verfügbar sind<br/>
          3. Prüfen Sie die Fehlermeldung auf spezifische Probleme<br/>
          4. Wiederholen Sie den Übersetzungsauftrag
        </mj-text>

        <mj-spacer height="30px" />

        <mj-button href="{{ retry_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          Übersetzung wiederholen
        </mj-button>

        <mj-spacer height="10px" />

        <mj-button href="{{ settings_url }}" background-color="#6b7280" color="#ffffff" font-size="14px" border-radius="6px" padding="10px 25px">
          Einstellungen prüfen
        </mj-button>

        <mj-spacer height="20px" />

        <mj-text font-size="13px" color="{{ theme.color.text_secondary|default:'#6b7280' }}" align="center">
          Wenn das Problem weiter besteht, kontaktieren Sie den Support mit Fehler-Code {{ error_code }}.
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
❌ ÜBERSETZUNGAUFGABE FEHLGESCHLAGEN

Übersetzungsfehler

Ihr Massen-Übersetzungsauftrag ist auf einen Fehler gestoßen und konnte nicht abgeschlossen werden.

AUFGABENDETAILS:
- Auftrags-ID: {{ job_id }}
- Inhaltstyp: {{ content_type }}
- Zielsprachen: {{ target_languages }}
- Fehlgeschlagen um: {{ failed_at }}
- Fehler-Code: {{ error_code }}

FEHLERMITTEILUNG:
{{ error_message }}

{% if partial_completion %}
TEILWEISE VERARBEITUNG:
{{ items_completed }} von {{ total_items }} Elementen wurden erfolgreich übersetzt, bevor der Fehler auftrat.
{% endif %}

HÄUFIGE URSACHEN:
• Probleme mit der Verbindung zur Übersetzungsdienstleister-API
• Unzureichende Übersetzungspunkte
• Ungültiger oder beschädigter Quellinhalt
• Nicht unterstützte Sprachkombination

EMPFOHLENE MAßNAHMEN:
1. Prüfen Sie die Einstellungen Ihres Übersetzungsdienstleisters
2. Stellen Sie sicher, dass Übersetzungspunkte verfügbar sind
3. Prüfen Sie die Fehlermeldung auf spezifische Probleme
4. Wiederholen Sie den Übersetzungsauftrag

Übersetzung wiederholen: {{ retry_url }}
Einstellungen prüfen: {{ settings_url }}

Wenn das Problem weiter besteht, kontaktieren Sie den Support mit Fehler-Code {{ error_code }}.