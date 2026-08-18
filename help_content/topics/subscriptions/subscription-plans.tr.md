---
title: Abonelik Planları
---

Abonelik planları, ürünleriniz için tekrarlayan faturalandırma sunmanıza olanak tanır. Bu, tüketicilerin tekrar tekrar satın aldıkları, tüketilebilir ürünler, hizmetler, derlenmiş kutular veya herhangi bir ürün için idealdir. Bu kılavuz, planlar oluşturmayı ve yapılandırmayı, fiyatlandırma seviyelerini ayarlamayı, deneme dönemleri eklemeyi ve isteğe bağlı ekstra bileşenleri eklemeyi anlatır.

## Başlarken

Yönetim yan menüsünde **Abonelikler > Abonelik Planları**'na gidin. Plan listesi, fiyatlandırma modeliniz, aktif abone sayısı ve erişim durumu ile tüm planlarınızı gösterir.

![Abonelik planları listesi](/static/core/admin/img/help/subscription-plans/plan-list.webp)

Yeni bir plan oluşturmak için **Sihirbazla Oluştur** butonuna tıklayın — bu, plan oluşturma sihirbazını açar ve kurulumu adım adım size götürür. Bunun yanında bulunan **+ Plan Ekle** butonu, sihirbaz yerine kendi başınıza tüm işlemleri yapılandırmayı tercih eden satıcılar için boş bir form açar.

Bir plan, kendi başına satın alınamaz — bir şablondur. Burada oluşturduğunuz planı, müşterilerin gerçekten abone olabilmesi için ürünün **Abonelikler** sekmesinden (Sadece, Değişken ve Dijital ürünler) bir veya daha fazla ürüne bağlayın. Bu adımı yapmak için [Ürünleri Abonelik Olarak Satma](/help/selling-products-as-subscriptions) sayfasına bakın.

## Plan düzenleyicisi

Listeden bir planı açmak (ismini veya kaleme alım ikonunu tıklayarak) plan düzenleyicisine gider. Başlık, plan adını, fiyatlandırma modelini, **Aktif**/**Pasif** ve **Kamu**/**Kamuüstü** durum badjerlerini ve ne zaman oluşturulduğunu gösterir. Başlıkta sağ üst köşedeki iki buton, değişikliklerinizi kaydeder — check-circle simgesi, listeye dönmek için kaydeder, düz check simgesi ise sayfada kalmak için kaydeder ve düzenlemeye devam edebilirsiniz.

Başlık altında, planın kısa özetini gösteren bir istatistik şeridi vardır: **Aktif Abonelikler**, **Fiyatlandırma Seviyeleri**, **Ekstra Bileşenler** ve **Toplam Gelir**.

Formun geri kalanı beş sekme göre düzenlenmiştir:

| Sekme | Ne içerir? |
|-----|-------------------|
| **Genel** | Plan Bilgisi (isim, slug, açıklama) ve Durum (aktif/kamu) |
| **Fiyatlandırma** | Fiyatlandırma Yapılandırması, Deneme Dönemi ve Sınırlar & Kısıtlamalar |
| **Seviyeler & Ekstra Bileşenler** | Fiyatlandırma Seviyeleri ve Ekstra Bileşenler editörü |
| **Yaşam Döngüsü** | İptal Politikası ve Plan Değiştirme Davranışı |
| **Gelişmiş** | Sağlayıcı Entegrasyonu ve İstatistikler |

Aşağıdaki bölümler, her sekmenin ayarlarını yürütmektedir. **+ Plan Ekle**'den doğrudan yeni bir plan oluşturduğunuzda (sihirbaz yerine), aynı alanlar tek bir kaydırılabilir formda görünür, ancak sekme yerine. Planı bir kez kaydedin ve tam sekmeli düzenleyiciyi almak için tekrar açın.

## Plan Bilgisi (Genel Sekme)

**Plan Bilgisi** kartı, planınızın temel kimliğini kaydeder.

