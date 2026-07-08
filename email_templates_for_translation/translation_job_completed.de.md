---
template_type: translation_job_completed
category: Translation Service
---

# Email Template: translation_job_completed

## Subject
✓ Übersetzung abgeschlossen: {{ content_type }} ({{ language_count }} Sprachen)

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#dcfce7">
      <mj-column>
        <mj-text font-size="24px" font-weight="bold" color="#065f46" align="center">
          ✓ Übersetzung abgeschlossen!
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Ihre Übersetzungen sind bereit
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Große Nachricht! Ihre Batch-Übersetzung wurde erfolgreich abgeschlossen.
        </mj-text>

        <mj-spacer height="30px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
              Aufgabenübersicht:
            </mj-text>
            <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>Aufgaben-ID:</strong> {{ job_id }}<br/>
              <strong>Inhaltstyp:</strong> {{ content_type }}<br/>
              <strong>Sprachen:</strong> {{ target_languages }}<br/>
              <strong>Übersetzte Elemente:</strong> {{ items_translated }}<br/>
              <strong>Gesamtwörter:</strong> {{ word_count }}<br/>
              <strong>Abgeschlossen:</strong> {{ completed_at }}<br/>
              <strong>Dauer:</strong> {{ job_duration }}
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Übersetzungsgüte:
        </mj-text>

        <mj-section background-color="#f0fdf4" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="15px" color="#065f46">
              <strong>Durchschnittliche Qualitätsbewertung:</strong> {{ quality_score }}%<br/>
              <strong>Hochwertige Übersetzungen:</strong> {{ high_quality_count }} Elemente<br/>
              <strong>Überprüfung empfohlen:</strong> {{ review_needed_count }} Elemente
            </mj-text>
          </mj-column>
        </mj-section>

        {% if review_needed_count > 0 %}
        <mj-spacer height="20px" />
        <mj-section background-color="#fef3c7" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="14px" color="#92400e" font-weight="bold">
              ⚠️ Überprüfung empfohlen
            </mj-text>
            <mj-text font-size="14px" color="#92400e" line-height="1.6">
              {{ review_needed_count }} Übersetzungen erzielten weniger als 85 % und sollten vor der Veröffentlichung überprüft werden.
            </mj-text>
          </mj-column>
        </mj-section>
        {% endif %}

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Nächste Schritte:
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}" line-height="1.8">
          1. Übersetzungen in Ihrem Admin-Panel überprüfen<br/>
          2. Jede Übersetzung, die Bearbeitung benötigt, bearbeiten<br/>
          3. Übersetzungen veröffentlichen, um sie live zu machen<br/>
          4. Ihre multilinguale Inhalt wird Kunden zur Verfügung stehen
        </mj-text>

        <mj-spacer height="30px" />

        <mj-button href="{{ review_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          Übersetzungen überprüfen
        </mj-button>

        {% if can_publish_all %}
        <mj-spacer height="10px" />
        <mj-button href="{{ publish_all_url }}" background-color="#059669" color="#ffffff" font-size="14px" border-radius="6px" padding="10px 25px">
          Alle veröffentlichen
        </mj-button>
        {% endif %}
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
✓ ÜBERSETZUNG ABGESCHLOSSEN!

Ihre Übersetzungen sind bereit

Große Nachricht! Ihre Batch-Übersetzung wurde erfolgreich abgeschlossen.

AUFGABENÜBERSICHT:
- Aufgaben-ID: {{ job_id }}
- Inhaltstyp: {{ content_type }}
- Sprachen: {{ target_languages }}
- Übersetzte Elemente: {{ items_translated }}
- Gesamtwörter: {{ word_count }}
- Abgeschlossen: {{ completed_at }}
- Dauer: {{ job_duration }}

ÜBERSETZUNGSGÜTE:
- Durchschnittliche Qualitätsbewertung: {{ quality_score }}%
- Hochwertige Übersetzungen: {{ high_quality_count }} Elemente
- Überprüfung empfohlen: {{ review_needed_count }} Elemente

{% if review_needed_count > 0 %}
⚠️ ÜBERPRÜFUNG EMPFOHLEN:
{{ review_needed_count }} Übersetzungen erzielten weniger als 85 % und sollten vor der Veröffentlichung überprüft werden.
{% endif %}

NÄCHSTE SCHREITEN:
1. Übersetzungen in Ihrem Admin-Panel überprüfen
2. Jede Übersetzung, die Bearbeitung benötigt, bearbeiten
3. Übersetzungen veröffentlichen, um sie live zu machen
4. Ihre multilinguale Inhalt wird Kunden zur Verfügung stehen

Übersetzungen überprüfen: {{ review_url }}
{% if can_publish_all %}Alle veröffentlichen: {{ publish_all_url }}{% endif %}