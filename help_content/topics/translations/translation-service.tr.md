---
title: Çeviri Hizmeti
---

Çeviri hizmeti, mağazanızın ürün açıklamaları, sayfa içerikleri, blog gönderileri, SEO alanları ve diğer satıcı içerikleri için yapay zeka destekli çeviriler sağlar. Çeviriler yerel sunucunuzda veya harici sağlayıcılara üzerinden çalışır, bu nedenle içerikleriniz özel kalır ve çeviriler saniyeler içinde gerçekleşir.

![Dil yönetimi](/static/core/admin/img/help/translation-service/language-management.webp)

## Nasıl Çalışır

1. Mağazanız için **dilleri etkinleştirin** (örneğin, İngilizce, Almanca, Japonca)
2. İçerik oluştururken veya düzenlerken (ürünler, sayfalar, blog gönderileri), varsayılan dilinizde yazın
3. Çevrilebilir herhangi bir alanda **Çevir** butonuna tıklayarak aktif dillerinize yapay zeka çevirileri oluşturun
4. Çeviriler orijinal içerikle birlikte saklanır ve ziyaretçinin diline göre otomatik olarak sunulur

## Dilleri Yönetme

Mağazanızın dillerini yönetmek için **Ayarlar > Diller** bölümüne gidin.

### Dil Panosu

Panoda aşağıdaki bilgiler gösterilir:
- **Toplam Diller** — Sistemde mevcut tüm diller (100+)
- **Etkin Diller** — Şu anda mağazanız için etkin olan diller
- **Model Kapsamı** — Yüklü çeviri modelinin hangi dilleri desteklediği

### Dil Etkinleştirme

1. **Mevcut Diller** sütununda dilinizi bulun
2. Dili seçerek **Etkin Diller** sütununa taşıyın
3. Dil, çeviri için hemen kullanılabilir hale gelir ve mağazanızın dil geçişçisinde görünür

### Varsayılan Dil

Bir dil **varsayılan** olarak işaretlenir. Bu:
- İçerik yazmak için kullandığınız dil
- Çeviri bulunamadığında varsayılan dil
- Ziyaretçiler bir tercih seçmediklerinde gösterilen dil

## Çeviri Modelleri

Spwig, tüm işlemi yerel sunucunuzda çalışan bir yapay zeka çeviri motoru içerir — harici hizmetlere veri gönderilmez.

### Mevcut Modeller

| Model | Diller | Hız | Kalite |
|-------|-----------|-------|---------|
| **M2M100-418M** | 100 | Hızlı | Ortak dil çiftleri için iyi |
| **M2M100-1.2B** | 100 | Orta | Daha iyi kalite, daha yüksek kaynak kullanımı |
| **NLLB-200** | 200+ | Orta | En kapsamlı, nadir diller dahil |

### Model Seçimi

Dil yönetimi sayfası, hangi modelin yüklendiğini ve dil kapsamlarını gösterir. Model, CTranslate2 kullanarak yerel bir hizmet olarak çalışır ve verimli çıkarım için optimize edilmiştir.

## Harici Sağlayıcılar

Bulut tabanlı çeviri tercih eden veya belirli dil kalitesi gerekli olan mağazalar için Spwig, harici çeviri sağlayıcılarını destekler.

| Sağlayıcı | Açıklama |
|----------|-------------|
| **DeepL** | Avrupa ve Asya dilleri için premium çeviri kalitesi |
| **Google Translate** | Nöral makine çevirisi ile geniş dil kapsamları |
| **Azure Translator** | Microsoft'un nöral çeviri hizmeti |
| **AWS Translate** | Amazon'un özel terimler desteğiyle makine çevirisi |

### Sağlayıcıyı Bağlama

1. **Ayarlar > Çeviri Sağlayıcıları** bölümüne gidin
2. Sağlayıcıyı seçin ve API anahtarınızı girin
3. Sağlayıcıyı tercih edilen çeviri motoru olarak ayarlayın
4. Çeviriler, yerel model yerine harici sağlayıcıyı kullanır

Harici sağlayıcıları yerel model ile birlikte kullanabilirsiniz — örneğin, Avrupa dilleri için DeepL kullanın ve diğer tüm diller için yerel modeli kullanın.

## İçerik Çevirisi

### Alan Seviyesi Çeviri

Çevrilebilir alanlar (ürün isimleri, açıklamalar, SEO başlıkları vb.) alanın yanına bir **çeviri butonu** gösterir. Tıklayınca:

1. **Tüm etkin dillere çevir** — Her bir etkin dil için bir kere tüm çevirileri oluşturur
2. **Belirli bir dile çevir** — Çevirmek istediğiniz bireysel dilleri seçin

