---
template_type: hosted_onboarding_tips
category: License
---

# Email Template: hosted_onboarding_tips

## Subject
Conseils pour tirer le meilleur parti de {{ store_name }}

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
          Conseils pour commencer
        </mj-text>
        <mj-text font-size="16px" color="#ffffffcc" align="center" padding-top="10px">
          Tirer le meilleur parti de votre boutique Spwig
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
          Maintenant que <strong>{{ store_name }}</strong> est opérationnelle, voici quelques conseils pour vous aider à en tirer le meilleur parti.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Tip 1: Theme -->
    <mj-section background-color="{{ theme.color.background_secondary|default:'#f9fafb' }}" padding="20px" border-radius="8px">
      <mj-column>
        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.primary|default:'#2563eb' }}" padding-bottom="5px">
          Personnalisez votre apparence
        </mj-text>
        <mj-text font-size="14px">
          Rendez-vous à <strong>Design > Paramètres du thème</strong> pour choisir un thème, charger votre logo et définir les couleurs de votre marque. Votre boutique se met à jour instantanément, ce qui vous permet de prévisualiser les modifications en temps réel.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Tip 2: Products -->
    <mj-section>
      <mj-column>
        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.primary|default:'#2563eb' }}" padding-bottom="5px">
          Ajoutez vos produits
        </mj-text>
        <mj-text font-size="14px">
          Allez à <strong>Catalogue > Produits</strong> pour commencer à ajouter vos articles. Vous pouvez créer des variantes de produits (taille, couleur), définir les prix, gérer l'inventaire et charger des images de haute qualité.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Tip 3: Payments -->
    <mj-section background-color="{{ theme.color.background_secondary|default:'#f9fafb' }}" padding="20px" border-radius="8px">
      <mj-column>
        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.primary|default:'#2563eb' }}" padding-bottom="5px">
          Configurez les paiements
        </mj-text>
        <mj-text font-size="14px">
          Allez à <strong>Paramètres > Fournisseurs de paiement</strong> pour connecter Stripe, PayPal ou un autre mode de paiement. Vous pouvez activer plusieurs fournisseurs afin que vos clients puissent payer selon leur préférence.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Tip 4: Shipping -->
    <mj-section>
      <mj-column>
        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.primary|default:'#2563eb' }}" padding-bottom="5px">
          Configurez l'expédition
        </mj-text>
        <mj-text font-size="14px">
          Sous <strong>Paramètres > Expédition</strong>, configurez vos zones et tarifs d'expédition. Vous pouvez créer des règles de tarification fixes, basées sur le poids ou gratuites pour différentes régions.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Tip 5: SEO -->
    <mj-section background-color="{{ theme.color.background_secondary|default:'#f9fafb' }}" padding="20px" border-radius="8px">
      <mj-column>
        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.primary|default:'#2563eb' }}" padding-bottom="5px">
          Améliorez votre SEO
        </mj-text>
        <mj-text font-size="14px">
          Spwig génère automatiquement des cartes du site et des balises méta. Rendez-vous à <strong>Paramètres > SEO</strong> pour personnaliser vos titres de page, descriptions et images de partage social afin que les clients trouvent votre boutique.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- CTA -->
    {% include 'email_system/mjml_components/cta_button.mjml' with url=admin_url text="Accédez au panneau d'administration" %}

    <!-- Support -->
    {% include 'email_system/mjml_components/support_block.mjml' %}
  </mj-body>
</mjml>

## Text Content
Conseils pour commencer - {{ store_name }}

Bonjour {{ name|default:'there' }},

Maintenant que {{ store_name }} est opérationnelle, voici quelques conseils pour vous aider à en tirer le meilleur parti.

1. Personnalisez votre apparence
Rendez-vous à Design > Paramètres du thème pour choisir un thème, charger votre logo et définir les couleurs de votre marque.

2. Ajoutez vos produits
Allez à Catalogue > Produits pour commencer à ajouter vos articles avec des variantes, des prix et des images.

3. Configurez les paiements
Allez à Paramètres > Fournisseurs de paiement pour connecter Stripe, PayPal ou un autre mode de paiement.

4. Configurez l'expédition
Sous Paramètres > Expédition, configurez vos zones et tarifs d'expédition pour différentes régions.

5. Améliorez votre SEO
Rendez-vous à Paramètres > SEO pour personnaliser vos titres de page, descriptions et images de partage social.

Accédez au panneau d'administration: {{ admin_url }}

Besoin d'aide ? Contactez {{ support_email }}