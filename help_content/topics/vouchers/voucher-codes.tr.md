---
title: Kupon Kodları
---

Kupon Kodları, müşterilerin ödeme sırasında indirim alabilmeleri için kullanabilecekleri indirim kodları, kuponlar ve hediye kartları oluşturmanıza olanak tanır. Yönetici menüsünden **Pazarlama > Kuponlar** bölümüne gidin.

![Kupon listesi](/static/core/admin/img/help/voucher-codes/voucher-list.webp)

## Kupon Paneli

Kupon sayfası, aşağıdaki genel bakış bilgilerini gösterir:

- **İstatistik Kartları** — Aktif, Pasif, Kullanım Sayısı ve Toplam kupon sayıları
- **Filtreler** — Kod veya isimle arama yapın, Tip, Durum ve Kapsam ile filtreleyin
- **Kupon Kartları** — Her kupon, kullanım ve durum detaylarıyla birlikte gösterilir

## Kupon Oluşturma

1. Üst sağ köşedeki **+ Kupon Ekle** butonuna tıklayın
2. Kupon detaylarını doldurun:
   - **Kod** — Müşterilerin ödeme sırasında gireceği kod (örneğin, "SAVE20", "FREESHIP")
   - **Adı/Açıklaması** — Kendi referansınız için iç açıklama
   - **İndirim Türü** — İndirimin nasıl uygulanacağı
   - **İndirim Değeri** — İndirim miktarı veya yüzdesi
3. Kullanım kurallarını yapılandırın:
   - **Kullanım Sınırlaması** — Toplam kullanım sayısı (0 = sınırsız)
   - **Müşteri Başına Sınırlama** — Her müşteri için maksimum kullanım sayısı
   - **Minimum Sipariş Değeri** — Gerekli minimum sepet toplamı
4. **Kapsam** ayarlayın:
   - **Tüm Sepet** — İndirim tüm siparişe uygulanır
   - **Belirli Ürünler** — Sadece seçilen ürünlere uygulanır
   - **Belirli Kategoriler** — Sadece seçilen kategorilere uygulanır
5. Opsiyonel olarak son kullanma tarihi ayarlayın:
   - **Son Kullanma Tarihi** — Kuponun artık işe yaramayacağı tarih
6. **Kaydet** butonuna tıklayın

## Kupon Türleri

| Tür | Açıklama | Örnek |
|------|-------------|---------|
| **Sabit Tutar** | Belirli bir dolar tutarını düşer | Siparişin 20$ indirilir |
| **Yüzde** | Toplamın bir yüzdesini düşer | Siparişin 15% indirilir |
| **Ücretsiz Kargo** | Kargo ücretlerini kaldırır | Herhangi bir siparişte ücretsiz kargo |

## Kuponları Yönetme

### Kupon Kartları

Her kupon kartı aşağıdaki bilgileri gösterir:
- **Kod** — Kupon kodu kalın yazıyla gösterilir
- **Açıklama** — Kuponun ne yaptığını gösterir
- **Durum Etiketi** — Aktif veya Pasif
- **İndirim Detayları** — Tür ve değer (örneğin, "$ 20.00" veya "15.00%")
- **Kapsam** — Tüm sepete mi yoksa belirli ürünlere mi uygulanır
- **Kullanım Sayısı** — Kuponun kaç kez kullanıldığını gösterir
- **Oluşturulma Tarihi** — Kuponun ne zaman oluşturulduğunu gösterir
- **Son Kullanma Tarihi** — Son kullanma tarihi veya "Son kullanma yok" yazısı

### Kupon İşlemleri

Her kartta aşağıdaki işlem butonları vardır:
- **Düzenle** — Kupon ayarlarını değiştirin
- **Tarihçeyi Görüntüle** — Kullanım tarihçesini görün
- **Sil** — Kuponu kaldırın

### Kuponları Filtreleme

Filtre çubuğunu kullanarak belirli kuponları bulun:
- **Arama** — Kod, isim veya açıklamaya göre arama yapın
- **Tip** — Sabit Tutar, Yüzde veya Ücretsiz Kargo
- **Durum** — Aktif veya Pasif
- **Kapsam** — Tüm Sepet veya ürün özelinde

## Toplu Kupon Oluşturma

Büyük kampanyalar için toplu kupon oluşturabilirsiniz:
1. Sistem, benzersiz kodları otomatik olarak oluşturur (örneğin, "COUPONX1600406498")
2. Oluşturulan tüm kuponlar için ortak parametreleri ayarlayın
3. Kodları e-posta, sosyal medya veya basılı malzemelerle dağıtın

## Müşteri Deneyimi

Bir müşteri kupon koduna sahipse:
1. **Ödeme** kısmına gider
2. Kodu **indirim kodu** alanına girer
3. Kupon geçerliyse indirim hemen uygulanır
4. Sipariş özeti, indirimi göstermek üzere güncellenir

Eğer kupon geçersizse (son kullanma tarihi geçmiş, kullanım sınırı aşıldı, minimum değer karşılanmadı), müşteriye açık bir hata mesajı gösterilir.

## İpuçları

- Pazarlama kampanyaları için kolayca hatırlanabilecek kodlar kullanın (örneğin, "SUMMER20" gibi rastgele dizgeler yerine).
- Değerli indirimlerin kötüye kullanılmasını önlemek için müşteri başına kullanım sınırlaması ayarlayın.
- Kârlılığı korumak için minimum sipariş değerleri kullanın (örneğin, "50$ üzerindeki siparişlerde 10$ indirim").
- Paneldeki Kullanım Sayısı'na bakarak kampanya etkinliğini izleyin.
- Aciliyet yaratmak için zaman sınırlı kuponlar oluşturun (örneğin, "Sadece bu hafta sonu geçerlidir").
- Kuponları silmeden durdurmak için Aktif/Pasif durumunu kullanın.
