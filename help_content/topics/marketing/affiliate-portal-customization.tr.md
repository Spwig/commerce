---
title: Affiliate Portal Özelleştirme
---

Spwig Affiliate Portalı, potansiyel ortakların program hakkında bilgi edinmeleri ve kaydolmaları için kullanılan kamuya açık bir giriş sayfasıdır. Bu portalı özelleştirerek, mesajlaşma, markalama ve çağrılar-çatı (CTA) ile mağazanızın benzersiz pozisyonunu uyumlu hale getirebilirsiniz. İyi tasarlanmış bir portal, yüksek kaliteli ortakları çeker ve ziyaretçileri aktif ortaklara dönüştürür.

## Affiliate Portalı Nedir?

Affiliate portalı, mağazanızın etki alanındaki `/affiliate/` yolunda erişilebilir. Aşağıdaki işlevleri sağlar:

- **Keşif Sayfası** — Potansiyel ortakların komisyon yapısını, faydalarını ve gereksinimlerini öğrenmesi için
- **Kayıt Giriş Noktası** — Yeni ortaklar için kayıt formu (misafir kayıt veya hesaba dayalı)
- **Giriş Ağ geçidi** — Mevcut ortaklar, dashboard'larına erişmek için giriş yapabilir
- **Marka Gösterisi** — Mağazanızın kimliğini ve affiliate programı değer önerisini yansıtır

Portal, Affiliate Ayarları admin paneli aracılığıyla tamamen özelleştirilebilir, bu da anasayfa mesajı, özellik vurguları, adım adım akışlar ve kayıt seçenekleri dahil olmak üzere birçok alanı içerir.

![Affiliate Portal Landing Page](/static/core/admin/img/help/affiliate-portal-customization/portal-landing.webp)

## Ayarlara Erişim

**Pazarlama > Affiliate Programı > Portal Ayarları** yolunu takip ederek portalı özelleştirebilirsiniz.

Affiliate Ayarları modeli bir **tekil** (singleton) modeldir — mağazanız için tamamen bir ayar kaydı vardır. Tüm alanlar, Spwig'ın çeviri sistemiyle **çevrilebilir**, bu nedenle mağazanızın desteklediği her dille mesajlaşmayı özelleştirebilirsiniz.

## Anasayfa Bölümü

Anasayfa bölümü, potansiyel ortakların ilk gördüğü bölümdür. Aşağıdakileri içerir:

- **Başlık** — Ana başlık (örneğin, "Affiliate Programımıza Katıl"),
- **Alt Başlık** — Programın değerini açıklayan destekleyici metin (örneğin, "Premium ürünleri hedef kitlenize tanıtarak komisyon kazanın"),
- **İstatistikler** — Otomatik olarak görüntülenen ölçümler:
  - Toplam aktif programlar
  - Toplam aktif ortaklar
  - Ortalama komisyon oranı (tüm aktif programlar üzerinden hesaplanır)
- **CTA Butonları** — Otomatik olarak oluşturulur:
  - **Giriş Yap** — Mevcut ortaklar için
  - **Ortak Ol** — Kayıt akışını başlatır

### Anasayfa Mesajlaşmasını Özelleştirme

| Alan | Örnek Değer | Amaç |
|------|-------------|------|
| **Anasayfa Başlığı** | "Bize Ortak Olun & Kazanın" | Fayda odaklı başlıkla dikkat çekin |
| **Anasayfa Alt Başlığı** | "500'den fazla ortak, her yönlendirdiğiniz satış için rekabetçi komisyonlar kazanıyor" | Sosyal kanıt sağlayın ve teklifi açıklayın |

İstatistikler **otomatik olarak hesaplanır** ve aktif programlarınız ve ortaklarınız temelinde anlık olarak güncellenir. Bu değerleri manuel olarak düzenleyemezsiniz.

## Özellikler Bölümü

Özellikler bölümü, ortakların programınıza katılmaları nedenlerini açıklayan **6 özelleştirilebilir fayda kartı** sunar. Her özellik kartı aşağıdaki öğeleri içerir:

- **Simge** — FontAwesome simgesi sınıfı (örneğin, `fa-dollar-sign`, `fa-chart-line`, `fa-headset`)
- **Başlık** — Fayda başlığı (örneğin, "Rekabetçi Komisyonlar")
- **Açıklama** — 1-2 cümle açıklaması (örneğin, "Her yönlendirdiğiniz satış için %15 kazanın")

