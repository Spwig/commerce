---
template_type: blog_comment_approved
category: Blog
---

# Email Template: blog_comment_approved

## Subject
आपका टिप्पणी "{{ post_title }}" पर अनुमोदित कर दी गई है - {{ blog_name }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#f0fdf4">
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="#059669" align="center">
          ✓ टिप्पणी अनुमोदित कर दी गई है
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          हे {{ commenter_name }},
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          अच्छी खबर! आपकी टिप्पणी "{{ post_title }}" पर अनुमोदित कर दी गई है और अब अन्य पाठकों के लिए दृश्य है।
        </mj-text>

        <mj-spacer height="20px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-size="14px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
              आपकी टिप्पणी:
            </mj-text>
            <mj-text font-size="14px" color="{{ theme.color.text|default:'#4b5563' }}" line-height="1.6">
              {{ comment_text }}
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-button href="{{ comment_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" border-radius="6px" padding="12px 30px">
          अपनी टिप्पणी देखें
        </mj-button>

        <mj-spacer height="20px" />

        <mj-text font-size="14px" color="{{ theme.color.text_secondary|default:'#6b7280' }}">
          हम आपको जानकारी देंगे जब कोई आपकी टिप्पणी के उत्तर देता है।
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
✓ COMMENT APPROVED

हे {{ commenter_name }},

अच्छी खबर! आपकी टिप्पणी "{{ post_title }}" पर अनुमोदित कर दी गई है और अब अन्य पाठकों के लिए दृश्य है।

आपकी टिप्पणी:
{{ comment_text }}

View your comment: {{ comment_url }}

हम आपको जानकारी देंगे जब कोई आपकी टिप्पणी के उत्तर देता है।