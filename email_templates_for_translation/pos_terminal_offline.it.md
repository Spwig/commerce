---
template_type: pos_terminal_offline
category: POS
---

# Email Template: pos_terminal_offline

## Subject
⚠️ POS Terminale Offline: {{ terminal_name }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#fee2e2">
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="#991b1b" align="center">
          ⚠️ Terminale Disconnessa
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="18px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          POS Terminale Offline
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}">
          {{ terminal_name }} has gone offline and is no longer responding.
        </mj-text>

        <mj-spacer height="20px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
              Informazioni sul Terminale:
            </mj-text>
            <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>Terminale:</strong> {{ terminal_name }}<br/>
              <strong>Location:</strong> {{ location }}<br/>
              <strong>Last Seen:</strong> {{ last_seen }}<br/>
              <strong>Offline Since:</strong> {{ offline_since }}<br/>
              <strong>Duration:</strong> {{ offline_duration }}
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Cause Comuni:
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}" line-height="1.8">
          • Network connectivity issues<br/>
          • Terminale spento o riavviato<br/>
          • Crisi o congelamento del software<br/>
          • Interruzione del servizio Internet
        </mj-text>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Azioni Consigliate:
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}" line-height="1.8">
          1. Controlla l'alimentazione del terminale e la connessione di rete<br/>
          2. Riavvia il dispositivo del terminale<br/>
          3. Verifica la connettività Internet<br/>
          4. Controlla i firewall e le impostazioni di sicurezza
        </mj-text>

        {% if active_shift %}
        <mj-spacer height="20px" />
        <mj-section background-color="#fef3c7" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="14px" color="#92400e" font-weight="bold">
              ⚠️ Avviso di Turno Attivo
            </mj-text>
            <mj-text font-size="14px" color="#92400e" line-height="1.6">
              Questo terminale ha un turno attivo. I dati delle vendite potrebbero non essere sincronizzati fino al riconnettersi.
            </mj-text>
          </mj-column>
        </mj-section>
        {% endif %}

        <mj-spacer height="30px" />

        <mj-button href="{{ admin_terminals_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          Visualizza lo stato del terminale
        </mj-button>

        <mj-spacer height="20px" />

        <mj-text font-size="13px" color="{{ theme.color.text_secondary|default:'#6b7280' }}" align="center">
          Riceverai un'altra notifica quando il terminale si riconnetterà.
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
⚠️ TERMINALE DISCONNESSO

POS Terminale Offline

{{ terminal_name }} has gone offline and is no longer responding.

INFORMAZIONI SUL TERMINALE:
- Terminale: {{ terminal_name }}
- Location: {{ location }}
- Last Seen: {{ last_seen }}
- Offline Since: {{ offline_since }}
- Duration: {{ offline_duration }}

CAUSE COMUNI:
• Network connectivity issues
• Terminale spento o riavviato
• Crisi o congelamento del software
• Interruzione del servizio Internet

AZIONI CONSIGLIATE:
1. Controlla l'alimentazione del terminale e la connessione di rete
2. Riavvia il dispositivo del terminale
3. Verifica la connettività Internet
4. Controlla i firewall e le impostazioni di sicurezza

{% if active_shift %}
⚠️ AVVISO DI TURNO ATTIVO:
Questo terminale ha un turno attivo. I dati delle vendite potrebbero non essere sincronizzati fino al riconnettersi.
{% endif %}

Visualizza lo stato del terminale: {{ admin_terminals_url }}

Riceverai un'altra notifica quando il terminale si riconnetterà.