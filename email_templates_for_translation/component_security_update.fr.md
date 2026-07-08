---
template_type: component_security_update
category: Component Updates
---

# Email Template: component_security_update

## Subject
🔒 URGENT : Mise à jour de sécurité disponible pour {{ component_name }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#fee2e2">
      <mj-column>
        <mj-text font-size="22px" font-weight="bold" color="#991b1b" align="center">
          🔒 MISE À JOUR DE SÉCURITÉ REQUISE
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="18px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Mise à jour de sécurité critique
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Une vulnérabilité de sécurité a été découverte dans {{ component_name }}. Veuillez mettre à jour immédiatement pour protéger votre magasin.
        </mj-text>

        <mj-spacer height="30px" />

        <mj-section background-color="#fee2e2" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="#991b1b" font-size="16px">
              ⚠️ Informations de sécurité
            </mj-text>
            <mj-text color="#991b1b">
              <strong>Composant :</strong> {{ component_name }}<br/>
              <strong>Version actuelle :</strong> {{ current_version }}<br/>
              <strong>Version corrigée :</strong> {{ patched_version }}<br/>
              <strong>Gravité :</strong> {{ severity_level }}<br/>
              <strong>ID CVE :</strong> {{ cve_id }}
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Détails de la vulnérabilité :
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}" line-height="1.8">
          {{ vulnerability_description }}
        </mj-text>

        <mj-spacer height="20px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Impact potentiel :
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}" line-height="1.8">
          {{ impact_description }}
        </mj-text>

        {% if mitigation_steps %}
        <mj-spacer height="30px" />
        <mj-section background-color="#fef3c7" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="14px" color="#92400e" font-weight="bold">
              Mitigation temporaire
            </mj-text>
            <mj-text font-size="14px" color="#92400e" line-height="1.6">
              {{ mitigation_steps }}
            </mj-text>
          </mj-column>
        </mj-section>
        {% endif %}

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}" align="center">
          Action requise : Installer la mise à jour immédiatement
        </mj-text>

        <mj-spacer height="20px" />

        <mj-button href="{{ update_url }}" background-color="#dc2626" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          Installer la mise à jour de sécurité
        </mj-button>

        <mj-spacer height="10px" />

        <mj-button href="{{ advisory_url }}" background-color="#6b7280" color="#ffffff" font-size="14px" border-radius="6px" padding="10px 25px">
          Lire l'avis de sécurité
        </mj-button>

        <mj-spacer height="30px" />

        <mj-text font-size="13px" color="{{ theme.color.text_secondary|default:'#6b7280' }}" align="center">
          Si vous avez besoin d'aide, contactez immédiatement le support Spwig.
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
🔒 MISE À JOUR DE SÉCURITÉ REQUISE

Mise à jour de sécurité critique

Une vulnérabilité de sécurité a été découverte dans {{ component_name }}. Veuillez mettre à jour immédiatement pour protéger votre magasin.

⚠️ INFORMATIONS DE SÉCURITÉ :
- Composant : {{ component_name }}
- Version actuelle : {{ current_version }}
- Version corrigée : {{ patched_version }}
- Gravité : {{ severity_level }}
- ID CVE : {{ cve_id }}

DÉTAILS DE LA VULNÉRABILITÉ :
{{ vulnerability_description }}

IMPACT POTENTIEL :
{{ impact_description }}

{% if mitigation_steps %}
MITIGATION TEMPORAIRE :
{{ mitigation_steps }}
{% endif %}

ACTION REQUISE : INSTALLER LA MISE À JOUR IMMÉDIATEMENT

Installer la mise à jour de sécurité : {{ update_url }}
Lire l'avis de sécurité : {{ advisory_url }}

Si vous avez besoin d'aide, contactez immédiatement le support Spwig.