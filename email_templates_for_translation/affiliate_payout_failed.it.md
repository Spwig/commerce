---
template_type: affiliate_payout_failed
category: Affiliate Program
---

# Email Template: affiliate_payout_failed

## Subject
Azione richiesta: Pagamento non riuscito

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
        <mj-text font-size="32px" font-weight="bold" color="#dc3545" align="center">
          ⚠️ Pagamento non riuscito
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Warning Display -->
    <mj-section background-color="#fff3cd" padding="40px 20px">
      <mj-column>
        <mj-text font-size="48px" font-weight="bold" color="#856404" align="center" line-height="1">
          {{ payout_amount }}
        </mj-text>
        <mj-text font-size="16px" color="#856404" align="center" padding-top="10px">
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
          Abbiamo riscontrato un problema nel processare il pagamento di {{ payout_amount }}.
        </mj-text>
        <mj-text font-size="16px" color="#212529">
          Questo è generalmente dovuto a informazioni di pagamento non corrette o a un problema con il tuo fornitore di pagamento.
        </mj-text>
        <mj-text font-size="16px" color="#212529">
          Aggiorna le tue informazioni di pagamento nel tuo pannello affiliato e contatta il nostro team di supporto per risolvere questo problema.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- CTA -->
    <mj-section background-color="#ffffff" padding="30px 20px">
      <mj-column>
        <mj-button background-color="#dc3545" color="#ffffff" href="{{ portal_url }}">
          Aggiorna le informazioni di pagamento
        </mj-button>
      </mj-column>
    </mj-section>

    <!-- Footer -->
    <mj-section background-color="#f8f9fa" padding="20px">
      <mj-column>
        <mj-text font-size="12px" color="#6c757d" align="center">
          {{ shop_name }}<br/>
          Hai bisogno di aiuto? <a href="mailto:{{ support_email }}" style="color: #007bff;">Contatta il supporto</a>
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
Azione richiesta: Pagamento non riuscito

Ciao {{ affiliate_name }},

Abbiamo riscontrato un problema nel processare il pagamento di {{ payout_amount }} (ID pagamento: {{ payout_id }}).

Questo è generalmente dovuto a informazioni di pagamento non corrette o a un problema con il tuo fornitore di pagamento.

Aggiorna le tue informazioni di pagamento nel tuo pannello affiliato e contatta il nostro team di supporto per risolvere questo problema.

Aggiorna le informazioni di pagamento: {{ portal_url }}

{{ shop_name }}
Hai bisogno di aiuto? Contatta {{ support_email }}