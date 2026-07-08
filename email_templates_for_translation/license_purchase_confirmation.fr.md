---
template_type: license_purchase_confirmation
category: License
---

# Email Template: license_purchase_confirmation

## Subject
Votre licence Spwig - Commande n°{{ order_number }}

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
          Merci pour votre achat !
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
          Votre achat de <strong>{{ product_name }}</strong> est terminé. Vous trouverez ci-dessous votre clé de licence et votre jeton d'installation pour commencer.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Order Summary -->
    <mj-section background-color="{{ theme.color.background_secondary|default:'#f9fafb' }}" padding="20px" border-radius="8px">
      <mj-column>
        <mj-text font-size="16px" font-weight="bold" padding-bottom="10px">
          Résumé de la commande
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          Produit : {{ product_name }}{% if includes_pos %} (inclut le POS){% endif %}
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          Montant : {{ price }}
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          Numéro de commande : {{ order_number }}
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- License Key Box -->
    <mj-section background-color="#eff6ff" padding="25px" border-radius="8px">
      <mj-column>
        <mj-text font-size="12px" color="#1e40af" font-weight="bold" align="center">
          VOTRE CLÉ DE LICENCE
        </mj-text>
        <mj-text font-size="18px" font-weight="bold" color="{{ theme.color.primary|default:'#2563eb' }}" align="center" font-family="'Courier New', monospace" padding="10px 0">
          {{ license_key }}
        </mj-text>
        <mj-text font-size="12px" color="{{ theme.color.text_muted|default:'#6b7280' }}" align="center">
          Enregistrez cette clé - vous en aurez besoin pour une réinstallation
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Setup Token Box -->
    <mj-section background-color="#f0fdf4" padding="25px" border-radius="8px">
      <mj-column>
        <mj-text font-size="12px" color="#065f46" font-weight="bold" align="center">
          VOTRE JETON D'INSTALLATION
        </mj-text>
        <mj-text font-size="14px" font-weight="bold" color="#059669" align="center" font-family="'Courier New', monospace" padding="10px 0" word-break="break-all">
          {{ setup_token }}
        </mj-text>
        <mj-text font-size="12px" color="{{ theme.color.text_muted|default:'#6b7280' }}" align="center">
          Utilisez ce jeton lors de l'installation pour activer votre boutique
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Getting Started -->
    <mj-section>
      <mj-column>
        <mj-text font-size="16px" font-weight="bold" padding-bottom="10px">
          Démarrage
        </mj-text>
        <mj-text font-size="14px">
          1. Suivez notre guide d'installation pour installer Spwig sur votre serveur
        </mj-text>
        <mj-text font-size="14px">
          2. Entrez votre jeton d'installation lorsqu'il vous sera demandé pendant l'installation
        </mj-text>
        <mj-text font-size="14px">
          3. Votre boutique sera activée automatiquement
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Setup Guide CTA -->
    {% include 'email_system/mjml_components/cta_button.mjml' with url=setup_url text="View Setup Guide" %}

    {% if activation_url %}
    <!-- Guest Account Activation -->
    <mj-section background-color="{{ theme.color.background|default:'#ffffff' }}" padding="20px 20px 10px">
      <mj-column>
        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}" align="center">
          Créez votre compte
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}" align="center" padding-top="5px">
          Définissez un mot de passe pour gérer vos licences, accéder aux téléchargements et recevoir les mises à jour.
        </mj-text>
      </mj-column>
    </mj-section>
    {% include 'email_system/mjml_components/cta_button.mjml' with url=activation_url text="Create Your Account" %}
    {% endif %}

    <!-- Important Notice -->
    <mj-section>
      <mj-column>
        <mj-text font-size="14px" color="{{ theme.color.warning|default:'#d97706' }}" font-weight="bold">
          Important :
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          Conservez ce courriel en sécurité - il contient votre clé de licence et votre jeton d'installation pour référence future. Ne partagez pas ces identifiants avec d'autres personnes.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Support -->
    {% include 'email_system/mjml_components/support_block.mjml' %}
  </mj-body>
</mjml>

## Text Content
Merci pour votre achat !

Commande n°{{ order_number }}

Bonjour {{ customer_name }},

Votre achat de {{ product_name }} est terminé. Vous trouverez ci-dessous votre clé de licence et votre jeton d'installation pour commencer.

Résumé de la commande:
- Produit : {{ product_name }}{% if includes_pos %} (inclut le POS){% endif %}
- Montant : {{ price }}
- Numéro de commande : {{ order_number }}

VOTRE CLÉ DE LICENCE:
{{ license_key }}
Enregistrez cette clé - vous en aurez besoin pour une réinstallation.

VOTRE JETON D'INSTALLATION:
{{ setup_token }}
Utilisez ce jeton lors de l'installation pour activer votre boutique.

Démarrage:
1. Suivez notre guide d'installation pour installer Spwig sur votre serveur
2. Entrez votre jeton d'installation lorsqu'il vous sera demandé pendant l'installation
3. Votre boutique sera activée automatiquement

Voir le guide d'installation: {{ setup_url }}
{% if activation_url %}
Créez votre compte:
Définissez un mot de passe pour gérer vos licences, accéder aux téléchargements et recevoir les mises à jour.
{{ activation_url }}
{% endif %}
IMPORTANT:
Conservez ce courriel en sécurité - il contient votre clé de licence et votre jeton d'installation pour référence future. Ne partagez pas ces identifiants avec d'autres personnes.

Besoin d'aide ? Contactez {{ support_email }}