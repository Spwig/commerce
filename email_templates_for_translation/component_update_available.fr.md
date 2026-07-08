---
template_type: component_update_available
category: Component Updates
---

# Email Template: component_update_available

## Subject
Mise à jour disponible : {{ component_name }} v{{ new_version }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#eff6ff">
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="#1e40af" align="center">
          📦 Mise à jour disponible
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="18px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Nouvelle version disponible
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}">
          Une nouvelle version de {{ component_name }} est disponible pour votre boutique Spwig.
        </mj-text>

        <mj-spacer height="20px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
              Détails de la mise à jour :
            </mj-text>
            <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>Composant :</strong> {{ component_name }}<br/>
              <strong>Version actuelle :</strong> {{ current_version }}<br/>
              <strong>Nouvelle version :</strong> {{ new_version }}<br/>
              <strong>Date de publication :</strong> {{ release_date }}
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Qu'est-ce de neuf :
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}" line-height="1.8">
          {{ changelog }}
        </mj-text>

        {% if breaking_changes %}
        <mj-spacer height="20px" />
        <mj-section background-color="#fef3c7" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="14px" color="#92400e" font-weight="bold">
              ⚠️ Changements rupture
            </mj-text>
            <mj-text font-size="14px" color="#92400e" line-height="1.6">
              {{ breaking_changes }}
            </mj-text>
          </mj-column>
        </mj-section>
        {% endif %}

        <mj-spacer height="30px" />

        <mj-button href="{{ update_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          Installer la mise à jour
        </mj-button>

        <mj-spacer height="20px" />

        <mj-text font-size="14px" color="{{ theme.color.text_secondary|default:'#6b7280' }}" align="center">
          <a href="{{ changelog_url }}" style="color: {{ theme.color.primary|default:'#2563eb' }};">
            Voir le journal des modifications complet
          </a>
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
📦 MISE À JOUR DISPO

Nouvelle version disponible

Une nouvelle version de {{ component_name }} est disponible pour votre boutique Spwig.

DÉTAILS DE LA MISE À JOUR : 
- Composant : {{ component_name }}
- Version actuelle : {{ current_version }}
- Nouvelle version : {{ new_version }}
- Date de publication : {{ release_date }}

QU'EST-CE DE NEUF : 
{{ changelog }}

{% if breaking_changes %}
⚠️ CHANGEMENTS DE RUPTURE : 
{{ breaking_changes }}
{% endif %}

Installer la mise à jour : {{ update_url }}
Voir le journal des modifications complet : {{ changelog_url }}