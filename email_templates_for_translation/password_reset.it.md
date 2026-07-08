---
template_type: password_reset
category: Authentication
---

# Email Template: password_reset

## Subject
Richiesta di reimpostazione password

## HTML Content
<mjml>
  <mj-body>
    <mj-section>
      <mj-column>
        <mj-text font-size="20px" font-weight="bold">
          Richiesta di reimpostazione password
        </mj-text>
        <mj-text>
          Abbiamo ricevuto una richiesta per reimpostare la tua password. Clicca sul pulsante qui sotto per reimpostarla.
        </mj-text>
        <mj-button href="{{ reset_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}">
          Reimposta password
        </mj-button>
        <mj-text color="#666666" font-size="12px">
          Se non hai richiesto questa operazione, puoi ignorare sicuramente questa email.
        </mj-text>
        <mj-text color="#666666" font-size="12px">
          Questo link scadrà tra {{ expiry_hours }} ore.
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
Richiesta di reimpostazione password

Abbiamo ricevuto una richiesta per reimpostare la tua password. Clicca sul link qui sotto per reimpostarla.

{{ reset_url }}

Se non hai richiesto questa operazione, puoi ignorare sicuramente questa email.
Questo link scadrà tra {{ expiry_hours }} ore.