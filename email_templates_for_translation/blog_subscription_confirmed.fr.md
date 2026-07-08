---
template_type: blog_subscription_confirmed
category: Blog
---

# Email Template: blog_subscription_confirmed

## Subject
Veuillez confirmer votre abonnement à {{ blog_name }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section>
      <mj-column>
        <mj-text font-size="22px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Confirmez votre abonnement
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Bonjour {{ subscriber_name }},
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Merci d'avoir souscrit à {{ blog_name }} ! Pour terminer votre abonnement et commencer à recevoir les mises à jour, veuillez confirmer votre adresse e-mail.
        </mj-text>

        <mj-spacer height="30px" />

        <mj-button href="{{ confirmation_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="18px" font-weight="bold" border-radius="6px" padding="18px 50px">
          Confirmer l'abonnement
        </mj-button>

        <mj-spacer height="30px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="14px" color="{{ theme.color.text|default:'#4b5563' }}">
              Impossible de cliquer sur le bouton ? Copiez et collez ce lien dans votre navigateur :<br/>
              <span style="color: {{ theme.color.primary|default:'#2563eb' }}; font-family: 'Courier New', monospace;">{{ confirmation_url }}</span>
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-size="14px" color="{{ theme.color.text_secondary|default:'#6b7280' }}">
          <strong>Pourquoi confirmer ?</strong><br/>
          La confirmation par e-mail nous aide à nous assurer que vous souhaitez recevoir les mises à jour et à prévenir le spam. Votre confidentialité et votre boîte de réception sont importantes pour nous.
        </mj-text>

        <mj-spacer height="20px" />

        <mj-text font-size="13px" color="{{ theme.color.text_secondary|default:'#6b7280' }}" align="center">
          N'avez-vous pas souscrit ? Vous pouvez ignorer en toute sécurité cet e-mail.
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
CONFIRMEZ VOTRE ABONNEMENT

Bonjour {{ subscriber_name }},

Merci d'avoir souscrit à {{ blog_name }} ! Pour terminer votre abonnement et commencer à recevoir les mises à jour, veuillez confirmer votre adresse e-mail.

Confirmez l'abonnement : {{ confirmation_url }}

POURQUOI CONFIRMER ?
La confirmation par e-mail nous aide à nous assurer que vous souhaitez recevoir les mises à jour et à prévenir le spam. Votre confidentialité et votre boîte de réception sont importantes pour nous.

N'avez-vous pas souscrit ? Vous pouvez ignorer en toute sécurité cet e-mail.