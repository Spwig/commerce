---
template_type: cart_recovered_thank_you
category: Cart Recovery
---

# Email Template: cart_recovered_thank_you

## Subject
注文番号 {{ order_number }} のご購入、ありがとうございます！ - {{ shop_name }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section>
      <mj-column>
        <mj-text font-size="24px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}" align="center">
          🎉 ご購入、ありがとうございます！
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          こんにちは {{ customer_name }}、
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          ご購入いただき、ありがとうございます！ご注文は確認済みで、出荷準備を進めています。
        </mj-text>

        <mj-spacer height="30px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
              注文の概要
            </mj-text>
            <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>注文番号:</strong> {{ order_number }}<br/>
              <strong>注文日:</strong> {{ order_date }}<br/>
              <strong>合計:</strong> {{ order_total }}
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-button href="{{ order_tracking_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          注文を追跡する
        </mj-button>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          次に何が起こるか？
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}" line-height="1.8">
          1. 注文を準備します（通常、1〜2営業日で完了します）<br/>
          2. 輸送確認と追跡情報が届きます<br/>
          3. 注文は以下に届けられます：{{ shipping_address }}
        </mj-text>

        <mj-spacer height="30px" />

        <mj-section background-color="#f0fdf4" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="14px" color="#065f46" align="center">
              💡 <strong>ご存知ですか？</strong><br/>
              いつでもアカウントダッシュボードで注文を追跡できます。
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="20px" />

        <mj-text font-size="14px" color="{{ theme.color.text_secondary|default:'#6b7280' }}" align="center">
          質問はありますか？<a href="{{ support_url }}" style="color: {{ theme.color.primary|default:'#2563eb' }};">サポートチームにお問い合わせください</a>
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
🎉 ご購入、ありがとうございます！

こんにちは {{ customer_name }}、

ご購入いただき、ありがとうございます！ご注文は確認済みで、出荷準備を進めています。

注文の概要：
- 注文番号: {{ order_number }}
- 注文日: {{ order_date }}
- 合計: {{ order_total }}

注文を追跡する: {{ order_tracking_url }}

次に何が起こるか？
1. 注文を準備します（通常、1〜2営業日で完了します）
2. 輸送確認と追跡情報が届きます
3. 注文は以下に届けられます：{{ shipping_address }}

💡 ご存知ですか？
いつでもアカウントダッシュボードで注文を追跡できます。

質問はありますか？サポートチームにお問い合わせください: {{ support_url }}

---
注文番号 {{ order_number }} で {{ shop_name }} でのご購入