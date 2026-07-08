---
template_type: translation_quality_review_needed
category: Translation Service
---

# Email Template: translation_quality_review_needed

## Subject
⚠️ Traduzioni di bassa qualità rilevate: {{ content_type }} - {{ low_quality_count }} elementi da revisionare

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#fef3c7">
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="#92400e" align="center">
          ⚠️ Alert sulla Qualità della Traduzione
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="18px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Revisione Consigliata
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}">
          Il tuo lavoro di traduzione è completato, ma {{ low_quality_count }} traduzioni hanno ottenuto un punteggio al di sotto del limite di qualità e dovrebbero essere revisionate prima della pubblicazione.
        </mj-text>

        <mj-spacer height="20px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
              Riepilogo del Lavoro:
            </mj-text>
            <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>ID Lavoro:</strong> {{ job_id }}<br/>
              <strong>Tipo di Contenuto:</strong> {{ content_type }}<br/>
              <strong>Totale Elementi:</strong> {{ total_items }}<br/>
              <strong>Qualità Media:</strong> {{ average_quality }}%<br/>
              <strong>Bassa Qualità:</strong> {{ low_quality_count }} elementi ({{ low_quality_percentage }}%)
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Analisi della Qualità:
        </mj-text>

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="14px" color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>Eccellente (95-100%):</strong> {{ excellent_count }} elementi<br/>
              <strong>Buona (85-94%):</strong> {{ good_count }} elementi<br/>
              <strong>Accettabile (70-84%):</strong> {{ fair_count }} elementi<br/>
              <strong>Pessima (&lt;70%):</strong> <span style="color: #dc2626; font-weight: bold;">{{ poor_count }} elementi</span>
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Problemi di Qualità Comuni:
        </mj-text>

        {% for issue in quality_issues %}
        <mj-section background-color="#fef3c7" border-radius="8px" padding="12px">
          <mj-column>
            <mj-text font-size="14px" color="#92400e">
              <strong>{{ issue.type }}:</strong> {{ issue.count }} occorrenze
            </mj-text>
          </mj-column>
        </mj-section>
        <mj-spacer height="8px" />
        {% endfor %}

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Azioni Consigliate:
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}" line-height="1.8">
          1. Rivedi le traduzioni segnalate nel pannello amministrativo<br/>
          2. Modifica manualmente le traduzioni di bassa qualità<br/>
          3. Considera di ristradurre gli elementi di scarsa qualità<br/>
          4. Pubblica solo dopo che la revisione è completata
        </mj-text>

        <mj-spacer height="30px" />

        <mj-button href="{{ review_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          Rivedi le Traduzioni
        </mj-button>

        <mj-spacer height="10px" />

        <mj-button href="{{ low_quality_url }}" background-color="#dc2626" color="#ffffff" font-size="14px" border-radius="6px" padding="10px 25px">
          Visualizza gli Elementi di Bassa Qualità
        </mj-button>

        <mj-spacer height="30px" />

        <mj-section background-color="#eff6ff" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="14px" color="#1e40af" line-height="1.6">
              💡 Suggerimento: I punteggi di qualità al di sotto del 85% indicano potenziali problemi con l'ortografia, il contesto o l'accuratezza. È fortemente consigliata una revisione umana prima della pubblicazione.
            </mj-text>
          </mj-column>
        </mj-section>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
⚠️ ALERT SULLA QUALITÀ DELLE TRADUZIONI

Revisione Consigliata

Il tuo lavoro di traduzione è completato, ma {{ low_quality_count }} traduzioni hanno ottenuto un punteggio al di sotto del limite di qualità e dovrebbero essere revisionate prima della pubblicazione.

RIEPILOGO DEL LAVORO:
- ID Lavoro: {{ job_id }}
- Tipo di Contenuto: {{ content_type }}
- Totale Elementi: {{ total_items }}
- Qualità Media: {{ average_quality }}%
- Bassa Qualità: {{ low_quality_count }} elementi ({{ low_quality_percentage }}%)

ANALISI DELLA QUALITÀ:
- Eccellente (95-100%): {{ excellent_count }} elementi
- Buona (85-94%): {{ good_count }} elementi
- Accettabile (70-84%): {{ fair_count }} elementi
- Pessima (<70%): {{ poor_count }} elementi

PROBLEMI DI QUALITÀ COMUNI:
{% for issue in quality_issues %}
{{ issue.type }}: {{ issue.count }} occorrenze
{% endfor %}

AZIONI CONSIGLIATE:
1. Rivedi le traduzioni segnalate nel pannello amministrativo
2. Modifica manualmente le traduzioni di bassa qualità
3. Considera di ristradurre gli elementi di scarsa qualità
4. Pubblica solo dopo che la revisione è completata

Rivedi le traduzioni: {{ review_url }}
Visualizza gli elementi di bassa qualità: {{ low_quality_url }}

💡 Suggerimento: I punteggi di qualità al di sotto del 85% indicano potenziali problemi con l'ortografia, il contesto o l'accuratezza. È fortemente consigliata una revisione umana prima della pubblicazione.