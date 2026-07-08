---
template_type: component_incompatible_warning
category: Component Updates
---

# Email Template: component_incompatible_warning

## Subject
⚠️ Kompatibilitätsproblem: {{ component_name }} und {{ conflicting_component }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#fef3c7">
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="#92400e" align="center">
          ⚠️ Kompatibilitätswarnung
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="18px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Versionskonflikt erkannt
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Ein Kompatibilitätsproblem wurde zwischen Komponenten in Ihrem Spwig-Store erkannt.
        </mj-text>

        <mj-spacer height="30px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
              Konfliktdetails:
            </mj-text>
            <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>Komponente 1:</strong> {{ component_name }} v{{ component_version }}<br/>
              <strong>Komponente 2:</strong> {{ conflicting_component }} v{{ conflicting_version }}<br/>
              <strong>Erkannt:</strong> {{ detected_at }}
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Kompatibilitätsproblem:
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}" line-height="1.8">
          {{ incompatibility_description }}
        </mj-text>

        <mj-spacer height="20px" />

        <mj-section background-color="#fee2e2" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="14px" color="#991b1b" font-weight="bold">
              Potenzieller Einfluss
            </mj-text>
            <mj-text font-size="14px" color="#991b1b" line-height="1.6">
              {{ impact_description }}
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Empfohlene Aktion:
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}" line-height="1.8">
          {{ recommended_action }}
        </mj-text>

        {% if compatible_versions %}
        <mj-spacer height="30px" />
        <mj-section background-color="#f0fdf4" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="14px" color="#065f46" font-weight="bold">
              Kompatibele Versionen
            </mj-text>
            <mj-text font-size="14px" color="#065f46" line-height="1.6">
              {{ compatible_versions }}
            </mj-text>
          </mj-column>
        </mj-section>
        {% endif %}

        <mj-spacer height="30px" />

        {% if update_url %}
        <mj-button href="{{ update_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          Konflikt beheben
        </mj-button>
        <mj-spacer height="10px" />
        {% endif %}

        <mj-button href="{{ support_url }}" background-color="#6b7280" color="#ffffff" font-size="14px" border-radius="6px" padding="10px 25px">
          Support kontaktieren
        </mj-button>

        <mj-spacer height="20px" />

        <mj-text font-size="13px" color="{{ theme.color.text_secondary|default:'#6b7280' }}" align="center">
          Ihr Store ist weiterhin betriebsbereit, aber wir empfehlen, diesen Konflikt baldmöglichst zu beheben.
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
⚠️ KOMPATIBILITÄTSWARNUNG

Versionskonflikt erkannt

Ein Kompatibilitätsproblem wurde zwischen Komponenten in Ihrem Spwig-Store erkannt.

KONFLIKTDETAILS:
- Komponente 1: {{ component_name }} v{{ component_version }}
- Komponente 2: {{ conflicting_component }} v{{ conflicting_version }}
- Erkannt: {{ detected_at }}

KOMPATIBILITÄTSPROBLEM:
{{ incompatibility_description }}

POTENZIELLER EINFLUSS:
{{ impact_description }}

EMPFOHLENE AKTION:
{{ recommended_action }}

{% if compatible_versions %}KOMPATIBILE VERSIONEN:
{{ compatible_versions }}{% endif %}

{% if update_url %}Konflikt beheben: {{ update_url }}{% endif %}
Support kontaktieren: {{ support_url }}

Ihr Store ist weiterhin betriebsbereit, aber wir empfehlen, diesen Konflikt baldmöglichst zu beheben.