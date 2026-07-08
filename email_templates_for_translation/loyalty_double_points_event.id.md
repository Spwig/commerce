---
template_type: loyalty_double_points_event
category: Loyalty Program
---

# Email Template: loyalty_double_points_event

## Subject
🔥 Acara 2X Poin Dimulai Sekarang! - {{ shop_name }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#fef3c7">
      <mj-column>
        <mj-text font-size="28px" font-weight="bold" color="#92400e" align="center">
          🔥 ACARA 2X POIN!
        </mj-text>
        <mj-text font-size="18px" color="#92400e" align="center">
          {{ event_start }} - {{ event_end }}
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Eksklusif untuk Anggota Loyalitas!
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Hi {{ customer_name }},
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Siap untuk mendapatkan poin besar! Untuk waktu terbatas, Anda akan mendapatkan {{ points_multiplier }}X poin pada setiap pembelian.
        </mj-text>

        <mj-spacer height="30px" />

        <mj-section background-color="#dcfce7" border-radius="8px" padding="25px">
          <mj-column>
            <mj-text font-size="24px" font-weight="bold" color="#047857" align="center">
              Dapatkan {{ points_multiplier }}X Poin
            </mj-text>
            <mj-text font-size="16px" color="#065f46" align="center">
              Pada semua pembelian<br/>
              {{ event_start }} - {{ event_end }}
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Contoh Poin yang Didapat:
        </mj-text>

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="4px" padding="15px">
          <mj-column>
            <mj-text font-size="14px" color="{{ theme.color.text|default:'#4b5563' }}">
              Beli $50 → Dapatkan {{ example_points_normal }} poin secara normal<br/>
              <strong style="color: #047857;">Selama acara ini → Dapatkan {{ example_points_bonus }} poin! 🎉</strong>
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="20px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="4px" padding="15px">
          <mj-column>
            <mj-text font-size="14px" color="{{ theme.color.text|default:'#4b5563' }}">
              Beli $100 → Dapatkan {{ example_points_normal_2 }} poin secara normal<br/>
              <strong style="color: #047857;">Selama acara ini → Dapatkan {{ example_points_bonus_2 }} poin! 🎉</strong>
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Saldo Anda Saat Ini:
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}">
          <strong>Poin:</strong> {{ current_points }} poin<br/>
          <strong>Tier:</strong> {{ loyalty_tier }}
        </mj-text>

        <mj-spacer height="30px" />

        <mj-button href="{{ shop_url }}" background-color="#dc2626" color="#ffffff" font-size="18px" font-weight="bold" border-radius="6px" padding="18px 50px">
          Belanja Sekarang & Dapatkan {{ points_multiplier }}X Poin
        </mj-button>

        <mj-spacer height="20px" />

        <mj-text font-size="13px" color="#dc2626" align="center" font-weight="bold">
          Acara berakhir {{ event_end }} - Jangan lewatkan!
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
🔥 ACARA 2X POIN!
{{ event_start }} - {{ event_end }}

Eksklusif untuk Anggota Loyalitas!

Hi {{ customer_name }},

Siap untuk mendapatkan poin besar! Untuk waktu terbatas, Anda akan mendapatkan {{ points_multiplier }}X poin pada setiap pembelian.

DAPATKAN {{ points_multiplier }}X POIN
Pada semua pembelian
{{ event_start }} - {{ event_end }}

CONTOH PEMOTONGAN:
- Beli $50 → Dapatkan {{ example_points_normal }} poin secara normal
  Selama acara ini → Dapatkan {{ example_points_bonus }} poin! 🎉

- Beli $100 → Dapatkan {{ example_points_normal_2 }} poin secara normal
  Selama acara ini → Dapatkan {{ example_points_bonus_2 }} poin! 🎉

SALDO ANDA SAAT INI:
- Poin: {{ current_points }} poin
- Tier: {{ loyalty_tier }}

Belanja sekarang & dapatkan {{ points_multiplier }}X poin: {{ shop_url }}

Acara berakhir {{ event_end }} - Jangan lewatkan!