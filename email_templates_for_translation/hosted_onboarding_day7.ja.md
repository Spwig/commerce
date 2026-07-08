---
template_type: hosted_onboarding_day7
category: License
---

# Email Template: hosted_onboarding_day7

## Subject
販売を拡大しましょう - {{ store_name }}

## HTML Content
<mjml>
  <mj-head>
    <mj-attributes>
      <mj-all font-family="'Helvetica Neue', Helvetica, Arial, sans-serif" />
      <mj-text font-size="14px" color="#333333" line-height="20px" />
      <mj-section background-color="{{ theme.color.background|default:'#ffffff' }}" padding="20px" />
    </mj-attributes>
  </mj-head>
  <mj-body background-color="{{ theme.color.background_secondary|default:'#f9fafb' }}">
    <!-- Header -->
    <mj-section background-color="{{ theme.color.primary|default:'#2563eb' }}" padding="30px 20px">
      <mj-column>
        <mj-text font-size="28px" font-weight="bold" color="#ffffff" align="center">
          スタートアップ: マーケティングと成長
        </mj-text>
        <mj-text font-size="16px" color="#ffffffcc" align="center" padding-top="10px">
          {{ store_name }} へのトラフィックと販売促進を推進しましょう
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Greeting -->
    <mj-section>
      <mj-column>
        <mj-text font-size="16px">
          こんにちは {{ name|default:'there' }}、
        </mj-text>
        <mj-text>
          {{ store_name }} が形になってきたので、今からトラフィックを増やし、販売を拡大する時間です。以下に、最初のステップとしての5つのマーケティングのヒントを紹介します。
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Tip 1 -->
    <mj-section background-color="{{ theme.color.background_secondary|default:'#f9fafb' }}" padding="20px" border-radius="8px">
      <mj-column>
        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.primary|default:'#2563eb' }}" padding-bottom="5px">
          最初の割引コードを作成しましょう
        </mj-text>
        <mj-text font-size="14px">
          最初のお客様を惹きつけるために、ローンチ割引を提供してください。Marketing > Discount Codes にアクセスして、使用回数の制限や有効期限の設定が可能な割引コード（百分比または固定金額）を作成してください。
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Tip 2 -->
    <mj-section>
      <mj-column>
        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.primary|default:'#2563eb' }}" padding-bottom="5px">
          放置されたカートの回復を設定しましょう
        </mj-text>
        <mj-text font-size="14px">
          販売を自動的に回復しましょう。Marketing > Abandoned Carts で、放置されたカートの回復メールを有効にして、顧客に残した商品を思い出させるようにしてください。
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Tip 3 -->
    <mj-section background-color="{{ theme.color.background_secondary|default:'#f9fafb' }}" padding="20px" border-radius="8px">
      <mj-column>
        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.primary|default:'#2563eb' }}" padding-bottom="5px">
          あなたのソーシャルメディアアカウントを接続しましょう
        </mj-text>
        <mj-text font-size="14px">
          顧客が見つけてフォローできるように、あなたのソーシャルメディアプロフィールをストアにリンクしてください。Settings > Social Media でソーシャルリンクを追加し、ストアフッターに表示してください。
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Tip 4 -->
    <mj-section>
      <mj-column>
        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.primary|default:'#2563eb' }}" padding-bottom="5px">
          Google Analytics トラッキングを設定しましょう
        </mj-text>
        <mj-text font-size="14px">
          あなたの訪問者の来源や、彼らがストアとどのようにやり取りしているかを理解しましょう。Settings > Analytics で Google Analytics トラッキングIDを追加して、データの収集を開始してください。
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Tip 5 -->
    <mj-section background-color="{{ theme.color.background_secondary|default:'#f9fafb' }}" padding="20px" border-radius="8px">
      <mj-column>
        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.primary|default:'#2563eb' }}" padding-bottom="5px">
          ニュースレターの登録フォームを作成しましょう
        </mj-text>
        <mj-text font-size="14px">
          一日からメールリストを構築しましょう。ストアにニュースレターの登録フォームを追加して、訪問者のメールアドレスを収集してください。これらの連絡先は、プロモーションや新商品の発表、顧客との関係構築に利用してください。
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- CTA -->
    {% include 'email_system/mjml_components/cta_button.mjml' with url=admin_url text="Go to Marketing" %}

    <!-- Support -->
    {% include 'email_system/mjml_components/support_block.mjml' %}
  </mj-body>
</mjml>

## Text Content
マーケティングと成長: スタートアップ - {{ store_name }}

こんにちは {{ name|default:'there' }},

{{ store_name }} が形になってきたので、今からトラフィックを増やし、販売を拡大する時間です。以下に、最初のステップとしての5つのマーケティングのヒントを紹介します。

1. 最初の割引コードを作成しましょう
最初のお客様を惹きつけるために、ローンチ割引を提供してください。Marketing > Discount Codes にアクセスして、使用回数の制限や有効期限の設定が可能な割引コード（百分比または固定金額）を作成してください。

2. 放置されたカートの回復を設定しましょう
販売を自動的に回復しましょう。Marketing > Abandoned Carts で、放置されたカートの回復メールを有効にして、顧客に残した商品を思い出させるようにしてください。

3. あなたのソーシャルメディアアカウントを接続しましょう
顧客が見つけてフォローできるように、あなたのソーシャルメディアプロフィールをストアにリンクしてください。Settings > Social Media でソーシャルリンクを追加し、ストアフッターに表示してください。

4. Google Analytics トラッキングを設定しましょう
あなたの訪問者の来源や、彼らがストアとどのようにやり取りしているかを理解しましょう。Settings > Analytics で Google Analytics トラッキングIDを追加して、データの収集を開始してください。

5. ニュースレターの登録フォームを作成しましょう
一日からメールリストを構築しましょう。ストアにニュースレターの登録フォームを追加して、訪問者のメールアドレスを収集してください。これらの連絡先は、プロモーションや新商品の発表、顧客との関係構築に利用してください。

マーケティングへ: {{ admin_url }}

お手伝いが必要ですか？ {{ support_email }} にご連絡ください