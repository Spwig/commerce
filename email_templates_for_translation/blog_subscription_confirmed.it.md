---
template_type: blog_subscription_confirmed
category: Blog
---

# Email Template: blog_subscription_confirmed

## Subject
Conferma la tua iscrizione a {{ blog_name }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section>
      <mj-column>
        <mj-text font-size="22px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Conferma la tua iscrizione
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Ciao {{ subscriber_name }},
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Grazie per l'iscrizione a {{ blog_name }}! Per completare l'iscrizione e iniziare a ricevere gli aggiornamenti, conferma il tuo indirizzo email.
        </mj-text>

        <mj-spacer height="30px" />

        <mj-button href="{{ confirmation_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="18px" font-weight="bold" border-radius="6px" padding="18px 50px">
          Conferma iscrizione
        </mj-button>

        <mj-spacer height="30px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="14px" color="{{ theme.color.text|default:'#4b5563' }}">
              Non puoi cliccare il pulsante? Copia e incolla questo link nel tuo browser:<br/>
              <span style="color: {{ theme.color.primary|default:'#2563eb' }}; font-family: 'Courier New', monospace;">{{ confirmation_url }}</span>
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-size="14px" color="{{ theme.color.text_secondary|default:'#6b7280' }}">
          <strong>Perché confermare?</strong><br/>
          La conferma dell'email ci aiuta a garantire che tu voglia ricevere gli aggiornamenti e a prevenire lo spam. La tua privacy e la tua casella di posta sono importanti per noi.
        </mj-text>

        <mj-spacer height="20px" />

        <mj-text font-size="13px" color="{{ theme.color.text_secondary|default:'#6b7280' }}" align="center">
          Non hai sottoscritto? Puoi tranquillamente ignorare questa email.
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
CONFIRM YOUR SUBSCRIPTION

Ciao {{ subscriber_name }},

Grazie per l'iscrizione a {{ blog_name }}! Per completare l'iscrizione e iniziare a ricevere gli aggiornamenti, conferma il tuo indirizzo email.

Conferma iscrizione: {{ confirmation_url }}

WHY CONFIRM?
La conferma dell'email ci aiuta a garantire che tu voglia ricevere gli aggiornamenti e a prevenire lo spam. La tua privacy e la tua casella di posta sono importanti per noi.

Non hai sottoscritto? Puoi tranquillamente ignorare questa email.