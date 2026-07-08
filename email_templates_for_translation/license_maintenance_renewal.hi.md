---
template_type: license_maintenance_renewal
category: License
---

# Email Template: license_maintenance_renewal

## Subject
रखरखाव नवीनीकरण - आदेश #{{ order_number }}

## HTML Content
<mjml>
  <mj-head>
    <mj-attributes>
      <mj-all font-family="'Helvetica Neue', Helvetica, Arial, sans-serif" />
      <mj-text font-size="14px" color="#333333" line-height="20px" />
      <mj-section background-color="{{ theme.color.background|default:'#ffffff' }}" padding="20px" />
    </mj-attributes>
  </mj-head>
  <mj-body background-color="{{ theme.color.background_secondary|default:'#f9fafb' }}">
    <!-- Header -->
    <mj-section background-color="{{ theme.color.success|default:'#10b981' }}" padding="30px 20px">
      <mj-column>
        <mj-text font-size="28px" font-weight="bold" color="#ffffff" align="center">
          रखरखाव नवीनीकरण!
        </mj-text>
        <mj-text font-size="16px" color="#ffffffcc" align="center" padding-top="10px">
          आदेश #{{ order_number }}
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Greeting -->
    <mj-section>
      <mj-column>
        <mj-text font-size="16px">
          हेलो {{ customer_name }},
        </mj-text>
        <mj-text>
          आपका Spwig रखरखाव सदस्यता सफलतापूर्वक नवीनीकृत कर दी गई है। आप लगातार प्लेटफॉर्म अपडेट, सुरक्षा पैच और नई सुविधाओं के लाभ ले सकते हैं।
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Renewal Summary -->
    <mj-section background-color="{{ theme.color.background_secondary|default:'#f9fafb' }}" padding="20px" border-radius="8px">
      <mj-column>
        <mj-text font-size="16px" font-weight="bold" padding-bottom="10px">
          नवीनीकरण सारांश
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          लाइसेंस कुंजी: {{ license_key }}
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          रखरखाव की अवधि: {{ renewal_expires_at }}
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          आदेश संख्या: {{ order_number }}
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- What's Included -->
    <mj-section>
      <mj-column>
        <mj-text font-size="16px" font-weight="bold" padding-bottom="10px">
          क्या शामिल है
        </mj-text>
        <mj-text font-size="14px">
          आपके सक्रिय रखरखाव के लाभ लेने के लिए आपके पास एक्सेस है:
        </mj-text>
        <mj-text font-size="14px" padding-top="5px">
          - प्लेटफॉर्म फीचर अपडेट और सुधार
        </mj-text>
        <mj-text font-size="14px">
          - सुरक्षा पैच और बग फिक्स
        </mj-text>
        <mj-text font-size="14px">
          - अपग्रेड सर्वर के माध्यम से नए कम्पोनेंट रिलीज
        </mj-text>
        <mj-text font-size="14px">
          - तकनीकी समर्थन
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Next Steps -->
    <mj-section>
      <mj-column>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          आपकी ओर से कोई कार्रवाई आवश्यक नहीं है। अपडेट आपके प्रशासन पैनल के कम्पोनेंट अपडेट प्रणाली के माध्यम से लगातार उपलब्ध रहेगा।
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Support -->
    {% include 'email_system/mjml_components/support_block.mjml' %}
  </mj-body>
</mjml>

## Text Content
रखरखाव नवीनीकरण!

आदेश #{{ order_number }}

हेलो {{ customer_name }},

आपका Spwig रखरखाव सदस्यता सफलतापूर्वक नवीनीकृत कर दी गई है। आप लगातार प्लेटफॉर्म अपडेट, सुरक्षा पैच और नई सुविधाओं के लाभ ले सकते हैं।

नवीनीकरण सारांश:
- लाइसेंस कुंजी: {{ license_key }}
- रखरखाव की अवधि: {{ renewal_expires_at }}
- आदेश संख्या: {{ order_number }}

क्या शामिल है:
- प्लेटफॉर्म फीचर अपडेट और सुधार
- सुरक्षा पैच और बग फिक्स
- अपग्रेड सर्वर के माध्यम से नए कम्पोनेंट रिलीज
- तकनीकी समर्थन

आपकी ओर से कोई कार्रवाई आवश्यक नहीं है। अपडेट आपके प्रशासन पैनल के कम्पोनेंट अपडेट प्रणाली के माध्यम से लगातार उपलब्ध रहेगा।

मदद की आवश्यकता है? {{ support_email }} से संपर्क करें