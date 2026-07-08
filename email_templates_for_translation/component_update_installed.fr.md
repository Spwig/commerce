---
template_type: component_update_installed
category: Component Updates
---

# Email Template: component_update_installed

## Subject
✓ {{ component_name }} mis à jour vers la v{{ new_version }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#dcfce7">
      <mj-column>
        <mj-text font-size="24px" font-weight="bold" color="#065f46" align="center">
          ✓ Mise à jour installée
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Mise à jour réussie
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          {{ component_name }} a été mis à jour avec succès vers la version {{ new_version }}.
        </mj-text>

        <mj-spacer height="30px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
              Détails d'installation:
            </mj-text>
            <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>Component:</strong> {{ component_name }}<br/>
              <strong>Previous Version:</strong> {{ old_version }}<br/>
              <strong>New Version:</strong> {{ new_version }}<br/>
              <strong>Installed:</strong> {{ installed_at }}<br/>
              <strong>Duration:</strong> {{ installation_duration }}
            </mj-text>
          </mj-column>
        </mj-section>

        {% if post_install_message %}
        <mj-spacer height="30px" />
        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Informations importantes:
        </mj-text>
        <mj-section background-color="#f0fdf4" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="14px" color="#065f46" line-height="1.6">
              {{ post_install_message }}
            </mj-text>
          </mj-column>
        </mj-section>
        {% endif %}

        {% if requires_configuration %}
        <mj-spacer height="20px" />
        <mj-section background-color="#fef3c7" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="14px" color="#92400e" font-weight="bold">
              ⚙️ Configuration requise
            </mj-text>
            <mj-text font-size="14px" color="#92400e" line-height="1.6">
              {{ configuration_message }}
            </mj-text>
          </mj-column>
        </mj-section>
        {% endif %}

        <mj-spacer height="30px" />

        {% if configuration_url %}
        <mj-button href="{{ configuration_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          Configurer le composant
        </mj-button>
        <mj-spacer height="10px" />
        {% endif %}

        <mj-button href="{{ component_url }}" background-color="#6b7280" color="#ffffff" font-size="14px" border-radius="6px" padding="10px 25px">
          Voir les détails du composant
        </mj-button>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
✓ MISE À JOUR INSTALLÉE

Mise à jour réussie

{{ component_name }} a été mis à jour avec succès vers la version {{ new_version }}.

DÉTAILS D'INSTALLATION:
- Composant: {{ component_name }}
- Version précédente: {{ old_version }}
- Nouvelle version: {{ new_version }}
- Installé le: {{ installed_at }}
- Durée: {{ installation_duration }}

{% if post_install_message %}
INFORMATIONS IMPORTANTES:
{{ post_install_message }}
{% endif %}

{% if requires_configuration %}
⚙️ CONFIGURATION REQUISE:
{{ configuration_message }}
{% endif %}

{% if configuration_url %}Configurer le composant: {{ configuration_url }}{% endif %}
Voir les détails du composant: {{ component_url }}