---
template_type: loyalty_referral_bonus
category: Loyalty Program
---

# Email Template: loyalty_referral_bonus

## Subject
🎁 Bonus-Punkte für die Weiterleitung von {{ referee_name }}!

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#dcfce7">
      <mj-column>
        <mj-text font-size="24px" font-weight="bold" color="#065f46" align="center">
          🎁 Bonuspunkte durch Weiterleitung erzielt!
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Vielen Dank für die Weiterleitung, {{ customer_name }}!
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Große Nachricht! {{ referee_name }} hat gerade unser Treueprogramm durch Ihre Weiterleitung beigetreten, und Sie haben Bonuspunkte verdient!
        </mj-text>

        <mj-spacer height="30px" />

        <mj-section background-color="#f0fdf4" border-radius="8px" padding="25px">
          <mj-column>
            <mj-text font-size="18px" font-weight="bold" color="#065f46" align="center">
              Sie haben verdient
            </mj-text>
            <mj-text font-size="36px" font-weight="bold" color="#047857" align="center">
              +{{ bonus_points }} Punkte
            </mj-text>
            <mj-text font-size="14px" color="#065f46" align="center">
              Durch Weiterleitung von {{ referee_name }}
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Ihr aktualisierter Saldo:
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}">
          <strong>Punkte-Saldo:</strong> {{ total_points }} Punkte<br/>
          <strong>Weiterleitungsbonus:</strong> +{{ bonus_points }} Punkte<br/>
          <strong>Freunde, die weitergeleitet wurden:</strong> {{ total_referrals }}
        </mj-text>

        <mj-spacer height="30px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
              Weitersenden und Punkte sammeln!
            </mj-text>
            <mj-text font-size="14px" color="{{ theme.color.text|default:'#4b5563' }}">
              Verdienen Sie {{ points_per_referral }} Punkte für jeden Freund, der beitritt. Es gibt keine Grenze!
            </mj-text>
            <mj-spacer height="15px" />
            <mj-button href="{{ referral_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="14px" border-radius="6px" padding="10px 25px">
              Teilen Sie Ihren Weiterleitungslink
            </mj-button>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-button href="{{ shop_url }}" background-color="#059669" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          Jetzt einkaufen
        </mj-button>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
🎁 Bonuspunkte durch Weiterleitung erzielt!

Vielen Dank für die Weiterleitung, {{ customer_name }}!

Große Nachricht! {{ referee_name }} hat gerade unser Treueprogramm durch Ihre Weiterleitung beigetreten, und Sie haben Bonuspunkte verdient!

SIE HABEN VERDIENST:
+{{ bonus_points }} Punkte
Durch Weiterleitung von {{ referee_name }}

IHR AKTUALISIERTER SALDO:
- Punkte-Saldo: {{ total_points }} Punkte
- Weiterleitungsbonus: +{{ bonus_points }} Punkte
- Freunde, die weitergeleitet wurden: {{ total_referrals }}

WEITERLEITEN UND PUNKTE SAMMELN!
Verdienen Sie {{ points_per_referral }} Punkte für jeden Freund, der beitritt. Es gibt keine Grenze!

Teilen Sie Ihren Weiterleitungslink: {{ referral_url }}
Starten Sie mit dem Einkaufen: {{ shop_url }}
