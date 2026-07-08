---
template_type: loyalty_double_points_event
category: Loyalty Program
---

# Email Template: loyalty_double_points_event

## Subject
🔥 지금 바로 2배 포인트 이벤트 시작! - {{ shop_name }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#fef3c7">
      <mj-column>
        <mj-text font-size="28px" font-weight="bold" color="#92400e" align="center">
          🔥 2배 포인트 이벤트!
        </mj-text>
        <mj-text font-size="18px" color="#92400e" align="center">
          {{ event_start }} - {{ event_end }}
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          충성도 멤버 전용!
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          안녕하세요, {{ customer_name }},
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          지금 바로 큰 혜택을 받아가세요! 제한된 기간 동안, 모든 구매 시 {{ points_multiplier }}배 포인트를 적립할 수 있습니다.
        </mj-text>

        <mj-spacer height="30px" />

        <mj-section background-color="#dcfce7" border-radius="8px" padding="25px">
          <mj-column>
            <mj-text font-size="24px" font-weight="bold" color="#047857" align="center">
              {{ points_multiplier }}배 포인트 적립
            </mj-text>
            <mj-text font-size="16px" color="#065f46" align="center">
              모든 구매 시<br/>
              {{ event_start }} - {{ event_end }}
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          예시 적립 금액:
        </mj-text>

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="4px" padding="15px">
          <mj-column>
            <mj-text font-size="14px" color="{{ theme.color.text|default:'#4b5563' }}">
              $50 사용 → 일반적으로 {{ example_points_normal }} 포인트 적립<br/>
              <strong style="color: #047857;">이벤트 기간 중 → {{ example_points_bonus }} 포인트 적립! 🎉</strong>
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="20px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="4px" padding="15px">
          <mj-column>
            <mj-text font-size="14px" color="{{ theme.color.text|default:'#4b5563' }}">
              $100 사용 → 일반적으로 {{ example_points_normal_2 }} 포인트 적립<br/>
              <strong style="color: #047857;">이벤트 기간 중 → {{ example_points_bonus_2 }} 포인트 적립! 🎉</strong>
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          현재 보유 포인트:
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}">
          <strong>포인트:</strong> {{ current_points }} 포인트<br/>
          <strong>등급:</strong> {{ loyalty_tier }}
        </mj-text>

        <mj-spacer height="30px" />

        <mj-button href="{{ shop_url }}" background-color="#dc2626" color="#ffffff" font-size="18px" font-weight="bold" border-radius="6px" padding="18px 50px">
          지금 바로 쇼핑하고 {{ points_multiplier }}배 포인트 적립
        </mj-button>

        <mj-spacer height="20px" />

        <mj-text font-size="13px" color="#dc2626" align="center" font-weight="bold">
          이벤트 종료: {{ event_end }} - 놓치지 마세요!
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
🔥 2배 포인트 이벤트!
{{ event_start }} - {{ event_end }}

충성도 멤버 전용!

안녕하세요, {{ customer_name }},

지금 바로 큰 혜택을 받아가세요! 제한된 기간 동안, 모든 구매 시 {{ points_multiplier }}배 포인트를 적립할 수 있습니다.

{{ points_multiplier }}배 포인트 적립
모든 구매 시
{{ event_start }} - {{ event_end }}

예시 적립 금액:
- $50 사용 → 일반적으로 {{ example_points_normal }} 포인트 적립
  이벤트 기간 중 → {{ example_points_bonus }} 포인트 적립! 🎉

- $100 사용 → 일반적으로 {{ example_points_normal_2 }} 포인트 적립
  이벤트 기간 중 → {{ example_points_bonus_2 }} 포인트 적립! 🎉

현재 보유 포인트:
- 포인트: {{ current_points }} 포인트
- 등급: {{ loyalty_tier }}

지금 바로 쇼핑하고 {{ points_multiplier }}배 포인트 적립: {{ shop_url }}

이벤트 종료: {{ event_end }} - 놓치지 마세요!