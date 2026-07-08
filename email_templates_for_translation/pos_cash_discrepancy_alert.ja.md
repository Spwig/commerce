---
template_type: pos_cash_discrepancy_alert
category: POS
---

# Email Template: pos_cash_discrepancy_alert

## Subject
⚠️ 現金の不一致: {{ terminal_name }} - {{ discrepancy_amount }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#fef3c7">
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="#92400e" align="center">
          ⚠️ 現金の不一致が検出されました
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="18px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          現金の不一致アラート
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}">
          {{ terminal_name }} のシフト終了時に現金の不一致額 {{ discrepancy_amount }} が検出されました。
        </mj-text>

        <mj-spacer height="20px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
              不一致の詳細:
            </mj-text>
            <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>端末:</strong> {{ terminal_name }}<br/>
              <strong>レジ担当:</strong> {{ cashier_name }}<br/>
              <strong>シフト日:</strong> {{ shift_date }}<br/>
              <strong>シフト期間:</strong> {{ shift_duration }}<br/>
              <strong>検出日時:</strong> {{ detected_at }}
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          現金の実数:
        </mj-text>

        <mj-section background-color="#fef3c7" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text color="#92400e">
              <strong>予想現金:</strong> {{ expected_cash }}<br/>
              <strong>実際の現金:</strong> {{ counted_cash }}<br/>
              <strong>不一致額:</strong> <span style="font-weight: bold; font-size: 18px;">{{ discrepancy_amount }}</span>
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="20px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="14px" color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>シフト開始時現金:</strong> {{ opening_cash }}<br/>
              <strong>現金売上:</strong> {{ cash_sales }}<br/>
              <strong>現金返金:</strong> {{ cash_refunds }}<br/>
              <strong>支払った現金:</strong> {{ cash_paid_out }}
            </mj-text>
          </mj-column>
        </mj-section>

        {% if cashier_note %}
        <mj-spacer height="30px" />
        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          レジ担当のメモ:
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
          お勧めの対応策:
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}" line-height="1.8">
          1. トランザクション履歴を確認してエラーを確認してください<br/>
          2. 記録されていない現金支払いを確認してください<br/>
          3. 現金の実数が正確であることを確認してください<br/>
          4. シフトメモに不一致を記録してください<br/>
          5. 必要に応じてレジ担当者と連絡を取りましょう
        </mj-text>

        <mj-spacer height="30px" />

        <mj-button href="{{ shift_report_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          シフトレポートを表示
        </mj-button>

        <mj-spacer height="10px" />

        <mj-button href="{{ transaction_history_url }}" background-color="#6b7280" color="#ffffff" font-size="14px" border-radius="6px" padding="10px 25px">
          トランザクションを確認
        </mj-button>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
⚠️ 現金の不一致が検出されました

現金の不一致アラート

{{ terminal_name }} のシフト終了時に現金の不一致額 {{ discrepancy_amount }} が検出されました。

不一致の詳細:
- 端末: {{ terminal_name }}
- レジ担当: {{ cashier_name }}
- シフト日: {{ shift_date }}
- シフト期間: {{ shift_duration }}
- 検出日時: {{ detected_at }}

現金の実数:
- 予想現金: {{ expected_cash }}
- 実際の現金: {{ counted_cash }}
- 不一致額: {{ discrepancy_amount }}

BREAKDOWN:
- シフト開始時現金: {{ opening_cash }}
- 現金売上: {{ cash_sales }}
- 現金返金: {{ cash_refunds }}
- 支払った現金: {{ cash_paid_out }}

{% if cashier_note %}
CASHIER'S NOTE:
"{{ cashier_note }}"
{% endif %}

お勧めの対応策:
1. トランザクション履歴を確認してエラーを確認してください
2. 記録されていない現金支払いを確認してください
3. 現金の実数が正確であることを確認してください
4. シフトメモに不一致を記録してください
5. 必要に応じてレジ担当者と連絡を取りましょう

シフトレポートを表示: {{ shift_report_url }}
トランザクションを確認: {{ transaction_history_url }}