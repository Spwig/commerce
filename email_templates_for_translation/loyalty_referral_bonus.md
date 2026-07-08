---
template_type: loyalty_referral_bonus
category: Loyalty Program
---

# Email Template: loyalty_referral_bonus

## Subject
🎁 Bonus Points for Referring {{ referee_name }}!

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#dcfce7">
      <mj-column>
        <mj-text font-size="24px" font-weight="bold" color="#065f46" align="center">
          🎁 Referral Bonus Earned!
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Thanks for Sharing, {{ customer_name }}!
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Great news! {{ referee_name }} just joined our loyalty program through your referral, and you've earned bonus points!
        </mj-text>

        <mj-spacer height="30px" />

        <mj-section background-color="#f0fdf4" border-radius="8px" padding="25px">
          <mj-column>
            <mj-text font-size="18px" font-weight="bold" color="#065f46" align="center">
              You Earned
            </mj-text>
            <mj-text font-size="36px" font-weight="bold" color="#047857" align="center">
              +{{ bonus_points }} Points
            </mj-text>
            <mj-text font-size="14px" color="#065f46" align="center">
              For referring {{ referee_name }}
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Your Updated Balance:
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}">
          <strong>Points Balance:</strong> {{ total_points }} points<br/>
          <strong>Referral Bonus:</strong> +{{ bonus_points }} points<br/>
          <strong>Friends Referred:</strong> {{ total_referrals }}
        </mj-text>

        <mj-spacer height="30px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
              Keep Sharing, Keep Earning!
            </mj-text>
            <mj-text font-size="14px" color="{{ theme.color.text|default:'#4b5563' }}">
              Earn {{ points_per_referral }} points for every friend who joins. There's no limit!
            </mj-text>
            <mj-spacer height="15px" />
            <mj-button href="{{ referral_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="14px" border-radius="6px" padding="10px 25px">
              Share Your Referral Link
            </mj-button>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-button href="{{ shop_url }}" background-color="#059669" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          Start Shopping
        </mj-button>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
🎁 REFERRAL BONUS EARNED!

Thanks for Sharing, {{ customer_name }}!

Great news! {{ referee_name }} just joined our loyalty program through your referral, and you've earned bonus points!

YOU EARNED:
+{{ bonus_points }} Points
For referring {{ referee_name }}

YOUR UPDATED BALANCE:
- Points Balance: {{ total_points }} points
- Referral Bonus: +{{ bonus_points }} points
- Friends Referred: {{ total_referrals }}

KEEP SHARING, KEEP EARNING!
Earn {{ points_per_referral }} points for every friend who joins. There's no limit!

Share your referral link: {{ referral_url }}
Start shopping: {{ shop_url }}

## Variables

| Variable | Description | Example |
|----------|-------------|---------|
| customer_name | Referrer's first name | Sarah |
| referee_name | Friend's first name | Emily |
| bonus_points | Points earned | 500 |
| total_points | Total after bonus | 2,750 |
| total_referrals | Total friends referred | 3 |
| points_per_referral | Points per friend | 500 |
| referral_url | Personal referral link | https://shop.com/en/refer/abc123 |
| shop_url | Shop homepage | https://shop.com/en/ |

## Notes

- Sent when referred friend joins loyalty program
- Celebrates sharing/referrals
- Encourages more referrals
- Marketing email - respects preferences
- Points auto-added before email
