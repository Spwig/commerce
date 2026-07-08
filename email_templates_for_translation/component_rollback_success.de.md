---
template_type: component_rollback_success
category: Component Updates
---

# Email Template: component_rollback_success

## Subject
✓ {{ component_name }} auf v{{ previous_version }} zurückgerollt

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#dbeafe">
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="#1e40af" align="center">
          ↩️ Rollback abgeschlossen
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="18px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Komponente wiederhergestellt
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          {{ component_name }} wurde erfolgreich auf die vorherige Version zurückgerollt.
        </mj-text>

        <mj-spacer height="30px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
              Rollback-Details:
            </mj-text>
            <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>Komponente:</strong> {{ component_name }}<br/>
              <strong>Zurückgerollt von:</strong> v{{ failed_version }}<br/>
              <strong>Zurückgerollt auf:</strong> v{{ previous_version }}<br/>
              <strong>Abgeschlossen:</strong> {{ completed_at }}<br/>
              <strong>Dauer:</strong> {{ rollback_duration }}
            </mj-text>
          </mj-column>
        </mj-section>

        {% if rollback_reason %}
        <mj-spacer height="30px" />
        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Grund für den Rollback:
        </mj-text>
        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}" line-height="1.8">
          {{ rollback_reason }}
        </mj-text>
        {% endif %}

        <mj-spacer height="30px" />

        <mj-section background-color="#f0fdf4" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="14px" color="#065f46" font-weight="bold">
              ✓ Store-Status
            </mj-text>
            <mj-text font-size="14px" color="#065f46" line-height="1.6">
              Ihr Store läuft nun auf der stabilen Version {{ previous_version }}. Alle Funktionen sollten wiederhergestellt sein.
            </mj-text>
          </mj-column>
        </mj-section>

        {% if data_restored %}
        <mj-spacer height="20px" />
        <mj-text font-size="14px" color="{{ theme.color.text_secondary|default:'#6b7280' }}">
          <strong>Datenwiederherstellung:</strong> {{ data_restoration_message }}
        </mj-text>
        {% endif %}

        {% if next_steps %}
        <mj-spacer height="30px" />
        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Nächste Schritte:
        </mj-text>
        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}" line-height="1.8">
          {{ next_steps }}
        </mj-text>
        {% endif %}

        <mj-spacer height="30px" />

        <mj-button href="{{ component_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          Komponentendetails ansehen
        </mj-button>

        {% if incident_report_url %}
        <mj-spacer height="10px" />
        <mj-button href="{{ incident_report_url }}" background-color="#6b7280" color="#ffffff" font-size="14px" border-radius="6px" padding="10px 25px">
          Zwischenfallbericht ansehen
        </mj-button>
        {% endif %}

        <mj-spacer height="20px" />

        <mj-text font-size="13px" color="{{ theme.color.text_secondary|default:'#6b7280' }}" align="center">
          Falls Sie weiterhin Probleme haben, wenden Sie sich bitte an den Support.
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
↩️ ROLLBACK ABGESCHLOSSEN

Komponente wiederhergestellt

{{ component_name }} wurde erfolgreich auf die vorherige Version zurückgerollt.

ROLLBACK-DETAILS:
- Komponente: {{ component_name }}
- Zurückgerollt von: v{{ failed_version }}
- Zurückgerollt auf: v{{ previous_version }}
- Abgeschlossen: {{ completed_at }}
- Dauer: {{ rollback_duration }}

{% if rollback_reason %}
GRUND FÜR DEN ROLLBACK:
{{ rollback_reason }}
{% endif %}

✓ STORE-STATUS:
Ihr Store läuft nun auf der stabilen Version {{ previous_version }}. Alle Funktionen sollten wiederhergestellt sein.

{% if data_restored %}
Datenwiederherstellung: {{ data_restoration_message }}
{% endif %}

{% if next_steps %}
Nächste Schritte:
{{ next_steps }}
{% endif %}

Komponentendetails ansehen: {{ component_url }}
{% if incident_report_url %}Zwischenfallbericht ansehen: {{ incident_report_url }}{% endif %}

Falls Sie weiterhin Probleme haben, wenden Sie sich bitte an den Support.