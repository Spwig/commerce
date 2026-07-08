---
template_type: digital_product_license_key
category: Digital Products
---

# Email Template: digital_product_license_key

## Subject
La tua chiave di licenza - Ordine #{{ order_number }}

## HTML Content
<mjml>
  <mj-head>
    <mj-attributes>
      <mj-all font-family="'Helvetica Neue', Helvetica, Arial, sans-serif" />
      <mj-text font-size="14px" color="#333333" line-height="20px" />
      <mj-section background-color="{{ theme.color.background|default:'#ffffff' }}" padding="20px" />
    </mj-attributes>
  </mj-head>
  <mj-body background-color="{{ theme.color.background_secondaryondary|default:'#f9fafb' }}">
    <!-- Header -->
    <mj-section background-color="#059669" padding="20px">
      <mj-column>
        <mj-text font-size="24px" font-weight="bold" color="{{ theme.color.background|default:'#ffffff' }}" align="center">
          La tua chiave di licenza è pronta
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Main Content -->
    <mj-section>
      <mj-column>
        <mj-text font-size="16px">
          Ciao {{ customer_name }},
        </mj-text>
        <mj-text>
          Grazie per l'acquisto di {{ product_name }}! Ecco la tua chiave di licenza per l'attivazione.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- License Key Box -->
    <mj-section background-color="#f0fdf4" padding="30px" border="2px solid #059669" border-radius="8px">
      <mj-column>
        <mj-text font-size="12px" color="#065f46" font-weight="bold" align="center">
          LA TUA CHIAVE DI LICENZA
        </mj-text>
        <mj-text font-size="20px" font-weight="bold" color="#059669" align="center" font-family="'Courier New', monospace" padding="10px 0">
          {{ license_key }}
        </mj-text>
        <mj-text font-size="12px" color="{{ theme.color.text_muted|default:'#6b7280' }}" align="center">
          Clicca per copiare o scrivila con attenzione
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- License Details -->
    <mj-section>
      <mj-column>
        <mj-text font-size="14px" font-weight="bold">
          Dettagli della licenza:
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          • Prodotto: {{ product_name }}
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          • Versione: {{ product_version }}
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          • Tipo di licenza: {{ license_type }}
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          • Massime attivazioni: {{ max_activations }} dispositivo(i)
        </mj-text>
        {% if is_lifetime %}
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          • Validità: Licenza a vita
        </mj-text>
        {% else %}
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          • Validità fino a: {{ expiration_date }}
        </mj-text>
        {% endif %}
      </mj-column>
    </mj-section>

    <!-- Activation Instructions -->
    <mj-section background-color="{{ theme.color.background_secondaryondary|default:'#f9fafb' }}" padding="20px" border-radius="8px">
      <mj-column>
        <mj-text font-size="16px" font-weight="bold">
          Come attivare:
        </mj-text>
        <mj-text font-size="14px">
          1. Scarica e installa il software
        </mj-text>
        <mj-text font-size="14px">
          2. Apri l'applicazione
        </mj-text>
        <mj-text font-size="14px">
          3. Inserisci la tua chiave di licenza quando richiesto
        </mj-text>
        <mj-text font-size="14px">
          4. Clicca su "Attiva" per completare il processo
        </mj-text>
      </mj-column>
    </mj-section>

    {% if download_url %}
    <!-- Download Button -->
    <mj-section>
      <mj-column>
        <mj-button href="{{ download_url }}" background-color="#059669" color="{{ theme.color.background|default:'#ffffff' }}" font-size="16px" padding="15px 30px" border-radius="6px">
          Scarica il software
        </mj-button>
      </mj-column>
    </mj-section>
    {% endif %}

    <!-- Important Notice -->
    <mj-section>
      <mj-column>
        <mj-text font-size="14px" color="{{ theme.color.error|default:'#ef4444' }}" font-weight="bold">
          ⚠️ Importante:
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          • Tieni questa email al sicuro - ti servirà la chiave di licenza per il reinstall
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          • Non condividere la tua chiave di licenza con altre persone
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          • Puoi disattivare i dispositivi dal tuo dashboard account
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Support -->
    <mj-section>
      <mj-column>
        <mj-divider border-color="{{ theme.color.border|default:'#e5e7eb' }}" />
        <mj-text font-size="12px" color="#9ca3af" align="center">
          Hai bisogno di aiuto per l'attivazione? Contatta {{ support_email }}
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
La tua chiave di licenza è pronta

Ciao {{ customer_name }},

Grazie per l'acquisto di {{ product_name }}! Ecco la tua chiave di licenza per l'attivazione.

LA TUA CHIAVE DI LICENZA:
{{ license_key }}

Dettagli della licenza:
• Prodotto: {{ product_name }}
• Versione: {{ product_version }}
• Tipo di licenza: {{ license_type }}
• Massime attivazioni: {{ max_activations }} dispositivo(i)
{% if is_lifetime %}• Validità: Licenza a vita{% else %}• Validità fino a: {{ expiration_date }}{% endif %}

Come attivare:
1. Scarica e installa il software
2. Apri l'applicazione
3. Inserisci la tua chiave di licenza quando richiesto
4. Clicca su "Attiva" per completare il processo

{% if download_url %}Scarica il software: {{ download_url }}

{% endif %}IMPORTANTE:
• Tieni questa email al sicuro - ti servirà la chiave di licenza per il reinstall
• Non condividere la tua chiave di licenza con altre persone
• Puoi disattivare i dispositivi dal tuo dashboard account

Hai bisogno di aiuto per l'attivazione? Contatta {{ support_email }}