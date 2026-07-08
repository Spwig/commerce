---
template_type: affiliate_account_activated
category: Affiliate Program
---

# Email Template: affiliate_account_activated

## Subject
Bienvenue de retour ! Compte réactivé

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
          🎉 Compte Réactivé !
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Success Banner -->
    <mj-section background-color="#28a745" padding="40px 20px">
      <mj-column>
        <mj-text font-size="24px" font-weight="bold" color="#ffffff" align="center">
          Bienvenue de retour !
        </mj-text>
        <mj-text font-size="16px" color="#ffffff" align="center" padding-top="10px">
          Votre compte affilié est à nouveau actif
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Content -->
    <mj-section background-color="#ffffff" padding="20px">
      <mj-column>
        <mj-text font-size="16px" color="#212529">
          Bonjour {{ affiliate_name }},
        </mj-text>
        <mj-text font-size="16px" color="#212529">
          Bonne nouvelle ! Votre compte affilié avec {{ shop_name }} a été réactivé.
        </mj-text>
        <mj-text font-size="16px" color="#212529">
          Vous pouvez reprendre la promotion de nos produits et percevoir des commissions dès maintenant.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- CTA -->
    <mj-section background-color="#ffffff" padding="30px 20px">
      <mj-column>
        <mj-button background-color="#007bff" color="#ffffff" href="{{ portal_url }}">
          Accéder au tableau de bord affilié
        </mj-button>
      </mj-column>
    </mj-section>

    <!-- Footer -->
    <mj-section background-color="#f8f9fa" padding="20px">
      <mj-column>
        <mj-text font-size="12px" color="#6c757d" align="center">
          {{ shop_name }}<br/>
          Questions ? <a href="mailto:{{ support_email }}" style="color: #007bff;">Contacter le support</a>
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
Bienvenue de retour ! Compte réactivé

Bonjour {{ affiliate_name }},

Bonne nouvelle ! Votre compte affilié avec {{ shop_name }} a été réactivé.

Vous pouvez reprendre la promotion de nos produits et percevoir des commissions dès maintenant.

Accédez à votre tableau de bord : {{ portal_url }}

{{ shop_name }}
Questions ? Contacter {{ support_email }}