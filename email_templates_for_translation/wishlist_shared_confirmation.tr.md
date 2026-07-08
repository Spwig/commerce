---
template_type: wishlist_shared_confirmation
category: Wishlist
---

# Email Template: wishlist_shared_confirmation

## Subject
✓ {{ shop_name }} alışveriş listesi paylaşıldı

## HTML Content
<mjml>
  <mj-body>
    <mj-section>
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          ✓ Favori Listesi Başarıyla Paylaşıldı!
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Merhaba {{ customer_name }},
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          {{ wishlist_item_count }} ürününüz olan favori listeniz başarıyla paylaşıldı. Şimdi aşağıda belirtilen linki kullanarak diğerlerinin favori listenizi görebilmesine izin verebilirsiniz.
        </mj-text>

        <mj-spacer height="30px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
              Paylaşılan Link:
            </mj-text>
            <mj-text font-family="'Courier New', monospace" font-size="14px" color="{{ theme.color.primary|default:'#2563eb' }}">
              {{ share_url }}
            </mj-text>
            <mj-spacer height="15px" />
            <mj-button href="{{ share_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="14px" border-radius="6px" padding="10px 25px">
              Linki Kopyala
            </mj-button>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Paylaşılanlar:
        </mj-text>

        <mj-text font-size="14px" color="{{ theme.color.text|default:'#4b5563' }}">
          • Favori listenizin adı (ayarlandıysa)<br/>
          • {{ wishlist_item_count }} ürün<br/>
          • Ürün adları, resimler ve fiyatları<br/>
          • Her ürün için satın alma linkleri
        </mj-text>

        <mj-spacer height="30px" />

        <mj-section background-color="#f0fdf4" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="14px" color="#065f46" align="center">
              💡 Arkadaşlarınız ve ailenizle hediyeler ve özel etkinlikler için paylaşmak için harika!
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-button href="{{ wishlist_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" border-radius="6px" padding="12px 30px">
          Favori Listemi Yönet
        </mj-button>

        <mj-spacer height="20px" />

        <mj-text font-size="13px" color="{{ theme.color.text_secondary|default:'#6b7280' }}" align="center">
          Paylaşmayı durdurmak isterseniz, <a href="{{ wishlist_settings_url }}">favori listesi ayarlarınızda</a> herhangi bir zaman paylaşım linkini devre dışı bırakabilirsiniz.
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
✓ FAVORİ LİSTE BAŞARIYLA PAYLAŞILDI!

Merhaba {{ customer_name }},

{{ wishlist_item_count }} ürününüz olan favori listeniz başarıyla paylaşıldı. Şimdi aşağıda belirtilen linki kullanarak diğerlerinin favori listenizi görebilmesine izin verebilirsiniz.

PAYLAŞILAN LINK:
{{ share_url }}

PAYLAŞILANLAR:
• Favori listenizin adı (ayarlandıysa)
• {{ wishlist_item_count }} ürün
• Ürün adları, resimler ve fiyatları
• Her ürün için satın alma linkleri

💡 Arkadaşlarınız ve ailenizle hediyeler ve özel etkinlikler için paylaşmak için harika!

Favori listemi yönet: {{ wishlist_url }}

Paylaşmayı durdurmak isterseniz, herhangi bir zaman favori listesi ayarlarınızda paylaşım linkini devre dışı bırakabilirsiniz: {{ wishlist_settings_url }}