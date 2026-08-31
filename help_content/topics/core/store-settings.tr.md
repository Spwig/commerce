---
title: Mağaza Ayarlarını Yapılandırma
---

Mağaza Ayarları, mağazanızın kimliği, yerel ayarlar, markalama ve operasyonel tercihlerini yapılandırmak için merkezi yerdir. Başlamak için **Ayarlar > Mağaza Ayarları**'na gidin.

![Mağaza ayarları genel sekmesi](/static/core/admin/img/help/store-settings/store-settings-general.webp)

## Genel Sekme

**Genel** sekmesi, mağazanızın temel kimlik ayarlarını içerir.

### Mağaza Kimliği

- **Mağaza Adı** — Sayfa başlıklarında, e-postalarda ve yönetici başlığında gösterilen görüntüleme ismi.
- **Vurgu** — SEO ve sosyal paylaşım için mağazanızın kısa bir tanımı.
- **Web Sitesi URL'si** — Mağazanızın kamuya açık web adresi. Bu, e-postalarda, sitemap oluşturmada ve bağlantı kurulumunda kullanılır.

### İletişim Bilgileri

- **İletişim E-posta Adresi** — Sipariş bildirimlerini alır ve müşteri iletişiminde gösterilir.
- **Telefon Numarası** — Opsiyonel destek telefon numarası, ayakta ve e-postalarda gösterilir.

### İş adresi

Mağazanızın tam adresini (sokak, şehir, il, posta kodu, ülke) girin. Bu bilgiler şu şekilde kullanılır:
- Kargo başlangıç hesaplamaları
- Vergi hesaplamaları
- Hukuki gereklilikler ve faturalar

## Markalama

### Logo

Mağaza logosunu yükleyin (PNG veya SVG önerilir, ~200x50px, transparan arka plan). Logo şunlarda görünür:
- Mağaza ön yüzü başlığı
- E-posta şablonları
- Yönetici paneli

### Favicon

Kare bir favicon yükleyin (ICO veya PNG, 32x32px). Şunlar olarak görünür:
- Tarayıcı sekmesi simgesi
- Yıldız işaretim simgesi
- Mobil ana ekran simgesi

## Yerelleştirme

### Varsayılan Dil

10 desteklenen seçenekten mağazanızın ana dilini seçin:

| Dil | Kod |
|----------|------|
| İngilizce | en |
| İspanyolca | es |
| Fransızca | fr |
| Almanca | de |
| Portekizce | pt |
| Japonca | ja |
| Basitleştirilmiş Çince | zh-hans |
| Geleneksel Çince | zh-hant |
| Rusça | ru |
| Arapça | ar |

Varsayılan dil, yönetici arayüzünün dilini ve mağaza arayüzünde içerik için yedek olarak kontrol eder.

### Saat Dilimi

Sipariş zaman damgaları, planlı promosyonlar ve raporlama için mağazanızın saat dilimini seçin.

### Para Birimi

- **Varsayılan Para Birimi** — Fiyatlandırma ve muhasebe için ana para birimi.
- **Çoklu Para Birimi** — Kullanıcının tercih ettiği para biriminde fiyatları göstermek için etkinleştirin ve gerçek zamanlı döviz kurları kullanarak otomatik çeviri yapın.

**Ayarlar > Mağaza Ayarları > Para Birimi**'nde ekstra para birimlerini yapılandırın.

## E-Ticaret Ayarları

### Misafir Alışverişi

Bir hesap oluşturmadan alışveriş yapmanıza izin verin:
- Daha hızlı ödeme akışı
- İlk kez satın alanlar için daha az zorluk
- Daha az müşteri verisi toplar

### Hesap Oluşturma Zamanı

Müşterilerin bir hesap oluşturmak için ne zaman sorulacağını kontrol edin:

| Seçenek | Açıklama |
|--------|-------------|
| **Siparişin Sonrası (Tavsiye Edilir)** | Başarılı bir siparişten sonra hesap oluşturma istemiğini gösterin — en iyi dönüşüm için sipariş sonrası iyi niyeti kullanın |
| **Ödeme Sırasında** | Ödeme işlemi tamamlanmadan önce bir hesap oluşturun |
| **Ödeme Öncesi** | Alışveriş yapmadan önce bir hesap zorunluluğu (tavsiye edilmez - dönüşümü azaltır) |

