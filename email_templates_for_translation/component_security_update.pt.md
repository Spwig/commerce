---
template_type: component_security_update
category: Component Updates
---

# Email Template: component_security_update

## Subject
🔒 URGENTE: Atualização de Segurança Disponível para {{ component_name }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#fee2e2">
      <mj-column>
        <mj-text font-size="22px" font-weight="bold" color="#991b1b" align="center">
          🔒 ATUALIZAÇÃO DE SEGURANÇA NECESSÁRIA
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="18px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Patch de Segurança Crítico
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Foi descoberta uma vulnerabilidade de segurança em {{ component_name }}. Por favor, atualize imediatamente para proteger sua loja.
        </mj-text>

        <mj-spacer height="30px" />

        <mj-section background-color="#fee2e2" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="#991b1b" font-size="16px">
              ⚠️ Informações de Segurança
            </mj-text>
            <mj-text color="#991b1b">
              <strong>Componente:</strong> {{ component_name }}<br/>
              <strong>Versão Atual:</strong> {{ current_version }}<br/>
              <strong>Versão Corrigida:</strong> {{ patched_version }}<br/>
              <strong>Gravidade:</strong> {{ severity_level }}<br/>
              <strong>ID do CVE:</strong> {{ cve_id }}
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Detalhes da Vulnerabilidade:
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}" line-height="1.8">
          {{ vulnerability_description }}
        </mj-text>

        <mj-spacer height="20px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Impacto Potencial:
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}" line-height="1.8">
          {{ impact_description }}
        </mj-text>

        {% if mitigation_steps %}
        <mj-spacer height="30px" />
        <mj-section background-color="#fef3c7" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="14px" color="#92400e" font-weight="bold">
              Mitigação Temporária
            </mj-text>
            <mj-text font-size="14px" color="#92400e" line-height="1.6">
              {{ mitigation_steps }}
            </mj-text>
          </mj-column>
        </mj-section>
        {% endif %}

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}" align="center">
          Ação Necessária: Instale a Atualização Imediatamente
        </mj-text>

        <mj-spacer height="20px" />

        <mj-button href="{{ update_url }}" background-color="#dc2626" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          Instale o Patch de Segurança
        </mj-button>

        <mj-spacer height="10px" />

        <mj-button href="{{ advisory_url }}" background-color="#6b7280" color="#ffffff" font-size="14px" border-radius="6px" padding="10px 25px">
          Leia o Aviso de Segurança
        </mj-button>

        <mj-spacer height="30px" />

        <mj-text font-size="13px" color="{{ theme.color.text_secondary|default:'#6b7280' }}" align="center">
          Se você precisar de assistência, entre em contato imediatamente com o suporte da Spwig.
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
🔒 ATUALIZAÇÃO DE SEGURANÇA NECESSÁRIA

Patch de Segurança Crítico

Foi descoberta uma vulnerabilidade de segurança em {{ component_name }}. Por favor, atualize imediatamente para proteger sua loja.

⚠️ INFORMAÇÕES DE SEGURANÇA:
- Componente: {{ component_name }}
- Versão Atual: {{ current_version }}
- Versão Corrigida: {{ patched_version }}
- Gravidade: {{ severity_level }}
- ID do CVE: {{ cve_id }}

DETALHES DA VULNERABILIDADE:
{{ vulnerability_description }}

IMPACTO POTENCIAL:
{{ impact_description }}

{% if mitigation_steps %}
MITIGAÇÃO TEMPORÁRIA:
{{ mitigation_steps }}
{% endif %}

AÇÃÃO NECESSÁRIA: INSTALE A ATUALIZAÇÃO IMEDIATAMENTE

Instale o patch de segurança: {{ update_url }}
Leia o aviso de segurança: {{ advisory_url }}

Se você precisar de assistência, entre em contato imediatamente com o suporte da Spwig.