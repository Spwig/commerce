---
template_type: hosted_terminated
category: License
---

# Email Template: hosted_terminated

## Subject
Magasin Supprimé - {{ store_name }}

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
    <mj-section background-color="#374151" padding="30px 20px">
      <mj-column>
        <mj-text font-size="28px" font-weight="bold" color="#ffffff" align="center">
          Magasin Supprimé
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
          Votre magasin <strong>{{ store_name }}</strong> a été définitivement supprimé.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Data Backup Info -->
    <mj-section background-color="{{ theme.color.background_secondary|default:'#f9fafb' }}" padding="20px" border-radius="8px">
      <mj-column>
        <mj-text font-size="16px" font-weight="bold" padding-bottom="10px">
          Sauvegarde des Données
        </mj-text>
        <mj-text font-size="14px">
          Une sauvegarde de vos données sera disponible pendant 90 jours sur demande. Contactez <strong>support@spwig.com</strong> si vous avez besoin d'une exportation des données.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Thank You -->
    <mj-section>
      <mj-column>
        <mj-text>
          Merci d'être un client Spwig. Nous espérons vous revoir à l'avenir.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Support -->
    {% include 'email_system/mjml_components/support_block.mjml' %}
  </mj-body>
</mjml>

## Text Content
Magasin Supprimé - {{ store_name }}

Bonjour {{ name|default:'there' }},

Votre magasin {{ store_name }} a été définitivement supprimé.

Sauvegarde des Données:
Une sauvegarde de vos données sera disponible pendant 90 jours sur demande. Contactez support@spwig.com si vous avez besoin d'une exportation des données.

Merci d'être un client Spwig. Nous espérons vous revoir à l'avenir.

Besoin d'aide ? Contactez {{ support_email }}