---
template_type: component_deprecated_warning
category: Component Updates
---

# Email Template: component_deprecated_warning

## Subject
⚠️ {{ component_name }} sera déprécié le {{ deprecation_date }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#fef3c7">
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="#92400e" align="center">
          ⚠️ Avertissement de dépréciation
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="18px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Ce composant sera déprécié
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          {{ component_name }} sera déprécié et ne sera plus recommandé à l'utilisation. Veuillez planifier la migration vers une solution alternative.
        </mj-text>

        <mj-spacer height="30px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
              Échéance de la dépréciation :
            </mj-text>
            <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>Composant :</strong> {{ component_name }}<br/>
              <strong>Version actuelle :</strong> {{ current_version }}<br/>
              <strong>Date de dépréciation :</strong> {{ deprecation_date }}<br/>
              <strong>Fin de support :</strong> {{ end_of_support_date }}
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Raison de la dépréciation :
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}" line-height="1.8">
          {{ deprecation_reason }}
        </mj-text>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Cela signifie :
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}" line-height="1.8">
          • Le composant fonctionnera encore jusqu'à {{ end_of_support_date }}<br/>
          • Aucune nouvelle fonctionnalité ne sera ajoutée<br/>
          • Les mises à jour de sécurité seront fournies jusqu'à la fin du support<br/>
          • Après {{ end_of_support_date }}, le composant ne recevra plus de mises à jour
        </mj-text>

        {% if recommended_alternative %}
        <mj-spacer height="30px" />
        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Alternative recommandée :
        </mj-text>
        <mj-section background-color="#f0fdf4" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="15px" color="#065f46" font-weight="bold">
              {{ alternative_name }}
            </mj-text>
            <mj-text font-size="14px" color="#065f46" line-height="1.6">
              {{ alternative_description }}
            </mj-text>
          </mj-column>
        </mj-section>
        {% endif %}

        {% if migration_guide %}
        <mj-spacer height="20px" />
        <mj-text font-size="14px" color="{{ theme.color.text_secondary|default:'#6b7280' }}" align="center">
          <a href="{{ migration_guide }}" style="color: {{ theme.color.primary|default:'#2563eb' }};">Voir le guide de migration</a>
        </mj-text>
        {% endif %}

        <mj-spacer height="30px" />

        {% if alternative_url %}
        <mj-button href="{{ alternative_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          Voir l'alternative
        </mj-button>
        <mj-spacer height="10px" />
        {% endif %}

        <mj-button href="{{ support_url }}" background-color="#6b7280" color="#ffffff" font-size="14px" border-radius="6px" padding="10px 25px">
          Contacter le support
        </mj-button>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
⚠️ AVERTISSEMENT DE DÉPRÉCIATION

Ce composant sera déprécié

{{ component_name }} sera déprécié et ne sera plus recommandé à l'utilisation. Veuillez planifier la migration vers une solution alternative.

Échéance de la dépréciation :
- Composant : {{ component_name }}
- Version actuelle : {{ current_version }}
- Date de dépréciation : {{ deprecation_date }}
- Fin de support : {{ end_of_support_date }}

RAISON DE LA DÉPRÉCIATION :
{{ deprecation_reason }}

CE QUE ÇA SIGNIFIE :
• Le composant fonctionnera encore jusqu'à {{ end_of_support_date }}
• Aucune nouvelle fonctionnalité ne sera ajoutée
• Les mises à jour de sécurité seront fournies jusqu'à la fin du support
• Après {{ end_of_support_date }}, le composant ne recevra plus de mises à jour

{% if recommended_alternative %}ALTERNATIVE RECOMMANDÉE :
{{ alternative_name }}
{{ alternative_description }}
{% endif %}

{% if migration_guide %}Voir le guide de migration : {{ migration_guide }}{% endif %}
{% if alternative_url %}Voir l'alternative : {{ alternative_url }}{% endif %}
Contacter le support : {{ support_url }}