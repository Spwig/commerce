---
title: Personel Roller ve İzinler
---

Personel rolleri, her bir ekibin üyesinin yönetici paneli ve POS terminalinde ne görebileceğini ve ne yapabileceğini tam olarak kontrol etmenizi sağlar. Belirli izinlerle roller tanımlayın ve ardından bunları personel üyelerine atayın. Bir kullanıcı birden fazla rol taşıyabilir ve etkili izinleri atanan tüm rollerin birleşimidir.

![Personel rolleri](/static/core/admin/img/help/staff-roles/role-list.webp)

## Nasıl Çalışır

1. **Roller** oluşturun, bu roller bir izin setini tanımlar (örneğin, "Sipariş Yöneticisi", "Kasayıcı")
2. Her rol, iki tür erişim kontrol eder: **yönetici paneli izinleri** ve **POS izinleri**
3. **Rolleri atayın** personel üyelerine profilleri sayfasından
4. Bir personelin etkili izinleri, tüm atanan rollerin **birleşimi**dir — eğer herhangi bir rol erişim sağlıyorsa, kullanıcı bunu kullanabilir
5. İzinler **önbelleğe alınır** performans için ve roller değiştiğinde otomatik olarak yenilenir

## Önceden Tanımlanmış Roller

Spwig, en yaygın ekip yapılarını kapsayan 7 yerleşik rol içerir. Bu roller silinemez, ancak daha spesifik ihtiyaçlar için özel roller oluşturabilirsiniz.

| Rol | Erişim | Açıklama |
|------|--------|-------------|
| **Mağaza Sahibi** | Yönetici + POS | Her şeyin tam erişimi. Ana mağaza yöneticisi için |
| **Mağaza Yöneticisi** | Yönetici + POS | Günlük operasyonlar — ürünleri, siparişleri, müşterileri, pazarlamayı ve aramayı tam erişim. Tasarım, e-posta, ödemeler ve ayarlar için sadece görüntüleme |
| **İçerik Düzenleyici** | Yönetici | Sayfaları, blog gönderilerini, tasarımı ve medyayı yönetir. Ürünler için sadece görüntüleme |
| **Sipariş Yöneticisi** | Yönetici | Siparişleri, sevkiyatı, iade ve müşteri hizmetlerini yönetir. Ürünler için sadece görüntüleme |
| **Pazarlama Yöneticisi** | Yönetici | Promosyonları, kuponları, ortaklık, sadakat ve referans programlarını yönetir. Ürünler, müşteriler ve medya için sadece görüntüleme |
| **Kasayıcı** | POS sadece | Ön uç POS personeli. Satışları işlemek ve hediye kartı bakiyelerini kontrol etmek için |
| **Deneyimli Kasayıcı** | POS sadece | Deneyimli POS personeli. İade işlemleri, indirimler (en fazla 25%), nakit yönetimi ve shift kapatma yapabilir |

## Özel Rol Oluşturma

**Ayarlar > Personel Roller** sayfasına gidin ve **Rol Ekle**'ye tıklayın.

### Genel Ayarlar

| Ayar | Açıklama |
|---------|-------------|
| **Gösterim Adı** | Yönetici panelinde gösterilen rol adı (örneğin, "Depo Personeli") |
| **Açıklama** | Bu rolün ne için kullanıldığını açıklayan kısa bir açıklama |
| **Sıralama** | Rol listesindeki gösterim sırasını kontrol eder |
| **Simge** | Rolün görsel olarak tanımlanması için 20 simgeden birini seçin |
| **Simge Rengi** | Rol simgeleri için kullanılan renk (Mavi, Yeşil, Turuncu, Kırmızı, Çıtır, Gri) |
| **Yönetici Paneli** | Bu rolün yönetici arka uç erişimini verip vermediğini ayarlar |
| **POS Terminali** | Bu rolün POS terminali erişimini verip vermediğini ayarlar |

### Yönetici İzin Kategorileri

Yönetici izinler sekmesi, tüm platform özelliklerini 13 kategoriye ayırır. Her kategori için, üç erişim düzeyinden birini ayarlayabilirsiniz:

- **Hiçbiri** — Bu alana erişim yok (menü öğeleri gizlenir)
- **Görüntüleme** — Sadece okunabilir erişim (verileri görebilir ama değiştiremez)
- **Tam** — Tam erişim (görebilir, oluşturabilir, düzenleyebilir ve silebilir)

![İzin kategorileri](/static/core/admin/img/help/staff-roles/permission-categories.webp)

