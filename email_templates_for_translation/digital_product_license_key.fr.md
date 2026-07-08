---
template_type: digital_product_license_key
category: Digital Products
---

# Email Template: digital_product_license_key

## Subject
Votre clé de licence logicielle - Commande n°{{ order_number }}

## HTML Content
<mjml>
  <mj-head>
    <mj-attributes>
      <mj-all font-family="'Helvetica Neue', Helvetica, Arial, sans-serif" />
      <mj-text font-size="14px" color="#333333" line-height="20px" />
      <mj-section background-color="{{ theme.color.background|default:'#ffffff' }}" padding="20px" />
    </mj-attributes>
  </mj-head>
  <mj-body background-color="{{ theme.color.background_secondaryondary|default:'#f9fafb' }}">
    <!-- Header -->
    <mj-section background-color="#059669" padding="20px">
      <mj-column>
        <mj-text font-size="24px" font-weight="bold" color="{{ theme.color.background|default:'#ffffff' }}" align="center">
          Votre clé de licence est prête
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Main Content -->
    <mj-section>
      <mj-column>
        <mj-text font-size="16px">
          Bonjour {{ customer_name }},
        </mj-text>
        <mj-text>
          Merci pour votre achat de {{ product_name }} ! Voici votre clé de licence pour l'activation.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- License Key Box -->
    <mj-section background-color="#f0fdf4" padding="30px" border="2px solid #059669" border-radius="8px">
      <mj-column>
        <mj-text font-size="12px" color="#065f46" font-weight="bold" align="center">
          VOTRE CLÉ DE LICENCE
        </mj-text>
        <mj-text font-size="20px" font-weight="bold" color="#059669" align="center" font-family="'Courier New', monospace" padding="10px 0">
          {{ license_key }}
        </mj-text>
        <mj-text font-size="12px" color="{{ theme.color.text_muted|default:'#6b7280' }}" align="center">
          Cliquez pour copier ou notez-la soigneusement
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- License Details -->
    <mj-section>
      <mj-column>
        <mj-text font-size="14px" font-weight="bold">
          Détails de la licence:
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          • Produit: {{ product_name }}
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          • Version: {{ product_version }}
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          • Type de licence: {{ license_type }}
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          • Max d'activations: {{ max_activations }} appareil(s)
        </mj-text>
        {% if is_lifetime %}
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          • Validité: Licence à vie
        </mj-text>
        {% else %}
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          • Valide jusqu'au: {{ expiration_date }}
        </mj-text>
        {% endif %}
      </mj-column>
    </mj-section>

    <!-- Activation Instructions -->
    <mj-section background-color="{{ theme.color.background_secondaryondary|default:'#f9fafb' }}" padding="20px" border-radius="8px">
      <mj-column>
        <mj-text font-size="16px" font-weight="bold">
          Comment activer:
        </mj-text>
        <mj-text font-size="14px">
          1. Téléchargez et installez le logiciel
        </mj-text>
        <mj-text font-size="14px">
          2. Ouvrez l'application
        </mj-text>
        <mj-text font-size="14px">
          3. Entrez votre clé de licence lorsqu'on vous le demandera
        </mj-text>
        <mj-text font-size="14px">
          4. Cliquez sur "Activer" pour terminer le processus
        </mj-text>
      </mj-column>
    </mj-section>

    {% if download_url %}
    <!-- Download Button -->
    <mj-section>
      <mj-column>
        <mj-button href="{{ download_url }}" background-color="#059669" color="{{ theme.color.background|default:'#ffffff' }}" font-size="16px" padding="15px 30px" border-radius="6px">
          Télécharger le logiciel
        </mj-button>
      </mj-column>
    </mj-section>
    {% endif %}

    <!-- Important Notice -->
    <mj-section>
      <mj-column>
        <mj-text font-size="14px" color="{{ theme.color.error|default:'#ef4444' }}" font-weight="bold">
          ⚠️ Important:
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          • Gardez cet e-mail en sécurité - vous en aurez besoin pour le réinstallation
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          • Ne partagez pas votre clé de licence avec d'autres personnes
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          • Vous pouvez désactiver les appareils depuis votre tableau de bord de compte
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Support -->
    <mj-section>
      <mj-column>
        <mj-divider border-color="{{ theme.color.border|default:'#e5e7eb' }}" />
        <mj-text font-size="12px" color="#9ca3af" align="center">
          Besoin d'aide pour l'activation ? Contactez {{ support_email }}
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
Votre clé de licence est prête

Bonjour {{ customer_name }},

Merci pour votre achat de {{ product_name }} ! Voici votre clé de licence pour l'activation.

VOTRE CLÉ DE LICENCE:
{{ license_key }}

Détails de la licence:
• Produit: {{ product_name }}
• Version: {{ product_version }}
• Type de licence: {{ license_type }}
• Max d'activations: {{ max_activations }} appareil(s)
{% if is_lifetime %}• Validité: Licence à vie{% else %}• Valide jusqu'au: {{ expiration_date }}{% endif %}

Comment activer:
1. Téléchargez et installez le logiciel
2. Ouvrez l'application
3. Entrez votre clé de licence lorsqu'on vous le demandera
4. Cliquez sur "Activer" pour terminer le processus

{% if download_url %}Télécharger le logiciel: {{ download_url }}

{% endif %}IMPORTANT:
• Gardez cet e-mail en sécurité - vous en aurez besoin pour le réinstallation
• Ne partagez pas votre clé de licence avec d'autres personnes
• Vous pouvez désactiver les appareils depuis votre tableau de bord de compte

Besoin d'aide pour l'activation ? Contactez {{ support_email }}