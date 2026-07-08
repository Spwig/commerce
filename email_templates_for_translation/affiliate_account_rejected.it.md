---
template_type: affiliate_account_rejected
category: Affiliate Program
---

# Email Template: affiliate_account_rejected

## Subject
Aggiornamento della candidatura affiliato

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
          Aggiornamento della candidatura
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
          Grazie per il tuo interesse a unirti al programma degli affiliati {{ shop_name }}.
        </mj-text>
        <mj-text font-size="16px" color="#212529">
          Dopo aver esaminato la tua candidatura, abbiamo deciso di non procedere in questo momento.
        </mj-text>
        <mj-text font-size="16px" color="#212529">
          Questa decisione è basata sui requisiti correnti del nostro programma degli affiliati e potrebbe non riflettere le tue qualifiche o potenziale.
        </mj-text>
        <mj-text font-size="16px" color="#212529">
          Se le tue circostanze cambiano, puoi riconciderare di candidarti in futuro.
        </mj-text>
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
Aggiornamento della candidatura affiliato

Ciao {{ affiliate_name }},

Grazie per il tuo interesse a unirti al programma degli affiliati {{ shop_name }}.

Dopo aver esaminato la tua candidatura, abbiamo deciso di non procedere in questo momento.

Questa decisione è basata sui requisiti correnti del nostro programma degli affiliati e potrebbe non riflettere le tue qualifiche o potenziale.

Se le tue circostanze cambiano, puoi riconciderare di candidarti in futuro.

{{ shop_name }}
Domande? Contatta {{ support_email }}