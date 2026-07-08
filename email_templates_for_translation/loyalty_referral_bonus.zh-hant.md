---
template_type: loyalty_referral_bonus
category: Loyalty Program
---

# Email Template: loyalty_referral_bonus

## Subject
🎁 推薦 {{ referee_name }} 的額外積分！

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#dcfce7">
      <mj-column>
        <mj-text font-size="24px" font-weight="bold" color="#065f46" align="center">
          🎁 推薦獎勵已獲得！
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          謝謝你與 {{ customer_name }} 分享！
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          好消息！{{ referee_name }} 剛剛透過你的推薦加入我們的忠誠計劃，你已經獲得額外積分！
        </mj-text>

        <mj-spacer height="30px" />

        <mj-section background-color="#f0fdf4" border-radius="8px" padding="25px">
          <mj-column>
            <mj-text font-size="18px" font-weight="bold" color="#065f46" align="center">
              你獲得
            </mj-text>
            <mj-text font-size="36px" font-weight="bold" color="#047857" align="center">
              +{{ bonus_points }} 點數
            </mj-text>
            <mj-text font-size="14px" color="#065f46" align="center">
              為了推薦 {{ referee_name }}
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          你的更新餘額：
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}">
          <strong>點數餘額：</strong>{{ total_points }} 點數<br/>
          <strong>推薦獎勵：</strong>+{{ bonus_points }} 點數<br/>
          <strong>推薦朋友數：</strong>{{ total_referrals }}
        </mj-text>

        <mj-spacer height="30px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
              繼續分享，持續賺取！
            </mj-text>
            <mj-text font-size="14px" color="{{ theme.color.text|default:'#4b5563' }}">
              每有朋友加入即可賺取 {{ points_per_referral }} 點數。沒有上限！
            </mj-text>
            <mj-spacer height="15px" />
            <mj-button href="{{ referral_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="14px" border-radius="6px" padding="10px 25px">
              分享你的推薦連結
            </mj-button>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-button href="{{ shop_url }}" background-color="#059669" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          開始購物
        </mj-button>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
🎁 推薦獎勵已獲得！

謝謝你與 {{ customer_name }} 分享！

好消息！{{ referee_name }} 剛剛透過你的推薦加入我們的忠誠計劃，你已經獲得額外積分！

你獲得：
+{{ bonus_points }} 點數
為推薦 {{ referee_name }}

你的更新餘額：
- 點數餘額：{{ total_points }} 點數
- 推薦獎勵：+{{ bonus_points }} 點數
- 推薦朋友數：{{ total_referrals }}

繼續分享，持續賺取！
每有朋友加入即可賺取 {{ points_per_referral }} 點數。沒有上限！

分享你的推薦連結：{{ referral_url }}
開始購物：{{ shop_url }}