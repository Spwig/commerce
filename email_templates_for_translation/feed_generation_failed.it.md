---
template_type: feed_generation_failed
category: Product Feeds
---

# Email Template: feed_generation_failed

## Subject
❌ Generazione feed non riuscita: {{ feed_name }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#fee2e2">
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="#991b1b" align="center">
          ❌ Generazione Feed Non Riuscita
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="18px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Errore di Generazione
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}">
          Il feed dei prodotti {{ feed_name }} non è riuscito a generarsi a causa di un errore.
        </mj-text>

        <mj-spacer height="20px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
              Dettagli dell'Errore:
            </mj-text>
            <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>Feed:</strong> {{ feed_name }}<br/>
              <strong>Failed At:</strong> {{ failed_at }}<br/>
              <strong>Codice Errore:</strong> {{ error_code }}
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Messaggio di Errore:
        </mj-text>

        <mj-section background-color="#fee2e2" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="14px" font-family="monospace" color="#991b1b" line-height="1.6">
              {{ error_message }}
            </mj-text>
          </mj-column>
        </mj-section>

        {% if error_log %}
        <mj-spacer height="20px" />
        <mj-text font-size="14px" color="{{ theme.color.text_secondary|default:'#6b7280' }}">
          <strong>Registro degli Errori:</strong><br/>
          <code style="font-size: 12px; color: #6b7280;">
            {{ error_log|truncatewords:30 }}
          </code>
        </mj-text>
        {% endif %}

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Cause Comuni:
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}" line-height="1.8">
          • Dati del prodotto mancanti (titolo, prezzo, immagine)<br/>
          • Formato dei dati del prodotto non valido<br/>
          • Problemi di connessione al database<br/>
          • Spazio del disco o memoria insufficienti
        </mj-text>

        <mj-spacer height="30px" />

        <mj-button href="{{ retry_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          Riprova Generazione
        </mj-button>

        <mj-spacer height="10px" />

        <mj-button href="{{ admin_feed_url }}" background-color="#6b7280" color="#ffffff" font-size="14px" border-radius="6px" padding="10px 25px">
          Visualizza Impostazioni Feed
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
❌ GENERAZIONE FEED NON RIUSCITA

Errore di Generazione

Il feed dei prodotti {{ feed_name }} non è riuscito a generarsi a causa di un errore.

DETTAGLI DELL'ERRORE:
- Feed: {{ feed_name }}
- Failed At: {{ failed_at }}
- Codice Errore: {{ error_code }}

MESSAGGIO DI ERRORE:
{{ error_message }}

{% if error_log %}
REGISTRO DEGLI ERRORI:
{{ error_log|truncatewords:30 }}
{% endif %}

CAUSE COMUNI:
• Dati del prodotto mancanti (titolo, prezzo, immagine)
• Formato dei dati del prodotto non valido
• Problemi di connessione al database
• Spazio del disco o memoria insufficienti

Riprova generazione: {{ retry_url }}
Visualizza impostazioni feed: {{ admin_feed_url }}

Se il problema persiste, contatta il supporto con il codice errore {{ error_code }}.