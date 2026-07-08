---
template_type: pos_cash_discrepancy_alert
category: POS
---

# Email Template: pos_cash_discrepancy_alert

## Subject
⚠️ 现金差异警报：{{ terminal_name }} - {{ discrepancy_amount }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#fef3c7">
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="#92400e" align="center">
          ⚠️ 现金差异检测到
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="18px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          现金差异警报
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}">
          在 {{ terminal_name }} 结束班次时检测到 {{ discrepancy_amount }} 的现金差异。
        </mj-text>

        <mj-spacer height="20px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
              差异详情：
            </mj-text>
            <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>终端：</strong> {{ terminal_name }}<br/>
              <strong>收银员：</strong> {{ cashier_name }}<br/>
              <strong>班次日期：</strong> {{ shift_date }}<br/>
              <strong>班次时长：</strong> {{ shift_duration }}<br/>
              <strong>检测时间：</strong> {{ detected_at }}
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          现金统计：
        </mj-text>

        <mj-section background-color="#fef3c7" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text color="#92400e">
              <strong>预期现金：</strong> {{ expected_cash }}<br/>
              <strong>实际清点现金：</strong> {{ counted_cash }}<br/>
              <strong>差异：</strong> <span style="font-weight: bold; font-size: 18px;">{{ discrepancy_amount }}</span>
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="20px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="14px" color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>班次开始现金：</strong> {{ opening_cash }}<br/>
              <strong>现金销售额：</strong> {{ cash_sales }}<br/>
              <strong>现金退款：</strong> {{ cash_refunds }}<br/>
              <strong>现金支出：</strong> {{ cash_paid_out }}
            </mj-text>
          </mj-column>
        </mj-section>

        {% if cashier_note %}
        <mj-spacer height="30px" />
        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          收银员备注：
        </mj-text>
        <mj-section background-color="#eff6ff" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="14px" color="#1e40af" line-height="1.6">
              "{{ cashier_note }}"
            </mj-text>
          </mj-column>
        </mj-section>
        {% endif %}

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          建议操作：
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}" line-height="1.8">
          1. 检查交易历史记录是否有错误<br/>
          2. 检查是否有未记录的现金支付<br/>
          3. 确认现金清点是否准确<br/>
          4. 在班次备注中记录差异<br/>
          5. 如有必要，与收银员跟进
        </mj-text>

        <mj-spacer height="30px" />

        <mj-button href="{{ shift_report_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          查看班次报告
        </mj-button>

        <mj-spacer height="10px" />

        <mj-button href="{{ transaction_history_url }}" background-color="#6b7280" color="#ffffff" font-size="14px" border-radius="6px" padding="10px 25px">
          检查交易
        </mj-button>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
⚠️ 检测到现金差异

现金差异警报

在 {{ terminal_name }} 结束班次时检测到 {{ discrepancy_amount }} 的现金差异。

差异详情：
- 终端：{{ terminal_name }}
- 收银员：{{ cashier_name }}
- 班次日期：{{ shift_date }}
- 班次时长：{{ shift_duration }}
- 检测时间：{{ detected_at }}

现金统计：
- 预期现金：{{ expected_cash }}
- 实际清点现金：{{ counted_cash }}
- 差异：{{ discrepancy_amount }}

详细信息：
- 班次开始现金：{{ opening_cash }}
- 现金销售额：{{ cash_sales }}
- 现金退款：{{ cash_refunds }}
- 现金支出：{{ cash_paid_out }}

{% if cashier_note %}
收银员备注：
"{{ cashier_note }}"
{% endif %}

建议操作：
1. 检查交易历史记录是否有错误
2. 检查是否有未记录的现金支付
3. 确认现金清点是否准确
4. 在班次备注中记录差异
5. 如有必要，与收银员跟进

查看班次报告：{{ shift_report_url }}
检查交易：{{ transaction_history_url }}