---
template_type: shipping_delayed
category: Shipping
---

# Email Template: shipping_delayed

## Subject
Mise à jour sur votre commande n°{{ order_number }} - Retard de livraison

## HTML Content
<mjml>
  <mj-body>
    <mj-section>
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Mise à jour sur votre commande
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Bonjour {{ customer_name }},
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Nous souhaitons vous informer d'un retard concernant votre commande. Nous nous excusons pour l'inconvenance et apprécions votre patience.
        </mj-text>

        <mj-spacer height="20px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
              Détails de la commande:
            </mj-text>
            <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>Numéro de commande:</strong> {{ order_number }}<br/>
              <strong>Date de livraison initiale:</strong> {{ original_delivery_date }}<br/>
              <strong>Nouvelle date de livraison:</strong> {{ new_delivery_date }}<br/>
              <strong>Numéro de suivi:</strong> {{ tracking_number }}
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="20px" />

        <mj-text font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Raison du retard:
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}">
          {{ delay_reason }}
        </mj-text>

        <mj-spacer height="30px" />

        <mj-button href="{{ tracking_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          Suivez votre commande
        </mj-button>

        <mj-spacer height="20px" />

        <mj-text font-size="14px" color="{{ theme.color.text_secondary|default:'#6b7280' }}">
          Nous faisons de notre mieux pour livrer votre commande aussi rapidement que possible. Vous recevrez une autre mise à jour lorsque votre colis sera en route.
        </mj-text>

        <mj-spacer height="20px" />

        <mj-text font-size="14px" color="{{ theme.color.text_secondary|default:'#6b7280' }}" align="center">
          Des questions ? <a href="{{ support_url }}" style="color: {{ theme.color.primary|default:'#2563eb' }};">Contactez notre équipe de service client</a>
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
Mise à jour sur votre commande n°{{ order_number }}

Bonjour {{ customer_name }},

Nous souhaitons vous informer d'un retard concernant votre commande. Nous nous excusons pour l'inconvenance et apprécions votre patience.

DÉTAILS DE LA COMMANDE:
- Numéro de commande: {{ order_number }}
- Date de livraison initiale: {{ original_delivery_date }}
- Nouvelle date de livraison: {{ new_delivery_date }}
- Numéro de suivi: {{ tracking_number }}

RAISON DU RETARD:
{{ delay_reason }}

Suivez votre commande: {{ tracking_url }}

Nous faisons de notre mieux pour livrer votre commande aussi rapidement que possible. Vous recevrez une autre mise à jour lorsque votre colis sera en route.

Des questions ? Contactez notre équipe de service client: {{ support_url }}

---
Cette mise à jour concerne la commande n°{{ order_number }} à {{ shop_name }}.