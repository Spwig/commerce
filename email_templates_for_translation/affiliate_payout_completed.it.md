---
template_type: affiliate_payout_completed
category: Affiliate Program
---

# Email Template: affiliate_payout_completed

## Subject
✓ Pagamento completato: {{ payout_amount }}

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
          🎉 Pagamento completato!
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Payout Display -->
    <mj-section background-color="#28a745" padding="40px 20px">
      <mj-column>
        <mj-text font-size="16px" color="#ffffff" align="center" padding-bottom="10px">
          ✓ Pagamento effettuato con successo
        </mj-text>
        <mj-text font-size="48px" font-weight="bold" color="#ffffff" align="center" line-height="1">
          {{ payout_amount }}
        </mj-text>
        <mj-text font-size="14px" color="rgba(255, 255, 255, 0.9)" align="center" padding-top="10px">
          ID Pagamento: {{ payout_id }}
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
          Il pagamento di {{ payout_amount }} è stato completato con successo!
        </mj-text>
        <mj-text font-size="16px" color="#212529">
          I fondi sono stati inviati al tuo metodo di pagamento. A seconda della tua banca o del processore di pagamento, potrebbero essere necessari 1-2 giorni lavorativi per apparire nel tuo conto.
        </mj-text>
        <mj-text font-size="16px" color="#212529">
          Grazie per aver promosso {{ shop_name }}. Continua il grande lavoro!
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- CTA -->
    <mj-section background-color="#ffffff" padding="30px 20px">
      <mj-column>
        <mj-button background-color="#007bff" color="#ffffff" href="{{ portal_url }}">
          Visualizza i dettagli del pagamento
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
✓ Pagamento completato: {{ payout_amount }}

Ciao {{ affiliate_name }},

Il pagamento di {{ payout_amount }} è stato completato con successo!

Dettagli del pagamento:
- ID Pagamento: {{ payout_id }}
- Importo: {{ payout_amount }}
- Metodo di pagamento: {{ payout_method }}

I fondi sono stati inviati al tuo metodo di pagamento. A seconda della tua banca o del processore di pagamento, potrebbero essere necessari 1-2 giorni lavorativi per apparire nel tuo conto.

Grazie per aver promosso {{ shop_name }}. Continua il grande lavoro!

Visualizza i dettagli del pagamento: {{ portal_url }}

{{ shop_name }}
Domande? Contatta {{ support_email }}