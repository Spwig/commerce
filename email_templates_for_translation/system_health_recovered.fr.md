---
template_type: system_health_recovered
category: System Health
---

# Email Template: system_health_recovered

## Subject
✓ Résolu : {{ metric_name }} est revenu à la normale

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#dcfce7">
      <mj-column>
        <mj-text font-size="24px" font-weight="bold" color="#065f46" align="center">
          ✓ Problème Résolu
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Récupération de la Santé du Système
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Bonne nouvelle ! Le problème de santé du système avec {{ metric_name }} a été résolu.
        </mj-text>

        <mj-spacer height="30px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
              Détails de la Récupération :
            </mj-text>
            <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>Métrique :</strong> {{ metric_name }}<br/>
              <strong>Valeur Actuelle :</strong> <span style="color: #059669; font-weight: bold;">{{ current_value }}</span><br/>
              <strong>Seuil Normal :</strong> {{ normal_threshold }}<br/>
              <strong>Problème Détecté :</strong> {{ issue_detected_at }}<br/>
              <strong>Rétabli :</strong> {{ recovered_at }}<br/>
              <strong>Durée :</strong> {{ issue_duration }}
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-section background-color="#f0fdf4" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="15px" color="#065f46" font-weight="bold">
              ✓ État du Système : Normal
            </mj-text>
            <mj-text font-size="14px" color="#065f46" line-height="1.6">
              {{ metric_name }} est revenu à un niveau normal et fonctionne dans les paramètres acceptables.
            </mj-text>
          </mj-column>
        </mj-section>

        {% if resolution_summary %}
        <mj-spacer height="30px" />
        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Résumé de la Résolution :
        </mj-text>
        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}" line-height="1.8">
          {{ resolution_summary }}
        </mj-text>
        {% endif %}

        {% if actions_taken %}
        <mj-spacer height="30px" />
        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Actions Prises :
        </mj-text>
        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="14px" color="{{ theme.color.text|default:'#4b5563' }}" line-height="1.6">
              {{ actions_taken }}
            </mj-text>
          </mj-column>
        </mj-section>
        {% endif %}

        {% if preventive_measures %}
        <mj-spacer height="30px" />
        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Mesures Préventives :
        </mj-text>
        <mj-section background-color="#eff6ff" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="14px" color="#1e40af" line-height="1.6">
              {{ preventive_measures }}
            </mj-text>
          </mj-column>
        </mj-section>
        {% endif %}

        <mj-spacer height="30px" />

        <mj-button href="{{ dashboard_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          Voir le Tableau de Bord du Système
        </mj-button>

        {% if incident_report_url %}
        <mj-spacer height="10px" />
        <mj-button href="{{ incident_report_url }}" background-color="#6b7280" color="#ffffff" font-size="14px" border-radius="6px" padding="10px 25px">
          Voir le Rapport d'Incident
        </mj-button>
        {% endif %}
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
✓ PROBLÈME RÉSOLU

Récupération de la Santé du Système

Bonne nouvelle ! Le problème de santé du système avec {{ metric_name }} a été résolu.

DÉTAILS DE LA RÉCUPÉRATION :
- Métrique : {{ metric_name }}
- Valeur Actuelle : {{ current_value }}
- Seuil Normal : {{ normal_threshold }}
- Problème Détecté : {{ issue_detected_at }}
- Rétabli : {{ recovered_at }}
- Durée : {{ issue_duration }}

✓ ÉTAT DU SYSTÈME : NORMAL
{{ metric_name }} est revenu à un niveau normal et fonctionne dans les paramètres acceptables.

{% if resolution_summary %}
RÉSUMÉ DE LA RÉSOLUTION :
{{ resolution_summary }}
{% endif %}

{% if actions_taken %}
ACTIONS PRISES :
{{ actions_taken }}
{% endif %}

{% if preventive_measures %}
MESURES PRÉVENTIVES :
{{ preventive_measures }}
{% endif %}

Voir le tableau de bord du système : {{ dashboard_url }}
{% if incident_report_url %}Voir le rapport d'incident : {{ incident_report_url }}{% endif %}