---
template_type: subscription_dunning_final_notice
category: Subscriptions
---

# Email Template: subscription_dunning_final_notice

## Subject
⚠️ AVVISO FINALE: La tua sottoscrizione verrà cancellata in {{ days_until_cancellation }} giorni

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#fee2e2">
      <mj-column>
        <mj-text font-size="22px" font-weight="bold" color="#991b1b" align="center">
          ⚠️ AVVISO FINALE
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="18px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Imminente Cancellazione della Sottoscrizione
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Ciao {{ customer_name }},
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Questo è il tuo avviso finale. Non siamo riusciti a processare il pagamento per la tua sottoscrizione {{ plan_name }}. Se non riceveremo il pagamento entro {{ days_until_cancellation }} giorni, la tua sottoscrizione verrà cancellata.
        </mj-text>

        <mj-spacer height="30px" />

        <mj-section background-color="#fee2e2" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="#991b1b" font-size="16px">
              ⚠️ Pagamento fallito - Azione richiesta
            </mj-text>
            <mj-text color="#991b1b">
              <strong>Sottoscrizione:</strong> {{ plan_name }}<br/>
              <strong>Importo dovuto:</strong> {{ amount_due }}<br/>
              <strong>Attempi falliti:</strong> {{ retry_count }}<br/>
              <strong>Ultimo tentativo:</strong> {{ last_retry_date }}<br/>
              <strong>Data di cancellazione:</strong> <span style="font-weight: bold; font-size: 16px;">{{ cancellation_date }}</span>
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Errore di Pagamento:
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
          Cosa accadrà:
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}" line-height="1.8">
          Se il pagamento non verrà ricevuto entro {{ cancellation_date }}:<br/>
          • La tua sottoscrizione verrà cancellata<br/>
          • Perderai l'accesso a tutti i vantaggi della sottoscrizione<br/>
          • I tuoi dati potrebbero essere eliminati (vedi politica di conservazione)<br/>
          • Dovrai riascriverti per ripristinare l'accesso
        </mj-text>

        <mj-spacer height="30px" />

        <mj-text font-size="18px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}" align="center">
          Aggiorna immediatamente il tuo metodo di pagamento
        </mj-text>

        <mj-spacer height="20px" />

        <mj-button href="{{ update_payment_url }}" background-color="#dc2626" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          Aggiorna metodo di pagamento
        </mj-button>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Problemi comuni e soluzioni:
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}" line-height="1.8">
          • <strong>Tarjeta scaduta:</strong> Aggiorna con una carta di credito attuale<br/>
          • <strong>Fondi insufficienti:</strong> Assicurati che il saldo sia sufficiente<br/>
          • <strong>Tarjeta rifiutata:</strong> Contatta la tua banca o usa una diversa carta<br/>
          • <strong>Mismatch dell'indirizzo:</strong> Verifica che l'indirizzo di fatturazione corrisponda alla carta
        </mj-text>

        <mj-spacer height="30px" />

        <mj-section background-color="#eff6ff" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="14px" color="#1e40af" font-weight="bold">
              Hai bisogno di aiuto?
            </mj-text>
            <mj-text font-size="14px" color="#1e40af" line-height="1.6">
              Se stai riscontrando problemi di pagamento o hai bisogno di assistenza, per favore contatta immediatamente il nostro team di supporto.
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="20px" />

        <mj-button href="{{ support_url }}" background-color="#6b7280" color="#ffffff" font-size="14px" border-radius="6px" padding="10px 25px">
          Contatta il supporto
        </mj-button>

        <mj-spacer height="30px" />

        <mj-text font-size="13px" color="{{ theme.color.text_secondary|default:'#6b7280' }}" align="center">
          Se desideri cancellare la tua sottoscrizione, puoi farlo nelle impostazioni del tuo account.
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
⚠️ AVVISO FINALE

Imminente Cancellazione della Sottoscrizione

Ciao {{ customer_name }},

Questo è il tuo avviso finale. Non siamo riusciti a processare il pagamento per la tua sottoscrizione {{ plan_name }}. Se non riceveremo il pagamento entro {{ days_until_cancellation }} giorni, la tua sottoscrizione verrà cancellata.

⚠️ PAGAMENTO FALLITO - AZIONE RICHIESTA:
- Sottoscrizione: {{ plan_name }}
- Importo Dovuto: {{ amount_due }}
- Attempi Falliti: {{ retry_count }}
- Ultimo Tentativo: {{ last_retry_date }}
- Data di Cancellazione: {{ cancellation_date }}

ERRORE DI PAGAMENTO:
{{ payment_error_message }}

COSA ACCADRÀ:
Se il pagamento non verrà ricevuto entro {{ cancellation_date }}:
• La tua sottoscrizione verrà cancellata
• Perderai l'accesso a tutti i vantaggi della sottoscrizione
• I tuoi dati potrebbero essere eliminati (vedi politica di conservazione)
• Dovrai riascriverti per ripristinare l'accesso

AGGIORNA IL TUO METODO DI PAGAMENTO ORA

Problemi comuni e soluzioni:
• Carta scaduta: Aggiorna con una carta di credito attuale
• Fondi insufficienti: Assicurati che il saldo sia sufficiente
• Carta rifiutata: Contatta la tua banca o usa una diversa carta
• Mismatch dell'indirizzo: Verifica che l'indirizzo di fatturazione corrisponda alla carta

HAI BISOGNO DI AIUTO?
Se stai riscontrando problemi di pagamento o hai bisogno di assistenza, per favore contatta immediatamente il nostro team di supporto.

Aggiorna metodo di pagamento: {{ update_payment_url }}
Contatta supporto: {{ support_url }}

Se desideri cancellare la tua sottoscrizione, puoi farlo nelle impostazioni del tuo account.