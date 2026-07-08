---
template_type: translation_job_completed
category: Translation Service
---

# Email Template: translation_job_completed

## Subject
✓ Traduction terminée : {{ content_type }} ({{ language_count }} langues)

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#dcfce7">
      <mj-column>
        <mj-text font-size="24px" font-weight="bold" color="#065f46" align="center">
          ✓ Traduction terminée !
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Vos traductions sont prêtes
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Grande nouvelle ! Votre travail de traduction en masse a été terminé avec succès.
        </mj-text>

        <mj-spacer height="30px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
              Résumé du travail:
            </mj-text>
            <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>Job ID:</strong> {{ job_id }}<br/>
              <strong>Type de contenu:</strong> {{ content_type }}<br/>
              <strong>Langues:</strong> {{ target_languages }}<br/>
              <strong>Items traduits:</strong> {{ items_translated }}<br/>
              <strong>Mots totaux:</strong> {{ word_count }}<br/>
              <strong>Terminé:</strong> {{ completed_at }}<br/>
              <strong>Durée:</strong> {{ job_duration }}
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Qualité des traductions:
        </mj-text>

        <mj-section background-color="#f0fdf4" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="15px" color="#065f46">
              <strong>Score de qualité moyen:</strong> {{ quality_score }}%<br/>
              <strong>Haute qualité:</strong> {{ high_quality_count }} éléments<br/>
              <strong>Revue recommandée:</strong> {{ review_needed_count }} éléments
            </mj-text>
          </mj-column>
        </mj-section>

        {% if review_needed_count > 0 %}
        <mj-spacer height="20px" />
        <mj-section background-color="#fef3c7" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="14px" color="#92400e" font-weight="bold">
              ⚠️ Revue recommandée
            </mj-text>
            <mj-text font-size="14px" color="#92400e" line-height="1.6">
              {{ review_needed_count }} traductions ont un score inférieur à 85 % et devraient être revues avant la publication.
            </mj-text>
          </mj-column>
        </mj-section>
        {% endif %}

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Étapes suivantes:
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}" line-height="1.8">
          1. Réviser les traductions dans votre tableau de bord administrateur<br/>
          2. Modifier les traductions nécessitant des ajustements<br/>
          3. Publier les traductions pour les rendre actives<br/>
          4. Votre contenu multilingue sera disponible pour les clients
        </mj-text>

        <mj-spacer height="30px" />

        <mj-button href="{{ review_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          Réviser les traductions
        </mj-button>

        {% if can_publish_all %}
        <mj-spacer height="10px" />
        <mj-button href="{{ publish_all_url }}" background-color="#059669" color="#ffffff" font-size="14px" border-radius="6px" padding="10px 25px">
          Publier toutes
        </mj-button>
        {% endif %}
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
✓ TRADUCTION TERMINÉE !

Vos traductions sont prêtes

Grande nouvelle ! Votre travail de traduction en masse a été terminé avec succès.

RÉSUMÉ DU TRAVAIL:
- ID du travail: {{ job_id }}
- Type de contenu: {{ content_type }}
- Langues: {{ target_languages }}
- Items traduits: {{ items_translated }}
- Mots totaux: {{ word_count }}
- Terminé: {{ completed_at }}
- Durée: {{ job_duration }}

QUALITÉ DES TRADUCTIONS:
- Score de qualité moyen: {{ quality_score }}%
- Haute qualité: {{ high_quality_count }} items
- Revue recommandée: {{ review_needed_count }} items

{% if review_needed_count > 0 %}
⚠️ RECOMMANDATION DE REVISION:
{{ review_needed_count }} traductions ont un score inférieur à 85% et devraient être revues avant la publication.
{% endif %}

ÉTAPES SUIVANTES:
1. Réviser les traductions dans votre tableau de bord administrateur
2. Modifier les traductions nécessitant des ajustements
3. Publier les traductions pour les rendre actives
4. Votre contenu multilingue sera disponible pour les clients

Réviser les traductions: {{ review_url }}
{% if can_publish_all %}Publier toutes: {{ publish_all_url }}{% endif %}