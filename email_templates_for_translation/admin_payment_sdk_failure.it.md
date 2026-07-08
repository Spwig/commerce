---
template_type: admin_payment_sdk_failure
category: Admin Notifications
---

# Email Template: admin_payment_sdk_failure

## Subject
Problema con il Fornitore di Pagamento - SDK di {{ provider_name }} non caricato

## HTML Content
<mjml>
  <mj-body>
    <mj-section>
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="{{ theme.color.warning|default:'#f59e0b' }}">
          Problema con il Fornitore di Pagamento
        </mj-text>
        <mj-text>
          Lo SDK di pagamento {{ provider_name }} non è stato caricato per un cliente durante il checkout. Questo potrebbe indicare un'interruzione del servizio da parte del fornitore.
        </mj-text>
        <mj-text>
          <strong>Fornitore:</strong> {{ provider_name }}
        </mj-text>
        <mj-text>
          <strong>Tipo di Errore:</strong> {{ error_type }}
        </mj-text>
        <mj-text>
          <strong>Ora:</strong> {{ timestamp }}
        </mj-text>
        <mj-text>
          <strong>Conteggio Fallimenti (ultima ora):</strong> {{ failure_count }}
        </mj-text>
        <mj-divider border-color="{{ theme.color.border|default:'#e5e7eb' }}" />
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          Questa notifica è limitata a una per fornitore all'ora. Se il problema persiste, controlla il dashboard del fornitore o contatta il loro supporto.
        </mj-text>
        <mj-button href="{{ admin_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}">
          Visualizza Impostazioni di Pagamento
        </mj-button>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
Problema con il Fornitore di Pagamento

Lo SDK di pagamento {{ provider_name }} non è stato caricato per un cliente durante il checkout. Questo potrebbe indicare un'interruzione del servizio da parte del fornitore.

Fornitore: {{ provider_name }}
Tipo di Errore: {{ error_type }}
Ora: {{ timestamp }}
Conteggio Fallimenti (ultima ora): {{ failure_count }}

Questa notifica è limitata a una per fornitore all'ora. Se il problema persiste, controlla il dashboard del fornitore o contatta il loro supporto.

Visualizza impostazioni di pagamento: {{ admin_url }}