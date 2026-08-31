---
title: Abonelik Planları
---

Abonelik planları, ürünleriniz için tekrarlayan faturalandırma sunmanıza olanak tanır. Bu, tüketilebilir ürünler, hizmetler, özel kutular veya müşterilerin tekrar tekrar satın aldıkları herhangi bir ürün için idealdir. Bu kılavuz, planlar oluşturmayı ve yapılandırmayı, fiyatlandırma seviyelerini ayarlamayı, deneme dönemleri eklemeyi ve isteğe bağlı ekstra bileşenler eklemeyi anlatır.

## Başlarken

Yönetim yan panelinde **Abonelikler > Abonelik Planları**'na gidin. Plan listesi, fiyatlandırma modeliniz, aktif abone sayısı ve erişim durumu ile tüm planlarınızı gösterir.

![Abonelik planları listesi](/static/core/admin/img/help/subscription-plans/plan-list.webp)

Yeni bir plan oluşturmak için **Sihirbazla Oluştur** butonuna tıklayın — bu, plan oluşturma sihirbazını açar ve kurulumu adım adım size götürür. Bunun yanında bulunan **+ Plan Ekle** butonu, sihirbaz yerine tüm özellikleri elle yapılandırmayı tercih eden satıcılar için boş bir form açar.

Bir plan, kendi başına satın alınamaz — bir şablondur. Burada oluşturduğunuz planı, müşterilerin gerçekten abone olabilmesi için ürünün **Abonelikler** sekmesinden (Sadece, Değişken ve Dijital ürünler) bir veya daha fazla ürüne ekleyin. Bu adımı yapmak için [Ürünleri Abonelik Olarak Satma](/help/selling-products-as-subscriptions) sayfasına bakın.

## Plan düzenleyicisi

Listeden bir planı açmak (ismini veya kaleme alım ikonunu tıklayarak) plan düzenleyicisine gider. Başlık, plan adını, fiyatlandırma modelini, **Aktif**/**Pasif** ve **Kamu**/**Kamu Olmayan** durum badajlarını ve ne zaman oluşturulduğunu gösterir. Başlıkta sağ üst köşedeki iki buton, değişikliklerinizi kaydeder — check-circle simgesi, listeye dönmek için kaydeder, düz check simgesi, sayfada kalmak için kaydeder ve devam eder.

Başlıktan sonra, planın kısa özetini gösteren bir istatistik şeridi vardır: **Aktif Abonelikler**, **Fiyatlandırma Seviyeleri**, **Ekstra Bileşenler** ve **Toplam Gelir**.

Formun geri kalanı beş sekme göre düzenlenmiştir:

| Sekme | Ne içerir | 
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
- **Açıklama** — Planın ne içerdiğini tanımlayan isteğe bağlı metin. Çevirilere izin verir.

