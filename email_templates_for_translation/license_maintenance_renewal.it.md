---
template_type: license_maintenance_renewal
category: License
---

# Email Template: license_maintenance_renewal

## Subject
Manutenzione rinnovata - Ordine #{{ order_number }}

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
    <mj-section background-color="{{ theme.color.success|default:'#10b981' }}" padding="30px 20px">
      <mj-column>
        <mj-text font-size="28px" font-weight="bold" color="#ffffff" align="center">
          Manutenzione rinnovata!
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
          La tua sottoscrizione di manutenzione Spwig è stata rinnovata con successo. Continuerai a ricevere aggiornamenti della piattaforma, patch di sicurezza e nuove funzionalità.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Renewal Summary -->
    <mj-section background-color="{{ theme.color.background_secondary|default:'#f9fafb' }}" padding="20px" border-radius="8px">
      <mj-column>
        <mj-text font-size="16px" font-weight="bold" padding-bottom="10px">
          Riepilogo del rinnovo
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          Chiave di licenza: {{ license_key }}
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          Manutenzione valida fino a: {{ renewal_expires_at }}
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          Numero ordine: {{ order_number }}
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- What's Included -->
    <mj-section>
      <mj-column>
        <mj-text font-size="16px" font-weight="bold" padding-bottom="10px">
          Cosa è incluso
        </mj-text>
        <mj-text font-size="14px">
          La tua manutenzione attiva ti dà accesso a:
        </mj-text>
        <mj-text font-size="14px" padding-top="5px">
          - Aggiornamenti e miglioramenti delle funzionalità della piattaforma
        </mj-text>
        <mj-text font-size="14px">
          - Patch di sicurezza e correzioni di bug
        </mj-text>
        <mj-text font-size="14px">
          - Nuove versioni di componenti tramite il server di aggiornamento
        </mj-text>
        <mj-text font-size="14px">
          - Supporto tecnico
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Next Steps -->
    <mj-section>
      <mj-column>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          Non è richiesta alcuna azione da parte tua. Gli aggiornamenti continueranno ad essere disponibili tramite il sistema di aggiornamento dei componenti del tuo pannello di amministrazione.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Support -->
    {% include 'email_system/mjml_components/support_block.mjml' %}
  </mj-body>
</mjml>

## Text Content
Manutenzione rinnovata!

Ordine #{{ order_number }}

Ciao {{ customer_name }},

La tua sottoscrizione di manutenzione Spwig è stata rinnovata con successo. Continuerai a ricevere aggiornamenti della piattaforma, patch di sicurezza e nuove funzionalità.

Riepilogo del rinnovo:
- Chiave di licenza: {{ license_key }}
- Manutenzione valida fino a: {{ renewal_expires_at }}
- Numero ordine: {{ order_number }}

Cosa è incluso:
- Aggiornamenti e miglioramenti delle funzionalità della piattaforma
- Patch di sicurezza e correzioni di bug
- Nuove versioni di componenti tramite il server di aggiornamento
- Supporto tecnico

Non è richiesta alcuna azione da parte tua. Gli aggiornamenti continueranno ad essere disponibili tramite il sistema di aggiornamento dei componenti del tuo pannello di amministrazione.

Hai bisogno di aiuto? Contatta {{ support_email }}