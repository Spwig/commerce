---
template_type: component_update_failed
category: Component Updates
---

# Email Template: component_update_failed

## Subject
❌ Atualização Falhou: {{ component_name }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#fee2e2">
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="#991b1b" align="center">
          ❌ Atualização Falhou
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="18px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Erro de Instalação
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}">
          A atualização para {{ component_name }} para a versão {{ target_version }} falhou na instalação.
        </mj-text>

        <mj-spacer height="20px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
              Detalhes do Falha:
            </mj-text>
            <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>Componente:</strong> {{ component_name }}<br/>
              <strong>Versão Alvo:</strong> {{ target_version }}<br/>
              <strong>Falhou Em:</strong> {{ failed_at }}<br/>
              <strong>Código de Erro:</strong> {{ error_code }}
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Mensagem de Erro:
        </mj-text>

        <mj-section background-color="#fee2e2" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="14px" font-family="monospace" color="#991b1b" line-height="1.6">
              {{ error_message }}
            </mj-text>
          </mj-column>
        </mj-section>

        {% if error_log %}
        <mj-spacer height="20px" />
        <mj-text font-size="14px" color="{{ theme.color.text_secondary|default:'#6b7280' }}">
          <strong>Log de Erro Completo:</strong><br/>
          <code style="font-size: 12px; color: #6b7280;">{{ error_log|truncatewords:50 }}</code>
        </mj-text>
        {% endif %}

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          O que Fazer:
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}" line-height="1.8">
          1. Verifique os requisitos do sistema e dependências<br/>
          2. Revise o log de erro para detalhes<br/>
          3. Tente instalar novamente, ou entre em contato com o suporte<br/>
          4. Seu loja ainda está rodando na {{ current_version }}
        </mj-text>

        <mj-spacer height="30px" />

        <mj-button href="{{ retry_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          Tente Novamente a Instalação
        </mj-button>

        <mj-spacer height="10px" />

        <mj-button href="{{ support_url }}" background-color="#6b7280" color="#ffffff" font-size="14px" border-radius="6px" padding="10px 25px">
          Entre em Contato com o Suporte
        </mj-button>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
❌ ATUALIZAÇÃO FALHOU

Erro de Instalação

A atualização para {{ component_name }} para a versão {{ target_version }} falhou na instalação.

DETALHES DA FALHA:
- Componente: {{ component_name }}
- Versão Alvo: {{ target_version }}
- Falhou Em: {{ failed_at }}
- Código de Erro: {{ error_code }}

MENSAGEM DE ERRO:
{{ error_message }}

{% if error_log %}
LOG DE ERRO COMPLETO:
{{ error_log|truncatewords:50 }}
{% endif %}

O QUE FAZER:
1. Verifique os requisitos do sistema e dependências
2. Revise o log de erro para detalhes
3. Tente instalar novamente, ou entre em contato com o suporte
4. Seu loja ainda está rodando na {{ current_version }}

Tente novamente a instalação: {{ retry_url }}
Entre em contato com o suporte: {{ support_url }}