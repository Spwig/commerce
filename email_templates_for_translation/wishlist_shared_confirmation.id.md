---
template_type: wishlist_shared_confirmation
category: Wishlist
---

# Email Template: wishlist_shared_confirmation

## Subject
✓ Daftar Keinginan Anda Telah Dibagikan - {{ shop_name }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section>
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          ✓ Wishlist Telah Dibagikan dengan Sukses!
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Hai {{ customer_name }},
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Daftar keinginan Anda dengan {{ wishlist_item_count }} item{{ wishlist_item_count|pluralize }} telah dibagikan dengan sukses. Orang lain kini dapat melihat daftar keinginan Anda menggunakan tautan di bawah ini.
        </mj-text>

        <mj-spacer height="30px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
              Tautan Bagikan:
            </mj-text>
            <mj-text font-family="'Courier New', monospace" font-size="14px" color="{{ theme.color.primary|default:'#2563eb' }}">
              {{ share_url }}
            </mj-text>
            <mj-spacer height="15px" />
            <mj-button href="{{ share_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="14px" border-radius="6px" padding="10px 25px">
              Salin Tautan
            </mj-button>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Apa yang Dibagikan:
        </mj-text>

        <mj-text font-size="14px" color="{{ theme.color.text|default:'#4b5563' }}">
          • Nama daftar keinginan Anda (jika diatur)<br/>
          • {{ wishlist_item_count }} produk{{ wishlist_item_count|pluralize }}<br/>
          • Nama, gambar, dan harga produk<br/>
          • Tautan pembelian untuk setiap item
        </mj-text>

        <mj-spacer height="30px" />

        <mj-section background-color="#f0fdf4" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="14px" color="#065f46" align="center">
              💡 Sempurna untuk dibagikan dengan teman dan keluarga untuk hadiah dan kesempatan khusus!
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-button href="{{ wishlist_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" border-radius="6px" padding="12px 30px">
          Kelola Daftar Keinginan Saya
        </mj-button>

        <mj-spacer height="20px" />

        <mj-text font-size="13px" color="{{ theme.color.text_secondary|default:'#6b7280' }}" align="center">
          Ingin berhenti berbagi? Anda dapat menonaktifkan tautan berbagi kapan saja di <a href="{{ wishlist_settings_url }}">pengaturan daftar keinginan</a> Anda.
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
✓ DAFTAR KEINGINAN TELAH DIBAGIKAN DENGAN SUKSES!

Hai {{ customer_name }},

Daftar keinginan Anda dengan {{ wishlist_item_count }} item{{ wishlist_item_count|pluralize }} telah dibagikan dengan sukses. Orang lain kini dapat melihat daftar keinginan Anda menggunakan tautan di bawah ini.

TAUTAN BAGIKAN:
{{ share_url }}

APA YANG DIBAGIKAN:
• Nama daftar keinginan Anda (jika diatur)
• {{ wishlist_item_count }} produk{{ wishlist_item_count|pluralize }}
• Nama, gambar, dan harga produk
• Tautan pembelian untuk setiap item

💡 Sempurna untuk dibagikan dengan teman dan keluarga untuk hadiah dan kesempatan khusus!

Kelola daftar keinginan saya: {{ wishlist_url }}

Ingin berhenti berbagi? Anda dapat menonaktifkan tautan berbagi kapan saja di pengaturan daftar keinginan Anda: {{ wishlist_settings_url }}