---
template_type: loyalty_double_points_event
category: Loyalty Program
---

# Email Template: loyalty_double_points_event

## Subject
🔥 现在开始双倍积分活动！- {{ shop_name }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#fef3c7">
      <mj-column>
        <mj-text font-size="28px" font-weight="bold" color="#92400e" align="center">
          🔥 双倍积分活动！
        </mj-text>
        <mj-text font-size="18px" color="#92400e" align="center">
          {{ event_start }} - {{ event_end }}
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          仅限忠诚会员！
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          你好 {{ customer_name }}，
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          准备赚大钱吧！在有限的时间内，您在每次购物时将获得 {{ points_multiplier }}X 积分。
        </mj-text>

        <mj-spacer height="30px" />

        <mj-section background-color="#dcfce7" border-radius="8px" padding="25px">
          <mj-column>
            <mj-text font-size="24px" font-weight="bold" color="#047857" align="center">
              获得 {{ points_multiplier }}X 积分
            </mj-text>
            <mj-text font-size="16px" color="#065f46" align="center">
              所有购买商品<br/>
              {{ event_start }} - {{ event_end }}
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          示例收益：
        </mj-text>

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="4px" padding="15px">
          <mj-column>
            <mj-text font-size="14px" color="{{ theme.color.text|default:'#4b5563' }}">
              消费 $50 → 正常获得 {{ example_points_normal }} 积分<br/>
              <strong style="color: #047857;">本次活动期间 → 获得 {{ example_points_bonus }} 积分！🎉</strong>
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="20px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="4px" padding="15px">
          <mj-column>
            <mj-text font-size="14px" color="{{ theme.color.text|default:'#4b5563' }}">
              消费 $100 → 正常获得 {{ example_points_normal_2 }} 积分<br/>
              <strong style="color: #047857;">本次活动期间 → 获得 {{ example_points_bonus_2 }} 积分！🎉</strong>
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          您的当前余额：
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}">
          <strong>积分：</strong> {{ current_points }} 积分<br/>
          <strong>等级：</strong> {{ loyalty_tier }}
        </mj-text>

        <mj-spacer height="30px" />

        <mj-button href="{{ shop_url }}" background-color="#dc2626" color="#ffffff" font-size="18px" font-weight="bold" border-radius="6px" padding="18px 50px">
          立即购物并获得 {{ points_multiplier }}X 积分
        </mj-button>

        <mj-spacer height="20px" />

        <mj-text font-size="13px" color="#dc2626" align="center" font-weight="bold">
          活动于 {{ event_end }} 结束 - 别错过！
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
🔥 双倍积分活动！
{{ event_start }} - {{ event_end }}

仅限忠诚会员！

你好 {{ customer_name }}，

准备赚大钱吧！在有限的时间内，您在每次购物时将获得 {{ points_multiplier }}X 积分。

获得 {{ points_multiplier }}X 积分
所有购买商品
{{ event_start }} - {{ event_end }}

示例收益：
- 消费 $50 → 正常获得 {{ example_points_normal }} 积分
  本次活动期间 → 获得 {{ example_points_bonus }} 积分！🎉

- 消费 $100 → 正常获得 {{ example_points_normal_2 }} 积分
  本次活动期间 → 获得 {{ example_points_bonus_2 }} 积分！🎉

您的当前余额：
- 积分：{{ current_points }} 积分
- 等级：{{ loyalty_tier }}

立即购物并获得 {{ points_multiplier }}X 积分：{{ shop_url }}

活动于 {{ event_end }} 结束 - 别错过！