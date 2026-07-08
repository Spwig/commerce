---
template_type: license_trial_welcome
category: License
---

# Email Template: license_trial_welcome

## Subject
Benvenuto in Spwig - Il tuo periodo di prova gratuito di {{ trial_days }} giorni

## HTML Content
<mjml>
  <mj-head>
    <mj-attributes>
      <mj-all font-family="'Helvetica Neue', Helvetica, Arial, sans-serif" />
      <mj-text font-size="14px" color="#333333" line-height="20px" />
      <mj-section background-color="{{ theme.color.background|default:'#ffffff' }}" padding="20px" />
    </mj-attributes>
  </mj-head>
  <mj-body background-color="{{ theme.color.background_secondary|default:'#f9fafb' }}">
    <!-- Header -->
    <mj-section background-color="#059669" padding="30px 20px">
      <mj-column>
        <mj-text font-size="28px" font-weight="bold" color="#ffffff" align="center">
          Benvenuto in Spwig!
        </mj-text>
        <mj-text font-size="16px" color="#ffffffcc" align="center" padding-top="10px">
          Il tuo periodo di prova gratuito di {{ trial_days }} giorni è pronto
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Greeting -->
    <mj-section>
      <mj-column>
        <mj-text font-size="16px">
          Ciao {{ customer_name }},
        </mj-text>
        <mj-text>
          Grazie per aver provato <strong>{{ product_name }}</strong>! Il tuo periodo di prova è stato attivato e hai <strong>{{ trial_days }} giorni</strong> per esplorare tutto ciò che Spwig ha da offrire{% if includes_pos %}, incluso il nostro sistema Point of Sale{% endif %}.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Setup Token Box -->
    <mj-section background-color="#f0fdf4" padding="25px" border-radius="8px">
      <mj-column>
        <mj-text font-size="12px" color="#065f46" font-weight="bold" align="center">
          IL TUO TOKEN DI CONFIGURAZIONE
        </mj-text>
        <mj-text font-size="14px" font-weight="bold" color="#059669" align="center" font-family="'Courier New', monospace" padding="10px 0" word-break="break-all">
          {{ setup_token }}
        </mj-text>
        <mj-text font-size="12px" color="{{ theme.color.text_muted|default:'#6b7280' }}" align="center">
          Usa questo token durante l'installazione per attivare il tuo negozio di prova
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Getting Started -->
    <mj-section>
      <mj-column>
        <mj-text font-size="16px" font-weight="bold" padding-bottom="10px">
          Getting Started
        </mj-text>
        <mj-text font-size="14px">
          1. Segui la nostra guida di configurazione per installare Spwig sul tuo server
        </mj-text>
        <mj-text font-size="14px">
          2. Inserisci il tuo token di configurazione quando richiesto durante l'installazione
        </mj-text>
        <mj-text font-size="14px">
          3. Inizia a costruire il tuo negozio online!
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Setup Guide CTA -->
    {% include 'email_system/mjml_components/cta_button.mjml' with url=setup_url text="View Setup Guide" %}

    <!-- What's Included -->
    <mj-section background-color="{{ theme.color.background_secondary|default:'#f9fafb' }}" padding="20px" border-radius="8px">
      <mj-column>
        <mj-text font-size="16px" font-weight="bold" padding-bottom="10px">
          Cosa è incluso nel tuo periodo di prova
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          Accesso completo a tutte le funzionalità principali per {{ trial_days }} giorni
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          Catalogo prodotti, ordini e gestione clienti
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          Personalizzazione del tema e costruttore di pagine
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          Integrazioni con fornitori di pagamento e spedizione
        </mj-text>
        {% if includes_pos %}
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          Sistema Point of Sale (POS)
        </mj-text>
        {% endif %}
      </mj-column>
    </mj-section>

    <!-- Trial Info -->
    <mj-section>
      <mj-column>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          Il tuo periodo di prova scadrà in {{ trial_days }} giorni. Quando sarai pronto, aggiorna a una licenza completa per continuare a far funzionare il tuo negozio senza perdita di dati.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Support -->
    {% include 'email_system/mjml_components/support_block.mjml' %}
  </mj-body>
</mjml>

## Text Content
Benvenuto in Spwig!
Il tuo periodo di prova gratuito di {{ trial_days }} giorni è pronto.

Ciao {{ customer_name }},

Grazie per aver provato {{ product_name }}! Il tuo periodo di prova è stato attivato e hai {{ trial_days }} giorni per esplorare tutto ciò che Spwig ha da offrire{% if includes_pos %}, incluso il nostro sistema Point of Sale{% endif %}.

IL TUO TOKEN DI CONFIGURAZIONE:
{{ setup_token }}
Usa questo token durante l'installazione per attivare il tuo negozio di prova.

Getting Started:
1. Segui la nostra guida di configurazione per installare Spwig sul tuo server
2. Inserisci il tuo token di configurazione quando richiesto durante l'installazione
3. Inizia a costruire il tuo negozio online!

View Setup Guide: {{ setup_url }}

Cosa è incluso nel tuo periodo di prova:
- Accesso completo a tutte le funzionalità principali per {{ trial_days }} giorni
- Catalogo prodotti, ordini e gestione clienti
- Personalizzazione del tema e costruttore di pagine
- Integrazioni con fornitori di pagamento e spedizione
{% if includes_pos %}- Sistema Point of Sale (POS){% endif %}

Il tuo periodo di prova scadrà in {{ trial_days }} giorni. Quando sarai pronto, aggiorna a una licenza completa per continuare a far funzionare il tuo negozio senza perdita di dati.

Need help? Contatta {{ support_email }}