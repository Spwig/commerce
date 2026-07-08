---
template_type: feed_generation_completed
category: Product Feeds
---

# Email Template: feed_generation_completed

## Subject
✓ Feed del prodotto generato: {{ feed_name }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#dcfce7">
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="#065f46" align="center">
          ✓ Feed Generato Con Successo
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="18px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Product Feed Ready
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}">
          Your {{ feed_name }} product feed has been successfully generated and is ready for use.
        </mj-text>

        <mj-spacer height="20px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
              Feed Details:
            </mj-text>
            <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>Feed:</strong> {{ feed_name }}<br/>
              <strong>Format:</strong> {{ feed_format }}<br/>
              <strong>Products:</strong> {{ product_count }}<br/>
              <strong>Generated:</strong> {{ generated_at }}<br/>
              <strong>File Size:</strong> {{ file_size }}
            </mj-text>
          </mj-column>
        </mj-section>

        {% if warnings_count > 0 %}
        <mj-spacer height="20px" />
        <mj-section background-color="#fef3c7" border-radius="8px" padding="15px">
          <mj-column>
            <mj:text font-size="14px" color="#92400e" font-weight="bold">
              ⚠️ {{ warnings_count }} Warning{{ warnings_count|pluralize }}
            </mj-text>
            <mj-text font-size="14px" color="#92400e">
              Some products have data quality issues. Review warnings in the admin panel.
            </mj-text>
          </mj-column>
        </mj-section>
        {% endif %}

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Feed URL:
        </mj-text>

        <mj-text font-size="13px" font-family="monospace" color="{{ theme.color.text_secondary|default:'#6b7280' }}" padding="10px" background-color="#f3f4f6">
          {{ feed_url }}
        </mj-text>

        <mj-spacer height="30px" />

        <mj-button href="{{ download_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          Download Feed
        </mj-button>

        <mj-spacer height="10px" />

        <mj-button href="{{ admin_feed_url }}" background-color="#6b7280" color="#ffffff" font-size="14px" border-radius="6px" padding="10px 25px">
          View in Admin
        </mj-button>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
✓ FEED GENERATO CON SUCCESSO

Product Feed Ready

Your {{ feed_name }} product feed has been successfully generated and is ready for use.

FEED DETAILS:
- Feed: {{ feed_name }}
- Format: {{ feed_format }}
- Products: {{ product_count }}
- Generated: {{ generated_at }}
- File Size: {{ file_size }}

{% if warnings_count > 0 %}
⚠️ {{ warnings_count }} WARNING{{ warnings_count|pluralize|upper }}:
Some products have data quality issues. Review warnings in the admin panel.
{% endif %}

FEED URL:
{{ feed_url }}

Download feed: {{ download_url }}
View in admin: {{ admin_feed_url }}