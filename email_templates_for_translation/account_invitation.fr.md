---
template_type: account_invitation
category: Core E-commerce
---

# Email Template: account_invitation

## Subject
Créez votre compte sur {{ site_name }}

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
    <mj-section background-color="{{ theme.color.primary|default:'#2563eb' }}" padding="30px 20px">
      <mj-column>
        <mj-text font-size="28px" font-weight="bold" color="#ffffff" align="center">
          Vous êtes invité(e) !
        </mj-text>
        <mj-text font-size="16px" color="#ffffffcc" align="center" padding-top="10px">
          Créez votre compte sur {{ site_name }}
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
          Nous avons remarqué que vous avez acheté chez nous en tant que client invité. Créez un compte complet pour accéder à des avantages tels que le suivi des commandes, un paiement plus rapide et des offres exclusives.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Order History Summary -->
    <mj-section background-color="{{ theme.color.background_secondary|default:'#f9fafb' }}" padding="20px" border-radius="8px">
      <mj-column>
        <mj-text font-size="16px" font-weight="bold" padding-bottom="10px">
          Votre historique d'achats
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          Total des commandes : {{ total_orders }}
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          Montant total dépensé : {{ total_spent }}
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Benefits -->
    <mj-section>
      <mj-column>
        <mj-text font-size="16px" font-weight="bold" padding-bottom="10px">
          Pourquoi créer un compte ?
        </mj-text>
        <mj-text font-size="14px">
          - Suivez vos commandes et consultez votre historique d'achats
        </mj-text>
        <mj-text font-size="14px">
          - Paiement plus rapide avec des détails enregistrés
        </mj-text>
        <mj-text font-size="14px">
          - Gérez vos adresses et vos préférences
        </mj-text>
        <mj-text font-size="14px">
          - Accédez à des offres et promotions exclusives
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- CTA Button -->
    {% include 'email_system/mjml_components/cta_button.mjml' with url=activation_url text="Créez votre compte" %}

    <!-- Note -->
    <mj-section>
      <mj-column>
        <mj-text font-size="12px" color="{{ theme.color.text_muted|default:'#6b7280' }}" align="center">
          Ce lien vous permettra de définir un mot de passe pour votre compte. Votre historique d'achats existant sera conservé.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Support -->
    {% include 'email_system/mjml_components/support_block.mjml' %}
  </mj-body>
</mjml>

## Text Content
Vous êtes invité(e) à créer votre compte !

Bonjour {{ customer_name }},

Nous avons remarqué que vous avez acheté chez nous en tant que client invité. Créez un compte complet pour accéder à des avantages tels que le suivi des commandes, un paiement plus rapide et des offres exclusives.

Votre historique d'achats :
- Total des commandes : {{ total_orders }}
- Montant total dépensé : {{ total_spent }}

Pourquoi créer un compte ?
- Suivez vos commandes et consultez votre historique d'achats
- Paiement plus rapide avec des détails enregistrés
- Gérez vos adresses et vos préférences
- Accédez à des offres et promotions exclusives

Créez votre compte : {{ activation_url }}

Ce lien vous permettra de définir un mot de passe pour votre compte. Votre historique d'achats existant sera conservé.

Besoin d'aide ? Contactez {{ support_email }}