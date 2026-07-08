---
title: Rezervasyon Yapılabilecek Ürünler
---

Rezervasyon yapabilecek ürünler, müşterilerin satın alma sırasında belirli bir tarih ve saat seçmelerine olanak tanır. Bu, randevular, kiralama, sınıflar, etkinlikler ve konaklama rezervasyonlarını destekler — tümü Spwig admin panelinizden doğrudan yönetilir.

## Rezervasyon Türleri

| Tür | En Uygun Olduğu Alan |
|------|----------|
| **Randevu** | Hizmetler: danışmanlık, saç kesimi, bireysel antrenman |
| **Kiralama** | Ekipman kiralama, araç kiralama, oda kiralama |
| **Sınıf / Atölye** | Belirli bir kapasite ile grup oturumları |
| **Konaklama** | Belirli giriş/çıkış saatleri olan çok gece konaklamalar |
| **Etkinlik** | Biletli tek seferlik veya tekrar eden etkinlikler |

## Rezervasyon Yapılabilecek Ürün Oluşturma

### Adım 1: Ürün Oluştur

1. **Ürünler > Tüm Ürünler** menüsüne gidin ve **+ Ürün Ekle**'ye tıklayın
2. **Ürün Türü** alanını **Rezervasyon Ürünü** olarak ayarlayın
3. Standart ürün alanlarını doldurun (ad, açıklama, fiyat)
4. Ürünü kaydedin

### Adım 2: Rezervasyon Ayarlarını Yapılandırın

Kaydetme işleminden sonra, ürün düzenleme formunda **Rezervasyon Yapılandırması** bölümü görünür. Rezervasyon ayarlarını doldurun:

#### Rezervasyon Türü ve Süresi

- **Rezervasyon Türü** — Hizmetinize en uygun türü seçin (Randevu, Kiralama, Sınıf vb.)
- **Süre Türü** — Otomatik olarak eklenen rezervasyonlar arasında hazırlık veya temizlik için zaman ayırmak için **Sabit Süre**'yi seçin veya müşterilerin ihtiyaç duydukları süreyi seçmelerine izin vermek için **Müşteri Süre Seçimi**'ni seçin
- **Süre** ve **Süre Birimi** — Sürenin uzunluğunu belirtin (örneğin, `60` dakika, `1` saat, `2` gün)
- **Min/Max Süre** — Müşterilerin süre seçimi yapabiliyorsa, izin verilen aralığı ayarlayın

#### Hazırlık Zamanı

Hazırlık zamanı, rezervasyonlar arasında otomatik olarak eklenir ve hazırlık veya temizlik için zaman ayırır:
- **Rezervasyon Öncesi** — Rezervasyon başlamadan önce ayrılan dakika sayısı
- **Rezervasyon Sonrası** — Rezervasyon bittikten sonra ayrılan dakika sayısı

Örneğin, 60 dakikalık bir masaj randevusunda rezervasyon sonrası 15 dakikalık bir hazırlık süresi, bir sonraki müşteri için 15 dakika ayırır.

#### Rezervasyon Penceresi

- **Minumum Rezervasyon Bildirimi** — Müşterilerin rezervasyon yapması gereken en erken zaman (örneğin, `24 saat` aynı gün rezervasyonları yasaklar)
- **Maksimum Rezervasyon Penceresi** — Müşterilerin ne kadar ileriye rezervasyon yapabileceğini belirtir (örneğin, `365 gün`)

#### Kapasite

- **Bir Oturumda Maksimum Rezervasyon Sayısı** — Sınıflar ve etkinlikler için aynı zaman diliminde rezervasyon yapabilecek müşteri sayısını belirtin. Özel randevular için `1` olarak ayarlayın.

#### Onaylama

- **El ile Onay Gerekiyor** — İşaretlendiğinde rezervasyonlar otomatik olarak onaylanmaz. Her rezervasyonu rezervasyon listesinden el ile onaylamalısınız. Müşterileri onaylamadan önce incelemek istiyorsanız yararlıdır.

