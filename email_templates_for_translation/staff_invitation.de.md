---
template_type: staff_invitation
category: Core E-commerce
---

# Email Template: staff_invitation

## Subject
Sie wurden zur Teilnahme an {{ store_name }} eingeladen

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
    <mj-section background-color="{{ theme.color.primary|default:'#2563eb' }}" padding="30px 20px">
      <mj-column>
        <mj-text font-size="28px" font-weight="bold" color="#ffffff" align="center">
          Staff Invitation
        </mj-text>
        <mj-text font-size="16px" color="#ffffffcc" align="center" padding-top="10px">
          Sie wurden zur Teilnahme an {{ store_name }} eingeladen
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Greeting -->
    <mj-section>
      <mj-column>
        <mj-text font-size="16px">
          Hi {{ first_name }},
        </mj-text>
        <mj-text>
          {{ invited_by }} hat Sie zur Teilnahme an <strong>{{ store_name }}</strong> als Mitarbeiter eingeladen. Sie können die Store-Verwaltung über das Admin-Dashboard übernehmen.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- CTA Button -->
    {% include 'email_system/mjml_components/cta_button.mjml' with url=invitation_url text="Accept Invitation" %}

    <!-- Expiry Note -->
    <mj-section>
      <mj-column>
        <mj-text font-size="12px" color="{{ theme.color.text_muted|default:'#6b7280' }}" align="center">
          Diese Einladung läuft am {{ expires_at|date:"N j, Y" }} ab. Wenn Sie diese Einladung nicht erwartet haben, können Sie diese E-Mail sicher ignorieren.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Support -->
    {% include 'email_system/mjml_components/support_block.mjml' %}
  </mj-body>
</mjml>

## Text Content
Sie wurden zur Teilnahme an {{ store_name }} eingeladen

Hi {{ first_name }},

{{ invited_by }} hat Sie zur Teilnahme an {{ store_name }} als Mitarbeiter eingeladen. Sie können die Store-Verwaltung über das Admin-Dashboard übernehmen.

Akzeptieren Sie die Einladung: {{ invitation_url }}

Diese Einladung läuft am {{ expires_at|date:"N j, Y" }} ab. Wenn Sie diese Einladung nicht erwartet haben, können Sie diese E-Mail sicher ignorieren.

Benötigen Sie Hilfe? Kontaktieren Sie {{ support_email }}