---
template_type: loyalty_birthday_bonus
category: Loyalty Program
---

# Email Template: loyalty_birthday_bonus

## Subject
🎂 Buon compleanno {{ customer_name }}! Ecco un regalo speciale da {{ shop_name }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#fef3c7">
      <mj-column>
        <mj-text font-size="32px" align="center">🎂🎉🎁</mj-text>
        <mj-text font-size="26px" font-weight="bold" color="#92400e" align="center">
          Buon compleanno!
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Buon compleanno, {{ customer_name }}!
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Per celebrare il tuo giorno speciale, abbiamo aggiunto {{ bonus_points }} punti bonus al tuo account fedeltà!
        </mj-text>

        <mj-spacer height="30px" />

        <mj-section background-color="#dcfce7" border-radius="8px" padding="25px">
          <mj-column>
            <mj-text font-size="18px" font-weight="bold" color="#065f46" align="center">
              Il tuo regalo di compleanno
            </mj-text>
            <mj-text font-size="36px" font-weight="bold" color="#047857" align="center">
              {{ bonus_points }} Punti
            </mj-text>
            <mj-text font-size="14px" color="#065f46" align="center">
              Aggiunti al tuo account!
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Il tuo account fedeltà:
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}">
          <strong>Bilancio dei punti:</strong> {{ total_points }} punti<br/>
          <strong>Livello attuale:</strong> {{ loyalty_tier }}<br/>
          <strong>Bonus compleanno:</strong> +{{ bonus_points }} punti
        </mj-text>

        <mj-spacer height="30px" />

        <mj-button href="{{ shop_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="18px" font-weight="bold" border-radius="6px" padding="18px 50px">
          Inizia a fare acquisti e usa i tuoi punti
        </mj-button>

        <mj-spacer height="20px" />

        <mj-text font-size="14px" color="{{ theme.color.text_secondary|default:'#6b7280' }}" align="center">
          Buon compleanno! 🎉<br/>
          - Il team {{ shop_name }}
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
🎂🎉🎁 BUON COMPLEANNO!

Buon compleanno, {{ customer_name }}!

Per celebrare il tuo giorno speciale, abbiamo aggiunto {{ bonus_points }} punti bonus al tuo account fedeltà!

IL TUO REGALO DI COMPLEANNO:
{{ bonus_points }} Punti
Aggiunti al tuo account!

IL TUO ACCOUNT FEDELTÀ:
- Bilancio dei punti: {{ total_points }} punti
- Livello attuale: {{ loyalty_tier }}
- Bonus compleanno: +{{ bonus_points }} punti

Inizia a fare acquisti e usa i tuoi punti: {{ shop_url }}

Buon compleanno! 🎉
- Il team {{ shop_name }}