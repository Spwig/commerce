---
title: Abonelik Planları
---

Abonelik planları, ürünleriniz için tekrarlayan faturalandırma sunmanıza olanak tanır. Bu, tüketicilerin tekrar tekrar satın aldıkları, tüketilebilir ürünler, hizmetler, derlenmiş kutular veya herhangi bir ürün için idealdir. Bu rehber, planları oluşturmak ve yapılandırmak, fiyatlandırma seviyelerini ayarlamak, deneme dönemlerini kurmak ve isteğe bağlı ekstra ürünler eklemek hakkında açıklar.

## Başlarken

Yönetim yan panelinde **Abonelikler > Abonelik Planları**'na gidin. Plan listesi, fiyatlandırma modeliniz, aktif abone sayısı ve erişilebilirlik durumu ile birlikte tüm planlarınızı gösterir.

Yeni bir plan oluşturmak için **+ Yeni Abonelik Planı Ekle** butonuna tıklayın — bu, adım adım kurulumu içeren bir plan oluşturma sihirbazı açar.

![Abonelik planları listesi](/static/core/admin/img/help/subscription-plans/plan-list.webp)

Bir plan, kendi başına satın alınamaz — bir şablondur. Burada oluşturduktan sonra, müşterilerin gerçekten abone olabilmesi için ürünün **Abonelikler** sekmesinden (Sadece, Değişken ve Dijital ürünler) bir veya daha fazla ürüne abone olmaları için bunu ekleyin. Bu adımı yapmak için [Ürünleri Abonelik Olarak Satma](/help/selling-products-as-subscriptions) sayfasına bakın.

## Plan Bilgisi

İlk bölüm, planınızın temel kimliğini yakalar.

- **Plan Adı** — Abonelik alırken müşterilerin gördüğü isim. Diğer mağaza dilleri için çeviri eklemek için dünya ikonuna tıklayın.
- **Slug** — Adından otomatik olarak üretilen URL'ye uygun bir tanımlayıcı (örn. `premium-plan`). İç ve entegrasyonlarda kullanılır.
- **Açıklama** — Planın ne içerdiğini tanımlayan isteğe bağlı metin. Çevirilere izin verir.

## Fiyatlandırma Modeli

Bu plan için fiyatlandırma nasıl yapılandırılacağını seçin:

| Fiyatlandırma Modeli | En Uygun Olan |
|---------------------|----------------|
| **Seviyeli Fiyatlandırma** | Uzun vade için indirimlerle aylık, çeyreklik ve yıllık taahhüt seçenekleri sunar |
| **Miktar Bazlı** | Toplamın miktarla ölçeklendiği (örn. ekip lisansları) koltuk veya kullanıcı bazlı fiyatlandırma |
| **Düz Fiyat** | Herhangi bir değişiklik olmayan tek bir sabit fiyat |

**Miktar Bazlı** planlar için, **Minimum Miktar**'ı (gereken en az koltuk sayısı) ve isteğe bağlı olarak bir **Maksimum Miktar** belirleyin, abone olabilecekleri koltuk sayısını sınırlayın.

## Fiyatlandırma Seviyeleri

Fiyatlandırma seviyeleri, bu plan üzerindeki müşterilerin faturalandırma sıklığı ve indirim seçeneklerini tanımlar. Ana formun hemen altında **Fiyatlandırma Seviyeleri** bölümünde ekleyin.

Her seviye şu alanı içerir:

- **Seviye Adı** — Müşterilere gösterilen etiket (örn. `Aylık`, `Yıllık — %20 Kazanın`). Çevirilere izin verir.
- **Faturalandırma Döngüsü** — Müşterinin ne sıklıkla faturalandırıldığını belirler: Günlük, Haftalık, Aylık, Çeyreklik, Yarıyıllık veya Yıllık.
- **Faturalandırma Aralığı** — Faturalandırma döngüsünün çarpanı. Aylık olarak 2'ye ayarlanırsa, 2 ayda bir faturalandırılır.
- **İndirim Yüzdesi** — Bu seviye için ürün fiyatına uygulanan indirim. Tam fiyata `0` olarak ayarlayın, ya da %20 indirim için `20` olarak ayarlayın. Bu indirim, ürünün kendisindeki herhangi bir satış fiyatına ek olarak biriktirilir.
- **Varsayılan Seviye** — Abone olma seçeneklerini görüntülediklerinde müşteriler için önceden seçili olacak şekilde bir seviyeyi vurgulayın.

İndirim, sadece yeniden imzalamalarda değil, müşteriye ait ilk faturalandırma döngüsünden itibaren geçerlidir — %20 indirimli bir seviye, ilk faturalandırma döngüsünden itibaren %20 indirimli olur (planın bir deneme dönemi varsa, deneme sonrası ilk faturalandırma döngüsünden itibaren).

### Örnek: Üç seçenekli seviyeli plan

"Kahve Kulübü" abonelik planı için:

| Seviye Adı | Faturalandırma Döngüsü | İndirim |
|------------|------------------------|---------|
| Aylık | Aylık | %0 |
| Çeyreklik — %10 Kazanın | Çeyreklik | %10 |
| Yıllık — %20 Kazanın | Yıllık | %20 |

## Deneme Dönemi

Bir deneme dönemi, müşterilerin ilk tam faturalandırma öncesi aboneliklerini denemelerini sağlar. Bunu **Deneme Dönemi** bölümünde yapılandırın:

