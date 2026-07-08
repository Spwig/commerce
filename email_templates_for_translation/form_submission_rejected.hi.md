---
template_type: form_submission_rejected
category: Form Builder
---

# Email Template: form_submission_rejected

## Subject
आपके {{ form_name }} फॉर्म के उपलब्धियों के बारे में अपडेट

## HTML Content
<mjml>
  <mj-body>
    <mj-section>
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Update on Your Submission
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Hi {{ submitter_name }},
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Thank you for submitting the {{ form_name }} form. After careful review, we're unable to approve your submission at this time.
        </mj-text>

        <mj-spacer height="30px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
              Submission Details:
            </mj-text>
            <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>Form:</strong> {{ form_name }}<br/>
              <strong>Submitted:</strong> {{ submission_date }}<br/>
              <strong>Reviewed:</strong> {{ rejection_date }}<br/>
              <strong>Reference #:</strong> {{ submission_id }}
            </mj-text>
          </mj-column>
        </mj-section>

        {% if rejection_reason %}
        <mj-spacer height="30px" />
        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Reason:
        </mj-text>
        <mj-section background-color="#fef3c7" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="14px" color="#92400e" line-height="1.6">
              {{ rejection_reason }}
            </mj-text>
          </mj-column>
        </mj-section>
        {% endif %}

        {% if can_resubmit %}
        <mj-spacer height="30px" />
        <mj-section background-color="#f0fdf4" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="14px" color="#065f46" font-weight="bold">
              You Can Resubmit
            </mj-text>
            <mj-text font-size="14px" color="#065f46" line-height="1.6">
              {{ resubmit_instructions }}
            </mj-text>
          </mj-column>
        </mj-section>
        {% endif %}

        <mj-spacer height="30px" />

        {% if resubmit_url %}
        <mj-button href="{{ resubmit_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          Submit Again
        </mj-button>
        <mj-spacer height="10px" />
        {% endif %}

        {% if support_url %}
        <mj-button href="{{ support_url }}" background-color="#6b7280" color="#ffffff" font-size="14px" border-radius="6px" padding="10px 25px">
          Contact Support
        </mj-button>
        <mj-spacer height="20px" />
        {% endif %}

        <mj-text font-size="14px" color="{{ theme.color.text_secondary|default:'#6b7280' }}" align="center">
          If you have questions about this decision, please don't hesitate to reach out.
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
आपके उपलब्धियों के बारे में अपडेट

हेलो {{ submitter_name }},

आपके द्वारा {{ form_name }} फॉर्म के उपलब्धियों के लिए धन्यवाद। ध्यान से समीक्षा के बाद, हम आपके उपलब्धियों को अभी के लिए अनुमोदित नहीं कर सकते।

उपलब्धियों के विवरण:
- फॉर्म: {{ form_name }}
- उपलब्ध: {{ submission_date }}
- समीक्षा: {{ rejection_date }}
- संदर्भ #: {{ submission_id }}

{% if rejection_reason %}
कारण:
{{ rejection_reason }}
{% endif %}

{% if can_resubmit %}
आप फिर से उपलब्धियों के लिए योग्य हैं:
{{ resubmit_instructions }}
{% endif %}

{% if resubmit_url %}फिर से उपलब्धियों के लिए: {{ resubmit_url }}{% endif %}
{% if support_url %}समर्थन से संपर्क करें: {{ support_url }}{% endif %}

यदि आपके इस निर्णय के बारे में कोई प्रश्न हैं, तो कृपया बिना किसी संकोच के संपर्क करें।