Ayrıca, kaydolmanın faydalarını anlatmak için özel bir **Hesap Oluşturma Mesajı** da ayarlayabilirsiniz.

### Stok Ayarları

- **Stok Takibi** — Tüm dünyada stok takibini etkinleştirin
- **Düşük Stok Eşiği** — Düşük stok uyarılarının yönetici e-postasına gönderilmesi için stok seviyesi (varsayılan: 10 birim)

## Stok Zekası

![Stok Zekası kartı, Varsayılan Yeniden Sipariş Süresi, Güvenlik Stoku Çarpanı, Hız Hesaplama Penceresi, Varsayılan Olarak Geri Siparişleri Aç, Düşük Stok Uyarı Sıklığı alanlarını gösterir](/static/core/admin/img/help/store-settings/ecommerce-inventory-intelligence.webp)

Bu ayarlar, otomatik yeniden sipariş, güvenlik stoku ve satış hızı hesaplamalarını ayarlar ve stokta kalmayan ve düşük stok durumlarının nasıl ele alınacağını kontrol eder.

- **Varsayılan Yeniden Sipariş Süresi (Gün)** — Bir sipariş verdiğinizde tedarikçiden stoktaki sevkiyatın ne kadar süreceğini gösterir (varsayılan: 14).

Talep tahmini, yeni stok gelene kadar bir stok eksikliği olmaması için hemen yeniden sipariş verilmesi gereken ürünleri belirlemek için kullanılır.
- **Güvenlik Stok Çarpanı** — Beklenen talebin üzerine, satış artışlarını veya tedarikçi gecikmelerini emniyete almak için uygulanan bir tampon.

Örneğin, 1.5 olan bir çarpan, hesaplanan güvenlik stokluğunun %50'si kadar bir tampon ekler; 2.0 ise iki katına çıkarır.

Bir ürünün bitmesinin maliyetinin yüksek olduğu durumlarda (en çok satanlar, sezonluk ürünler) bu değeri artırın; aksi takdirde, fazla sipariş vermek istemediğiniz yavaş hareket eden stoklar için bu değeri düşürün.
- **Hız Hesaplama Penceresi (Gün)** — Spwig'in her ürünün satış hızını hesaplamak için kullandığı geriye dönük pencere, bu da yeniden sipariş önerilerini ve stok günleri değerlerini etkiler (varsayılan: 30).

Daha kısa bir pencere, son talep değişimlerine daha hızlı tepki verir; daha uzun bir pencere, sezonluk zirveleri düzeltir, bu nedenle tek bir yoğun haftanın tahminiye yanlış yönlendirilmesine neden olmaz.
- **Varsayılan Olarak Geri Siparişlere Izin Ver** — Yeni oluşturulan ürünler için uygulanan başlangıç geri sipariş ayarı (varsayılan olarak kapalı).

Her ürün, kendi ürün sayfasında bireysel olarak bunu geçersiz kılabilir ve mevcut ürünler, zaten sahip oldukları ayarları korur — bunu değiştirmek, sadece yeni ürünlerin başlangıç ayarlarını değiştirir, katalogunuzu retroaktif olarak güncellemeyebilir.
- **Düşük Stok Uyarısı Sıklığı** — Spwig mobil uygulamanızın, düşük stok hakkında ne sıklıkla bildirim alacağı: **Anlık** bir ürünün düşük stok eşiğine ulaşması anında bir bildirim gönderir; **Günlük Özeti** ve **Haftalık Özeti** ise bu sıklıkta mevcut düşük stoklu tüm ürünleri özetleyen tek bir bildirim gönderir.

Bu ayar, **Düşük Stok Bildirimleri** (aşağıdaki E-Posta Ayarları) etkinken geçerli olur — bildirimler kapalıyken, herhangi bir sıklıkta bildirim gönderilmez.

### Belgeler ve Faturalar

