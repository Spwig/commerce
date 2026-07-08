---
title: Abonelik Planları
---

Abonelik planları, ürünleriniz için tekrar eden faturalandırma sunmanıza olanak tanır — tüketim ürünlerleri, hizmetler, özelleştirilmiş kutular veya müşterilerin tekrar tekrar satın aldığı herhangi bir ürün için idealdir. Bu kılavuz, planları oluşturma ve yapılandırma, fiyatlandırma katmanlarını ayarlama, deneme dönemleri ekleme ve isteğe bağlı eklentiler eklemeyi açıklar.

## Başlangıç

**Abonelikler > Abonelik Planları** menüsünü admin yan çubuğundan seçin. Plan listesi, tüm planlarınıza ait fiyatlandırma modelini, aktif aboneyi sayısını ve görünür durumunu gösterir.

Yeni bir plan oluşturmak için **+ Abonelik Planı Ekle** butonuna tıklayın — bu, plan oluşturma asistanını açar ve kurulumu adım adım size rehberlik eder.

![Abonelik planları listesi](/static/core/admin/img/help/subscription-plans/plan-list.webp)

## Plan bilgisi

İlk bölüm, planınızın temel kimliğini yakalar.

- **Plan Adı** — Müşterilerin abone olurken gördüğü ad. Diğer mağaza dilleri için çeviri eklemek için dünya simgesine tıklayın.
- **Slug** — Adından otomatik olarak oluşturulan URL dostu bir tanımlayıcı (örneğin, `premium-plan`). İçeride ve entegrasyonlarda kullanılır.
- **Açıklama** — Planın ne içerdiğini açıklayan isteğe bağlı metin. Çevirilere destek sağlar.

## Fiyatlandırma modeli

Bu plan için fiyatlandırma nasıl yapılandırılacağını seçin:

| Fiyatlandırma Modeli | En Uygun Kullanım Alanı |
|----------------------|------------------------|
| **Katmanlı Fiyatlandırma** | Aylık, çeyreklik ve yıllık taahhüt seçeneklerini sunmak ve daha uzun süreler için indirimler sunmak |
| **Miktar Temelli** | Kişilik veya kullanıcı başına fiyatlandırma, toplam miktar miktarı ile ölçeklendirilir (örneğin, ekip lisansları) |
| **Düz Fiyat** | Değişmeyen tek bir fiyat |

**Miktar Temelli** planlar için **Minimum Miktar** (gereken minimum koltuk sayısı) ve isteğe bağlı olarak **Maksimum Miktar** (aboneyin satın alabileceği maksimum koltuk sayısını sınırlamak için) ayarlayın.

## Fiyatlandırma katmanları

Fiyatlandırma katmanları, bu plana abone olan müşterilere sunulan faturalandırma sıklığı ve indirim seçeneklerini tanımlar. Ana formun altındaki **Fiyatlandırma Katmanları** bölümünden ekleyin.

Her katman şu alanlara sahiptir:

- **Katman Adı** — Müşterilere gösterilen etiket (örneğin, `Aylık`, `Yıllık — %20 İndirim`). Çevirilere destek sağlar.
- **Faturalandırma Döngüsü** — Müşterinin ne sıklıkta faturalandırıldığı: Günlük, Haftalık, Aylık, Çeyreklik, Yarı-Yıllık veya Yıllık.
- **Faturalandırma Aralığı** — Faturalandırma döngüsünün katlayıcısı. Aylık olarak `2` ayda bir faturalandırmak için `2` olarak ayarlayın.
- **İndirim Yüzdesi** — Bu katman için ürün fiyatına uygulanan indirim. `0` olarak ayarlayarak tam fiyat, `20` olarak ayarlayarak %20 indirim yapın. Bu indirim, ürünün kendisindeki herhangi bir satış fiyatına eklenir.
- **Varsayılan Katman** — Müşterilerin abonelik seçeneklerini görüntülediğinde öntanımlı olarak seçili olan bir katman olarak işaretleyin.

### Örnek: üç seçeneği olan katmanlı plan

"Kahve Kulübü" abonelik planı için:

| Katman Adı | Faturalandırma Döngüsü | İndirim |
|------------|------------------------|--------|
| Aylık | Aylık | 0% |
| Çeyreklik — %10 İndirim | Çeyreklik | 10% |
| Yıllık — %20 İndirim | Yıllık | 20% |

## Deneme Dönemi

Deneme dönemi, müşterilerin ilk tam ödeme öncesi aboneliklerini denemelerine olanak tanır. Bu, **Deneme Dönemi** bölümünde yapılandırılabilir:

- **Deneme Dönemi (Gün)** — Ücretsiz deneme gün sayısı. `0` olarak ayarlayarak denemeleri devre dışı bırakın. Maksimum 365 gün.
- **Deneme Fiyatı** — Deneme sırasında uygulanan indirilmiş fiyat (örneğin, ilk ay için $1). Tamamen ücretsiz bir deneme için boş bırakın.

## İptal Politikası

Müşterilerin aboneliklerini nasıl iptal edebileceğini **İptal Politikası** bölümünde kontrol edin:

