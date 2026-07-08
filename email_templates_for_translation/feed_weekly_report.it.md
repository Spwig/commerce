---
template_type: feed_weekly_report
category: Product Feeds
---

# Email Template: feed_weekly_report

## Subject
📊 Rapporto settimanale sul feed dei prodotti - {{ week_range }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#eff6ff">
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="#1e40af" align="center">
          📊 Performance settimanale del feed
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="18px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Riepilogo performance del feed
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}">
          Ecco come i tuoi feed dei prodotti si sono comportati da {{ week_range }}.
        </mj-text>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Statistiche generali:
        </mj-text>

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>Totale feed:</strong> {{ total_feeds }}<br/>
              <strong>Feed attivi:</strong> {{ active_feeds }}<br/>
              <strong>Totale sincronizzazioni:</strong> {{ total_syncs }}<br/>
              <strong>Sincronizzazioni riuscite:</strong> {{ successful_syncs }} ({{ success_rate }}%)<br/>
              <strong>Sincronizzazioni fallite:</strong> {{ failed_syncs }}
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Performance per feed:
        </mj-text>

        {% for feed in feed_stats %}
        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="15px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
              {{ feed.name }}
            </mj-text>
            <mj-text font-size="14px" color="{{ theme.color.text|default:'#4b5563' }}">
              Piattaforma: {{ feed.platform }}<br/>
              Sincronizzazioni: {{ feed.sync_count }} ({{ feed.success_count }} riuscite)<br/>
              Prodotti: {{ feed.product_count }}<br/>
              {% if feed.errors > 0 %}Errori: {{ feed.errors }}{% endif %}
            </mj-text>
          </mj-column>
        </mj-section>
        <mj-spacer height="10px" />
        {% endfor %}

        {% if top_errors %}
        <mj-spacer height="30px" />
        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Problemi più comuni:
        </mj-text>
        {% for error in top_errors %}
        <mj-section background-color="#fef3c7" border-radius="8px" padding="12px">
          <mj-column>
            <mj-text font-size="14px" color="#92400e">
              <strong>{{ error.type }}:</strong> {{ error.count }} occorrenze
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
              💡 Suggerimenti
            </mj-text>
            <mj-text font-size="14px" color="#065f46" line-height="1.6">
              {{ recommendations }}
            </mj-text>
          </mj-column>
        </mj-section>
        {% endif %}

        <mj-spacer height="30px" />

        <mj-button href="{{ feeds_dashboard_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          Visualizza il pannello dei feed
        </mj-button>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
📊 PERFORMANCE DEL FEED SETTIMANALE

Riepilogo performance del feed

Ecco come i tuoi feed dei prodotti si sono comportati da {{ week_range }}.

STATISTICHE GENERALI:
- Totale feed: {{ total_feeds }}
- Feed attivi: {{ active_feeds }}
- Totale sincronizzazioni: {{ total_syncs }}
- Sincronizzazioni riuscite: {{ successful_syncs }} ({{ success_rate }}%)
- Sincronizzazioni fallite: {{ failed_syncs }}

PERFORMANCE PER FEED:
{% for feed in feed_stats %}
{{ feed.name }}
Piattaforma: {{ feed.platform }}
Sincronizzazioni: {{ feed.sync_count }} ({{ feed.success_count }} riuscite)
Prodotti: {{ feed.product_count }}
{% if feed.errors > 0 %}Errori: {{ feed.errors }}{% endif %}

{% endfor %}

{% if top_errors %}
PROBLEMI PIÙ COMUNI:
{% for error in top_errors %}
{{ error.type }}: {{ error.count }} occorrenze
{% endfor %}
{% endif %}

{% if recommendations %}
💡 SUGGERIMENTI:
{{ recommendations }}
{% endif %}

Visualizza il pannello dei feed: {{ feeds_dashboard_url }}