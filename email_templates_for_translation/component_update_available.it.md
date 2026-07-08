---
template_type: component_update_available
category: Component Updates
---

# Email Template: component_update_available

## Subject
Aggiornamento disponibile: {{ component_name }} v{{ new_version }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#eff6ff">
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="#1e40af" align="center">
          📦 Aggiornamento disponibile
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="18px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Nuova versione disponibile
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}">
          Una nuova versione di {{ component_name }} è disponibile per il tuo negozio Spwig.
        </mj-text>

        <mj-spacer height="20px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
              Dettagli dell'aggiornamento:
            </mj-text>
            <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>Componente:</strong> {{ component_name }}<br/>
              <strong>Versione attuale:</strong> {{ current_version }}<br/>
              <strong>Nuova versione:</strong> {{ new_version }}<br/>
              <strong>Data di rilascio:</strong> {{ release_date }}
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Cosa è nuovo:
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}" line-height="1.8">
          {{ changelog }}
        </mj-text>

        {% if breaking_changes %}
        <mj-spacer height="20px" />
        <mj-section background-color="#fef3c7" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="14px" color="#92400e" font-weight="bold">
              ⚠️ Cambiamenti che rompono la compatibilità
            </mj-text>
            <mj-text font-size="14px" color="#92400e" line-height="1.6">
              {{ breaking_changes }}
            </mj-text>
          </mj-column>
        </mj-section>
        {% endif %}

        <mj-spacer height="30px" />

        <mj-button href="{{ update_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          Installa aggiornamento
        </mj-button>

        <mj-spacer height="20px" />

        <mj-text font-size="14px" color="{{ theme.color.text_secondary|default:'#6b7280' }}" align="center">
          <a href="{{ changelog_url }}" style="color: {{ theme.color.primary|default:'#2563eb' }};">
            Visualizza l'intero log delle modifiche
          </a>
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
📦 AGGIORNAMENTO DISPOINIBILE

Nuova versione disponibile

Una nuova versione di {{ component_name }} è disponibile per il tuo negozio Spwig.

DETTAGLI DELL'AGGIORNAMENTO:
- Componente: {{ component_name }}
- Versione attuale: {{ current_version }}
- Nuova versione: {{ new_version }}
- Data di rilascio: {{ release_date }}

COSA È NUOVO:
{{ changelog }}

{% if breaking_changes %}
⚠️ CAMBIAMENTI CHE ROMPONO LA COMPATIBILITÀ:
{{ breaking_changes }}
{% endif %}

Installa aggiornamento: {{ update_url }}
Visualizza l'intero log delle modifiche: {{ changelog_url }}