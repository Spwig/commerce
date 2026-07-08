---
template_type: blog_subscriber_welcome
category: Blog
---

# Email Template: blog_subscriber_welcome

## Subject
ยินดีต้อนรับสู่ {{ blog_name }}! 🎉

## HTML Content
<mjml>
  <mj-body>
    <mj-section>
      <mj-column>
        <mj-text font-size="24px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}" align="center">
          🎉 ยินดีต้อนรับสู่ {{ blog_name }}!
        </mj-text>

        <mj-spacer height="20px" />

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          คุณ {{ subscriber_name }},
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          ขอบคุณที่สมัครสมาชิก! เราตื่นเต้นที่จะแบ่งปันเนื้อหาล่าสุดของเราให้คุณ
        </mj-text>

        <mj-spacer height="30px" />

        <mj-section background-color="#f0fdf4" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-size="16px" font-weight="bold" color="#065f46">
              สิ่งที่คุณจะได้รับ:
            </mj-text>
            <mj-text font-size="14px" color="#065f46" line-height="1.8">
              ✓ โพสต์ใหม่ส่งถึงกล่องจดหมายของคุณ\n<br/>
              ✓ เนื้อหาพิเศษเฉพาะสมาชิก\n<br/>
              ✓ การอัปเดต {{ publish_frequency }}\n<br/>
              ✓ ไม่มีสแปม ยกเลิกการสมัครสมาชิกได้ตลอดเวลา
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-size="18px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          เริ่มอ่าน:
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}">
          ดูบทความยอดนิยมของเรา:
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
          สำรวจบทความทั้งหมด
        </mj-button>

        <mj-spacer height="30px" />

        <mj-text font-size="13px" color="{{ theme.color.text_secondary|default:'#6b7280' }}" align="center">
          จัดการการสมัครสมาชิกของคุณ: <a href="{{ preferences_url }}">Email Preferences</a>
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
🎉 ยินดีต้อนรับสู่ {{ blog_name }}!

คุณ {{ subscriber_name }},

ขอบคุณที่สมัครสมาชิก! เราตื่นเต้นที่จะแบ่งปันเนื้อหาล่าสุดของเราให้คุณ

สิ่งที่คุณจะได้รับ:
✓ โพสต์ใหม่ส่งถึงกล่องจดหมายของคุณ
✓ เนื้อหาพิเศษเฉพาะสมาชิก
✓ {{ publish_frequency }} การอัปเดต
✓ ไม่มีสแปม ยกเลิกการสมัครสมาชิกได้ตลอดเวลา

เริ่มอ่าน - บทความยอดนิยม:
{% for post in popular_posts %}
- {{ post.title }} ({{ post.reading_time }} นาทีอ่าน)
  {{ post.url }}
{% endfor %}

สำรวจบทความทั้งหมด: {{ blog_url }}

จัดการการสมัครสมาชิกของคุณ: {{ preferences_url }}