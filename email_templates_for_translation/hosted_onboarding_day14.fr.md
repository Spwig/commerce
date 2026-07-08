---
template_type: hosted_onboarding_day14
category: License
---

# Email Template: hosted_onboarding_day14

## Subject
Pousser Plus loin - {{ store_name }}

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
          Démarrage : Fonctionnalités avancées
        </mj-text>
        <mj-text font-size="16px" color="#ffffffcc" align="center" padding-top="10px">
          Découvrez le plein potentiel de {{ store_name }}
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
          Vous utilisez {{ store_name }} depuis quelques semaines maintenant. Voici quelques fonctionnalités avancées pour vous aider à améliorer votre boutique.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Tip 1 -->
    <mj-section background-color="{{ theme.color.background_secondary|default:'#f9fafb' }}" padding="20px" border-radius="8px">
      <mj-column>
        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.primary|default:'#2563eb' }}" padding-bottom="5px">
          Mettez en place des workflows d'e-mails automatisés
        </mj-text>
        <mj-text font-size="14px">
          Automatisez votre communication avec les clients via des workflows d'e-mails. Configurez des séquences de bienvenue, des rappels post-achat et des campagnes de réengagement sous <strong>Marketing > Workflows d'e-mails</strong>.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Tip 2 -->
    <mj-section>
      <mj-column>
        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.primary|default:'#2563eb' }}" padding-bottom="5px">
          Configurez les règles de taxes pour vos régions
        </mj-text>
        <mj-text font-size="14px">
          Assurez-vous de facturer les taux de taxes corrects. Allez dans <strong>Paramètres > Taxes</strong> pour configurer les règles de taxes pour chaque région dans laquelle vous vendez. Vous pouvez configurer des prix avec ou sans taxes.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Tip 3 -->
    <mj-section background-color="{{ theme.color.background_secondary|default:'#f9fafb' }}" padding="20px" border-radius="8px">
      <mj-column>
        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.primary|default:'#2563eb' }}" padding-bottom="5px">
          Explorez l'API pour les intégrations
        </mj-text>
        <mj-text font-size="14px">
          Si votre plan inclut l'accès à l'API, vous pouvez intégrer votre boutique avec des outils et services externes. Rendez-vous sur <strong>Paramètres > API</strong> pour générer des clés API et explorer la documentation.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Tip 4 -->
    <mj-section>
      <mj-column>
        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.primary|default:'#2563eb' }}" padding-bottom="5px">
          Consultez votre tableau de bord d'analyse
        </mj-text>
        <mj-text font-size="14px">
          Suivez les performances de votre boutique. Votre <strong>Tableau de bord</strong> affiche des métriques clés telles que le chiffre d'affaires, les commandes, les produits les plus vendus et des informations sur les clients pour vous aider à prendre des décisions basées sur les données.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Tip 5 -->
    <mj-section background-color="{{ theme.color.background_secondary|default:'#f9fafb' }}" padding="20px" border-radius="8px">
      <mj-column>
        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.primary|default:'#2563eb' }}" padding-bottom="5px">
          Pensez à ajouter un point de vente pour les ventes en magasin
        </mj-text>
        <mj-text font-size="14px">
          Vendez aussi en personne ? La fonctionnalité de point de vente de Spwig vous permet de traiter les transactions en magasin qui s'ynchronisent avec votre inventaire en ligne et votre gestion des commandes. Consultez <strong>Paramètres > Point de vente</strong> pour en savoir plus.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- CTA -->
    {% include 'email_system/mjml_components/cta_button.mjml' with url=admin_url text="Explorer votre tableau de bord" %}

    <!-- Support -->
    {% include 'email_system/mjml_components/support_block.mjml' %}
  </mj-body>
</mjml>

## Text Content
Démarrage : Fonctionnalités avancées - {{ store_name }}

Bonjour {{ name|default:'there' }},

Vous utilisez {{ store_name }} depuis quelques semaines maintenant. Voici quelques fonctionnalités avancées pour vous aider à améliorer votre boutique.

1. Mettez en place des workflows d'e-mails automatisés
Automatisez votre communication avec les clients via des séquences de bienvenue, des rappels post-achat et des campagnes de réengagement.

2. Configurez les règles de taxes pour vos régions
Assurez-vous de facturer les taux de taxes corrects. Allez dans Paramètres > Taxes pour configurer les règles pour chaque région.

3. Explorez l'API pour les intégrations
Si votre plan inclut l'accès à l'API, intégrez votre boutique avec des outils externes. Rendez-vous sur Paramètres > API pour commencer.

4. Consultez votre tableau de bord d'analyse
Votre tableau de bord affiche des métriques clés telles que le chiffre d'affaires, les commandes, les produits les plus vendus et des informations sur les clients.

5. Pensez à ajouter un point de vente pour les ventes en magasin
Vendez aussi en personne ? La fonctionnalité de point de vente de Spwig synchronise les transactions en magasin avec votre inventaire en ligne.

Explorer votre tableau de bord : {{ admin_url }}

Besoin d'aide ? Contactez {{ support_email }}