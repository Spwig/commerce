---
template_type: loyalty_anniversary_bonus
category: Loyalty Program
---

# Email Template: loyalty_anniversary_bonus

## Subject
🎉 {{ years_as_member }}年間 {{ shop_name }} にご参加いただき、ありがとうございます！

## HTML Content
<mjml>
  <mj-body>
    <mj-section>
      <mj-column>
        <mj-text font-size="28px" align="center">🎉</mj-text>
        <mj-text font-size="24px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}" align="center">
          {{ years_as_member }}年間一緒に過ごしました！
        </mj-text>

        <mj-spacer height="20px" />

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          こんにちは {{ customer_name }}、
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          今日は、あなたがロイヤルティプログラムにご参加してから{{ years_as_member }}年間が経ちました。そんなご参加を心より感謝しています！
        </mj-text>

        <mj-spacer height="30px" />

        <mj-section background-color="#f0fdf4" border-radius="8px" padding="25px">
          <mj-column>
            <mj-text font-size="18px" font-weight="bold" color="#065f46" align="center">
              アニバーサリーボーナス
            </mj-text>
            <mj-text font-size="36px" font-weight="bold" color="#047857" align="center">
              {{ bonus_points }} ポイント
            </mj-text>
            <mj-text font-size="14px" color="#065f46" align="center">
              {{ years_as_member }}年間を祝して追加されました！
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-size="18px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          ご参加から{{ years_as_member }}年間の旅:
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}" line-height="1.8">
          <strong>Member Since:</strong> {{ member_since }}<br/>
          <strong>Total Orders:</strong> {{ total_orders }}<br/>
          <strong>Points Earned:</strong> {{ lifetime_points }} points<br/>
          <strong>Current Tier:</strong> {{ loyalty_tier }}<br/>
          <strong>Total Savings:</strong> {{ total_savings }}
        </mj-text>

        <mj-spacer height="30px" />

        <mj-button href="{{ loyalty_dashboard_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          ロイヤルティダッシュボードを確認する
        </mj-button>

        <mj-spacer height="30px" />

        <mj-text font-size="14px" color="{{ theme.color.text_secondary|default:'#6b7280' }}" align="center">
          {{ years_as_member }}年間、素晴らしいご参加をありがとうございます！<br/>
          今後ともよろしくお願いいたします 🥂
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
🎉 {{ years_as_member }}年間一緒に過ごしました！

こんにちは {{ customer_name }}、

今日は、あなたがロイヤルティプログラムにご参加してから{{ years_as_member }}年間が経ちました。そんなご参加を心より感謝しています！

アニバーサリーボーナス：
{{ bonus_points }} ポイント
{{ years_as_member }}年間を祝して追加されました！

ご参加から{{ years_as_member }}年間の旅：
- Member Since: {{ member_since }}
- Total Orders: {{ total_orders }}
- Points Earned: {{ lifetime_points }} points
- Current Tier: {{ loyalty_tier }}
- Total Savings: {{ total_savings }}

ロイヤルティダッシュボードを確認する： {{ loyalty_dashboard_url }}

{{ years_as_member }}年間、素晴らしいご参加をありがとうございます！
今後ともよろしくお願いいたします 🥂