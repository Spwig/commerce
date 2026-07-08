---
template_type: blog_subscriber_welcome
category: Blog
---

# Email Template: blog_subscriber_welcome

## Subject
🎉 {{ blog_name }}へようこそ！

## HTML Content
<mjml>
  <mj-body>
    <mj-section>
      <mj-column>
        <mj-text font-size="24px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}" align="center">
          🎉 {{ blog_name }}へようこそ！
        </mj-text>

        <mj-spacer height="20px" />

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          こんにちは {{ subscriber_name }}、
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          ご登録ありがとうございます！私たちが最新のコンテンツとお届けできるのを楽しみにしています。
        </mj-text>

        <mj-spacer height="30px" />

        <mj-section background-color="#f0fdf4" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-size="16px" font-weight="bold" color="#065f46">
              期待できること:
            </mj-text>
            <mj-text font-size="14px" color="#065f46" line-height="1.8">
              ✓ メールボックスにお届けする新着投稿<br/>
              ✓ 限定された購読者専用コンテンツ<br/>
              ✓ {{ publish_frequency }}更新<br/>
              ✓ スパムなし、いつでも購読解除可能
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-size="18px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          読み始めましょう:
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}">
          人気の記事をチェックしてみてください:
        </mj-text>

        <mj-spacer height="15px" />

        {% for post in popular_posts %}
        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="15px">
          <mj-column width="30%">
            <mj-image src="{{ post.featured_image }}" alt="{{ post.title }}" border-radius="4px" />
          </mj-column>
          <mj-column width="70%">
            <mj-text font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
              {{ post.title }}
            </mj-text>
            <mj-text font-size="13px" color="{{ theme.color.text_secondary|default:'#6b7280' }}">
              {{ post.reading_time }} min read
            </mj-text>
            <mj-text font-size="14px">
              <a href="{{ post.url }}" style="color: {{ theme.color.primary|default:'#2563eb' }};">Read now →</a>
            </mj-text>
          </mj-column>
        </mj-section>
        <mj-spacer height="10px" />
        {% endfor %}

        <mj-spacer height="30px" />

        <mj-button href="{{ blog_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          すべての記事を確認する
        </mj-button>

        <mj-spacer height="30px" />

        <mj-text font-size="13px" color="{{ theme.color.text_secondary|default:'#6b7280' }}" align="center">
          サブスクリプションの管理: <a href="{{ preferences_url }}">メール設定</a>
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
🎉 {{ blog_name }}へようこそ！

こんにちは {{ subscriber_name }}、

ご登録ありがとうございます！私たちが最新のコンテンツとお届けできるのを楽しみにしています。

期待できること:
✓ メールボックスにお届けする新着投稿
✓ 限定された購読者専用コンテンツ
✓ {{ publish_frequency }}更新
✓ スパムなし、いつでも購読解除可能

START READING - POPULAR ARTICLES:
{% for post in popular_posts %}
- {{ post.title }} ({{ post.reading_time }} min read)
  {{ post.url }}
{% endfor %}

Explore all articles: {{ blog_url }}

Manage your subscription: {{ preferences_url }}