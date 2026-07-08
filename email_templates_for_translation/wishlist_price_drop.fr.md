---
template_type: wishlist_price_drop
category: Wishlist
---

# Email Template: wishlist_price_drop

## Subject
🔥 Alerte de baisse de prix : {{ product_name }} est maintenant à {{ discount_percentage }}% de réduction !

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#dcfce7">
      <mj-column>
        <mj-text font-size="24px" font-weight="bold" color="#065f46" align="center">
          🔥 Alerte de baisse de prix !
        </mj-text>
        <mj-text font-size="18px" color="#047857" align="center">
          Économisez {{ discount_percentage }}% sur votre article de la liste de souhaits
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Grande nouvelle, {{ customer_name }} !
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Un produit de votre liste de souhaits vient de baisser de prix ! Ne manquez pas cette opportunité d'économiser.
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
              Was: <span style="text-decoration: line-through;">{{ original_price }}</span>
            </mj-text>
            <mj-text font-size="24px" font-weight="bold" color="#059669">
              Now: {{ new_price }}
            </mj-text>
            <mj-text font-size="16px" font-weight="bold" color="#dc2626">
              Économisez {{ savings_amount }} ({{ discount_percentage }}% DE RÉDUCTION)
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-button href="{{ product_url }}" background-color="#059669" color="#ffffff" font-size="18px" font-weight="bold" border-radius="6px" padding="18px 50px">
          Acheter maintenant & économiser {{ discount_percentage }}%
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
          Remove from wishlist: <a href="{{ remove_wishlist_url }}">Click here</a>
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
🔥 ALERTE DE BAISSE DE PRIX !
Économisez {{ discount_percentage }}% sur votre article de la liste de souhaits

Grande nouvelle, {{ customer_name }} !

Un produit de votre liste de souhaits vient de baisser de prix ! Ne manquez pas cette opportunité d'économiser.

{{ product_name }}
Was: {{ original_price }}
NOW: {{ new_price }}
Économisez {{ savings_amount }} ({{ discount_percentage }}% DE RÉDUCTION)

Acheter maintenant & économiser {{ discount_percentage }}% : {{ product_url }}

⏰ DURÉE LIMITÉE : Cette offre ne durera pas éternellement. Les prix peuvent remonter à tout moment !

Retirer de la liste de souhaits : {{ remove_wishlist_url }}