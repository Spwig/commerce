---
template_type: affiliate_commission_reversed
category: Affiliate Program
---

# Email Template: affiliate_commission_reversed

## Subject
手数料が戻されました - 注文番号 #{{ order_number }}

## HTML Content
<mjml>
  <mj-head>
    <mj-attributes>
      <mj-text font-family="Arial, sans-serif" line-height="1.6" />
      <mj-all font-family="Arial, sans-serif" />
    </mj-attributes>
  </mj-head>
  <mj-body background-color="#f8f9fa">
    <!-- Header -->
    <mj-section background-color="#ffffff" padding="40px 20px">
      <mj-column>
        <mj-text font-size="32px" font-weight="bold" color="#212529" align="center">
          手数料が戻されました
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Content -->
    <mj-section background-color="#ffffff" padding="20px">
      <mj-column>
        <mj-text font-size="16px" color="#212529">
          こんにちは {{ affiliate_name }}、
        </mj-text>
        <mj-text font-size="16px" color="#212529">
          顧客の返金により、注文番号 #{{ order_number }} ({{ commission_amount }}) の手数料が戻されました。
        </mj-text>
        <mj-text font-size="16px" color="#212529">
          顧客が返金を依頼した場合、関連する手数料は自動的に戻されるため、正確な会計を保証しています。
        </mj-text>
        <mj-text font-size="16px" color="#212529">
          これはアフィリエイトプロセスの通常の一部です。新しい手数料を獲得するために、{{ shop_name }} の宣伝を続けてください！
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- CTA -->
    <mj-section background-color="#ffffff" padding="30px 20px">
      <mj-column>
        <mj-button background-color="#007bff" color="#ffffff" href="{{ portal_url }}">
          アフィリエイトダッシュボードを表示
        </mj-button>
      </mj-column>
    </mj-section>

    <!-- Footer -->
    <mj-section background-color="#f8f9fa" padding="20px">
      <mj-column>
        <mj-text font-size="12px" color="#6c757d" align="center">
          {{ shop_name }}<br/>
          ご質問は? <a href="mailto:{{ support_email }}" style="color: #007bff;">
            サポートに連絡
          </a>
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
手数料が戻されました - 注文番号 #{{ order_number }}

こんにちは {{ affiliate_name }}、

顧客の返金により、注文番号 #{{ order_number }} ({{ commission_amount }}) の手数料が戻されました。

顧客が返金を依頼した場合、関連する手数料は自動的に戻されるため、正確な会計を保証しています。

これはアフィリエイトプロセスの通常の一部です。新しい手数料を獲得するために、{{ shop_name }} の宣伝を続けてください！

アフィリエイトダッシュボードを表示: {{ portal_url }}

{{ shop_name }}
ご質問は? サポートに連絡: {{ support_email }}