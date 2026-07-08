---
template_type: hosted_suspended
category: License
---

# Email Template: hosted_suspended

## Subject
Magasin suspendu - {{ store_name }}

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
    <mj-section background-color="#dc2626" padding="30px 20px">
      <mj-column>
        <mj-text font-size="28px" font-weight="bold" color="#ffffff" align="center">
          Compte suspendu
        </mj-text>
        <mj-text font-size="16px" color="#ffffffcc" align="center" padding-top="10px">
          {{ store_name }}
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Greeting -->
    <mj-section>
      <mj-column>
        <mj-text font-size="16px">
          Bonjour {{ name|default:'there' }},
        </mj-text>
        <mj-text>
          Votre magasin <strong>{{ store_name }}</strong> a été suspendu en raison d'un solde impayé.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- What This Means -->
    <mj-section background-color="{{ theme.color.background_secondary|default:'#f9fafb' }}" padding="20px" border-radius="8px">
      <mj-column>
        <mj-text font-size="16px" font-weight="bold" padding-bottom="10px">
          Cela signifie quoi
        </mj-text>
        <mj-text font-size="14px">
          Votre magasin est désormais en mode lecture seule — les clients peuvent naviguer, mais les commandes sont désactivées. Vos données sont en sécurité et seront conservées pendant 30 jours.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Reactivate -->
    <mj-section>
      <mj-column>
        <mj-text>
          Pour rétablir l'accès complet, veuillez mettre à jour votre méthode de paiement et régler le solde restant.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- CTA -->
    {% include 'email_system/mjml_components/cta_button.mjml' with url="https://spwig.com/account" text="Réactiver votre magasin" %}

    <!-- Support -->
    {% include 'email_system/mjml_components/support_block.mjml' %}
  </mj-body>
</mjml>

## Text Content
Compte suspendu - {{ store_name }}

Bonjour {{ name|default:'there' }},

Votre magasin {{ store_name }} a été suspendu en raison d'un solde impayé.

Cela signifie quoi:
Votre magasin est désormais en mode lecture seule — les clients peuvent naviguer, mais les commandes sont désactivées. Vos données sont en sécurité et seront conservées pendant 30 jours.

Pour rétablir l'accès complet, veuillez mettre à jour votre méthode de paiement et régler le solde restant.

Réactiver votre magasin: https://spwig.com/account

Besoin d'aide ? Contactez {{ support_email }}