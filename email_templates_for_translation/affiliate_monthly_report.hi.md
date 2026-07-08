---
template_type: affiliate_monthly_report
category: Affiliate Program
---

# Email Template: affiliate_monthly_report

## Subject
आपकी मासिक पार्टनर रिपोर्ट - {{ month_name }} {{ year }}

## HTML Content
<mjml>
  <mj-head>
    <mj-attributes>
      <mj-text font-family="Arial, sans-serif" line-height="1.6" />
      <mj-all font-family="Arial, sans-serif" />
    </mj-attributes>
  </mj-head>
  <mj-body background-color="#f8f9fa">
    <!-- Header -->
    <mj-section background-color="#ffffff" padding="40px 20px">
      <mj-column>
        <mj-text font-size="32px" font-weight="bold" color="#212529" align="center">
          📊 मासिक पार्टनर रिपोर्ट
        </mj-text>
        <mj-text font-size="18px" color="#6c757d" align="center">
          {{ month_name }} {{ year }} प्रदर्शन सारांश
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Summary Cards -->
    <mj-section background-color="#ffffff" padding="20px">
      <mj-column width="33%">
        <mj-text font-size="14px" color="#6c757d" align="center" padding-bottom="5px">
          💰 कुल कमाई
        </mj-text>
        <mj-text font-size="28px" font-weight="bold" color="#28a745" align="center" line-height="1">
          {{ total_earned }}
        </mj-text>
      </mj-column>
      <mj-column width="33%">
        <mj-text font-size="14px" color="#6c757d" align="center" padding-bottom="5px">
          📦 कमीशन
        </mj-text>
        <mj-text font-size="28px" font-weight="bold" color="#007bff" align="center" line-height="1">
          {{ commission_count }}
        </mj-text>
      </mj-column>
      <mj-column width="33%">
        <mj-text font-size="14px" color="#6c757d" align="center" padding-bottom="5px">
          📈 प्रति बिक्री औसत
        </mj-text>
        <mj-text font-size="28px" font-weight="bold" color="#6f42c1" align="center" line-height="1">
          {{ avg_commission }}
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Greeting -->
    <mj-section background-color="#f8f9fa" padding="30px 20px">
      <mj-column>
        <mj-text font-size="16px" color="#212529">
          हाय {{ affiliate_name }},
        </mj-text>
        <mj-text font-size="16px" color="#212529">
          यहाँ {{ month_name }} {{ year }} के लिए आपका प्रदर्शन सारांश है। इस महीने आपका अच्छा काम है!
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Top Orders Table -->
    <mj-section background-color="#ffffff" padding="20px">
      <mj-column>
        <mj-text font-size="18px" font-weight="bold" color="#212529" padding-bottom="15px">
          🏆 {{ top_orders_count }} शीर्ष आदेश
        </mj-text>
        <mj-text font-size="14px" color="#212529">
          <table style="width: 100%; border-collapse: collapse;">
            <thead>
              <tr style="background-color: #f8f9fa;">
                <th style="padding: 10px; text-align: left; border-bottom: 2px solid #dee2e6;">आदेश</th>
                <th style="padding: 10px; text-align: right; border-bottom: 2px solid #dee2e6;">कमीशन</th>
                <th style="padding: 10px; text-align: right; border-bottom: 2px solid #dee2e6;">तिथि</th>
              </tr>
            </thead>
            <tbody>
              {% for order in top_orders %}
              <tr>
                <td style="padding: 10px; border-bottom: 1px solid #dee2e6;">#{{ order.order_number }}</td>
                <td style="padding: 10px; text-align: right; border-bottom: 1px solid #dee2e6; color: #28a745; font-weight: 600;">{{ order.commission_amount }}</td>
                <td style="padding: 10px; text-align: right; border-bottom: 1px solid #dee2e6; color: #6c757d;">{{ order.order_date }}</td>
              </tr>
              {% endfor %}
            </tbody>
          </table>
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Payment Status -->
    <mj-section background-color="#e3f2fd" padding="20px">
      <mj-column>
        <mj-text font-size="16px" color="#212529">
          <strong>💳 भुगतान का स्थिति</strong>
        </mj-text>
        <mj-text font-size="14px" color="#212529">
          अपेक्षित शेष: <strong>{{ pending_balance }}</strong><br/>
          स्थिति: {{ payment_status }}
          {% if next_payout_date %}
          <br/>अगला भुगतान: {{ next_payout_date }}
          {% endif %}
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- CTA -->
    <mj-section background-color="#ffffff" padding="30px 20px">
      <mj-column>
        <mj-button background-color="#007bff" color="#ffffff" href="{{ portal_url }}">
          पूरा डैशबोर्ड देखें
        </mj-button>
      </mj-column>
    </mj-section>

    <!-- Footer -->
    <mj-section background-color="#f8f9fa" padding="20px">
      <mj-column>
        <mj-text font-size="12px" color="#6c757d" align="center">
          {{ shop_name }}<br/>
          सवाल हैं? <a href="mailto:{{ support_email }}" style="color: #007bff;">समर्थन से संपर्क करें</a>
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
आपकी मासिक पार्टनर रिपोर्ट - {{ month_name }} {{ year }}

हाय {{ affiliate_name }},

यहाँ {{ month_name }} {{ year }} के लिए आपका प्रदर्शन सारांश है:

📊 मासिक सारांश
- कुल कमाई: {{ total_earned }}
- कमीशन की संख्या: {{ commission_count }}
- प्रति बिक्री औसत: {{ avg_commission }}

🏆 {{ top_orders_count }} शीर्ष आदेश
{% for order in top_orders %}
#{{ order.order_number }} - {{ order.commission_amount }} ({{ order.order_date }})
{% endfor %}

💳 भुगतान की स्थिति
अपेक्षित शेष: {{ pending_balance }}
स्थिति: {{ payment_status }}
{% if next_payout_date %}अगला भुगतान: {{ next_payout_date }}{% endif %}

अपना पूरा डैशबोर्ड देखें: {{ portal_url }}

इस महीने आपका अच्छा काम है!

{{ shop_name }}
सवाल हैं? {{ support_email }} से संपर्क करें

