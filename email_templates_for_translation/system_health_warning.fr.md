---
template_type: system_health_warning
category: System Health
---

# Email Template: system_health_warning

## Subject
⚠️ Avertissement de santé du système : {{ metric_name }} - {{ current_value }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#fef3c7">
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="#92400e" align="center">
          ⚠️ Avertissement de santé du système
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="18px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Seuil d'avertissement dépassé
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}">
          Un indicateur de santé du système a dépassé le seuil d'avertissement sur votre installation Spwig.
        </mj-text>

        <mj-spacer height="20px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
              Détails de l'avertissement :
            </mj-text>
            <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>Métrique :</strong> {{ metric_name }}<br/>
              <strong>Valeur actuelle :</strong> <span style="color: #d97706; font-weight: bold;">{{ current_value }}</span><br/>
              <strong>Seuil d'avertissement :</strong> {{ warning_threshold }}<br/>
              <strong>Seuil critique :</strong> {{ critical_threshold }}<br/>
              <strong>Détecté :</strong> {{ detected_at }}
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Impact potentiel :
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}" line-height="1.8">
          {{ impact_description }}
        </mj-text>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Actions recommandées :
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}" line-height="1.8">
          {{ recommended_actions }}
        </mj-text>

        {% if trend_data %}
        <mj-spacer height="30px" />
        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Analyse des tendances :
        </mj-text>
        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="14px" color="{{ theme.color.text|default:'#4b5563' }}">
              {{ trend_data }}
            </mj-text>
          </mj-column>
        </mj-section>
        {% endif %}

        <mj-spacer height="30px" />

        <mj-section background-color="#eff6ff" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="14px" color="#1e40af" line-height="1.6">
              💡 Action requise : Bien qu'il ne soit pas critique pour le moment, résoudre cet avertissement maintenant peut empêcher des problèmes de service futurs.
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-button href="{{ dashboard_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          Voir le tableau de bord du système
        </mj-button>

        <mj-spacer height="10px" />

        <mj-button href="{{ metrics_url }}" background-color="#6b7280" color="#ffffff" font-size="14px" border-radius="6px" padding="10px 25px">
          Voir les métriques détaillées
        </mj-button>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
⚠️ AVERTISSEMENT DE SANTÉ DU SYSTÈME

Seuil d'avertissement dépassé

Un indicateur de santé du système a dépassé le seuil d'avertissement sur votre installation Spwig.

DÉTAILS DE L'AVERTISSEMENT :
- Métrique : {{ metric_name }}
- Valeur actuelle : {{ current_value }}
- Seuil d'avertissement : {{ warning_threshold }}
- Seuil critique : {{ critical_threshold }}
- Détecté : {{ detected_at }}

IMPACT POTENTIEL :
{{ impact_description }}

ACTIONS RECOMMANDÉES :
{{ recommended_actions }}

{% if trend_data %}
ANALYSE DES TENDANCES :
{{ trend_data }}
{% endif %}

💡 ACTION REQUIS : Bien qu'il ne soit pas critique pour le moment, résoudre cet avertissement maintenant peut empêcher des problèmes de service futurs.

Voir le tableau de bord du système : {{ dashboard_url }}
Voir les métriques détaillées : {{ metrics_url }}
