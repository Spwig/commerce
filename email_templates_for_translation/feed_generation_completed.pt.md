---
template_type: feed_generation_completed
category: Product Feeds
---

# Email Template: feed_generation_completed

## Subject
✓ Feed de produto gerado: {{ feed_name }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#dcfce7">
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="#065f46" align="center">
          ✓ Feed Gerado com Sucesso
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="18px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Feed de Produto Pronto
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}">
          Seu feed de produto {{ feed_name }} foi gerado com sucesso e está pronto para uso.
        </mj-text>

        <mj-spacer height="20px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
              Detalhes do Feed:
            </mj-text>
            <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>Feed:</strong> {{ feed_name }}<br/>
              <strong>Formato:</strong> {{ feed_format }}<br/>
              <strong>Produtos:</strong> {{ product_count }}<br/>
              <strong>Gerado:</strong> {{ generated_at }}<br/>
              <strong>Tamanho do Arquivo:</strong> {{ file_size }}
            </mj-text>
          </mj-column>
        </mj-section>

        {% if warnings_count > 0 %}
        <mj-spacer height="20px" />
        <mj-section background-color="#fef3c7" border-radius="8px" padding="15px">
          <mj-column>
            <mj:text font-size="14px" color="#92400e" font-weight="bold">
              ⚠️ {{ warnings_count }} Aviso{{ warnings_count|pluralize }}
            </mj-text>
            <mj-text font-size="14px" color="#92400e">
              Alguns produtos têm problemas de qualidade dos dados. Revise os avisos no painel de administração.
            </mj-text>
          </mj-column>
        </mj-section>
        {% endif %}

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          URL do Feed:
        </mj-text>

        <mj-text font-size="13px" font-family="monospace" color="{{ theme.color.text_secondary|default:'#6b7280' }}" padding="10px" background-color="#f3f4f6">
          {{ feed_url }}
        </mj-text>

        <mj-spacer height="30px" />

        <mj-button href="{{ download_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          Baixar Feed
        </mj-button>

        <mj-spacer height="10px" />

        <mj-button href="{{ admin_feed_url }}" background-color="#6b7280" color="#ffffff" font-size="14px" border-radius="6px" padding="10px 25px">
          Ver no Admin
        </mj-button>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
✓ FEED GERADO COM SUCESSO

Feed de Produto Pronto

Seu feed de produto {{ feed_name }} foi gerado com sucesso e está pronto para uso.

DETALHES DO FEED:
- Feed: {{ feed_name }}
- Formato: {{ feed_format }}
- Produtos: {{ product_count }}
- Gerado: {{ generated_at }}
- Tamanho do Arquivo: {{ file_size }}

{% if warnings_count > 0 %}
⚠️ {{ warnings_count }} AVISO{{ warnings_count|pluralize|upper }}:
Alguns produtos têm problemas de qualidade dos dados. Revise os avisos no painel de administração.
{% endif %}

URL DO FEED:
{{ feed_url }}

Baixar feed: {{ download_url }}
Ver no admin: {{ admin_feed_url }}