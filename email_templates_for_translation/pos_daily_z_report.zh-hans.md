---
template_type: pos_daily_z_report
category: POS
---

# Email Template: pos_daily_z_report

## Subject
📊 每日Z报告 - {{ report_date }} - {{ location_name }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#eff6ff">
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="#1e40af" align="center">
          📊 每日Z报告
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="18px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          结束日结算报告
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}">
          {{ location_name }} 在 {{ report_date }} 的每日摘要。
        </mj-text>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          销售摘要：
        </mj-text>

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>总销售额：</strong> <span style="font-size: 20px; font-weight: bold; color: #059669;">{{ total_sales }}</span><br/>
              <strong>交易次数：</strong> {{ transaction_count }}<br/>
              <strong>售出商品数量：</strong> {{ items_sold }}<br/>
              <strong>平均销售额：</strong> {{ average_sale }}<br/>
              <strong>已收税款：</strong> {{ tax_collected }}
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          支付方式：
        </mj-text>

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="15px">
          <mj-column>
            {% for payment in payment_methods %}
            <mj-text font-size="14px" color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>{{ payment.method }}：</strong> {{ payment.amount }}（{{ payment.count }} 次交易）
            </mj-text>
            {% endfor %}
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          班次摘要：
        </mj-text>

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>总班次：</strong> {{ shift_count }}<br/>
              <strong>使用的终端机数量：</strong> {{ terminal_count }}<br/>
              <strong>当前收银员数量：</strong> {{ cashier_count }}
            </mj-text>
          </mj-column>
        </mj-section>

        {% for terminal in terminal_stats %}
        <mj-spacer height="15px" />
        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="15px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
              {{ terminal.name }}
            </mj-text>
            <mj-text font-size="14px" color="{{ theme.color.text|default:'#4b5563' }}">
              销售额：{{ terminal.sales }} | 交易次数：{{ terminal.transactions }}
            </mj-text>
          </mj-column>
        </mj-section>
        {% endfor %}

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          调整与折扣：
        </mj-text>

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>给予的折扣：</strong> {{ discounts_total }}<br/>
              <strong>发出的退款：</strong> {{ refunds_total }}<br/>
              <strong>作废交易：</strong> {{ voids_total }}
            </mj-text>
          </mj-column>
        </mj-section>

        {% if cash_variance != 0 %}
        <mj-spacer height="20px" />
        <mj-section background-color="#fef3c7" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="14px" color="#92400e" font-weight="bold">
              ⚠️ 总现金差异：{{ cash_variance }}
            </mj-text>
            <mj-text font-size="14px" color="#92400e">
              {{ variance_note }}
            </mj-text>
          </mj-column>
        </mj-section>
        {% endif %}

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          销售额最高的产品：
        </mj-text>

        {% for product in top_products %}
        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="12px">
          <mj-column>
            <mj-text font-size="14px" color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>{{ product.rank }}. {{ product.name }}</strong> - {{ product.quantity }} 件售出（{{ product.revenue }}）
            </mj-text>
          </mj-column>
        </mj-section>
        <mj-spacer height="8px" />
        {% endfor %}

        <mj-spacer height="30px" />

        <mj-button href="{{ full_report_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          查看完整报告
        </mj-button>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
📊 每日Z报告

结束日结算报告

{{ location_name }} 在 {{ report_date }} 的每日摘要。

销售摘要：
- 总销售额：{{ total_sales }}
- 交易次数：{{ transaction_count }}
- 售出商品数量：{{ items_sold }}
- 平均销售额：{{ average_sale }}
- 已收税款：{{ tax_collected }}

支付方式：
{% for payment in payment_methods %}
{{ payment.method }}：{{ payment.amount }}（{{ payment.count }} 次交易）
{% endfor %}

班次摘要：
- 总班次：{{ shift_count }}
- 使用的终端机数量：{{ terminal_count }}
- 当前收银员数量：{{ cashier_count }}

终端机明细：
{% for terminal in terminal_stats %}
{{ terminal.name }}：{{ terminal.sales }} | {{ terminal.transactions }} 次交易
{% endfor %}

调整与折扣：
- 给予的折扣：{{ discounts_total }}
- 发出的退款：{{ refunds_total }}
- 作废交易：{{ voids_total }}

{% if cash_variance != 0 %}
⚠️ 总现金差异：{{ cash_variance }}
{{ variance_note }}
{% endif %}

销售额最高的产品：
{% for product in top_products %}
{{ product.rank }}. {{ product.name }} - {{ product.quantity }} 件售出（{{ product.revenue }}）
{% endfor %}

查看完整报告：{{ full_report_url }}