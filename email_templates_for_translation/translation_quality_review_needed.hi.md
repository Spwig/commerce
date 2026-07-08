---
template_type: translation_quality_review_needed
category: Translation Service
---

# Email Template: translation_quality_review_needed

## Subject
⚠️ कम गुणवत्ता अनुवाद पाए गए: {{ content_type }} - {{ low_quality_count }} आइटम समीक्षा की आवश्यकता है

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#fef3c7">
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="#92400e" align="center">
          ⚠️ अनुवाद गुणवत्ता सचेति
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="18px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          समीक्षा की आवश्यकता है
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}">
          आपका अनुवाद कार्य पूर्ण हो गया, लेकिन {{ low_quality_count }} अनुवाद गुणवत्ता द्वारा नीचे स्कोर किए गए और प्रकाशित करने से पहले समीक्षा की आवश्यकता है।
        </mj-text>

        <mj-spacer height="20px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
              कार्य सारांश:
            </mj-text>
            <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>कार्य ID:</strong> {{ job_id }}<br/>
              <strong>सामग्री प्रकार:</strong> {{ content_type }}<br/>
              <strong>कुल आइटम:</strong> {{ total_items }}<br/>
              <strong>औसत गुणवत्ता:</strong> {{ average_quality }}%<br/>
              <strong>कम गुणवत्ता:</strong> {{ low_quality_count }} आइटम ({{ low_quality_percentage }}%)
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          गुणवत्ता विस्तार:
        </mj-text>

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="14px" color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>अद्भुत (95-100%):</strong> {{ excellent_count }} आइटम<br/>
              <strong>अच्छा (85-94%):</strong> {{ good_count }} आइटम<br/>
              <strong>सामान्य (70-84%):</strong> {{ fair_count }} आइटम<br/>
              <strong>खराब (&lt;70%):</strong> <span style="color: #dc2626; font-weight: bold;">{{ poor_count }} आइटम</span>
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          सामान्य गुणवत्ता समस्याएँ:
        </mj-text>

        {% for issue in quality_issues %}
        <mj-section background-color="#fef3c7" border-radius="8px" padding="12px">
          <mj-column>
            <mj-text font-size="14px" color="#92400e">
              <strong>{{ issue.type }}:</strong> {{ issue.count }} आवृत्तियाँ
            </mj-text>
          </mj-column>
        </mj-section>
        <mj-spacer height="8px" />
        {% endfor %}

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          सिफारिश की गई कार्रवाई:
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}" line-height="1.8">
          1. प्रशासन पैनल में चिह्नित अनुवादों की समीक्षा करें<br/>
          2. कम गुणवत्ता वाले अनुवादों को मैनुअली संपादित करें<br/>
          3. खराब गुणवत्ता वाले आइटम को पुनः अनुवाद करने की गणना करें<br/>
          4. समीक्षा पूरी होने के बाद केवल प्रकाशित करें
        </mj-text>

        <mj-spacer height="30px" />

        <mj-button href="{{ review_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          अनुवादों की समीक्षा
        </mj-button>

        <mj-spacer height="10px" />

        <mj-button href="{{ low_quality_url }}" background-color="#dc2626" color="#ffffff" font-size="14px" border-radius="6px" padding="10px 25px">
          कम गुणवत्ता वाले आइटम देखें
        </mj-button>

        <mj-spacer height="30px" />

        <mj-section background-color="#eff6ff" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="14px" color="#1e40af" line-height="1.6">
              💡 सुझाव: 85% से कम गुणवत्ता स्कोर व्याकरण, प्रसंग या सटीकता के संभावित समस्याओं को इंगित करता है। प्रकाशित करने से पहले मनुष्य समीक्षा के लिए मजबूर की जानी चाहिए।
            </mj-text>
          </mj-column>
        </mj-section>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
⚠️ अनुवाद गुणवत्ता सचेति

समीक्षा की आवश्यकता है

आपका अनुवाद कार्य पूर्ण हो गया, लेकिन {{ low_quality_count }} अनुवाद गुणवत्ता द्वारा नीचे स्कोर किए गए और प्रकाशित करने से पहले समीक्षा की आवश्यकता है।

कार्य सारांश:
- कार्य ID: {{ job_id }}
- सामग्री प्रकार: {{ content_type }}
- कुल आइटम: {{ total_items }}
- औसत गुणवत्ता: {{ average_quality }}%
- कम गुणवत्ता: {{ low_quality_count }} आइटम ({{ low_quality_percentage }}%)

गुणवत्ता विस्तार:
- अद्भुत (95-100%): {{ excellent_count }} आइटम
- अच्छा (85-94%): {{ good_count }} आइटम
- सामान्य (70-84%): {{ fair_count }} आइटम
- खराब (<70%): {{ poor_count }} आइटम

सामान्य गुणवत्ता समस्याएँ:
{% for issue in quality_issues %}
{{ issue.type }}: {{ issue.count }} आवृत्तियाँ
{% endfor %}

सिफारिश की गई कार्रवाई:
1. प्रशासन पैनल में चिह्नित अनुवादों की समीक्षा करें
2. कम गुणवत्ता वाले अनुवादों को मैनुअली संपादित करें
3. खराब गुणवत्ता वाले आइटम को पुनः अनुवाद करने की गणना करें
4. समीक्षा पूरी होने के बाद केवल प्रकाशित करें

अनुवादों की समीक्षा: {{ review_url }}
कम गुणवत्ता वाले आइटम देखें: {{ low_quality_url }}

💡 सुझाव: 85% से कम गुणवत्ता स्कोर व्याकरण, प्रसंग या सटीकता के संभावित समस्याओं को इंगित करता है। प्रकाशित करने से पहले मनुष्य समीक्षा के लिए मजबूर की जानी चाहिए।