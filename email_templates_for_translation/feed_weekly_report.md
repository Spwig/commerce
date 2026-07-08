---
template_type: feed_weekly_report
category: Product Feeds
---

# Email Template: feed_weekly_report

## Subject
📊 Weekly Product Feed Report - {{ week_range }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#eff6ff">
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="#1e40af" align="center">
          📊 Weekly Feed Performance
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="18px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Feed Performance Summary
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}">
          Here's how your product feeds performed from {{ week_range }}.
        </mj-text>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Overall Stats:
        </mj-text>

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>Total Feeds:</strong> {{ total_feeds }}<br/>
              <strong>Active Feeds:</strong> {{ active_feeds }}<br/>
              <strong>Total Syncs:</strong> {{ total_syncs }}<br/>
              <strong>Successful Syncs:</strong> {{ successful_syncs }} ({{ success_rate }}%)<br/>
              <strong>Failed Syncs:</strong> {{ failed_syncs }}
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Feed-by-Feed Performance:
        </mj-text>

        {% for feed in feed_stats %}
        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="15px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
              {{ feed.name }}
            </mj-text>
            <mj-text font-size="14px" color="{{ theme.color.text|default:'#4b5563' }}">
              Platform: {{ feed.platform }}<br/>
              Syncs: {{ feed.sync_count }} ({{ feed.success_count }} successful)<br/>
              Products: {{ feed.product_count }}<br/>
              {% if feed.errors > 0 %}Errors: {{ feed.errors }}{% endif %}
            </mj-text>
          </mj-column>
        </mj-section>
        <mj-spacer height="10px" />
        {% endfor %}

        {% if top_errors %}
        <mj-spacer height="30px" />
        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Most Common Issues:
        </mj-text>
        {% for error in top_errors %}
        <mj-section background-color="#fef3c7" border-radius="8px" padding="12px">
          <mj-column>
            <mj-text font-size="14px" color="#92400e">
              <strong>{{ error.type }}:</strong> {{ error.count }} occurrences
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
              💡 Recommendations
            </mj-text>
            <mj-text font-size="14px" color="#065f46" line-height="1.6">
              {{ recommendations }}
            </mj-text>
          </mj-column>
        </mj-section>
        {% endif %}

        <mj-spacer height="30px" />

        <mj-button href="{{ feeds_dashboard_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          View Feeds Dashboard
        </mj-button>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
📊 WEEKLY FEED PERFORMANCE

Feed Performance Summary

Here's how your product feeds performed from {{ week_range }}.

OVERALL STATS:
- Total Feeds: {{ total_feeds }}
- Active Feeds: {{ active_feeds }}
- Total Syncs: {{ total_syncs }}
- Successful Syncs: {{ successful_syncs }} ({{ success_rate }}%)
- Failed Syncs: {{ failed_syncs }}

FEED-BY-FEED PERFORMANCE:
{% for feed in feed_stats %}
{{ feed.name }}
Platform: {{ feed.platform }}
Syncs: {{ feed.sync_count }} ({{ feed.success_count }} successful)
Products: {{ feed.product_count }}
{% if feed.errors > 0 %}Errors: {{ feed.errors }}{% endif %}

{% endfor %}

{% if top_errors %}
MOST COMMON ISSUES:
{% for error in top_errors %}
{{ error.type }}: {{ error.count }} occurrences
{% endfor %}
{% endif %}

{% if recommendations %}
💡 RECOMMENDATIONS:
{{ recommendations }}
{% endif %}

View feeds dashboard: {{ feeds_dashboard_url }}

## Variables

| Variable | Description | Example |
|----------|-------------|---------|
| week_range | Week date range | February 8-14, 2026 |
| total_feeds | Total configured feeds | 5 |
| active_feeds | Currently active feeds | 4 |
| total_syncs | Total sync attempts | 28 |
| successful_syncs | Successful syncs | 26 |
| success_rate | Success percentage | 92.9 |
| failed_syncs | Failed syncs | 2 |
| feed_stats | Per-feed stats array | [{name: 'Google Shopping', platform: 'Google Merchant', sync_count: 7, ...}] |
| top_errors | Most common error types | [{type: 'Missing GTIN', count: 12}] |
| recommendations | Suggested improvements | Consider adding GTIN codes to improve product eligibility |
| feeds_dashboard_url | Feeds dashboard | https://shop.com/en/admin/feeds |

## Notes

- Admin report - weekly digest
- Sent every Monday morning
- Summarizes all feed activity
- Shows per-feed performance metrics
- Highlights common issues
- Provides actionable recommendations
- Recipients can opt out in communication preferences
