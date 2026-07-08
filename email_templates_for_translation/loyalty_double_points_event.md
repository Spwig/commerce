---
template_type: loyalty_double_points_event
category: Loyalty Program
---

# Email Template: loyalty_double_points_event

## Subject
🔥 Double Points Event Starts Now! - {{ shop_name }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#fef3c7">
      <mj-column>
        <mj-text font-size="28px" font-weight="bold" color="#92400e" align="center">
          🔥 2X POINTS EVENT!
        </mj-text>
        <mj-text font-size="18px" color="#92400e" align="center">
          {{ event_start }} - {{ event_end }}
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Exclusive for Loyalty Members!
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Hi {{ customer_name }},
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Get ready to earn BIG! For a limited time, you'll earn {{ points_multiplier }}X points on every purchase.
        </mj-text>

        <mj-spacer height="30px" />

        <mj-section background-color="#dcfce7" border-radius="8px" padding="25px">
          <mj-column>
            <mj-text font-size="24px" font-weight="bold" color="#047857" align="center">
              Earn {{ points_multiplier }}X Points
            </mj-text>
            <mj-text font-size="16px" color="#065f46" align="center">
              On all purchases<br/>
              {{ event_start }} - {{ event_end }}
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Example Earnings:
        </mj-text>

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="4px" padding="15px">
          <mj-column>
            <mj-text font-size="14px" color="{{ theme.color.text|default:'#4b5563' }}">
              Spend $50 → Earn {{ example_points_normal }} points normally<br/>
              <strong style="color: #047857;">During this event → Earn {{ example_points_bonus }} points! 🎉</strong>
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="20px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="4px" padding="15px">
          <mj-column>
            <mj-text font-size="14px" color="{{ theme.color.text|default:'#4b5563' }}">
              Spend $100 → Earn {{ example_points_normal_2 }} points normally<br/>
              <strong style="color: #047857;">During this event → Earn {{ example_points_bonus_2 }} points! 🎉</strong>
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Your Current Balance:
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}">
          <strong>Points:</strong> {{ current_points }} points<br/>
          <strong>Tier:</strong> {{ loyalty_tier }}
        </mj-text>

        <mj-spacer height="30px" />

        <mj-button href="{{ shop_url }}" background-color="#dc2626" color="#ffffff" font-size="18px" font-weight="bold" border-radius="6px" padding="18px 50px">
          Shop Now & Earn {{ points_multiplier }}X Points
        </mj-button>

        <mj-spacer height="20px" />

        <mj-text font-size="13px" color="#dc2626" align="center" font-weight="bold">
          Event ends {{ event_end }} - Don't miss out!
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
🔥 2X POINTS EVENT!
{{ event_start }} - {{ event_end }}

Exclusive for Loyalty Members!

Hi {{ customer_name }},

Get ready to earn BIG! For a limited time, you'll earn {{ points_multiplier }}X points on every purchase.

EARN {{ points_multiplier }}X POINTS
On all purchases
{{ event_start }} - {{ event_end }}

EXAMPLE EARNINGS:
- Spend $50 → Earn {{ example_points_normal }} points normally
  During this event → Earn {{ example_points_bonus }} points! 🎉

- Spend $100 → Earn {{ example_points_normal_2 }} points normally
  During this event → Earn {{ example_points_bonus_2 }} points! 🎉

YOUR CURRENT BALANCE:
- Points: {{ current_points }} points
- Tier: {{ loyalty_tier }}

Shop now & earn {{ points_multiplier }}X points: {{ shop_url }}

Event ends {{ event_end }} - Don't miss out!

## Variables

| Variable | Description | Example |
|----------|-------------|---------|
| customer_name | Customer's first name | Sarah |
| points_multiplier | Multiplier (2x, 3x) | 2 |
| event_start | Event start date/time | February 15, 2026 at 12:00 AM |
| event_end | Event end date/time | February 17, 2026 at 11:59 PM |
| example_points_normal | Normal points for $50 | 50 |
| example_points_bonus | Bonus points for $50 | 100 |
| example_points_normal_2 | Normal points for $100 | 100 |
| example_points_bonus_2 | Bonus points for $100 | 200 |
| current_points | Current balance | 1,450 |
| loyalty_tier | Customer's tier | Gold |
| shop_url | Shop homepage | https://shop.com/en/ |
| shop_name | Store name | Amazing Shop |

## Notes

- Marketing email - promotional event
- Creates urgency with limited time
- Shows clear earning examples
- Encourages immediate purchases
- Red CTA emphasizes urgency
