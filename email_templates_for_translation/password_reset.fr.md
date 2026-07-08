---
template_type: password_reset
category: Authentication
---

# Email Template: password_reset

## Subject
Demande de réinitialisation du mot de passe

## HTML Content
<mjml>
  <mj-body>
    <mj-section>
      <mj-column>
        <mj-text font-size="20px" font-weight="bold">
          Demande de réinitialisation du mot de passe
        </mj-text>
        <mj-text>
          Nous avons reçu une demande de réinitialisation de votre mot de passe. Cliquez sur le bouton ci-dessous pour le réinitialiser.
        </mj-text>
        <mj-button href="{{ reset_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}">
          Réinitialiser le mot de passe
        </mj-button>
        <mj-text color="#666666" font-size="12px">
          Si vous n'avez pas demandé cela, vous pouvez ignorer ce courriel en toute sécurité.
        </mj-text>
        <mj-text color="#666666" font-size="12px">
          Ce lien expirera dans {{ expiry_hours }} heures.
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
Demande de réinitialisation du mot de passe

Nous avons reçu une demande de réinitialisation de votre mot de passe. Cliquez sur le lien ci-dessous pour le réinitialiser.

{{ reset_url }}

Si vous n'avez pas demandé cela, vous pouvez ignorer ce courriel en toute sécurité.
Ce lien expirera dans {{ expiry_hours }} heures.