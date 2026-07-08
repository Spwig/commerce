---
template_type: gift_card_delivery
category: Gift Cards
---

# Email Template: gift_card_delivery

## Subject
🎁 {{ sender_name }} から {{ shop_name }} からのギフトカード

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
          🎁 ギフトカードを受領しました！
        </mj-text>
        <mj-text font-size="18px" color="{{ theme.color.text_muted|default:'#6b7280' }}" align="center" padding-top="10px">
          あなたのために特別な人が考えました
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
                あなたのギフトカードコード
              </mj-text>

              <mj-text font-size="32px" font-weight="bold" color="{{ theme.color.info|default:'#3b82f6' }}" align="center" font-family="'Courier New', Courier, monospace" letter-spacing="2px" padding="15px 0">
                {{ gift_card.code }}
              </mj-text>

              <mj-text font-size="28px" font-weight="600" color="{{ theme.color.success|default:'#10b981' }}" align="center" padding-top="10px">
                {{ gift_card.current_balance.amount }} {{ gift_card.current_balance.currency }}
              </mj-text>

              {% if gift_card.expires_at %}
              <mj-text font-size="13px" color="{{ theme.color.error|default:'#ef4444' }}" align="center" padding-top="10px">
                ⏰ 有効期限: {{ gift_card.expires_at|date:"F d, Y" }}
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
          ギフトカードの使用方法
        </mj-text>

        <mj-text font-size="14px" color="{{ theme.color.text|default:'#1f2937' }}" padding="8px 20px" line-height="1.6">
          <span style="color: {{ theme.color.info|default:'#3b82f6' }}; font-size: 18px; margin-right: 8px;">1.</span>
          商品を閲覧し、カートに商品を追加してください
        </mj-text>

        <mj-text font-size="14px" color="{{ theme.color.text|default:'#1f2937' }}" padding="8px 20px" line-height="1.6">
          <span style="color: {{ theme.color.info|default:'#3b82f6' }}; font-size: 18px; margin-right: 8px;">2.</span>
          チェックアウトに進み、ギフトカードコードを入力してください
        </mj-text>

        <mj-text font-size="14px" color="{{ theme.color.text|default:'#1f2937' }}" padding="8px 20px" line-height="1.6">
          <span style="color: {{ theme.color.info|default:'#3b82f6' }}; font-size: 18px; margin-right: 8px;">3.</span>
          ギフトカードの残高が注文に適用されます
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- CTA Button -->
    <mj-section background-color="{{ theme.color.background|default:'#ffffff' }}" padding="10px 20px 30px 20px">
      <mj-column>
        <mj-button href="{{ shop_url }}" background-color="{{ theme.color.info|default:'#3b82f6' }}" color="{{ theme.color.background|default:'#ffffff' }}" font-size="18px" font-weight="600" border-radius="6px" padding="16px 40px">
          ショッピングを開始する
        </mj-button>
      </mj-column>
    </mj-section>

    <!-- Check Balance Link -->
    <mj-section background-color="{{ theme.color.background|default:'#ffffff' }}" padding="0 20px 20px 20px">
      <mj-column>
        <mj-text font-size="13px" color="{{ theme.color.text_muted|default:'#6b7280' }}" align="center">
          いつでも残高を確認してください：
          <a href="{{ check_balance_url }}" style="color: {{ theme.color.info|default:'#3b82f6' }}; text-decoration: none;">
            ギフトカード残高を確認する
          </a>
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Gift Card Terms -->
    <mj-section background-color="{{ theme.color.background_secondaryondary|default:'#f9fafb' }}" padding="20px">
      <mj-column>
        <mj-text font-size="11px" color="{{ theme.color.text_muted|default:'#6b7280' }}" align="center" line-height="1.5">
          ギフトカードは返金不可で、現金に交換することはできません。
          {% if not gift_card.expires_at %}このギフトカードは期限がありません。{% endif %}
          ギフトカードは他のギフトカードの購入には使用できません。
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Support Block -->
    <mj-section background-color="{{ theme.color.background|default:'#ffffff' }}" padding="20px">
      <mj-column>
        <mj-divider border-color="{{ theme.color.border|default:'#e5e7eb' }}" />
        <mj-text font-size="12px" color="#9ca3af" align="center">
          お手伝いが必要ですか？ {{ support_email }} までご連絡ください
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
            Spwig によって提供されています
          </a>
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
🎁 ギフトカードを受領しました！

{% if gift_card.sender_name %}From: {{ gift_card.sender_name }}

{% endif %}{% if gift_card.message %}Personal Message:
"{{ gift_card.message }}"

{% endif %}YOUR GIFT CARD CODE:
{{ gift_card.code }}

Gift Card Balance:
{{ gift_card.current_balance.amount }} {{ gift_card.current_balance.currency }}

{% if gift_card.expires_at %}Expires: {{ gift_card.expires_at|date:"F d, Y" }}
{% endif %}

How to Use Your Gift Card:
1. 商品を閲覧し、カートに商品を追加してください
2. チェックアウトに進み、ギフトカードコードを入力してください
3. ギフトカードの残高が注文に適用されます

Start Shopping:
{{ shop_url }}

Check Your Balance:
{{ check_balance_url }}

Gift Card Terms:
ギフトカードは返金不可で、現金に交換することはできません。{% if not gift_card.expires_at %} このギフトカードは期限がありません。{% endif %} ギフトカードは他のギフトカードの購入には使用できません。

Need help? Contact us at {{ support_email }}

---
Powered by Spwig - https://spwig.com