- **Deneme Dönemi (Gün)** — Ücretsiz deneme günü sayısı. Deneme'yi devre dışı kılmak için `0` olarak ayarlayın. Maksimum 365 gündür.
- **Deneme Fiyatı** — Deneme süresince isteğe bağlı olarak azaltılmış fiyat (örn. ilk ay için $1). Tamamen ücretsiz bir deneme için boş bırakın.

## İptal Politikası

**İptal Politikası** bölümünde, müşterilerin aboneliklerini nasıl iptal edebileceğini kontrol edin.

| Politika | Açıklama |
|--------|-------------|
| **Her Zaman İptal** | Müşteriler her zaman anında iptal edilebilir |
| **Dönem Sonunda İptal** | İptal, ödemeli dönemin sonunda geçerli olur — müşteriler, süresi dolana kadar erişime devam eder |
| **Minimum Taahhüt Gerekli** | İptal etmeden önce müşteri, minimum sayıda faturalandırma döngüsü tamamlamalıdır |

Ek ayarlar:

- **Minimum Taahhüt (Döngü)** — Taahhüt politikası kullanırken, faturalandırma döngüsünün (örneğin, 3 aylık minimum için `3`) minimum sayısını ayarlayın.
- **İzinli Süre (Gün)** — bir ödeme hatası sonrasında, abonelik devre dışı bırakılmadan önce devam eden erişim günleri. Hemen devre dışı etmek için `0` olarak ayarlayın.
- **Yeniden Aktivasyon Periyodu (Gün)** - Abonelikten çıkışın ardından, müşteriye yeni bir abonelik oluşturmadan önce yeniden aktif hale getirebileceği günler.

## Plan değişikliği davranışı

Müşteriler planlar arası yukarı veya aşağı geçiş yaparken, değişimin ne zaman geçerli olacağını kontrol edebilirsiniz:

- **Yükseltme Davranışı** — **Ani** (şimdi kademeli miktar tahsil edin) veya **Yenileme Sırasında** (bir sonraki faturalandırma tarihinde değiştirin) olarak ayarlayın.
- **Aşağılama Davranışı** — **Ani** (bir sonraki faturaya kredi uygulayın) veya **Yenileme Sırasında** (bir sonraki faturalandırma tarihinde değiştirin) olarak ayarlayın.

## Sınırlar ve kısıtlamalar

- **Maksimum Faturalandırma Döngüsü** — abonelik otomatik olarak bitemeden önceki toplam faturalandırma döngüsü sayısı. Yeniden tekrarlayan faturalandırma için boş bırakın. Taksit planları veya zaman sınırlı abonelikler için yararlıdır.
- **Kurulum Ücreti** — abonelik ilk oluşturulduğunda toplanan tek seferlik bir ücret (örneğin, danışmanlık veya aktifleştirme ücreti). Kurulum ücreti olmayacaksa `0.00` olarak ayarlayın.

## Plan eklentileri

Eklentiler, abonelerin planlarına ekleyebilecekleri isteğe bağlı ekstra unsurlardır. **Plan Eklentileri** bölümünde ekleyin:

- **Eklenti Adı** — müşteriye gösterilen isim. Çevirilere uygun.
- **Açıklama** — eklentinin sağladığı şey.
- **Fiyat** — eklentinin maliyeti.
- **Faturalandırma Sıklığı** — eklentinin **Faturalandırma Döngüsüne Göre** (tekrarlayan) veya **Bir Kere** (abonelik başlangıcında) faturalandırılıp edilmediğini belirtin.
- **Miktarı Kabul Et** — müşterilerin eklentinin birden fazla birimini satın almasına izin vermek için etkinleştirin.
- **Zorunlu** — tüm yeni abonelere otomatik olarak eklentiyi dahil etmek için bu alanı işaretleyin. Zorunlu eklentiler, müşteri tarafından kaldırılamaz.

## Görünürlük ve durum

- **Aktif** — bir planı yeni abonelikler için devre dışı kılmak için işareti kaldırın. Mevcut abonelikler etkilenmez.
- **Kamuya Açık** — planı müşteriye açık sayfalardan saklamak için işareti kaldırın (mevcut abonelerin devam ettiği içi veya eski planlar için yararlıdır).
- **Sıralama Sırası** — abonelik seçim sayfalarında görüntüleme sırasını kontrol eder. Düşük sayılar önce gelir.

## İpuçları

- **Deneme süresi** kullanarak tereddütü azaltın — hatta 7 günlük ücretsiz deneme bile, abonelik ürünlerinde dönüşüm oranlarını significantly artırabilir.
- **Üç fiyat seviyesi** oluşturun (aylık, çeyreklik, yıllık) ve yıllık taahhütleri teşvik etmek ve nakit akışınızı artırmak için artan indirimlerle.
- Hizmet temelli abonelikler için **İptal Politikası** 'nı **Dönem Sonunda İptal** olarak ayarlayın, böylece müşterileri ödeme dönemlerine kadar erişimlerini korursun — bu adil hissi verir ve iade oranlarını azaltır.
- **İzinli Süre** 'yi 3-7 gün olarak ayarlayın, ödeme hataları için. Bu, erişimden uzaklaşmadan önce müşteriye ödeme yöntemini güncellemesi için zaman tanır.
- **Zorunlu** bandını eklentilerde seyrek kullanın — sadece gerçek manasında zorunlu olanlar (örneğin, bir hizmet sözleşmesi) için kullanın, fiyatları artırmak için bir yolla değil.
- Aboneliği olmayan planları silmek yerine devre dışı bırakın — bu, daha önce abone olan müşteriler için tarihsel verileri korur.