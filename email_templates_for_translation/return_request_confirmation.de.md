---
template_type: return_request_confirmation
category: Returns
---

# Email Template: return_request_confirmation

## Subject
Rückgabeantrag erhalten - Bestellung #{{ order_number }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="{{ theme.color.surface|default:'#eff6ff' }}">
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="{{ theme.color.text|default:'#1e40af' }}">
          Rückgabeantrag erhalten
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text|default:'#1e40af' }}">
          Bestellung #{{ order_number }}
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Hi {{ customer_name }},
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Wir haben Ihren Rückgabeantrag für die Bestellung <strong>#{{ order_number }}</strong> erhalten.
        </mj-text>

        <mj-spacer height="20px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
              Rückgabeantrag-Details:
            </mj-text>
            <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>Grund:</strong> {{ return_reason }}<br/>
              <strong>Artikel:</strong> {{ items_count }} Artikel(s)<br/>
              <strong>Status:</strong> {{ return_status }}
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="20px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Was geschieht als nächstes?
        </mj-text>

        <mj-text font-size="15px" line-height="1.8" color="{{ theme.color.text|default:'#4b5563' }}">
          1. Unser Team wird Ihren Rückgabeantrag innerhalb von 24–48 Stunden prüfen<br/>
          2. Sobald der Antrag genehmigt ist, senden wir Ihnen eine Rücksendeetikett per E-Mail<br/>
          3. Packen Sie die Artikel sicher und heften Sie das Rücksendeetikett an<br/>
          4. Geben Sie das Paket bei der nächsten Versandstelle ab<br/>
          5. Die Rückerstattung wird verarbeitet, sobald wir die Artikel erhalten und geprüft haben
        </mj-text>

        <mj-spacer height="20px" />

        <mj-text font-size="15px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Wenn Sie Fragen haben, zögern Sie nicht, uns zu kontaktieren.
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
RÜCKGABEANTRAG ERHALTEN
Bestellung #{{ order_number }}

Hi {{ customer_name }},

Wir haben Ihren Rückgabeantrag für die Bestellung #{{ order_number }} erhalten.

RÜCKGABEANTRAG-DETAILS:
- Grund: {{ return_reason }}
- Artikel: {{ items_count }} Artikel(s)
- Status: {{ return_status }}

WAS GESCHIEHT ALS NÄCHSTES?
1. Unser Team wird Ihren Rückgabeantrag innerhalb von 24–48 Stunden prüfen
2. Sobald der Antrag genehmigt ist, senden wir Ihnen eine Rücksendeetikett per E-Mail
3. Packen Sie die Artikel sicher und heften Sie das Rücksendeetikett an
4. Geben Sie das Paket bei der nächsten Versandstelle ab
5. Die Rückerstattung wird verarbeitet, sobald wir die Artikel erhalten und geprüft haben

Wenn Sie Fragen haben, zögern Sie nicht, uns zu kontaktieren.