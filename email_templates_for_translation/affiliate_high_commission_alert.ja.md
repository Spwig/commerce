---
template_type: affiliate_high_commission_alert
category: Affiliate Program
---

# Email Template: affiliate_high_commission_alert

## Subject
⚠️ 通常でない手数料活動の検出 - {{ affiliate_name }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#fef3c7">
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="#92400e" align="center">
          ⚠️ 高い手数料のアラート
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="18px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          通常でない活動の検出
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}">
          アフィリエイター {{ affiliate_name }} が異常に高い手数料を獲得しました。これは、詐欺の防止のために確認が必要です。
        </mj-text>

        <mj-spacer height="20px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
              アラートの詳細:
            </mj-text>
            <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>アフィリエイター:</strong> {{ affiliate_name }} ({{ affiliate_id }})<br/>
              <strong>手数料額:</strong> <span style="font-weight: bold; color: #dc2626;">{{ commission_amount }}</span><br/>
              <strong>注文金額:</strong> {{ order_value }}<br/>
              <strong>注文ID:</strong> {{ order_number }}<br/>
              <strong>検出日時:</strong> {{ detected_at }}
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          なぜフラグが立たれたか:
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}" line-height="1.8">
          {{ flag_reason }}
        </mj-text>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          お勧めのアクション:
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}" line-height="1.8">
          • 注文の詳細を確認して正当性をチェック<br/>
          • アフィリエイターの紹介履歴を確認<br/>
          • 顧客が紹介者と関連していないことを確認<br/>
          • 管理パネルで手数料を承認または拒否
        </mj-text>

        <mj-spacer height="30px" />

        <mj-button href="{{ review_commission_url }}" background-color="#dc2626" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          手数料の確認
        </mj-button>

        <mj-spacer height="10px" />

        <mj-button href="{{ affiliate_details_url }}" background-color="#6b7280" color="#ffffff" font-size="14px" border-radius="6px" padding="10px 25px">
          アフィリエイターの詳細を確認
        </mj-button>

        <mj-spacer height="20px" />

        <mj-text font-size="13px" color="{{ theme.color.text_secondary|default:'#6b7280' }}" align="center">
          この手数料は確認待ちで、承認されるまで支払われません。
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
⚠️ 高い手数料のアラート

通常でない活動の検出

アフィリエイター {{ affiliate_name }} が異常に高い手数料を獲得しました。これは、詐欺の防止のために確認が必要です。

アラートの詳細:
- アフィリエイター: {{ affiliate_name }} ({{ affiliate_id }})
- 手数料額: {{ commission_amount }}
- 注文金額: {{ order_value }}
- 注文ID: {{ order_number }}
- 検出日時: {{ detected_at }}

なぜフラグが立たれたか:
{{ flag_reason }}

お勧めのアクション:
• 注文の詳細を確認して正当性をチェック
• アフィリエイターの紹介履歴を確認
• 顧客が紹介者と関連していないことを確認
• 管理パネルで手数料を承認または拒否

手数料の確認: {{ review_commission_url }}
アフィリエイターの詳細を確認: {{ affiliate_details_url }}

この手数料は確認待ちで、承認されるまで支払われません。