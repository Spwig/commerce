---
template_type: feed_sync_failed
category: Product Feeds
---

# Email Template: feed_sync_failed

## Subject
❌ Sincronização do {{ feed_name }} falhou para {{ platform_name }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#fee2e2">
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="#991b1b" align="center">
          ❌ Sincronização Falhou
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="18px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Erro de Sincronização
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}">
          Falha na sincronização do {{ feed_name }} para {{ platform_name }}.
        </mj-text>

        <mj-spacer height="20px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
              Detalhes do Falha:
            </mj-text>
            <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>Feed:</strong> {{ feed_name }}<br/>
              <strong>Plataforma:</strong> {{ platform_name }}<br/>
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

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Causas Comuns:
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}" line-height="1.8">
          • Credenciais de API inválidas ou token expirado<br/>
          • Problemas de conectividade de rede<br/>
          • Limites de taxa da API da plataforma excedidos<br/>
          • O formato do feed não atende aos requisitos da plataforma
        </mj-text>

        {% if recommended_action %}
        <mj-spacer height="30px" />
        <mj-section background-color="#fef3c7" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="14px" color="#92400e" font-weight="bold">
              Ação Recomendada
            </mj-text>
            <mj-text font-size="14px" color="#92400e" line-height="1.6">
              {{ recommended_action }}
            </mj-text>
          </mj-column>
        </mj-section>
        {% endif %}

        <mj-spacer height="30px" />

        <mj-button href="{{ retry_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          Tentar Novamente
        </mj-button>

        <mj-spacer height="10px" />

        <mj-button href="{{ admin_feed_url }}" background-color="#6b7280" color="#ffffff" font-size="14px" border-radius="6px" padding="10px 25px">
          Verificar Configurações do Feed
        </mj-button>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
❌ SINCRONIZAÇÃO FALHOU

Erro de Sincronização

Falha na sincronização do {{ feed_name }} para {{ platform_name }}.

DETALHES DA FALHA:
- Feed: {{ feed_name }}
- Plataforma: {{ platform_name }}
- Falhou em: {{ failed_at }}
- Código de Erro: {{ error_code }}

MENSAGEM DE ERRO:
{{ error_message }}

CAUSAS COMUNS:
• Credenciais de API inválidas ou token expirado
• Problemas de conectividade de rede
• Limites de taxa da API da plataforma excedidos
• O formato do feed não atende aos requisitos da plataforma

{% if recommended_action %}
AÇÃO RECOMENDADA:
{{ recommended_action }}
{% endif %}

Tentar sincronização novamente: {{ retry_url }}
Verificar configurações do feed: {{ admin_feed_url }}