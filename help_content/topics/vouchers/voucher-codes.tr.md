---
title: Kupon Kodları
---

Kupon Kodları, müşterilerin ödeme sırasında indirim alabilmeleri için kullanabilecekleri indirim kodları ve kuponlar oluşturmanıza olanak tanır. Yönetici menüsünden **Pazarlama > Kuponlar** bölümüne gidin.

Mağaza kredisi satmak istiyorsanız? Bu, **Ürünler > Hediye Çeki** altında ayrı olarak yönetilen bir hediye çektir — **Hediye Çekleri** yardım konusuna bakın.

![Kupon listesi](/static/core/admin/img/help/voucher-codes/voucher-list.webp)

## Kupon Paneli

Kupon sayfası, şunları gösteren bir genel bakışa sahiptir:

- **İstatistik Kartları** — Aktif, Pasif, Kullanım Sayısı ve Toplam kupon sayıları
- **Filtreler** — Kod veya isimle arama, Tip, Durum ve Kapsam ile filtreleme
- **Kupon Kartları** — Her kupon, kullanım ve durum detaylarıyla birlikte gösterilir

## Kupon Oluşturma

1. Üst sağ köşedeki **+ Kupon Ekle**'ye tıklayın
2. Kupon detaylarını doldurun:
   - **Kod** — Müşterilerin ödeme sırasında gireceği kod (örneğin, "SAVE20", "FREESHIP")
   - **Adı/Açıklama** — Kendi referansınız için iç açıklama
   - **İndirim Türü** — İndirimin nasıl uygulanacağı
   - **İndirim Değeri** — İndirim miktarı veya yüzdesi
3. Kullanım kurallarını yapılandırın:
   - **Kullanım Sınırlaması** — Toplam kullanım sayısı (0 = sınırsız)
   - **Müşteri Başına Sınırlama** — Müşteri başına maksimum kullanım sayısı
   - **Minimum Sipariş Değeri** — Gerekli minimum sepet toplamı
4. **Kapsam**'ı ayarlayın:
   - **Tüm Sepet** — İndirim tüm siparişe uygulanır
   - **Belirli Ürünler** — Sadece seçilen öğelere uygulanır
   - **Belirli Kategoriler** — Sadece seçilen kategorilere ait öğelere uygulanır
5. Opsiyonel olarak son kullanma tarihini ayarlayın:
   - **Son Kullanma Tarihi** — Kuponun işe yaramaması için tarih
6. **Kaydet**'e tıklayın

## Kupon Türleri

| Tür | Açıklama | Örnek |
|------|-------------|---------|
| **Sabit Tutar** | Sabit dolar tutarı keser | Siparişin $20 indirilir |
| **Yüzde** | Toplamın bir yüzdesi keser | Siparişin 15% indirilir |
| **Ücretsiz Kargo** | Kargo ücretlerini kaldırır | Herhangi bir siparişte ücretsiz kargo |

## Kuponları Yönetme

### Kupon Kartları

Her kupon kartı şu bilgileri gösterir:
- **Kod** — Kupon kodu kalın yazıyla
- **Açıklama** — Kuponun ne yaptığını gösterir
- **Durum Etiketi** — Aktif veya Pasif
- **İndirim Detayları** — Tür ve değer (örneğin, "$ 20.00" veya "15.00%")
- **Kapsam** — Tüm sepete mi yoksa belirli öğelere mi uygulanır
- **Kullanım Sayısı** — Kuponun kaç kez kullanıldığını gösterir
- **Oluşturulma Tarihi** — Kuponun ne zaman oluşturulduğunu gösterir
- **Son Kullanma Tarihi** — Son kullanma tarihi veya "Son kullanma yok"

### Kupon Eylemleri

Her kartta eylem butonları vardır:
- **Düzenle** — Kupon ayarlarını değiştir
- **Tarihçeyi Görüntüle** — Kullanım tarihçesini görüntüle
- **Sil** — Kuponu kaldır

### Kuponları Filtreleme

Filtre çubuğunu kullanarak belirli kuponları bulun:
- **Arama** — Kod, isim veya açıklamaya göre arama yapın
- **Tip** — Sabit Tutar, Yüzde veya Ücretsiz Kargo
- **Durum** — Aktif veya Pasif
- **Kapsam** — Tüm Sepet veya ürün özel

## Toplu Kupon Oluşturma

Büyük kampanyalar için toplu kupon oluşturabilirsiniz:
1. Sistem, benzersiz kodları otomatik olarak oluşturur (örneğin, "COUPONX1600406498")
2. Oluşturulan tüm kuponlar için ortak parametreleri ayarlayın
3. Kodları e-posta, sosyal medya veya basılı materyal yoluyla dağıtın

## Müşteri Deneyimi

Bir müşteri kupon koduna sahipse:
1. Ödeme ekranına gider
2. Kodu **indirim kodu** alanına girer
3. Kupon geçerliyse indirim hemen uygulanır
4. Sipariş özeti, indirimi göstermek için güncellenir

Eğer kupon geçersizse (son kullanma tarihi geçmiş, kullanım sınırı aşılmış, minimum tutar karşılanmamış), müşteriye net bir hata mesajı gösterilir.

## İpuçları

- Pazarlama kampanyaları için kolayca hatırlanabilecek kodlar kullanın (örneğin, "SUMMER20" gibi rastgele dizgeler yerine).
- Değerli indirimlerin kötüye kullanılmasını önlemek için müşteri başına kullanım sınırlaması ayarlayın.
- Kârlılığı korumak için minimum sipariş değerleri kullanın (örneğin, "$50'den fazla siparişlerde $10 indirim").
- Paneldeki Kullanım Sayısı'na bakarak kampanya etkinliğini izleyin.
- Aciliyet yaratmak için zaman sınırlı kuponlar oluşturun (örneğin, "Sadece bu hafta sonu geçerlidir").
- Kuponları silmeden durdurmak için Aktif/Pasif durumunu kullanın.