- **Plan Adı** — Abonelik alırken müşterilerin gördüğü isim. Diğer mağaza dilleri için çeviri eklemek için dünya ikonuna tıklayın.
- **Slug** — İsimden otomatik olarak üretilen URL dostu bir tanımlayıcı (örneğin, `premium-plan`). İçinde ve entegrasyonlarda kullanılır.
- **Açıklama** — Planın neye dahil olduğunu açıklayan isteğe bağlı metin. Çevirilere izin verir.

Aynı sekmedeki **Durum** kartı, **Aktif** ve **Kamu** anahtarlarını kontrol eder — aşağıda ki [Erişilebilirlik ve Durum](#visibility-and-status) bölümüne bakın.

![Plan düzenleyicisinin Genel sekmesi](/static/core/admin/img/help/subscription-plans/edit-form-general-tab.webp)

## Fiyatlandırma Modeli (Fiyatlandırma Sekmesi)

**Fiyatlandırma Yapılandırması** kartı, bu plan için fiyatlandırma yapısını kontrol eder:

| Fiyatlandırma Modeli | En Uygun Olan |
|---------------|----------|
| **Seviyeli Fiyatlandırma** | Uzun vadeli anlaşmalar için aylık, çeyreklik ve yıllık seçenekler sunar ve daha uzun süreler için indirimler |
| **Miktar Temelli** | Toplamın miktarla ölçeklendiği (örneğin, ekip lisansları) için kişi başı veya kullanıcı başı fiyatlandırma |
| **Düz Seviye** | Herhangi bir varyasyon olmayan tek bir sabit fiyat |

**Miktar Temelli** planlar için **Miktarı Aç** ve **Minimum Miktar**'ı (en az koltuk sayısı) ayarlayın ve isteğe bağlı olarak **Maksimum Miktar**'ı belirleyin — bir abonelinin satın alabileceği koltuk sayısını sınırlayın.

Tüm markdown formatını, resim yollarını, kod bloklarını ve teknik terimleri koruyun.

[![](https://spwig.com/static/core/admin/img/help/subscription-plans/edit-form-pricing-tab.webp)](/static/core/admin/img/help/subscription-plans/edit-form-pricing-tab.webp)

## Fiyatlandırma seviyeleri (Seviyeler & Ek Bölümler sekmesi)

Fiyatlandırma seviyeleri, bu plan üzerinde müşterilere sunulan faturalandırma sıklığı ve indirim seçeneklerini tanımlar. Eklerini **Seviyeler & Ek Bölümler** sekmesindeki **Fiyatlandırma Seviyeleri** kartında, Ek Bölümler düzenleyicisiyle birlikte ekleyin.

Her seviye şu alanlara sahiptir:

- **Seviye Adı** — Müşterilere gösterilen etiket (örneğin, `Aylık`, `Yıllık — %20 Kazanın`). Çevirilere uygun.
- **Faturalandırma Döngüsü** — Müşterinin ne sıklıkla faturalandırıldığını gösterir: Günlük, Haftalık, Aylık, Çeyreklik, Yarıyıllık veya Yıllık.
- **Faturalandırma Aralığı** — Faturalandırma döngüsü için çarpan. Aylık olarak 2 olarak ayarlanırsa, 2 aylık aralıkla faturalandırılır.
- **İndirim Yüzdesi** — Bu seviye için ürün fiyatına uygulanan indirim. Tam fiyat için `0` olarak ayarlayın, ya da %20 indirim için `20` ayarlayın. Bu indirim, ürünün kendisindeki herhangi bir satış fiyatına ek olarak biriktirilir.
- **Varsayılan Seviye** — Müşteriler planı görüntülediğinde bu seviyeyi önceden seçmek için bir tane seviyeyi varsayılan olarak işaretleyin.

İndirim, sadece yeniden imzalamalarda değil, müşteriye ait ilk faturalandırma döngüsünden itibaren geçerlidir — %20 indirimli bir seviye, ilk faturalandırma döngüsünden itibaren (veya planın varsa bir deneme sonrası ilk faturalandırma döngüsünden itibaren) %20 indirimli olarak çalışır.

### Örnek: Üç seçenekli seviyeli plan

"Kahve Kulübü" abonelik planı için:

| Seviye Adı | Faturalandırma Döngüsü | İndirim |
|-----------|-------------------|----------|
| Aylık | Aylık | %0 |
| Çeyreklik — %10 Kazanın | Çeyreklik | %10 |
| Yıllık — %20 Kazanın | Yıllık | %20 |

## Plan ekleri (Seviyeler & Ek Bölümler sekmesi)

Ekler, abonelerin planlarına ekleyebilecekleri isteğe bağlı ekstra unsurlardır. Bunları aynı sekmedeki **Ek Bölümler** kartında, Fiyatlandırma Seviyeleri'nin hemen altında ekleyin:

- **Ek Adı** — Müşterilere gösterilen isim. Çevirilere uygun.
- **Açıklama** — Ek'in sağladığı şey.
- **Fiyat** — Ek'in maliyeti.
- **Faturalandırma Sıklığı** — Ek, **Faturalandırma Döngüsüne Göre** (tekrarlayan) veya **Bir Kez** abonelik başlangıcında faturalandırılır.
- **Miktarı Kabul Et** — Müşterilerin ekten birden fazla birim almasına izin vermek için bu seçeneği etkinleştirin.
- **Zorunlu** — Yeni tüm aboneliklerde ekli olarak otomatik olarak eklenmesi için bu ekleyi zorunlu olarak işaretleyin. Zorunlu ekler, müşteri tarafından kaldırılamaz.

[![](https://spwig.com/static/core/admin/img/help/subscription-plans/edit-form-tiers-addons-tab.webp)](/static/core/admin/img/help/subscription-plans/edit-form-tiers-addons-tab.webp)

## Deneme süresi (Fiyatlandırma sekmesi)

Deneme süresi, ilk tam faturalandırma öncesi aboneliğinizi denemenize olanak tanır. Bunu **Deneme Süresi** kartında, Fiyatlandırma Yapılandırması'nın altında yapılandırın:

- **Deneme Süresi (Gün)** — Ücretsiz deneme günleri sayısı. Deneme'yi devre dışı etmek için `0` olarak ayarlayın. Maksimum 365 gündür.
- **Deneme Fiyatı** — Deneme süresindeki indirimsiz fiyat (örneğin, ilk ay için $1). Tamamen ücretsiz bir deneme için boş bırakın.

## Sınırlar ve kısıtlamalar (Fiyatlandırma sekmesi)

**Sınırlar & Kısıtlamalar** kartı, aynı Fiyatlandırma sekmesinde de bulunur ve şu bilgileri içerir:

- **Maksimum Faturalandırma Döngüsü Sayısı** — Abonelik otomatik olarak biteceği toplam faturalandırma döngüsü sayısı. Sınırsız tekrarlayan faturalandırma için boş bırakın. Taksit planları veya zaman sınırlı abonelikler için yararlıdır.

**Kurulum Ücreti** ve **Sıralama Sırası**, bu kartın bir parçası değildir — bu değerler, planı ilk kez **Sihirli Akışla Oluştur** akışı üzerinden oluşturduğunuzda bir kere ayarlanır ve daha sonra düzenleme ekranından değiştirilemez. Herhangi bir değeri değiştirmek isterseniz, planı devre dışı bırakın ve sihirli akışı kullanarak yeniden oluşturun, mevcut planı düzenlemek yerine. Kurulum ücretlerinin bu sürümdeki alışveriş sırasında otomatik olarak tahsil edilmeyeceğini unutmayın — bu alanı gelecekteki bir güncelleme için ayrılmış bir alan olarak kabul edin, ancak çalışan bir tahsilat olarak değil.

## İptal politikası (Yaşam döngüsü sekmesi)

**İptal Politikası** kartında, müşterilerin aboneliklerini nasıl iptal edebileceğini kontrol edin.

{
  "Policy": "Açıklama",
  "--------": "-------------",
  "**Cancel Anytime**": "Müşteriler herhangi bir zaman, hemen iptal edebilir",
  "**Cancel at Period End**": "İptal, ödemeli dönemin sonunda geçerli olur - müşteriler, süresi dolana kadar erişime devam eder",
  "**Minimum Commitment Required**": "Müşterilerin iptal etmeden önce minimum sayıda faturalandırma döngüsünü tamamlaması gerekir"
}

Ek ayarlar:

- **Minimum Taahhüt (Döngü)** — Taahhüt politikası kullanırken, faturalandırma döngülerinin (örneğin, 3 aylık minimum için `3`) minimum sayısını ayarlayın.
- **İzinli Dönem (Gün)** — Bir ödeme hatası sonrası, abonelik devamsızlığa geçmeden önce devam eden erişim günleri. Hemen devamsızlık için `0` ayarlayın.
- **Yeniden Aktivasyon Dönemi (Gün)** — Müşterinin bir daha abone olmadan, aboneliğini yeniden aktif hale getirebileceği iptal edildikten sonra günler.

## Plan değişikliği davranışı (Yaşam döngüsü sekmesi)

**Plan Değiştirme Davranışı** kartı, müşteriler planlar arası geçiş yaparken ne olacağını kontrol eder:

- **Yükseltme Davranışı** — **Ani** (şimdi kademeli miktar tahsil edin) veya **Yeniden Yenileme** (bir sonraki faturalandırma tarihinde değiştirin) olarak ayarlayın.
- **Aşağılama Davranışı** — **Ani** (bir sonraki faturaya kredi uygulayın) veya **Yeniden Yenileme** (bir sonraki faturalandırma tarihinde değiştirin) olarak ayarlayın.

![Plan düzenleyicisinin Yaşam döngüsü sekmesi](/static/core/admin/img/help/subscription-plans/edit-form-lifecycle-tab.webp)

## Gelişmiş sekme

**Gelişmiş** sekmesi, günlük hayatta nadiren ihtiyaç duyduğunuz ayarları içerir:

- **Sağlayıcı Entegrasyonu** — Bu planı, mağazanızın doğrudan sağlayıcı üzerinden abonelikleri yönetmesi yerine Spwig'ın kendi faturalandırma motoru üzerinden yönetmediği durumlarda, ödeme sağlayıcılarından plan/fiyat ID'lerine haritalayın (örneğin, `{"stripe": "price_xxx", "paypal": "P-xxx"}`).
- **İstatistikler** — Okunur rakamlar: **Aktif Abonelikler**, **Toplam Gelir**, ve planın **Oluşturulma Zamanı** / **Güncellenme Zamanı** zaman damgaları. Bu, sayfanın en üstündeki istatistik şeridindeki istatistikleri yansıtır.

![Plan düzenleyicisinin Gelişmiş sekmesi](/static/core/admin/img/help/subscription-plans/edit-form-advanced-tab.webp)

## Görünürlük ve durum (Genel sekme)

- **Aktif** — Yeni aboneliklerin oluşturulmasını engellemek için bir planı devre dışı bırakın. Mevcut abonelikler etkilenmez.
- **Kamuya Açık** — Müşteriye açık sayfalardan planı gizlemek için devre dışı bırakın (mevcut abonelerin devam ettiği içi veya eski planlar için faydalıdır).

## İpuçları

- **Deneme süresi** kullanarak tereddütü azaltın - hatta 7 günlük ücretsiz bir deneme süresi bile abonelik ürünlerinde dönüşüm oranlarını显著 artırmada faydalıdır.
- **Üç fiyat seviyesi** (aylık, çeyreklik, yıllık) oluşturun ve yıllık taahhütlere ve nakit akışınızı artırmanıza yardımcı olmak için artan indirimlerle birlikte sunun.
- Hizmet temelli abonelikler için, **İptal Politikası**'nı **Dönem Sonunda İptal** olarak ayarlayın, böylece müşterileri ödeme dönemlerine kadar erişime devam etsin - bu adil hissi verir ve iade oranlarını azaltır.
- Ödeme hataları için **İzinli Dönem**'i 3-7 gün olarak ayarlayın. Bu, erişim kaybetmeden önce müşteriye ödeme yöntemini güncellemek için zaman tanır.
- Ekstra hizmetler için **Gerekli** bandını seyrek kullanın - sadece gerçekten zorunlu olanlar (örneğin, bir hizmet sözleşmesi) için kullanın, fiyatları artırmak için bir yol olarak kullanmayın.
- Aboneliği olmayan planları silmek yerine devre dışı bırakın - bu, daha önce abone olan müşteriler için tarihsel veri korur.