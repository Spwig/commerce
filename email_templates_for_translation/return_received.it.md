---
template_type: return_received
category: Returns
---

# Email Template: return_received

## Subject
Abbiamo ricevuto il tuo reso - Ordine #{{ order_number }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="{{ theme.color.surface|default:'#eff6ff' }}">
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="{{ theme.color.primary|default:'#1d4ed8' }}">
          Reso ricevuto
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.primary|default:'#1d4ed8' }}">
          Ordine #{{ order_number }}
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Ciao {{ customer_name }},
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Abbiamo ricevuto i prodotti restituiti per l'ordine <strong>#{{ order_number }}</strong>.
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          <strong>Cosa succede adesso:</strong>
        </mj-text>

        <mj-text font-size="15px" line-height="1.8" color="{{ theme.color.text|default:'#4b5563' }}">
          1. Il nostro team esaminerà i prodotti restituiti entro 2-3 giorni lavorativi<br/>
          2. Verificheremo che i prodotti siano nella loro condizione originale<br/>
          3. Una volta completata l'ispezione, procederemo al rimborso<br/>
          4. Riceverai una e-mail di conferma una volta che il rimborso sarà processato
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Il rimborso verrà accreditato sul metodo di pagamento originale e potrebbe richiedere 5-10 giorni lavorativi per apparire sul tuo account.
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Grazie per la tua pazienza!
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
Reso ricevuto - Ordine #{{ order_number }}

Ciao {{ customer_name }},

Abbiamo ricevuto i prodotti restituiti per l'ordine #{{ order_number }}.

Cosa succede adesso:
1. Il nostro team esaminerà i prodotti restituiti entro 2-3 giorni lavorativi
2. Verificheremo che i prodotti siano nella loro condizione originale
3. Una volta completata l'ispezione, procederemo al rimborso
4. Riceverai una e-mail di conferma una volta che il rimborso sarà processato

Il rimborso verrà accreditato sul metodo di pagamento originale e potrebbe richiedere 5-10 giorni lavorativi per apparire sul tuo account.

Grazie per la tua pazienza!