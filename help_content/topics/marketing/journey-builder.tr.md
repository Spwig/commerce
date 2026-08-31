---
title: Journey Builder
---

<!-- screenshots-needed:
- url: /admin/campaigns/journeys/  (open any journey's builder, click Templates)
  filename: journey-builder-templates.webp
  description: The template picker with all eight starters visible (Welcome series,
    First-order onboarding, Post-purchase & review, VIP vs. standard offer, Abandoned
    cart recovery, Win-back lapsed customers, Post-delivery review request,
    Back-in-stock alert) — replaces the existing four-template screenshot at the same
    path, which is now stale.
  save-to: core/static/core/admin/img/help/journey-builder/
  viewport: 1440x900
-->

**Journey Builder**, bir [Journey](/help/triggered-journeys)'ın ne yaptığını tasarladığınız görsel, sürükle-bırak tuvalidir — hangi e-postaların gönderileceği, aralarında ne kadar beklenmesi gerektiği ve farklı abonelerin farklı yolları izleyip izlemeyeceği. Bir form doldurmak yerine, akışı bir akış şeması olarak oluşturursunuz: yeniden düzenleyebileceğiniz, dallandırabileceğiniz ve bir bakışta önizleyebileceğiniz, tuval üzerinde birbirine bağlı kutular.

## Oluşturucuyu açma

Her journey'in kendi oluşturucu tuvali vardır. Bunu iki yolla erişebilirsiniz:

- Yeni bir journey oluşturma — ayarlar sayfasında **Ad**, **Tetikleyici** ve hedef kitleyi doldurup **Kaydet**'e tıkladığınızda, hemen tasarıma başlayabilmeniz için doğrudan oluşturucuya yönlendirilirsiniz.
- Mevcut bir journey'in ayarlar sayfasını açıp üst kısımdaki **Journey'i tasarla** seçeneğine tıklama.

Oluşturucu, üç alana sahip tam ekran bir çalışma alanıdır: solda adım türlerini içeren bir **palet**, ortada **tuval** ve bir şey seçtiğinizde sağda beliren bir **adım ayarları** paneli.

![Yes/No dallanması olan bir hoş geldiniz serisini gösteren Journey Builder tuvali](/static/core/admin/img/help/journey-builder/journey-builder-canvas.webp)

Tuvalin üst kısmında, journey'in **Tetikleyicisi** ve **hedef kitlesi** (segment ayarlanmadıysa "Tüm aboneler") tekrarlanır, böylece oluşturucudan ayrılmadan kimin için tasarladığınızı her zaman bilirsiniz. Journey'in ayarlar sayfasına dönmek için **Geri** düğmesini kullanın.

## Adım türleri

Bir adımı sol paletten tuvale sürükleyin veya palet öğesine tıklayarak otomatik olarak yerleştirin. Dört adım türü mevcuttur:

| Adım | Ne yapar |
|------|--------------|
| **E-posta gönder** | Aboneye kampanyalarınızdan birini gönderir. |
| **Bekle** | Devam etmeden önce belirli bir saat veya gün sayısı kadar duraklatır. |
| **Dallan** | Seçtiğiniz bir segmente abonenin ait olup olmadığına göre yolu ikiye böler — **Evet** veya **Hayır**. |
| **Çıkış** | Abone için journey'i sonlandırır. |

Her journey, oluşturucuyu ilk kez açtığınızda otomatik olarak oluşturulan tek bir **Giriş** adımıyla başlar. Journey'in tetikleyicisini gösterir ve silinemez — yalnızca abonelerin akışa girdiği yerdir.

## Adımları bağlama

Her adımın küçük dairesel bir **portu** vardır: üstte bir tane (giriş) ve altta bir veya daha fazla (çıkış). İki adımı bağlamak için, bir adımın alt portundan diğer adımın üst portuna sürükleyin — onları birbirine bağlayan kıvrımlı bir çizgi görünür.

Bir **Dallan** adımının bir yerine iki çıkış portu vardır: yeşil bir **Evet** ve kırmızı bir **Hayır**. Her birini o yolun gitmesi gereken yere bağlayın — daha sonra aynı adımda yeniden birleşebilirler (yukarıdaki örnekte olduğu gibi, her iki yol da aynı **Çıkış**a geri döner) veya tamamen ayrı yollar izleyebilirler.

Düzeni yeniden düzenlemek için, bir adımı gövdesinden sürükleyerek konumunu değiştirin — bağlı çizgiler otomatik olarak takip eder. Tuval arka planının boş bir kısmını sürükleyerek etrafında gezinme yapın ve fare tekerleğinizi yakınlaştırmak veya uzaklaştırmak için kullanın. Akışı kaybederseniz, her şeyi ekrana sığdırmak için yeniden ortalamak ve yakınlaştırmak için araç çubuğundaki **Sığdır**'a tıklayın.

## Bir adımı yapılandırma

Ayarlarını sağdaki panelde açmak için herhangi bir adıma tıklayın:


| Adım | Ayar |
|------|---------|
| **E-posta gönder** | Kampanyalarınızın açılır menüsünden **Gönderilecek e-posta** seçin. |
| **Bekle** | **Bekleme süresi** — bir sayı ve **saat** veya **gün** belirleyin. |
| **Dal** | **Abone segmentteyse** seçin — Evet veya Hayır kararını veren segment. |
| **Çıkış** | Ayar yok — sadece bir uç nokta. |

![Bir Dal adımını yapılandıran sağ panel, arkasında soluklaşmış tuval](/static/core/admin/img/help/journey-builder/journey-builder-branch-config.webp)

Bir değer seçtiğiniz anda değişiklikler otomatik olarak kaydedilir — tuval üzerinde ayrı bir **Kaydet** düğmesi yoktur. **Giriş** dışındaki her adımın ayar panelinin altında bir **Adımı sil** düğmesi vardır.

**E-posta gönder** adımları için seçtiğiniz e-postalar, Campaign Studio'nun düzenli görsel oluşturucusunda tasarladığınız sıradan kampanyalardır — konu satırı, içerik blokları, her şey. Bunları **Taslak** olarak bırakın ve buradaki açılır menüden sadece seçin; yolculuk bunları sizin için gönderir, kendiniz asla Gönder'e tıklamazsınız.

## Şablonla başlama

Boş tuvalden bir akış oluşturmak her zaman gerekli değildir — araç çubuğundaki **Şablonlar**'a (veya boş tuvaldeki **Şablonları görüntüle**'ye) tıklayarak sekiz hazır başlangıç içeren bir seçici açın:

