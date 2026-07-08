---
template_type: admin_payment_sdk_failure
category: Admin Notifications
---

# Email Template: admin_payment_sdk_failure

## Subject
Problème avec le fournisseur de paiement - Le SDK {{ provider_name }} n'a pas pu être chargé

## HTML Content
<mjml>
  <mj-body>
    <mj-section>
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="{{ theme.color.warning|default:'#f59e0b' }}">
          Problème avec le fournisseur de paiement
        </mj-text>
        <mj-text>
          Le SDK de paiement {{ provider_name }} n'a pas pu être chargé pour un client lors de la validation de la commande. Cela peut indiquer une interruption de service du fournisseur.
        </mj-text>
        <mj-text>
          <strong>Fournisseur :</strong> {{ provider_name }}
        </mj-text>
        <mj-text>
          <strong>Type d'erreur :</strong> {{ error_type }}
        </mj-text>
        <mj-text>
          <strong>Heure :</strong> {{ timestamp }}
        </mj-text>
        <mj-text>
          <strong>Nombre de défaillances (dernière heure) :</strong> {{ failure_count }}
        </mj-text>
        <mj-divider border-color="{{ theme.color.border|default:'#e5e7eb' }}" />
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          Cette notification est limitée à une par fournisseur par heure. Si le problème persiste, vérifiez le tableau de bord du fournisseur ou contactez leur support.
        </mj-text>
        <mj-button href="{{ admin_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}">
          Voir les paramètres de paiement
        </mj-button>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
Problème avec le fournisseur de paiement

Le SDK de paiement {{ provider_name }} n'a pas pu être chargé pour un client lors de la validation de la commande. Cela peut indiquer une interruption de service du fournisseur.

Fournisseur : {{ provider_name }}
Type d'erreur : {{ error_type }}
Heure : {{ timestamp }}
Nombre de défaillances (dernière heure) : {{ failure_count }}

Cette notification est limitée à une par fournisseur par heure. Si le problème persiste, vérifiez le tableau de bord du fournisseur ou contactez leur support.

Voir les paramètres de paiement : {{ admin_url }}