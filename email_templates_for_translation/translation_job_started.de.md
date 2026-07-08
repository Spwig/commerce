---
template_type: translation_job_started
category: Translation Service
---

# Email Template: translation_job_started

## Subject
🌐 Übersetzungsauftrag gestartet: {{ content_type }} ({{ source_language }} → {{ target_languages }})

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#eff6ff">
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="#1e40af" align="center">
          🌐 Übersetzungsauftrag gestartet
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="18px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Massenübersetzung in Bearbeitung
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}">
          Ihr Massenübersetzungsauftrag wurde gestartet und wird nun verarbeitet.
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
              <strong>Quellsprache:</strong> {{ source_language }}<br/>
              <strong>Zielsprachen:</strong> {{ target_languages }}<br/>
              <strong>Zu übersetzende Elemente:</strong> {{ item_count }}<br/>
              <strong>Gestartet:</strong> {{ started_at }}
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Schätzung der Fertigstellung:
        </mj-text>

        <mj-section background-color="#f0fdf4" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="15px" color="#065f46" font-weight="bold" align="center">
              {{ estimated_completion }}
            </mj-text>
            <mj-text font-size="14px" color="#065f46" align="center">
              (Basiert auf {{ word_count }} Wörtern)
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Was kommt als nächstes:
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}" line-height="1.8">
          1. Der KI-Übersetzungsdienst verarbeitet Ihren Inhalt<br/>
          2. Die Übersetzungen werden als Entwürfe gespeichert, um sie zu überprüfen<br/>
          3. Sie erhalten eine E-Mail, sobald der Auftrag abgeschlossen ist<br/>
          4. Überprüfen und veröffentlichen Sie die Übersetzungen über Ihr Admin-Panel
        </mj-text>

        <mj-spacer height="30px" />

        <mj-button href="{{ job_status_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          Auftragsstatus ansehen
        </mj-button>

        <mj-spacer height="20px" />

        <mj-text font-size="13px" color="{{ theme.color.text_secondary|default:'#6b7280' }}" align="center">
          Sie können diese E-Mail schließen. Wir benachrichtigen Sie, sobald die Übersetzung abgeschlossen ist.
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
🌐 ÜBERSETZUNGAUFGABE GESTARTET

Massenübersetzung in Bearbeitung

Ihr Massenübersetzungsauftrag wurde gestartet und wird nun verarbeitet.

AUFGABENDETAILS:
- Auftrags-ID: {{ job_id }}
- Inhaltstyp: {{ content_type }}
- Quellsprache: {{ source_language }}
- Zielsprachen: {{ target_languages }}
- Zu übersetzende Elemente: {{ item_count }}
- Gestartet: {{ started_at }}

GESCHÄTZTE FERTIGSTELLUNG:
{{ estimated_completion }}
(Basiert auf {{ word_count }} Wörtern)

WAS KOMMT ALS NÄCHSTES:
1. Der KI-Übersetzungsdienst verarbeitet Ihren Inhalt
2. Die Übersetzungen werden als Entwürfe gespeichert, um sie zu überprüfen
3. Sie erhalten eine E-Mail, sobald der Auftrag abgeschlossen ist
4. Überprüfen und veröffentlichen Sie die Übersetzungen über Ihr Admin-Panel

Auftragsstatus ansehen: {{ job_status_url }}

Sie können diese E-Mail schließen. Wir benachrichtigen Sie, sobald die Übersetzung abgeschlossen ist.