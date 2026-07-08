---
template_type: feed_weekly_report
category: Product Feeds
---

# Email Template: feed_weekly_report

## Subject
📊 सीधा उत्पाद फीड रिपोर्ट - {{ week_range }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#eff6ff">
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="#1e40af" align="center">
          📊 सीधा फीड की कार्यक्षमता
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="18px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          फीड कार्यक्षमता सारांश
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}">
          यहाँ {{ week_range }} के दौरान आपके उत्पाद फीड के कार्यक्षमता के बारे में बताया गया है।
        </mj-text>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          समग्र सांख्यिकी:
        </mj-text>

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>कुल फीड:</strong> {{ total_feeds }}<br/>
              <strong>सक्रिय फीड:</strong> {{ active_feeds }}<br/>
              <strong>कुल सिंक:</strong> {{ total_syncs }}<br/>
              <strong>सफल सिंक:</strong> {{ successful_syncs }} ({{ success_rate }}%)<br/>
              <strong>असफल सिंक:</strong> {{ failed_syncs }}
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          फीड-द्वारा फीड कार्यक्षमता:
        </mj-text>

        {% for feed in feed_stats %}
        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="15px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
              {{ feed.name }}
            </mj-text>
            <mj-text font-size="14px" color="{{ theme.color.text|default:'#4b5563' }}">
              प्लेटफॉर्म: {{ feed.platform }}<br/>
              सिंक: {{ feed.sync_count }} ({{ feed.success_count }} सफल)<br/>
              उत्पाद: {{ feed.product_count }}<br/>
              {% if feed.errors > 0 %}त्रुटि: {{ feed.errors }}{% endif %}
            </mj-text>
          </mj-column>
        </mj-section>
        <mj-spacer height="10px" />
        {% endfor %}

        {% if top_errors %}
        <mj-spacer height="30px" />
        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          सबसे आम समस्याएं:
        </mj-text>
        {% for error in top_errors %}
        <mj-section background-color="#fef3c7" border-radius="8px" padding="12px">
          <mj-column>
            <mj-text font-size="14px" color="#92400e">
              <strong>{{ error.type }}:</strong> {{ error.count }} घटनाएं
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
              💡 सुझाव
            </mj-text>
            <mj-text font-size="14px" color="#065f46" line-height="1.6">
              {{ recommendations }}
            </mj-text>
          </mj-column>
        </mj-section>
        {% endif %}

        <mj-spacer height="30px" />

        <mj-button href="{{ feeds_dashboard_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          फीड डैशबोर्ड देखें
        </mj-button>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
📊 सीधा फीड कार्यक्षमता

फीड कार्यक्षमता सारांश

यहाँ {{ week_range }} के दौरान आपके उत्पाद फीड के कार्यक्षमता के बारे में बताया गया है।

समग्र सांख्यिकी:
- कुल फीड: {{ total_feeds }}
- सक्रिय फीड: {{ active_feeds }}
- कुल सिंक: {{ total_syncs }}
- सफल सिंक: {{ successful_syncs }} ({{ success_rate }}%)
- असफल सिंक: {{ failed_syncs }}

फीड-द्वारा फीड कार्यक्षमता:
{% for feed in feed_stats %}
{{ feed.name }}
प्लेटफॉर्म: {{ feed.platform }}
सिंक: {{ feed.sync_count }} ({{ feed.success_count }} सफल)
उत्पाद: {{ feed.product_count }}
{% if feed.errors > 0 %}त्रुटि: {{ feed.errors }}{% endif %}

{% endfor %}

{% if top_errors %}
सबसे आम समस्याएं:
{% for error in top_errors %}
{{ error.type }}: {{ error.count }} घटनाएं
{% endfor %}
{% endif %}

{% if recommendations %}
💡 सुझाव:
{{ recommendations }}
{% endif %}

फीड डैशबोर्ड देखें: {{ feeds_dashboard_url }}