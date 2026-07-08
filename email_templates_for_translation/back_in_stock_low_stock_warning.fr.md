---
template_type: back_in_stock_low_stock_warning
category: Stock Notifications
---

# Email Template: back_in_stock_low_stock_warning

## Subject
⚠️ {{ product_name }} est de retour mais en stock limité ! - {{ shop_name }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#fef3c7">
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="#92400e" align="center">
          ⚠️ Stock limité - Agissez vite !
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          {{ product_name }} est de retour en stock !
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Hi {{ customer_name }},
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Grande nouvelle ! Le produit que vous attendiez est de retour en stock. Mais dépêchez-vous - nous n'avons que {{ stock_remaining }} unité{{ stock_remaining|pluralize }} restante{{ stock_remaining|pluralize }} !
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
              Variant: {{ variant_name }}
            </mj-text>
            {% endif %}
            <mj-spacer height="10px" />
            <mj-text font-size="14px" color="#dc2626" font-weight="bold">
              ⚠️ Seulement {{ stock_remaining }} restant en stock !
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-button href="{{ product_url }}" background-color="#dc2626" color="#ffffff" font-size="18px" font-weight="bold" border-radius="6px" padding="18px 50px">
          Achetez maintenant avant qu'il ne soit épuisé
        </mj-button>

        <mj-spacer height="20px" />

        <mj-section background-color="#fee2e2" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="14px" color="#991b1b" align="center">
              🔥 <strong>Ce produit a été en rupture de stock {{ times_sold_out }} fois{{ times_sold_out|pluralize }} le mois dernier !</strong><br/>
              Ne manquez plus jamais cette opportunité - commandez maintenant tant que les stocks durent.
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-size="13px" color="{{ theme.color.text_secondary|default:'#6b7280' }}" align="center">
          Plus intéressé ? <a href="{{ unsubscribe_url }}" style="color: {{ theme.color.primary|default:'#2563eb' }};">Se désinscrire de cette notification</a>
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
⚠️ STOCK LIMITÉ - AGISSEZ VITE !

{{ product_name }} est de retour en stock !

Hi {{ customer_name }},

Grande nouvelle ! Le produit que vous attendiez est de retour en stock. Mais dépêchez-vous - nous n'avons que {{ stock_remaining }} unité{{ stock_remaining|pluralize }} restante{{ stock_remaining|pluralize }} !

PRODUIT : 
{{ product_name }}
{{ product_description }}
Price: {{ product_price }}
{% if variant_name %}Variant: {{ variant_name }}{% endif %}

⚠️ SEULEMENT {{ stock_remaining }} RESTANT EN STOCK !

Achetez maintenant avant qu'il ne soit épuisé : {{ product_url }}

🔥 Ce produit a été en rupture de stock {{ times_sold_out }} fois{{ times_sold_out|pluralize }} le mois dernier !
Ne manquez plus jamais cette opportunité - commandez maintenant tant que les stocks durent.

Plus intéressé ? Se désinscrire : {{ unsubscribe_url }}