| Kategori | Ne Kontrol Ediyor |
|----------|-----------------|
| **Ürün Kataloğu** | Ürünler, kategoriler, markalar, öznitelikler, stok, depolar, dijital varlıklar |
| **Siparişler & Teslimat** | Siparişler, iadeler, iade işlemleri, sevkiyatlar, taşıma yapılandırması |
| **Müşteriler** | Müşteri profilleri, segmentler, analiz |
| **İçerik & Sayfalar** | Sayfalar, blog gönderileri, duyurular, formlar |
| **Tasarım & Tema** | Temalar, üst bilgi/alt bilgi şablonları, menüler, tasarım token'ları, özel CSS |
| **Pazarlama & Promosyonlar** | Promosyonlar, kuponlar, ortaklık, sadakat, referanslar, ürün beslemeleri |
| **Medya Kütüphanesi** | Görseller, videolar, klasörler, etiketler |
| **E-posta Sistemi** | E-posta hesapları, şablonlar, teslimat kuyruğu |
| **Ödeme & Faturalandırma** | Ödeme sağlayıcıları, işlemler, webhooks, abonelikler, döviz kurları |
| **Arama** | Arama ayarları, eşanlamlılar, yönlendirmeler, analiz |
| **Mağaza Ayarları** | Site ayarları, coğrafi konum, ülke eşlemeleri, iş kuralları |
| **POS Yönetimi** | POS terminalleri, shift'ler, nakit hareketleri, fatura şablonları |
| **Kullanıcılar & Roller** | Personel kullanıcı hesapları, roller, API token'ları |

Bir kullanıcı birden fazla rol sahibi olduğunda, **en yüksek** erişim düzeyi geçerlidir. Örneğin, Rol A ürünleri için "Görüntüle" ve Rol B ürünleri için "Tam" izin veriyorsa, kullanıcı "Tam" erişim sağlar.

### POS İzin Bayrakları

Rol POS erişimi veriyorsa, POS İzinleri sekmesi, POS operatörünün ne yapabileceğini tam olarak ayarlamanıza olanak tanır. Bu, yönetici izinlerinden ayrıdır ve POS terminalinde kontrol edilir.

![POS izinleri](/static/core/admin/img/help/staff-roles/pos-permissions.webp)

| Grup | İzin | Açıklama |
|-------|-----------|-------------|
| **Genel** | POS Erişimi | POS sisteminde kullanılabiliyor |
| **Satışlar & İndirimler** | Manuel İndirimler | Satır öğesi veya sepet seviyesindeki manuel indirimleri uygulayabilir |
| | Maksimum İndirim % | İzin verilen en yüksek indirim yüzdesi (0–100) |
| | Fiyat Değiştirme | Kayıtta ürün fiyatlarını geçersiz kılabilir |
| **İadeler & İptaller** | İade İşlemleri | POS siparişlerinde iade işlemleri yapabilir |
| | Sipariş İptali | Mevcut shift'ten POS siparişlerini iptal edebilir |
| **Hediye Kartları** | Hediye Kartı Ver | Kayıtta yeni hediye kartları verebilir |
| | Hediye Kartı Bakiyesi Kontrolü | Hediye kartı bakiyelerini kontrol edebilir |
| **Nakit Yönetimi** | Nakit Yönetimi | Nakit giriş ve çıkış işlemleri yapabilir |
| | Nakit Çantayı Aç | Satış olmadan nakit çantayı açabilir |
| | Shift Kapat | Shift'leri kapatıp nakit dengeleme yapabilir |
| **Raporlama** | POS Raporlarını Görüntüle | Shift raporlarını ve satış özetlerini görüntüleyebilir |
| **Stok** | Stok Ayarlamaları | Stok seviyelerini ayarlayabilir (alınan, hasarlı, yeniden sayım, iade) |

Boole tipi izinler için, kullanıcıların herhangi bir rolü bu izini etkinleştirmişse, kullanıcı bu izini kullanabilir. Maksimum İndirim % için, tüm rollerdeki **en yüksek** değer geçerlidir.

## Personel Üyelerini Yönetme

**Ayarlar > Personel Yönetimi** sayfasına gidin ve ekibinizi görüntüleyin ve yönetin.

### Personel Listesi

Personel listesi, personel erişimi olan tüm kullanıcıları gösterir. Her üyenin için:
- **Ad ve e-posta**
- **Atanmış roller** (renkli simgeler olarak gösterilir)
- **Erişim türü** — Sadece Yönetici, Sadece POS veya Her ikisi de
- **2FA durumu** — İki faktörlü kimlik doğrulama etkin mi
- **Aktif/Devre Dışı** durumu

Filtreleri kullanarak rol, erişim türü veya 2FA durumuna göre daraltabilirsiniz.