#### İptal Politikası

- **İptal İznini Ver** — Müşterilerin rezervasyonlarını iptal edebilir mi?
- **İptal Süresi** — Müşterilerin rezervasyonlarını iptal edebilecekleri saat/gün sayısı (örneğin, `24 saat`)

#### Takvim Gösterimi

Müşterilerin ürün sayfasında tarih ve saat seçimi nasıl yapılır:

| Gösterim Modu | En Uygun Olduğu Alan |
|-------------|----------|
| **Takvim Görünümü** | Genel kullanım — tam aylık takvim |
| **Tarih Seçici** | Basit tek tarih seçimi |
| **Mevcut Tarihler Düşüncesi** | Sınırlı mevcut tarihleri olan ürünler |
| **Tarih Aralığı Seçici** | Konaklama ve çok günlük kiralama |

#### Güvenlik Fonu

Ödeme sırasında tam ödemeye göre bir güvenlik fonu istemek için:
1. **Güvenlik Fonu Etkin** kutusunu işaretleyin
2. **Güvenlik Fonu Türü** alanını **Sabit Tutar** veya **Toplamın Yüzdesi** olarak ayarlayın
3. **Güvenlik Fonu Tutarı** alanına girin (örneğin, `50` için $50, `25` için 25%)

#### Konaklama Özel Ayarları

Konaklama rezervasyonları için ek alanlar görünür:
- **Giriş Saati** ve **Çıkış Saati** — Emlak için standart saatler
- **Standart Kapasite** — Temel ücrette dahil olan varsayılan misafir sayısı

### Adım 3: Rezervasyon Kaynaklarını Ekle (Opsiyonel)

Kaynaklar, bir rezervasyona atanan fiziksel eşyalar veya personel üyeleridir — örneğin, "Oda 1", "A Sahası" veya "Antrenör Sam".

1. Ürün düzenleme formunda **Rezervasyon Kaynakları** bölümüne gidin
2. **Kaynak Ekle**'ye tıklayın
3. Kaynak için bir **Ad** verin ve **Kapasite**'yi ayarlayın (kaynakın aynı anda kaç rezervasyon işleyebileceğini belirtin)
4. Opsiyonel olarak kaynak resimleri ekleyin


Kaynaklar, rezervasyonların sadece zaman dilimine göre değil, bireysel varlıklar veya personel üyelerine göre de kullanılabilirliğini izlemenizi sağlar.

### Adım 4: Kullanılabilirlik kurallarını ayarla

Kullanılabilirlik kuralları, rezervasyonların ne zaman yapılabileceğini tanımlar:

1. Ürünün **Kullanılabilirlik** bölümü altında, **Kullanılabilirlik Kuralı Ekle**'ye tıklayın
2. Bu kuralın uygulandığı **Kaynak**'ı seçin
3. Kullanılabilir olduğu **Haftanın Günleri**'ni belirleyin
4. Kullanılabilirlik penceresi için **Başlangıç Zamanı** ve **Bitiş Zamanı**'nı ayarlayın
5. Mevsimsel kullanılabilirlik için isteğe bağlı olarak bir tarih aralığı (**Geçerli Olmaya Başlama** / **Geçerlilik Bitiş Tarihi**) belirleyin
6. Kaydedin

## Rezervasyonları görüntüleme ve yönetme

### Rezervasyon listesi

**Katalog > Rezervasyonlar** menüsüne giderek tüm rezervasyonları görüntüleyebilirsiniz. Aşağıdakilerle filtreleyebilirsiniz:
- Durum (Onay Bekleyen, Onaylı, İptal Edilen, Tamamlanan, Gelmedi)
- Ürün
- Tarih aralığı

### Rezervasyon durumları

