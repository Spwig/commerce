---
template_type: subscription_dunning_final_notice
category: Subscriptions
---

# Email Template: subscription_dunning_final_notice

## Subject
⚠️ ABSCHIEDSBELEGEN: Ihre Abonnement wird in {{ days_until_cancellation }} Tagen gekündigt

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#fee2e2">
      <mj-column>
        <mj-text font-size="22px" font-weight="bold" color="#991b1b" align="center">
          ⚠️ ABSCHIEDSBELEGEN
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="18px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Abonnement Kündigung bevorstehend
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Hi {{ customer_name }},
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Dies ist Ihre letzte Benachrichtigung. Wir konnten die Zahlung für Ihr {{ plan_name }}-Abonnement nicht verarbeiten. Wenn wir innerhalb von {{ days_until_cancellation }} Tagen keine Zahlung erhalten, wird Ihr Abonnement gekündigt.
        </mj-text>

        <mj-spacer height="30px" />

        <mj-section background-color="#fee2e2" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="#991b1b" font-size="16px">
              ⚠️ Zahlung fehlgeschlagen - Aktion erforderlich
            </mj-text>
            <mj-text color="#991b1b">
              <strong>Abonnement:</strong> {{ plan_name }}<br/>
              <strong>Zu zahlender Betrag:</strong> {{ amount_due }}<br/>
              <strong>Misslungen Versuche:</strong> {{ retry_count }}<br/>
              <strong>Letzte Versuch:</strong> {{ last_retry_date }}<br/>
              <strong>Kündigungsdatum:</strong> <span style="font-weight: bold; font-size: 16px;">{{ cancellation_date }}</span>
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Zahlung Fehler:
        </mj-text>

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="14px" font-family="monospace" color="{{ theme.color.text|default:'#4b5563' }}">
              {{ payment_error_message }}
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Was wird passieren:
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}" line-height="1.8">
          Wenn die Zahlung bis {{ cancellation_date }} nicht empfangen wird:<br/>
          • Ihr Abonnement wird gekündigt<br/>
          • Sie verlieren den Zugang zu allen Abonnement-Vorteilen<br/>
          • Ihre Daten können gelöscht werden (siehe Datenhaltungspolitik)<br/>
          • Sie müssen sich erneut abonnieren, um den Zugang wieder zu erhalten
        </mj-text>

        <mj-spacer height="30px" />

        <mj-text font-size="18px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}" align="center">
          Aktualisieren Sie jetzt Ihre Zahlungsmethode
        </mj-text>

        <mj-spacer height="20px" />

        <mj-button href="{{ update_payment_url }}" background-color="#dc2626" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          Zahlungsmethode aktualisieren
        </mj-button>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Häufige Probleme & Lösungen:
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}" line-height="1.8">
          • <strong>Abgelaufene Karte:</strong> Aktualisieren Sie mit einer aktuellen Kreditkarte<br/>
          • <strong>Unzureichende Mittel:</strong> Stellen Sie sicher, dass der Kontostand ausreichend ist<br/>
          • <strong>Karte abgelehnt:</strong> Kontaktieren Sie Ihre Bank oder verwenden Sie eine andere Karte<br/>
          • <strong>Adresse nicht übereinstimmt:</strong> Bestätigen Sie, dass die Rechnungsadresse mit der Karte übereinstimmt
        </mj-text>

        <mj-spacer height="30px" />

        <mj-section background-color="#eff6ff" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="14px" color="#1e40af" font-weight="bold">
              Benötigen Sie Hilfe?
            </mj-text>
            <mj-text font-size="14px" color="#1e40af" line-height="1.6">
              Wenn Sie Probleme mit der Zahlung haben oder Hilfe benötigen, wenden Sie sich bitte sofort an unser Support-Team.
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="20px" />

        <mj-button href="{{ support_url }}" background-color="#6b7280" color="#ffffff" font-size="14px" border-radius="6px" padding="10px 25px">
          Support kontaktieren
        </mj-button>

        <mj-spacer height="30px" />

        <mj-text font-size="13px" color="{{ theme.color.text_secondary|default:'#6b7280' }}" align="center">
          Wenn Sie Ihr Abonnement kündigen möchten, können Sie dies in Ihren Konto-Einstellungen tun.
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
⚠️ ABSCHIEDSBELEGEN

Abonnement Kündigung bevorstehend

Hi {{ customer_name }},

Dies ist Ihre letzte Benachrichtigung. Wir konnten die Zahlung für Ihr {{ plan_name }}-Abonnement nicht verarbeiten. Wenn wir innerhalb von {{ days_until_cancellation }} Tagen keine Zahlung erhalten, wird Ihr Abonnement gekündigt.

⚠️ ZAHLUNG FEHLGESCHLAGEN - AUFTRAG ERLEICHTERT:
- Abonnement: {{ plan_name }}
- Zu zahlender Betrag: {{ amount_due }}
- Misslungen Versuche: {{ retry_count }}
- Letzte Versuch: {{ last_retry_date }}
- Kündigungsdatum: {{ cancellation_date }}

ZAHLUNG FEHLER:
{{ payment_error_message }}

WAS WIRD PASSIEREN:
Wenn die Zahlung bis {{ cancellation_date }} nicht empfangen wird:
• Ihr Abonnement wird gekündigt
• Sie verlieren den Zugang zu allen Abonnement-Vorteilen
• Ihre Daten können gelöscht werden (siehe Datenhaltungspolitik)
• Sie müssen sich erneut abonnieren, um den Zugang wieder zu erhalten

AKTUALISIEREN SIE JETZT IHRE ZAHLUNGSWEISE

Häufige Probleme & Lösungen:
• Abgelaufene Karte: Aktualisieren Sie mit einer aktuellen Kreditkarte
• Unzureichende Mittel: Stellen Sie sicher, dass der Kontostand ausreichend ist
• Karte abgelehnt: Kontaktieren Sie Ihre Bank oder verwenden Sie eine andere Karte
• Adresse nicht übereinstimmt: Bestätigen Sie, dass die Rechnungsadresse mit der Karte übereinstimmt

BRAUCHEN SIE HILFE?
Wenn Sie Probleme mit der Zahlung haben oder Hilfe benötigen, wenden Sie sich bitte sofort an unser Support-Team.

Aktualisieren Sie Zahlungsmethode: {{ update_payment_url }}
Kontaktieren Sie Support: {{ support_url }}

Wenn Sie Ihr Abonnement kündigen möchten, können Sie dies in Ihren Konto-Einstellungen tun.