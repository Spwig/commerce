---
title: Cari Programı
---

Cari program, ürünleri tanıtacak ortaklar kazanmak ve onların oluşturduğu satışlardan komisyon elde etmek için size olan ortakları recruit etmenizi sağlar. Cari ortaklar benzersiz referans bağlantılarını paylaşır ve Spwig otomatik olarak tıklamaları izler, siparişleri atar ve komisyonları hesaplar.

![Cari programları](/static/core/admin/img/help/affiliate-program/program-list.webp)

## Nasıl Çalışır

1. Komisyon oranları ve kurallarla bir veya daha fazla **cari programı** oluşturun
2. Cari ortaklar **kayıt olur** bir kamu portalı üzerinden veya manuel olarak eklenir
3. Her cari ortak, takip kodu ile birlikte **benzersiz referans bağlantısı** alır
4. Bir müşteri bağlantıya tıklar ve bir satın alma yapar, **komisyon** kaydedilir
5. Komisyonları inceleyin ve onaylayın, sonra **ödeme** işlemini yapın

## Program Oluşturma

**Pazarlama > Cari Programlar**'a gidin ve **Program Ekle**'ye tıklayın.

### Program Ayarları

| Ayar | Açıklama |
|---------|-------------|
| **Ad** | Ortaklara görünen program adı (örneğin, "Ortak Program") |
| **Komisyon Türü** | Sipariş toplamının **Yüzdesi** veya satış başına **Sabit** bir miktar |
| **Komisyon Oranı** | Ortakların kazandığı yüzdelik veya sabit miktar |
| **Çerez Ömrü** | Referans takip çerezinin kaç gün sürer (varsayılan: 30 gün) |
| **Minimum Ödeme** | Ortak bir ödeme talep edebilmeden önce kazanması gereken minimum miktar |
| **Ortakları Otomatik Onayla** | Yeni cari başvuruları otomatik olarak kabul et veya manuel onay gerektir |
| **Durum** | Aktif, duraklatılmış veya kapatılmış |

### Komisyon Türleri

- **Yüzdesel** — Ortaklar, her referans siparişinin alt toplamının yüzdesini kazanır (örneğin, 100 dolarlık bir siparişin 10% = 10 dolarlık komisyon)
- **Sabit** — Ortaklar, sipariş değeri ne olursa olsun her satış başına sabit bir miktar kazanır (örneğin, her satış başına 5 dolar)

## Ortakları Yönetme

**Pazarlama > Ortaklar**'a gidin ve ortak hesaplarını görüntüleyin ve yönetin.

### Ortak Detayları

Her ortakın:
- **Ortak Kodu** — Referans URL'lerinde kullanılan benzersiz bir kod (otomatik olarak oluşturulmuş veya özel)
- **Referans Bağlantısı** — Ortak tarafından paylaşılacak tam takip URL'si (örneğin, `yourstore.com/?ref=CODE`)
- **Durum** — Beklemede, onaylanmış veya reddedilmiş
- **Ödeme Yöntemi** — Ortakın ödemeleri nasıl alır (PayPal veya banka transferi)
- **Program Üyeliği** — Ortakın hangi programlara ait olduğunu

### Manuel Ortak Ekleme

1. **Ortak Ekle**'ye tıklayın
2. Mevcut bir müşteri hesabı seçin veya yeni bir tane oluşturun
3. Ortakı bir veya daha fazla programa atayın
4. Ortak kodunu belirleyin (veya boş bırakın otomatik olarak oluşturulsun)

### Ortak Portalı

Ortaklar, kendilerine özel bir portal üzerinden:
- Kazançlarını ve tıklama istatistiklerini gösterecek bir dashboard'a erişebilir
- Referans bağlantılarını kopyalayabilir
- Komisyon geçmişini takip edebilir
- Ödeme talep edebilir

Portal URL'si, mağazanızda `/affiliate/` adresinde otomatik olarak mevcuttur.

## Takip ve Komisyonlar

### Takip Nasıl Çalışır

1. Bir müşteri bir ortakın referans bağlantısına tıklar
2. Müşterinin tarayıcısında bir takip çerezinin ayarlanır (konfigüre edilen çerez ömrü kadar)
3. Müşteri, çerez ömrü boyunca bir sipariş verirse, sipariş ortak olarak atılır
4. Durumu **Beklemede** olan bir komisyon kaydı oluşturulur

