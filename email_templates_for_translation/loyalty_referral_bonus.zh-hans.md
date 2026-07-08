---
template_type: loyalty_referral_bonus
category: Loyalty Program
---

# Email Template: loyalty_referral_bonus

## Subject
🎁 推荐 {{ referee_name }} 的奖励积分！

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#dcfce7">
      <mj-column>
        <mj-text font-size="24px" font-weight="bold" color="#065f46" align="center">
          🎁 推荐奖励积分已到账！
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          谢谢你，{{ customer_name }}！
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          好消息！{{ referee_name }} 通过你的推荐刚刚加入了我们的忠诚度计划，你已经获得了奖励积分！
        </mj-text>

        <mj-spacer height="30px" />

        <mj-section background-color="#f0fdf4" border-radius="8px" padding="25px">
          <mj-column>
            <mj-text font-size="18px" font-weight="bold" color="#065f46" align="center">
              你获得了
            </mj-text>
            <mj-text font-size="36px" font-weight="bold" color="#047857" align="center">
              +{{ bonus_points }} 积分
            </mj-text>
            <mj-text font-size="14px" color="#065f46" align="center">
              推荐 {{ referee_name }}
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          你的更新余额：
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}">
          <strong>积分余额：</strong>{{ total_points }} 积分<br/>
          <strong>推荐奖励：</strong>+{{ bonus_points }} 积分<br/>
          <strong>已推荐好友：</strong>{{ total_referrals }}
        </mj-text>

        <mj-spacer height="30px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
              继续分享，继续赚取！
            </mj-text>
            <mj-text font-size="14px" color="{{ theme.color.text|default:'#4b5563' }}">
              每推荐一位好友加入，即可赚取 {{ points_per_referral }} 积分。没有上限！
            </mj-text>
            <mj-spacer height="15px" />
            <mj-button href="{{ referral_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="14px" border-radius="6px" padding="10px 25px">
              分享你的推荐链接
            </mj-button>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-button href="{{ shop_url }}" background-color="#059669" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          开始购物
        </mj-button>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
🎁 推荐奖励积分已到账！

谢谢你，{{ customer_name }}！

好消息！{{ referee_name }} 通过你的推荐刚刚加入了我们的忠诚度计划，你已经获得了奖励积分！

你获得了：
+{{ bonus_points }} 积分
推荐 {{ referee_name }}

你的更新余额：
- 积分余额：{{ total_points }} 积分
- 推荐奖励：+{{ bonus_points }} 积分
- 已推荐好友：{{ total_referrals }}

继续分享，继续赚取！
每推荐一位好友加入，即可赚取 {{ points_per_referral }} 积分。没有上限！

分享你的推荐链接：{{ referral_url }}
开始购物：{{ shop_url }}