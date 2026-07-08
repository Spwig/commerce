---
template_type: component_update_failed
category: Component Updates
---

# Email Template: component_update_failed

## Subject
❌ Aggiornamento fallito: {{ component_name }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#fee2e2">
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="#991b1b" align="center">
          ❌ Aggiornamento fallito
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="18px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Errore di installazione
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}">
          L'aggiornamento di {{ component_name }} alla versione {{ target_version }} non è riuscito nell'installazione.
        </mj-text>

        <mj-spacer height="20px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
              Dettagli del fallimento:
            </mj-text>
            <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>Componente:</strong> {{ component_name }}<br/>
              <strong>Versione Obiettivo:</strong> {{ target_version }}<br/>
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

        {% if error_log %}
        <mj-spacer height="20px" />
        <mj-text font-size="14px" color="{{ theme.color.text_secondary|default:'#6b7280' }}">
          <strong>Registro completo degli errori:</strong><br/>
          <code style="font-size: 12px; color: #6b7280;">
            {{ error_log|truncatewords:50 }}
          </code>
        </mj-text>
        {% endif %}

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Cosa fare:
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}" line-height="1.8">
          1. Controlla i requisiti del sistema e le dipendenze<br/>
          2. Esamina il registro degli errori per i dettagli<br/>
          3. Prova a reinstallare, o contatta il supporto<br/>
          4. Il tuo negozio è ancora in esecuzione su {{ current_version }}
        </mj-text>

        <mj-spacer height="30px" />

        <mj-button href="{{ retry_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          Riprova l'installazione
        </mj-button>

        <mj-spacer height="10px" />

        <mj-button href="{{ support_url }}" background-color="#6b7280" color="#ffffff" font-size="14px" border-radius="6px" padding="10px 25px">
          Contatta il supporto
        </mj-button>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
❌ AGGIORNAMENTO FALLITO

Errore di installazione

L'aggiornamento di {{ component_name }} alla versione {{ target_version }} non è riuscito nell'installazione.

DETTAGLI DEL FALLIMENTO:
- Componente: {{ component_name }}
- Versione Obiettivo: {{ target_version }}
- Fallito a: {{ failed_at }}
- Codice di errore: {{ error_code }}

MESSAGGIO DI ERRORE:
{{ error_message }}

{% if error_log %}
REGISTRO COMPLETO DEGLI ERRORI:
{{ error_log|truncatewords:50 }}
{% endif %}

COSA FARE:
1. Controlla i requisiti del sistema e le dipendenze
2. Esamina il registro degli errori per i dettagli
3. Prova a reinstallare, o contatta il supporto
4. Il tuo negozio è ancora in esecuzione su {{ current_version }}

Riprova l'installazione: {{ retry_url }}
Contatta il supporto: {{ support_url }}