| Şablon | Ne oluşturur |
|----------|-----------------|
| **Hoş geldiniz serisi** | Yeni aboneleri selamlayın, ne yaptığınızı paylaşın, ardından ilk sipariş hatırlatması. |
| **İlk sipariş oryantasyonu** | İlk kez alışveriş yapan bir müşteriyi nazik bir oryantasyon dizisiyle tekrarlayan müşteriye dönüştürün. |
| **Satın alma sonrası ve değerlendirme** | Herhangi bir siparişten sonra teşekkür edin, ardından teslim edildikten sonra bir değerlendirme isteyin. |
| **VIP ve standart teklif** | Bir siparişten sonra, VIP segmentinize göre dallanarak her gruba doğru takip teklifini gönderin. |
| **Terk edilen sepet kurtarma** | Arkasında ürünler bırakan bir alışverişçiyi hatırlatın, ardından bir gün sonra takip hatırlatması. |
| **Kayıp müşterileri geri kazanma** | Bir süredir alışveriş yapmamış bir müşteriyi geri dönmek için bir sebeple yeniden etkileşime geçirin. |
| **Teslimat sonrası değerlendirme isteği** | Bir sipariş Teslim Edildi olarak işaretlendikten birkaç gün sonra bir değerlendirme isteyin. |
| **Yeniden stokta uyarısı** | İstediği ürün tekrar stokta olduğunda bekleyen bir alışverişçiye anında bildirin. |

Her şablon, eşleşen tetikleyiciye önceden bağlanmıştır — örneğin, **Kayıp müşterileri geri kazanma**'yı yeni bir yolculuğa uygulamak, o yolculuğun **Tetikleyici**'sinin de **Müşteri kayıp (geri kazanma)** olmasını bekler. Bu tetikleyici olaylarından her birinin ne zaman tetiklendiğini ve kurtarmaya odaklananların nasıl davrandığını (boşta kalma pencereleri, misafir alışverişi, sipariş başına bir kez değerlendirme istekleri ve yeniden stokta yolculuğunun düz tek seferlik uyarıdan nasıl devraldığını) görmek için [Tetiklenen yolculuklar](/help/triggered-journeys) sayfasına bakın.

![Hazır başlangıç yolculuklarını gösteren şablon seçici](/static/core/admin/img/help/journey-builder/journey-builder-templates.webp)

Bir şablon uygulamak, tuvaldeki **mevcut akışı değiştirir**, bu yüzden bunu bir yolculuğu tasarlarken yarıda değil, başında kullanın. Spwig, adlar zaten sahip olduğunuz bir e-posta veya segmentle eşleşiyorsa her adımı gerçek bir e-posta veya segmente yeniden bağlar; eşleşme bulamadığı her yerde, başlık, yayına geçmeden önce tam olarak neyi bitirmeniz gerektiğini bilmeniz için hâlâ bir e-posta veya segment seçilmesi gereken adım sayısını raporlar.

## Yolculukları paylaşma

İki araç çubuğu düğmesi, bir yolculuğun tasarımını adımlar arasında veya mağazalar arasında taşımanızı sağlar:

- **Dışa aktar**, yolculuğu bir `.journey.json` dosyası olarak indirir — akışın şeklinin (adımları, bekleme süreleri, dalları ve Evet/Hayır yolları) taşınabilir bir açıklaması, ayrıca her adımın kullandığı e-postaların ve segmentlerin *adları*. E-posta tasarımlarının kendilerini veya herhangi bir abone verisini içermez.
- **İçe aktar**, bir `.journey.json` dosyasını mevcut yolculuğa yükler ve tuvaldeki içeriği değiştirir.

