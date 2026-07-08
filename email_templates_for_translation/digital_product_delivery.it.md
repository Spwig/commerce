---
template_type: digital_product_delivery
category: Digital Products
---

# Email Template: digital_product_delivery

## Subject
Il tuo prodotto digitale è pronto - Ordine #{{ order_number }}

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
    <mj-section background-color="{{ theme.color.primary|default:'#2563eb' }}" padding="20px">
      <mj-column>
        <mj-text font-size="24px" font-weight="bold" color="{{ theme.color.background|default:'#ffffff' }}" align="center">
          Il tuo prodotto digitale è pronto!
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
          Grazie per l'acquisto! Il tuo prodotto digitale è ora pronto per il download.
        </mj-text>
        <mj-text font-weight="bold">
          Ordine #{{ order_number }}
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Product Details -->
    <mj-section background-color="{{ theme.color.background_secondaryondary|default:'#f9fafb' }}" padding="20px" border-radius="8px">
      <mj-column>
        <mj-text font-size="18px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          {{ product_name }}
        </mj-text>
        <mj-text color="{{ theme.color.text_muted|default:'#6b7280' }}">
          Versione: {{ product_version }}
        </mj-text>
        <mj-text color="{{ theme.color.text_muted|default:'#6b7280' }}">
          Dimensione del file: {{ file_size }}
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Download Button -->
    <mj-section>
      <mj-column>
        <mj-button href="{{ download_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="{{ theme.color.background|default:'#ffffff' }}" font-size="16px" padding="15px 30px" border-radius="6px">
          Scarica ora
        </mj-button>
      </mj-column>
    </mj-section>

    <!-- Important Information -->
    <mj-section>
      <mj-column>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          <strong>Informazioni importanti:</strong>
        </mj-text>
        {% if download_limit %}
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          • Puoi scaricare questo prodotto {{ download_limit }} volta(e)
        </mj-text>
        {% endif %}
        {% if expiration_days %}
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          • Il link di download scadrà in {{ expiration_days }} giorni
        </mj-text>
        {% endif %}
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          • Conserva questa email per riferimenti futuri
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Support -->
    <mj-section>
      <mj-column>
        <mj-divider border-color="{{ theme.color.border|default:'#e5e7eb' }}" />
        <mj-text font-size="12px" color="#9ca3af" align="center">
          Hai bisogno di aiuto? Contatta il nostro team di supporto a {{ support_email }}
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
Il tuo prodotto digitale è pronto!

Ciao {{ customer_name }},

Grazie per l'acquisto! Il tuo prodotto digitale è ora pronto per il download.

Ordine #{{ order_number }}

Prodotto: {{ product_name }}
Versione: {{ product_version }}
Dimensione del file: {{ file_size }}

Scarica il tuo prodotto qui:
{{ download_url }}

Informazioni importanti:
{% if download_limit %}• Puoi scaricare questo prodotto {{ download_limit }} volta(e)
{% endif %}{% if expiration_days %}• Il link di download scadrà in {{ expiration_days }} giorni
{% endif %}• Conserva questa email per riferimenti futuri

Hai bisogno di aiuto? Contatta il nostro team di supporto a {{ support_email }}