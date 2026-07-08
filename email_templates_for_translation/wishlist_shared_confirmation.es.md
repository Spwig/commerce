---
template_type: wishlist_shared_confirmation
category: Wishlist
---

# Email Template: wishlist_shared_confirmation

## Subject
✓ Tu lista de deseos ha sido compartida - {{ shop_name }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section>
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          ✓ Lista de Deseos Compartida Exitosamente!
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Hola {{ customer_name }},
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Tu lista de deseos con {{ wishlist_item_count }} elemento{{ wishlist_item_count|pluralize }} ha sido compartida con éxito. Ahora otros pueden ver tu lista de deseos usando el enlace de abajo.
        </mj-text>

        <mj-spacer height="30px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
              Enlace para Compartir:
            </mj-text>
            <mj-text font-family="'Courier New', monospace" font-size="14px" color="{{ theme.color.primary|default:'#2563eb' }}">
              {{ share_url }}
            </mj-text>
            <mj-spacer height="15px" />
            <mj-button href="{{ share_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="14px" border-radius="6px" padding="10px 25px">
              Copiar Enlace
            </mj-button>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          ¿Qué se comparte:
        </mj-text>

        <mj-text font-size="14px" color="{{ theme.color.text|default:'#4b5563' }}">
          • El nombre de tu lista de deseos (si está establecido)<br/>
          • {{ wishlist_item_count }} producto{{ wishlist_item_count|pluralize }}<br/>
          • Nombres de productos, imágenes y precios<br/>
          • Enlaces de compra para cada elemento
        </mj-text>

        <mj-spacer height="30px" />

        <mj-section background-color="#f0fdf4" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="14px" color="#065f46" align="center">
              💡 ¡Perfecto para compartir con amigos y familiares para regalos y ocasiones especiales!
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-button href="{{ wishlist_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" border-radius="6px" padding="12px 30px">
          Administrar mi lista de deseos
        </mj-button>

        <mj-spacer height="20px" />

        <mj-text font-size="13px" color="{{ theme.color.text_secondary|default:'#6b7280' }}" align="center">
          ¿Quieres dejar de compartir? Puedes deshabilitar el enlace de compartir en cualquier momento en tu <a href="{{ wishlist_settings_url }}">configuración de la lista de deseos</a>.
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
✓ LISTA DE DESEOS COMPARTIDA EXITOSAMENTE!

Hola {{ customer_name }},

Tu lista de deseos con {{ wishlist_item_count }} elemento{{ wishlist_item_count|pluralize }} ha sido compartida con éxito. Ahora otros pueden ver tu lista de deseos usando el enlace de abajo.

ENLACE PARA COMPARTIR:
{{ share_url }}

¿QUÉ SE COMPARTIÓ:
• El nombre de tu lista de deseos (si está establecido)
• {{ wishlist_item_count }} producto{{ wishlist_item_count|pluralize }}
• Nombres de productos, imágenes y precios
• Enlaces de compra para cada elemento

💡 ¡Perfecto para compartir con amigos y familiares para regalos y ocasiones especiales!

Administrar mi lista de deseos: {{ wishlist_url }}

¿Quieres dejar de compartir? Puedes deshabilitar el enlace de compartir en cualquier momento en tu configuración de la lista de deseos: {{ wishlist_settings_url }}