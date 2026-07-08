---
title: Komisyonları Anlamak
---

Komisyonlar, bir ortakın mağazanıza satışları yönlendirmesi halinde oluşturulan gelir kayıtlarıdır. Her komisyon, belirli bir sipariş, ortak ve programla ilişkilidir ve "Beklemede" durumundan "Ödenmiş" durumuna kadar bir yaşam döngüsü geçirecektir. Bu kılavuz, komisyonların nasıl çalıştığını, nasıl hesaplandığını ve etkili bir şekilde nasıl yönetileceğini açıklar.

## Komisyon Nedir?

Bir komisyon, bir ortağın bir müşteriye referans vererek tamamlanmış bir satış için borçlu olduğu miktarı temsil eder. Bir müşteri, ortağın referans linkini tıklattığında ve çerez yaşam süresi penceresi içinde bir sipariş verdiğinde, Spwig otomatik olarak bir komisyon kaydı oluşturur.

Her komisyon şu bilgileri içerir:
- **Ortak** — Müşteriyi referans veren ortak
- **Program** — Komisyon kurallarını tanımlayan ortak program
- **Sipariş** — Komisyonu oluşturmuş olan sipariş
- **Miktar** — Hesaplanan komisyon değeri
- **Durum** — Komisyon yaşam döngüsünde mevcut aşama
- **Tarihler** — Oluşturulma tarihi, onaylama/red etme tarihi ve ödeme tarihi

## Komisyon Hesaplama

Komisyonlar, programın komisyon türü ve oranına göre otomatik olarak hesaplanır.

| Komisyon Türü | Hesaplama | Örnek |
|-----------------|-------------|---------|
| **Yüzde** | Sipariş Toplamı × Komisyon % ÷ 100 | Sipariş: $200, Oran: 10% → **$20 komisyon** |
| **Sabit** | Sipariş başına sabit miktar | Oran: $15 → **$15 komisyon** (sipariş değeri ne olursa olsun) |

### Hesaplama Örnekleri

**Yüzde Komisyon (10%)**:
- Müşteri $50 siparişi verir → $5 komisyon
- Müşteri $150 siparişi verir → $15 komisyon
- Müşteri $300 siparişi verir → $30 komisyon

**Sabit Komisyon ($20)**:
- Müşteri $50 siparişi verir → $20 komisyon
- Müşteri $150 siparişi verir → $20 komisyon
- Müşteri $300 siparişi verir → $20 komisyon

Komisyon, **sipariş alt toplamı** (kargo ve vergilerden önce) üzerinden hesaplanır ve sipariş verildiğinde hemen oluşturulur.

## Komisyon Yaşam Döngüsü

Her komisyon, ödeme yapılıncaya kadar bir dizi durum geçer:

```
Beklemede → Onaylandı → Ödenmiş
   ↓
Reddedildi
```

### Durum Tanımlamaları

| Durum | Açıklama | Ne Olur |
|--------|-------------|--------------|
| **Beklemede** | Sipariş verildi, komisyon onay bekliyor | Komisyon oluşturuldu ama henüz onaylanmadı. Ortak bunu görebilir ama para çekemez. |
| **Onaylandı** | Satıcının satışın geçerli olduğunu onaylaması | Komisyon doğrulanır ve ortağın mevcut bakiyesine eklenir. Ödeme için elverişli. |
| **Reddedildi** | Satıcı komisyonu reddeder | Komisyon reddedilir (örneğin, sipariş iade edildi, dolandırıcılık veya koşulları ihlal etti). Ödeme için elverişli değildir. |
| **Ödenmiş** | Komisyon tamamlanmış bir ödeme ile birlikte | Ortak ödendi. Komisyon sonlandırılmıştır ve değiştirilemez. |

![Komisyon Listesi](/static/core/admin/img/help/commission-management/commission-list.webp)

## Komisyonların Oluşturulduğu Zamanlar

Komisyonlar, şu sırayla otomatik olarak oluşturulur:

1. **Müşteri ortak linkini tıklar** — Referans URL'si, ortağın benzersiz izleme kodunu içerir (örneğin, `?ref=JOHNSMITH`)
2. **Çerez ayarlanır** — Müşterinin tarayıcısında, ortak kodu içeren bir izleme çerezi saklanır
3. **Çerez yaşam süresi içinde satın alma** — Müşteri, çerezin süresi dolmadan önce bir sipariş tamamlar (varsayılan: 30 gün)
4. **Sistem siparişi atar** — Spwig, aktif bir izleme çerezini kontrol eder ve referans ortağı tanımlar
5. **Komisyon otomatik olarak oluşturulur** — Sipariş verildiğinde, durumu **Beklemede** olan bir komisyon kaydı oluşturulur

Sipariş verildiğinde komisyon **hemen** oluşturulur, ödeme onaylandığında bile. Bu, siparişler işlenirken komisyonları incelemek için satıcıları sağlar.

