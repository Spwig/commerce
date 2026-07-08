---
template_type: component_rollback_success
category: Component Updates
---

# Email Template: component_rollback_success

## Subject
✓ {{ component_name }} revertido para v{{ previous_version }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#dbeafe">
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="#1e40af" align="center">
          ↩️ Reversão Concluída
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="18px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Componente Restaurado
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          {{ component_name }} foi revertido com sucesso para a versão anterior.
        </mj-text>

        <mj-spacer height="30px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
              Detalhes da Reversão:
            </mj-text>
            <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>Componente:</strong> {{ component_name }}<br/>
              <strong>Revertido de:</strong> v{{ failed_version }}<br/>
              <strong>Restaurado para:</strong> v{{ previous_version }}<br/>
              <strong>Concluído:</strong> {{ completed_at }}<br/>
              <strong>Duração:</strong> {{ rollback_duration }}
            </mj-text>
          </mj-column>
        </mj-section>

        {% if rollback_reason %}
        <mj-spacer height="30px" />
        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Motivo da Reversão:
        </mj-text>
        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}" line-height="1.8">
          {{ rollback_reason }}
        </mj-text>
        {% endif %}

        <mj-spacer height="30px" />

        <mj-section background-color="#f0fdf4" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="14px" color="#065f46" font-weight="bold">
              ✓ Status do Loja
            </mj-text>
            <mj-text font-size="14px" color="#065f46" line-height="1.6">
              Sua loja agora está rodando na versão estável {{ previous_version }}. Todas as funcionalidades devem estar restauradas.
            </mj-text>
          </mj-column>
        </mj-section>

        {% if data_restored %}
        <mj-spacer height="20px" />
        <mj-text font-size="14px" color="{{ theme.color.text_secondary|default:'#6b7280' }}">
          <strong>Restauração de Dados:</strong> {{ data_restoration_message }}
        </mj-text>
        {% endif %}

        {% if next_steps %}
        <mj-spacer height="30px" />
        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Próximos Passos:
        </mj-text>
        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}" line-height="1.8">
          {{ next_steps }}
        </mj-text>
        {% endif %}

        <mj-spacer height="30px" />

        <mj-button href="{{ component_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          Ver Detalhes do Componente
        </mj-button>

        {% if incident_report_url %}
        <mj-spacer height="10px" />
        <mj-button href="{{ incident_report_url }}" background-color="#6b7280" color="#ffffff" font-size="14px" border-radius="6px" padding="10px 25px">
          Ver Relatório de Incidente
        </mj-button>
        {% endif %}

        <mj-spacer height="20px" />

        <mj-text font-size="13px" color="{{ theme.color.text_secondary|default:'#6b7280' }}" align="center">
          Se você continuar a ter problemas, entre em contato com o suporte.
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
↩️ REVERSÃO CONCLUIDA

Componente Restaurado

{{ component_name }} foi revertido com sucesso para a versão anterior.

DETALHES DA REVERSÃO:
- Componente: {{ component_name }}
- Revertido de: v{{ failed_version }}
- Restaurado para: v{{ previous_version }}
- Concluído: {{ completed_at }}
- Duração: {{ rollback_duration }}

{% if rollback_reason %}
MOTIVO DA REVERSÃO:
{{ rollback_reason }}
{% endif %}

✓ STATUS DA LOJA:
Sua loja agora está rodando na versão estável {{ previous_version }}. Todas as funcionalidades devem estar restauradas.

{% if data_restored %}
RESTAURAÇÃO DE DADOS: {{ data_restoration_message }}
{% endif %}

{% if next_steps %}
PRÓXIMOS PASSOS:
{{ next_steps }}
{% endif %}

Ver detalhes do componente: {{ component_url }}
{% if incident_report_url %}Ver relatório de incidente: {{ incident_report_url }}{% endif %}

Se você continuar a ter problemas, entre em contato com o suporte.