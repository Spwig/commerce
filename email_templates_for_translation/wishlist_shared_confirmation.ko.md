---
template_type: wishlist_shared_confirmation
category: Wishlist
---

# Email Template: wishlist_shared_confirmation

## Subject
✓ {{ shop_name }}에서 위시리스트 공유 완료

## HTML Content
<mjml>
  <mj-body>
    <mj-section>
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          ✓ 위시리스트가 성공적으로 공유되었습니다!
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          안녕하세요, {{ customer_name }}!
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          {{ wishlist_item_count }}개의 항목이 포함된 위시리스트가 성공적으로 공유되었습니다. 아래 링크를 통해 다른 사람들이 이제 귀하의 위시리스트를 볼 수 있습니다.
        </mj-text>

        <mj-spacer height="30px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
              공유 링크:
            </mj-text>
            <mj-text font-family="'Courier New', monospace" font-size="14px" color="{{ theme.color.primary|default:'#2563eb' }}">
              {{ share_url }}
            </mj-text>
            <mj-spacer height="15px" />
            <mj-button href="{{ share_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="14px" border-radius="6px" padding="10px 25px">
              링크 복사
            </mj-button>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          공유 내용:
        </mj-text>

        <mj-text font-size="14px" color="{{ theme.color.text|default:'#4b5563' }}">
          • 위시리스트 이름 (설정한 경우)<br/>
          • {{ wishlist_item_count }}개의 상품<br/>
          • 상품 이름, 이미지, 가격<br/>
          • 각 항목의 구매 링크
        </mj-text>

        <mj-spacer height="30px" />

        <mj-section background-color="#f0fdf4" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="14px" color="#065f46" align="center">
              💡 친구와 가족과 선물이나 특별한 기념일을 위해 공유하기에 완벽합니다!
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-button href="{{ wishlist_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" border-radius="6px" padding="12px 30px">
          내 위시리스트 관리
        </mj-button>

        <mj-spacer height="20px" />

        <mj-text font-size="13px" color="{{ theme.color.text_secondary|default:'#6b7280' }}" align="center">
          더 이상 공유하고 싶지 않다면, 언제든지 <a href="{{ wishlist_settings_url }}">위시리스트 설정</a>에서 공유 링크를 비활성화할 수 있습니다.
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
✓ 위시리스트 공유 완료!

안녕하세요, {{ customer_name }}!

{{ wishlist_item_count }}개의 항목이 포함된 위시리스트가 성공적으로 공유되었습니다. 아래 링크를 통해 다른 사람들이 이제 귀하의 위시리스트를 볼 수 있습니다.

공유 링크:
{{ share_url }}

공유 내용:
• 위시리스트 이름 (설정한 경우)
• {{ wishlist_item_count }}개의 상품
• 상품 이름, 이미지, 가격
• 각 항목의 구매 링크

💡 친구와 가족과 선물이나 특별한 기념일을 위해 공유하기에 완벽합니다!

내 위시리스트 관리: {{ wishlist_url }}

더 이상 공유하고 싶지 않다면, 언제든지 위시리스트 설정에서 공유 링크를 비활성화할 수 있습니다: {{ wishlist_settings_url }}