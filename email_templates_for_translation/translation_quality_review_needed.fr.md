---
template_type: translation_quality_review_needed
category: Translation Service
---

# Email Template: translation_quality_review_needed

## Subject
⚠️ Mauvaise qualité des traductions détectées : {{ content_type }} - {{ low_quality_count }} éléments nécessitent un examen

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#fef3c7">
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="#92400e" align="center">
          ⚠️ Avertissement de qualité des traductions
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="18px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Examen recommandé
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}">
          Votre tâche de traduction est terminée, mais {{ low_quality_count }} traductions ont obtenu un score inférieur au seuil de qualité et devraient être examinées avant la publication.
        </mj-text>

        <mj-spacer height="20px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
              Résumé de la tâche : 
            </mj-text>
            <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>Job ID:</strong> {{ job_id }}<br/>
              <strong>Type de contenu:</strong> {{ content_type }}<br/>
              <strong>Total d'éléments:</strong> {{ total_items }}<br/>
              <strong>Qualité moyenne:</strong> {{ average_quality }}%<br/>
              <strong>Qualité faible:</strong> {{ low_quality_count }} éléments ({{ low_quality_percentage }}%)
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Détail des scores de qualité : 
        </mj-text>

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="14px" color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>Excellent (95-100%):</strong> {{ excellent_count }} éléments<br/>
              <strong>Bon (85-94%):</strong> {{ good_count }} éléments<br/>
              <strong>Acceptable (70-84%):</strong> {{ fair_count }} éléments<br/>
              <strong>Mauvais (<70%):</strong> <span style="color: #dc2626; font-weight: bold;">{{ poor_count }} éléments</span>
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Problèmes de qualité courants : 
        </mj-text>

        {% for issue in quality_issues %}
        <mj-section background-color="#fef3c7" border-radius="8px" padding="12px">
          <mj-column>
            <mj-text font-size="14px" color="#92400e">
              <strong>{{ issue.type }}:</strong> {{ issue.count }} occurrences
            </mj-text>
          </mj-column>
        </mj-section>
        <mj-spacer height="8px" />
        {% endfor %}

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Actions recommandées : 
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}" line-height="1.8">
          1. Vérifier les traductions signalées via le panneau d'administration<br/>
          2. Modifier manuellement les traductions de faible qualité<br/>
          3. Réfléchir à la re-traduction des éléments de faible qualité<br/>
          4. Publier uniquement après la vérification complète
        </mj-text>

        <mj-spacer height="30px" />

        <mj-button href="{{ review_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          Vérifier les traductions
        </mj-button>

        <mj-spacer height="10px" />

        <mj-button href="{{ low_quality_url }}" background-color="#dc2626" color="#ffffff" font-size="14px" border-radius="6px" padding="10px 25px">
          Voir les éléments de faible qualité
        </mj-button>

        <mj-spacer height="30px" />

        <mj-section background-color="#eff6ff" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="14px" color="#1e40af" line-height="1.6">
              💡 Conseil : Les scores de qualité inférieurs à 85 % indiquent des problèmes potentiels liés à la grammaire, au contexte ou à la précision. Un examen humain est fortement recommandé avant la publication.
            </mj-text>
          </mj-column>
        </mj-section>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
⚠️ AVERTISSEMENT DE QUALITÉ DES TRADUCTIONS

Examen recommandé

Votre tâche de traduction est terminée, mais {{ low_quality_count }} traductions ont obtenu un score inférieur au seuil de qualité et devraient être examinées avant la publication.

RÉSUMÉ DE LA TÂCHE : 
- Job ID : {{ job_id }}
- Type de contenu : {{ content_type }}
- Total d'éléments : {{ total_items }}
- Qualité moyenne : {{ average_quality }}%
- Qualité faible : {{ low_quality_count }} éléments ({{ low_quality_percentage }}%)

DÉTAIL DES SCORES DE QUALITÉ : 
- Excellent (95-100%) : {{ excellent_count }} éléments
- Bon (85-94%) : {{ good_count }} éléments
- Acceptable (70-84%) : {{ fair_count }} éléments
- Mauvais (<70%) : {{ poor_count }} éléments

PROBLÈMES DE QUALITÉ COURANTS : 
{% for issue in quality_issues %}
{{ issue.type }} : {{ issue.count }} occurrences
{% endfor %}

ACTIONS RÉCOMMANDEES : 
1. Vérifier les traductions signalées via le panneau d'administration
2. Modifier manuellement les traductions de faible qualité
3. Réfléchir à la re-traduction des éléments de faible qualité
4. Publier uniquement après la vérification complète

Vérifier les traductions : {{ review_url }}
Voir les éléments de faible qualité : {{ low_quality_url }}

💡 Conseil : Les scores de qualité inférieurs à 85 % indiquent des problèmes potentiels liés à la grammaire, au contexte ou à la précision. Un examen humain est fortement recommandé avant la publication.