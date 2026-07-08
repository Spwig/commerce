---
template_type: feed_sync_failed
category: Product Feeds
---

# Email Template: feed_sync_failed

## Subject
❌ Sincronizzazione {{ feed_name }} fallita su {{ platform_name }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#fee2e2">
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="#991b1b" align="center">
          ❌ Sincronizzazione Fallita
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="18px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Errore di Sincronizzazione
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}">
          Impossibile sincronizzare {{ feed_name }} su {{ platform_name }}.
        </mj-text>

        <mj-spacer height="20px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
              Dettagli dell'errore:
            </mj-text>
            <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>Feed:</strong> {{ feed_name }}<br/>
              <strong>Piattaforma:</strong> {{ platform_name }}<br/>
              <strong>Fallito a:</strong> {{ failed_at }}<br/>
              <strong>Codice di errore:</strong> {{ error_code }}
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

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Cause Comuni:
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}" line-height="1.8">
          • Credenziali API non valide o token scaduto<br/>
          • Problemi di connettività di rete<br/>
          • Limite di velocità API della piattaforma superato<br/>
          • Il formato del feed non soddisfa i requisiti della piattaforma
        </mj-text>

        {% if recommended_action %}
        <mj-spacer height="30px" />
        <mj-section background-color="#fef3c7" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="14px" color="#92400e" font-weight="bold">
              Azione Consigliata
            </mj-text>
            <mj-text font-size="14px" color="#92400e" line-height="1.6">
              {{ recommended_action }}
            </mj-text>
          </mj-column>
        </mj-section>
        {% endif %}

        <mj-spacer height="30px" />

        <mj-button href="{{ retry_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          Riprova Sincronizzazione
        </mj-button>

        <mj-spacer height="10px" />

        <mj-button href="{{ admin_feed_url }}" background-color="#6b7280" color="#ffffff" font-size="14px" border-radius="6px" padding="10px 25px">
          Controlla Impostazioni Feed
        </mj-button>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
❌ SINCRONIZZAZIONE FALLITA

Errore di sincronizzazione

Impossibile sincronizzare {{ feed_name }} su {{ platform_name }}.

DETTAGLI DELL'ERRORE:
- Feed: {{ feed_name }}
- Piattaforma: {{ platform_name }}
- Fallito a: {{ failed_at }}
- Codice di errore: {{ error_code }}

MSESSAGGIO DI ERRORE:
{{ error_message }}

CAUSE COMUNI:
• Credenziali API non valide o token scaduto
• Problemi di connettività di rete
• Limite di velocità API della piattaforma superato
• Il formato del feed non soddisfa i requisiti della piattaforma

{% if recommended_action %}
AZIONE CONSIGLIATA:
{{ recommended_action }}
{% endif %}

Riprova sincronizzazione: {{ retry_url }}
Controlla impostazioni feed: {{ admin_feed_url }}