![Dökümanlar & Faturalar kartı, örnek değerlerle doldurulmuş olan Vergi Kimliği / KDV Numarası, Fatura Altbilgisi Metni, Paketleme Formu Altbilgisi Metni ve Belge Logosu Genişliği alanlarını göstermektedir](/static/core/admin/img/help/store-settings/ecommerce-documents-invoicing.webp)

Bu alanlar, siparişler için Spwig tarafından oluşturulan faturalar ve paketleme formları için doldurulur — örneğin bir satıcı, bir PDF faturasını indirir veya e-postayla gönderirken veya bir gönderi için paketleme formunu bastırırken.
- **Vergi Kimliği / KDV Numarası** — İşletmenizin vergi kimlik numarası. Oluşturulan faturaların yerel vergi belgelenme gerekliliklerini karşılamasını sağlamak için faturalara yazılır.
- **Fatura Altbilgisi Metni** — Oluşturulan her faturanın altında gösterilen serbest metin. Sık kullanılan kullanımlar: ödeme koşulları (30 gün içinde ödeme), bir teşekkür mesajı veya banka transferi bilgileri.
- **Paketleme Formu Altbilgisi Metni** — Oluşturulan her paketleme formunun altında gösterilen serbest metin. Sık kullanılan kullanımlar: iade talimatları veya depo/amaçlama ekibi için bir not.
- **Belge Logosu Genişliği (px)** — PDF faturalarında ve paketleme formlarında mağaza logosunun genişliği (varsayılan: 200px). Yükseklik, logosunun orantıları korunarak otomatik olarak ölçeklendirilir. Logonun kendisi, **Logo** (Yukarıdaki Markalama)’dan gelir — SVG logoları PDF belgelerinde çizilmez, dolayısıyla mağaza eklentisinde vektör sanat kullanıyorsanız, bir PNG veya JPG versiyonu yüklemeniz gerekir.

## E-Posta Ayarları

E-posta teslimatı ayarlarını **Ayarlar > E-Posta Hesapları** ve **Ayarlar > E-Posta Şablonları**’nda yapılandırın. Tam detaylar için [E-Posta Yapılandırması](/help/email-configuration) sayfasına bakın.

Mağaza Ayarları’nda mevcut olan temel e-posta ayarları:
- **Sipariş Onay E-Postaları** — Otomatik onay e-postalarını aç/kapat
- **Kargo Bildirimleri E-Postaları** — Kargo güncellemesi bildirimlerini aç/kapat
- **Düşük Stok Uyarıları** — Stok eşiğin altında olduğunda yönetici e-postasına uyarı gönder
- **E-Posta Teslimat Modu** — Canlı (normal teslimat), Duraklat (tüm e-postaları tut), Yalnızca Günlük (kaydet, ama asla gönderme)
- **Test Yönlendirme E-Postası** — Test için tüm giden e-postaları tek bir adrese yönlendir

## Güvenlik Ayarları

### İki Faktörlü Kimlik Doğrulama (2FA)

Personelin iki faktörlü kimlik doğrulama kullanmaları gerekip gerekmediğini kontrol edin:

Tüm markdown formatını, resim yollarını, kod bloklarını ve teknik terimleri koruyun.

{
  "Setting": "Açıklama",
  "---------": "-------------",
  "**Optional**": "Personel, 2FA'yı etkinleştirmeyi seçebilir ancak gerekli değildir",
  "**Recommended**": "Personel, 2FA kurulumunu teşvik eden bir pencere görür",
  "**Required**": "2FA etkinleştirilene kadar personel yöneticiye erişemez"
}

- **Gecikmeli Süre (Gün)** — 2FA kurulumunun zorunlu hale gelmesinden sonra personelin ne kadar gününün olduğuna dair
- **Güvenilir Cihazlar** — Belirli sayıda gün için tanıdık cihazlarda 2FA doğrulamasını atlayabilir

## Çerez Onayı

Mağaza ziyaretçilerine gösterilen çerez onayı bannerını yapılandırın:

