---
template_type: component_incompatible_warning
category: Component Updates
---

# Email Template: component_incompatible_warning

## Subject
⚠️ Problema di compatibilità: {{ component_name }} e {{ conflicting_component }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#fef3c7">
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="#92400e" align="center">
          ⚠️ Warning di compatibilità
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="18px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Conflitto di versioni rilevato
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          È stato rilevato un problema di compatibilità tra i componenti del tuo negozio Spwig.
        </mj-text>

        <mj-spacer height="30px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
              Dettagli del conflitto:
            </mj-text>
            <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>Componente 1:</strong> {{ component_name }} v{{ component_version }}<br/>
              <strong>Componente 2:</strong> {{ conflicting_component }} v{{ conflicting_version }}<br/>
              <strong>Rilevato:</strong> {{ detected_at }}
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Problema di compatibilità:
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}" line-height="1.8">
          {{ incompatibility_description }}
        </mj-text>

        <mj-spacer height="20px" />

        <mj-section background-color="#fee2e2" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="14px" color="#991b1b" font-weight="bold">
              Impatto potenziale
            </mj-text>
            <mj-text font-size="14px" color="#991b1b" line-height="1.6">
              {{ impact_description }}
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Azione consigliata:
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}" line-height="1.8">
          {{ recommended_action }}
        </mj-text>

        {% if compatible_versions %}
        <mj-spacer height="30px" />
        <mj-section background-color="#f0fdf4" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="14px" color="#065f46" font-weight="bold">
              Versioni compatibili
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
          Risolvi conflitto
        </mj-button>
        <mj-spacer height="10px" />
        {% endif %}

        <mj-button href="{{ support_url }}" background-color="#6b7280" color="#ffffff" font-size="14px" border-radius="6px" padding="10px 25px">
          Contatta il supporto
        </mj-button>

        <mj-spacer height="20px" />

        <mj-text font-size="13px" color="{{ theme.color.text_secondary|default:'#6b7280' }}" align="center">
          Il tuo negozio è ancora operativo, ma ti consigliamo di risolvere questo conflitto al più presto.
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
⚠️ AVVERTENZA DI COMPATIBILITÀ

Conflitto di versioni rilevato

È stato rilevato un problema di compatibilità tra i componenti del tuo negozio Spwig.

DETTAGLI DEL CONFLITTO:
- Componente 1: {{ component_name }} v{{ component_version }}
- Componente 2: {{ conflicting_component }} v{{ conflicting_version }}
- Rilevato: {{ detected_at }}

PROBLEMA DI COMPATIBILITÀ:
{{ incompatibility_description }}

IMPATTO POTENZIALE:
{{ impact_description }}

AZIONE CONSIGLIATA:
{{ recommended_action }}

{% if compatible_versions %}VERSIONI COMPATIBILI:
{{ compatible_versions }}{% endif %}

{% if update_url %}Risolve conflitto: {{ update_url }}{% endif %}
Contatta il supporto: {{ support_url }}

Il tuo negozio è ancora operativo, ma ti consigliamo di risolvere questo conflitto al più presto.