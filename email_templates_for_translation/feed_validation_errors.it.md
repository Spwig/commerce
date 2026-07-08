---
template_type: feed_validation_errors
category: Product Feeds
---

# Email Template: feed_validation_errors

## Subject
⚠️ {{ feed_name }}: {{ error_count }} errori di convalida rilevati

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#fef3c7">
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="#92400e" align="center">
          ⚠️ Errori di Convalida del Feed
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="18px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Problemi di Qualità dei Dati Rilevati
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}">
          {{ error_count }} errore di convalida{{ error_count|pluralize }} rilevato nel {{ feed_name }}. Questi problemi potrebbero impedire ai prodotti di apparire su {{ platform_name }}.
        </mj-text>

        <mj-spacer height="20px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
              Riepilogo della Convalida:
            </mj-text>
            <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>Feed:</strong> {{ feed_name }}<br/>
              <strong>Piattaforma:</strong> {{ platform_name }}<br/>
              <strong>Convalidato:</strong> {{ validated_at }}<br/>
              <strong>Totale Prodotti:</strong> {{ total_products }}<br/>
              <strong>Prodotti con Errori:</strong> {{ affected_products }}
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Principali Errori:
        </mj-text>

        {% for error in top_errors %}
        <mj-section background-color="#fee2e2" border-radius="8px" padding="12px">
          <mj-column>
            <mj-text font-size="14px" color="#991b1b" font-weight="bold">
              {{ error.type }}
            </mj-text>
            <mj-text font-size="13px" color="#991b1b">
              {{ error.count }} prodotto{{ error.count|pluralize }} interessato: {{ error.message }}
            </mj-text>
          </mj-column>
        </mj-section>
        <mj-spacer height="8px" />
        {% endfor %}

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Cosa Correggere:
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}" line-height="1.8">
          {{ fix_instructions }}
        </mj-text>

        <mj-spacer height="30px" />

        <mj-button href="{{ errors_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          Visualizza Tutti gli Errori
        </mj-button>

        <mj-spacer height="10px" />

        <mj-button href="{{ admin_feed_url }}" background-color="#6b7280" color="#ffffff" font-size="14px" border-radius="6px" padding="10px 25px">
          Gestisci il Feed
        </mj-button>

        <mj-spacer height="20px" />

        <mj-text font-size="13px" color="{{ theme.color.text_secondary|default:'#6b7280' }}" align="center">
          Correggi questi errori per assicurarti che tutti i prodotti appaiano su {{ platform_name }}.
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
⚠️ ERRORE DI CONVALIDA DEL FEED

Problemi di Qualità dei Dati Rilevati

{{ error_count }} errore di convalida{{ error_count|pluralize }} rilevato nel {{ feed_name }}. Questi problemi potrebbero impedire ai prodotti di apparire su {{ platform_name }}.

RIEPILOGO DELLA CONVALIDA:
- Feed: {{ feed_name }}
- Piattaforma: {{ platform_name }}
- Convalidato: {{ validated_at }}
- Totale Prodotti: {{ total_products }}
- Prodotti con Errori: {{ affected_products }}

PRINCIPALI ERRORI:
{% for error in top_errors %}
{{ error.type }}: {{ error.count }} prodotto{{ error.count|pluralize }} - {{ error.message }}
{% endfor %}

COSA CORREGGERE:
{{ fix_instructions }}

Visualizza tutti gli errori: {{ errors_url }}
Gestisci feed: {{ admin_feed_url }}

Correggi questi errori per assicurarti che tutti i prodotti appaiano su {{ platform_name }}.