| Politika | Açıklama |
|----------|----------|
| **Her Zaman İptal Et** | Müşteriler herhangi bir zaman anında hemen iptal edebilir |
| **Ödeme Dönemi Sonunda İptal Et** | İptal, ödenen dönemin sonunda etkin olur — müşteriler, sona erene kadar erişime devam eder |
| **Minimum Taahhüt Gereklidir** | Müşteriler, iptal etmeden önce minimum sayıda faturalandırma döngüsünü tamamlamak zorundadır |

Ek ayarlar:

- **Minimum Commitment (Cycles)** — Taahhüt politikasını kullanırken, gerekli fatura döngü sayısını belirleyin (örneğin, 3 aylık minimum için `3`).

- **Grace Period (Days)** — Abonelik askıya alınmadan önce bir ödemede başarısızlık yaşanması durumunda devam eden erişim gün sayısı.

`0` olarak ayarlayarak hemen askıya alma.

- **Reactivation Period (Days)** — İptal sonrası, müşteri aboneliğini baştan abone olmadan yeniden etkinleştirebileceği gün sayısı.

## Plan değişiklik davranışı

Müşteriler planlar arasında yükseltme veya düşürme yaparsa, değişikliğin ne zaman etkinleşeceğini kontrol edebilirsiniz:

- **Upgrade Behavior** — **Immediate** (şimdilik prorated miktarı tahsil et) veya **At Renewal** (bir sonraki fatura tarihinde geçiş yap) olarak ayarlayın.

- **Downgrade Behavior** — **Immediate** (bir sonraki faturaya kredi uygula) veya **At Renewal** (bir sonraki fatura tarihinde geçiş yap) olarak ayarlayın.

## Sınırlar ve kısıtlamalar

- **Maximum Billing Cycles** — Abonelik otomatik olarak sona ermeden önceki toplam fatura döngü sayısı. Sınırsız tekrarlı fatura için boş bırakın. Taksit planları veya zaman sınırlı abonelikler için kullanışlıdır.

- **Setup Fee** — Abonelik ilk oluşturulduğunda toplanan tek seferlik ücret (örneğin, onboarding veya etkinleştirme ücreti). Kurulum ücreti olmaması için `0.00` olarak ayarlayın.

## Plan eklentileri

Eklentiler, abonelerin planlarına ekleyebilecekleri isteğe bağlı ekstra öğelerdir. Onları **Plan Eklentileri** bölümünde ekleyin:

- **Add-on Name** — Müşterilere gösterilen isim. Çevirileri destekler.

- **Description** — Eklenti ne sağlar.

- **Price** — Eklentinin maliyeti.

- **Billing Frequency** — Eklentinin **Per Billing Cycle** (tekrar eden) olarak ücretlendirilip ücretlendirilmediğini veya abonelik başlangıcında **One-Time** olarak ücretlendirilip ücretlendirilmediğini belirtir.

- **Allow Quantity** — Müşterilerin eklentinin birden fazla birimini satın almasına izin vermek için etkinleştirin.

- **Required** — Tüm yeni aboneliklerde eklentinin otomatik olarak dahil edilmesi için işaretleyin. Gerekli eklentiler müşteri tarafından kaldırılamaz.

## Görünürlük ve durum

- **Active** — Yeni aboneliklerin oluşturulmasını önlemek için işaretini kaldırın. Mevcut abonelikler etkilenmez.

- **Public** — Müşteri odaklı sayfalardan planı gizlemek için işaretini kaldırın (mevcut abonelerin üzerinde kaldığı iç veya eski planlar için faydalıdır).

- **Sort Order** — Abonelik seçim sayfalarında görüntü sırasını kontrol eder. Düşük numaralar önce görünür.

## İpuçları

- **Deneme süresi** kullanarak tereddütleri azaltın — kısa bir 7 günlük ücretsiz deneme, abonelik ürünlerinde dönüşüm oranlarını önemli ölçüde artırabilir.

- Artan indirimlerle **üç fiyatlandırma katmanı** (aylık, çeyreklik, yıllık) oluşturun, yıllık taahhütleri teşvik edin ve nakit akışınızı iyileştirin.

- Hizmet tabanlı abonelikler için **Cancellation Policy** (İptal Politikası)’ni **Cancel at Period End** (Dönem Sonunda İptal Et) olarak ayarlayın, böylece müşteriler ödemeleri süresince erişimini korur — bu adil gibi görünür ve iade taleplerini azaltır.

- Ödeme başarısızlıklarında **Grace Period**’ı 3–7 gün olarak tutun. Bu, müşterilere erişimi kaybetmeden önce ödeme yöntemlerini güncellemeleri için zaman sağlar.

- Eklentilerde **Required** bayrağını az kullanın — sadece gerçekten zorunlu olan şeylere (örneğin, bir hizmet anlaşması) uygulayın, fiyat artışını artırmak için değil.

- Aboneliği olmayan planları silmek yerine devre dışı bırakın — bu, önce abone olan müşteriler için tarihsel veriyi korur.