---
template_type: system_performance_degraded
category: System Health
---

# Email Template: system_performance_degraded

## Subject
⚠️ Performance Degradation Detected - {{ affected_area }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#fef3c7">
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="#92400e" align="center">
          ⚠️ Performance Degradation
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="18px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Slow Response Times Detected
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}">
          Your Spwig installation is experiencing performance degradation.
        </mj-text>

        <mj-spacer height="20px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
              Performance Issue:
            </mj-text>
            <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>Affected Area:</strong> {{ affected_area }}<br/>
              <strong>Current Response Time:</strong> <span style="color: #d97706; font-weight: bold;">{{ current_response_time }}ms</span><br/>
              <strong>Normal Response Time:</strong> {{ normal_response_time }}ms<br/>
              <strong>Degradation:</strong> {{ degradation_percentage }}% slower<br/>
              <strong>Detected:</strong> {{ detected_at }}
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
          Possible Causes:
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}" line-height="1.8">
          {{ possible_causes }}
        </mj-text>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Slowest Endpoints:
        </mj-text>

        {% for endpoint in slow_endpoints %}
        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="12px">
          <mj-column>
            <mj-text font-size="14px" color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>{{ endpoint.path }}</strong> - {{ endpoint.avg_time }}ms ({{ endpoint.request_count }} requests)
            </mj-text>
          </mj-column>
        </mj-section>
        <mj-spacer height="8px" />
        {% endfor %}

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Recommended Actions:
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}" line-height="1.8">
          {{ recommended_actions }}
        </mj-text>

        <mj-spacer height="30px" />

        <mj-button href="{{ performance_dashboard_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          View Performance Dashboard
        </mj-button>

        <mj-spacer height="10px" />

        <mj-button href="{{ slow_queries_url }}" background-color="#6b7280" color="#ffffff" font-size="14px" border-radius="6px" padding="10px 25px">
          View Slow Queries
        </mj-button>

        <mj-spacer height="20px" />

        <mj-text font-size="13px" color="{{ theme.color.text_secondary|default:'#6b7280' }}" align="center">
          We'll notify you when performance returns to normal.
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
⚠️ PERFORMANCE DEGRADATION

Slow Response Times Detected

Your Spwig installation is experiencing performance degradation.

PERFORMANCE ISSUE:
- Affected Area: {{ affected_area }}
- Current Response Time: {{ current_response_time }}ms
- Normal Response Time: {{ normal_response_time }}ms
- Degradation: {{ degradation_percentage }}% slower
- Detected: {{ detected_at }}

IMPACT:
{{ impact_description }}

POSSIBLE CAUSES:
{{ possible_causes }}

SLOWEST ENDPOINTS:
{% for endpoint in slow_endpoints %}
{{ endpoint.path }} - {{ endpoint.avg_time }}ms ({{ endpoint.request_count }} requests)
{% endfor %}

RECOMMENDED ACTIONS:
{{ recommended_actions }}

View performance dashboard: {{ performance_dashboard_url }}
View slow queries: {{ slow_queries_url }}

We'll notify you when performance returns to normal.

## Variables

| Variable | Description | Example |
|----------|-------------|---------|
| affected_area | What's slow | Product Pages |
| current_response_time | Current avg response time | 2,450 |
| normal_response_time | Normal avg response time | 850 |
| degradation_percentage | Percentage slower | 188 |
| detected_at | When detected | February 15, 2026 at 3:45 PM |
| impact_description | Customer impact | Customers may experience slower page loads, potentially affecting conversion rates |
| possible_causes | What might cause it | • Database query performance issues\n• High server load\n• External API slowdown\n• Memory constraints |
| slow_endpoints | Slowest URL paths | [{path: '/products/category/electronics/', avg_time: 3200, request_count: 245}] |
| recommended_actions | What to do | • Review database query logs\n• Check server resource usage\n• Monitor external API status\n• Consider enabling caching |
| performance_dashboard_url | Performance dashboard | https://shop.com/en/admin/system/performance |
| slow_queries_url | Slow queries log | https://shop.com/en/admin/system/slow-queries |

## Notes

- Admin/technical notification
- Sent when response times exceed threshold (e.g., 2x normal)
- Focus on customer-facing impact
- Provides troubleshooting starting points
- Lists specific slow endpoints
- Links to performance tools
- Transactional email
