---
template_type: blog_subscription_confirmed
category: Blog
---

# Email Template: blog_subscription_confirmed

## Subject
يرجى تأكيد اشتراكك في {{ blog_name }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section>
      <mj-column>
        <mj-text font-size="22px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          تأكيد اشتراكك
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          السلام عليكم {{ subscriber_name }},
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          شكرًا لاشتراكك في {{ blog_name }}! لتأكيد اشتراكك وتلقي التحديثات، يرجى تأكيد عنوان بريدك الإلكتروني.
        </mj-text>

        <mj-spacer height="30px" />

        <mj-button href="{{ confirmation_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="18px" font-weight="bold" border-radius="6px" padding="18px 50px">
          تأكيد الاشتراك
        </mj-button>

        <mj-spacer height="30px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="14px" color="{{ theme.color.text|default:'#4b5563' }}">
              لا يمكنك النقر على الزر؟ قم بنسخ هذا الرابط ولصقه في متصفحك:<br/>
              <span style="color: {{ theme.color.primary|default:'#2563eb' }}; font-family: 'Courier New', monospace;">{{ confirmation_url }}</span>
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-size="14px" color="{{ theme.color.text_secondary|default:'#6b7280' }}">
          <strong>لماذا تأكيد؟</strong><br/>
          يساعد التأكيد عبر البريد الإلكترونينا في التأكد من أنك ترغب في تلقي التحديثات ومنع البريد العشوائي. خصوصيتك وصندوق الوارد الخاص بك مهمان بالنسبة لنا.
        </mj-text>

        <mj-spacer height="20px" />

        <mj-text font-size="13px" color="{{ theme.color.text_secondary|default:'#6b7280' }}" align="center">
          لم تُشترك؟ يمكنك تجاهل هذا البريد الإلكتروني بأمان.
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
تأكيد اشتراكك

السلام عليكم {{ subscriber_name }},

شكرًا لاشتراكك في {{ blog_name }}! لتأكيد اشتراكك وتلقي التحديثات، يرجى تأكيد عنوان بريدك الإلكتروني.

تأكيد الاشتراك: {{ confirmation_url }}

لماذا تأكيد؟
تأكيد البريد الإلكتروني يساعدنا على التأكد من أنك ترغب في تلقي التحديثات ومنع البريد العشوائي. خصوصيتك وصندوق الوارد الخاص بك مهمان بالنسبة لنا.

لم تُشترك؟ يمكنك تجاهل هذا البريد الإلكتروني بأمان.