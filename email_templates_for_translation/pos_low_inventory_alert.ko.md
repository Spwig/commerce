---
template_type: pos_low_inventory_alert
category: POS
---

# Email Template: pos_low_inventory_alert

## Subject
📦 재고 부족 경고: {{ location_name }}에서 {{ product_count }}개의 상품{{ product_count|pluralize }}이 부족합니다

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#fef3c7">
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="#92400e" align="center">
          📦 재고 부족 경고
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="18px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          재고 부족
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}">
          {{ product_count }}개의 상품{{ product_count|pluralize }} {{ product_count|pluralize:'is,are' }}이 {{ location_name }}에서 부족합니다.
        </mj-text>

        <mj-spacer height="20px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
              경고 세부 정보:
            </mj-text>
            <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>위치:</strong> {{ location_name }}<br/>
              <strong>영향을 받은 상품:</strong> {{ product_count }}<br/>
              <strong>감지 시간:</strong> {{ detected_at }}
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          재고 부족 상품:
        </mj-text>

        {% for item in low_stock_items %}
        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="15px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
              {{ item.product_name }}
            </mj-text>
            <mj-text font-size="14px" color="{{ theme.color.text|default:'#4b5563' }}">
              {% if item.variant_name %}<strong>변형:</strong> {{ item.variant_name }}<br/>{% endif %}
              <strong>현재 재고:</strong> <span style="color: #dc2626; font-weight: bold;">{{ item.current_stock }}</span><br/>
              <strong>재주문 수준:</strong> {{ item.reorder_point }}<br/>
              <strong>SKU:</strong> {{ item.sku }}
            </mj-text>
          </mj-column>
        </mj-section>
        <mj-spacer height="10px" />
        {% endfor %}

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          권장 조치:
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}" line-height="1.8">
          • 재고 부족 상품에 대한 구매 주문서 생성<br/>
          • 다른 위치에서 재고 이전<br/>
          • 필요 시 재주문 수준 업데이트<br/>
          • 필요 시 파 레벨 조정 고려
        </mj-text>

        <mj-spacer height="30px" />

        <mj-button href="{{ inventory_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          재고 확인
        </mj-button>

        <mj-spacer height="10px" />

        <mj-button href="{{ purchase_orders_url }}" background-color="#6b7280" color="#ffffff" font-size="14px" border-radius="6px" padding="10px 25px">
          구매 주문서 생성
        </mj-button>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
📦 재고 부족 경고

재고 부족

{{ product_count }}개의 상품{{ product_count|pluralize }} {{ product_count|pluralize:'is,are' }}이 {{ location_name }}에서 부족합니다.

경고 세부 정보:
- 위치: {{ location_name }}
- 영향을 받은 상품: {{ product_count }}
- 감지 시간: {{ detected_at }}

재고 부족 상품:
{% for item in low_stock_items %}
{{ item.product_name }}
{% if item.variant_name %}변형: {{ item.variant_name }}{% endif %}
현재 재고: {{ item.current_stock }}
재주문 수준: {{ item.reorder_point }}
SKU: {{ item.sku }}

{% endfor %}

권장 조치:
• 재고 부족 상품에 대한 구매 주문서 생성
• 다른 위치에서 재고 이전
• 필요 시 재주문 수준 업데이트
• 필요 시 파 레벨 조정 고려

재고 확인: {{ inventory_url }}
구매 주문서 생성: {{ purchase_orders_url }}