---
template_type: license_trial_welcome
category: License
---

# Email Template: license_trial_welcome

## Subject
Bienvenue sur Spwig - Votre essai gratuit de {{ trial_days }} jours

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
    <mj-section background-color="#059669" padding="30px 20px">
      <mj-column>
        <mj-text font-size="28px" font-weight="bold" color="#ffffff" align="center">
          Bienvenue sur Spwig !
        </mj-text>
        <mj-text font-size="16px" color="#ffffffcc" align="center" padding-top="10px">
          Votre essai gratuit de {{ trial_days }} jours est prêt
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
          Merci d'avoir essayé <strong>{{ product_name }}</strong> ! Votre essai a été activé et vous avez <strong>{{ trial_days }} jours</strong> pour explorer tout ce que Spwig a à offrir{% if includes_pos %}, y compris notre système de Point de Vente{% endif %}.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Setup Token Box -->
    <mj-section background-color="#f0fdf4" padding="25px" border-radius="8px">
      <mj-column>
        <mj-text font-size="12px" color="#065f46" font-weight="bold" align="center">
          VOTRE TOKEN D'INSTALLATION
        </mj-text>
        <mj-text font-size="14px" font-weight="bold" color="#059669" align="center" font-family="'Courier New', monospace" padding="10px 0" word-break="break-all">
          {{ setup_token }}
        </mj-text>
        <mj-text font-size="12px" color="{{ theme.color.text_muted|default:'#6b7280' }}" align="center">
          Utilisez ce token lors de l'installation pour activer votre boutique d'essai
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Getting Started -->
    <mj-section>
      <mj-column>
        <mj-text font-size="16px" font-weight="bold" padding-bottom="10px">
          Getting Started
        </mj-text>
        <mj-text font-size="14px">
          1. Suivez notre guide d'installation pour installer Spwig sur votre serveur
        </mj-text>
        <mj-text font-size="14px">
          2. Entrez votre token d'installation lorsqu'il vous sera demandé pendant l'installation
        </mj-text>
        <mj-text font-size="14px">
          3. Commencez à construire votre boutique en ligne !
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Setup Guide CTA -->
    {% include 'email_system/mjml_components/cta_button.mjml' with url=setup_url text="View Setup Guide" %}

    <!-- What's Included -->
    <mj-section background-color="{{ theme.color.background_secondary|default:'#f9fafb' }}" padding="20px" border-radius="8px">
      <mj-column>
        <mj-text font-size="16px" font-weight="bold" padding-bottom="10px">
          What's Included in Your Trial
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          Full access to all core features for {{ trial_days }} days
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          Product catalog, orders, and customer management
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          Theme customization and page builder
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          Payment and shipping provider integrations
        </mj-text>
        {% if includes_pos %}
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          Point of Sale (POS) system
        </mj-text>
        {% endif %}
      </mj-column>
    </mj-section>

    <!-- Trial Info -->
    <mj-section>
      <mj-column>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          Votre essai expirera dans {{ trial_days }} jours. Lorsque vous serez prêt, mettez à niveau vers une licence complète pour continuer à faire fonctionner votre boutique sans perte de données.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Support -->
    {% include 'email_system/mjml_components/support_block.mjml' %}
  </mj-body>
</mjml>

## Text Content
Bienvenue sur Spwig !
Votre essai gratuit de {{ trial_days }} jours est prêt.

Bonjour {{ customer_name }},

Merci d'avoir essayé {{ product_name }} ! Votre essai a été activé et vous avez {{ trial_days }} jours pour explorer tout ce que Spwig a à offrir{% if includes_pos %}, y compris notre système de Point de Vente{% endif %}.

VOTRE TOKEN D'INSTALLATION:
{{ setup_token }}
Utilisez ce token lors de l'installation pour activer votre boutique d'essai.

Getting Started:
1. Suivez notre guide d'installation pour installer Spwig sur votre serveur
2. Entrez votre token d'installation lorsqu'il vous sera demandé pendant l'installation
3. Commencez à construire votre boutique en ligne !

View Setup Guide: {{ setup_url }}

What's Included in Your Trial:
- Full access to all core features for {{ trial_days }} days
- Product catalog, orders, and customer management
- Theme customization and page builder
- Payment and shipping provider integrations
{% if includes_pos %}- Point of Sale (POS) system{% endif %}

Votre essai expirera dans {{ trial_days }} jours. Lorsque vous serez prêt, mettez à niveau vers une licence complète pour continuer à faire fonctionner votre boutique sans perte de données.

Need help? Contact {{ support_email }}