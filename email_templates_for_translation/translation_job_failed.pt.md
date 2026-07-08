---
template_type: translation_job_failed
category: Translation Service
---

# Email Template: translation_job_failed

## Subject
❌ Tarefa de tradução falhou: {{ content_type }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#fee2e2">
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="#991b1b" align="center">
          ❌ Tarefa de Tradução Falhou
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="18px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Erro de Tradução
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}">
          Sua tarefa de tradução em lote encontrou um erro e não pude ser concluída.
        </mj-text>

        <mj-spacer height="20px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
              Detalhes da Tarefa:
            </mj-text>
            <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>ID da Tarefa:</strong> {{ job_id }}<br/>
              <strong>Tipo de Conteúdo:</strong> {{ content_type }}<br/>
              <strong>Idiomas de Destino:</strong> {{ target_languages }}<br/>
              <strong>Falhou em:</strong> {{ failed_at }}<br/>
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

        {% if partial_completion %}
        <mj-spacer height="30px" />
        <mj-section background-color="#fef3c7" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="14px" color="#92400e" font-weight="bold">
              Conclusão Parcial
            </mj-text>
            <mj-text font-size="14px" color="#92400e" line-height="1.6">
              {{ items_completed }} de {{ total_items }} itens foram traduzidos com sucesso antes que o erro ocorresse.
            </mj-text>
          </mj-column>
        </mj-section>
        {% endif %}

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Causas Comuns:
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}" line-height="1.8">
          • Problemas de conexão com a API do serviço de tradução<br/>
          • Crédito insuficiente de tradução<br/>
          • Conteúdo de origem inválido ou corrompido<br/>
          • Par de idiomas não suportado
        </mj-text>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Ações Recomendadas:
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}" line-height="1.8">
          1. Verifique as configurações do serviço de tradução<br/>
          2. Verifique se há crédito de tradução disponível<br/>
          3. Revise a mensagem de erro para problemas específicos<br/>
          4. Tente novamente a tarefa de tradução
        </mj-text>

        <mj-spacer height="30px" />

        <mj-button href="{{ retry_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          Tente Novamente a Tradução
        </mj-button>

        <mj-spacer height="10px" />

        <mj-button href="{{ settings_url }}" background-color="#6b7280" color="#ffffff" font-size="14px" border-radius="6px" padding="10px 25px">
          Verifique as Configurações
        </mj-button>

        <mj-spacer height="20px" />

        <mj-text font-size="13px" color="{{ theme.color.text_secondary|default:'#6b7280' }}" align="center">
          Se o problema persistir, entre em contato com o suporte com o código de erro {{ error_code }}.
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
❌ TAREFA DE TRADUÇÃO FALHOU

Erro de Tradução

Sua tarefa de tradução em lote encontrou um erro e não pôde ser concluída.

DETALHES DA TAREFA:
- ID da Tarefa: {{ job_id }}
- Tipo de Conteúdo: {{ content_type }}
- Idiomas de Destino: {{ target_languages }}
- Falhou em: {{ failed_at }}
- Código de Erro: {{ error_code }}

MENSAGEM DE ERRO:
{{ error_message }}

{% if partial_completion %}
CONCLUSÃO PARCIAL:
{{ items_completed }} de {{ total_items }} itens foram traduzidos com sucesso antes que o erro ocorresse.
{% endif %}

CAUSAS COMUNS:
• Problemas de conexão com a API do serviço de tradução
• Crédito insuficiente de tradução
• Conteúdo de origem inválido ou corrompido
• Par de idiomas não suportado

AÇÕES RECOMENDADAS:
1. Verifique as configurações do serviço de tradução
2. Verifique se há crédito de tradução disponível
3. Revise a mensagem de erro para problemas específicos
4. Tente novamente a tarefa de tradução

Tente novamente a tradução: {{ retry_url }}
Verifique as configurações: {{ settings_url }}

Se o problema persistir, entre em contato com o suporte com o código de erro {{ error_code }}.