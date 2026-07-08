---
template_type: system_performance_degraded
category: System Health
---

# Email Template: system_performance_degraded

## Subject
⚠️ Détérioration des performances - {{ affected_area }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#fef3c7">
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="#92400e" align="center">
          ⚠️ Détérioration des performances
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="18px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Temps de réponse lents détectés
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}">
          Votre installation Spwig subit une déterioration des performances.
        </mj-text>

        <mj-spacer height="20px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
              Problème de performance:
            </mj-text>
            <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>Zone affectée :</strong> {{ affected_area }}<br/>
              <strong>Temps de réponse actuel :</strong> <span style="color: #d97706; font-weight: bold;">{{ current_response_time }}ms</span><br/>
              <strong>Temps de réponse normal :</strong> {{ normal_response_time }}ms<br/>
              <strong>Détérioration :</strong> {{ degradation_percentage }}% plus lent<br/>
              <strong>Détecté :</strong> {{ detected_at }}
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Impact:
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}" line-height="1.8">
          {{ impact_description }}
        </mj-text>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Causes possibles:
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}" line-height="1.8">
          {{ possible_causes }}
        </mj-text>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Endpoints les plus lents:
        </mj-text>

        {% for endpoint in slow_endpoints %}
        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="12px">
          <mj-column>
            <mj-text font-size="14px" color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>{{ endpoint.path }}</strong> - {{ endpoint.avg_time }}ms ({{ endpoint.request_count }} requêtes)
            </mj-text>
          </mj-column>
        </mj-section>
        <mj-spacer height="8px" />
        {% endfor %}

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Actions recommandées:
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}" line-height="1.8">
          {{ recommended_actions }}
        </mj-text>

        <mj-spacer height="30px" />

        <mj-button href="{{ performance_dashboard_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          Voir le tableau de bord des performances
        </mj-button>

        <mj-spacer height="10px" />

        <mj-button href="{{ slow_queries_url }}" background-color="#6b7280" color="#ffffff" font-size="14px" border-radius="6px" padding="10px 25px">
          Voir les requêtes lentes
        </mj-button>

        <mj-spacer height="20px" />

        <mj-text font-size="13px" color="{{ theme.color.text_secondary|default:'#6b7280' }}" align="center">
          Nous vous informerons lorsque les performances retrouveront un fonctionnement normal.
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
⚠️ DÉTÉRIORATION DES PERFORMANCES

Temps de réponse lents détectés

Votre installation Spwig subit une déterioration des performances.

PROBLÈME DE PERFORMANCE:
- Zone affectée : {{ affected_area }}
- Temps de réponse actuel : {{ current_response_time }}ms
- Temps de réponse normal : {{ normal_response_time }}ms
- Détérioration : {{ degradation_percentage }}% plus lent
- Détecté : {{ detected_at }}

IMPACT:
{{ impact_description }}

CAUSES POSSIBLES:
{{ possible_causes }}

ENDPOINTS LES PLUS LENTS:
{% for endpoint in slow_endpoints %}
{{ endpoint.path }} - {{ endpoint.avg_time }}ms ({{ endpoint.request_count }} requêtes)
{% endfor %}

ACTIONS RECOMMANDÉES:
{{ recommended_actions }}

Voir le tableau de bord des performances : {{ performance_dashboard_url }}
Voir les requêtes lentes : {{ slow_queries_url }}

Nous vous informerons lorsque les performances retrouveront un fonctionnement normal.