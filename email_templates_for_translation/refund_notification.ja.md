---
template_type: refund_notification
category: Core E-commerce
---

# Email Template: refund_notification

## Subject
返金が処理されました - 注文番号 #{{ order_number }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section>
      <mj-column>
        <mj-text font-size="20px" font-weight="bold">
          返金が処理されました
        </mj-text>
        <mj-text>
          注文番号 #{{ order_number }} に対して返金が処理されました。
        </mj-text>
        <mj-text>
          <strong>返金額：</strong>{{ refund_amount }}
        </mj-text>
        <mj-text>
          返金は {{ refund_days }} 個の営業日以内にあなたのアカウントに表示されます。
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
返金が処理されました

注文番号 #{{ order_number }} に対して返金が処理されました。

返金額：{{ refund_amount }}

返金は {{ refund_days }} 個の営業日以内にあなたのアカウントに表示されます。