### Personel Üyelerine Roller Atama

1. Bir personel üyesine tıklayarak profilini açın
2. **Roller** bölümünde, her mevcut rol için kartlar görünecektir
3. Herhangi bir rol kartındaki anahtarlayıcıyı tıklayarak rolü atayın veya kaldırın
4. Değişiklikler hemen etkili olur — kaydetme butonuna gerek yoktur
5. Aşağıdaki **Etkili İzinler** özeti, tüm atanan rollerin birleşimini gösterir

### Yeni Personel Üye Ekleme

1. **Ayarlar > Personel Yönetimi** sayfasına gidin ve **Personel Üye Ekle**'ye tıklayın
2. Kullanıcının e-postasını, adını ve soyadını girin
3. Geçici bir şifre ayarlayın
4. Bir veya daha fazla rol atayın
5. Kullanıcı, rollerinin verdiği erişimle giriş yapabilir

## Rollerı Kopyalama

Mevcut bir rol temelinde yeni bir rol oluşturmak için:

1. Kopyalamak istediğiniz rolü açın
2. Sayfanın alt kısmında **Rol Kopyala**'ya tıklayın
3. Aynı izinlerle yeni bir rol oluşturulur
4. Yeniden adlandırın ve gerekirse izinleri düzenleyin
5. Yeni rolü kaydedin

Bu, mevcut bir rolle benzer ama küçük farklarla bir rol gerekli olduğunda yararlıdır — örneğin, "Yeni Yönetici" rolü "Mağaza Yöneticisi" rolüne dayanabilir ama daha az iznine sahip olabilir.

## İzinler Nasıl Uygulanır

### Yönetici Paneli

- **Menü görünümü** — Kullanıcının "Hiçbiri" erişimi olan kategorilerde yan panel bölümleri gizlenir
- **Sayfa erişimi** — Kısıtlı bir sayfaya gitmeye çalışmak bir izin hatası gösterir
- **Eylem kısıtlamaları** — "Görüntüle" erişimi ile düzenleme ve silme düğmeleri gizlenir ve kaydetme eylemleri engellenir
- **Superuser atlaması** — Superuser hesapları, rol atamalarından bağımsız olarak her zaman tam erişime sahiptir

### POS Terminali

- **Giriş kapısı** — En az bir rolü "POS Terminali" etkin olan kullanıcılar POS'a giriş yapabilir
- **Özellik anahtarları** — POS düğmeleri ve eylemleri (iade, indirim, iptal vb.) kullanıcıların birleştirilmiş POS izinlerine göre gösterilir veya gizlenir
- **İndirim sınırı** — Maksimum İndirim %, POS operatörünün uygulayabileceği indirim büyüklüğünde sert bir sınır koyar
- **API uygulaması** — Tüm POS izinleri API katmanında sunucu tarafında kontrol edilir, sadece UI'da değil

## İpuçları

- **Önceden tanımlanmış rollerle başlayın** — 7 yerleşik rol, çoğu ekip yapısını kapsar. Daha spesifik erişim kontrolleri gerekmedikçe özel roller oluşturmayın.
- **Kopyalama özelliğini kullanın** — Mevcut bir rolle benzer bir rol gerekliyse, onu kopyalayın ve düzenleyin, sıfırdan inşa etmek yerine.
- **Gerekirse birden fazla rol atayın** — Hem siparişleri hem de pazarlamayı yöneten bir personel hem "Sipariş Yöneticisi" hem de "Pazarlama Yöneticisi" rolleri atayılabilir. İzinler otomatik olarak birleşir.
- **Yönetici ve POS erişimini ayırın** — Kasayıcılar genellikle yönetici erişimine ihtiyaç duymaz ve ofis personeli POS erişimine ihtiyaç duymaz. Erişim anahtarlarını kullanarak her şeyi temiz tutun.
- **POS personelleri için indirim sınırları ayarlayın** — Maksimum İndirim %, kasayıcıların aşırı indirimler uygulamasını önler. Hiçbir indirim için 0 olarak ayarlayın veya deneyimli personel için 10–25% gibi akıllıca bir sınır ayarlayın.
- **Rol atamalarını düzenli olarak gözden geçirin** — Ekibiniz büyüdükçe, personelin işlerini yapabilmeleri için gerekli olan minimum erişimi sağladığınızdan emin olun. Pozisyonları değiştiren kişilerden rolleri kaldırın.
- **Önemli roller için 2FA etkinleştirin** — Ödemelere, ayarlara veya kullanıcı yönetimi erişimi olan personel için güvenlik amacıyla iki faktörlü kimlik doğrulamasını etkinleştirin.

