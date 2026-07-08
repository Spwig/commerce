---
template_type: wishlist_shared_confirmation
category: Wishlist
---

# Email Template: wishlist_shared_confirmation

## Subject
✓ La tua lista dei desideri è stata condivisa - {{ shop_name }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section>
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          ✓ Lista dei desideri condivisa con successo!
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Ciao {{ customer_name }},
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          La tua lista dei desideri con {{ wishlist_item_count }} elemento{{ wishlist_item_count|pluralize }} è stata condivisa con successo. Altri possono ora visualizzare la tua lista dei desideri utilizzando il link qui sotto.
        </mj-text>

        <mj-spacer height="30px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
              Link di condivisione:
            </mj-text>
            <mj-text font-family="'Courier New', monospace" font-size="14px" color="{{ theme.color.primary|default:'#2563eb' }}">
              {{ share_url }}
            </mj-text>
            <mj-spacer height="15px" />
            <mj-button href="{{ share_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="14px" border-radius="6px" padding="10px 25px">
              Copia il link
            </mj-button>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Cosa è condiviso:
        </mj-text>

        <mj-text font-size="14px" color="{{ theme.color.text|default:'#4b5563' }}">
          • Il nome della tua lista dei desideri (se impostato)<br/>
          • {{ wishlist_item_count }} prodotto{{ wishlist_item_count|pluralize }}<br/>
          • Nomi, immagini e prezzi dei prodotti<br/>
          • Link per l'acquisto di ogni elemento
        </mj-text>

        <mj-spacer height="30px" />

        <mj-section background-color="#f0fdf4" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="14px" color="#065f46" align="center">
              💡 Ideale per condividere con amici e familiari per regali e occasioni speciali!
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-button href="{{ wishlist_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" border-radius="6px" padding="12px 30px">
          Gestisci la mia lista dei desideri
        </mj-button>

        <mj-spacer height="20px" />

        <mj-text font-size="13px" color="{{ theme.color.text_secondary|default:'#6b7280' }}" align="center">
          Vuoi smettere di condividere? Puoi disattivare il link di condivisione in qualsiasi momento nelle <a href="{{ wishlist_settings_url }}">impostazioni della tua lista dei desideri</a>.
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
✓ LISTA DEI DESIDERI CONDIVISA CON SUCCESSO!

Ciao {{ customer_name }},

La tua lista dei desideri con {{ wishlist_item_count }} elemento{{ wishlist_item_count|pluralize }} è stata condivisa con successo. Altri possono ora visualizzare la tua lista dei desideri utilizzando il link qui sotto.

LINK DI CONDIVISIONE:
{{ share_url }}

COSA È CONDIVISO:
• Il nome della tua lista dei desideri (se impostato)
• {{ wishlist_item_count }} prodotto{{ wishlist_item_count|pluralize }}
• Nomi, immagini e prezzi dei prodotti
• Link per l'acquisto di ogni elemento

💡 Ideale per condividere con amici e familiari per regali e occasioni speciali!

Gestisci la mia lista dei desideri: {{ wishlist_url }}

Vuoi smettere di condividere? Puoi disattivare il link di condivisione in qualsiasi momento nelle impostazioni della tua lista dei desideri: {{ wishlist_settings_url }}