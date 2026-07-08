---
template_type: back_in_stock_low_stock_warning
category: Stock Notifications
---

# Email Template: back_in_stock_low_stock_warning

## Subject
⚠️ {{ product_name }} está de volta, mas vendendo rápido! - {{ shop_name }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#fef3c7">
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="#92400e" align="center">
          ⚠️ Estoque Limitado - Aja Rápido!
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          {{ product_name }} Está de Volta no Estoque!
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Olá {{ customer_name }},
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Boa notícia! O item que você estava esperando está de volta no estoque. Mas apresse-se - temos apenas {{ stock_remaining }} unidade{{ stock_remaining|pluralize }} restante(s)!
        </mj-text>

        <mj-spacer height="30px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column width="35%">
            <mj-image src="{{ product_image }}" alt="{{ product_name }}" border-radius="8px" />
          </mj-column>
          <mj-column width="65%">
            <mj-text font-weight="bold" font-size="18px" color="{{ theme.color.text|default:'#1f2937' }}">
              {{ product_name }}
            </mj-text>
            <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}">
              {{ product_description }}
            </mj-text>
            <mj-text font-size="18px" font-weight="bold" color="{{ theme.color.primary|default:'#2563eb' }}">
              {{ product_price }}
            </mj-text>
            {% if variant_name %}
            <mj-text font-size="14px" color="{{ theme.color.text_secondary|default:'#6b7280' }}">
              Variante: {{ variant_name }}
            </mj-text>
            {% endif %}
            <mj-spacer height="10px" />
            <mj-text font-size="14px" color="#dc2626" font-weight="bold">
              ⚠️ Apenas {{ stock_remaining }} restante no estoque!
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-button href="{{ product_url }}" background-color="#dc2626" color="#ffffff" font-size="18px" font-weight="bold" border-radius="6px" padding="18px 50px">
          Compre Agora Antes que Acabe
        </mj-button>

        <mj-spacer height="20px" />

        <mj-section background-color="#fee2e2" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="14px" color="#991b1b" align="center">
              🔥 <strong>Este produto esgotou {{ times_sold_out }} vez{{ times_sold_out|pluralize }} no último mês!</strong><br/>
              Não perca novamente - compre agora enquanto durar o estoque.
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-size="13px" color="{{ theme.color.text_secondary|default:'#6b7280' }}" align="center">
          Não está mais interessado? <a href="{{ unsubscribe_url }}" style="color: {{ theme.color.primary|default:'#2563eb' }};">Cancelar inscrição nesta notificação</a>
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
⚠️ ESTOQUE LIMITADO - AJA RÁPIDO!

{{ product_name }} Está de Volta no Estoque!

Olá {{ customer_name }},

Boa notícia! O item que você estava esperando está de volta no estoque. Mas apresse-se - temos apenas {{ stock_remaining }} unidade{{ stock_remaining|pluralize }} restante(s)!

PRODUTO:
{{ product_name }}
{{ product_description }}
Preço: {{ product_price }}
{% if variant_name %}Variante: {{ variant_name }}{% endif %}

⚠️ APENAS {{ stock_remaining }} RESTANTE NO ESTOQUE!

Compre agora antes que acabe: {{ product_url }}

🔥 Este produto esgotou {{ times_sold_out }} vez{{ times_sold_out|pluralize }} no último mês!
Não perca novamente - compre agora enquanto durar o estoque.

Não está mais interessado? Cancelar inscrição: {{ unsubscribe_url }}