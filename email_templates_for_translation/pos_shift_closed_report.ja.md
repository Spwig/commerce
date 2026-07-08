---
template_type: pos_shift_closed_report
category: POS
---

# Email Template: pos_shift_closed_report

## Subject
📊 シフトレポート: {{ terminal_name }} - {{ shift_date }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#eff6ff">
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="#1e40af" align="center">
          📊 シフト終了
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="18px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          シフト概要レポート
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}">
          {{ terminal_name }} のシフトを {{ cashier_name }} により終了しました。
        </mj-text>

        <mj-spacer height="30px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
              シフトの詳細:
            </mj-text>
            <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>端末:</strong> {{ terminal_name }}<br/>
              <strong>レジ:</strong> {{ cashier_name }}<br/>
              <strong>開始:</strong> {{ shift_started }}<br/>
              <strong>終了:</strong> {{ shift_ended }}<br/>
              <strong>所要時間:</strong> {{ shift_duration }}
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          売上概要:
        </mj-text>

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>総売上:</strong> {{ total_sales }}<br/>
              <strong>取引件数:</strong> {{ transaction_count }}<br/>
              <strong>販売商品数:</strong> {{ items_sold }}<br/>
              <strong>平均売上:</strong> {{ average_sale }}<br/>
              <strong>徴収税金:</strong> {{ tax_collected }}
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          支払いの明細:
        </mj-text>

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="15px">
          <mj-column>
            {% for payment in payment_methods %}
            <mj-text font-size="14px" color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>{{ payment.method }}:</strong> {{ payment.amount }} ({{ payment.count }} 取引)
            </mj-text>
            {% endfor %}
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          現金の照合:
        </mj-text>

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>初期現金:</strong> {{ opening_cash }}<br/>
              <strong>現金売上:</strong> {{ cash_sales }}<br/>
              <strong>予想現金:</strong> {{ expected_cash }}<br/>
              <strong>数えた現金:</strong> {{ counted_cash }}<br/>
              <strong>差額:</strong> <span style="color: {{ cash_difference_color }};">{{ cash_difference }}</span>
            </mj-text>
          </mj-column>
        </mj-section>

        {% if discrepancy_amount != 0 %}
        <mj-spacer height="20px" />
        <mj-section background-color="#fef3c7" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="14px" color="#92400e" font-weight="bold">
              ⚠️ 現金の不一致: {{ discrepancy_amount }}
            </mj-text>
            {% if discrepancy_note %}
            <mj-text font-size="14px" color="#92400e">
              ノート: {{ discrepancy_note }}
            </mj-text>
            {% endif %}
          </mj-column>
        </mj-section>
        {% endif %}

        <mj-spacer height="30px" />

        <mj-button href="{{ shift_report_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          詳細レポートを表示
        </mj-button>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
📊 シフト終了

シフト概要レポート

{{ terminal_name }} のシフトを {{ cashier_name }} により終了しました。

シフトの詳細:
- 端末: {{ terminal_name }}
- レジ: {{ cashier_name }}
- 開始: {{ shift_started }}
- 終了: {{ shift_ended }}
- 所要時間: {{ shift_duration }}

売上概要:
- 総売上: {{ total_sales }}
- 取引件数: {{ transaction_count }}
- 販売商品数: {{ items_sold }}
- 平均売上: {{ average_sale }}
- 徴収税金: {{ tax_collected }}

支払いの明細:
{% for payment in payment_methods %}
{{ payment.method }}: {{ payment.amount }} ({{ payment.count }} 取引)
{% endfor %}

現金の照合:
- 初期現金: {{ opening_cash }}
- 現金売上: {{ cash_sales }}
- 予想現金: {{ expected_cash }}
- 数えた現金: {{ counted_cash }}
- 差額: {{ cash_difference }}

{% if discrepancy_amount != 0 %}
⚠️ 現金の不一致: {{ discrepancy_amount }}
{% if discrepancy_note %}ノート: {{ discrepancy_note }}{% endif %}
{% endif %}

詳細レポートを表示: {{ shift_report_url }}