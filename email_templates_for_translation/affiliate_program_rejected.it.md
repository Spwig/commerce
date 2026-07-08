---
template_type: affiliate_program_rejected
category: Affiliate Program
---

# Email Template: affiliate_program_rejected

## Subject
Aggiornamento sulla candidatura al programma

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
          Aggiornamento sull'applicazione
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
          Grazie per aver candidato per la promozione di {{ program_name }}.
        </mj-text>
        <mj-text font-size="16px" color="#212529">
          Dopo aver revisionato la tua candidatura, abbiamo deciso di non approvarla in questo momento.
        </mj-text>
        <mj-text font-size="16px" color="#212529">
          Puoi comunque promuovere altri programmi nella nostra rete di affiliati.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- CTA -->
    <mj-section background-color="#ffffff" padding="30px 20px">
      <mj-column>
        <mj-button background-color="#6c757d" color="#ffffff" href="{{ portal_url }}">
          Visualizza altri programmi
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
Aggiornamento sulla candidatura al programma

Ciao {{ affiliate_name }},

Grazie per aver candidato per la promozione di {{ program_name }}.

Dopo aver revisionato la tua candidatura, abbiamo deciso di non approvarla in questo momento.

Puoi comunque promuovere altri programmi nella nostra rete di affiliati.

Visualizza altri programmi: {{ portal_url }}

{{ shop_name }}
Domande? Contatta {{ support_email }}