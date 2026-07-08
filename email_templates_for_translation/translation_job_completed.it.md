---
template_type: translation_job_completed
category: Translation Service
---

# Email Template: translation_job_completed

## Subject
✓ Traduzione completata: {{ content_type }} ({{ language_count }} lingue)

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#dcfce7">
      <mj-column>
        <mj-text font-size="24px" font-weight="bold" color="#065f46" align="center">
          ✓ Traduzione completata!
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Le tue traduzioni sono pronte
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Buone notizie! Il tuo lavoro di traduzione di massa è stato completato con successo.
        </mj-text>

        <mj-spacer height="30px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
              Riepilogo lavoro:
            </mj-text>
            <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>ID lavoro:</strong> {{ job_id }}<br/>
              <strong>Tipo di contenuto:</strong> {{ content_type }}<br/>
              <strong>Lingue:</strong> {{ target_languages }}<br/>
              <strong>Oggetti tradotti:</strong> {{ items_translated }}<br/>
              <strong>Parole totali:</strong> {{ word_count }}<br/>
              <strong>Completato:</strong> {{ completed_at }}<br/>
              <strong>Durata:</strong> {{ job_duration }}
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Qualità della traduzione:
        </mj-text>

        <mj-section background-color="#f0fdf4" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="15px" color="#065f46">
              <strong>Punteggio medio di qualità:</strong> {{ quality_score }}%<br/>
              <strong>Alta qualità:</strong> {{ high_quality_count }} elementi<br/>
              <strong>Revisione consigliata:</strong> {{ review_needed_count }} elementi
            </mj-text>
          </mj-column>
        </mj-section>

        {% if review_needed_count > 0 %}
        <mj-spacer height="20px" />
        <mj-section background-color="#fef3c7" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="14px" color="#92400e" font-weight="bold">
              ⚠️ Revisione consigliata
            </mj-text>
            <mj-text font-size="14px" color="#92400e" line-height="1.6">
              {{ review_needed_count }} traduzioni hanno ottenuto un punteggio inferiore all'85% e dovrebbero essere revisionate prima della pubblicazione.
            </mj-text>
          </mj-column>
        </mj-section>
        {% endif %}

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Passaggi successivi:
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}" line-height="1.8">
          1. Rivedi le traduzioni nel tuo pannello di amministrazione<br/>
          2. Modifica eventuali traduzioni che necessitano di raffinamento<br/>
          3. Pubblica le traduzioni per renderle attive<br/>
          4. Il tuo contenuto multilingua sarà disponibile per i clienti
        </mj-text>

        <mj-spacer height="30px" />

        <mj-button href="{{ review_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          Rivedi le traduzioni
        </mj-button>

        {% if can_publish_all %}
        <mj-spacer height="10px" />
        <mj-button href="{{ publish_all_url }}" background-color="#059669" color="#ffffff" font-size="14px" border-radius="6px" padding="10px 25px">
          Pubblica tutto
        </mj-button>
        {% endif %}
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
✓ TRADUZIONE COMPLETATA!

Le tue traduzioni sono pronte

Buone notizie! Il tuo lavoro di traduzione di massa è stato completato con successo.

RIEPILOGO LAVORO:
- ID lavoro: {{ job_id }}
- Tipo di contenuto: {{ content_type }}
- Lingue: {{ target_languages }}
- Oggetti tradotti: {{ items_translated }}
- Parole totali: {{ word_count }}
- Completato: {{ completed_at }}
- Durata: {{ job_duration }}

QUALITÀ DELLE TRADUZIONI:
- Punteggio medio di qualità: {{ quality_score }}%
- Alta qualità: {{ high_quality_count }} elementi
- Revisione consigliata: {{ review_needed_count }} elementi

{% if review_needed_count > 0 %}
⚠️ REVISIONE CONSIGLIATA:
{{ review_needed_count }} traduzioni hanno ottenuto un punteggio inferiore all'85% e dovrebbero essere revisionate prima della pubblicazione.
{% endif %}

PASSAGGI SUCCESSIVI:
1. Rivedi le traduzioni nel tuo pannello di amministrazione
2. Modifica eventuali traduzioni che necessitano di raffinamento
3. Pubblica le traduzioni per renderle attive
4. Il tuo contenuto multilingua sarà disponibile per i clienti

Rivedi le traduzioni: {{ review_url }}
{% if can_publish_all %}Pubblica tutto: {{ publish_all_url }}{% endif %}