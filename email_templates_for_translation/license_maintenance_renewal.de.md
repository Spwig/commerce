---
template_type: license_maintenance_renewal
category: License
---

# Email Template: license_maintenance_renewal

## Subject
Wartung verlängert – Bestellung #{{ order_number }}

## HTML Content
<mjml>
  <mj-head>
    <mj-attributes>
      <mj-all font-family="'Helvetica Neue', Helvetica, Arial, sans-serif" />
      <mj-text font-size="14px" color="#333333" line-height="20px" />
      <mj-section background-color="{{ theme.color.background|default:'#ffffff' }}" padding="20px" />
    </mj-attributes>
  </mj-head>
  <mj-body background-color="{{ theme.color.background_secondary|default:'#f9fafb' }}">
    <!-- Header -->
    <mj-section background-color="{{ theme.color.success|default:'#10b981' }}" padding="30px 20px">
      <mj-column>
        <mj-text font-size="28px" font-weight="bold" color="#ffffff" align="center">
          Wartung verlängert!
        </mj-text>
        <mj-text font-size="16px" color="#ffffffcc" align="center" padding-top="10px">
          Bestellung #{{ order_number }}
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Greeting -->
    <mj-section>
      <mj-column>
        <mj-text font-size="16px">
          Hallo {{ customer_name }},
        </mj-text>
        <mj-text>
          Ihre Spwig-Wartungsbuchung wurde erfolgreich verlängert. Sie erhalten weiterhin Plattform-Updates, Sicherheitspatches und neue Funktionen.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Renewal Summary -->
    <mj-section background-color="{{ theme.color.background_secondary|default:'#f9fafb' }}" padding="20px" border-radius="8px">
      <mj-column>
        <mj-text font-size="16px" font-weight="bold" padding-bottom="10px">
          Verlängerungszusammenfassung
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          Lizenzschlüssel: {{ license_key }}
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          Wartung gültig bis: {{ renewal_expires_at }}
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          Bestellnummer: {{ order_number }}
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- What's Included -->
    <mj-section>
      <mj-column>
        <mj-text font-size="16px" font-weight="bold" padding-bottom="10px">
          Was ist enthalten
        </mj-text>
        <mj-text font-size="14px">
          Ihre aktive Wartung gewährt Ihnen Zugriff auf:
        </mj-text>
        <mj-text font-size="14px" padding-top="5px">
          - Plattformfunktionsupdates und Verbesserungen
        </mj-text>
        <mj-text font-size="14px">
          - Sicherheitspatches und Fehlerbehebungen
        </mj-text>
        <mj-text font-size="14px">
          - Neue Komponenten über den Upgrade-Server
        </mj-text>
        <mj-text font-size="14px">
          - Technischen Support
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Next Steps -->
    <mj-section>
      <mj-column>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          Keine Aktion ist von Ihrer Seite erforderlich. Updates werden weiterhin über das Komponenten-Update-System in Ihrem Admin-Panel verfügbar sein.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Support -->
    {% include 'email_system/mjml_components/support_block.mjml' %}
  </mj-body>
</mjml>

## Text Content
Wartung verlängert!

Bestellung #{{ order_number }}

Hallo {{ customer_name }},

Ihre Spwig-Wartungsbuchung wurde erfolgreich verlängert. Sie erhalten weiterhin Plattform-Updates, Sicherheitspatches und neue Funktionen.

Verlängerungszusammenfassung:
- Lizenzschlüssel: {{ license_key }}
- Wartung gültig bis: {{ renewal_expires_at }}
- Bestellnummer: {{ order_number }}

Was ist enthalten:
- Plattformfunktionsupdates und Verbesserungen
- Sicherheitspatches und Fehlerbehebungen
- Neue Komponenten über den Upgrade-Server
- Technischen Support

Keine Aktion ist von Ihrer Seite erforderlich. Updates werden weiterhin über das Komponenten-Update-System in Ihrem Admin-Panel verfügbar sein.

Benötigen Sie Hilfe? Kontaktieren Sie {{ support_email }}