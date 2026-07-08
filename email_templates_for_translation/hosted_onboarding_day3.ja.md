---
template_type: hosted_onboarding_day3
category: License
---

# Email Template: hosted_onboarding_day3

## Subject
カタログを構築しましょう - {{ store_name }}

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
          スタート: あなたの商品
        </mj-text>
        <mj-text font-size="16px" color="#ffffffcc" align="center" padding-top="10px">
          {{ store_name }} 用のカタログを構築しましょう
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
          あなたのストア <strong>{{ store_name }}</strong> はすべて準備ができました。今から商品カタログを構築しましょう。以下に5つのヒントを紹介します。
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Tip 1 -->
    <mj-section background-color="{{ theme.color.background_secondary|default:'#f9fafb' }}" padding="20px" border-radius="8px">
      <mj-column>
        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.primary|default:'#2563eb' }}" padding-bottom="5px">
          CSVから商品をインポート
        </mj-text>
        <mj-text font-size="14px">
          すでに商品リストを持っている場合は、<strong>Admin > Catalog > Import</strong> にアクセスしてCSVファイルから商品を一括インポートしてください。これはストアを迅速に構築する最も効率的な方法です。
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Tip 2 -->
    <mj-section>
      <mj-column>
        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.primary|default:'#2563eb' }}" padding-bottom="5px">
          カテゴリとフィルタで整理
        </mj-text>
        <mj-text font-size="14px">
          顧客が簡単に商品を検索できるように、カテゴリと属性フィルタを作成してください。整理されたカタログは変換率を高めます。
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Tip 3 -->
    <mj-section background-color="{{ theme.color.background_secondary|default:'#f9fafb' }}" padding="20px" border-radius="8px">
      <mj-column>
        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.primary|default:'#2563eb' }}" padding-bottom="5px">
          説得力のある商品説明を書こう
        </mj-text>
        <mj-text font-size="14px">
          良い説明は商品を売ります。特徴だけでなく、利点に焦点を当てましょう。顧客がなぜあなたの商品が必要で、それがどんな問題を解決するかを伝えてください。
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Tip 4 -->
    <mj-section>
      <mj-column>
        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.primary|default:'#2563eb' }}" padding-bottom="5px">
          高品質な商品画像をアップロード
        </mj-text>
        <mj-text font-size="14px">
          明確でプロフェッショナルな画像は大きな違いを生みます。複数の角度をアップロードし、一貫した照明を使用してください。Spwigは画像を高速ロード用に自動で最適化します。
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Tip 5 -->
    <mj-section background-color="{{ theme.color.background_secondary|default:'#f9fafb' }}" padding="20px" border-radius="8px">
      <mj-column>
        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.primary|default:'#2563eb' }}" padding-bottom="5px">
          商品のバリエーションを設定
        </mj-text>
        <mj-text font-size="14px">
          商品がさまざまなサイズ、色、スタイルがある場合は、バリエーションを作成して顧客が欲しいものを正確に選べるようにしてください。各バリエーションは独自の価格、在庫数、画像を持つことができます。
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- CTA -->
    {% include 'email_system/mjml_components/cta_button.mjml' with url=admin_url text="Manage Your Products" %}

    <!-- Support -->
    {% include 'email_system/mjml_components/support_block.mjml' %}
  </mj-body>
</mjml>

## Text Content
商品のカタログ構築: {{ store_name }}

こんにちは {{ name|default:'there' }},

あなたのストア {{ store_name }} はすべて準備ができました。今から商品カタログを構築しましょう。以下に5つのヒントを紹介します。

1. CSVから商品をインポート
すでに商品リストを持っている場合は、Admin > Catalog > Import にアクセスしてCSVファイルから商品を一括インポートしてください。

2. カテゴリとフィルタで整理
顧客が簡単に商品を検索できるように、カテゴリと属性フィルタを作成してください。

3. 説得力のある商品説明を書こう
良い説明は商品を売ります。特徴だけでなく、利点に焦点を当てましょう。顧客がなぜあなたの商品が必要で、それがどんな問題を解決するかを伝えてください。

4. 高品質な商品画像をアップロード
明確でプロフェッショナルな画像は大きな違いを生みます。複数の角度をアップロードし、一貫した照明を使用してください。

5. 商品のバリエーションを設定
商品がさまざまなサイズ、色、スタイルがある場合は、バリエーションを作成して顧客が欲しいものを正確に選べるようにしてください。

商品の管理: {{ admin_url }}

お手伝いが必要ですか？ {{ support_email }} にご連絡ください。