### Varsayılan Özellikler

Affiliate uygulamasını ilk kez yüklediğinizde Spwig, aşağıdaki varsayılan özellikleri sunar:

| Simge | Başlık | Açıklama |
|-------|--------|---------|
| `fa-dollar-sign` | Rekabetçi Komisyonlar | Her yönlendirdiğiniz satış için yüksek komisyonlar kazanın |
| `fa-link` | Kolay Takip Bağlantıları | Her yerde işe yarar olan benzersiz takip bağlantıları alın |
| `fa-chart-line` | Anlık Analizler | Dashboard'ınızda tıklamaları, dönüşümleri ve kazançları izleyin |
| `fa-calendar-check` | Güvenilir Ödemeler | PayPal veya banka transferi aracılığıyla zamanında ödeme alın |
| `fa-headset` | Özel Desteğe Erişim | Ekibimiz burada, başarıya ulaşmanız için yardımcı olur |
| `fa-gift` | Pazarlama Malzemeleri | Bannere, görseller ve promosyon içeriğine erişin |

### Özellikleri Özelleştirme

Özellikler, veritabanında bir **JSON dizi** olarak saklanır. Admin formunda doğrudan düzenleyebilirsiniz:

```json
[
  {
    "icon": "fa-percent",
    "title": "Up to 20% Commission",
    "description": "Earn industry-leading commissions on premium product sales"
  },
  {
    "icon": "fa-rocket",
    "title": "Fast Approval",
    "description": "Get approved in 24 hours and start promoting immediately"
  },
  {
    "icon": "fa-mobile-alt",
    "title": "Mobile Dashboard",
    "description": "Manage your links and track earnings from any device"
  }
]
```

