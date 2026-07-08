---
template_type: feed_generation_completed
category: Product Feeds
---

# Email Template: feed_generation_completed

## Subject
✓ Produkt-Feed generiert: {{ feed_name }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#dcfce7">
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="#065f46" align="center">
          ✓ Feed erfolgreich generiert
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="18px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Produkt-Feed bereit
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}">
          Ihr {{ feed_name }} Produkt-Feed wurde erfolgreich generiert und ist jetzt zum Verwenden bereit.
        </mj-text>

        <mj-spacer height="20px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
              Feed-Details:
            </mj-text>
            <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>Feed:</strong> {{ feed_name }}<br/>
              <strong>Format:</strong> {{ feed_format }}<br/>
              <strong>Produkte:</strong> {{ product_count }}<br/>
              <strong>Generiert:</strong> {{ generated_at }}<br/>
              <strong>Dateigröße:</strong> {{ file_size }}
            </mj-text>
          </mj-column>
        </mj-section>

        {% if warnings_count > 0 %}
        <mj-spacer height="20px" />
        <mj-section background-color="#fef3c7" border-radius="8px" padding="15px">
          <mj-column>
            <mj:text font-size="14px" color="#92400e" font-weight="bold">
              ⚠️ {{ warnings_count }} Warnung{{ warnings_count|pluralize }}
            </mj:text>
            <mj-text font-size="14px" color="#92400e">
              Einige Produkte haben Datenqualitätsprobleme. Überprüfen Sie die Warnungen in der Admin-Oberfläche.
            </mj-text>
          </mj-column>
        </mj-section>
        {% endif %}

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Feed-URL:
        </mj-text>

        <mj-text font-size="13px" font-family="monospace" color="{{ theme.color.text_secondary|default:'#6b7280' }}" padding="10px" background-color="#f3f4f6">
          {{ feed_url }}
        </mj-text>

        <mj-spacer height="30px" />

        <mj-button href="{{ download_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          Feed herunterladen
        </mj-button>

        <mj-spacer height="10px" />

        <mj-button href="{{ admin_feed_url }}" background-color="#6b7280" color="#ffffff" font-size="14px" border-radius="6px" padding="10px 25px">
          In Admin ansehen
        </mj-button>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
✓ FEED ERSTELLT

Produkt-Feed bereit

Ihr {{ feed_name }} Produkt-Feed wurde erfolgreich generiert und ist jetzt zum Verwenden bereit.

FEED-DETAILS:
- Feed: {{ feed_name }}
- Format: {{ feed_format }}
- Produkte: {{ product_count }}
- Generiert: {{ generated_at }}
- Dateigröße: {{ file_size }}

{% if warnings_count > 0 %}
⚠️ {{ warnings_count }} WARNGEBOTE{{ warnings_count|pluralize|upper }}:
Einige Produkte haben Datenqualitätsprobleme. Überprüfen Sie die Warnungen in der Admin-Oberfläche.
{% endif %}

FEED-URL:
{{ feed_url }}

Download feed: {{ download_url }}
View in admin: {{ admin_feed_url }}