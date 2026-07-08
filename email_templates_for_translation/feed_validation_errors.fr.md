---
template_type: feed_validation_errors
category: Product Feeds
---

# Email Template: feed_validation_errors

## Subject
⚠️ {{ feed_name }} : {{ error_count }} erreurs de validation trouvées

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#fef3c7">
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="#92400e" align="center">
          ⚠️ Erreurs de validation du flux
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="18px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Problèmes de qualité des données détectés
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}">
          {{ error_count }} erreur de validation{{ error_count|pluralize }} trouvée dans {{ feed_name }}. Ces problèmes peuvent empêcher les produits d'apparaître sur {{ platform_name }}.
        </mj-text>

        <mj-spacer height="20px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
              Résumé de validation :
            </mj-text>
            <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>Flux :</strong> {{ feed_name }}<br/>
              <strong>Plateforme :</strong> {{ platform_name }}<br/>
              <strong>Validé le :</strong> {{ validated_at }}<br/>
              <strong>Total des produits :</strong> {{ total_products }}<br/>
              <strong>Produits avec erreurs :</strong> {{ affected_products }}
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Principales erreurs :
        </mj-text>

        {% for error in top_errors %}
        <mj-section background-color="#fee2e2" border-radius="8px" padding="12px">
          <mj-column>
            <mj-text font-size="14px" color="#991b1b" font-weight="bold">
              {{ error.type }}
            </mj-text>
            <mj-text font-size="13px" color="#991b1b">
              {{ error.count }} produit{{ error.count|pluralize }} affecté(s) : {{ error.message }}
            </mj-text>
          </mj-column>
        </mj-section>
        <mj-spacer height="8px" />
        {% endfor %}

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Qu'est-ce qui doit être corrigé ?
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}" line-height="1.8">
          {{ fix_instructions }}
        </mj-text>

        <mj-spacer height="30px" />

        <mj-button href="{{ errors_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          Voir toutes les erreurs
        </mj-button>

        <mj-spacer height="10px" />

        <mj-button href="{{ admin_feed_url }}" background-color="#6b7280" color="#ffffff" font-size="14px" border-radius="6px" padding="10px 25px">
          Gérer le flux
        </mj-button>

        <mj-spacer height="20px" />

        <mj-text font-size="13px" color="{{ theme.color.text_secondary|default:'#6b7280' }}" align="center">
          Corrigez ces erreurs pour assurer l'apparition de tous les produits sur {{ platform_name }}.
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
⚠️ ERREURS DE VALIDATION DU FLUX

Problèmes de qualité des données détectés

{{ error_count }} erreur de validation{{ error_count|pluralize }} trouvée dans {{ feed_name }}. Ces problèmes peuvent empêcher les produits d'apparaître sur {{ platform_name }}.

RÉSUMÉ DE VALIDATION:
- Flux: {{ feed_name }}
- Plateforme: {{ platform_name }}
- Validé: {{ validated_at }}
- Total des produits: {{ total_products }}
- Produits avec erreurs: {{ affected_products }}

PRINCIPALES ERREURS:
{% for error in top_errors %}
{{ error.type }}: {{ error.count }} produit{{ error.count|pluralize }} - {{ error.message }}
{% endfor %}

QU'EST-CE QUI DOIT ÊTRE CORRIGÉ:
{{ fix_instructions }}

Voir toutes les erreurs: {{ errors_url }}
Gérer le flux: {{ admin_feed_url }}

Corrigez ces erreurs pour assurer l'apparition de tous les produits sur {{ platform_name }}.