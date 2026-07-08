---
template_type: admin_new_order
category: Admin Notifications
---

# Email Template: admin_new_order

## Subject
Nouvelle commande reçue - Commande n°{{ order_number }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section>
      <mj-column>
        <mj-text font-size="20px" font-weight="bold">
          Nouvelle commande reçue
        </mj-text>
        <mj-text>
          Une nouvelle commande a été passée sur votre boutique.
        </mj-text>
        <mj-text>
          <strong>Numéro de commande :</strong> {{ order_number }}
        </mj-text>
        <mj-text>
          <strong>Client :</strong> {{ customer_name }}
        </mj-text>
        <mj-text>
          <strong>Total :</strong> {{ order_total }}
        </mj-text>
        <mj-button href="{{ admin_order_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}">
          Voir dans l'admin
        </mj-button>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
Nouvelle commande reçue

Une nouvelle commande a été passée sur votre boutique.

Numéro de commande : {{ order_number }}
Client : {{ customer_name }}
Total : {{ order_total }}

Voir dans l'admin : {{ admin_order_url }}
