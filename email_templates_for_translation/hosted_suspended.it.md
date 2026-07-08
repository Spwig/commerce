---
template_type: hosted_suspended
category: License
---

# Email Template: hosted_suspended

## Subject
Negozio Sospeso - {{ store_name }}

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
    <mj-section background-color="#dc2626" padding="30px 20px">
      <mj-column>
        <mj-text font-size="28px" font-weight="bold" color="#ffffff" align="center">
          Account Sospeso
        </mj-text>
        <mj-text font-size="16px" color="#ffffffcc" align="center" padding-top="10px">
          {{ store_name }}
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Greeting -->
    <mj-section>
      <mj-column>
        <mj-text font-size="16px">
          Ciao {{ name|default:'there' }},
        </mj-text>
        <mj-text>
          Il tuo negozio <strong>{{ store_name }}</strong> è stato sospeso a causa di un pagamento non effettuato.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- What This Means -->
    <mj-section background-color="{{ theme.color.background_secondary|default:'#f9fafb' }}" padding="20px" border-radius="8px">
      <mj-column>
        <mj-text font-size="16px" font-weight="bold" padding-bottom="10px">
          Cosa Significa Questo
        </mj-text>
        <mj-text font-size="14px">
          Il tuo negozio è ora in modalità sola lettura — i clienti possono navigare, ma gli ordini sono disabilitati. I tuoi dati sono al sicuro e verranno conservati per 30 giorni.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Reactivate -->
    <mj-section>
      <mj-column>
        <mj-text>
          Per ripristinare l'accesso completo, aggiorna il metodo di pagamento e salda il saldo rimanente.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- CTA -->
    {% include 'email_system/mjml_components/cta_button.mjml' with url="https://spwig.com/account" text="Ripristina il Tuo Negozio" %}

    <!-- Support -->
    {% include 'email_system/mjml_components/support_block.mjml' %}
  </mj-body>
</mjml>

## Text Content
Account Sospeso - {{ store_name }}

Ciao {{ name|default:'there' }},

Il tuo negozio {{ store_name }} è stato sospeso a causa di un pagamento non effettuato.

Cosa Significa Questo:
Il tuo negozio è ora in modalità sola lettura — i clienti possono navigare, ma gli ordini sono disabilitati. I tuoi dati sono al sicuro e verranno conservati per 30 giorni.

Per ripristinare l'accesso completo, aggiorna il metodo di pagamento e salda il saldo rimanente.

Ripristina il Tuo Negozio: https://spwig.com/account

Hai bisogno di aiuto? Contatta {{ support_email }}