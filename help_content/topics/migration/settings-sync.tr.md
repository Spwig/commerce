---
title: Ayarlar Senkronizasyonu
---

Ayarlar Senkronizasyonu, iki Spwig kurulumu arasında mağaza yapılandırmasını kopyalamanıza olanak tanır. Bu, staging ve üretim ortamlarını korumak için idealdir, çünkü değişiklikleri staging ortamında yapılandırıp ve test edip, daha sonra canlı mağazanıza dağıtmadan önce onları üretim ortamına gönderirsiniz.

## Ne Zaman Ayarlar Senkronizasyonu Kullanılır

- **Staging'den Üretim'e**: Staging mağazanızda ayarları yapılandırın, ardından bunları üretim ortamına gönderin
- **Üretimden Staging'e**: Üretim ayarlarını staging'e çekerek eşleşen bir ortamla başlayın
- **Yedekleme Yapılandırması**: Üretimden yedekleme örneğine ayarları çekerek koruma sağlayın

Ayarlar Senkronizasyonu yalnızca yapılandırma verilerini işler -- ürünleri, müşterileri, siparişleri veya medya dosyalarını aktarmaz. Tam veri aktarımı için Tam Sistem Göçü yerine kullanın.

## Senkronize Edilebilecekler

Ayarlar Senkronizasyonu aşağıdaki kategorileri destekler:

| Grup | Kategoriler |
|-------|-----------|
| **Ayarlar** | Site Ayarları, Vergi & Para Birimi, Vergi Oranları, Diller, Blog Ayarları, Sosyal Paylaşım, Satış Bölgeleri & Depoları, Arama Yapılandırması, Özel Alanlar, Personel Roller, Müşteri Analitiği |
| **Tasarım** | Tasarım & Tema, Başlıklar/Araç Çubukları/Menüler |
| **Sağlayıcılar** | E-posta, SMS/WhatsApp, Ödeme Sağlayıcıları, Nakliye, SEO Sağlayıcıları, Ürün Besleme, Blog Sosyal Bağlantıları, POS Yapılandırması |
| **İçerik** | Sayfalar & Şablonlar, Blog Yazıları, Duyurular, Formlar, Ürün Koleksiyonları |
| **Ticaret** | Ticaret Kuralları (Bono, Kampanyalar, Loyalite, Abonelikler), Ortaklık Programı, Webhook'lar & Entegrasyonlar |

> **Not:** Kimlik bilgileri içeren kategoriler (ödeme sağlayıcıları, nakliye hesapları vb.) bir anahtar simgesiyle işaretlenir. API anahtarları ve gizli ifadeler güvenli bir şekilde aktarılır ancak OAuth tabanlı entegrasyonlar için yeniden girilmesi gerekebilir.

## Adım Adım Kılavuz

### Adım 1: Bağlantıyı Kur

1. Yönetici yan çubuğunda **Veri Göçü > Spwig'den Spwig'e Senkronizasyon** bölümüne gidin
2. **Ayarlar Senkronizasyonunu Başlat**'a tıklayın
3. Kaydedilmiş bir bağlantı seçin veya yeni bir bağlantı oluşturun:
   - Uzak mağazanın URL'sini girin (örneğin, `https://staging.yourstore.com`)
   - Uzak mağazada oluşturulan senkronizasyon token'ını yapıştırın
   - Bağlantıya tanımlayıcı bir isim verin
   - Rolü belirleyin (Staging, Üretim, Yedek veya Diğer)
4. **Bağlantıyı Test Et**'e tıklayarak işe yarayıp yaramadığını doğrulayın
5. **İleri**'ye tıklayarak devam edin

### Adım 2: Kategorileri ve Yönleri Seçin

**Yön:**
- **Çek** -- Bağlantılı mağazadan bu mağazaya ayarları kopyalar
- **Yolla** -- Bu mağazadan bağlantılı mağazaya ayarları kopyalar

**Senkronizasyon Modu:**
- **Ekle & Güncelle** -- Yeni öğeleri ekler ve var olanları günceller, ancak hiçbir şeyi silmez. Bu en güvenli seçenektir.
- **Tam Kopya** -- Hedefi kaynakla tam olarak eşler, hedefte ancak kaynakta olmayan öğeleri kaldırır. Dikkatli kullanın.

Senkronize etmek istediğiniz kategorileri seçin, ardından **İleri**'ye tıklayın.

### Adım 3: Değişiklikleri Önizle

Herhangi bir değişiklik uygulanmadan önce, her kategori için ne ekleneceğini, neyi değiştireceğini ve neyi kaldıracağını gösteren ayrıntılı bir önizleme göreceksiniz. Bu konuda dikkatle inceleyin.

Üretim bağlantısına gönderiyorsanız, değişikliklerin canlı mağazanıza etki edeceğini anladığınızı onaylamalısınız.

Hazır olduğunuzda **Senkronizasyonu Başlat**'a tıklayın.

### Adım 4: İlerlemeyi İzle

Senkronizasyon arka planda çalışır. İlerleme sayfasından güvenli bir şekilde uzaklaşabilirsiniz -- senkronizasyon devam edecektir.

İlerleme sayfası şunları gösterir:
- Genel tamamlanma yüzdesi ile kalan tahmini süre
- Kategori bazlı ilerleme ile başarı / başarısızlık sayıları
- Ayrıntılı çıktı için genişletilebilen canlı etkinlik günlüğü

## Geri Dönüşüm

Senkronizasyon tamamlandıktan sonra, değişiklikleri **24 saat** boyunca geri alabilirsiniz. Geri dönüşüm, tüm etkilenen ayarların önceki durumunu geri yükler.

Geri dönüşüm yapmak için:
1. **Senkronizasyon Panosu**'na gidin
2. Tamamlanmış işi bulun
3. **Geri Dönüşüm**'e tıklayın ve onaylayın

24 saat sonra geri dönüşüm seçeneği sona erer ve değişiklikler kalıcı hale gelir.

## İpuçları

Tüm markdown biçimlendirmesini, resim yollarını, kod bloklarını ve teknik terimleri koruyun.

- **Stajing ortamında önce test edin**:

Ürün ortamına göndermeden önce sonuçları doğrulamak için ilk olarak bir stajing ortamına senkronize edin

- **Add & Update modunu kullanın**:

Mevcut verileri hiçbir zaman silmediği için bu en güvenli moddur

- **Önizlemeyi dikkatle inceleyin**:

Herhangi bir değişiklik uygulanmadan önce ne değişeceğini size gösteren diff önizlemesi vardır

- **Üretim bağlantıları uyardılar gösterir**:

Üretim olarak işaretlenmiş bir bağlantıya gönderdiğinizde, ek güvenlik onayları gerekir