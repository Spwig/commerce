---
template_type: translation_job_started
category: Translation Service
---

# Email Template: translation_job_started

## Subject
🌐 Inizio del lavoro di traduzione: {{ content_type }} ({{ source_language }} → {{ target_languages }})

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#eff6ff">
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="#1e40af" align="center">
          🌐 Inizio del lavoro di traduzione
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="18px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Traduzione in blocco in corso
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}">
          Il tuo lavoro di traduzione in blocco è stato avviato e sta ora elaborando.
        </mj-text>

        <mj-spacer height="20px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
              Dettagli del lavoro:
            </mj-text>
            <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>ID del lavoro:</strong> {{ job_id }}<br/>
              <strong>Tipo di contenuto:</strong> {{ content_type }}<br/>
              <strong>Lingua di origine:</strong> {{ source_language }}<br/>
              <strong>Lingue di destinazione:</strong> {{ target_languages }}<br/>
              <strong>Oggetti da tradurre:</strong> {{ item_count }}<br/>
              <strong>Iniziato:</strong> {{ started_at }}
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Completamento stimato:
        </mj-text>

        <mj-section background-color="#f0fdf4" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="15px" color="#065f46" font-weight="bold" align="center">
              {{ estimated_completion }}
            </mj-text>
            <mj-text font-size="14px" color="#065f46" align="center">
              (Basato su {{ word_count }} parole)
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Cosa succederà adesso:
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}" line-height="1.8">
          1. Il servizio di traduzione AI elabora il tuo contenuto<br/>
          2. Le traduzioni vengono salvate come bozze per la revisione<br/>
          3. Riceverai una e-mail quando il lavoro sarà completato<br/>
          4. Revisa e pubblica le traduzioni dal tuo pannello di amministrazione
        </mj-text>

        <mj-spacer height="30px" />

        <mj-button href="{{ job_status_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          Visualizza lo stato del lavoro
        </mj-button>

        <mj-spacer height="20px" />

        <mj-text font-size="13px" color="{{ theme.color.text_secondary|default:'#6b7280' }}" align="center">
          Puoi chiudere questa e-mail. Ti notificheremo quando la traduzione sarà completata.
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
🌐 LAVORO DI TRADUZIONE INIZIATO

Traduzione in blocco in corso

Il tuo lavoro di traduzione in blocco è stato avviato e sta ora elaborando.

DETTAGLI DEL LAVORO:
- ID del lavoro: {{ job_id }}
- Tipo di contenuto: {{ content_type }}
- Lingua di origine: {{ source_language }}
- Lingue di destinazione: {{ target_languages }}
- Oggetti da tradurre: {{ item_count }}
- Iniziato: {{ started_at }}

COMPLETAMENTO STIMATO:
{{ estimated_completion }}
(Basato su {{ word_count }} parole)

COSA SUCCEDE SUCCESSIVAMENTE:
1. Il servizio di traduzione AI elabora il tuo contenuto
2. Le traduzioni vengono salvate come bozze per la revisione
3. Riceverai una e-mail quando il lavoro sarà completato
4. Revisa e pubblica le traduzioni dal tuo pannello di amministrazione

Visualizza lo stato del lavoro: {{ job_status_url }}

Puoi chiudere questa e-mail. Ti notificheremo quando la traduzione sarà completata.