| Durum | Anlamı |
|--------|---------|
| **Onay Bekleyen** | Manuel onay bekliyor (eğer onay gerekliyse) |
| **Onaylı** | Rezervasyon onaylanmış ve aktif |
| **İptal Edilen** | Rezervasyon müşteri veya siz tarafından iptal edildi |
| **Tamamlanan** | Rezervasyon tarihi geçmiş ve tamamlanmış |
| **Gelmedi** | Müşteri gelmedi |

### Onay bekleyen bir rezervasyonu onaylama

1. **Katalog > Rezervasyonlar** üzerinden rezervasyonu açın
2. **Durum**'u **Onaylı** olarak değiştirin
3. Kaydedin — müşteriye otomatik olarak onay e-postası gönderilir

### Rezervasyonu iptal etme

1. Rezervasyonu açın
2. **Durum**'u **İptal Edilen** olarak değiştirin
3. **İptal Nedeni** girin (müşteri e-postasında gösterilir)
4. Kaydedin

## Bekleme listesini yönetme

Bir zaman dilimi tamamen dolu olduğunda müşteriler kendilerini bekleme listesine ekleyebilir. Spwig, iptal bir boşluk yarattığında bekleme listesindeki müşterilere otomatik olarak bildirim gönderir.

### Bekleme listesini görüntüleme

**Katalog > Rezervasyon Bekleme Listesi** menüsüne giderek tüm bekleme listesi girdilerini görüntüleyebilirsiniz. Her girdi şu bilgileri gösterir:
- Müşteri adı ve e-postası
- Ürün ve istenen tarih
- Durum: **Bekleme**, **Bildirildi**, **Rezervasyona Dönüştürüldü** veya **Süresi Dolmuş**

### Bekleme listesi durumları

| Durum | Anlamı |
|--------|---------|
| **Bekleme** | Müşteri kuyruğa girildi, zaman dilimi henüz mevcut değil |
| **Bildirildi** | Müşteriye mevcut bir zaman dilimi hakkında e-posta gönderildi |
| **Rezervasyona Dönüştürüldü** | Müşteri zaman dilimini aldı ve bir rezervasyon tamamladı |
| **Süresi Dolmuş** | İstenen tarih geçmiş ve bir zaman dilimi mevcut olmadan geçti |

### Bekleme listesindeki bir müşteriyi manuel olarak bildirme

Otomatik bildirimden önce belirli bir bekleme listesindeki müşteriyi doğrudan iletişim kurmak isterseniz:
1. Bekleme listesi girdisini açın
2. E-posta adresini kopyalayın ve doğrudan onlarla iletişime geçin
3. Onlar bir rezervasyon tamamladığında, bekleme listesi girdi durumu **Rezervasyona Dönüştürüldü** olarak güncellenir

## İpuçları

- Yüksek değerli rezervasyonlar için (örneğin, fotoğraf oturumları, özel etkinlikler) manuel onayı etkinleştirin — böylece rezervasyon yapmadan önce kullanılabilirliği kontrol edebilir ve gereksinimleri eşleştirebilirsiniz.
- Başlangıçta buffer zamanını genel olarak ayarlayın — gerçek dünya dönüş süresi ihtiyaçlarını anladığınızda her zaman azaltabilirsiniz.
- Grup sınıfları için **Slot Başına Maksimum Rezervasyon Sayısı**'nı sınıf kapasitesine ayarlayın ve bekleme listesini etkinleştirin — popüler oturumlar otomatik olarak bir kuyruk oluşturur.
- Konaklama ürünleri için tarih aralığı seçici görüntüleme modunu kullanın — müşteriler genellikle giriş ve çıkış tarihlerini birlikte seçmek ister.
- Hazırlık süresi gerekiyorsa (örneğin, özel yemek siparişleri için 48 saatlik minimum), minimum önceden haber verme süresi ayarlayarak son dakika rezervasyonlarını önleyin.
- Mevsimsel yoğunluk dönemlerinde bekleme listesini düzenli olarak gözden geçirin — bekleme listesindeki müşterilere manuel olarak ulaşmak, otomatik bildirimden daha hızlı iptalleri doldurabilir.