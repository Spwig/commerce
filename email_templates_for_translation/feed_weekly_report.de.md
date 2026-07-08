---
template_type: feed_weekly_report
category: Product Feeds
---

# Email Template: feed_weekly_report

## Subject
📊 Wöchentlicher Produkt-Feed-Bericht - {{ week_range }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#eff6ff">
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="#1e40af" align="center">
          📊 Wöchentliche Feed-Leistung
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="18px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Feed-Leistungsübersicht
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}">
          Hier sehen Sie, wie Ihre Produkt-Feeds von {{ week_range }} abgelaufen sind.
        </mj-text>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Gesamte Statistiken:
        </mj-text>

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>Gesamtfeeds:</strong> {{ total_feeds }}<br/>
              <strong>Aktive Feeds:</strong> {{ active_feeds }}<br/>
              <strong>Gesamte Syncs:</strong> {{ total_syncs }}<br/>
              <strong>Erfolgreiche Syncs:</strong> {{ successful_syncs }} ({{ success_rate }}%)<br/>
              <strong>Fehlgeschlagene Syncs:</strong> {{ failed_syncs }}
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Leistungsübersicht pro Feed:
        </mj-text>

        {% for feed in feed_stats %}
        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="15px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
              {{ feed.name }}
            </mj-text>
            <mj-text font-size="14px" color="{{ theme.color.text|default:'#4b5563' }}">
              Plattform: {{ feed.platform }}<br/>
              Syncs: {{ feed.sync_count }} ({{ feed.success_count }} erfolgreich)<br/>
              Produkte: {{ feed.product_count }}<br/>
              {% if feed.errors > 0 %}Fehler: {{ feed.errors }}{% endif %}
            </mj-text>
          </mj-column>
        </mj-section>
        <mj-spacer height="10px" />
        {% endfor %}

        {% if top_errors %}
        <mj-spacer height="30px" />
        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Häufigste Probleme:
        </mj-text>
        {% for error in top_errors %}
        <mj-section background-color="#fef3c7" border-radius="8px" padding="12px">
          <mj-column>
            <mj-text font-size="14px" color="#92400e">
              <strong>{{ error.type }}:</strong> {{ error.count }} Vorkommnisse
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
              💡 Empfehlungen
            </mj-text>
            <mj-text font-size="14px" color="#065f46" line-height="1.6">
              {{ recommendations }}
            </mj-text>
          </mj-column>
        </mj-section>
        {% endif %}

        <mj-spacer height="30px" />

        <mj-button href="{{ feeds_dashboard_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          Feed-Dashboard ansehen
        </mj-button>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
📊 WÖCHENTLICHE FEED-LEISTUNG

Feed-Leistungsübersicht

Hier sehen Sie, wie Ihre Produkt-Feeds von {{ week_range }} abgelaufen sind.

GESAMTE STATISTIKEN:
- Gesamtfeeds: {{ total_feeds }}
- Aktive Feeds: {{ active_feeds }}
- Gesamte Syncs: {{ total_syncs }}
- Erfolgreiche Syncs: {{ successful_syncs }} ({{ success_rate }}%)
- Fehlgeschlagene Syncs: {{ failed_syncs }}

LEISTUNGSÜBERSICHT PRO FEED:
{% for feed in feed_stats %}
{{ feed.name }}
Plattform: {{ feed.platform }}
Syncs: {{ feed.sync_count }} ({{ feed.success_count }} erfolgreich)
Produkte: {{ feed.product_count }}
{% if feed.errors > 0 %}Fehler: {{ feed.errors }}{% endif %}

{% endfor %}

{% if top_errors %}
HÄUFIGSTE PROBLEME:
{% for error in top_errors %}
{{ error.type }}: {{ error.count }} Vorkommnisse
{% endfor %}
{% endif %}

{% if recommendations %}
💡 EMPFEHLUNGEN:
{{ recommendations }}
{% endif %}

Feed-Dashboard ansehen: {{ feeds_dashboard_url }}