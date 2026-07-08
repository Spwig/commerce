---
template_type: feed_validation_errors
category: Product Feeds
---

# Email Template: feed_validation_errors

## Subject
⚠️ {{ feed_name }}: {{ error_count }} Validierungsfehler gefunden

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#fef3c7">
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="#92400e" align="center">
          ⚠️ Feed-Validierungsfehler
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="18px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Probleme mit Datenqualität erkannt
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}">
          {{ error_count }} Validierungsfehler gefunden in {{ feed_name }}. Diese Probleme können verhindern, dass Produkte auf {{ platform_name }} erscheinen.
        </mj-text>

        <mj-spacer height="20px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
              Validierungszusammenfassung:
            </mj-text>
            <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>Feed:</strong> {{ feed_name }}<br/>
              <strong>Plattform:</strong> {{ platform_name }}<br/>
              <strong>Validiert:</strong> {{ validated_at }}<br/>
              <strong>Gesamte Produkte:</strong> {{ total_products }}<br/>
              <strong>Produkte mit Fehlern:</strong> {{ affected_products }}
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Wichtige Fehler:
        </mj-text>

        {% for error in top_errors %}
        <mj-section background-color="#fee2e2" border-radius="8px" padding="12px">
          <mj-column>
            <mj-text font-size="14px" color="#991b1b" font-weight="bold">
              {{ error.type }}
            </mj-text>
            <mj-text font-size="13px" color="#991b1b">
              {{ error.count }} Produkt{{ error.count|pluralize }} betroffen: {{ error.message }}
            </mj-text>
          </mj-column>
        </mj-section>
        <mj-spacer height="8px" />
        {% endfor %}

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Was zu beheben ist:
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}" line-height="1.8">
          {{ fix_instructions }}
        </mj-text>

        <mj-spacer height="30px" />

        <mj-button href="{{ errors_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          Alle Fehler ansehen
        </mj-button>

        <mj-spacer height="10px" />

        <mj-button href="{{ admin_feed_url }}" background-color="#6b7280" color="#ffffff" font-size="14px" border-radius="6px" padding="10px 25px">
          Feed verwalten
        </mj-button>

        <mj-spacer height="20px" />

        <mj-text font-size="13px" color="{{ theme.color.text_secondary|default:'#6b7280' }}" align="center">
          Beheben Sie diese Fehler, um sicherzustellen, dass alle Produkte auf {{ platform_name }} angezeigt werden.
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
⚠️ FEED-VALIDIERUNGSFehler

Probleme mit Datenqualität erkannt

{{ error_count }} Validierungsfehler gefunden in {{ feed_name }}. Diese Probleme können verhindern, dass Produkte auf {{ platform_name }} erscheinen.

VALIDIERUNGSSUMMARY:
- Feed: {{ feed_name }}
- Plattform: {{ platform_name }}
- Validiert: {{ validated_at }}
- Gesamte Produkte: {{ total_products }}
- Produkte mit Fehlern: {{ affected_products }}

TOP FEHLER:
{% for error in top_errors %}
{{ error.type }}: {{ error.count }} Produkt{{ error.count|pluralize }} - {{ error.message }}
{% endfor %}

WAS ZU BEHEBEN IST:
{{ fix_instructions }}

Alle Fehler ansehen: {{ errors_url }}
Feed verwalten: {{ admin_feed_url }}

Beheben Sie diese Fehler, um sicherzustellen, dass alle Produkte auf {{ platform_name }} angezeigt werden.