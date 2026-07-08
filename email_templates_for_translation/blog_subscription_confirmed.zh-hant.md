---
template_type: blog_subscription_confirmed
category: Blog
---

# Email Template: blog_subscription_confirmed

## Subject
請確認您對 {{ blog_name }} 的訂閱

## HTML Content
<mjml>
  <mj-body>
    <mj-section>
      <mj-column>
        <mj-text font-size="22px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          確認您的訂閱
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Hi {{ subscriber_name }},
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          感謝您訂閱 {{ blog_name }}！請確認您的電子郵件地址以完成訂閱並開始接收更新。
        </mj-text>

        <mj-spacer height="30px" />

        <mj-button href="{{ confirmation_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="18px" font-weight="bold" border-radius="6px" padding="18px 50px">
          確認訂閱
        </mj-button>

        <mj-spacer height="30px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="14px" color="{{ theme.color.text|default:'#4b5563' }}">
              無法點擊按鈕？將此連結複製並貼到瀏覽器中：<br/>
              <span style="color: {{ theme.color.primary|default:'#2563eb' }}; font-family: 'Courier New', monospace;">{{ confirmation_url }}</span>
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-size="14px" color="{{ theme.color.text_secondary|default:'#6b7280' }}">
          <strong>為何要確認？</strong><br/>
          電子郵件確認能幫助我們確保您希望接收更新，並防止垃圾郵件。您的隱私和收件箱對我們來說都很重要。
        </mj-text>

        <mj-spacer height="20px" />

        <mj-text font-size="13px" color="{{ theme.color.text_secondary|default:'#6b7280' }}" align="center">
          如果您沒有訂閱，可以放心忽略這封郵件。
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
確認您的訂閱

Hi {{ subscriber_name }},

感謝您訂閱 {{ blog_name }}！請確認您的電子郵件地址以完成訂閱並開始接收更新。

確認訂閱：{{ confirmation_url }}

為何要確認？
電子郵件確認能幫助我們確保您希望接收更新，並防止垃圾郵件。您的隱私和收件箱對我們來說都很重要。

如果您沒有訂閱，可以放心忽略這封郵件。