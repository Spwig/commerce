---
template_type: license_maintenance_renewal
category: License
---

# Email Template: license_maintenance_renewal

## Subject
Maintenance Renouvelée - Commande n°{{ order_number }}

## HTML Content
<mjml>
  <mj-head>
    <mj-attributes>
      <mj-all font-family="'Helvetica Neue', Helvetica, Arial, sans-serif" />
      <mj-text font-size="14px" color="#333333" line-height="20px" />
      <mj-section background-color="{{ theme.color.background|default:'#ffffff' }}" padding="20px" />
    </mj-attributes>
  </mj-head>
  <mj-body background-color="{{ theme.color.background_secondary|default:'#f9fafb' }}">
    <!-- Header -->
    <mj-section background-color="{{ theme.color.success|default:'#10b981' }}" padding="30px 20px">
      <mj-column>
        <mj-text font-size="28px" font-weight="bold" color="#ffffff" align="center">
          Maintenance Renouvelée !
        </mj-text>
        <mj-text font-size="16px" color="#ffffffcc" align="center" padding-top="10px">
          Commande n°{{ order_number }}
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Greeting -->
    <mj-section>
      <mj-column>
        <mj-text font-size="16px">
          Bonjour {{ customer_name }},
        </mj-text>
        <mj-text>
          Votre abonnement de maintenance Spwig a été renouvelé avec succès. Vous continuerez à recevoir des mises à jour du plateau, des correctifs de sécurité et de nouvelles fonctionnalités.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Renewal Summary -->
    <mj-section background-color="{{ theme.color.background_secondary|default:'#f9fafb' }}" padding="20px" border-radius="8px">
      <mj-column>
        <mj-text font-size="16px" font-weight="bold" padding-bottom="10px">
          Résumé du renouvellement
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          Clé de licence : {{ license_key }}
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          Maintenance valide jusqu'au : {{ renewal_expires_at }}
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          Numéro de commande : {{ order_number }}
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- What's Included -->
    <mj-section>
      <mj-column>
        <mj-text font-size="16px" font-weight="bold" padding-bottom="10px">
          Ce qui est inclus
        </mj-text>
        <mj-text font-size="14px">
          Votre maintenance active vous donne accès à :
        </mj-text>
        <mj-text font-size="14px" padding-top="5px">
          - Mises à jour et améliorations des fonctionnalités du plateau
        </mj-text>
        <mj-text font-size="14px">
          - Correctifs de sécurité et de bugs
        </mj-text>
        <mj-text font-size="14px">
          - Nouvelles versions de composants via le serveur de mise à jour
        </mj-text>
        <mj-text font-size="14px">
          - Support technique
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Next Steps -->
    <mj-section>
      <mj-column>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          Aucune action de votre part n'est requise. Les mises à jour continueront d'être disponibles via le système de mise à jour des composants de votre panneau d'administration.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Support -->
    {% include 'email_system/mjml_components/support_block.mjml' %}
  </mj-body>
</mjml>

## Text Content
Maintenance Renouvelée !

Commande n°{{ order_number }}

Bonjour {{ customer_name }},

Votre abonnement de maintenance Spwig a été renouvelé avec succès. Vous continuerez à recevoir des mises à jour du plateau, des correctifs de sécurité et de nouvelles fonctionnalités.

Résumé du renouvellement:
- Clé de licence : {{ license_key }}
- Maintenance valide jusqu'au : {{ renewal_expires_at }}
- Numéro de commande : {{ order_number }}

Ce qui est inclus:
- Mises à jour et améliorations des fonctionnalités du plateau
- Correctifs de sécurité et de bugs
- Nouvelles versions de composants via le serveur de mise à jour
- Support technique

Aucune action de votre part n'est requise. Les mises à jour continueront d'être disponibles via le système de mise à jour des composants de votre panneau d'administration.

Besoin d'aide ? Contactez {{ support_email }}