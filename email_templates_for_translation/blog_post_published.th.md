---
template_type: blog_post_published
category: Blog
---

# Email Template: blog_post_published

## Subject
บล็อกใหม่: {{ post_title }} - {{ shop_name }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section>
      <mj-column>
        <mj-text font-size="22px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          📝 บล็อกใหม่
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          คุณ {{ subscriber_name }},
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          เราเพิ่งตีพิมพ์โพสต์ใหม่ที่คิดว่าคุณจะชอบ!
        </mj-text>

        <mj-spacer height="30px" />

        {% if featured_image %}
        <mj-image src="{{ featured_image }}" alt="{{ post_title }}" border-radius="8px" />
        <mj-spacer height="20px" />
        {% endif %}

        <mj-text font-size="24px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}" line-height="1.3">
          {{ post_title }}
        </mj-text>

        <mj-spacer height="15px" />

        <mj-text font-size="14px" color="{{ theme.color.text_secondary|default:'#6b7280' }}">
          โดย {{ author_name }} | {{ publish_date }} | {{ reading_time }} นาทีในการอ่าน
        </mj-text>

        <mj-spacer height="20px" />

        <mj-text font-size="16px" line-height="1.8" color="{{ theme.color.text|default:'#4b5563' }}">
          {{ post_excerpt }}
        </mj-text>

        <mj-spacer height="30px" />

        <mj-button href="{{ post_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          อ่านบทความทั้งหมด
        </mj-button>

        <mj-spacer height="30px" />

        {% if related_posts %}
        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          คุณอาจชอบเพิ่มเติม:
        </mj-text>

        {% for post in related_posts %}
        <mj-spacer height="15px" />
        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="4px" padding="12px">
          <mj-column>
            <mj-text font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
              {{ post.title }}
            </mj-text>
            <mj-text font-size="14px" color="{{ theme.color.text_secondary|default:'#6b7280' }}">
              {{ post.excerpt }}
            </mj-text>
            <mj-text font-size="14px">
              <a href="{{ post.url }}" style="color: {{ theme.color.primary|default:'#2563eb' }};">อ่านเพิ่มเติม →</a>
            </mj-text>
          </mj-column>
        </mj-section>
        {% endfor %}
        <mj-spacer height="30px" />
        {% endif %}

        <mj-text font-size="13px" color="{{ theme.color.text_secondary|default:'#6b7280' }}" align="center">
          คุณได้รับอีเมลนี้เพราะคุณสมัครสมาชิกบล็อก {{ blog_name }}.<br/>
          <a href="{{ unsubscribe_url }}">ยกเลิกการสมัครสมาชิกการอัปเดตบล็อก</a>
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
📝 บล็อกใหม่

คุณ {{ subscriber_name }},

เราเพิ่งตีพิมพ์โพสต์ใหม่ที่คิดว่าคุณจะชอบ!

{{ post_title }}
โดย {{ author_name }} | {{ publish_date }} | {{ reading_time }} นาทีในการอ่าน

{{ post_excerpt }}

อ่านบทความทั้งหมด: {{ post_url }}

{% if related_posts %}
YOU MIGHT ALSO LIKE:
{% for post in related_posts %}
- {{ post.title }}
  {{ post.url }}
{% endfor %}
{% endif %}

---

คุณได้รับอีเมลนี้เพราะคุณสมัครสมาชิกบล็อก {{ blog_name }}.
ยกเลิกการสมัครสมาชิกการอัปเดตบล็อก: {{ unsubscribe_url }}