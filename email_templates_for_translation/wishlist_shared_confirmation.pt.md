---
template_type: wishlist_shared_confirmation
category: Wishlist
---

# Email Template: wishlist_shared_confirmation

## Subject
✓ Sua lista de desejos foi compartilhada - {{ shop_name }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section>
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          ✓ Lista de Desejos Compartilhada com Sucesso!
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Olá {{ customer_name }},
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Sua lista de desejos com {{ wishlist_item_count }} item{{ wishlist_item_count|pluralize }} foi compartilhada com sucesso. Outras pessoas podem agora visualizar sua lista de desejos usando o link abaixo.
        </mj-text>

        <mj-spacer height="30px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
              Link para Compartilhar:
            </mj-text>
            <mj-text font-family="'Courier New', monospace" font-size="14px" color="{{ theme.color.primary|default:'#2563eb' }}">
              {{ share_url }}
            </mj-text>
            <mj-spacer height="15px" />
            <mj-button href="{{ share_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="14px" border-radius="6px" padding="10px 25px">
              Copiar Link
            </mj-button>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          O que foi Compartilhado:
        </mj-text>

        <mj-text font-size="14px" color="{{ theme.color.text|default:'#4b5563' }}">
          • O nome da sua lista de desejos (se definido)<br/>
          • {{ wishlist_item_count }} produto{{ wishlist_item_count|pluralize }}<br/>
          • Nomes, imagens e preços dos produtos<br/>
          • Links de compra para cada item
        </mj-text>

        <mj-spacer height="30px" />

        <mj-section background-color="#f0fdf4" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="14px" color="#065f46" align="center">
              💡 Perfeito para compartilhar com amigos e familiares para presentes e ocasiões especiais!
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-button href="{{ wishlist_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" border-radius="6px" padding="12px 30px">
          Gerenciar minha lista de desejos
        </mj-button>

        <mj-spacer height="20px" />

        <mj-text font-size="13px" color="{{ theme.color.text_secondary|default:'#6b7280' }}" align="center">
          Quer parar de compartilhar? Você pode desativar o link de compartilhamento a qualquer momento nas <a href="{{ wishlist_settings_url }}">configurações da lista de desejos</a>.
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
✓ LISTA DE DESEJOS COMPARTILHADA COM SUCESSO!

Olá {{ customer_name }},

Sua lista de desejos com {{ wishlist_item_count }} item{{ wishlist_item_count|pluralize }} foi compartilhada com sucesso. Outras pessoas podem agora visualizar sua lista de desejos usando o link abaixo.

LINK PARA COMPARTILHAR:
{{ share_url }}

O QUE FOI COMPARTILHADO:
• O nome da sua lista de desejos (se definido)
• {{ wishlist_item_count }} produto{{ wishlist_item_count|pluralize }}
• Nomes, imagens e preços dos produtos
• Links de compra para cada item

💡 Perfeito para compartilhar com amigos e familiares para presentes e ocasiões especiais!

Gerenciar minha lista de desejos: {{ wishlist_url }}

Quer parar de compartilhar? Você pode desativar o link de compartilhamento a qualquer momento nas configurações da lista de desejos: {{ wishlist_settings_url }}