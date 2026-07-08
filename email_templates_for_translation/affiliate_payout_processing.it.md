---
template_type: affiliate_payout_processing
category: Affiliate Program
---

# Email Template: affiliate_payout_processing

## Subject
Il pagamento di {{ payout_amount }} è in elaborazione

## HTML Content
<mjml>
  <mj-head>
    <mj-attributes>
      <mj-text font-family="Arial, sans-serif" line-height="1.6" />
      <mj-all font-family="Arial, sans-serif" />
    </mj-attributes>
  </mj-head>
  <mj-body background-color="#f8f9fa">
    <!-- Header -->
    <mj-section background-color="#ffffff" padding="40px 20px">
      <mj-column>
        <mj-text font-size="32px" font-weight="bold" color="#212529" align="center">
          💸 Elaborazione del pagamento
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Payout Display -->
    <mj-section background-color="#17a2b8" padding="40px 20px">
      <mj-column>
        <mj-text font-size="16px" color="#ffffff" align="center" padding-bottom="10px">
          Elaborazione del pagamento
        </mj-text>
        <mj-text font-size="48px" font-weight="bold" color="#ffffff" align="center" line-height="1">
          {{ payout_amount }}
        </mj-text>
        <mj-text font-size="14px" color="rgba(255, 255, 255, 0.9)" align="center" padding-top="10px">
          ID pagamento: {{ payout_id }}
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Content -->
    <mj-section background-color="#ffffff" padding="20px">
      <mj-column>
        <mj-text font-size="16px" color="#212529">
          Ciao {{ affiliate_name }},
        </mj-text>
        <mj-text font-size="16px" color="#212529">
          Buone notizie! Il pagamento di {{ payout_amount }} è ora in elaborazione.
        </mj-text>
        <mj-text font-size="16px" color="#212529">
          I fondi dovrebbero arrivare sul tuo account entro 3-5 giorni lavorativi. Riceverai un altro email quando l'elaborazione sarà completata.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Payout Details -->
    <mj-section background-color="#f8f9fa" padding="30px 20px">
      <mj-column>
        <mj-text font-size="16px" color="#212529">
          <strong>ID pagamento:</strong> {{ payout_id }}<br/>
          <strong>Importo:</strong> {{ payout_amount }}<br/>
          <strong>Metodo di pagamento:</strong> {{ payout_method }}
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- CTA -->
    <mj-section background-color="#ffffff" padding="30px 20px">
      <mj-column>
        <mj-button background-color="#007bff" color="#ffffff" href="{{ portal_url }}">
          Visualizza l'elaborazione dei pagamenti
        </mj-button>
      </mj-column>
    </mj-section>

    <!-- Footer -->
    <mj-section background-color="#f8f9fa" padding="20px">
      <mj-column>
        <mj-text font-size="12px" color="#6c757d" align="center">
          {{ shop_name }}<br/>
          Domande? <a href="mailto:{{ support_email }}" style="color: #007bff;">Contatta il supporto</a>
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
Il pagamento di {{ payout_amount }} è in elaborazione

Ciao {{ affiliate_name }},

Buone notizie! Il pagamento di {{ payout_amount }} è ora in elaborazione.

Dettagli del pagamento:
- ID pagamento: {{ payout_id }}
- Importo: {{ payout_amount }}
- Metodo di pagamento: {{ payout_method }}

I fondi dovrebbero arrivare sul tuo account entro 3-5 giorni lavorativi. Riceverai un altro email quando l'elaborazione sarà completata.

Visualizza l'elaborazione dei pagamenti: {{ portal_url }}

{{ shop_name }}
Domande? Contatta {{ support_email }}