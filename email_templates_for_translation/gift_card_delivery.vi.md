---
template_type: gift_card_delivery
category: Gift Cards
---

# Email Template: gift_card_delivery

## Subject
🎁 Bạn đã nhận được Thẻ Quà từ {{ sender_name }} - {{ shop_name }}

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
          🎁 Bạn đã nhận được Thẻ Quà!
        </mj-text>
        <mj-text font-size="18px" color="{{ theme.color.text_muted|default:'#6b7280' }}" align="center" padding-top="10px">
          Ai đó đặc biệt đã nghĩ đến bạn
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
                Mã Thẻ Quà của Bạn
              </mj-text>

              <mj-text font-size="32px" font-weight="bold" color="{{ theme.color.info|default:'#3b82f6' }}" align="center" font-family="'Courier New', Courier, monospace" letter-spacing="2px" padding="15px 0">
                {{ gift_card.code }}
              </mj-text>

              <mj-text font-size="28px" font-weight="600" color="{{ theme.color.success|default:'#10b981' }}" align="center" padding-top="10px">
                {{ gift_card.current_balance.amount }} {{ gift_card.current_balance.currency }}
              </mj-text>

              {% if gift_card.expires_at %}
              <mj-text font-size="13px" color="{{ theme.color.error|default:'#ef4444' }}" align="center" padding-top="10px">
                ⏰ Hết hạn: {{ gift_card.expires_at|date:"F d, Y" }}
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
          Cách Sử Dụng Thẻ Quà
        </mj-text>

        <mj-text font-size="14px" color="{{ theme.color.text|default:'#1f2937' }}" padding="8px 20px" line-height="1.6">
          <span style="color: {{ theme.color.info|default:'#3b82f6' }}; font-size: 18px; margin-right: 8px;">1.</span>
          Xem sản phẩm và thêm các mặt hàng vào giỏ hàng
        </mj-text>

        <mj-text font-size="14px" color="{{ theme.color.text|default:'#1f2937' }}" padding="8px 20px" line-height="1.6">
          <span style="color: {{ theme.color.info|default:'#3b82f6' }}; font-size: 18px; margin-right: 8px;">2.</span>
          Tiến hành thanh toán và nhập mã thẻ quà
        </mj-text>

        <mj-text font-size="14px" color="{{ theme.color.text|default:'#1f2937' }}" padding="8px 20px" line-height="1.6">
          <span style="color: {{ theme.color.info|default:'#3b82f6' }}; font-size: 18px; margin-right: 8px;">3.</span>
          Số dư thẻ quà sẽ được áp dụng cho đơn hàng của bạn
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- CTA Button -->
    <mj-section background-color="{{ theme.color.background|default:'#ffffff' }}" padding="10px 20px 30px 20px">
      <mj-column>
        <mj-button href="{{ shop_url }}" background-color="{{ theme.color.info|default:'#3b82f6' }}" color="{{ theme.color.background|default:'#ffffff' }}" font-size="18px" font-weight="600" border-radius="6px" padding="16px 40px">
          Bắt đầu Mua Sắm
        </mj-button>
      </mj-column>
    </mj-section>

    <!-- Check Balance Link -->
    <mj-section background-color="{{ theme.color.background|default:'#ffffff' }}" padding="0 20px 20px 20px">
      <mj-column>
        <mj-text font-size="13px" color="{{ theme.color.text_muted|default:'#6b7280' }}" align="center">
          Kiểm tra số dư bất kỳ lúc nào:
          <a href="{{ check_balance_url }}" style="color: {{ theme.color.info|default:'#3b82f6' }}; text-decoration: none;">
            Kiểm tra Số Dư Thẻ Quà
          </a>
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Gift Card Terms -->
    <mj-section background-color="{{ theme.color.background_secondaryondary|default:'#f9fafb' }}" padding="20px">
      <mj-column>
        <mj-text font-size="11px" color="{{ theme.color.text_muted|default:'#6b7280' }}" align="center" line-height="1.5">
          Thẻ quà không hoàn tiền và không thể đổi lấy tiền mặt.
          {% if not gift_card.expires_at %}Thẻ quà này không bao giờ hết hạn.{% endif %}
          Thẻ quà không thể được sử dụng để mua các thẻ quà khác.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Support Block -->
    <mj-section background-color="{{ theme.color.background|default:'#ffffff' }}" padding="20px">
      <mj-column>
        <mj-divider border-color="{{ theme.color.border|default:'#e5e7eb' }}" />
        <mj-text font-size="12px" color="#9ca3af" align="center">
          Cần hỗ trợ? Liên hệ với chúng tôi tại {{ support_email }}
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
            Được cung cấp bởi Spwig
          </a>
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
🎁 Bạn đã nhận được Thẻ Quà!

{% if gift_card.sender_name %}Từ: {{ gift_card.sender_name }}

{% endif %}{% if gift_card.message %}Thông điệp cá nhân:
"{{ gift_card.message }}"

{% endif %}MÃ THẺ QUÀ CỦA BẠN:
{{ gift_card.code }}

Số dư Thẻ Quà:
{{ gift_card.current_balance.amount }} {{ gift_card.current_balance.currency }}

{% if gift_card.expires_at %}Hết hạn: {{ gift_card.expires_at|date:"F d, Y" }}
{% endif %}

Cách Sử Dụng Thẻ Quà:
1. Xem sản phẩm và thêm các mặt hàng vào giỏ hàng
2. Tiến hành thanh toán và nhập mã thẻ quà
3. Số dư thẻ quà sẽ được áp dụng cho đơn hàng của bạn

Bắt đầu Mua Sắm:
{{ shop_url }}

Kiểm tra Số Dư:
{{ check_balance_url }}

Điều Khoản Thẻ Quà:
Thẻ quà không hoàn tiền và không thể đổi lấy tiền mặt.{% if not gift_card.expires_at %} Thẻ quà này không bao giờ hết hạn.{% endif %} Thẻ quà không thể được sử dụng để mua các thẻ quà khác.

Cần hỗ trợ? Liên hệ với chúng tôi tại {{ support_email }}

---
Được cung cấp bởi Spwig - https://spwig.com