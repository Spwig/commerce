---
template_type: referral_reward_expiring
category: Referral Program
---

# Email Template: referral_reward_expiring

## Subject
Ricordo: Il tuo premio {{ reward_amount }} scadrà presto

## HTML Content
<mjml>
  <mj-head>
    <mj-attributes>
      <mj-text font-family="Arial, sans-serif" line-height="1.6" />
      <mj-all font-family="Arial, sans-serif" />
    </mj-attributes>
  </mj-head>
  <mj-body background-color="{{ theme.color.background_secondaryondary|default:'#f9fafb' }}">
    <!-- Header -->
    <mj-section background-color="{{ theme.color.background|default:'#ffffff' }}" padding="40px 20px">
      <mj-column>
        <mj-text font-size="32px" font-weight="bold" color="{{ theme.color.error|default:'#ef4444' }}" align="center">
          ⏰ Premio che scade presto
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Warning Banner -->
    <mj-section background-color="{{ theme.color.warning_light|default:'#fef3c7' }}" padding="40px 20px">
      <mj-column>
        <mj-text font-size="48px" font-weight="bold" color="#856404" align="center" line-height="1">
          {{ reward_amount }}
        </mj-text>
        <mj-text font-size="18px" color="#856404" align="center" padding-top="10px">
          scadrà in {{ days_until_expiration }} giorni
        </mj-text>
        <mj-text font-size="14px" color="#856404" align="center" padding-top="5px">
          Data di scadenza: {{ expiration_date }}
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Content -->
    <mj-section background-color="{{ theme.color.background|default:'#ffffff' }}" padding="20px">
      <mj-column>
        <mj-text font-size="16px" color="{{ theme.color.text|default:'#1f2937' }}">
          Ciao {{ customer_name }},
        </mj-text>
        <mj-text font-size="16px" color="{{ theme.color.text|default:'#1f2937' }}">
          Non lasciare che il tuo premio di referenza {{ reward_amount }} vada perduto! Scadrà in {{ days_until_expiration }} giorni.
        </mj-text>
        <mj-text font-size="16px" color="{{ theme.color.text|default:'#1f2937' }}">
          Usa il premio ora sul tuo prossimo acquisto prima che sia troppo tardi!
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Reward Details -->
    <mj-section background-color="{{ theme.color.background_secondaryondary|default:'#f9fafb' }}" padding="30px 20px">
      <mj-column>
        <mj-text font-size="16px" color="{{ theme.color.text|default:'#1f2937' }}">
          <strong>Tipo di premio:</strong> {{ reward_type_display }}<br/>
          <strong>Importo:</strong> {{ reward_amount }}<br/>
          <strong>Scade:</strong> {{ expiration_date }}
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- CTA -->
    <mj-section background-color="{{ theme.color.background|default:'#ffffff' }}" padding="30px 20px">
      <mj-column>
        <mj-button background-color="{{ theme.color.error|default:'#ef4444' }}" color="{{ theme.color.background|default:'#ffffff' }}" href="{{ shop_url }}">
          Acquista Ora
        </mj-button>
      </mj-column>
    </mj-section>

    <!-- Footer -->
    <mj-section background-color="{{ theme.color.background_secondaryondary|default:'#f9fafb' }}" padding="20px">
      <mj-column>
        <mj-text font-size="12px" color="{{ theme.color.text_muted|default:'#6b7280' }}" align="center">
          {{ shop_name }}<br/>
          Hai domande? <a href="mailto:{{ support_email }}" style="color: {{ theme.color.primary|default:'#2563eb' }};">Contatta il supporto</a>
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
Ricordo: Il tuo premio {{ reward_amount }} scadrà presto

Ciao {{ customer_name }},

Non lasciare che il tuo premio di referenza {{ reward_amount }} vada perduto! Scadrà in {{ days_until_expiration }} giorni.

Dettagli del premio:
- Tipo: {{ reward_type_display }}
- Importo: {{ reward_amount }}
- Scade: {{ expiration_date }}

Usalo ora sul tuo prossimo acquisto prima che sia troppo tardi!

Acquista ora: {{ shop_url }}

{{ shop_name }}
Hai domande? Contatta {{ support_email }}