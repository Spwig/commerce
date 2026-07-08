---
template_type: wishlist_item_added_confirmation
category: Wishlist
---

# Email Template: wishlist_item_added_confirmation

## Subject
✓ {{ product_name }} adicionado à sua lista de desejos - {{ shop_name }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section>
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          ❤️ Adicionado à Sua Lista de Desejos!
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Olá {{ customer_name }},
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Você adicionou com sucesso {{ product_name }} à sua lista de desejos. Estaremos de olho nela para você!
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
            <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.primary|default:'#2563eb' }}">
              {{ product_price }}
            </mj-text>
            {% if product_in_stock %}
            <mj-text font-size="13px" color="#059669">
              ✓ Em Estoque
            </mj-text>
            {% else %}
            <mj-text font-size="13px" color="#dc2626">
              ⚠️ Fora de Estoque - Nós avisaremos quando voltar!
            </mj-text>
            {% endif %}
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-section background-color="#f0fdf4" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="14px" color="#065f46" align="center">
              💡 <strong>Vamos notificá-lo sobre:</strong><br/>
              • Redução de preços<br/>
              • Alertas de volta ao estoque<br/>
              • Vendas por tempo limitado
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-button href="{{ wishlist_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          Ver Minha Lista de Desejos
        </mj-button>

        {% if product_in_stock %}
        <mj-spacer height="10px" />
        <mj-button href="{{ product_url }}" background-color="#059669" color="#ffffff" font-size="14px" border-radius="6px" padding="10px 25px">
          Comprar Agora
        </mj-button>
        {% endif %}
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
❤️ ADICIONADO À SUA LISTA DE DESEJOS!

Olá {{ customer_name }},

Você adicionou com sucesso {{ product_name }} à sua lista de desejos. Estaremos de olho nela para você!

{{ product_name }}
Preço: {{ product_price }}
{% if product_in_stock %}✓ Em Estoque{% else %}⚠️ Fora de Estoque - Nós avisaremos quando voltar!{% endif %}

💡 VAMOS NOTIFICÁ-LO SOBRE:
• Redução de preços
• Alertas de volta ao estoque
• Vendas por tempo limitado

Ver minha lista de desejos: {{ wishlist_url }}
{% if product_in_stock %}Comprar agora: {{ product_url }}{% endif %}