Aynı sekmedeki **Durum** kartı, **Aktif** ve **Kamu** anahtarlarını kontrol eder — aşağıda ki [Erişilebilirlik ve Durum](#visibility-and-status) bölümüne bakın.

![Plan düzenleyicisinin Genel sekmesi](/static/core/admin/img/help/subscription-plans/edit-form-general-tab.webp)

## Fiyatlandırma Modeli (Fiyatlandırma sekmesi)

**Fiyatlandırma Yapılandırması** kartı, bu plan için fiyatlandırma yapısını kontrol eder:

| Fiyatlandırma Modeli | En Uygun Olan | 
|---------------|----------| 
| **Seviyeli Fiyatlandırma** | Uzun vadeli anlaşmalar için aylık, çeyreklik ve yıllık seçenekler sunar ve daha uzun süreler için indirimler | 
| **Miktar Temelli** | Toplamın miktarla ölçeklendiği (örneğin, ekip lisansları) koltuk veya kullanıcı bazlı fiyatlandırma | 
| **Düz Seviye** | Herhangi bir değişiklik olmayan tek bir sabit fiyat | 

**Miktar Temelli** planlar için **Miktarı Aç** ve **Minimum Miktar**'ı (gereken koltuk sayısı) ayarlayın ve isteğe bağlı olarak **Maksimum Miktar**'ı belirleyin — bir abonelinin satın alabileceği koltuk sayısını sınırlayın.

Tüm markdown formatlamalarını, resim yollarını, kod bloklarını ve teknik terimleri koruyun.

[![](https://spwig.com/static/core/admin/img/help/subscription-plans/edit-form-pricing-tab.webp)](/static/core/admin/img/help/subscription-plans/edit-form-pricing-tab.webp)

## Fiyatlandırma seviyeleri (Seviyeler & Ek Bölümler sekmesi)

Fiyatlandırma seviyeleri, bu plan üzerinde müşterilere sunulan faturalandırma sıklığı ve indirim seçeneklerini tanımlar. Ekleyin **Fiyatlandırma Seviyeleri** kartında **Seviyeler & Ek Bölümler** sekmesinde, ek bölümler editöründe birlikte.

Her seviye şu alanlara sahiptir:

- **Seviye Adı** — Müşterilere gösterilen etiket (örneğin, `Aylık`, `Yıllık — %20 Kazanın`). Çevirilere uygun.
- **Faturalandırma Döngüsü** — Müşterinin ne sıklıkla faturalandırıldığını gösterir: Günlük, Haftalık, Aylık, Çeyreklik, Yarıyıllık veya Yıllık.
- **Faturalandırma Aralığı** — Faturalandırma döngüsü için çarpan. Aylık olarak `2` olarak ayarlanırsa, 2 ayda bir faturalandırılır.
- **İndirim Yüzdesi** — Bu seviye için ürün fiyatına uygulanan indirim. Tam fiyat için `0` olarak ayarlayın, ya da %20 indirim için `20` ayarlayın. Bu indirim, ürünün kendisindeki herhangi bir satış fiyatına ek olarak biriktirilir.
- **Varsayılan Seviye** — Müşterilerin abonelik seçeneklerini görüntülediğinde bunu önceden seçmek için bir seviyeyi vurgulayın.

İndirim, sadece yeniden imzalamalarda değil, müşteriye ait ilk faturalandırma döngüsünden itibaren geçerlidir — %20 indirimli bir seviye, ilk faturalandırma döngüsünden itibaren (ya da planın bir deneme süresi varsa, deneme süresinden sonraki ilk faturalandırma döngüsünden itibaren) %20 indirimli olarak çalışır.

### Örnek: Üç seçenekli seviyeli plan

"Kahve Kulübü" abonelik planı için:

| Seviye Adı | Faturalandırma Döngüsü | İndirim |
|-----------|-------------------|----------|
| Aylık | Aylık | %0 |
| Çeyreklik — %10 Kazanın | Çeyreklik | %10 |
| Yıllık — %20 Kazanın | Yıllık | %20 |

## Plan ekleri (Seviyeler & Ek Bölümler sekmesi)

Ekler, abonelerin planlarına ekleyebilecekleri isteğe bağlı ekstra unsurlardır. Aynı sekmedeki **Fiyatlandırma Seviyeleri** kartının hemen altında bulunan **Ekler** kartında ekleyin:

- **Ek Adı** — Müşterilere gösterilen isim. Çevirilere uygun.
- **Açıklama** — Ekstra ne sunar.
- **Fiyat** — Ekstra için maliyet.
- **Faturalandırma Sıklığı** — Ekstra, **Faturalandırma Döngüsüne Göre** (tekrarlayan) ya da **Bir Kere** abonelik başlangıcında faturalandırılır.
- **Miktarı Kabul Et** — Müşterilerin ekstra birimlerinin sayısını satın almasına izin vermek için etkinleştirin.
- **Zorunlu** — Tüm yeni aboneliklerde ekstra eklemek için bu seçeneği işaretleyin. Zorunlu ekler, müşteri tarafından kaldırılamaz.

[![](https://spwig.com/static/core/admin/img/help/subscription-plans/edit-form-tiers-addons-tab.webp)](/static/core/admin/img/help/subscription-plans/edit-form-tiers-addons-tab.webp)

## Deneme süresi (Fiyatlandırma sekmesi)

Bir deneme süresi, müşterilere ilk tam faturalandırma öncesi aboneliklerini denemelerini sağlar. **Fiyatlandırma Yapılandırması** altındaki **Deneme Süresi** kartında yapılandırın:

- **Deneme Süresi (Gün)** — Ücretsiz deneme günleri sayısı. Denemeleri devre dışı etmek için `0` olarak ayarlayın. Maksimum 365 gündür.
- **Deneme Fiyatı** — Deneme süresindeki indirimsiz fiyat (örneğin, ilk ay için $1). Tamamen ücretsiz bir deneme için boş bırakın.

## Sınırlar ve kısıtlamalar (Fiyatlandırma sekmesi)

**Sınırlar & Kısıtlamalar** kartı, aynı zamanda Fiyatlandırma sekmesinde de bulunur ve şu bilgileri içerir:

- **Maksimum Faturalandırma Döngüsü Sayısı** — Abonelik otomatik olarak biteceği toplam faturalandırma döngüsü sayısı. Sınırsız tekrarlayan faturalandırma için boş bırakın. Taksit planları ya da zaman sınırlı abonelikler için yararlıdır.

**Kurulum Ücreti** ve **Sıralama Sırası**, bu kartın bir parçası değildir — bu değerler, **Yaratma Sihirbazı** akışı aracılığıyla ilk kez planı yaratırken ayarlanır ve daha sonra düzenleme ekranından değiştirilemez. Bu değeri değiştirmeniz gerekirse, planı devre dışı bırakın ve sihirbaz aracılığıyla yeniden oluşturun, mevcut planı düzenlemek yerine. Kurulum ücretlerinin bu sürümdeki alışveriş sırasında otomatik olarak tahsil edilmediğini not edin — bu alanı gelecekteki bir güncelleme için ayrılmış bir alan olarak düşünün, çalışan bir ücret olarak değil.

## İptal politikası (Yaşam döngüsü sekmesi)

**İptal Politikası** kartında, müşterilerin aboneliklerini nasıl iptal edebileceğini kontrol edin:

{
  "Policy": "Amaç",
  "Description": "Açıklama",
  "**Cancel Anytime**": "Müşteriler, herhangi bir zaman anında iptal edilebilir",
  "**Cancel at Period End**": "İptal, ödemeli dönemin sonunda geçerli olur - müşteriler, süresi dolana kadar erişime devam eder",
  "**Minimum Commitment Required**": "Müşterilerin iptal etmeden önce minimum sayıda faturalandırma döngüsünü tamamlaması gerekir",
  "Additional settings": "Ek ayarlar",
  "- **Minimum Commitment (Cycles)**": "- **Minimum Taahhüt (Döngüler)** - Taahhüt politikası kullanırken, faturalandırma döngülerinin (örneğin, 3 aylık minimum için `3`) sayısını ayarlayın.",
  "- **Grace Period (Days)**": "- **Göreve Dönüklük Süresi (Gün)** - bir ödeme başarısızlığından sonra abonelik devre dışı bırakılmadan önce devam eden erişim günleri. Hemen devre dışı etmek için `0` ayarlayın.",
  "- **Reactivation Period (Days)**": "- **Yeniden Aktivasyon Süresi (Gün)** - bir müşterinin aboneliğini yeniden aktif hale getirebileceği, yeniden abone olmadan önceki an."
}

## Plan değişimi davranışı (Yaşam döngüsü sekmesi)

**Plan Değişim Davranışı** kartı, müşteriler planlar arası geçiş yaparken ne olacağını kontrol eder:

- **Yükseltme Davranışı** - Şu anki indirimli tutarı tahsil etmek için **Ani** (prorated miktarı şimdi tahsil) veya **Yeniden Yükleme** (bir sonraki faturalandırma tarihinde değiştirme) olarak ayarlayın.
- **Aşağılama Davranışı** - Şu anki sonraki faturaya kredi uygulamak için **Ani** (prorated miktarı şimdi tahsil) veya **Yeniden Yükleme** (bir sonraki faturalandırma tarihinde değiştirme) olarak ayarlayın.

![Plan düzenleyicisinin Yaşam döngüsü sekmesi](/static/core/admin/img/help/subscription-plans/edit-form-lifecycle-tab.webp)

## Gelişmiş sekme

**Gelişmiş** sekmesi, günlük hayatta nadiren ihtiyaç duyduğunuz ayarları içerir:

- **Sağlayıcı Entegrasyonu** - Bu planı, mağazanızın sağlayıcı aracılığıyla abonelikleri doğrudan yönettiği yerde plan/fiyat kimliklerine haritalayın (örneğin, `{"stripe": "price_xxx", "paypal": "P-xxx"}`).
- **İstatistikler** - **Aktif Abonelikler**, **Toplam Gelir** ve planın **Oluşturulma Zamanı** / **Güncellenme Zamanı** zaman damgaları dahil olmak üzere, sadece okunur rakamlar. Bu, sayfanın en üstündeki istatistik şeridindeki istatistikleri yansıtır.

![Plan düzenleyicisinin Gelişmiş sekmesi](/static/core/admin/img/help/subscription-plans/edit-form-advanced-tab.webp)

## Görünürlük ve durum (Genel sekme)

- **Aktif** - Yeni aboneliklerin oluşturulmasını engellemek için planı devre dışı bırakın. Zaten mevcut abonelikler etkilenmez.
- **Kamuya açık** - Müşteriye açık sayfalardan planı gizlemek için devre dışı bırakın (mevcut abonelerin devam ettiği içi hizmet planları gibi içsel veya eski planlar için yararlıdır).

## İpuçları

- **Deneme süresi** kullanarak tereddütü azaltın - hatta 7 günlük ücretsiz bir deneme bile, abonelik ürünlerinde dönüşüm oranlarını显著 bir şekilde artırabilir.
- **Üç fiyat seviyesi** (aylık, çeyreklik, yıllık) oluşturun ve yıllık taahhütlere teşvik etmek ve nakit akışınızı artırarak artan indirimlerle birlikte kullanın.
- Hizmet temelli abonelikler için, **İptal Politikası**'nı **Dönem Sonunda İptal** olarak ayarlayın, böylece müşterileri ödeme süresi boyunca erişime devam etsin - bu adil hissettirir ve iade oranlarını azaltır.
- Ödeme hatalarında **Göreve Dönüklük Süresi**'ni 3-7 gün olarak ayarlayın. Erişim kaybetmeden önce müşteriye ödeme yöntemini güncellemesi için zaman tanır.
- Ekstra birimlerde **Gerekli** işaretini dikkatle kullanın - sadece gerçekten zorunlu olanlar (örneğin, bir hizmet sözleşmesi) için kullanın, fiyatları artırmak için bir yol olarak kullanmayın.
- Aboneliği olmayan planları silmek yerine devre dışı bırakın - bu, daha önce abone olan her müşteri için tarihsel veri korur.

Tüm markdown formatlamalarını, resim yollarını, kod bloklarını ve teknik terimleri koruyun.