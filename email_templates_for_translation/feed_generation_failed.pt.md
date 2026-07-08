---
template_type: feed_generation_failed
category: Product Feeds
---

# Email Template: feed_generation_failed

## Subject
❌ Geração do feed falhou: {{ feed_name }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#fee2e2">
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="#991b1b" align="center">
          ❌ Geração do Feed Falhou
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="18px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Erro de Geração
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}">
          O feed de produtos {{ feed_name }} falhou na geração devido a um erro.
        </mj-text>

        <mj-spacer height="20px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
              Detalhes do Erro:
            </mj-text>
            <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>Feed:</strong> {{ feed_name }}<br/>
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

        {% if error_log %}
        <mj-spacer height="20px" />
        <mj-text font-size="14px" color="{{ theme.color.text_secondary|default:'#6b7280' }}">
          <strong>Log de Erro:</strong><br/>
          <code style="font-size: 12px; color: #6b7280;">{{ error_log|truncatewords:30 }}</code>
        </mj-text>
        {% endif %}

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Causas Comuns:
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}" line-height="1.8">
          • Dados do produto ausentes (título, preço, imagem)<br/>
          • Formato inválido dos dados do produto<br/>
          • Problemas de conexão com o banco de dados<br/>
          • Espaço em disco ou memória insuficiente
        </mj-text>

        <mj-spacer height="30px" />

        <mj-button href="{{ retry_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          Tente Novamente
        </mj-button>

        <mj-spacer height="10px" />

        <mj-button href="{{ admin_feed_url }}" background-color="#6b7280" color="#ffffff" font-size="14px" border-radius="6px" padding="10px 25px">
          Ver Configurações do Feed
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
❌ GERAÇÃO DO FEED FALHOU

Erro de Geração

O feed de produtos {{ feed_name }} falhou na geração devido a um erro.

DETALHES DO ERRO:
- Feed: {{ feed_name }}
- Falhou em: {{ failed_at }}
- Código de Erro: {{ error_code }}

MENSAGEM DE ERRO:
{{ error_message }}

{% if error_log %}
LOG DE ERRO:
{{ error_log|truncatewords:30 }}
{% endif %}

CAUSAS COMUNS:
• Dados do produto ausentes (título, preço, imagem)
• Formato inválido dos dados do produto
• Problemas de conexão com o banco de dados
• Espaço em disco ou memória insuficiente

Tente novamente: {{ retry_url }}
Ver configurações do feed: {{ admin_feed_url }}

Se o problema persistir, entre em contato com o suporte com o código de erro {{ error_code }}.