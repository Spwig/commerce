---
template_type: wishlist_price_drop
category: Wishlist
---

# Email Template: wishlist_price_drop

## Subject
🔥 Alerta de Redução de Preço: {{ product_name }} está agora {{ discount_percentage }}% de desconto!

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#dcfce7">
      <mj-column>
        <mj-text font-size="24px" font-weight="bold" color="#065f46" align="center">
          🔥 Alerta de Redução de Preço!
        </mj-text>
        <mj-text font-size="18px" color="#047857" align="center">
          Economize {{ discount_percentage }}% no Item da Lista de Desejos
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Boa notícia, {{ customer_name }}!
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Um produto da sua lista de desejos acabou de reduzir o preço! Não perca essa oportunidade de economizar.
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
            <mj-spacer height="10px" />
            <mj-text font-size="14px" color="{{ theme.color.text_secondary|default:'#6b7280' }}">
              Era: <span style="text-decoration: line-through;">{{ original_price }}</span>
            </mj-text>
            <mj-text font-size="24px" font-weight="bold" color="#059669">
              Agora: {{ new_price }}
            </mj-text>
            <mj-text font-size="16px" font-weight="bold" color="#dc2626">
              Economize {{ savings_amount }} ({{ discount_percentage }}% DE DESCONTO)
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-button href="{{ product_url }}" background-color="#059669" color="#ffffff" font-size="18px" font-weight="bold" border-radius="6px" padding="18px 50px">
          Compre Agora & Economize {{ discount_percentage }}%
        </mj-button>

        <mj-spacer height="30px" />

        <mj-section background-color="#fee2e2" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="14px" color="#991b1b" align="center">
              ⏰ <strong>Limited Time:</strong> This sale won't last forever. Prices may go back up at any time!
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="20px" />

        <mj-text font-size="13px" color="{{ theme.color.text_secondary|default:'#6b7280' }}" align="center">
          Remover da lista de desejos: <a href="{{ remove_wishlist_url }}">Clique aqui</a>
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
🔥 ALERTA DE REDUÇÃO DE PREÇO!
Economize {{ discount_percentage }}% no Item da Lista de Desejos

Boa notícia, {{ customer_name }}!

Um produto da sua lista de desejos acabou de reduzir o preço! Não perca essa oportunidade de economizar.

{{ product_name }}
Era: {{ original_price }}
AGORA: {{ new_price }}
ECONOMIZE {{ savings_amount }} ({{ discount_percentage }}% DE DESCONTO)

Compre agora & economize {{ discount_percentage }}%: {{ product_url }}

⏰ TEMPO LIMITADO: Esta promoção não durará para sempre. Os preços podem voltar a subir a qualquer momento!

Remover da lista de desejos: {{ remove_wishlist_url }}