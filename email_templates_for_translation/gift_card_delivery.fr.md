---
template_type: gift_card_delivery
category: Gift Cards
---

# Email Template: gift_card_delivery

## Subject
🎁 Carte cadeau de {{ sender_name }} - {{ shop_name }}

## HTML Content
<mjml>
  <mj-head>
    <mj-attributes>
      <mj-all font-family="'Helvetica Neue', Helvetica, Arial, sans-serif" />
      <mj-text font-size="14px" color="#333333" line-height="20px" />
      <mj-section background-color="{{ theme.color.background|default:'#ffffff' }}" padding="20px" />
    </mj-attributes>
  </mj-head>
  <mj-body background-color="{{ theme.color.background_secondaryondary|default:'#f9fafb' }}">
    <!-- Header -->
    <mj-section background-color="{{ theme.color.background|default:'#ffffff' }}" padding="40px 20px">
      <mj-column>
        <mj-text font-size="32px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}" align="center">
          🎁 Vous avez reçu une carte cadeau !
        </mj-text>
        <mj-text font-size="18px" color="{{ theme.color.text_muted|default:'#6b7280' }}" align="center" padding-top="10px">
          Quelqu'un de spécial a pensé à vous
        </mj-text>
      </mj-column>
    </mj-section>

    {% if gift_card.message %}
    <!-- Personal Message -->
    <mj-section background-color="{{ theme.color.background_secondaryondary|default:'#f9fafb' }}" padding="20px">
      <mj-column>
        <mj-text font-size="16px" color="{{ theme.color.text|default:'#1f2937' }}" padding="15px 20px" background-color="{{ theme.color.background|default:'#ffffff' }}" border-radius="8px" align="center">
          <em>"{{ gift_card.message }}"</em>
          {% if gift_card.sender_name %}
          <br/><br/>
          <strong>— {{ gift_card.sender_name }}</strong>
          {% endif %}
        </mj-text>
      </mj-column>
    </mj-section>
    {% endif %}

    <!-- Gift Card Code Card -->
    <mj-section background-color="{{ theme.color.background|default:'#ffffff' }}" padding="30px 20px">
      <mj-column>
        <mj-wrapper background-color="#f0f9ff" padding="30px" border="2px solid #0ea5e9" border-radius="12px">
          <mj-section background-color="transparent">
            <mj-column>
              <mj-text font-size="14px" color="#0c4a6e" align="center" text-transform="uppercase" letter-spacing="1px" font-weight="600" padding-bottom="10px">
                Votre code de carte cadeau
              </mj-text>

              <mj-text font-size="32px" font-weight="bold" color="{{ theme.color.info|default:'#3b82f6' }}" align="center" font-family="'Courier New', Courier, monospace" letter-spacing="2px" padding="15px 0">
                {{ gift_card.code }}
              </mj-text>

              <mj-text font-size="28px" font-weight="600" color="{{ theme.color.success|default:'#10b981' }}" align="center" padding-top="10px">
                {{ gift_card.current_balance.amount }} {{ gift_card.current_balance.currency }}
              </mj-text>

              {% if gift_card.expires_at %}
              <mj-text font-size="13px" color="{{ theme.color.error|default:'#ef4444' }}" align="center" padding-top="10px">
                ⏰ Expire le : {{ gift_card.expires_at|date:"F d, Y" }}
              </mj-text>
              {% endif %}
            </mj-column>
          </mj-section>
        </mj-wrapper>
      </mj-column>
    </mj-section>

    <!-- How to Use Section -->
    <mj-section background-color="{{ theme.color.background|default:'#ffffff' }}" padding="30px 20px">
      <mj-column>
        <mj-text font-size="20px" font-weight="600" color="{{ theme.color.text|default:'#1f2937' }}" align="center" padding-bottom="15px">
          Comment utiliser votre carte cadeau
        </mj-text>

        <mj-text font-size="14px" color="{{ theme.color.text|default:'#1f2937' }}" padding="8px 20px" line-height="1.6">
          <span style="color: {{ theme.color.info|default:'#3b82f6' }}; font-size: 18px; margin-right: 8px;">1.</span>
          Parcourez nos produits et ajoutez des articles à votre panier
        </mj-text>

        <mj-text font-size="14px" color="{{ theme.color.text|default:'#1f2937' }}" padding="8px 20px" line-height="1.6">
          <span style="color: {{ theme.color.info|default:'#3b82f6' }}; font-size: 18px; margin-right: 8px;">2.</span>
          Proceedez au paiement et entrez votre code de carte cadeau
        </mj-text>

        <mj-text font-size="14px" color="{{ theme.color.text|default:'#1f2937' }}" padding="8px 20px" line-height="1.6">
          <span style="color: {{ theme.color.info|default:'#3b82f6' }}; font-size: 18px; margin-right: 8px;">3.</span>
          Le solde de la carte cadeau sera appliqué à votre commande
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- CTA Button -->
    <mj-section background-color="{{ theme.color.background|default:'#ffffff' }}" padding="10px 20px 30px 20px">
      <mj-column>
        <mj-button href="{{ shop_url }}" background-color="{{ theme.color.info|default:'#3b82f6' }}" color="{{ theme.color.background|default:'#ffffff' }}" font-size="18px" font-weight="600" border-radius="6px" padding="16px 40px">
          Commencer à shopper
        </mj-button>
      </mj-column>
    </mj-section>

    <!-- Check Balance Link -->
    <mj-section background-color="{{ theme.color.background|default:'#ffffff' }}" padding="0 20px 20px 20px">
      <mj-column>
        <mj-text font-size="13px" color="{{ theme.color.text_muted|default:'#6b7280' }}" align="center">
          Vérifiez votre solde à tout moment :
          <a href="{{ check_balance_url }}" style="color: {{ theme.color.info|default:'#3b82f6' }}; text-decoration: none;">
            Vérifier le solde de la carte cadeau
          </a>
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Gift Card Terms -->
    <mj-section background-color="{{ theme.color.background_secondaryondary|default:'#f9fafb' }}" padding="20px">
      <mj-column>
        <mj-text font-size="11px" color="{{ theme.color.text_muted|default:'#6b7280' }}" align="center" line-height="1.5">
          Les cartes cadeaux ne sont pas remboursables et ne peuvent pas être échangées contre de l'argent.
          {% if not gift_card.expires_at %}Cette carte cadeau ne expire jamais.{% endif %}
          Les cartes cadeaux ne peuvent pas être utilisées pour acheter d'autres cartes cadeaux.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Support Block -->
    <mj-section background-color="{{ theme.color.background|default:'#ffffff' }}" padding="20px">
      <mj-column>
        <mj-divider border-color="{{ theme.color.border|default:'#e5e7eb' }}" />
        <mj-text font-size="12px" color="#9ca3af" align="center">
          Besoin d'aide ? Contactez-nous à {{ support_email }}
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Spwig Branding Footer -->
    <mj-section padding="15px 0 10px 0" background-color="transparent">
      <mj-column>
        <mj-divider border-color="{{ theme.color.border|default:'#e5e7eb' }}" border-width="1px" padding="0 0 12px 0"></mj-divider>
        <mj-text align="center" padding="0" font-size="11px" color="#9ca3af" line-height="16px">
          <a href="https://spwig.com" style="color: #9ca3af; text-decoration: none; display: inline-flex; align-items: center; gap: 4px;" target="_blank">
            <img src="{{ shop_url }}/static/email_system/img/spwig-favicon.png" alt="Spwig" width="12" height="12" style="vertical-align: middle; display: inline-block;" />
            Propulsé par Spwig
          </a>
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
🎁 Vous avez reçu une carte cadeau !

