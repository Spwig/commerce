---
template_type: license_trial_welcome
category: License
---

# Email Template: license_trial_welcome

## Subject
Willkommen bei Spwig - Ihr {{ trial_days }}-Tage Probetrial

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
    <mj-section background-color="#059669" padding="30px 20px">
      <mj-column>
        <mj-text font-size="28px" font-weight="bold" color="#ffffff" align="center">
          Willkommen bei Spwig!
        </mj-text>
        <mj-text font-size="16px" color="#ffffffcc" align="center" padding-top="10px">
          Ihr {{ trial_days }}-Tage Probetrial ist bereit
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
          Vielen Dank, dass Sie {{ product_name }} ausprobieren! Ihr Probetrial wurde aktiviert und Sie haben {{ trial_days }} Tage, um alles zu erkunden, was Spwig zu bieten hat{% if includes_pos %}, einschließlich unseres Point of Sale-Systems{% endif %}.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Setup Token Box -->
    <mj-section background-color="#f0fdf4" padding="25px" border-radius="8px">
      <mj-column>
        <mj-text font-size="12px" color="#065f46" font-weight="bold" align="center">
          IHR SETUP-TOKEN
        </mj-text>
        <mj-text font-size="14px" font-weight="bold" color="#059669" align="center" font-family="'Courier New', monospace" padding="10px 0" word-break="break-all">
          {{ setup_token }}
        </mj-text>
        <mj-text font-size="12px" color="{{ theme.color.text_muted|default:'#6b7280' }}" align="center">
          Verwenden Sie dieses Token während der Installation, um Ihr Probentoken zu aktivieren
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Getting Started -->
    <mj-section>
      <mj-column>
        <mj-text font-size="16px" font-weight="bold" padding-bottom="10px">
          Getting Started
        </mj-text>
        <mj-text font-size="14px">
          1. Folgen Sie unserem Setup-Leitfaden, um Spwig auf Ihrem Server zu installieren
        </mj-text>
        <mj-text font-size="14px">
          2. Geben Sie Ihr Setup-Token ein, wenn Sie während der Installation aufgefordert werden
        </mj-text>
        <mj-text font-size="14px">
          3. Beginnen Sie mit der Erstellung Ihres Online-Shops!
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Setup Guide CTA -->
    {% include 'email_system/mjml_components/cta_button.mjml' with url=setup_url text="View Setup Guide" %}

    <!-- What's Included -->
    <mj-section background-color="{{ theme.color.background_secondary|default:'#f9fafb' }}" padding="20px" border-radius="8px">
      <mj-column>
        <mj-text font-size="16px" font-weight="bold" padding-bottom="10px">
          Was ist in Ihrem Probetrial enthalten
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          Vollständiger Zugriff auf alle Kernfunktionen für {{ trial_days }} Tage
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          Produktkatalog, Bestellungen und Kundenverwaltung
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          Theme-Anpassung und Seiten-Builder
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          Zahlungs- und Versanddienstanbieter-Integrationen
        </mj-text>
        {% if includes_pos %}
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          Point of Sale (POS)-System
        </mj-text>
        {% endif %}
      </mj-column>
    </mj-section>

    <!-- Trial Info -->
    <mj-section>
      <mj-column>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          Ihr Probetrial läuft in {{ trial_days }} Tagen ab. Wenn Sie bereit sind, können Sie auf eine Vollversion upgraden, um Ihren Shop weiterhin ohne Datenverlust zu betreiben.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Support -->
    {% include 'email_system/mjml_components/support_block.mjml' %}
  </mj-body>
</mjml>

## Text Content
Willkommen bei Spwig!
Ihr {{ trial_days }}-Tage Probetrial ist bereit.

Hallo {{ customer_name }},

Vielen Dank, dass Sie {{ product_name }} ausprobieren! Ihr Probetrial wurde aktiviert und Sie haben {{ trial_days }} Tage, um alles zu erkunden, was Spwig zu bieten hat{% if includes_pos %}, einschließlich unseres Point of Sale-Systems{% endif %}.

IHR SETUP-TOKEN:
{{ setup_token }}
Verwenden Sie dieses Token während der Installation, um Ihr Probentoken zu aktivieren.

Getting Started:
1. Folgen Sie unserem Setup-Leitfaden, um Spwig auf Ihrem Server zu installieren
2. Geben Sie Ihr Setup-Token ein, wenn Sie während der Installation aufgefordert werden
3. Beginnen Sie mit der Erstellung Ihres Online-Shops!

View Setup Guide: {{ setup_url }}

Was ist in Ihrem Probetrial enthalten:
- Vollständiger Zugriff auf alle Kernfunktionen für {{ trial_days }} Tage
- Produktkatalog, Bestellungen und Kundenverwaltung
- Theme-Anpassung und Seiten-Builder
- Zahlungs- und Versanddienstanbieter-Integrationen
{% if includes_pos %}- Point of Sale (POS)-System{% endif %}

Ihr Probetrial läuft in {{ trial_days }} Tagen ab. Wenn Sie bereit sind, können Sie auf eine Vollversion upgraden, um Ihren Shop weiterhin ohne Datenverlust zu betreiben.

Need help? Kontaktieren Sie {{ support_email }}