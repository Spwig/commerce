---
title: Özel Alanlar
---

Özel alanlar, ürünleri, kategorileri, siparişleri ve müşteri profillerini değiştirmeden ek veri eklemenizi sağlar. Onları, dış API kimliklerini, depo konumlarını, uyumluluk verilerini veya mağazanızın ihtiyaç duyduğu herhangi bir özniteliği saklamak için kullanın.

## Özel Alanlara Erişim

**Ayarlar > Özel Alanlar** bölümünde bulunan admin yan çubuğundan erişin.

![Özel Alanlar sayfası](/static/core/admin/img/help/custom-fields/custom-fields-page.webp)

## Temel Kavramlar

### Alan Grupları

Alanlar, mantıksal koleksiyonlar olarak görünen birlikte görünen bölümler halinde **gruplara** organize edilir. Örneğin, "Kargo Bilgisi" grubu, depo konumu, paket boyutları ve tehlikeli madde sınıflandırması için alanları içerebilir.

### Alan Tanımları

Her alan tanımı şu şeyleri kontrol eder:
- **Ad**: Formlarda gösterilen etiket
- **Slug**: JSON depolama ve API yanıtlarında kullanılan makine okunabilir anahtar
- **Alan Türü**: Render edilen giriş türü (metin, sayı, açılır liste vb.)
- **Doğrulama**: Min/max, maksimum uzunluk, regex veya izin verilen seçenekler gibi kurallar
- **Görünüm**: Alanın mağaza ön yüzünde görünüp görünmeyeceğini belirler

### Desteklenen Alan Türleri

| Tür | Açıklama | Örnek Kullanım |
|------|-------------|-------------|
| **Metin** | Tek satırlık metin girişi | Dış API Kimliği, marka kodu |
| **Metin Alanı** | Çok satırlık metin | Özel işlem notları |
| **Sayı** | Tamsayı değerleri | Minimum sipariş miktarı |
| **Ondalık** | Ondalık değerler | Ağırlık geçersizleştirme, özel boyut |
| **Evet/Hayır** | Onay kutusu | Kırılgan mı, imza gerekli mi |
| **Tarih** | Tarih seçici | Yayın tarihi, son kullanma tarihi |
| **Tarih & Saat** | Tarih ve saat seçici | Planlı mevcutluk |
| **URL** | Web adresi | Tedarikçi bağlantısı, teknik özellik sayfası URL'si |
| **E-posta** | E-posta adresi | Üretici iletişim |
| **Açılır Liste** | Tekli seçim listesi | Malzeme türü, köken ülkesi |
| **Çoklu Seçim** | Çoklu seçim listesi | Sertifikalar, etiketler |
| **Renk** | Renk seçici | Marka rengi, etiket rengi |

## Özel Alanları Yönetme

### Bir Alan Grubu Oluşturma

1. **Ayarlar > Özel Alanlar** açın
2. Model sekmesini seçin (Ürünler, Kategoriler, Siparişler veya Müşteri Profilleri)
3. **Grup Ekle**'ye tıklayın
4. Bir **Grup Adı** girin (örneğin, "Dış Entegrasyonlar")
5. Bu alanların müşteriler tarafından görünmesi gerekiyorsa, **Mağaza ön yüzünde Göster**'i isteğe bağlı olarak etkinleştirin
6. **Grubu Kaydet**'e tıklayın

### Bir Gruba Alan Ekleme

1. Grup kartında **Alan Ekle**'ye tıklayın
2. Bir **Alan Adı** girin — slug otomatik olarak oluşturulur
3. **Alan Türünü** seçin
4. İsteğe bağlı olarak bir **Yardım Metni** ve **Varsayılan Değer** ayarlayın
5. Doğrulama seçeneklerini yapılandırın (alan türüne göre değişir):
   - Metin: maksimum uzunluk, regex deseni
   - Sayı/Ondalık: min ve max değerleri
   - Açılır Liste: seçenekler listesini tanımlayın
6. Alan seçeneklerini ayarlayın:
   - **Gerekli**: Satıcılar, kaydetme sırasında bu alanı doldurmak zorundadır
   - **Mağaza ön yüzünde Göster**: Müşteri odaklı sayfada değeri görüntüleyin
   - **Çevrilebilir**: Değerin çevrilebilir olmasına izin verin (yalnızca metin/metin alanı)
7. **Alanı Kaydet**'e tıklayın

### Düzenleme ve Sıralama

- Herhangi bir grup veya alana tıklayarak **kalem simgesini** düzenleyin
- **grip handle**'ı sürükleyerek grupları veya bir gruptaki alanları sıralayın
- Değişiklikler, ilgili tüm formlar üzerinde hemen etkilidir

### Gruplar ve Alanları Silme

- Bir grup veya alana tıklayarak **çöp simgesini** silin
- Silmeler **zayıf silmelerdir** — veriler veritabanında korunur ancak formlardan gizlenir
- Bu, mevcut verilerin yanlışlıkla kaybolmasından korur

