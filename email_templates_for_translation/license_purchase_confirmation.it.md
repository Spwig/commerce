---
template_type: license_purchase_confirmation
category: License
---

# Email Template: license_purchase_confirmation

## Subject
La tua Licenza Spwig - Ordine #{{ order_number }}

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
    <mj-section background-color="{{ theme.color.primary|default:'#2563eb' }}" padding="30px 20px">
      <mj-column>
        <mj-text font-size="28px" font-weight="bold" color="#ffffff" align="center">
          Grazie per l'acquisto!
        </mj-text>
        <mj-text font-size="16px" color="#ffffffcc" align="center" padding-top="10px">
          Ordine #{{ order_number }}
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
          Il tuo acquisto di <strong>{{ product_name }}</strong> è completo. Di seguito troverai la tua chiave di licenza e il token di configurazione per iniziare.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Order Summary -->
    <mj-section background-color="{{ theme.color.background_secondary|default:'#f9fafb' }}" padding="20px" border-radius="8px">
      <mj-column>
        <mj-text font-size="16px" font-weight="bold" padding-bottom="10px">
          Riepilogo Ordine
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          Prodotto: {{ product_name }}{% if includes_pos %} (includes POS){% endif %}
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          Importo: {{ price }}
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          Numero Ordine: {{ order_number }}
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- License Key Box -->
    <mj-section background-color="#eff6ff" padding="25px" border-radius="8px">
      <mj-column>
        <mj-text font-size="12px" color="#1e40af" font-weight="bold" align="center">
          LA TUA CHIAVE DI LICENZA
        </mj-text>
        <mj-text font-size="18px" font-weight="bold" color="{{ theme.color.primary|default:'#2563eb' }}" align="center" font-family="'Courier New', monospace" padding="10px 0">
          {{ license_key }}
        </mj-text>
        <mj-text font-size="12px" color="{{ theme.color.text_muted|default:'#6b7280' }}" align="center">
          Salva questa chiave - ti servirà per il reinstall
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
          Usa questo token durante l'installazione per attivare il tuo negozio
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Getting Started -->
    <mj-section>
      <mj-column>
        <mj-text font-size="16px" font-weight="bold" padding-bottom="10px">
          Iniziare
        </mj-text>
        <mj-text font-size="14px">
          1. Segui la nostra guida di configurazione per installare Spwig sul tuo server
        </mj-text>
        <mj-text font-size="14px">
          2. Inserisci il tuo token di configurazione quando richiesto durante l'installazione
        </mj-text>
        <mj-text font-size="14px">
          3. Il tuo negozio verrà attivato automaticamente
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Setup Guide CTA -->
    {% include 'email_system/mjml_components/cta_button.mjml' with url=setup_url text="View Setup Guide" %}

    {% if activation_url %}
    <!-- Guest Account Activation -->
    <mj-section background-color="{{ theme.color.background|default:'#ffffff' }}" padding="20px 20px 10px">
      <mj-column>
        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}" align="center">
          Crea il Tuo Account
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}" align="center" padding-top="5px">
          Imposta una password per gestire le tue licenze, accedere ai download e ricevere aggiornamenti.
        </mj-text>
      </mj-column>
    </mj-section>
    {% include 'email_system/mjml_components/cta_button.mjml' with url=activation_url text="Create Your Account" %}
    {% endif %}

    <!-- Important Notice -->
    <mj-section>
      <mj-column>
        <mj-text font-size="14px" color="{{ theme.color.warning|default:'#d97706' }}" font-weight="bold">
          Importante:
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          Mantieni questa email al sicuro - contiene la tua chiave di licenza e il token di configurazione per riferimenti futuri. Non condividere queste credenziali con altre persone.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Support -->
    {% include 'email_system/mjml_components/support_block.mjml' %}
  </mj-body>
</mjml>

## Text Content
Grazie per l'acquisto!

Ordine #{{ order_number }}

Ciao {{ customer_name }},

Il tuo acquisto di {{ product_name }} è completo. Di seguito troverai la tua chiave di licenza e il token di configurazione per iniziare.

Riepilogo Ordine:
- Prodotto: {{ product_name }}{% if includes_pos %} (includes POS){% endif %}
- Importo: {{ price }}
- Numero Ordine: {{ order_number }}

LA TUA CHIAVE DI LICENZA:
{{ license_key }}
Salva questa chiave - ti servirà per il reinstall.

IL TUO TOKEN DI CONFIGURAZIONE:
{{ setup_token }}
Usa questo token durante l'installazione per attivare il tuo negozio.

Iniziare:
1. Segui la nostra guida di configurazione per installare Spwig sul tuo server
2. Inserisci il tuo token di configurazione quando richiesto durante l'installazione
3. Il tuo negozio verrà attivato automaticamente

Visualizza la guida di configurazione: {{ setup_url }}
{% if activation_url %}
Crea il Tuo Account:
Imposta una password per gestire le tue licenze, accedere ai download e ricevere aggiornamenti.
{{ activation_url }}
{% endif %}
IMPORTANTE:
Mantieni questa email al sicuro - contiene la tua chiave di licenza e il token di configurazione per riferimenti futuri. Non condividere queste credenziali con altre persone.

Hai bisogno di aiuto? Contatta {{ support_email }}