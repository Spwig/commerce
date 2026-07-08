---
template_type: digital_product_license_key
category: Digital Products
---

# Email Template: digital_product_license_key

## Subject
Lisans Anahtarınız - Sipariş #{{ order_number }}

## HTML Content
<mjml>
  <mj-head>
    <mj-attributes>
      <mj-all font-family="'Helvetica Neue', Helvetica, Arial, sans-serif" />
      <mj-text font-size="14px" color="#333333" line-height="20px" />
      <mj-section background-color="{{ theme.color.background|default:'#ffffff' }}" padding="20px" />
    </mj-attributes>
  </mj-head>
  <mj-body background-color="{{ theme.color.background_secondaryondary|default:'#f9fafb' }}">
    <!-- Header -->
    <mj-section background-color="#059669" padding="20px">
      <mj-column>
        <mj-text font-size="24px" font-weight="bold" color="{{ theme.color.background|default:'#ffffff' }}" align="center">
          Lisans Anahtarınız Hazır
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Main Content -->
    <mj-section>
      <mj-column>
        <mj-text font-size="16px">
          Merhaba {{ customer_name }},
        </mj-text>
        <mj-text>
          {{ product_name }} ürününüz için teşekkür ederiz! Aktivasyon için lisans anahtarınız aşağıdadır.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- License Key Box -->
    <mj-section background-color="#f0fdf4" padding="30px" border="2px solid #059669" border-radius="8px">
      <mj-column>
        <mj-text font-size="12px" color="#065f46" font-weight="bold" align="center">
          LISANS ANAHTARINIZ
        </mj-text>
        <mj-text font-size="20px" font-weight="bold" color="#059669" align="center" font-family="'Courier New', monospace" padding="10px 0">
          {{ license_key }}
        </mj-text>
        <mj-text font-size="12px" color="{{ theme.color.text_muted|default:'#6b7280' }}" align="center">
          Kopyalayın ya da dikkatlice not alın
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- License Details -->
    <mj-section>
      <mj-column>
        <mj-text font-size="14px" font-weight="bold">
          Lisans Detayları:
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          • Ürün: {{ product_name }}
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          • Sürüm: {{ product_version }}
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          • Lisans Türü: {{ license_type }}
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          • Maksimum Aktivasyonlar: {{ max_activations }} cihaz(lar)
        </mj-text>
        {% if is_lifetime %}
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          • Geçerlilik: Hayat Boyu Lisans
        </mj-text>
        {% else %}
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          • Geçerlilik Bitiş Tarihi: {{ expiration_date }}
        </mj-text>
        {% endif %}
      </mj-column>
    </mj-section>

    <!-- Activation Instructions -->
    <mj-section background-color="{{ theme.color.background_secondaryondary|default:'#f9fafb' }}" padding="20px" border-radius="8px">
      <mj-column>
        <mj-text font-size="16px" font-weight="bold">
          Aktivasyon Nasıl Yapılır:
        </mj-text>
        <mj-text font-size="14px">
          1. Yazılımı indirin ve yükleyin
        </mj-text>
        <mj-text font-size="14px">
          2. Uygulamayı açın
        </mj-text>
        <mj-text font-size="14px">
          3. Lisans anahtarınızı istendiğinde girin
        </mj-text>
        <mj-text font-size="14px">
          4. İşlemi tamamlamak için "Aktif Et" butonuna tıklayın
        </mj-text>
      </mj-column>
    </mj-section>

    {% if download_url %}
    <!-- Download Button -->
    <mj-section>
      <mj-column>
        <mj-button href="{{ download_url }}" background-color="#059669" color="{{ theme.color.background|default:'#ffffff' }}" font-size="16px" padding="15px 30px" border-radius="6px">
          Yazılımı İndir
        </mj-button>
      </mj-column>
    </mj-section>
    {% endif %}

    <!-- Important Notice -->
    <mj-section>
      <mj-column>
        <mj-text font-size="14px" color="{{ theme.color.error|default:'#ef4444' }}" font-weight="bold">
          ⚠️ Önemli:
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          • Bu e-postayı güvenli bir yerde saklayınız - yeniden kurulum için lisans anahtarına ihtiyacınız olacak
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          • Lisans anahtarınızı başkalarıyla paylaşmayın
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          • Hesap panelinizden cihazları devre dışı bırakabilirsiniz
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Support -->
    <mj-section>
      <mj-column>
        <mj-divider border-color="{{ theme.color.border|default:'#e5e7eb' }}" />
        <mj-text font-size="12px" color="#9ca3af" align="center">
          Aktivasyonla ilgili yardım mı istiyorsunuz? {{ support_email }} ile iletişime geçin
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
Lisans Anahtarınız Hazır

Merhaba {{ customer_name }},

{{ product_name }} ürününüz için teşekkür ederiz! Aktivasyon için lisans anahtarınız aşağıdadır.

LISANS ANAHTARINIZ:
{{ license_key }}

Lisans Detayları:
• Ürün: {{ product_name }}
• Sürüm: {{ product_version }}
• Lisans Türü: {{ license_type }}
• Maksimum Aktivasyonlar: {{ max_activations }} cihaz(lar)
{% if is_lifetime %}• Geçerlilik: Hayat Boyu Lisans{% else %}• Geçerlilik Bitiş Tarihi: {{ expiration_date }}{% endif %}

Aktivasyon Nasıl Yapılır:
1. Yazılımı indirin ve yükleyin
2. Uygulamayı açın
3. Lisans anahtarınızı istendiğinde girin
4. İşlemi tamamlamak için "Aktif Et" butonuna tıklayın

{% if download_url %}Yazılımı İndir: {{ download_url }}

{% endif %}Önemli:
• Bu e-postayı güvenli bir yerde saklayınız - yeniden kurulum için lisans anahtarına ihtiyacınız olacak
• Lisans anahtarınızı başkalarıyla paylaşmayın
• Hesap panelinizden cihazları devre dışı bırakabilirsiniz

Aktivasyonla ilgili yardım mı istiyorsunuz? {{ support_email }}