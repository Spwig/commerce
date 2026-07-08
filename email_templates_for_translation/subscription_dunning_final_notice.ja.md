---
template_type: subscription_dunning_final_notice
category: Subscriptions
---

# Email Template: subscription_dunning_final_notice

## Subject
⚠️ 最終通知: ご契約は{{ days_until_cancellation }}日後にキャンセルされます

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#fee2e2">
      <mj-column>
        <mj-text font-size="22px" font-weight="bold" color="#991b1b" align="center">
          ⚠️ 最終通知
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="18px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          ご契約のキャンセルが迫っています
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          こんにちは {{ customer_name }}、
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          これは最終のお知らせです。{{ plan_name }} ご契約の支払い処理が出来ませんでした。{{ days_until_cancellation }} 日以内に支払いを受信できなかった場合、ご契約はキャンセルされます。
        </mj-text>

        <mj-spacer height="30px" />

        <mj-section background-color="#fee2e2" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="#991b1b" font-size="16px">
              ⚠️ 支払い失敗 - 行動が必要です
            </mj-text>
            <mj-text color="#991b1b">
              <strong>Subscription:</strong> {{ plan_name }}<br/>
              <strong>Amount Due:</strong> {{ amount_due }}<br/>
              <strong>Failed Attempts:</strong> {{ retry_count }}<br/>
              <strong>Last Attempt:</strong> {{ last_retry_date }}<br/>
              <strong>Cancellation Date:</strong> <span style="font-weight: bold; font-size: 16px;">{{ cancellation_date }}</span>
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          支払いエラー:
        </mj-text>

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="14px" font-family="monospace" color="{{ theme.color.text|default:'#4b5563' }}">
              {{ payment_error_message }}
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          何が起こるか:
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}" line-height="1.8">
          {{ cancellation_date }} までに支払いを受信しない場合:<br/>
          • ご契約はキャンセルされます<br/>
          • すべてのサブスクリプションの利益へのアクセス権を失います<br/>
          • データが削除される可能性があります（保持ポリシーをご覧ください）<br/>
          • 再度サブスクライブする必要がありますアクセスを再開するため
        </mj-text>

        <mj-spacer height="30px" />

        <mj-text font-size="18px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}" align="center">
          今すぐ支払い方法を更新してください
        </mj-text>

        <mj-spacer height="20px" />

        <mj-button href="{{ update_payment_url }}" background-color="#dc2626" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          支払い方法を更新
        </mj-button>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          一般的な問題と解決策:
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}" line-height="1.8">
          • <strong>有効期限切れのカード:</strong> 現在のクレジットカードで更新してください<br/>
          • <strong>資金不足:</strong> 十分な残高を確認してください<br/>
          • <strong>カードが拒否されました:</strong> 銀行にお問い合わせください、または別のカードをご利用ください<br/>
          • <strong>住所が一致しません:</strong> 請求先住所がカードと一致することを確認してください
        </mj-text>

        <mj-spacer height="30px" />

        <mj-section background-color="#eff6ff" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="14px" color="#1e40af" font-weight="bold">
              お手伝いが必要ですか？
            </mj-text>
            <mj-text font-size="14px" color="#1e40af" line-height="1.6">
              支払いに問題が発生している場合、またはお手伝いが必要な場合は、すぐにサポートチームにお問い合わせください。
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="20px" />

        <mj-button href="{{ support_url }}" background-color="#6b7280" color="#ffffff" font-size="14px" border-radius="6px" padding="10px 25px">
          サポートに連絡
        </mj-button>

        <mj-spacer height="30px" />

        <mj-text font-size="13px" color="{{ theme.color.text_secondary|default:'#6b7280' }}" align="center">
          ご契約をキャンセルしたい場合は、アカウント設定でキャンセルできます。
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
⚠️ 最終通知

ご契約のキャンセルが迫っています

こんにちは {{ customer_name }}、

これは最終のお知らせです。{{ plan_name }} ご契約の支払い処理が出来ませんでした。{{ days_until_cancellation }} 日以内に支払いを受信できなかった場合、ご契約はキャンセルされます。

⚠️ PAYMENT FAILED - ACTION REQUIRED:
- Subscription: {{ plan_name }}
- Amount Due: {{ amount_due }}
- Failed Attempts: {{ retry_count }}
- Last Attempt: {{ last_retry_date }}
- Cancellation Date: {{ cancellation_date }}

PAYMENT ERROR:
{{ payment_error_message }}

WHAT WILL HAPPEN:
{{ cancellation_date }} までに支払いを受信しない場合:
• ご契約はキャンセルされます
• すべてのサブスクリプションの利益へのアクセス権を失います
• データが削除される可能性があります（保持ポリシーをご覧ください）
• 再度サブスクライブする必要がありますアクセスを再開するため

UPDATE YOUR PAYMENT METHOD NOW

Common Issues & Solutions:
• 有効期限切れのカード: 現在のクレジットカードで更新してください
• 資金不足: 十分な残高を確認してください
• カードが拒否されました: 銀行にお問い合わせください、または別のカードをご利用ください
• 住所が一致しません: 請求先住所がカードと一致することを確認してください

NEED HELP?:
支払いに問題が発生している場合、またはお手伝いが必要な場合は、すぐにサポートチームにお問い合わせください。

Update payment method: {{ update_payment_url }}
Contact support: {{ support_url }}

ご契約をキャンセルしたい場合は、アカウント設定でキャンセルできます。