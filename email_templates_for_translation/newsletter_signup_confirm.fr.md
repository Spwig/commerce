---
template_type: newsletter_signup_confirm
category: Newsletter
---

# Email Template: newsletter_signup_confirm

## Subject
Veuillez confirmer votre abonnement à {{ store_name }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section>
      <mj-column>
        <mj-text font-size="22px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Confirmez votre abonnement
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Merci de vous être inscrit pour recevoir des nouvelles de {{ store_name }} ! Veuillez confirmer votre adresse e-mail pour commencer à recevoir nos mises à jour et nos offres.
        </mj-text>

        <mj-spacer height="30px" />

        <mj-button href="{{ confirmation_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="18px" font-weight="bold" border-radius="6px" padding="18px 50px">
          Confirmer l'abonnement
        </mj-button>

        <mj-spacer height="30px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="14px" color="{{ theme.color.text|default:'#4b5563' }}">
              Ne parvenez-vous pas à cliquer sur le bouton ? Copiez-coller ce lien dans votre navigateur :<br/>
              <span style="color: {{ theme.color.primary|default:'#2563eb' }}; font-family: 'Courier New', monospace;">{{ confirmation_url }}</span>
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-size="14px" color="{{ theme.color.text_secondary|default:'#6b7280' }}">
          <strong>Pourquoi confirmer ?</strong><br/>
          Confirmer votre adresse e-mail nous permet de nous assurer que vous souhaitez réellement nos mises à jour, et de garder votre boîte de réception propre.
        </mj-text>

        <mj-spacer height="20px" />

        <mj-text font-size="13px" color="{{ theme.color.text_secondary|default:'#6b7280' }}" align="center">
          Vous n'avez pas souscrit ? Vous pouvez ignorer cet e-mail en toute sécurité.
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
Confirmez votre abonnement à {{ store_name }}

Merci de vous être inscrit pour recevoir des nouvelles de {{ store_name }} ! Veuillez confirmer votre adresse e-mail pour commencer à recevoir nos mises à jour et nos offres :

{{ confirmation_url }}

Confirmer votre adresse e-mail nous permet de nous assurer que vous souhaitez réellement nos mises à jour, et de garder votre boîte de réception propre.

Vous n'avez pas souscrit ? Vous pouvez ignorer cet e-mail en toute sécurité.