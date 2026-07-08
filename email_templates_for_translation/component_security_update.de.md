---
template_type: component_security_update
category: Component Updates
---

# Email Template: component_security_update

## Subject
🔒 DRINGEND: Sicherheitsupdate für {{ component_name }} verfügbar

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#fee2e2">
      <mj-column>
        <mj-text font-size="22px" font-weight="bold" color="#991b1b" align="center">
          🔒 SICHERHEITSAKTUALISIERUNG ERWÄUTERT
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="18px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Kritische Sicherheitskorrektur
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Es wurde eine Sicherheitslücke in {{ component_name }} entdeckt. Bitte aktualisieren Sie sofort, um Ihren Store zu schüzen.
        </mj-text>

        <mj-spacer height="30px" />

        <mj-section background-color="#fee2e2" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="#991b1b" font-size="16px">
              ⚠️ Sicherheitsinformationen
            </mj-text>
            <mj-text color="#991b1b">
              <strong>Komponente:</strong> {{ component_name }}<br/>
              <strong>Aktuelle Version:</strong> {{ current_version }}<br/>
              <strong>Behandelte Version:</strong> {{ patched_version }}<br/>
              <strong>Schweregrad:</strong> {{ severity_level }}<br/>
              <strong>CVE-ID:</strong> {{ cve_id }}
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Sicherheitsdetails:
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}" line-height="1.8">
          {{ vulnerability_description }}
        </mj-text>

        <mj-spacer height="20px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Potenzieller Einfluss:
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}" line-height="1.8">
          {{ impact_description }}
        </mj-text>

        {% if mitigation_steps %}
        <mj-spacer height="30px" />
        <mj-section background-color="#fef3c7" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="14px" color="#92400e" font-weight="bold">
              Temporäre Abmilderung
            </mj-text>
            <mj-text font-size="14px" color="#92400e" line-height="1.6">
              {{ mitigation_steps }}
            </mj-text>
          </mj-column>
        </mj-section>
        {% endif %}

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}" align="center">
          Aktion erforderlich: Update sofort installieren
        </mj-text>

        <mj-spacer height="20px" />

        <mj-button href="{{ update_url }}" background-color="#dc2626" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          Sicherheitskorrektur installieren
        </mj-button>

        <mj-spacer height="10px" />

        <mj-button href="{{ advisory_url }}" background-color="#6b7280" color="#ffffff" font-size="14px" border-radius="6px" padding="10px 25px">
          Sicherheitsberatung lesen
        </mj-button>

        <mj-spacer height="30px" />

        <mj-text font-size="13px" color="{{ theme.color.text_secondary|default:'#6b7280' }}" align="center">
          Falls Sie Hilfe benötigen, kontaktieren Sie sofort den Spwig-Support.
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
🔒 SICHERHEITSAKTUALISIERUNG ERWÄUTERT

Kritische Sicherheitskorrektur

Es wurde eine Sicherheitslücke in {{ component_name }} entdeckt. Bitte aktualisieren Sie sofort, um Ihren Store zu schüzen.

⚠️ SICHERHEITSDATEN:
- Komponente: {{ component_name }}
- Aktuelle Version: {{ current_version }}
- Behandelte Version: {{ patched_version }}
- Schweregrad: {{ severity_level }}
- CVE-ID: {{ cve_id }}

SICHERHEITSDetails:
{{ vulnerability_description }}

POTENZIELLER EINFLUSS:
{{ impact_description }}

{% if mitigation_steps %}
TEMPORÄRE ABDIMMERUNG:
{{ mitigation_steps }}
{% endif %}

Aktion erforderlich: Update sofort installieren

Sicherheitskorrektur installieren: {{ update_url }}
Sicherheitsberatung lesen: {{ advisory_url }}

Falls Sie Hilfe benötigen, kontaktieren Sie sofort den Spwig-Support.