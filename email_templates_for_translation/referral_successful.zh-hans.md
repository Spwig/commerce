---
template_type: referral_successful
category: Referral Program
---

# Email Template: referral_successful

## Subject
🎉 你的朋友 {{ referee_name }} 刚刚注册了！

## HTML Content
<mjml>
  <mj-head>
    <mj-attributes>
      <mj-text font-family="Arial, sans-serif" line-height="1.6" />
      <mj-all font-family="Arial, sans-serif" />
    </mj-attributes>
  </mj-head>
  <mj-body background-color="{{ theme.color.background_secondaryondary|default:'#f9fafb' }}">
    <!-- Header -->
    <mj-section background-color="{{ theme.color.background|default:'#ffffff' }}" padding="40px 20px">
      <mj-column>
        <mj-text font-size="32px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}" align="center">
          🎉 推荐成功！
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Success Banner -->
    <mj-section background-color="{{ theme.color.success|default:'#10b981' }}" padding="30px 20px">
      <mj-column>
        <mj-text font-size="24px" font-weight="bold" color="{{ theme.color.background|default:'#ffffff' }}" align="center">
          {{ referee_name }} 已加入！
        </mj-text>
        <mj-text font-size="16px" color="{{ theme.color.background|default:'#ffffff' }}" align="center" padding-top="10px">
          你的推荐现在已成为会员
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Content -->
    <mj-section background-color="{{ theme.color.background|default:'#ffffff' }}" padding="20px">
      <mj-column>
        <mj-text font-size="16px" color="{{ theme.color.text|default:'#1f2937' }}">
          你好 {{ customer_name }}，
        </mj-text>
        <mj-text font-size="16px" color="{{ theme.color.text|default:'#1f2937' }}">
          好消息！{{ referee_name }} 刚刚使用你的推荐链接注册了。
        </mj-text>
        <mj-text font-size="16px" color="{{ theme.color.text|default:'#1f2937' }}">
          一旦他们完成首次购买，你和他们都将获得奖励！当发生这种情况时，我们会再发一封邮件给你。
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Next Steps -->
    <mj-section background-color="{{ theme.color.background_secondaryondary|default:'#f9fafb' }}" padding="30px 20px">
      <mj-column>
        <mj-text font-size="18px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}" align="center" padding-bottom="10px">
          接下来会发生什么？
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          1. {{ referee_name }} 完成首次购买<br/>
          2. 你和他都会自动获得奖励<br/>
          3. 你可以在任何未来的购买中使用你的奖励
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Keep Sharing -->
    <mj-section background-color="{{ theme.color.background|default:'#ffffff' }}" padding="30px 20px">
      <mj-column>
        <mj-text font-size="18px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}" align="center" padding-bottom="15px">
          继续分享以赚取更多奖励！
        </mj-text>
        <mj-text
          background-color="{{ theme.color.background_secondaryondary|default:'#f9fafb' }}"
          border="2px dashed {{ theme.color.primary|default:'#2563eb' }}"
          border-radius="8px"
          padding="15px"
          font-size="14px"
          color="{{ theme.color.primary|default:'#2563eb' }}"
          align="center"
          font-family="monospace"
        >
          {{ referral_link }}
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section background-color="{{ theme.color.background|default:'#ffffff' }}" padding="10px 20px 30px 20px">
      <mj-column>
        <mj-button background-color="{{ theme.color.primary|default:'#2563eb' }}" color="{{ theme.color.background|default:'#ffffff' }}" href="{{ referral_dashboard_url }}">
          查看我的推荐
        </mj-button>
      </mj-column>
    </mj-section>

    <!-- Footer -->
    <mj-section background-color="{{ theme.color.background_secondaryondary|default:'#f9fafb' }}" padding="20px">
      <mj-column>
        <mj-text font-size="12px" color="{{ theme.color.text_muted|default:'#6b7280' }}" align="center">
          {{ shop_name }}
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
🎉 你的朋友 {{ referee_name }} 刚刚注册了！

你好 {{ customer_name }}，

好消息！{{ referee_name }} 刚刚使用你的推荐链接注册了。

一旦他们完成首次购买，你和他们都将获得奖励！当发生这种情况时，我们会再发一封邮件给你。

接下来会发生什么？
1. {{ referee_name }} 完成首次购买
2. 你和他都会自动获得奖励
3. 你可以在任何未来的购买中使用你的奖励

继续分享以赚取更多奖励：
{{ referral_link }}

查看你的推荐：{{ referral_dashboard_url }}

{{ shop_name }}