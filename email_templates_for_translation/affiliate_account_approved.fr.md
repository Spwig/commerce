---
template_type: affiliate_account_approved
category: Affiliate Program
---

# Email Template: affiliate_account_approved

## Subject
🎉 Bienvenue au programme de parrainage {{ shop_name }} !

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
          🎉 Application approuvée !
        </mj-text>
        <mj-text font-size="18px" color="#6c757d" align="center">
          Bienvenue dans notre programme de parrainage
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Success Banner -->
    <mj-section background-color="#28a745" padding="40px 20px">
      <mj-column>
        <mj-text font-size="24px" font-weight="bold" color="#ffffff" align="center">
          Vous êtes maintenant affilié(e) !
        </mj-text>
        <mj-text font-size="16px" color="#ffffff" align="center" padding-top="10px">
          Commencez à gagner des commissions dès aujourd'hui
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
          Félicitations ! Votre candidature pour rejoindre le programme de parrainage {{ shop_name }} a été approuvée.
        </mj-text>
        <mj-text font-size="16px" color="#212529">
          Vous pouvez maintenant commencer à promouvoir nos produits et à gagner des commissions sur chaque vente que vous générerez.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- How it Works -->
    <mj-section background-color="#f8f9fa" padding="30px 20px">
      <mj-column>
        <mj-text font-size="18px" font-weight="bold" color="#212529" align="center" padding-bottom="10px">
          Comment ça marche
        </mj-text>
        <mj-text font-size="14px" color="#6c757d">
          1. Obtenez vos liens d'affiliation uniques depuis le tableau de bord<br/>
          2. Partagez ces liens avec votre public<br/>
          3. Gagnez des commissions lorsque des personnes achètent via vos liens<br/>
          4. Recevez des paiements selon votre calendrier de paiement
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
🎉 Bienvenue au programme de parrainage {{ shop_name }} !

Bonjour {{ affiliate_name }},

Félicitations ! Votre candidature pour rejoindre le programme de parrainage {{ shop_name }} a été approuvée.

Vous pouvez maintenant commencer à promouvoir nos produits et à gagner des commissions sur chaque vente que vous générerez.

Comment ça marche :
1. Obtenez vos liens d'affiliation uniques depuis le tableau de bord
2. Partagez ces liens avec votre public
3. Gagnez des commissions lorsque des personnes achètent via vos liens
4. Recevez des paiements selon votre calendrier de paiement

Accédez à votre tableau de bord : {{ portal_url }}

{{ shop_name }}
Questions ? Contactez {{ support_email }}