## Formlarda Özel Alanlar Kullanma

Bir model için özel alanlar tanımladığınızda, ilgili düzenleme formunda otomatik olarak bir **Özel Alanlar** sekmesi görünür olur.

### Ürünler ve Kategoriler

1. Herhangi bir ürün veya kategoriyi düzenleme için açın
2. **Özel Alanlar** sekmesine tıklayın
3. Gerekli alanları doldurun
4. **Kaydet**'e tıklayın — değerler kayda eşlik edilir

### Siparişler

Siparişler için özel alan değerleri, sipariş detay sayfasında bir **sadece okunabilir bölüm** olarak görüntülenir. Sipariş özel alanları genellikle API veya ödeme sırasında ayarlanır.

### Müşteri Profilleri

1. Bir müşteri profilini açın
2. **Özel Alanlar** sekmesine tıklayın
3. Alanları doldurun ve kaydedin

## API Erişimi

### Alan Tanımlarını Listeleme

Bir model için tüm özel alan tanımlarını alın:

```
GET /api/custom-fields/definitions/?model=product&app=catalog
```

**Yanıt:"
```json
[
  {
    "id": 1,
    "name": "Dış API Kimliği",
    "slug": "external_api_id",
    "field_type": "text",
    "is_required": false,
    "group": { "name": "Dış Entegrasyonlar" }
  }
]
```

### Özel Alan Değerlerini Okuma

Özel alan değerleri, model API yanıtlarında `custom_fields` JSON nesnesinde yer alır:

```json
{
  "id": 42,
  "name": "Mavi Cihaz",
  "custom_fields": {
    "external_api_id": "API-12345",
    "is_fragile": true
  }
}
```

### Özel Alan Değerlerini Yazma

API üzerinden bir kaydı oluştururken veya güncellerken `custom_fields`'i dahil edin:

```json
{
  "custom_fields": {
    "external_api_id": "API-67890",
    "warehouse_location": "WH-A3"
  }
}
```

Değerler, alan tanımlarıyla doğrulanır. Geçersiz değerler, ayrıntılarla birlikte bir `400` hatası döndürür.

### Özel Alanlara Göre Sorgulama

Özel alanlar, hızlı veritabanı sorguları için dizine alınmıştır. Kayıtları filtrelemek için veritabanı sorgu filtrelerini kullanın:

```
GET /api/products/?custom_fields__warehouse_location=WH-A3
```

## Mağaza Ön Yüzünde Gösterim

### Tema Geliştiricileri İçin

Mağaza ön yüzünde özel alanları göstermek için `render_custom_fields` şablon etiketini kullanın:

```python
{% load custom_fields_tags %}

{# Mağaza ön yüzünde görünen tüm alanları göster #}
{% render_custom_fields product %}

{# Belirli bir alan değerini alın #}
{% get_custom_field product "warehouse_location" as location %}
<p>Kargo: {{ location }}</p>
```

Grup ve alan düzeyinde **Mağaza ön yüzünde Göster** etkinleştirilmiş olan alanlar yalnızca işlenir.

## En İyi Uygulamalar

- **Açıklayıcı isimler kullanın** — alan isimleri formlarda ve mağaza ön yüzünde görünür
- **Yardım metni ayarlayın** — satıcıların her alanın içine ne gireceğini rehberlik edin
- **İlgili alanları gruplandırın** — formları organize ve sezgisel tutun
- **Varsayılan değerleri kullanın** — veri girişi azaltmak için mantıklı varsayılanlar ayarlayın
- **Mağaza ön yüzü görünümüne dikkatli olun** — sadece müşterilere anlamlı olan alanları gösterin
- **Entegrasyonlarda slug kullanın** — slugs sabit kimliklerdir; alan isimleri değişebilir

## Sorun Giderme

**Özel Alanlar sekmesi görünmüyorsa:**
- Bu model için en az bir aktif alan grubunun mevcut olduğundan emin olun
- Admin sınıfının `CustomFieldsAdminMixin` içerdiğinden emin olun
- Önbelleği temizleyin ve sayfayı yenileyin

**Alan değerleri kaydedilmiyorsa:**
- Gerekli alanların doldurulduğundan emin olun
- Doğrulama kurallarını kontrol edin (min/max, regex desenleri, izin verilen seçenekler)
- Alanın aktif olduğundan ve zayıf silinmediğinden emin olun

**API özel_fields boş döndürüyorsa:**
- Modelin `CustomFieldsMixin` içerdiğinden emin olun
- Doğru içerik türü için alan tanımlarının mevcut olduğundan emin olun
- Serializerın `CustomFieldsSerializerMixin` içerdiğinden emin olun

## İlgili Konular

- [Ürün Ekleme](#)
- [Mağaza Ayarları](#)