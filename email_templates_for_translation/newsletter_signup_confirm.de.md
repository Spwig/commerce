---
template_type: newsletter_signup_confirm
category: Newsletter
---

# Email Template: newsletter_signup_confirm

## Subject
Bestätige deine Abonnements bei {{ store_name }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section>
      <mj-column>
        <mj-text font-size="22px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Abonnement bestätigen
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Danke, dass du dich bei {{ store_name }} angemeldet hast! Bitte bestätige deine E-Mail-Adresse, um unsere Updates und Angebote zu erhalten.
        </mj-text>

        <mj-spacer height="30px" />

        <mj-button href="{{ confirmation_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="18px" font-weight="bold" border-radius="6px" padding="18px 50px">
          Abonnement bestätigen
        </mj-button>

        <mj-spacer height="30px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="14px" color="{{ theme.color.text|default:'#4b5563' }}">
              Kannst du auf den Button klicken? Kopiere diesen Link in deinen Browser:
              <br/>
              <span style="color: {{ theme.color.primary|default:'#2563eb' }}; font-family: 'Courier New', monospace;">{{ confirmation_url }}</span>
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-size="14px" color="{{ theme.color.text_secondary|default:'#6b7280' }}">
          <strong>Warum bestätigen?</strong><br/>
          Die Bestätigung deiner E-Mail-Adresse hilft uns sicherzustellen, dass du unsere Updates wirklich willst, und hält deine E-Mails vor Spam schützt.
        </mj-text>

        <mj-spacer height="20px" />

        <mj-text font-size="13px" color="{{ theme.color.text_secondary|default:'#6b7280' }}" align="center">
          Hast du dich nicht angemeldet? Du kannst diese E-Mail sicher ignorieren.
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
Abonnement bestätigen bei {{ store_name }}

Danke, dass du dich bei {{ store_name }} angemeldet hast! Bitte bestätige deine E-Mail-Adresse, um unsere Updates und Angebote zu erhalten:

{{ confirmation_url }}

Die Bestätigung deiner E-Mail-Adresse hilft uns sicherzustellen, dass du unsere Updates wirklich willst, und hält deine E-Mails vor Spam schützt.

Hast du dich nicht angemeldet? Du kannst diese E-Mail sicher ignorieren.