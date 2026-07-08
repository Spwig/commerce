---
template_type: feed_weekly_report
category: Product Feeds
---

# Email Template: feed_weekly_report

## Subject
📊 Rapport hebdomadaire des alimentations de produits - {{ week_range }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#eff6ff">
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="#1e40af" align="center">
          📊 Performance des alimentations hebdomadaires
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="18px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Résumé de la performance des alimentations
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}">
          Voici comment vos alimentations de produits se sont déroulées pendant {{ week_range }}.
        </mj-text>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Statistiques globales :
        </mj-text>

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>Total des alimentations :</strong> {{ total_feeds }}<br/>
              <strong>Alimentations actives :</strong> {{ active_feeds }}<br/>
              <strong>Total des synchronisations :</strong> {{ total_syncs }}<br/>
              <strong>Synchronisations réussies :</strong> {{ successful_syncs }} ({{ success_rate }}%)<br/>
              <strong>Synchronisations échouées :</strong> {{ failed_syncs }}
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Performance par alimentation : 
        </mj-text>

        {% for feed in feed_stats %}
        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="15px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
              {{ feed.name }}
            </mj-text>
            <mj-text font-size="14px" color="{{ theme.color.text|default:'#4b5563' }}">
              Plateforme : {{ feed.platform }}<br/>
              Synchronisations : {{ feed.sync_count }} ({{ feed.success_count }} réussies)<br/>
              Produits : {{ feed.product_count }}<br/>
              {% if feed.errors > 0 %}Erreurs : {{ feed.errors }}{% endif %}
            </mj-text>
          </mj-column>
        </mj-section>
        <mj-spacer height="10px" />
        {% endfor %}

        {% if top_errors %}
        <mj-spacer height="30px" />
        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Problèmes les plus courants : 
        </mj-text>
        {% for error in top_errors %}
        <mj-section background-color="#fef3c7" border-radius="8px" padding="12px">
          <mj-column>
            <mj-text font-size="14px" color="#92400e">
              <strong>{{ error.type }} :</strong> {{ error.count }} occurrences
            </mj-text>
          </mj-column>
        </mj-section>
        <mj-spacer height="8px" />
        {% endfor %}
        {% endif %}

        <mj-spacer height="30px" />

        {% if recommendations %}
        <mj-section background-color="#f0fdf4" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="15px" color="#065f46" font-weight="bold">
              💡 Recommandations
            </mj-text>
            <mj-text font-size="14px" color="#065f46" line-height="1.6">
              {{ recommendations }}
            </mj-text>
          </mj-column>
        </mj-section>
        {% endif %}

        <mj-spacer height="30px" />

        <mj-button href="{{ feeds_dashboard_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          Voir le tableau de bord des alimentations
        </mj-button>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
📊 PERFORMANCE DES ALIMENTATIONS HEBDOMADAIRES

Résumé de la performance des alimentations

Voici comment vos alimentations de produits se sont déroulées pendant {{ week_range }}.

STATISTIQUES GLOBALES : 
- Total des alimentations : {{ total_feeds }}
- Alimentations actives : {{ active_feeds }}
- Total des synchronisations : {{ total_syncs }}
- Synchronisations réussies : {{ successful_syncs }} ({{ success_rate }}%)
- Synchronisations échouées : {{ failed_syncs }}

PERFORMANCE PAR ALIMENTATION : 
{% for feed in feed_stats %}
{{ feed.name }}
Plateforme : {{ feed.platform }}
Synchronisations : {{ feed.sync_count }} ({{ feed.success_count }} réussies)
Produits : {{ feed.product_count }}
{% if feed.errors > 0 %}Erreurs : {{ feed.errors }}{% endif %}

{% endfor %}

{% if top_errors %}
PROBLEMES LES PLUS COURANTS : 
{% for error in top_errors %}
{{ error.type }} : {{ error.count }} occurrences
{% endfor %}
{% endif %}

{% if recommendations %}
💡 RECOMMANDATIONS : 
{{ recommendations }}
{% endif %}

Voir le tableau de bord des alimentations : {{ feeds_dashboard_url }}