{% if gift_card.sender_name %}De : {{ gift_card.sender_name }}

{% endif %}{% if gift_card.message %}Message personnel :"{{ gift_card.message }}"

{% endif %}VOTRE CODE DE CARTE CADEAU :{{ gift_card.code }}

Solde de la carte cadeau :{{ gift_card.current_balance.amount }} {{ gift_card.current_balance.currency }}

{% if gift_card.expires_at %}Expire le : {{ gift_card.expires_at|date:"F d, Y" }}
{% endif %}

Comment utiliser votre carte cadeau :1. Parcourez nos produits et ajoutez des articles à votre panier2. Proceedez au paiement et entrez votre code de carte cadeau3. Le solde de la carte cadeau sera appliqué à votre commande

Commencer à shopper :{{ shop_url }}

Vérifier votre solde :{{ check_balance_url }}

Conditions de la carte cadeau :Les cartes cadeaux ne sont pas remboursables et ne peuvent pas être échangées contre de l'argent.{% if not gift_card.expires_at %} Cette carte cadeau ne expire jamais.{% endif %} Les cartes cadeaux ne peuvent pas être utilisées pour acheter d'autres cartes cadeaux.

Besoin d'aide ? Contactez-nous à {{ support_email }}

---
Propulsé par Spwig - https://spwig.com