---
template_type: affiliate_commission_reversed
category: Affiliate Program
---

# Email Template: affiliate_commission_reversed

## Subject
Commissione annullata - Ordine #{{ order_number }}

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
          Commissione annullata
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
          La commissione per l'ordine #{{ order_number }} ({{ commission_amount }}) è stata annullata a causa di un rimborso del cliente.
        </mj-text>
        <mj-text font-size="16px" color="#212529">
          Quando i clienti richiedono un rimborso, eventuali commissioni associate vengono automaticamente annullate per garantire un contabile accurato.
        </mj-text>
        <mj-text font-size="16px" color="#212529">
          Questo è un aspetto normale del processo dell'affiliazione. Continua a promuovere {{ shop_name }} per guadagnare nuove commissioni!
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- CTA -->
    <mj-section background-color="#ffffff" padding="30px 20px">
      <mj-column>
        <mj-button background-color="#007bff" color="#ffffff" href="{{ portal_url }}">
          Visualizza il pannello dell'affiliazione
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
Commissione annullata - Ordine #{{ order_number }}

Ciao {{ affiliate_name }},

La commissione per l'ordine #{{ order_number }} ({{ commission_amount }}) è stata annullata a causa di un rimborso del cliente.

Quando i clienti richiedono un rimborso, eventuali commissioni associate vengono automaticamente annullate per garantire un contabile accurato.

Questo è un aspetto normale del processo dell'affiliazione. Continua a promuovere {{ shop_name }} per guadagnare nuove commissioni!

Visualizza il pannello: {{ portal_url }}

{{ shop_name }}
Domande? Contatta {{ support_email }}

