---
template_type: component_update_available
category: Component Updates
---

# Email Template: component_update_available

## Subject
Update verfügbar: {{ component_name }} v{{ new_version }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#eff6ff">
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="#1e40af" align="center">
          📦 Update verfügbar
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="18px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Neue Version verfügbar
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}">
          Eine neue Version von {{ component_name }} ist für Ihr Spwig-Geschäft verfügbar.
        </mj-text>

        <mj-spacer height="20px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
              Update Details:
            </mj-text>
            <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>Komponente:</strong> {{ component_name }}<br/>
              <strong>Aktuelle Version:</strong> {{ current_version }}<br/>
              <strong>Neue Version:</strong> {{ new_version }}<br/>
              <strong>Veröffentlichungsdatum:</strong> {{ release_date }}
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Was ist neu:
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}" line-height="1.8">
          {{ changelog }}
        </mj-text>

        {% if breaking_changes %}
        <mj-spacer height="20px" />
        <mj-section background-color="#fef3c7" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="14px" color="#92400e" font-weight="bold">
              ⚠️ Breaking Changes
            </mj-text>
            <mj-text font-size="14px" color="#92400e" line-height="1.6">
              {{ breaking_changes }}
            </mj-text>
          </mj-column>
        </mj-section>
        {% endif %}

        <mj-spacer height="30px" />

        <mj-button href="{{ update_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          Update installieren
        </mj-button>

        <mj-spacer height="20px" />

        <mj-text font-size="14px" color="{{ theme.color.text_secondary|default:'#6b7280' }}" align="center">
          <a href="{{ changelog_url }}" style="color: {{ theme.color.primary|default:'#2563eb' }};">
            Vollen Changelog ansehen
          </a>
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
📦 UPDATE VERFÜGBAR

Neue Version verfügbar

Eine neue Version von {{ component_name }} ist für Ihr Spwig-Geschäft verfügbar.

UPDATE DETAILS:
- Komponente: {{ component_name }}
- Aktuelle Version: {{ current_version }}
- Neue Version: {{ new_version }}
- Veröffentlichungsdatum: {{ release_date }}

WHAT'S NEW:
{{ changelog }}

{% if breaking_changes %}
⚠️ BREAKING CHANGES:
{{ breaking_changes }}
{% endif %}

Install update: {{ update_url }}
View full changelog: {{ changelog_url }}