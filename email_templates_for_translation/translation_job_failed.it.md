---
template_type: translation_job_failed
category: Translation Service
---

# Email Template: translation_job_failed

## Subject
❌ Traduzione non riuscita: {{ content_type }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#fee2e2">
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="#991b1b" align="center">
          ❌ Traduzione non riuscita
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="18px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Errore di traduzione
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}">
          Il tuo lavoro di traduzione in blocco ha incontrato un errore e non è potuto essere completato.
        </mj-text>

        <mj-spacer height="20px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
              Dettagli del lavoro:
            </mj-text>
            <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>ID lavoro:</strong> {{ job_id }}<br/>
              <strong>Tipo contenuto:</strong> {{ content_type }}<br/>
              <strong>Lingue di destinazione:</strong> {{ target_languages }}<br/>
              <strong>Errore verificato a:</strong> {{ failed_at }}<br/>
              <strong>Codice errore:</strong> {{ error_code }}
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Messaggio di errore:
        </mj-text>

        <mj-section background-color="#fee2e2" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="14px" font-family="monospace" color="#991b1b" line-height="1.6">
              {{ error_message }}
            </mj-text>
          </mj-column>
        </mj-section>

        {% if partial_completion %}
        <mj-spacer height="30px" />
        <mj-section background-color="#fef3c7" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="14px" color="#92400e" font-weight="bold">
              Completamento parziale
            </mj-text>
            <mj-text font-size="14px" color="#92400e" line-height="1.6">
              {{ items_completed }} di {{ total_items }} elementi sono stati tradotti con successo prima che l'errore si verificasse.
            </mj-text>
          </mj-column>
        </mj-section>
        {% endif %}

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Cause comuni:
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}" line-height="1.8">
          • Problemi di connessione al servizio di traduzione API<br/>
          • Crediti di traduzione insufficienti<br/>
          • Contenuto sorgente non valido o danneggiato<br/>
          • Coppia di lingue non supportata
        </mj-text>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Azioni consigliate:
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}" line-height="1.8">
          1. Controlla le impostazioni del servizio di traduzione<br/>
          2. Verifica che siano disponibili crediti di traduzione<br/>
          3. Controlla il messaggio di errore per problemi specifici<br/>
          4. Riprova a eseguire il lavoro di traduzione
        </mj-text>

        <mj-spacer height="30px" />

        <mj-button href="{{ retry_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          Riprova traduzione
        </mj-button>

        <mj-spacer height="10px" />

        <mj-button href="{{ settings_url }}" background-color="#6b7280" color="#ffffff" font-size="14px" border-radius="6px" padding="10px 25px">
          Controlla le impostazioni
        </mj-button>

        <mj-spacer height="20px" />

        <mj-text font-size="13px" color="{{ theme.color.text_secondary|default:'#6b7280' }}" align="center">
          Se il problema persiste, contatta il supporto con il codice errore {{ error_code }}.
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
❌ LAVORO DI TRADUZIONE NON RISULTATO COMPLETATO

Errore di traduzione

Il tuo lavoro di traduzione in blocco ha incontrato un errore e non è potuto essere completato.

DETTAGLI DEL LAVORO:
- ID lavoro: {{ job_id }}
- Tipo contenuto: {{ content_type }}
- Lingue di destinazione: {{ target_languages }}
- Errore verificato a: {{ failed_at }}
- Codice errore: {{ error_code }}

MESSAGGIO DI ERRORE:
{{ error_message }}

{% if partial_completion %}
COMPLETAMENTO PARZIALE:
{{ items_completed }} di {{ total_items }} elementi sono stati tradotti con successo prima che l'errore si verificasse.
{% endif %}

CAUSE COMUNI:
• Problemi di connessione al servizio di traduzione API
• Crediti di traduzione insufficienti
• Contenuto sorgente non valido o danneggiato
• Coppia di lingue non supportata

AZIONI CONSIGLIATE:
1. Controlla le impostazioni del servizio di traduzione
2. Verifica che siano disponibili crediti di traduzione
3. Controlla il messaggio di errore per problemi specifici
4. Riprova a eseguire il lavoro di traduzione

Riprova traduzione: {{ retry_url }}
Controlla le impostazioni: {{ settings_url }}

Se il problema persiste, contatta il supporto con il codice errore {{ error_code }}.