---
template_type: return_received
category: Returns
---

# Email Template: return_received

## Subject
Wir haben Ihre Rücksendung erhalten - Bestellung #{{ order_number }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="{{ theme.color.surface|default:'#eff6ff' }}">
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="{{ theme.color.primary|default:'#1d4ed8' }}">
          Rücksendung erhalten
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.primary|default:'#1d4ed8' }}">
          Bestellung #{{ order_number }}
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Hallo {{ customer_name }},
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Wir haben Ihre zurückgesendeten Artikel für die Bestellung <strong>#{{ order_number }}</strong> erhalten.
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          <strong>Was als nächstes passiert:</strong>
        </mj-text>

        <mj-text font-size="15px" line-height="1.8" color="{{ theme.color.text|default:'#4b5563' }}">
          1. Unser Team wird die zurückgesendeten Artikel innerhalb von 2-3 Werktagen prüfen<br/>
          2. Wir werden überprüfen, ob die Artikel in ihrem ursprünglichen Zustand sind<br/>
          3. Sobald die Prüfung abgeschlossen ist, werden wir Ihren Rückzahlungsbetrag verarbeiten<br/>
          4. Sie erhalten eine Bestätigungs-E-Mail, sobald die Rückzahlung verarbeitet wurde
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Die Rückzahlung wird auf Ihre ursprüngliche Zahlungsmethode gutgeschrieben und kann 5-10 Werktagen benötigen, um auf Ihrem Konto sichtbar zu werden.
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Vielen Dank für Ihre Geduld!
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
Rücksendung erhalten - Bestellung #{{ order_number }}

Hallo {{ customer_name }},

Wir haben Ihre zurückgesendeten Artikel für die Bestellung #{{ order_number }} erhalten.

Was als nächstes passiert:
1. Unser Team wird die zurückgesendeten Artikel innerhalb von 2-3 Werktagen prüfen
2. Wir werden überprüfen, ob die Artikel in ihrem ursprünglichen Zustand sind
3. Sobald die Prüfung abgeschlossen ist, werden wir Ihren Rückzahlungsbetrag verarbeiten
4. Sie erhalten eine Bestätigungs-E-Mail, sobald die Rückzahlung verarbeitet wurde

Die Rückzahlung wird auf Ihre ursprüngliche Zahlungsmethode gutgeschrieben und kann 5-10 Werktagen benötigen, um auf Ihrem Konto sichtbar zu werden.

Vielen Dank für Ihre Geduld!