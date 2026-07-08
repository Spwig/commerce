---
template_type: return_received
category: Returns
---

# Email Template: return_received

## Subject
返品を受け取りました - 注文 #{{ order_number }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="{{ theme.color.surface|default:'#eff6ff' }}">
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="{{ theme.color.primary|default:'#1d4ed8' }}">
          返品を受け取りました
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.primary|default:'#1d4ed8' }}">
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
          注文 <strong>#{{ order_number }}</strong> に関する返品品を受け取りました。
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          <strong>今後のお手続き：</strong>
        </mj-text>

        <mj-text font-size="15px" line-height="1.8" color="{{ theme.color.text|default:'#4b5563' }}">
          1. スタッフが返品品を2〜3営業日以内に検査します<br/>
          2. 商品が元の状態であることを確認します<br/>
          3. 検査が完了したら、返金手続きを行います<br/>
          4. 返金が完了した後、確認メールをお送りします
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          返金は、元の支払い方法に反映され、5〜10営業日かかる場合があります。
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          ご理解とご協力に感謝いたします。
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
返品を受け取りました - 注文 #{{ order_number }}

こんにちは {{ customer_name }}、

注文 #{{ order_number }} に関する返品品を受け取りました。

今後のお手続き：
1. スタッフが返品品を2〜3営業日以内に検査します
2. 商品が元の状態であることを確認します
3. 検査が完了したら、返金手続きを行います
4. 返金が完了した後、確認メールをお送りします

返金は、元の支払い方法に反映され、5〜10営業日かかる場合があります。

ご理解とご協力に感謝いたします。