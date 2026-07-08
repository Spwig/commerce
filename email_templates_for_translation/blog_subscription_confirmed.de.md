---
template_type: blog_subscription_confirmed
category: Blog
---

# Email Template: blog_subscription_confirmed

## Subject
Bestätigen Sie Ihre Abonnement für {{ blog_name }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section>
      <mj-column>
        <mj-text font-size="22px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Bestätigen Sie Ihr Abonnement
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Hi {{ subscriber_name }},
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Vielen Dank, dass Sie sich für {{ blog_name }} angemeldet haben! Um Ihr Abonnement abzuschließen und die Updates zu erhalten, bestätigen Sie bitte Ihre E-Mail-Adresse.
        </mj-text>

        <mj-spacer height="30px" />

        <mj-button href="{{ confirmation_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="18px" font-weight="bold" border-radius="6px" padding="18px 50px">
          Abonnement bestätigen
        </mj-button>

        <mj-spacer height="30px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="14px" color="{{ theme.color.text|default:'#4b5563' }}">
              Kein Klick auf die Schaltfläche? Kopieren Sie diesen Link in Ihren Browser:<br/>
              <span style="color: {{ theme.color.primary|default:'#2563eb' }}; font-family: 'Courier New', monospace;">{{ confirmation_url }}</span>
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-size="14px" color="{{ theme.color.text_secondary|default:'#6b7280' }}">
          <strong>Warum bestätigen?</strong><br/>
          E-Mail-Bestätigung hilft uns dabei, sicherzustellen, dass Sie Updates erhalten möchten und verhindert Spam. Ihre Privatsphäre und Ihr Posteingang sind uns wichtig.
        </mj-text>

        <mj-spacer height="20px" />

        <mj-text font-size="13px" color="{{ theme.color.text_secondary|default:'#6b7280' }}" align="center">
          Nicht angemeldet? Sie können diese E-Mail sicher ignorieren.
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
ABONNEMENT BESTÄTIGEN

Hi {{ subscriber_name }},

Vielen Dank, dass Sie sich für {{ blog_name }} angemeldet haben! Um Ihr Abonnement abzuschließen und die Updates zu erhalten, bestätigen Sie bitte Ihre E-Mail-Adresse.

Bestätigen Sie Ihr Abonnement: {{ confirmation_url }}

WARUM BESTÄTIGEN?
E-Mail-Bestätigung hilft uns dabei, sicherzustellen, dass Sie Updates erhalten möchten und verhindert Spam. Ihre Privatsphäre und Ihr Posteingang sind uns wichtig.

Nicht angemeldet? Sie können diese E-Mail sicher ignorieren.