---
template_type: hosted_provision_failed
category: License
---

# Email Template: hosted_provision_failed

## Subject
Azione richiesta - Problema durante la configurazione del negozio {{ store_name }}

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
    <mj-section background-color="{{ theme.color.error|default:'#dc2626' }}" padding="30px 20px">
      <mj-column>
        <mj-text font-size="28px" font-weight="bold" color="#ffffff" align="center">
          Problema durante la configurazione del negozio
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
          Abbiamo riscontrato un problema durante la configurazione del tuo negozio <strong>{{ store_name }}</strong>. Il nostro team è stato notificato e sta indagando.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Error Details -->
    <mj-section background-color="#fef2f2" padding="20px" border-radius="8px">
      <mj-column>
        <mj-text font-size="14px" font-weight="bold" color="#991b1b" padding-bottom="10px">
          Cosa è successo
        </mj-text>
        <mj-text font-size="14px" color="#7f1d1d">
          {{ provision_error }}
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- What's Next -->
    <mj-section>
      <mj-column>
        <mj-text font-size="16px" font-weight="bold" padding-bottom="10px">
          Cosa succederà adesso?
        </mj-text>
        <mj-text font-size="14px">
          Il nostro team di supporto è stato automaticamente notificato su questo problema. Non devi prendere alcuna azione - ti contatteremo appena il problema sarà risolto.
        </mj-text>
        <mj-text font-size="14px" padding-top="10px">
          Se hai domande nel frattempo, non esitare a contattarci.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Support -->
    {% include 'email_system/mjml_components/support_block.mjml' %}
  </mj-body>
</mjml>

## Text Content
Problema durante la configurazione del negozio - {{ store_name }}

Ciao {{ name|default:'there' }},

Abbiamo riscontrato un problema durante la configurazione del tuo negozio {{ store_name }}. Il nostro team è stato notificato e sta indagando.

Cosa è successo:
{{ provision_error }}

Cosa succederà adesso?
Il nostro team di supporto è stato automaticamente notificato su questo problema. Non devi prendere alcuna azione - ti contatteremo appena il problema sarà risolto.

Se hai domande nel frattempo, non esitare a contattarci.

Hai bisogno di aiuto? Contatta {{ support_email }}