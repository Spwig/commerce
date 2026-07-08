---
template_type: hosted_provision_complete
category: License
---

# Email Template: hosted_provision_complete

## Subject
Votre Magasin est Prêt - {{ store_name }}

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
          Votre Magasin est En Ligne !
        </mj-text>
        <mj-text font-size="16px" color="#ffffffcc" align="center" padding-top="10px">
          {{ store_name }} est prêt pour vous
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
          Grande nouvelle ! Votre magasin Spwig <strong>{{ store_name }}</strong> a été provisionné et est désormais en ligne. Vous pouvez commencer à configurer vos produits, votre branding et vos méthodes de paiement dès maintenant.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Store Details -->
    <mj-section background-color="{{ theme.color.background_secondary|default:'#f9fafb' }}" padding="20px" border-radius="8px">
      <mj-column>
        <mj-text font-size="16px" font-weight="bold" padding-bottom="10px">
          Vos Détails de Magasin
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          URL du Magasin : {{ store_url }}
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          Tableau de Bord : {{ admin_url }}
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          Région : {{ region }}
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Getting Started -->
    <mj-section>
      <mj-column>
        <mj-text font-size="16px" font-weight="bold" padding-bottom="10px">
          Démarrage Rapide
        </mj-text>
        <mj-text font-size="14px">
          1. Connectez-vous à votre tableau de bord avec l'adresse e-mail et le mot de passe que vous avez définis lors de la commande
        </mj-text>
        <mj-text font-size="14px">
          2. Ajoutez votre logo et votre branding sous Design > Paramètres du thème
        </mj-text>
        <mj-text font-size="14px">
          3. Ajoutez vos premiers produits sous Catalogue > Produits
        </mj-text>
        <mj-text font-size="14px">
          4. Configurez un fournisseur de paiement sous Paramètres > Fournisseurs de paiement
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- CTA -->
    {% include 'email_system/mjml_components/cta_button.mjml' with url=admin_url text="Go to Admin Panel" %}

    <!-- Support -->
    {% include 'email_system/mjml_components/support_block.mjml' %}
  </mj-body>
</mjml>

## Text Content
Votre Magasin est En Ligne !

{{ store_name }} est prêt pour vous.

Bonjour {{ name|default:'there' }},

Grande nouvelle ! Votre magasin Spwig {{ store_name }} a été provisionné et est désormais en ligne. Vous pouvez commencer à configurer vos produits, votre branding et vos méthodes de paiement dès maintenant.

Vos Détails de Magasin:
- URL du Magasin: {{ store_url }}
- Tableau de Bord: {{ admin_url }}
- Région: {{ region }}

Démarrage Rapide:
1. Connectez-vous à votre tableau de bord avec l'adresse e-mail et le mot de passe que vous avez définis lors de la commande
2. Ajoutez votre logo et votre branding sous Design > Paramètres du thème
3. Ajoutez vos premiers produits sous Catalogue > Produits
4. Configurez un fournisseur de paiement sous Paramètres > Fournisseurs de paiement

Aller au Tableau de Bord: {{ admin_url }}

Besoin d'aide ? Contactez {{ support_email }}