### Komisyon Durumları

| Durum | Açıklama |
|--------|-------------|
| **Beklemede** | Komisyon kaydedildi, inceleme bekliyor |
| **Onaylandı** | Doğrulandı ve ödeme için hazırdır |
| **Reddedildi** | Komisyon reddedildi (örneğin, sahte sipariş veya iade edilen ürün) |
| **Ödenmiş** | Komisyon tamamlanmış bir ödeme ile birlikte |

### Komisyonları İnceleme

**Pazarlama > Komisyonlar**'a gidin ve bekleyen komisyonları inceleyin:

1. Sipariş detaylarını kontrol ederek satışın geçerli olup olmadığını doğrulayın
2. **Onayla**'yı tıklayarak onaylayın veya **Reddet**'i bir nedenle seçin
3. Onaylanan komisyonlar, ortağın ödeme bakiyesine eklenir

## Ödemeler

Bir ortağın onaylanmış komisyon bakiyesi minimum ödeme eşiğini ulaştığında, bir ödeme işleme yapabilirsiniz.

### Ödeme İşleme

1. **Pazarlama > Ödemeler**'e gidin
2. Mevcut bakiyeleri olan ortakları seçin
3. Ödeme yöntemini seçin:
   - **PayPal** — Ortakın PayPal e-postasına doğrudan fon gönderin
   - **Banka Transferi** — Manuel bir banka transferi kaydedin
4. Ödeme işlemini onaylayıp yapın
5. Ödeme durumu **Tamamlandı** olarak güncellenir ve komisyonlar **Ödenmiş** olarak işaretlenir

### Ödeme Sağlayıcıları

Spwig, otomatik ödemeler için ödeme sağlayıcılarıyla entegre olur:
- **PayPal** — PayPal API üzerinden otomatik kitle ödemeleri
- **Airwallex** — Döviz kuru rekabetçi uluslararası ödemeler
- **Manuel** — Spwig dışındaki ödemeleri kaydedin

## Referans Bağlantıları

Her ortağın referans bağlantısı şu deseni takip eder:

```
https://yourstore.com/?ref=AFFILIATE_CODE
```

Ortaklar ayrıca belirli ürün veya kategorilere bağlantılar oluşturabilir:

```
https://yourstore.com/products/shoe-name/?ref=AFFILIATE_CODE
```

`ref` parametresi herhangi bir sayfada çalışır — takip çerezinin ayarlanması, hangi sayfaya düştüğünüzle ilgili değildir.

## Program Analitiği

Cari program dashboard'ı şu bilgileri gösterir:
- **Toplam Tıklamalar** — Referans bağlantılarının kaç kez tıklandığı
- **Toplam Siparişler** — Ortaklara atanan siparişler
- **Toplam Komisyonlar** — Tüm komisyonların toplamı (beklemede, onaylanmış ve ödenmiş)
- **Aktif Ortaklar** — Mevcut referanslar oluşturan onaylanmış ortakların sayısı

## İpuçları

- Başlangıçta **yüzdesel komisyon** (5–15%) ile başlayın — bu, sipariş değeriyle doğal olarak ölçeklenebilir ve ortaklar için anlaşılması kolaydır.
- **30 günlük çerez ömrü**'nü temel olarak ayarlayın — bu, müşterilere geri dönmeleri ve satın almayı tamamlamaları için zaman sağlar, ancak hala satışın ortaklara atandığını sağlar.
- Kamu programları için **otomatik onay**'ı etkinleştirin, böylece sürtünmeyi azaltın, veya davet etme odaklı programlarda her ortağı doğrulamak istiyorsanız manuel onay kullanın.
- **Minimum ödeme** (örneğin, 25–50 dolar) ayarlayın, böylece birçok küçük işlemi işlemekten kaçının.
- **Ortak portalını** markanızla özelleştirin — ortaklar, deneyim profesyonel hissediyorsa, mağazanızı daha çok tanıtma eğilimindedir.
- **Sahte örüntüleri** için komisyonları düzenli olarak izleyin, örneğin, kendine referans, anormal yüksek iade oranları veya şüpheli tıklama hacimleri.

