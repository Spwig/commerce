---
template_type: cart_recovered_thank_you
category: Cart Recovery
---

# Email Template: cart_recovered_thank_you

## Subject
Merci pour votre commande n°{{ order_number }} - {{ shop_name }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section>
      <mj-column>
        <mj-text font-size="24px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}" align="center">
          🎉 Merci pour votre commande !
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Hi {{ customer_name }},
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Nous sommes ravis que vous ayez terminé votre achat ! Votre commande a été confirmée et nous la préparons pour l'expédition.
        </mj-text>

        <mj-spacer height="30px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
              Résumé de la commande
            </mj-text>
            <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>Numéro de commande :</strong> {{ order_number }}<br/>
              <strong>Date de commande :</strong> {{ order_date }}<br/>
              <strong>Total :</strong> {{ order_total }}
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-button href="{{ order_tracking_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          Suivez votre commande
        </mj-button>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Qu'est-ce qui arrive ensuite ?
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}" line-height="1.8">
          1. Nous préparerons votre commande (généralement dans les 1 à 2 jours ouvrés)<br/>
          2. Vous recevrez une confirmation d'expédition avec les informations de suivi<br/>
          3. Votre commande sera livrée à : {{ shipping_address }}
        </mj-text>

        <mj-spacer height="30px" />

        <mj-section background-color="#f0fdf4" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="14px" color="#065f46" align="center">
              💡 <strong>Le saviez-vous ?</strong><br/>
              Vous pouvez suivre votre commande à tout moment depuis le tableau de bord de votre compte.
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="20px" />

        <mj-text font-size="14px" color="{{ theme.color.text_secondary|default:'#6b7280' }}" align="center">
          Questions ? <a href="{{ support_url }}" style="color: {{ theme.color.primary|default:'#2563eb' }};">Contactez notre équipe de support</a>
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
🎉 MERCi POUR VOTRE COMMANDE !

Hi {{ customer_name }},

Nous sommes ravis que vous ayez terminé votre achat ! Votre commande a été confirmée et nous la préparons pour l'expédition.

RÉSUMÉ DE LA COMMANDE : 
- Numéro de commande : {{ order_number }}
- Date de commande : {{ order_date }}
- Total : {{ order_total }}

Suivez votre commande : {{ order_tracking_url }}

QU'EST-CE QUI ARRIVE EN SUITE ?
1. Nous préparerons votre commande (généralement dans les 1 à 2 jours ouvrés)
2. Vous recevrez une confirmation d'expédition avec les informations de suivi
3. Votre commande sera livrée à : {{ shipping_address }}

💡 LE SAVIEZ-VOUS ?
Vous pouvez suivre votre commande à tout moment depuis le tableau de bord de votre compte.

Questions ? Contactez notre équipe de support : {{ support_url }}

---
Commande n°{{ order_number }} à {{ shop_name }}