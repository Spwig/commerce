---
template_type: pos_shift_closed_report
category: POS
---

# Email Template: pos_shift_closed_report

## Subject
📊 班次报告：{{ terminal_name }} - {{ shift_date }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#eff6ff">
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="#1e40af" align="center">
          📊 班次已关闭
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="18px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          班次摘要报告
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}">
          班次在{{ terminal_name }}由{{ cashier_name }}关闭。
        </mj-text>

        <mj-spacer height="30px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
              班次详情：
            </mj-text>
            <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>终端：</strong>{{ terminal_name }}<br/>
              <strong>收银员：</strong>{{ cashier_name }}<br/>
              <strong>开始时间：</strong>{{ shift_started }}<br/>
              <strong>结束时间：</strong>{{ shift_ended }}<br/>
              <strong>持续时间：</strong>{{ shift_duration }}
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          销售摘要：
        </mj-text>

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>总销售额：</strong>{{ total_sales }}<br/>
              <strong>交易次数：</strong>{{ transaction_count }}<br/>
              <strong>售出商品数：</strong>{{ items_sold }}<br/>
              <strong>平均销售额：</strong>{{ average_sale }}<br/>
              <strong>收取税款：</strong>{{ tax_collected }}
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          支付方式明细：
        </mj-text>

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="15px">
          <mj-column>
            {% for payment in payment_methods %}
            <mj-text font-size="14px" color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>{{ payment.method }}：</strong>{{ payment.amount }} （{{ payment.count }} 次交易）
            </mj-text>
            {% endfor %}
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          现金核对：
        </mj-text>

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>初始现金：</strong>{{ opening_cash }}<br/>
              <strong>现金销售额：</strong>{{ cash_sales }}<br/>
              <strong>预期现金：</strong>{{ expected_cash }}<br/>
              <strong>清点现金：</strong>{{ counted_cash }}<br/>
              <strong>差异：</strong><span style="color: {{ cash_difference_color }};">{{ cash_difference }}</span>
            </mj-text>
          </mj-column>
        </mj-section>

        {% if discrepancy_amount != 0 %}
        <mj-spacer height="20px" />
        <mj-section background-color="#fef3c7" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="14px" color="#92400e" font-weight="bold">
              ⚠️ 现金差异：{{ discrepancy_amount }}
            </mj-text>
            {% if discrepancy_note %}
            <mj-text font-size="14px" color="#92400e">
              备注：{{ discrepancy_note }}
            </mj-text>
            {% endif %}
          </mj-column>
        </mj-section>
        {% endif %}

        <mj-spacer height="30px" />

        <mj-button href="{{ shift_report_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          查看完整报告
        </mj-button>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
📊 班次已关闭

班次摘要报告

班次在{{ terminal_name }}由{{ cashier_name }}关闭。

班次详情：
- 终端：{{ terminal_name }}
- 收银员：{{ cashier_name }}
- 开始时间：{{ shift_started }}
- 结束时间：{{ shift_ended }}
- 持续时间：{{ shift_duration }}

销售摘要：
- 总销售额：{{ total_sales }}
- 交易次数：{{ transaction_count }}
- 售出商品数：{{ items_sold }}
- 平均销售额：{{ average_sale }}
- 收取税款：{{ tax_collected }}

支付方式明细：
{% for payment in payment_methods %}
{{ payment.method }}：{{ payment.amount }} （{{ payment.count }} 次交易）
{% endfor %}

现金核对：
- 初始现金：{{ opening_cash }}
- 现金销售额：{{ cash_sales }}
- 预期现金：{{ expected_cash }}
- 清点现金：{{ counted_cash }}
- 差异：{{ cash_difference }}

{% if discrepancy_amount != 0 %}
⚠️ 现金差异：{{ discrepancy_amount }}
{% if discrepancy_note %}备注：{{ discrepancy_note }}{% endif %}
{% endif %}

查看完整报告：{{ shift_report_url }}