---
template_type: return_request_confirmation
category: Returns
---

# Email Template: return_request_confirmation

## Subject
返品依頼を受け付けました - 注文 #{{ order_number }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="{{ theme.color.surface|default:'#eff6ff' }}">
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="{{ theme.color.text|default:'#1e40af' }}">
          返品依頼を受け付けました
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text|default:'#1e40af' }}">
          注文 #{{ order_number }}
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          こんにちは {{ customer_name }}、
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          注文 <strong>#{{ order_number }}</strong> に関する返品依頼を受け付けました。
        </mj-text>

        <mj-spacer height="20px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
              返品の詳細:
            </mj-text>
            <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>理由:</strong> {{ return_reason }}<br/>
              <strong>商品:</strong> {{ items_count }} 品目<br/>
              <strong>ステータス:</strong> {{ return_status }}
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="20px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          次の手順は?
        </mj-text>

        <mj-text font-size="15px" line-height="1.8" color="{{ theme.color.text|default:'#4b5563' }}">
          1. 私たちのチームが24〜48時間以内に返品依頼を確認します<br/>
          2. 承認後、返品用の配送ラベルをメールで送信します<br/>
          3. 商品を安全に梱包し、返品ラベルを貼り付けます<br/>
          4. 最寄りの配送拠点にパッケージを届けます<br/>
          5. 商品を受け取り、検査が完了した後、返金が処理されます
        </mj-text>

        <mj-spacer height="20px" />

        <mj-text font-size="15px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          ご質問があれば、どうぞお気軽にお問い合わせください。
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
返品依頼を受け付けました
注文 #{{ order_number }}

こんにちは {{ customer_name }}、

注文 #{{ order_number }} に関する返品依頼を受け付けました。

返品の詳細:
- 理由: {{ return_reason }}
- 商品: {{ items_count }} 品目
- ステータス: {{ return_status }}

WHAT HAPPENS NEXT?
1. 私たちのチームが24〜48時間以内に返品依頼を確認します
2. 承認後、返品用の配送ラベルをメールで送信します
3. 商品を安全に梱包し、返品ラベルを貼り付けます
4. 最寄りの配送拠点にパッケージを届けます
5. 商品を受け取り、検査が完了した後、返金が処理されます

ご質問があれば、どうぞお気軽にお問い合わせください。