- **Çerez Onayı Etkin** — Çerez bannerını göster veya gizle
- **Banner Konumu** — Ekran üzerindeki bannerin nerede görüneceğini belirtin (alt bar, köşe popupı, vb.)
- **Onay Modu** — Basit bir duyuru, tercih edilen veya tercih edilmeyen
- **Banner Başlığı ve Metni** — Ziyaretçilere gösterilebilen özelleştirilebilir başlık ve açıklama
- **Kategori Açıklamaları** — Analitik, pazarlama ve fonksiyonel çerezler için ayrı ayrı açıklamalar

Tüm banner metin alanları, çok dilli mağazalar için çeviriye uygun olur.

## İletişim

**İletişim** sekmesi, mağazanızanın pazarlama e-postası ve SMS için gerekli onayı nasıl alacağını, onaylayacağını ve müşterilerin bu onayı nasıl yönetebileceğini kontrol eder. Bu ayarlar, GDPR için e-posta (TCPA için SMS) ile yasal uyumunuzu şekillendirir, bu nedenle lütfen açıklamadan önce kendi hukuk danışmanlarınızla inceleyin — Spwig, danışmanlık vermez, sadece kontrolleri sağlar.

![İletişim sekmesi, E-posta Pazarlama Onayı, Tercihler & İptal, ve SMS Onayı kartlarını gösterir](/static/core/admin/img/help/store-settings/communications-tab.webp)

### E-posta Pazarlama Onayı

- **Pazarlama E-postaları İçin Çift Onay Etkin** — Açık olduğunda, bir müşteri pazarlama e-postasına kayıt olursa, Spwig ona herhangi bir pazarlama mesajı göndermeden önce bir onay e-postası gönderilir. Açık olduğunda, bir müşteri pazarlama opt-in kutusunu işaretlerse yeterlidir. Aksi takdirde, varsayılan olarak etkinleştirilir, GDPR en iyi uygulamalarına uygun şekilde.
- **Varsayılan Pazarlama Opt-In Durumu** — Yeni oluşturulan müşteri hesapları için uygulanacak ilk pazarlama opt-in durumu. Varsayılan olarak kapalıdır (GDPR opt-out), bu nedenle yeni müşteriler, aktif olarak opt-in yapana kadar pazarlama e-postasına abone olmaz.

Çift onay etkinleştirildiğinde, opt-in, onay e-postası ile birlikte bir doğrulama bağlantısı içeren bir e-posta gönderir. Müşteri bağlantıyı tıklayana kadar, onlar opt-in olarak kaydedilir ancak onaylanmamıştır ve pazarlama gönderileri onları atlar — işlem e-postaları (sipariş onayları, kargo güncellemeleri, parola sıfırlama) bu ayar tarafından asla etkilenmez.

### Tercihler & İptal

- **Müşteri Tercih Merkezini Etkinleştir** — Açık olduğunda, müşteriler hesap dashboard'larından bir self-service sayfasında e-posta ve SMS tercihlerini yönetebilir. Kapalı olduğunda, o sayfa ve destekleyici API'si mevcut değil ve dashboard bağlantısı gizlenir. Her iki durumda da bir-click iptal bağlantısı e-postalarınızda çalışır — bu, uyumluluk için gerekli olan ve bu geçiş tarafından etkilenmeyen bir kaçık deliktir.
- **İptal Nedenlerini Topla** — Açık olduğunda, bir-click iptal sayfası müşteriye kısa bir neden sorar: *Çok fazla e-posta alıyorum*, *İçerik bana ait değil*, *Bunu kaydolmadım*, *Artık ilgilenmiyorum*, veya *Diğer*. Bir müşteri seçtiği neden, onay incelemesi kayıtlarına kaydedilir ve bu sayede zaman içinde iptal kalıplarını inceleyebilirsiniz.

### SMS Onayı

- **SMS Doğrulaması Gerekli** — Açık olduğunda (varsayılan), bir müşteri, Spwig'in herhangi bir SMS'sini (pazarlama metni dahil) göndermeden önce telefon numarasını bir kezlik bir kodla doğrulamalıdır. Kapalı olduğunda, SMS opt-in kutusunu işaretlemek yeterlidir. Bu varsayılan, TCPA güvenliği için **açık** olarak değiştirilmiştir — signup akışınızdaki başka bir doğrulama adımınız varsa bu ayarı kapatın.

