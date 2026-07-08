---
template_type: feed_validation_errors
category: Product Feeds
---

# Email Template: feed_validation_errors

## Subject
⚠️ {{ feed_name }}: {{ error_count }} erros de validação encontrados

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#fef3c7">
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="#92400e" align="center">
          ⚠️ Erros de Validação do Feed
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="18px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Problemas de Qualidade de Dados Detectados
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}">
          {{ error_count }} erro de validação{{ error_count|pluralize }} encontrado no {{ feed_name }}. Esses problemas podem impedir que os produtos apareçam no {{ platform_name }}.
        </mj-text>

        <mj-spacer height="20px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
              Resumo da Validação:
            </mj-text>
            <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>Feed:</strong> {{ feed_name }}<br/>
              <strong>Plataforma:</strong> {{ platform_name }}<br/>
              <strong>Validado:</strong> {{ validated_at }}<br/>
              <strong>Total de Produtos:</strong> {{ total_products }}<br/>
              <strong>Produtos com Erros:</strong> {{ affected_products }}
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Principais Erros:
        </mj-text>

        {% for error in top_errors %}
        <mj-section background-color="#fee2e2" border-radius="8px" padding="12px">
          <mj-column>
            <mj-text font-size="14px" color="#991b1b" font-weight="bold">
              {{ error.type }}
            </mj-text>
            <mj-text font-size="13px" color="#991b1b">
              {{ error.count }} produto{{ error.count|pluralize }} afetado(s): {{ error.message }}
            </mj-text>
          </mj-column>
        </mj-section>
        <mj-spacer height="8px" />
        {% endfor %}

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          O Que Corrigir:
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}" line-height="1.8">
          {{ fix_instructions }}
        </mj-text>

        <mj-spacer height="30px" />

        <mj-button href="{{ errors_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          Ver Todos os Erros
        </mj-button>

        <mj-spacer height="10px" />

        <mj-button href="{{ admin_feed_url }}" background-color="#6b7280" color="#ffffff" font-size="14px" border-radius="6px" padding="10px 25px">
          Gerenciar Feed
        </mj-button>

        <mj-spacer height="20px" />

        <mj-text font-size="13px" color="{{ theme.color.text_secondary|default:'#6b7280' }}" align="center">
          Corrija esses erros para garantir que todos os produtos apareçam no {{ platform_name }}.
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
⚠️ ERROS DE VALIDAÇÃO DO FEED

Problemas de Qualidade de Dados Detectados

{{ error_count }} erro de validação{{ error_count|pluralize }} encontrado no {{ feed_name }}. Esses problemas podem impedir que os produtos apareçam no {{ platform_name }}.

RESUMO DA VALIDAÇÃO:
- Feed: {{ feed_name }}
- Plataforma: {{ platform_name }}
- Validado: {{ validated_at }}
- Total de Produtos: {{ total_products }}
- Produtos com Erros: {{ affected_products }}

PRINCIPAIS ERROS:
{% for error in top_errors %}
{{ error.type }}: {{ error.count }} produto{{ error.count|pluralize }} - {{ error.message }}
{% endfor %}

O QUE CORRIGIR:
{{ fix_instructions }}

Ver todos os erros: {{ errors_url }}
Gerenciar feed: {{ admin_feed_url }}

Corrija esses erros para garantir que todos os produtos apareçam no {{ platform_name }}.