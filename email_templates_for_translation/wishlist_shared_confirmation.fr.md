---
template_type: wishlist_shared_confirmation
category: Wishlist
---

# Email Template: wishlist_shared_confirmation

## Subject
✓ Votre liste de souhaits a été partagée - {{ shop_name }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section>
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          ✓ Liste de souhaits partagée avec succès !
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Bonjour {{ customer_name }},
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Votre liste de souhaits avec {{ wishlist_item_count }} élément{{ wishlist_item_count|pluralize }} a été partagée avec succès. Les autres peuvent maintenant consulter votre liste de souhaits en utilisant le lien ci-dessous.
        </mj-text>

        <mj-spacer height="30px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
              Lien de partage:
            </mj-text>
            <mj-text font-family="'Courier New', monospace" font-size="14px" color="{{ theme.color.primary|default:'#2563eb' }}">
              {{ share_url }}
            </mj-text>
            <mj-spacer height="15px" />
            <mj-button href="{{ share_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="14px" border-radius="6px" padding="10px 25px">
              Copier le lien
            </mj-button>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Ce qui est partagé:
        </mj-text>

        <mj-text font-size="14px" color="{{ theme.color.text|default:'#4b5563' }}">
          • Le nom de votre liste de souhaits (si défini)<br/>
          • {{ wishlist_item_count }} produit{{ wishlist_item_count|pluralize }}<br/>
          • Noms, images et prix des produits<br/>
          • Liens d'achat pour chaque élément
        </mj-text>

        <mj-spacer height="30px" />

        <mj-section background-color="#f0fdf4" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="14px" color="#065f46" align="center">
              💡 Idéal pour partager avec vos amis et votre famille pour des cadeaux et des occasions spéciales !
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-button href="{{ wishlist_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" border-radius="6px" padding="12px 30px">
          Gérer ma liste de souhaits
        </mj-button>

        <mj-spacer height="20px" />

        <mj-text font-size="13px" color="{{ theme.color.text_secondary|default:'#6b7280' }}" align="center">
          Vous souhaitez arrêter de partager ? Vous pouvez désactiver le lien de partage à tout moment dans vos <a href="{{ wishlist_settings_url }}">paramètres de liste de souhaits</a>.
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
✓ LISTE DE SOUHAITS PARTAGÉE AVEC SUCCÈS !

Bonjour {{ customer_name }},

Votre liste de souhaits avec {{ wishlist_item_count }} élément{{ wishlist_item_count|pluralize }} a été partagée avec succès. Les autres peuvent maintenant consulter votre liste de souhaits en utilisant le lien ci-dessous.

LIEN DE PARTAGE : 
{{ share_url }}

CE QUI EST PARTAGÉ : 
• Le nom de votre liste de souhaits (si défini)
• {{ wishlist_item_count }} produit{{ wishlist_item_count|pluralize }}
• Noms, images et prix des produits
• Liens d'achat pour chaque élément

💡 Idéal pour partager avec vos amis et votre famille pour des cadeaux et des occasions spéciales !

Gérer ma liste de souhaits : {{ wishlist_url }}

Vous souhaitez arrêter de partager ? Vous pouvez désactiver le lien de partage à tout moment dans vos paramètres de liste de souhaits : {{ wishlist_settings_url }}