Bu, gurur duyduğunuz bir akışı yedeklemek, kanıtlanmış bir hoş geldiniz serisini başka bir Spwig mağazasına devretmek veya mağazanızı yeni bir kurulumda klonladıktan sonra bir yolculuğu yeniden oluşturmak için kullanışlıdır.

Şablonlarda olduğu gibi, Spwig hedef mağazada eşleşme varsa e-postaları ve segmentleri adlarına göre yeniden bağlar ve eşleştiremediği her şeyi işaretler, böylece kurulumu tamamlayabilirsiniz.

## Yolculuğunuzu etkinleştirme

Akış hazır olduğunda, oluşturucunun sağ üst köşesindeki durum denetimini kullanın. Bir rozet, yolculuğun mevcut durumunu — **Taslak**, **Aktif** veya **Duraklatıldı** — bir **Etkinleştir** düğmesinin yanında gösterir.

**Etkinleştir** düğmesine tıklamak **önce akışı kontrol eder**. Çalışmasını engelleyecek bir şey varsa, etkinleştirme engellenir ve bir banner sorunları listeler — örneğin seçili bir e-postası olmayan bir **E-posta gönder** adımı, segmenti veya Evet/Hayır yolu olmayan bir **Dal**, o zamandan beri silinmiş bir e-posta veya segment veya sonsuza kadar çalışacak bir döngü. Her sorun tıklanabilirdir: seçtiğinizde, soruna neden olan adıma atlar ve düzelteceğiniz kadar kırmızıyla çerçevelenir. Uyarılar (erişilemeyen bir adım veya gecikme ayarlanmamış bir **Bekle** gibi) da listelenir ancak etkinleştirmeyi engellemez.

![Etkinleştirme engellendi, sorun bir banner'da listelendi ve soruna neden olan adım kırmızıyla çerçevelendi](/static/core/admin/img/help/journey-builder/journey-builder-activate-blocked.webp)

Akış kontrolü geçtiğinde, rozet **Aktif** olarak değişir ve yolculuğu tetikleyicisi her ateşlendiğinde aboneleri kaydetmeye başlar. Düğme **Duraklat** olur, bu da yeni kayıtları durdurur — zaten yarıda olan aboneler kalan adımlarını almaya devam eder. Kayıt, soğuma süreleri ve durumun nasıl etkileşime girdiğini görmek için [Tetiklenen yolculuklar](/help/triggered-journeys) sayfasına bakın.

## Yolculukta kimlerin olduğunu görme

Bir yolculuk yayına alındığında, her adımın köşesinde küçük bir **sayı rozeti** gösterilir: şu anda o adımda bekleyen abone sayısı. İnsanların nereye aktığını ve nerede biriktiğini görmek için hızlı bir yoldur — bir **Bekle** adımında büyük bir sayı beklenirken, belirli bir e-postadan hemen önceki birikme bir inceleme gerektirebilir. Sayılar, oluşturucu sekmesine her döndüğünüzde yenilenir.

![Adımlarda canlı sayı rozetleri ve araç çubuğunda Etkinleştir düğmesi olan tuval](/static/core/admin/img/help/journey-builder/journey-builder-live-counts.webp)

## İpuçları

- Akışı hâlâ **Taslak**ken tasarlayın — **Etkinleştir**meden kimse kaydedilmez. Oluşturucudan etkinleştirme önce hızlı bir kontrol yapar ve bozuk bir akışın yayına alınmasına izin vermez, bu nedenle yarı yapılmış bir yolculuğun aboneleri kaydetme riski yoktur.
- Aşırı özelleştirme planlasanız bile bir **Şablondan** başlayın — mevcut bir akışı düzenlemek, düğüm düğüm bir tane oluşturmak daha hızlıdır ve daha önce kullanmadıysanız dal desenini gösterir.
- Bir şablon uyguladıktan veya bir dosya içe aktardıktan sonra, eşleşmeyen adımlar notu için başlığı kontrol edin ve etkinleştirmeden önce eşleştiremediği **E-posta gönder** veya **Dal** adımlarını doldurun.
- Bir akış genişlediğinde (özellikle dallar) her zaman **Sığdır** düğmesine tıklayın — yakınlaştırdıktan veya kaydırdıktan sonra tüm şekli tekrar görmek için en hızlı yoldur.
- Adım adlarını taranabilir tutmak için, her **Bekle** adımını geciktirdiği e-postanın hemen öncesinde tutun, bunun yerine birkaç bekleme adımını bir araya toplamayın.
- Büyük değişiklikler yapmadan önce çalışan bir yolculuğu **Dışa aktarın** — sonuçtan memnun kalmazsanız yeniden içe aktarabileceğiniz bir yedek kopya tutmanın hızlı bir yoludur.