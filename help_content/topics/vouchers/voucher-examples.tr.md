---
title: Bono Örnekleri
---

Bu kılavuz, en yaygın bono türleri için alan alan alan örnekler sunar. Her örnek, **Pazarlama > Bono** → **+ Bono Ekle** ile bir bono oluştururken ne gireceğinizi gösterir.

![Bono Kartı](/static/core/admin/img/help/voucher-examples/voucher-card.webp)

## Örnek 1: İndirim Sınırına Uğramış Yüzde İndirimi

**Senaryo:** Sepetin tamamına %20 indirim sunun, ancak indirim $50'ye kadar sınırlanmalı ve yüksek değerli siparişler kârlı kalmalı. Geçerlilik tarihi yok.

| Alan | Değer |
|-------|-------|
| Kod | `SAVE20` |
| Ad | %20 İndirim — Maksimum $50 |
| İndirim Türü | Yüzde |
| İndirim Değeri | 20 |
| Maksimum İndirim Tutarı | 50 |
| Uygulama Kapsamı | Sepetin Tamamı |
| Toplam Maksimum Kullanım Sayısı | *(boş — sınırsız)* |
| Müşteri Başına Maksimum Kullanım Sayısı | 1 |
| Minimum Sipariş Değeri | *(boş — minimum yok)* |

**Sınır nasıl çalışır:** $200'lık bir siparişte indirim $40'dır. $300'lık bir siparişte $60 olurdu, ancak sınır $50'e sınırlanır. $500'lık bir siparişte indirim hala $50'dir. Bu, hem etkileyici hem de gerçek indirim tahmini olan bir kampanya başlatmanıza olanak tanır.

## Örnek 2: Minimum Değerle Sabit Tutarlı İndirim

**Senaryo:** $75'ten fazla herhangi bir siparişte müşterilere $10 indirim vererek daha büyük sepetlerin teşvik edilmesini sağlayın.

| Alan | Değer |
|-------|-------|
| Kod | `TAKE10` |
| Ad | $75'ten Üstü Siparişlerde $10 İndirim |
| İndirim Türü | Sabit Tutar |
| İndirim Değeri | 10 |
| Uygulama Kapsamı | Sepetin Tamamı |
| Minimum Sipariş Değeri | 75 |
| Müşteri Başına Maksimum Kullanım Sayısı | 0 *(sınırsız)* |
| Bitiş Tarihi | *(boş — geçerlilik yok)* |

> **Not:** Minimum sipariş değeri ayarlamak, marjınızı korur. Bu ayar yapılmazsa, müşteri bu kodu $12'lik bir siparişte kullanabilir ve kârınız yok olur. Sabit tutarlı bonoları her zaman mantıklı bir minimumla birlikte kullanın.

## Örnek 3: Ücretsiz Kargo

**Senaryo:** Herhangi bir siparişte minimum harcama olmadan ücretsiz kargo sunun.

| Alan | Değer |
|-------|-------|
| Kod | `FREESHIP` |
| Ad | Ücretsiz Kargo |
| İndirim Türü | Ücretsiz Kargo |
| Uygulama Kapsamı | Sepetin Tamamı |
| Toplam Maksimum Kullanım Sayısı | *(boş — sınırsız)* |
| Müşteri Başına Maksimum Kullanım Sayısı | 1 |
| Minimum Sipariş Değeri | *(boş — minimum yok)* |

> **Not:** **Ücretsiz Kargo** indirim türünü seçin, bu da siparişten otomatik olarak kargo ücretlerini kaldırır. Bu, müşteri hangi kargo yöntemini seçerek çalışır.

## Örnek 4: İlk Ziyaretçi Hoş Geldiniz Kodu

**Senaryo:** Yeni müşterilere ilk siparişlerinde %15 indirim vererek dönüşümü teşvik edin.

| Alan | Değer |
|-------|-------|
| Kod | `WELCOME15` |
| Ad | Hoş Geldiniz — İlk Siparişte %15 İndirim |
| İndirim Türü | Yüzde |
| İndirim Değeri | 15 |
| Uygulama Kapsamı | Sepetin Tamamı |
| Müşteri Başına Maksimum Kullanım Sayısı | 1 |
| Sadece İlk Ziyaretçiler | İşaretlenmiş |