## Bakım Modu

Mağazanızı geçici olarak kapalı tutmak için bakım modunu etkinleştirin:
- Ziyaretçilere özel bir bakım mesajı gösterir
- Sayfa Builder'da yapılandırılmış bir **Bakım Sayfası** linkleyebilirsiniz, böylece tamamen markalı bir bakım deneyimi elde edersiniz
- Sadece yönetici kullanıcılarına erişimi sınırlar
- Büyük güncellemeler veya geçişler sırasında yararlıdır

Tüm markdown formatlamasını, resim yollarını, kod bloklarını ve teknik terimleri koruyun.

## Sosyal Medya

Mağazanızın sosyal medya hesaplarını ilişkilendirin. Bu alanlar ayakta ve e-posta şablonlarında görünür:

- **Facebook URL**
- **Twitter URL**
- **Instagram URL**
- **LinkedIn URL**

## SEO Varsayımları

Sayfaların kendi SEO ayarlarına sahip olmadığı zaman kullanılan varsayılan meta etiketlerini ayarlayın:

- **Meta Başlığı** — Varsayılan sayfa başlığı (60 karaktere kadar)
- **Meta Açıklaması** — Arama sonuçlarında gösterilen varsayılan açıklama (160 karaktere kadar)
- **Meta Anahtar Kelimeleri** — Varsayılan virgülle ayrılmış anahtar kelimeler

## Vergi Ayarları

**Ayarlar > Vergi Ayarları**'nda vergi toplama ayarlarını yapılandırın:

1. **Hesaplama Yöntemi** — Kargo adresine, faturalandırma adresine veya mağaza konumuna göre
2. **Vergi Oranları** — Bölge ve ürün vergi sınıfına göre oranları tanımlayın
3. **Vergi Gösterimi** — Fiyatları vergiyle, vergisiz veya her ikisiyle birlikte gösterin

## İpuçları