## İzleme & Atama

Spwig, bir satışın hangi ortağa kredi verileceğini belirlemek için **son tıklama ataması** kullanır.

### Atama Nasıl Çalışır

- **Son tıklama modeli** — En son tıklanmış ortak linki kredi alır (çoklu ortaklar tarafından referans verilmiş olsa bile)
- **Çerez tabanlı izleme** — Bir çerez, müşterinin tarayıcısında ortak kodunu saklar
- **Çerez yaşam süresi** — Satışın ataması için olan pencereyi belirler (program başına yapılandırılabilir, genellikle 30 gün)
- **IP ve oturum izleme** — Ek veriler, dolandırıcılık desenlerini tanımlamaya yardımcı olur

### Atama Örneği

- Gün 1: Müşteri Ortak A'nın linkini tıklar → Ortak A için çerez ayarlanır
- Gün 5: Müşteri Ortak B'nin linkini tıklar → Çerez **güncellenir** Ortak B'ye (son tıklama kazanır)
- Gün 7: Müşteri bir sipariş verir → Komisyon **Ortak B**'ye gider

Eğer müşteri Gün 35'te (30 günlük çerez süresi dolduktan sonra) döner ve bir sipariş verirse, **hiçbir komisyon** oluşturulmaz çünkü izleme penceresi kapanmıştır.

## Komisyon Detayları

**Pazarlama > Komisyonlar** menüsüne giderek tüm komisyon kayıtlarını görüntüleyebilirsiniz.

### Komisyon Alanları

Her komisyon şu alanları görüntüler:

| Alan | Açıklama |
|-------|-------------|
| **Ortak** | Ortakın adı ve kodu |
| **Program** | Ortak program adı |
| **Sipariş** | Sipariş numarası (tam sipariş detaylarını görmek için tıklayabilirsiniz) |
| **Miktar** | Hesaplanan komisyon değeri |
| **Durum** | Mevcut aşama (Beklemede, Onaylandı, Reddedildi, Ödenmiş) |
| **Oluşturulma Tarihi** | Komisyonun oluşturulduğu zaman |
| **Onay/Reddetme Tarihi** | Durumun güncellendiği zaman |
| **Ödeme Tarihi** | Ödeme işleminin yapıldığı zaman |
| **Notlar** | Komisyon hakkında iç notlar |

### Sipariş Detaylarını Görüntüleme

Komisyon kaydındaki **sipariş numarasını** tıklayarak orijinal siparişi görüntüleyebilirsiniz. Bu, şu şeyleri doğrulamanıza olanak tanır:
- Sipariş toplamı ve satın alınan ürünler
- Müşteri bilgileri
- Ödeme durumu
- Kargo durumu
- Herhangi bir iade veya iade

Bu bağlam, komisyonu onaylamayı veya reddetmeyi karar vermenize yardımcı olur.

## Komisyonları Yönetme

Bu kılavuz, komisyonları anlamanıza odaklanıyor. Ancak, komisyonları onaylama, reddetme ve ödeme işlemleri için pratik adımlar **Komisyon Yönetimi** yardım konusunda ayrıntılı olarak ele alınmıştır.

### Hızlı Genel Bakış

- **Onaylama** — Siparişin geçerli olduğunu doğrulayın ve komisyonun geçerli olduğunu onaylayın
- **Reddetme** — Hileli siparişler, iadeler veya politika ihlalleri için komisyonları reddedin
- **Not ekleme** — Onay veya reddetme nedenlerini belgeleyin, gelecekteki başvurular için
- **Ödeme işleme** — Onaylanan komisyonları toplu ödeme işlemlerine gruplayın

Her yönetim görevi için adım adım talimatlar için ilgili yardım konularını inceleyin.

## İpuçları

- İlk ayınızda **günlük olarak** bekleyen komisyonları inceleyin, bir ritim kurun ve izleme sorunlarını erken fark edin
- Yeni komisyonlar oluşturulduğunda size haber veren **e-posta bildirimlerini** ayarlayın, böylece sipariş detayları hâlâ taze iken onları inceleyebilirsiniz
- Siparişin tamamlanmasından **sonra** komisyonları onaylayın (siparişin verilmesinden hemen sonra değil), iptaller ve iadeleri hesaba katın
- **Not alanı**'nı kullanarak kararlarınızı belgeleyin, özellikle reddedilen komisyonlar için, ortaklar sorular sorarsa bir kayıtınız olsun
- **Reddetme desenlerini** inceleyin — eğer bir ortakta birçok reddedilmiş komisyon varsa, dolandırıcılık veya program koşullarının anlaşılması sorununu gösterebilir
- **Komisyon onaylama politikası** oluşturmayı düşünün (örneğin, "14 günlük iade penceresinden sonra onaylanır") ve ortaklara açık ve net beklentiler belirtmek için bunu onlara iletin