Sistem, müşteriye önceki tamamlanmış siparişleri olup olmadığını kontrol ederek ilk ziyaretçi durumunu doğrular. Geçmiş siparişi olan bir müşteri bu kodu uygulamaya çalışırsa, ödeme sırasında açık bir hata mesajı görür.

## Örnek 5: Ürün Özel Bono

**Senaryo:** Seçilmiş ürünlerde $5 indirim sunun — örneğin, yavaş satılan stokları hareketlendirmek için.

| Alan | Değer |
|-------|-------|
| Kod | `PICK5` |
| Ad | Seçilmiş Ürünlerde $5 İndirim |
| İndirim Türü | Sabit Tutar |
| İndirim Değeri | 5 |
| Uygulama Kapsamı | Belirli Ürünler |
| Uygun Ürünler | *(hedef ürünleri seçin)* |
| Müşteri Başına Maksimum Kullanım Sayısı | 1 |

> **Not:** Ürün kapsamı, bireysel SKU'ları indirmek istediğinizde kullanın. Kategori kapsamı (bir sonraki örnek), bir bölümdeki tüm ürünleri indirmek istediğinizde kullanın. Ürün kapsamı, size hassas kontrol sağlar; kategori kapsamı, katalogunuz sık sık değiştiğinde daha kolay bakım sağlar.

## Örnek 6: Kategori Bono

**Senaryo:** Elektronik kategorisindeki tüm ürünleri %25 indirimle kampanya yapın.

| Alan | Değer |
|-------|-------|
| Kod | `ELEC25` |
| Ad | Elektronik Ürünlerde %25 İndirim |
| İndirim Türü | Yüzde |
| İndirim Değeri | 25 |
| Uygulama Kapsamı | Belirli Kategoriler |
| Uygun Kategoriler | Elektronik |
| Toplam Maksimum Kullanım Sayısı | *(boş — sınırsız)* |
| Müşteri Başına Maksimum Kullanım Sayısı | 1 |


Kategoriye bağlandığında, indirim sepetinizdeki uygun öğelere uygulanır.

Elektronik olmayan ürünler, tam fiyatla ücretlendirilir.

## İndirim Türü Karşılaştırması

| Tür | Nasıl Çalışır | En Uygun Olduğu | Örnek |
|------|-------------|----------|---------|
| **Yüzde** | Uygun toplamın bir yüzdesini indirir | Sipariş büyüklüğüyle artan ölçekli indirimler | Sepetin tamamına %20 indirim |
| **Sabit Tutar** | Sabit bir dolar tutarını indirir | Basit ve öngörülebilir kampanyalar | $75 üzeri siparişlere $10 indirim |
| **Ücretsiz Kargo** | Siparişten kargo ücretlerini kaldırır | Ödeme sırasında sepet boşalmasını azaltmak | Ücretsiz kargo, minimum tutar yok |

## Kapsam Karşılaştırması

| Kapsam | Nasıl Çalışır | En Uygun Olduğu |
|-------|-------------|----------|
| **Tüm Sepet** | İndirim, tam sipariş toplamına uygulanır | Mağaza genelindeki kampanyalar ve hoş geldiniz kodları |
| **Belirli Ürünler** | İndirim, sepetteki seçilmiş ürünlerde uygulanır | Belirli bir stokun temizlenmesi veya özel fırsatlar |
| **Belirli Kategoriler** | İndirim, seçilmiş kategorilerdeki öğelere uygulanır | Departman genelindeki satışlar ve mevsimsel kampanyalar |

## İpuçları

- **Hafızada kalabilecek kodlar kullanın** — `SUMMER20`, `COUPONX1600406498`'den daha iyi dönüştürülür. Toplu kampanyalar için otomatik olarak oluşturulan kodları saklayın.
- **Dağıtmadan test edin** — Voucher koduyla test siparişi vererek, kodun doğru uygulandığını ve tüm sınırları saygılı olduğundan emin olun.
- **Kullanımı izleyin** — Her voucher kartındaki Kullanımlar sayısını kontrol ederek kampanya performansını gerçek zamanlı olarak izleyin.
- **Duyuru çubuğu ile birlikte kullanın** — Voucher kodunuzu bir site genelinde duyuru ile tanıtın, müşteriler alışverişe başlamadan önce onu görsün.