**Simge Referansı:** FontAwesome 5 Free simgesi sınıfını kullanın. Simgeleri [fontawesome.com/icons](https://fontawesome.com/icons) adresinden tarayın ve sınıf adını kullanın (örneğin, `fa-trophy`, `fa-users`, `fa-star`).

## Nasıl Çalışır Bölümü

"Nasıl Çalışır" bölümü, affiliate yolculuğunu açıklayan bir **4 adımlık görsel akış** görüntüler. Her adım aşağıdaki öğeleri içerir:

- **Başlık** — Adım adı (örneğin, "Kayıt Ol"),
- **Açıklama** — 1-2 cümle açıklaması (ne olur)

### Varsayılan Adımlar

| Adım | Başlık | Açıklama |
|------|--------|---------|
| 1 | Kayıt Ol | Ücretsiz affiliate hesabınızı birkaç dakika içinde oluşturun |
| 2 | Bağlantılarınızı Alın | Her ürün veya sayfaya özel takip bağlantıları oluşturun |
| 3 | Pazarlayın | İçerik, sosyal medya veya e-posta yoluyla hedef kitlenize bağlantılarınızı paylaşın |
| 4 | Komisyon Kazanın | Referans bağlantılarınızla yapılan satışlardan ödeme alın |

### Adımları Özelleştirme

Adımlar, bir **JSON dizi** olarak saklanır. Admin'de düzenleyebilirsiniz:

```json
[
  {
    "title": "Ortak Olma Başvurusu",
    "description": "Başvurunuzu gönderin ve platformunuz hakkında bize bilgi verin"
  },
  {
    "title": "Onaylanma",
    "description": "Ekibimiz 24 saat içinde başvurunuzu inceleyecektir"
  },
  {
    "title": "Bağlantı Oluştur",
    "description": "Dashboard'ınıza erişin ve takip bağlantılarını anında oluşturun"
  },
  {
    "title": "Kazanmaya Başla",
    "description": "Referans bağlantılarınızla yapılan her satıştan komisyon kazanın — PayPal ile aylık ödeme alın"
  }
]
```

Görsel akış, her adımın (1, 2, 3, 4) sayfa başlığında otomatik olarak numaralandırılır.

## CTA Bölümü

Kayıt formundan önceki son bölüm, **Çağrı Yap (CTA) Bölümü**dür. Kayıt yapmaları için bir sonraki itici olur.

| Alan | Örnek Değer | Amaç |
|------|-------------|------|
| **CTA Başlığı** | "Kazanmaya Hazır Mısınız?" | Doğrudan soru, aciliyet yaratır |
| **CTA Açıklaması** | "Bugün affiliate programımıza katılarak sevdikleriniz ve önerdiğiniz ürünler üzerinde komisyon kazanmaya başlayın." | Faydaları tekrar edin ve sürtünmeyi kaldırın |

CTA bölümü, metnin altına **Ortak Ol** butonunu otomatik olarak görüntüler.

## Kayıt Ayarları

Yeni ortakların nasıl kayıt olacağını ve hangi bilgileri sağlayacağını kontrol edin.

### Özelleştirilmiş Kayıt Formu

**Alan:** `custom_form` (FormBuilder formuna ForeignKey)

Spwig Form Builder ile oluşturduğunuz özel bir kayıt formu varsa, burada seçin. Bu, kayıt sırasında ek bilgileri toplamak için izin verir (örneğin, web sitesi URL'si, hedef kitlesi boyutu, pazarlama kanalları).

**Boş bırakın** varsayılan affiliate kayıt formunu kullanın (e-posta, şifre, ödeme ayrıntıları).

### Misafir Kaydı İzin Ver

**Alan:** `allow_guest_registration` (Boole)

- **Onaylı** — Ziyaretçiler, Spwig hesabı oluşturmadan önce başvurabilir
- **Onaysız** — Ziyaretçiler, başvurmadan önce giriş yapmalı veya müşteri hesabı oluşturmalı

**Öneri:** Misafir kaydı etkinleştirin, sürtünmeyi azaltın. Her zaman onay isteyebilirsiniz, başvuruları etkinleştirmeden önce doğrulayın.

### Onay Gerekiyor

**Alan:** `require_approval` (Boole)

- **Onaylı** — Yeni ortaklar, dashboard'larına erişmeden önce manuel onay beklemelidir
- **Onaysız** — Yeni ortaklar, anında bağlantı oluşturabilir

**Öneri:** Affiliate'leri marka uyumu, dolandırıcılık önleme veya özel programlar için doğrulamak istiyorsanız, manuel onayı etkinleştirin.

### Şartlar & Koşullar URL'si

**Alan:** `terms_url` (URL)

Affiliate programınızın şart ve koşullarına bağlantı. Eğer sağlanırsa, kayıt formu, ortakların kayıt olmadan önce şartlarını onaylamaları için bir onay kutusu görüntüler.

**Örnek:** `/pages/affiliate-terms/`

### Hoş geldiniz Mesajı

**Alan:** `welcome_message` (Metin)

Başarıyla kayıt olduktan sonra ortaklara gösterilen mesaj. Aşağıdakiler için kullanın:

- Onları katılmaları için teşekkür edin
- Sonraki adımları açıklayın (örneğin, "Başvurunuz 24 saat içinde incelenecektir")
- Başlangıç kaynaklarına bağlantı sağlayın

**Örnek:*
```
Affiliate programımıza hoş geldiniz! Başvurunuzu aldık ve 24 saat içinde incelenecektir. Onaylama doğrulaması ve giriş talimatları için e-postanızı kontrol edin.
```

## Çok Dilli Desteğe Sahip Olma

Affiliate Ayarları'daki tüm metin alanları, Spwig'ın çeviri widget'ı ile **çevrilebilir**:

- Anasayfa Başlığı
- Anasayfa Alt Başlığı
- Özellikler (dil başına JSON çeviri)
- Nasıl Çalışır adımları (dil başına JSON çeviri)
- CTA Başlığı
- CTA Açıklaması
- Hoş geldiniz Mesajı

### Çeviri Nasıl Çalışır

Bir çevrilebilir alanı düzenlerken, her etkin dille ilgili içerik sağlamanıza olanak tanıyan bir çeviri widget'ı görürsünüz. JSON alanları (özellikler, adımlar) için, dil başına ayrı JSON nesneleri sağlarsınız:

**İngilizce:*
```json
[
  {"icon": "fa-dollar-sign", "title": "Competitive Commissions", "description": "Earn up to 15% on every sale"}
]
```

**İspanyolca:*
```json
[
  {"icon": "fa-dollar-sign", "title": "Comisiones Competitivas", "description": "Gana hasta el 15% en cada venta"}
]
```

Portal, ziyaretçinin dil tercihine göre doğru dil sürümünü otomatik olarak görüntüler.

## Değişiklikleri Önizleme

Portal ayarlarını özelleştirdikten sonra:

1. **Admin'de** değişikliklerinizi kaydedin
2. Mağazanızın frontendinde `/affiliate/` yoluna gidin (yeni bir sekmede açın)
3. **Kayıt akışını test edin** — "Ortak Ol" butonuna tıklayarak
4. **Marka uyumunu kontrol edin** — portal, mağazanızın tasarımı ve mesajlaşma ile uyumlu mu?

İteratif değişiklikler yapabilir ve sayfayı yenileyerek güncellemeleri hemen görebilirsiniz.

## Örnek Özelleştirmeler

### Senaryo 1: E-Ticaret Moda Mağazası

**Hedef:** Moda etkiliyici ve blog yazarlarını çekmek

| Ayar | Değer |
|------|-------|
| Anasayfa Başlığı | "Sevdiklerinizin Modasını Tanıtın & Kazanın" |
| Anasayfa Alt Başlığı | "1.200'den fazla etkiliyici, her satış için %12 komisyon kazanıyor" |
| Özellik 1 | Simge: `fa-tshirt`, Başlık: "Moda Koleksiyonları", Açıklama: "Premium giyim ve aksesuarları tanıtın" |
| Özellik 2 | Simge: `fa-percentage`, Başlık: "%12 Komisyon", Açıklama: "Tüm ürünlerde endüstri lideri oranlar" |
| Özellik 3 | Simge: `fa-camera`, Başlık: "Özel İçerik", Açıklama: "Ürün fotoğrafları, videoları ve kampanya malzemelerine erişin" |
| Misafir Kaydı İzin Ver | Onaylı |
| Onay Gerekiyor | Onaylı (marka uyumu için manuel inceleme) |

### Senaryo 2: B2B SaaS Ortak Programı

**Hedef:** Kurumsal yazılım referansları için iş danışmanlarını ve ajansları çekmek

| Ayar | Değer |
|------|-------|
| Anasayfa Başlığı | "Bize Ortak Olun ve Gelirinizi Artırın" |
| Anasayfa Alt Başlığı | "B2B ortak programımız aracılığıyla her kurumsal referans için 500 dolar kazanın" |
| Özellik 1 | Simge: `fa-handshake`, Başlık: "Her Referans İçin 500 Dolar", Açıklama: "Kalifiye kurumsal potansiyeller için sabit komisyon" |
| Özellik 2 | Simge: `fa-clock`, Başlık: "180 Günden Uzun Ödeme", Açıklama: "Karma satış döngüleri için uzun ödüllendirme penceresi" |
| Özellik 3 | Simge: `fa-user-tie`, Başlık: "Özel Ortak Yöneticisi", Açıklama: "Müşterileriniz için özel destek" |
| Misafir Kaydı İzin Ver | Onaysız (B2B hesabı gerekir) |
| Onay Gerekiyor | Onaylı (davet etme programı) |
| Şartlar URL'si | `/pages/partner-program-terms/` |

## İpuçları

- **Anasayfa başlığını** faydalar üzerine odaklanarak özelleştirin, değil de özellikler — "Uyku Halinde Kazan" daha etkileyicidir "Affiliate Programı Kayıt"dan
- **Sosyal kanıt** alt başlıkta kullanın (örneğin, "500'den fazla ortak katıldı") güven ve inanç kurmak için
- Her fayda için **FontAwesome simgeleri** seçin — simge, değeri anında iletmelidir
- Özellik açıklamalarını **1-2 cümle** olarak tutun — portal, dönüşüm için değil, kapsamlı açıklama için değil
- Portalı tanıtma öncesi **kayıt akışını kendiniz test edin** — karışık form alanları veya kırık bağlantılar gibi sürtünme noktalarını yakalayın
- **Misafir kaydını** etkinleştirmek için kayıt sürtünmesini azaltın, ardından **onay gerekir** kullanarak başvuruları gönderdikten sonra ortakları doğrulayın
- **Hoş geldiniz mesajını** kullanarak beklenti (onay zaman çizelgesi, sonraki adımlar, destek iletişim) ayarlayın ve destek sorgularını azaltın
- Portalı **sezonluk olarak güncelleyin** — kampanyalarla uyumlu hale getirin, özel komisyon tekliflerini veya ürün tanıtımını vurgulayın