Çeviriler, düzenleyicideki dil sekmelerinde görünür. Makine çevirilerini inceleyebilir ve herhangi bir makine çeviriyi elle düzenleyebilirsiniz.

### Toplu Çeviri İşleri

Büyük miktarda içerik için **çeviri işleri** kullanın:

1. **Ayarlar > Çeviri İşleri** bölümüne gidin
2. Yeni bir iş oluşturun ve aşağıdaki seçenekleri seçin:
   - **İçerik türü** — Ürünler, sayfalar, blog gönderileri, kategoriler vb.
   - **Kaynak dili** — Çeviri yapılacak dil
   - **Hedef diller** — Çeviri yapılacak bir veya daha fazla dil
   - **Kapsam** — Tüm içerik veya yalnızca çevrilmemiş alanlar
3. İşi gönderin — Arka planda bir görev kuyruğu üzerinden çalışır
4. İş listesinde ilerlemeyi izleyin (kuyruğa alındı → işleniyor → tamamlandı)

Toplu işler, yeni bir dil etkinleştirdiğinizde ve tüm kataloğunuzu bir seferde çevirmek istiyorsanız yararlıdır.

## Çeviri Yönetimi

### Çevirileri İnceleme

Her çevrilen alan aşağıdaki bilgileri izler:
- **Çeviri durumu** — Alanın makine çevirisiyle çevrildiğine, elle düzenlendiğine veya eksik olduğuna dair bilgi
- **Kilit durumu** — Kilitli çeviriler gelecekteki makine çevirileri tarafından geçersiz kılınmaz
- **Son çeviri zamanı** — Çevirinin son kez oluşturulduğu veya düzenlendiği zaman

### Çevirileri Kilitleme

Makine çevirilerini elle düzenleyerek daha iyi hale getirdiyseniz, **kilitleyin** alanın, toplu çeviri çalıştırıldığında yeniden yazılmasını önlemek için. Kilitli alanlar, otomatik çeviri sırasında atlanır.

### Çeviri Kapsamı

Kapsam izleyici, her dil için içeriklerinizin ne kadarının çevrildiğini gösterir. **Ayarlar > Diller** bölümüne giderek aşağıdaki bilgileri görebilirsiniz:
- Dil bazlı tamamlanma yüzdelikleri
- Hangi içerik türlerinde boşluklar var
- Hâlâ çevrilmesi gereken alanlar

## Kullanıcı Arayüzü Çeviri Üstünlüğüleri

Ürün ve sayfa içeriklerinin ötesinde, **ön uç arayüz dizelerini** özelleştirebilirsiniz — düğmeler, etiketler, mesajlar ve ziyaretçilere gösterilen diğer kullanıcı arayüzü metinleri.

**Ayarlar > Kullanıcı Arayüzü Üstünlükleri** bölümüne giderek:
1. Belirli bir dizeyi arayın (örneğin, "Sepete Ekle")
2. Her dil için tercih ettiğiniz çeviriyi girin
3. Kaydedin — üstünlük hemen etkinleşir

Özelleştirmek için yaklaşık 300 ön uç dizesi mevcuttur. Üstünlükler, varsayılan çevirilerden önceliklidir.

## İpuçları

- İlk olarak, müşterilerin gerçekten kullandığı dilleri etkinleştirin — daha sonra her zaman daha fazlasını ekleyebilirsiniz.
- Günlük çeviriler için **yerel yapay zeka modelini** kullanın — hızlı, özel ve her çeviri için ücret yoktur.
- Ana Avrupa dilleri için en yüksek kalite gerekirse **DeepL**'i düşünün — genel modellerden daha doğal çeviriler üretir.
- Ürün isimlerini, marka terimlerini ve pazarlama metnini her zaman **makine çevirilerini inceleyin** — yapay zeka teknik içerikleri iyi işler ancak yaratıcı metinlerde incelemeyi kaçırabilir.
- Manuel olarak düzeltilmiş herhangi bir çeviriyi **kilitleyin** — toplu çeviri işlerinin sırasında yeniden yazılmasını önlemek için.
- Yeni bir dil etkinleştirdiğinizde **toplu çeviri işlerini** kullanın — tüm kataloğunuzu tek bir geçişte çevirmek yerine ürünlerinizi tek tek çevirmek yerine.
- Markanızın sesini eşleştirmek için **kullanıcı arayüzü üstünlüklerini** özelleştirin — örneğin, "Sepete Ekle"yi "Şimdi Satın Al" olarak değiştirin, eğer mağazanız için daha uygundur.

