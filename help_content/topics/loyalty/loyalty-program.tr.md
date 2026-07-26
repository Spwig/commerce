---
title: Sadakat Programı
---

Sadakat Programı, müşterilere alışverişler ve etkileşimler için bir puan tabanlı sistemle ödüllendirme imkanı tanır. Müşteriler puan kazanır, seviyelerde ilerler ve ödülleri kullanır. Yönetici menüsünden **Pazarlama > Sadakat Programı** bölümüne gidin.

![Sadakat paneli](/static/core/admin/img/help/loyalty-program/loyalty-dashboard.webp)

## Sadakat Paneli

Panel, sadakat programınız hakkında kapsamlı bir genel bakış sağlar:

### Ana Göstergeler

- **Toplam Üyeler** — Kayıtlı toplam müşteriler
- **Aktif Üyeler (30g)** — Geçen 30 günde puan kazanmış veya ödülleri kullanmış üyeler
- **Kalan Puanlar** — Tüm üyelerin kullanılmamış toplam puanları
- **Ödül Oranı** — Kazanılan puanların kullanılmış oranı
- **Kazanılan Puanlar (30g)** — Geçen 30 günde kazanılan puanlar
- **Kullanılan Puanlar (30g)** — Geçen 30 günde kullanılan puanlar
- **Ortalama Puan/Üye** — Üye başına ortalama puan bakiyesi
- **Aktif Kurallar** — Şu anda etkin olan kazanma kuralları sayısı

### Hızlı Eylemler

Panel, programın tüm yönlerini yönetmek için kısayol kartları içerir:
- **Üyeler** — Sadakat üyelerini görüntüleyin ve yönetin
- **Seviyeler** — Üyelik seviyelerini yapılandırın
- **Ödüller** — Ödül kataloğunu ayarlayın
- **Kullanımlar** — Kullanım geçmişini görüntüleyin
- **Kurallar** — Puanların nasıl kazanıldığını yapılandırın
- **Şapkalar** — Başarı şapkalarını yönetin
- **Kampanyalar** — Özel sadakat kampanyaları düzenleyin
- **Segmentler** — Hedefleme için üye segmentleri oluşturun

### Grafikler ve Analizler

- **Üye Kayıt Eğilimi** — Zaman içinde yeni üye kayıtları
- **Kazanılan Puanlar vs. Kullanılan Puanlar** — Puan akışının dengesini izleyin
- **Seviye Dağılımı** — Üyelerin seviyeler arasında nasıl dağıldığını görün

## Programı Kurma

### Adım 1: Seviyeler Oluşturun

Seviyeler, artan faydalarla üyelik düzeylerini tanımlar:

1. **Sadakat > Seviyeler** bölümüne gidin
2. Bronz, Gümüş, Altın, Platin gibi seviyeler oluşturun
3. Her seviye için ayarlayın:
   - **Ad** — Seviye görüntü adı
   - **Rütbe** — Sıralama (düşük rütbe = düşük seviye, örneğin, Bronz = 1, Gümüş = 2)
   - **Renk** — Üye şapkalarında görünen görsel acent renk
   - **Min Puan Kazan** — Bu seviye için gereken toplam puan
   - **Min Harcama** — Bu seviye için gereken toplam harcama tutarı
   - **Min Sipariş** — Bu seviye için gereken sipariş sayısı
   - **Puan Çarpanı** — Bu seviyedeki üyeler için ekstra kazanma oranı (örneğin, 2.0 = 2x puan)

Bir üye, **herhangi** üç eşikten birini karşıladığında bir seviye için eligible hale gelir. Sadece bir eşik kullanabilir veya üçünü birlikte kullanabilirsiniz.

### Adım 2: Kazanma Kurallarını Yapılandırın

Kurallar, müşterilerin puan kazanma şeklini tanımlar:

1. **Sadakat > Kurallar** bölümüne gidin
2. Dört kural türlerinden birini kullanarak kurallar oluşturun:

| Kural Türü | Açıklama | Örnek |
|-----------|-------------|---------|
| **Harcama** | Harcanan miktar başına puan | 1 puan her $1 başına |
| **Ürün** | Satın alınan ürün başına puan | Belirli bir kategorideki her ürün için 50 puan |
| **Eylem** | Belirli bir eylem için puan | Kayıt için 200 puan |
| **Etkinlik** | Takvim etkinliği için puan | Doğum gününde ekstra puan |

3. Ek kural ayarlarını yapılandırın:
   - **Kapsam / Kapsam Filtreleri** — Kuralı belirli ürünler, kategoriler veya müşteri seviyelerine sınırlayın
   - **Min Sipariş Tutarı** — Kuralın uygulanması için gereken minimum sepet değeri
   - **İzin Verilen Seviyeler** — Kuralı belirli üyelik seviyelerine sınırlayın
   - **Özel** — Etkinleştirildiğinde, bu kural diğer kurallarla üst üste gelmez
   - **Puan Bekleme Günü** — Kazanılan puanların kullanıma hazır hale gelmesi için gereken gün sayısı (iade pencerelerini hesaba katmak için faydalıdır)
   - **Puan Süresi Bitiş Günü** — Kazanma sonrası puanların süresi bitmesi için gereken gün sayısı (boş bırakın, süresiz kalsın)
   - **Başlangıç / Bitiş Tarihi** — Kuralı bir tarih aralığına sınırlayın

