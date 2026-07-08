---
template_type: affiliate_commission_earned
category: Affiliate Program
---

# Email Template: affiliate_commission_earned

## Subject
Hai guadagnato una commissione di {{ commission_amount }}!

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
          💰 Commissione Guadagnata!
        </mj-text>
        <mj-text font-size="18px" color="#6c757d" align="center">
          Grande notizia da {{ shop_name }}
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Commission Display -->
    <mj-section background-color="#28a745" padding="40px 20px">
      <mj-column>
        <mj-text font-size="16px" color="#ffffff" align="center" padding-bottom="10px">
          💵 La tua Commissione
        </mj-text>
        <mj-text font-size="48px" font-weight="bold" color="#ffffff" align="center" line-height="1">
          {{ commission_amount }}
        </mj-text>
        <mj-text font-size="14px" color="rgba(255, 255, 255, 0.9)" align="center" padding-top="10px">
          Dall'ordine #{{ order_number }}
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
          Congratulazioni! Hai guadagnato una commissione di {{ commission_amount }} dall'ordine #{{ order_number }}.
        </mj-text>
        <mj-text font-size="16px" color="#212529">
          Continua a promuovere {{ shop_name }} per guadagnare altre commissioni. Più vendite generi, più guadagni!
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Commission Details -->
    <mj-section background-color="#f8f9fa" padding="30px 20px">
      <mj-column>
        <mj-text font-size="16px" color="#212529">
          <strong>Numero Ordine:</strong> #{{ order_number }}<br/>
          <strong>Importo Commissione:</strong> {{ commission_amount }}<br/>
          <strong>Tasso Commissione:</strong> {{ commission_rate }}%
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- CTA -->
    <mj-section background-color="#ffffff" padding="30px 20px">
      <mj-column>
        <mj-button background-color="#007bff" color="#ffffff" href="{{ portal_url }}">
          Visualizza il Pannello Affiliato
        </mj-button>
      </mj-column>
    </mj-section>

    <!-- Footer -->
    <mj-section background-color="#f8f9fa" padding="20px">
      <mj-column>
        <mj-text font-size="12px" color="#6c757d" align="center">
          {{ shop_name }}<br/>
          Domande? <a href="mailto:{{ support_email }}" style="color: #007bff;">
            Contatta il Supporto
          </a>
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
Hai guadagnato una commissione di {{ commission_amount }}!

Ciao {{ affiliate_name }},

Congratulazioni! Hai guadagnato una commissione di {{ commission_amount }} dall'ordine #{{ order_number }}.

Dettagli della commissione:
- Numero Ordine: #{{ order_number }}
- Importo Commissione: {{ commission_amount }}
- Tasso Commissione: {{ commission_rate }}%

Continua a promuovere {{ shop_name }} per guadagnare altre commissioni.

Visualizza il tuo pannello: {{ portal_url }}

{{ shop_name }}
Domande? Contatta {{ support_email }}