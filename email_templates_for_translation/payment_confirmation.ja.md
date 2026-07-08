---
template_type: payment_confirmation
category: Core E-commerce
---

# Email Template: payment_confirmation

## Subject
支払いが確認されました - 注文番号 #{{ order_number }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section>
      <mj-column>
        <mj-text font-size="20px" font-weight="bold">
          支払いが確認されました
        </mj-text>
        <mj-text>
          注文番号 #{{ order_number }} に関するお支払いが正常に処理されました。
        </mj-text>
        <mj-text>
          <strong>支払った金額:</strong> {{ amount_paid }}
        </mj-text>
        <mj-text>
          <strong>支払い方法:</strong> {{ payment_method }}
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
支払いが確認されました

注文番号 #{{ order_number }} に関するお支払いが正常に処理されました。

支払った金額: {{ amount_paid }}
支払い方法: {{ payment_method }}