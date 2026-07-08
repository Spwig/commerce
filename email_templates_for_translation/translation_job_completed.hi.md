---
template_type: translation_job_completed
category: Translation Service
---

# Email Template: translation_job_completed

## Subject
✓ अनुवाद पूरा: {{ content_type }} ({{ language_count }} भाषाओं)

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#dcfce7">
      <mj-column>
        <mj-text font-size="24px" font-weight="bold" color="#065f46" align="center">
          ✓ अनुवाद पूरा!
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          आपके अनुवाद तैयार हैं
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          अच्छी खबर! आपका बैच अनुवाद कार्य सफलतापूर्वक पूरा कर लिया गया है।
        </mj-text>

        <mj-spacer height="30px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
              कार्य सारांश:
            </mj-text>
            <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>कार्य का आईडी:</strong> {{ job_id }}<br/>
              <strong>सामग्री प्रकार:</strong> {{ content_type }}<br/>
              <strong>भाषाएं:</strong> {{ target_languages }}<br/>
              <strong>अनुवादित आइटम:</strong> {{ items_translated }}<br/>
              <strong>कुल शब्द:</strong> {{ word_count }}<br/>
              <strong>पूरा कर लिया गया:</strong> {{ completed_at }}<br/>
              <strong>अवधि:</strong> {{ job_duration }}
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          अनुवाद गुणवत्ता:
        </mj-text>

        <mj-section background-color="#f0fdf4" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="15px" color="#065f46">
              <strong>औसत गुणवत्ता स्कोर:</strong> {{ quality_score }}%<br/>
              <strong>उच्च गुणवत्ता:</strong> {{ high_quality_count }} आइटम<br/>
              <strong>समीक्षा की आवश्यकता है:</strong> {{ review_needed_count }} आइटम
            </mj-text>
          </mj-column>
        </mj-section>

        {% if review_needed_count > 0 %}
        <mj-spacer height="20px" />
        <mj-section background-color="#fef3c7" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="14px" color="#92400e" font-weight="bold">
              ⚠️ समीक्षा की आवश्यकता है
            </mj-text>
            <mj-text font-size="14px" color="#92400e" line-height="1.6">
              {{ review_needed_count }} अनुवाद 85% से कम अंक हासिल करते हैं और प्रकाशित करने से पहले उनकी समीक्षा करनी चाहिए।
            </mj-text>
          </mj-column>
        </mj-section>
        {% endif %}

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          अगले कदम:
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}" line-height="1.8">
          1. अपने प्रशासन पैनल में अनुवादों की समीक्षा करें<br/>
          2. किसी भी सुधार की आवश्यकता वाले अनुवादों को संपादित करें<br/>
          3. अनुवादों को लाइव करने के लिए प्रकाशित करें<br/>
          4. आपकी बहुभाषी सामग्री ग्राहकों के लिए उपलब्ध होगी
        </mj-text>

        <mj-spacer height="30px" />

        <mj-button href="{{ review_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          अनुवाद समीक्षा करें
        </mj-button>

        {% if can_publish_all %}
        <mj-spacer height="10px" />
        <mj-button href="{{ publish_all_url }}" background-color="#059669" color="#ffffff" font-size="14px" border-radius="6px" padding="10px 25px">
          सभी को प्रकाशित करें
        </mj-button>
        {% endif %}
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
✓ अनुवाद पूरा!

आपके अनुवाद तैयार हैं

अच्छी खबर! आपका बैच अनुवाद कार्य सफलतापूर्वक पूरा कर लिया गया है।

कार्य सारांश:
- कार्य का आईडी: {{ job_id }}
- सामग्री प्रकार: {{ content_type }}
- भाषाएं: {{ target_languages }}
- अनुवादित आइटम: {{ items_translated }}
- कुल शब्द: {{ word_count }}
- पूरा कर लिया गया: {{ completed_at }}
- अवधि: {{ job_duration }}

अनुवाद गुणवत्ता:
- औसत गुणवत्ता स्कोर: {{ quality_score }}%
- उच्च गुणवत्ता: {{ high_quality_count }} आइटम
- समीक्षा की आवश्यकता है: {{ review_needed_count }} आइटम

{% if review_needed_count > 0 %}
⚠️ समीक्षा की आवश्यकता है:
{{ review_needed_count }} अनुवाद 85% से कम अंक हासिल करते हैं और प्रकाशित करने से पहले उनकी समीक्षा करनी चाहिए।
{% endif %}

अगले कदम:
1. अपने प्रशासन पैनल में अनुवादों की समीक्षा करें
2. किसी भी सुधार की आवश्यकता वाले अनुवादों को संपादित करें
3. अनुवादों को लाइव करने के लिए प्रकाशित करें
4. आपकी बहुभाषी सामग्री ग्राहकों के लिए उपलब्ध होगी

अनुवाद समीक्षा करें: {{ review_url }}
{% if can_publish_all %}सभी को प्रकाशित करें: {{ publish_all_url }}{% endif %}