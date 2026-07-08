---
template_type: wishlist_item_added_confirmation
category: Wishlist
---

# Email Template: wishlist_item_added_confirmation

## Subject
✓ {{ product_name }} ajouté à votre liste de souhaits - {{ shop_name }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section>
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          ❤️ Ajouté à votre liste de souhaits !
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Bonjour {{ customer_name }},
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Vous avez ajouté {{ product_name }} à votre liste de souhaits. Nous le surveillerons pour vous !
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
              ✓ En stock
            </mj-text>
            {% else %}
            <mj-text font-size="13px" color="#dc2626">
              ⚠️ En rupture de stock - Nous vous informerons lors de son retour !
            </mj-text>
            {% endif %}
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-section background-color="#f0fdf4" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="14px" color="#065f46" align="center">
              💡 <strong>Nous vous informerons concernant :</strong><br/>
              • Des baisses de prix<br/>
              • Des alertes de disponibilité<br/>
              • Des ventes à durée limitée
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-button href="{{ wishlist_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          Voir ma liste de souhaits
        </mj-button>

        {% if product_in_stock %}
        <mj-spacer height="10px" />
        <mj-button href="{{ product_url }}" background-color="#059669" color="#ffffff" font-size="14px" border-radius="6px" padding="10px 25px">
          Acheter maintenant
        </mj-button>
        {% endif %}
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
❤️ AJOUTÉ À VOTRE LISTE DE SOUHAITS !

Bonjour {{ customer_name }},

Vous avez ajouté {{ product_name }} à votre liste de souhaits. Nous le surveillerons pour vous !

{{ product_name }}
Price: {{ product_price }}
{% if product_in_stock %}✓ En stock{% else %}⚠️ En rupture de stock - Nous vous informerons lors de son retour !{% endif %}

💡 NOUS VOUS INFORMERONS CONCERNANT : 
• Des baisses de prix
• Des alertes de disponibilité
• Des ventes à durée limitée

Voir ma liste de souhaits : {{ wishlist_url }}
{% if product_in_stock %}Acheter maintenant : {{ product_url }}{% endif %}