### Adım 3: Ödülleri Kurulum

Ödüller, müşterilerin puanlarını kullanabileceği şeydir:

1. **Sadakat > Ödüller** bölümüne gidin
2. Aşağıdaki gibi ödüller oluşturun:
   - **$5 İndirim Kuponu** — 500 puan
   - **Ücretsiz Kargo** — 300 puan
   - **10% İndirim** — 1000 puan

> **İndirim Kodu ödülleri şu anda kullanılamıyor.** **Ödül Türü**'si **İndirim Kodu** olarak ayarlanmış bir ödül — yukarıdaki $5 İndirim Kuponu veya 10% İndirim örnekleri gibi — şu anda kullanılamıyor.

Üye, açık bir hata mesajı görür ve puanları otomatik olarak bakiyesine geri döner, bu nedenle hiçbir şey kaybedilmez, ancak ödül şu anda kullanılamaz.

Bu, bilinçli bir düzeltmedir: ödüllendirme önceki versiyonda başarılı olarak bildiriliyordu ancak sessizce puanları keserek hiçbir şey vermiyordu.

Eğer üyeler bir ödüllendirme "çalışmıyorsa" diyorlarsa, bu da budur — yeni bir sorun değil.

İndirim ödülleri, gelecekteki bir sürümde tekrar çalışmaya başlayacak.

Bu, Ücretsiz Kargo, Ücretsiz Ürün veya Deneyim/Avantaj ödüllerini etkilemez.

### Adım 4: Başarılar Oluştur (Opsiyonel)

Başarılar, müşteri başarılarını tanır:

1. **Loyalty > Başarılar**'a gidin
2. Milestone'lar için başarılar oluşturun:
   - **İlk Satın Alma** — İlk siparişten sonra verilir
   - **Büyük Harcama** — 500$+ harcamadan sonra verilir
   - **Sadık Müşteri** — 10 siparişten sonra verilir

Başarılar, kazandıklarında ekstra puan verme içerebilir.

## Üyeleri Yönetme

### Üye Listesi

Tüm sadakat üyeleri ile ilgili bilgileri görüntüleyin:
- Mevcut seviye ve durum
- Puan bakiyesi
- Kayıt tarihi
- Son etkinlik

### En Çok Puan Kazananlar

Görsel paneller, en aktif üyelerinizi gösterir ve bir sıralama tablosu ile gösterir: sıralama, isim, seviye ve dönem içinde kazanılan puanlar.

### Son İşlemler

Bir işlem günlüğü, tüm son puan etkinliklerini gösterir. İşlem türleri şunları içerir:

| Tür | Anlamı |
|------|---------|
| **Kazan** | Kalifiye bir satın alma veya kuraldan puan kredisi |
| **Kullan** | Bir ödülden harcanan puan |
| **Bonus** | Bir başarı, kampanya veya el ile verilen ekstra puan |
| **Düzenleme** | Bir personel tarafından yapılan el ile puan düzeltmesi |
| **İptal** | Sipariş iptalinden sonra kaldırılan puanlar |
| **Süresi Dolmuş** | Süresi geçmiş puanlar |

### El ile Puan Düzenlemeleri

Herhangi bir üyeye el ile puan ekleyebilir veya düşürebilirsiniz:

1. Üyenin detay sayfasını açın
2. **Puan Düzenle**'ye tıklayın
3. Puan miktarını girin (pozitif puan eklemek için, negatif puan düşürmek için)
4. Düzenleme nedenini girin
5. **Kaydet**'e tıklayın

Düzenleme, bir işlem olarak kaydedilir ve üyenin işlem geçmişinde görünür.

## Kampanyalar

Sadakat kampanyaları, özel promosyonlar düzenlemenizi sağlar:
- **Çift Puan Hafta Sonları** — Kazanma oranlarını geçici olarak artırın
- **Ekstra Puan Olayları** — Belirli eylemler için ekstra puan verin
- **Seviye Yükseltme Kampanyaları** — Seviye ilerlemesinin eşiğini düşürün

## İpuçları

- Basit kazanma kuralları ile başlayın (1$ harcanan her 1 puan) ve zamanla genişletin.
- Erkene ulaşılabilir ödül eşiklerini ayarlayarak üyelerin ilgisini koruyun — eğer ödüller ulaşılması zor gibi görünüyorsa, üyeler ilgi kaybeder.
- Başarılar, deneyimi oyunlaştırarak ve belirli davranışları teşvik ederek kullanın.
- Ödülleme Oranını izleyin — sağlıklı bir programda 10-30% arası bir ödüllendirme oranı vardır.
- Düşük dönemlerde kampanyalar düzenleyerek etkileşimi artırın.
- Kazanılan Puanlar vs. Kullanılan Puanlar grafiğini kullanarak programınızın sürdürülebilirliğini sağlayın.