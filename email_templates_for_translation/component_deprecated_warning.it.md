---
template_type: component_deprecated_warning
category: Component Updates
---

# Email Template: component_deprecated_warning

## Subject
⚠️ {{ component_name }} sarà deprecato il {{ deprecation_date }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#fef3c7">
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="#92400e" align="center">
          ⚠️ Avviso di deprecato
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="18px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Componente che verrà deprecato
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          {{ component_name }} verrà deprecato e non è più consigliabile per l'utilizzo. Pianifica la migrazione a una soluzione alternativa.
        </mj-text>

        <mj-spacer height="30px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
              Cronologia della deprecato:
            </mj-text>
            <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>Componente:</strong> {{ component_name }}<br/>
              <strong>Versione corrente:</strong> {{ current_version }}<br/>
              <strong>Data di deprecato:</strong> {{ deprecation_date }}<br/>
              <strong>Fine supporto:</strong> {{ end_of_support_date }}
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Motivo della deprecato:
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}" line-height="1.8">
          {{ deprecation_reason }}
        </mj-text>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Cosa significa questo:
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}" line-height="1.8">
          • Il componente continuerà a funzionare fino a {{ end_of_support_date }}<br/>
          • Non saranno aggiunte nuove funzionalità<br/>
          • Gli aggiornamenti di sicurezza saranno forniti fino alla fine del supporto<br/>
          • Dopo {{ end_of_support_date }}, il componente non riceverà più aggiornamenti
        </mj-text>

        {% if recommended_alternative %}
        <mj-spacer height="30px" />
        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Alternativa consigliata:
        </mj-text>
        <mj-section background-color="#f0fdf4" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="15px" color="#065f46" font-weight="bold">
              {{ alternative_name }}
            </mj-text>
            <mj-text font-size="14px" color="#065f46" line-height="1.6">
              {{ alternative_description }}
            </mj-text>
          </mj-column>
        </mj-section>
        {% endif %}

        {% if migration_guide %}
        <mj-spacer height="20px" />
        <mj-text font-size="14px" color="{{ theme.color.text_secondary|default:'#6b7280' }}" align="center">
          <a href="{{ migration_guide }}" style="color: {{ theme.color.primary|default:'#2563eb' }};">Visualizza la guida alla migrazione</a>
        </mj-text>
        {% endif %}

        <mj-spacer height="30px" />

        {% if alternative_url %}
        <mj-button href="{{ alternative_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          Visualizza l'alternativa
        </mj-button>
        <mj-spacer height="10px" />
        {% endif %}

        <mj-button href="{{ support_url }}" background-color="#6b7280" color="#ffffff" font-size="14px" border-radius="6px" padding="10px 25px">
          Contatta il supporto
        </mj-button>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
⚠️ AVVISO DI DEPRECATO

Componente che verrà deprecato

{{ component_name }} verrà deprecato e non è più consigliabile per l'utilizzo. Pianifica la migrazione a una soluzione alternativa.

CRONOLOGIA DELLA DEPRECATO:
- Componente: {{ component_name }}
- Versione corrente: {{ current_version }}
- Data di deprecato: {{ deprecation_date }}
- Fine supporto: {{ end_of_support_date }}

MOTIVO DELLA DEPRECATO:
{{ deprecation_reason }}

COSA SIGNIFICA QUESTO:
• Il componente continuerà a funzionare fino a {{ end_of_support_date }}
• Non saranno aggiunte nuove funzionalità
• Gli aggiornamenti di sicurezza saranno forniti fino alla fine del supporto
• Dopo {{ end_of_support_date }}, il componente non riceverà più aggiornamenti

{% if recommended_alternative %}
ALTERNATIVA CONSIGLIATA:
{{ alternative_name }}
{{ alternative_description }}
{% endif %}

{% if migration_guide %}Visualizza la guida alla migrazione: {{ migration_guide }}{% endif %}
{% if alternative_url %}Visualizza l'alternativa: {{ alternative_url }}{% endif %}
Contatta il supporto: {{ support_url }}