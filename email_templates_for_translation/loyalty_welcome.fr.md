---
template_type: loyalty_welcome
category: Loyalty Program
---

# Email Template: loyalty_welcome

## Subject
Bienvenue dans les Récompenses de {{ shop_name }} !

## HTML Content
<mjml>
  <mj-head>
    <mj-attributes>
      <mj-text font-family="Arial, sans-serif" line-height="1.6" />
      <mj-all font-family="Arial, sans-serif" />
    </mj-attributes>
  </mj-head>
  <mj-body background-color="{{ theme.color.background_secondaryondary|default:'#f9fafb' }}">
    <!-- Header -->
    <mj-section background-color="{{ theme.color.background|default:'#ffffff' }}" padding="40px 20px">
      <mj-column>
        <mj-text font-size="32px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}" align="center">
          🎉 Bienvenue dans les Récompenses !
        </mj-text>
        <mj-text font-size="18px" color="{{ theme.color.text_muted|default:'#6b7280' }}" align="center">
          Commencez à accumuler des points avec chaque achat
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Content -->
    <mj-section background-color="{{ theme.color.background|default:'#ffffff' }}" padding="20px">
      <mj-column>
        <mj-text font-size="16px" color="{{ theme.color.text|default:'#1f2937' }}">
          Bonjour {{ customer_name }},
        </mj-text>
        <mj-text font-size="16px" color="{{ theme.color.text|default:'#1f2937' }}">
          Bienvenue dans le programme de récompenses de {{ shop_name }} ! Vous avez été inscrit automatiquement et pouvez commencer à accumuler des points dès maintenant.
        </mj-text>

        <!-- Bonus Points (if any) -->
        {% if bonus_points %}
        <mj-text font-size="16px" color="{{ theme.color.text|default:'#1f2937' }}" padding-top="20px">
          <strong>🎁 Bonus de bienvenue : {{ bonus_points }} points !</strong>
        </mj-text>
        {% endif %}

        <!-- Current Tier -->
        <mj-divider border-color="{{ theme.color.border|default:'#e5e7eb' }}" padding="20px 0" />
        <mj-text font-size="16px" color="{{ theme.color.text|default:'#1f2937' }}">
          <strong>Votre niveau :</strong> {{ current_tier }}
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          {{ tier_benefits }}
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- How to Earn -->
    <mj-section background-color="{{ theme.color.background_secondaryondary|default:'#f9fafb' }}" padding="30px 20px">
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}" align="center">
          Comment accumuler des points
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          • Faire des achats - Gagnez des points sur chaque commande<br/>
          • Rédiger des avis - Partagez votre avis<br/>
          • Référez des amis - Propagez le mot<br/>
          • Récompenses d'anniversaire - Points spéciaux à votre anniversaire
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- CTA -->
    <mj-section background-color="{{ theme.color.background|default:'#ffffff' }}" padding="30px 20px">
      <mj-column>
        <mj-button background-color="{{ theme.color.primary|default:'#2563eb' }}" color="{{ theme.color.background|default:'#ffffff' }}" href="{{ account_url }}">
          Voir mes récompenses
        </mj-button>
      </mj-column>
    </mj-section>

    <!-- Footer -->
    <mj-section background-color="{{ theme.color.background_secondaryondary|default:'#f9fafb' }}" padding="20px">
      <mj-column>
        <mj-text font-size="12px" color="{{ theme.color.text_muted|default:'#6b7280' }}" align="center">
          {{ shop_name }}<br/>
          Questions ? <a href="mailto:{{ support_email }}" style="color: {{ theme.color.primary|default:'#2563eb' }};">Contacter le support</a>
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
Bienvenue dans les Récompenses de {{ shop_name }} !

Bonjour {{ customer_name }},

Bienvenue dans le programme de récompenses de {{ shop_name }} ! Vous avez été inscrit automatiquement et pouvez commencer à accumuler des points dès maintenant.

{% if bonus_points %}Bonus de bienvenue : {{ bonus_points }} points !{% endif %}

Votre niveau : {{ current_tier }}
{{ tier_benefits }}

Comment accumuler des points : 
- Faire des achats - Gagnez des points sur chaque commande
- Rédiger des avis - Partagez votre avis
- Référez des amis - Propagez le mot
- Récompenses d'anniversaire - Points spéciaux à votre anniversaire

Voir vos récompenses : {{ account_url }}

{{ shop_name }}
Questions ? Contacter {{ support_email }}