---
template_type: translation_quality_review_needed
category: Translation Service
---

# Email Template: translation_quality_review_needed

## Subject
⚠️ Qualitätsschwankungen erkannt: {{ content_type }} - {{ low_quality_count }} Elemente zur Prüfung

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#fef3c7">
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="#92400e" align="center">
          ⚠️ Übersetzung Qualität Warnung
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="18px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Prüfung empfohlen
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}">
          Ihre Übersetzungsaufgabe ist abgeschlossen, aber {{ low_quality_count }} Übersetzungen haben unter dem QualitätsSchwellenwert gescoret und sollten vor der Veröffentlichung geprüft werden.
        </mj-text>

        <mj-spacer height="20px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
              Aufgabenübersicht:
            </mj-text>
            <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>Aufgaben-ID:</strong> {{ job_id }}<br/>
              <strong>Inhaltstyp:</strong> {{ content_type }}<br/>
              <strong>Gesamtartikel:</strong> {{ total_items }}<br/>
              <strong>Durchschnittsqualität:</strong> {{ average_quality }}%<br/>
              <strong>Niedrige Qualität:</strong> {{ low_quality_count }} Artikel ({{ low_quality_percentage }}%)
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Qualitätsermittlung:
        </mj-text>

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="14px" color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>Exzellent (95-100%):</strong> {{ excellent_count }} Artikel<br/>
              <strong>Gut (85-94%):</strong> {{ good_count }} Artikel<br/>
              <strong>Angemessen (70-84%):</strong> {{ fair_count }} Artikel<br/>
              <strong>Schlecht (&lt;70%):</strong> <span style="color: #dc2626; font-weight: bold;">{{ poor_count }} Artikel</span>
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Häufige Qualitätsschwächen:
        </mj-text>

        {% for issue in quality_issues %}
        <mj-section background-color="#fef3c7" border-radius="8px" padding="12px">
          <mj-column>
            <mj-text font-size="14px" color="#92400e">
              <strong>{{ issue.type }}:</strong> {{ issue.count }} Vorkommen
            </mj-text>
          </mj-column>
        </mj-section>
        <mj-spacer height="8px" />
        {% endfor %}

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Empfohlene Maßnahmen:
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}" line-height="1.8">
          1. Prüfen Sie die markierten Übersetzungen im Admin-Panel<br/>
          2. Bearbeiten Sie niedrigwertige Übersetzungen manuell<br/>
          3. Überlegen Sie, ob Sie die schlechten Übersetzungen erneut übersetzen sollten<br/>
          4. Veröffentlichen Sie nur nach Abschluss der Prüfung
        </mj-text>

        <mj-spacer height="30px" />

        <mj-button href="{{ review_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          Übersetzungen prüfen
        </mj-button>

        <mj-spacer height="10px" />

        <mj-button href="{{ low_quality_url }}" background-color="#dc2626" color="#ffffff" font-size="14px" border-radius="6px" padding="10px 25px">
          Schlechte Qualitätselemente ansehen
        </mj-button>

        <mj-spacer height="30px" />

        <mj-section background-color="#eff6ff" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="14px" color="#1e40af" line-height="1.6">
              💡 Tipp: Qualitätsscores unter 85% deuten auf potenzielle Probleme mit Grammatik, Kontext oder Genauigkeit hin. Eine menschliche Prüfung wird stark empfohlen, bevor Sie etwas veröffentlichen.
            </mj-text>
          </mj-column>
        </mj-section>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
⚠️ QUALITÄTSWARNUNG ÜBERSETZUNG

Prüfung empfohlen

Ihre Übersetzungsaufgabe ist abgeschlossen, aber {{ low_quality_count }} Übersetzungen haben unter dem QualitätsSchwellenwert gescoret und sollten vor der Veröffentlichung geprüft werden.

AUFGABENÜBERSICHT:
- Aufgaben-ID: {{ job_id }}
- Inhaltstyp: {{ content_type }}
- Gesamtartikel: {{ total_items }}
- Durchschnittsqualität: {{ average_quality }}%
- Niedrige Qualität: {{ low_quality_count }} Artikel ({{ low_quality_percentage }}%)

QUALITÄTSVERTEILUNG:
- Exzellent (95-100%): {{ excellent_count }} Artikel
- Gut (85-94%): {{ good_count }} Artikel
- Angemessen (70-84%): {{ fair_count }} Artikel
- Schlecht (<70%): {{ poor_count }} Artikel

GEMEINSAME QUALITÄTSFÄLLE:
{% for issue in quality_issues %}
{{ issue.type }}: {{ issue.count }} Vorkommen
{% endfor %}

EMPFOHLENE MAßNAHMEN:
1. Prüfen Sie die markierten Übersetzungen im Admin-Panel
2. Bearbeiten Sie niedrigwertige Übersetzungen manuell
3. Überlegen Sie, ob Sie die schlechten Übersetzungen erneut übersetzen sollten
4. Veröffentlichen Sie nur nach Abschluss der Prüfung

Übersetzungen prüfen: {{ review_url }}
Schlechte Qualitätselemente ansehen: {{ low_quality_url }}

💡 Tipp: Qualitätsscores unter 85% deuten auf potenzielle Probleme mit Grammatik, Kontext oder Genauigkeit hin. Eine menschliche Prüfung wird stark empfohlen, bevor Sie etwas veröffentlichen.