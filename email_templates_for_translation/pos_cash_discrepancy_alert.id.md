---
template_type: pos_cash_discrepancy_alert
category: POS
---

# Email Template: pos_cash_discrepancy_alert

## Subject
⚠️ Perbedaan Uang Tunai: {{ terminal_name }} - {{ discrepancy_amount }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#fef3c7">
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="#92400e" align="center">
          ⚠️ Perbedaan Uang Tunai Terdeteksi
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="18px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Peringatan Perbedaan Uang Tunai
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}">
          Terdeteksi perbedaan uang tunai sebesar {{ discrepancy_amount }} saat menutup shift di {{ terminal_name }}.
        </mj-text>

        <mj-spacer height="20px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
              Detail Perbedaan:
            </mj-text>
            <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>Terminal:</strong> {{ terminal_name }}<br/>
              <strong>Kasir:</strong> {{ cashier_name }}<br/>
              <strong>Tanggal Shift:</strong> {{ shift_date }}<br/>
              <strong>Lama Shift:</strong> {{ shift_duration }}<br/>
              <strong>Terdeteksi:</strong> {{ detected_at }}
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Penghitungan Uang Tunai:
        </mj-text>

        <mj-section background-color="#fef3c7" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text color="#92400e">
              <strong>Uang Tunai yang Diharapkan:</strong> {{ expected_cash }}<br/>
              <strong>Uang Tunai yang Dihitung:</strong> {{ counted_cash }}<br/>
              <strong>Perbedaan:</strong> <span style="font-weight: bold; font-size: 18px;">{{ discrepancy_amount }}</span>
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="20px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="14px" color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>Uang Tunai Awal:</strong> {{ opening_cash }}<br/>
              <strong>Jual Uang Tunai:</strong> {{ cash_sales }}<br/>
              <strong>Pengembalian Uang Tunai:</strong> {{ cash_refunds }}<br/>
              <strong>Uang Tunai yang Dikeluarkan:</strong> {{ cash_paid_out }}
            </mj-text>
          </mj-column>
        </mj-section>

        {% if cashier_note %}
        <mj-spacer height="30px" />
        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Catatan Kasir:
        </mj-text>
        <mj-section background-color="#eff6ff" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="14px" color="#1e40af" line-height="1.6">
              "{{ cashier_note }}"
            </mj-text>
          </mj-column>
        </mj-section>
        {% endif %}

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Tindakan yang Direkomendasikan:
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}" line-height="1.8">
          1. Periksa riwayat transaksi untuk kesalahan<br/>
          2. Periksa pembayaran uang tunai yang tidak tercatat<br/>
          3. Verifikasi penghitungan uang tunai sudah akurat<br/>
          4. Dokumentasikan perbedaan dalam catatan shift<br/>
          5. Lakukan follow-up dengan kasir jika diperlukan
        </mj-text>

        <mj-spacer height="30px" />

        <mj-button href="{{ shift_report_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          Lihat Laporan Shift
        </mj-button>

        <mj-spacer height="10px" />

        <mj-button href="{{ transaction_history_url }}" background-color="#6b7280" color="#ffffff" font-size="14px" border-radius="6px" padding="10px 25px">
          Periksa Transaksi
        </mj-button>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
⚠️ PERBEDAAN UANG TUNAI TERDETEKSI

Peringatan Perbedaan Uang Tunai

Terdeteksi perbedaan uang tunai sebesar {{ discrepancy_amount }} saat menutup shift di {{ terminal_name }}.

DETAIL PERBEDAAN:
- Terminal: {{ terminal_name }}
- Kasir: {{ cashier_name }}
- Tanggal Shift: {{ shift_date }}
- Lama Shift: {{ shift_duration }}
- Terdeteksi: {{ detected_at }}

PENGHITUNGAN UANG TUNAI:
- Uang Tunai yang Diharapkan: {{ expected_cash }}
- Uang Tunai yang Dihitung: {{ counted_cash }}
- Perbedaan: {{ discrepancy_amount }}

BREAKDOWN:
- Uang Tunai Awal: {{ opening_cash }}
- Jual Uang Tunai: {{ cash_sales }}
- Pengembalian Uang Tunai: {{ cash_refunds }}
- Uang Tunai yang Dikeluarkan: {{ cash_paid_out }}

{% if cashier_note %}
CATATAN KASIR:
"{{ cashier_note }}"
{% endif %}

TINDAKAN YANG DIREKOMENDASIKAN:
1. Periksa riwayat transaksi untuk kesalahan
2. Periksa pembayaran uang tunai yang tidak tercatat
3. Verifikasi penghitungan uang tunai sudah akurat
4. Dokumentasikan perbedaan dalam catatan shift
5. Lakukan follow-up dengan kasir jika diperlukan

Lihat laporan shift: {{ shift_report_url }}
Periksa transaksi: {{ transaction_history_url }}