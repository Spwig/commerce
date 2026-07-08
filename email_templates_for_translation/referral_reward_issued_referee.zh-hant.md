---
template_type: referral_reward_issued_referee
category: Referral Program
---

# Email Template: referral_reward_issued_referee

## Subject
歡迎！這是您的 {{ reward_amount }} 優惠

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
          🎁 歡迎禮品！
        </mj-text>
        <mj-text font-size="18px" color="{{ theme.color.text_muted|default:'#6b7280' }}" align="center">
          謝謝您加入我們
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Reward Display -->
    <mj-section background-color="{{ theme.color.primary|default:'#2563eb' }}" padding="40px 20px">
      <mj-column>
        <mj-text font-size="16px" color="{{ theme.color.background|default:'#ffffff' }}" align="center" padding-bottom="10px">
          🎉 您的歡迎禮品
        </mj-text>
        <mj-text font-size="48px" font-weight="bold" color="{{ theme.color.background|default:'#ffffff' }}" align="center" line-height="1">
          {{ reward_amount }}
        </mj-text>
        <mj-text font-size="16px" color="{{ theme.color.background|default:'#ffffff' }}" align="center" padding-top="10px">
          {{ reward_type_display }}
        </mj-text>
        {% if expires_at %}
        <mj-text font-size="13px" color="rgba(255, 255, 255, 0.9)" align="center" padding-top="5px">
          到期日：{{ expires_at }}
        </mj-text>
        {% endif %}
      </mj-column>
    </mj-section>

    <!-- Content -->
    <mj-section background-color="{{ theme.color.background|default:'#ffffff' }}" padding="20px">
      <mj-column>
        <mj-text font-size="16px" color="{{ theme.color.text|default:'#1f2937' }}">
          您好 {{ customer_name }}，
        </mj-text>
        <mj-text font-size="16px" color="{{ theme.color.text|default:'#1f2937' }}">
          歡迎來到 {{ shop_name }}！{{ referrer_name }} 推薦了您，我們想以 {{ reward_amount }} 的歡迎禮品向您致謝。
        </mj-text>
        <mj-text font-size="16px" color="{{ theme.color.text|default:'#1f2937' }}">
          您的禮品已經加入您的帳戶，準備在您下次購物時使用！
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- How to Use -->
    <mj-section background-color="{{ theme.color.background_secondaryondary|default:'#f9fafb' }}" padding="30px 20px">
      <mj-column>
        <mj-text font-size="18px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}" align="center" padding-bottom="10px">
          如何使用您的禮品
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          1. 瀏覽我們的產品並將商品加入購物車<br/>
          2. 繼續結帳<br/>
          3. 您的禮品將自動套用<br/>
          4. 享受您的節省！
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- CTA -->
    <mj-section background-color="{{ theme.color.background|default:'#ffffff' }}" padding="30px 20px">
      <mj-column>
        <mj-button background-color="{{ theme.color.primary|default:'#2563eb' }}" color="{{ theme.color.background|default:'#ffffff' }}" href="{{ shop_url }}">
          開始購物
        </mj-button>
      </mj-column>
    </mj-section>

    <!-- Share and Earn -->
    <mj-section background-color="{{ theme.color.background_secondaryondary|default:'#f9fafb' }}" padding="30px 20px">
      <mj-column>
        <mj-text font-size="18px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}" align="center" padding-bottom="10px">
          您也可以賺取獎勵！
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}" align="center">
          與朋友分享您的推薦連結，當他們進行首次購買時，您也可以賺取獎勵。
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section background-color="{{ theme.color.background_secondaryondary|default:'#f9fafb' }}" padding="10px 20px 30px 20px">
      <mj-column>
        <mj-button background-color="{{ theme.color.success|default:'#10b981' }}" color="{{ theme.color.background|default:'#ffffff' }}" href="{{ my_referral_link_url }}">
          獲取我的推薦連結
        </mj-button>
      </mj-column>
    </mj-section>

    <!-- Footer -->
    <mj-section background-color="{{ theme.color.background_secondaryondary|default:'#f9fafb' }}" padding="20px">
      <mj-column>
        <mj-text font-size="12px" color="{{ theme.color.text_muted|default:'#6b7280' }}" align="center">
          {{ shop_name }}<br/>
          有問題？<a href="mailto:{{ support_email }}" style="color: {{ theme.color.primary|default:'#2563eb' }};">聯繫支援</a>
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
歡迎！這是您的 {{ reward_amount }} 優惠

您好 {{ customer_name }}，

歡迎來到 {{ shop_name }}！{{ referrer_name }} 推薦了您，我們想以 {{ reward_amount }} 的歡迎禮品向您致謝。

您的獎勵：{{ reward_amount }}
類型：{{ reward_type_display }}
{% if expires_at %}到期日：{{ expires_at }}{% endif %}

如何使用您的獎勵：
1. 瀏覽我們的產品並將商品加入購物車
2. 繼續結帳
3. 您的獎勵將自動套用
4. 享受您的節省！

開始購物：{{ shop_url }}

您也可以賺取獎勵！
與朋友分享您的推薦連結，當他們進行首次購買時，您也可以賺取獎勵。
獲取您的推薦連結：{{ my_referral_link_url }}

{{ shop_name }}
有問題？聯繫 {{ support_email }}