- Sipariş işlemeden önce zaman diliminizi doğru şekilde ayarlayın — tüm zaman damgalarını ve raporları etkiler.
- Dönüşüm oranlarını artırmak için misafir ödeme yapma özelliğini etkinleştirin.
- Doğru sevkiyat ve vergi hesaplamaları için işinizin adresini doldurun.
- Profesyonel, markalı bir deneyim için hem bir logo hem de bir favicon yükleyin.
- En iyi kayıt oranları için **Sonraki Satın Alma** hesap oluşturma timingini kullanın.
- Mağaza adminini korumak için personel için iki faktörlü kimlik doğrulama zorunluluğunu etkinleştirin.
- canlıya geçmeden önce **Test Yönlendirme E-postası** ayarını kullanarak e-posta akışlarını test edin.
- **Varsayılan Tekrar Sipariş Liderlik Süresi**'ni, en yavaş düzenli tedarikçinizle eşleştirin — tekrar sipariş tahmini, tüm kataloğunuza tek bir değer uygular, bu yüzden en uzun liderlik süresine sahip ürünlerinize göre yan yana olun.
- **Hız Hesaplama Penceresini** kısaltın, sık sık kampanyalar veya yeniden stoklamalar yapıyorsanız ve tahminlerin son birkaç günde satışa hızlı tepki vermesini istiyorsanız; talep üzerinde daha dengeli, daha az dalgalanmaya sahip bir bakış için uzatın.
- **Varsayılan Geri Siparişleri Açmana** izin verirseniz, bu sadece değişiklikten sonra oluşturulan ürünler için başlangıç noktasını ayarlar — mevcut katalogdaki mevcut ürünleri tek tek ziyaret ederseniz, mevcut katalogdaki tüm ürünlerde geri siparişlerin etkin olduğundan emin olun.
- **Düşük Stok Uyarı Sıklığı**'nı, stok yönetiminizi ne kadar aktif şekilde yönettiğinizle eşleştirin: Hareketli kataloglar için **Anlık**, daha büyük bir katalogda uyarı yorgunluğunu önlemek için **Günlük Özeti** veya **Haftalık Özet**.
- **Vergi Kimliği / KDV Numarası**'nı ve alt bilgi metnini, bir müşteriye ilk gerçek faturayı göndermeden önce doldurun — her iki alan da varsayılan olarak boş olur.
- **Logo**'nuz bir SVG ise, bir PNG veya JPG versiyonunu da yükleyin — **Belge Logosu Genişliği** Spwig, oluşturulan faturalar ve paketleme formları üzerinde SVG resmini çalamayacağı için PDF'ler üzerinde hiçbir etkisi yoktur.
- **Pazarlama E-postaları için Çift Onay'ı** devre dışı bırakma, hesap dashboardsunuzu basitleştirmek için sadece - bu, müşterilerin tek bir mesaj türüne abone olmaktan kurtulmasına izin verir, ancak onların tercihleri üzerinde ince ayar yapma imkanını kaybetmelerine neden olur (örneğin, sevkiyat güncellemelerini koruyup bülteni düşürme).
- **Varsayılan Pazarlama Onayı Durumu**'nu kapalı tutun. Yeni hesaplar için pazarlama rızasını ön onaylamak, bir müşteri teknik olarak kaldırılamazsa dahi GDPR opt-in gerekliliğini alt üst eder.
- **Müşteri Tercih Merkezini** devre dışı bırakma, hesap dashboardsunuzu basitleştirmek için sadece - bununla birlikte, müşterilerin tek bir mesaj türüne abone olmaktan kurtulmalarına izin verilir, ancak ince ayar imkanlarını kaybetmelerine neden olur (örneğin, sevkiyat güncellemelerini koruyup bülteni düşürme).
- **SMS Doğrulamasını** devre dışı bırakma, telefon numaranızı başka bir yolla doğrulamak için bir akışınız varsa (örneğin, SMS tabanlı bir oturum açma) - bu ayar, TCPA kuralları içinde kalmak için özel olarak mevcuttur.

## Sorun Giderme

**Mağaza yüzeyinde değişiklikler görünmüyorsa:**
- Tarayıcınızın cache'ini temizleyin
- Admin panelinden bir cache temizliği yapın
- Kapatma modunun yanlışlıkla etkinleştirildiğinden emin olun

**E-postalar gönderilmiyor:**
- E-posta yapılandırması içindeki e-posta sağlayıcısı ayarlarını kontrol edin
- **E-posta Teslimat Modu**'nun **Canlı** olarak ayarlandığından emin olun
- **Test Yönlendirme E-postası**'nın, gerçek alıcılar için e-postaların gönderilmesini istiyorsanız boş olduğundan emin olun

**Döviz çeviri işlemi çalışmıyor:**
- Kur değişim oranı sağlayıcınızın bağlı olduğundan emin olun
- Kur değişim ayarlarında API kimlik bilgilerini kontrol edin
- Kurları manuel olarak güncellemeyi deneyin

**Pazarlama e-postaları, katılmaya karar veren müşterilere ulaşmıyor:**
- **Pazarlama e-postaları için Çift Onay'ı Etkinleştir** ayarının açık olduğundan emin olun — bu durumda, pazarlama e-postaları devam edene kadar müşteri doğrulama e-postasındaki onay bağlantısına tıklamalıdır
- Müşteriden doğrulama e-postasını alıp almadığını kontrol etmesini isteyin
- Müşterinin tercihlerinde pazarlama onayı ayarının hâlâ açık olduğundan emin olun — bir istenmeme tıklaması bu ayarı kapatır

**Müşteriler tercih merkezini bulamadıklarını söylüyor:**
- **Müşteri Tercih Merkezini** etkin olduğundan emin olun — bu ayar kapalıysa, dashbord bağlantısı gizlenir ve sayfa tasarım olarak erişilemez
- Herhangi bir pazarlama e-postasındaki istenmeme bağlantısı bu ayara rağmen her zaman çalışır, bu yüzden müşterilere alternatif olarak oraya yönlendirin