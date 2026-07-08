---
template_type: account_invitation
category: Core E-commerce
---

# Email Template: account_invitation

## Subject
Crea il Tuo Account su {{ site_name }}

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
          Sei invitato!
        </mj-text>
        <mj-text font-size="16px" color="#ffffffcc" align="center" padding-top="10px">
          Crea il tuo account su {{ site_name }}
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
          Abbiamo notato che hai fatto shopping da noi come ospite. Crea un account completo per sbloccare vantaggi come il tracciamento degli ordini, un checkout più veloce e offerte esclusive.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Order History Summary -->
    <mj-section background-color="{{ theme.color.background_secondary|default:'#f9fafb' }}" padding="20px" border-radius="8px">
      <mj-column>
        <mj-text font-size="16px" font-weight="bold" padding-bottom="10px">
          La Tua Storia di Acquisto
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          Totale Ordini: {{ total_orders }}
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          Totale Speso: {{ total_spent }}
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Benefits -->
    <mj-section>
      <mj-column>
        <mj-text font-size="16px" font-weight="bold" padding-bottom="10px">
          Perché Creare un Account?
        </mj-text>
        <mj-text font-size="14px">
          - Traccia i tuoi ordini e visualizza la storia degli ordini
        </mj-text>
        <mj-text font-size="14px">
          - Checkout più veloce con dettagli salvati
        </mj-text>
        <mj-text font-size="14px">
          - Gestisci gli indirizzi e le preferenze
        </mj-text>
        <mj-text font-size="14px">
          - Accedi a offerte e promozioni esclusive
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- CTA Button -->
    {% include 'email_system/mjml_components/cta_button.mjml' with url=activation_url text="Crea il Tuo Account" %}

    <!-- Note -->
    <mj-section>
      <mj-column>
        <mj-text font-size="12px" color="{{ theme.color.text_muted|default:'#6b7280' }}" align="center">
          Questo link ti permetterà di impostare una password per il tuo account. La tua storia degli ordini esistente verrà conservata.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Support -->
    {% include 'email_system/mjml_components/support_block.mjml' %}
  </mj-body>
</mjml>

## Text Content
Sei invitato a creare il tuo account!

Ciao {{ customer_name }},

Abbiamo notato che hai fatto shopping da noi come ospite. Crea un account completo per sbloccare vantaggi come il tracciamento degli ordini, un checkout più veloce e offerte esclusive.

La Tua Storia di Acquisto:
- Totale Ordini: {{ total_orders }}
- Totale Speso: {{ total_spent }}

Perché Creare un Account?
- Traccia i tuoi ordini e visualizza la storia degli ordini
- Checkout più veloce con dettagli salvati
- Gestisci gli indirizzi e le preferenze
- Accedi a offerte e promozioni esclusive

Crea il Tuo Account: {{ activation_url }}

Questo link ti permetterà di impostare una password per il tuo account. La tua storia degli ordini esistente verrà conservata.

Hai bisogno di aiuto? Contatta {{ support_email }}