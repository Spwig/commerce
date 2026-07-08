---
template_type: referral_invitation
category: Referral Program
---

# Email Template: referral_invitation

## Subject
{{ referrer_name }} 送你一份礼物！

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
          🎁 有人邀请你！
        </mj-text>
        <mj-text font-size="18px" color="{{ theme.color.text_muted|default:'#6b7280' }}" align="center">
          {{ referrer_name }} 想与你分享 {{ shop_name }}
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Reward Offer -->
    <mj-section background-color="{{ theme.color.primary|default:'#2563eb' }}" padding="40px 20px">
      <mj-column>
        <mj-text font-size="18px" color="{{ theme.color.background|default:'#ffffff' }}" align="center" padding-bottom="10px">
          领取你的欢迎礼物
        </mj-text>
        <mj-text font-size="48px" font-weight="bold" color="{{ theme.color.background|default:'#ffffff' }}" align="center" line-height="1">
          {{ reward_amount }}
        </mj-text>
        <mj-text font-size="16px" color="{{ theme.color.background|default:'#ffffff' }}" align="center" padding-top="10px">
          你的首次购物可享受优惠
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Personal Message -->
    {% if personal_message %}
    <mj-section background-color="{{ theme.color.background_secondaryondary|default:'#f9fafb' }}" padding="30px 20px">
      <mj-column>
        <mj-text font-size="14px" color="{{ theme.color.text|default:'#1f2937' }}" font-style="italic" padding="15px" background-color="{{ theme.color.background|default:'#ffffff' }}" border-left="3px solid {{ theme.color.primary|default:'#2563eb' }}">
          "{{ personal_message }}"
          <br/><br/>
          - {{ referrer_name }}
        </mj-text>
      </mj-column>
    </mj-section>
    {% endif %}

    <!-- Content -->
    <mj-section background-color="{{ theme.color.background|default:'#ffffff' }}" padding="20px">
      <mj-column>
        <mj-text font-size="16px" color="{{ theme.color.text|default:'#1f2937' }}">
          你好，
        </mj-text>
        <mj-text font-size="16px" color="{{ theme.color.text|default:'#1f2937' }}">
          {{ referrer_name }} 认为你会喜欢在 {{ shop_name }} 购物。为了欢迎你，我们为你提供首次购物 {{ reward_amount }} 的优惠！
        </mj-text>
        <mj-text font-size="16px" color="{{ theme.color.text|default:'#1f2937' }}">
          只需点击下方按钮开始购物，优惠将自动应用于你的首次订单。
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- How it Works -->
    <mj-section background-color="{{ theme.color.background_secondaryondary|default:'#f9fafb' }}" padding="30px 20px">
      <mj-column>
        <mj-text font-size="18px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}" align="center" padding-bottom="10px">
          使用方法
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          1. 点击按钮访问 {{ shop_name }}<br/>
          2. 浏览并把商品加入购物车<br/>
          3. 完成购买<br/>
          4. 你的 {{ reward_amount }} 优惠将自动应用！
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- CTA -->
    <mj-section background-color="{{ theme.color.background|default:'#ffffff' }}" padding="30px 20px">
      <mj-column>
        <mj-button background-color="{{ theme.color.success|default:'#10b981' }}" color="{{ theme.color.background|default:'#ffffff' }}" href="{{ referral_link }}">
          领取我的 {{ reward_amount }} 礼物
        </mj-button>
      </mj-column>
    </mj-section>

    <!-- Footer -->
    <mj-section background-color="{{ theme.color.background_secondaryondary|default:'#f9fafb' }}" padding="20px">
      <mj-column>
        <mj-text font-size="12px" color="{{ theme.color.text_muted|default:'#6b7280' }}" align="center">
          {{ shop_name }}<br/>
          此邀请由 {{ referrer_name }} 发送<br/>
          有问题？ <a href="mailto:{{ support_email }}" style="color: {{ theme.color.primary|default:'#2563eb' }};">联系支持</a>
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
{{ referrer_name }} 送你一份礼物！

你好，

{{ referrer_name }} 认为你会喜欢在 {{ shop_name }} 购物。为了欢迎你，我们为你提供首次购物 {{ reward_amount }} 的优惠！

{% if personal_message %}"{{ personal_message }}"
- {{ referrer_name }}
{% endif %}

使用方法：
1. 访问 {{ shop_name }}
2. 浏览并把商品加入购物车
3. 完成购买
4. 你的 {{ reward_amount }} 优惠将自动应用！

领取你的礼物：{{ referral_link }}

{{ shop_name }}
此邀请由 {{ referrer_name }} 发送
有问题？联系 {{ support_email }}