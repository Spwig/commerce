---
template_type: system_health_critical
category: System Health
---

# Email Template: system_health_critical

## Subject
🚨 ALERTE CRITIQUE : {{ metric_name }} - {{ current_value }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#fee2e2">
      <mj-column>
        <mj-text font-size="22px" font-weight="bold" color="#991b1b" align="center">
          🚨 ALERTE SYSTEME CRITIQUE
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="18px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Attention immédiate requise
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}">
          Un problème critique de santé du système a été détecté sur votre installation Spwig.
        </mj-text>

        <mj-spacer height="20px" />

        <mj-section background-color="#fee2e2" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="#991b1b" font-size="16px">
              🚨 Problème critique
            </mj-text>
            <mj-text color="#991b1b">
              <strong>Métrique :</strong> {{ metric_name }}<br/>
              <strong>Valeur actuelle :</strong> <span style="font-size: 18px; font-weight: bold;">{{ current_value }}</span><br/>
              <strong>Seuil critique :</strong> {{ critical_threshold }}<br/>
              <strong>Détecté :</strong> {{ detected_at }}<br/>
              <strong>Gravité :</strong> CRITIQUE
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Impact : 
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}" line-height="1.8">
          {{ impact_description }}
        </mj-text>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Actions immédiates requises : 
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}" line-height="1.8">
          {{ recommended_actions }}
        </mj-text>

        {% if trend_data %}
        <mj-spacer height="30px" />
        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Tendance : 
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

        <mj-section background-color="#fef3c7" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="14px" color="#92400e" font-weight="bold">
              ⚠️ Avertissement de dégradation du service
            </mj-text>
            <mj-text font-size="14px" color="#92400e" line-height="1.6">
              Ce problème peut entraîner des interruptions de service ou une dégradation des performances. Résolvez-le immédiatement pour éviter un impact sur les clients.
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-button href="{{ dashboard_url }}" background-color="#dc2626" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          Voir le tableau de bord du système
        </mj-button>

        <mj-spacer height="10px" />

        <mj-button href="{{ logs_url }}" background-color="#6b7280" color="#ffffff" font-size="14px" border-radius="6px" padding="10px 25px">
          Voir les journaux du système
        </mj-button>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
🚨 ALERTE SYSTEME CRITIQUE

Attention immédiate requise

Un problème critique de santé du système a été détecté sur votre installation Spwig.

🚨 PROBLEME CRITIQUE : 
- Métrique : {{ metric_name }}
- Valeur actuelle : {{ current_value }}
- Seuil critique : {{ critical_threshold }}
- Détecté : {{ detected_at }}
- Gravité : CRITIQUE

IMPACT : 
{{ impact_description }}

ACTIONS IMMEDIATES REQUISES : 
{{ recommended_actions }}

{% if trend_data %}
TENDANCE : 
{{ trend_data }}
{% endif %}

⚠️ AVERTISSEMENT DE DEGRADATION DU SERVICE : 
Ce problème peut entraîner des interruptions de service ou une dégradation des performances. Résolvez-le immédiatement pour éviter un impact sur les clients.

Voir le tableau de bord du système : {{ dashboard_url }}
Voir les journaux du système : {{ logs_url }}