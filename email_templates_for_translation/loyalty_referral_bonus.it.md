---
template_type: loyalty_referral_bonus
category: Loyalty Program
---

# Email Template: loyalty_referral_bonus

## Subject
🎁 Bonus Punti per il Riferimento di {{ referee_name }}!

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#dcfce7">
      <mj-column>
        <mj-text font-size="24px" font-weight="bold" color="#065f46" align="center">
          🎁 Bonus di Riferimento Guadagnato!
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Grazie per il Condivisione, {{ customer_name }}!
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Grande notizia! {{ referee_name }} appena si è unito al nostro programma fedeltà tramite il tuo riferimento, e hai guadagnato punti bonus!
        </mj-text>

        <mj-spacer height="30px" />

        <mj-section background-color="#f0fdf4" border-radius="8px" padding="25px">
          <mj-column>
            <mj-text font-size="18px" font-weight="bold" color="#065f46" align="center">
              Hai Guadagnato
            </mj-text>
            <mj-text font-size="36px" font-weight="bold" color="#047857" align="center">
              +{{ bonus_points }} Punti
            </mj-text>
            <mj-text font-size="14px" color="#065f46" align="center">
              Per riferire {{ referee_name }}
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Il Vostro Bilancio Aggiornato:
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}">
          <strong>Bilancio dei Punti:</strong> {{ total_points }} punti<br/>
          <strong>Bonus di Riferimento:</strong> +{{ bonus_points }} punti<br/>
          <strong>Amici Riferiti:</strong> {{ total_referrals }}
        </mj-text>

        <mj-spacer height="30px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
              Continua a Condividere, Continua a Guadagnare!
            </mj-text>
            <mj-text font-size="14px" color="{{ theme.color.text|default:'#4b5563' }}">
              Guadagna {{ points_per_referral }} punti per ogni amico che si unisce. Non c'è limite!
            </mj-text>
            <mj-spacer height="15px" />
            <mj-button href="{{ referral_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="14px" border-radius="6px" padding="10px 25px">
              Condividi il Tuo Link di Riferimento
            </mj-button>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-button href="{{ shop_url }}" background-color="#059669" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          Inizia a Sfoggiare
        </mj-button>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
🎁 BONUS DI RIFERIMENTO GUADAGNATO!

Grazie per il Condivisione, {{ customer_name }}!

Grande notizia! {{ referee_name }} appena si è unito al nostro programma fedeltà tramite il tuo riferimento, e hai guadagnato punti bonus!

HAI GUADAGNATO:
+{{ bonus_points }} Punti
Per riferire {{ referee_name }}

IL VOSTRO BILANCIO AGGIORNATO:
- Bilancio dei Punti: {{ total_points }} punti
- Bonus di Riferimento: +{{ bonus_points }} punti
- Amici Riferiti: {{ total_referrals }}

CONTINUA A CONDIVIDERE, CONTINUA A GUADAGNARE!
Guadagna {{ points_per_referral }} punti per ogni amico che si unisce. Non c'è limite!

Condividi il tuo link di riferimento: {{ referral_url }}
Inizia a sfoggiare: {{ shop_url }}