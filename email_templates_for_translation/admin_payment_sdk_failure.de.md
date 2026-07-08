---
template_type: admin_payment_sdk_failure
category: Admin Notifications
---

# Email Template: admin_payment_sdk_failure

## Subject
Problem mit Zahlungsdienstleister - SDK von {{ provider_name }} konnte nicht geladen werden

## HTML Content
<mjml>
  <mj-body>
    <mj-section>
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="{{ theme.color.warning|default:'#f59e0b' }}">
          Problem mit Zahlungsdienstleister
        </mj-text>
        <mj-text>
          Das Zahlungssystem (SDK) von {{ provider_name }} konnte nicht geladen werden, während ein Kunde am Checkout war. Dies kann darauf hindeuten, dass es zu einem Dienstunterbrechung beim Anbieter gekommen ist.
        </mj-text>
        <mj-text>
          <strong>Anbieter:</strong> {{ provider_name }}
        </mj-text>
        <mj-text>
          <strong>Fehlerart:</strong> {{ error_type }}
        </mj-text>
        <mj-text>
          <strong>Zeit:</strong> {{ timestamp }}
        </mj-text>
        <mj-text>
          <strong>Fehleranzahl (letzte Stunde):</strong> {{ failure_count }}
        </mj-text>
        <mj-divider border-color="{{ theme.color.border|default:'#e5e7eb' }}" />
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          Diese Benachrichtigung ist auf eine pro Anbieter pro Stunde begrenzt. Falls das Problem weiterhin besteht, prüfen Sie das Dashboard des Anbieters oder kontaktieren Sie deren Support.
        </mj-text>
        <mj-button href="{{ admin_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}">
          Zahlungseinstellungen ansehen
        </mj-button>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
Problem mit Zahlungsdienstleister

Das Zahlungssystem (SDK) von {{ provider_name }} konnte nicht geladen werden, während ein Kunde am Checkout war. Dies kann darauf hindeuten, dass es zu einer Dienstunterbrechung beim Anbieter gekommen ist.

Anbieter: {{ provider_name }}
Fehlerart: {{ error_type }}
Zeit: {{ timestamp }}
Fehleranzahl (letzte Stunde): {{ failure_count }}

Diese Benachrichtigung ist auf eine pro Anbieter pro Stunde begrenzt. Falls das Problem weiterhin besteht, prüfen Sie das Dashboard des Anbieters oder kontaktieren Sie deren Support.

Zahlungseinstellungen ansehen: {{ admin_url }}