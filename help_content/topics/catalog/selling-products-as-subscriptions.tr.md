---
title: Ürünleri Abonelik Şeklinde Satma
---

Herhangi bir Basit, Değişken ya da Dijital ürün, bir kerelik bir satın alma ile aynı anda ya da yerine, tekrarlayan bir şekilde satılabilir. Bu kılavuz, bir ürün için abonelikleri açma, müşterilerin seçebileceği planları seçme ve müşterilerin ne sattığını ne sıklıkla göründüğünü kapsar.

## Hangi ürün türleri abonelik olarak satılabilir

Abonelikler, bu ürün türleri için sadece mevcuttur:

| Uygun | Uygun Değil |
|----------|---------------|
| Basit Ürün | Ürün Paketi |
| Değişken Ürün | Hediye Kartı |
| Dijital Ürün | Özelleştirilebilir Ürün |
| | Yapılandırılamaz Ürün |
| | Rezervasyon Ürünü |

Neden teslimat, fiyatlandırma değil: bir abonelik, her döngüde müşteriye yeniden faturalandırır ve her seferinde yeni bir siparişle ürünün yeniden teslim edilmesini sağlar. Spwig, bir Basit ya da Değişken ürünü yeniden sevk etmeyi ve her yenilemede Dijital bir ürünün indirme veya lisansını yeniden verme konusunda bilinçlidir — ancak, hediye kartı verilimini, çok bileşenli bir paketi, bir müşterinin kayıtlı özelleştirmesini, bir yapılandırıcı kurulumunu ya da bir rezervasyon yuvasını tekrarlayan bir düzende yeniden çalıştırmak güvenli değildir. Bu türleri abonelik olarak satmaya izin vermek, 2. döngüde müşteri parasını alırken hiçbir şey teslim edememe riskini doğurur.

**Abonelik Etkinleştir** onay kutusu, uygun olmayan türler için gizli veya griye dönmüş değildir — her ürün üzerinde teknik olarak kontrol edilebilir. Abonelikler etkinleştirilmiş bir Hediye Kartı, Paket, Özelleştirilebilir, Yapılandırılamaz ya da Rezervasyon ürünü üzerinde kaydetmeye çalışırsanız, Spwig, bu ürün türünün abonelik olarak satılamayacağını açıklayan bir doğrulama hatasıyla kaydı reddedecektir. Önce **Ürün Türü** 'nü değiştirin (Temel Bilgiler sekmesi), ya da bu ürün için abonelikleri kapatın.

## Bir ürün üzerinde abonelikleri etkinleştirme

1. **Ürünler > Tüm Ürünler** 'e gidin ve abonelik olarak satmak istediğiniz ürünü açın (ya da yeni bir tane oluşturun).
2. Temel Bilgiler sekmesindeki **Ürün Türü** 'nü Basit, Değişken ya da Dijital olduğundan emin olun.
3. **Abonelikler** sekmesine tıklayın.
4. **Abonelik Etkinleştir** 'i seçin.
5. **Abonelik Planları** alanındaki, bu ürünün sunulacağı planları seçin. Henüz bir plan oluşturmadıysanız, lütfen önce [Abonelik Planları](/help/subscription-plans) 'na bakın.
6. Aşağıdaki iki satın alma modu onay kutusunu yapılandırın.
7. **Kaydet** 'e tıklayın.

![Ürün düzenleme formunun Abonelikler sekmesi: Abonelik Etkinleştir checked, Abonelik Planları listesinde bir plan seçili ve Bir Kerelik Alışverişi'ni Izın Ver ve Abonelik Olarak Varsayılan'ı içeren onay kutuları](/static/core/admin/img/help/selling-products-as-subscriptions/subscriptions-tab.webp)

## Abonelik planlarını ekleyin

Bir **Abonelik Planı**, tekrarlanabilir bir şablon — faturalandırma sıklığı seçenekleri, deneme, kurulum ücreti, fesih kuralları — ki bunu bir kez oluşturursunuz ve herhangi bir sayıda uygun ürüne ekleyebilirsiniz. **Abonelikler** sekmesindeki **Abonelik Planları** alanına, ürünün hangi planlar altında satılacağını bağlamak için bir plan eklersiniz.

Aynı produkte birden fazla plan ekleyebilirsiniz. Örneğin, aynı item için "Standart" ve "Premium" tekrarlayan bir seviye sunmak isterseniz, her planın kendi fiyatlandırma seviyeleri, deneme ve fesih politikası olabilir. Bir ürünün birden fazla planı varsa, müşteriler, ödeme sıklığını seçmeden önce ürün sayfasında bir plan seçici görür.

## Bir kerelik ya da abonelik satınalmalarını kontrol etme

Abonelikler sekmesindeki iki onay kutusu, müşterilerin ürünleri nasıl alabileceğini kontrol eder:

- **Bir Kerelik Alışverişi'ni Izın Ver** — Varsayılan olarak etkinleştirilir.

Seçiliyse, müşteriler, normal bir kerelik alışveriş ile abonelik arasında seçim yapabilir.

Bunun tersine, ürünü abonelik olarak sınırlayın — her satın alma tekrarlayan bir sipariş olur ve hiçbir kerelik seçenek gösterilmez.
- **Abonelik Olarak Varsayılan** — Ürün sayfası açıldığında, müşterilerin bunu aktif olarak seçmesine gerek kalmadan abonelik seçeneğini (ve varsayılan plan/seviyesini) önceden seçer.



Bu, yalnızca **Bir Kez Alım'a Izin Ver** seçeneğinin de işaretli olduğunda etkili olur — bir kez alım kapalıysa, bu ayar ne olursa olsun ürün sadece aboneliklidir.

Bir kez alımın doğal beklenti olduğu ürünler için (kahve, takviyeler, tüketilebilirler) **Abonelik Olarak Varsayılacak** seçeneğini kullanın — bu, müşterilerin sadece bir kez alım yapmalarına izin verirken, onları tekrar gelmeye yönlendiren seçeneğe doğru bir adım atmasına neden olur, ancak onların bir kez alım yapma yeteneklerini kalmaz.

## Müşterilerin Nerede Gördüğü

### Ürün sayfasında

Bir ürünün abonelikleri etkinleştirilmiş ve en az bir tane aktif, kamuya açık planı varsa, bir satın alma modu seçici ürün sayfasında görünür:

![Mağaza satın alma seçicisi, "Abone Ol ve Tasarruflu" seçili: Bir kez alım vs Abone Ol ve Tasarruflu geçişleri, yıllık (Yüzde 20 Tasarruf), aylık ve çeyrek yıllık (Yüzde 10 Tasarruf) seviyeleri içeren bir teslim sıklığı listesiyle birlikte, deneme, iptal ve ödeme notları ile birlikte](/static/core/admin/img/help/selling-products-as-subscriptions/subscribe-and-save-selector.webp)

- Bir kez alım izin verilirse, müşteriler **"Bir kez alım"** ve **"Abone Ol ve Tasarruflu"** seçeneğini görür, varsayılan olarak neyi yapılandırdığınıza göre ayarlanır.
- Ürünün birden fazla planı varsa, "Abone Ol ve Tasarruflu" seçildiğinde bir plan seçici görünür.
- Seçilen plan için, müşterilerin planın fiyatlandırma seviyelerinden oluşan bir **teslim sıklığı** listesi görür, örneğin aylık, çeyrek yıllık, yıllık, her biri için fiyatı ve **"X% Tasarruf"** etiketi ile birlikte, seviye bir indirim taşıyorsa.
- Deneme süresi, kurulum ücreti ve planın iptal politikası (örneğin, "Her zaman iptal edilebilir") seviye listesiyle birlikte, ayrıca ödeme yönteminin ödeme sırasında ekleneceğini belirten bir not gösterilir.

### Sepet ve ödeme sırasında

Abonelik satırı sepette **Abonelik** etiketiyle, ödeme sıklığı (örneğin, "Her ay") ve bir deneme notu varsa, müşteriye hangi satırların tekrarlayan olduğunu açıkça belirtir. Ödeme sırasında, müşteri normalde olduğu gibi bir ödeme sağlayıcısı seçer — bu, gelecekteki yeniden doğrulamalarda şahsının ödemesi gereken yöntemdir.

> **Bilinen sınırlama:** Bazı ödeme sağlayıcıları için müşteri kartının otomatik olarak ödeme sırasında yeniden doğrulamaları için saklanması hâlâ bağlanmaktadır. Belirli bir sağlayıcı bu özelliği desteklemeyecek olursa, bu sağlayıcı üzerinden yapılan aboneliklerin yeniden doğrulamalarının otomatik olarak yapılmaması gerekir, bu yüzden bir sonraki yeniden doğrulama öncesi müşteriye güncel ödeme bilgilerini istemek gibi ekstra bir takip gerekir. İlk günden itibaren tamamen elden verilmemiş olur. Abonelikten yeniden doğrulamaların otomatik olarak yapılmadığını fark ederseniz, ödeme sağlayıcınızla iletişime geçin.

## İpuçları

- Abonelik planını önce oluşturun ve test edin (fiyat seviyeleri, deneme, iptal politikası), daha sonra ürününe ekleyin — planı daha sonra birkaç ürün arasında düzeltmekten daha kolaydır.
- Çoğu ürün için **Bir Kez Alım'a Izin Ver** seçili tutun. Bir kez alımın gerçekten işinize yaramadığı durumlar için abonelikli ürünleri saklayın.
- Eski bir en çok satan ürünü bir abonelik seçeneğine dönüştürüyorsanız, müşterilerin bir kez alım yapmaya alışık olmalarını bozmamak için ilk başta **Abonelik Olarak Varsayılacak** seçeneğini kapatın — abonelerin nasıl davrandığını gördükten sonra daha sonra açın.
- Dijital ürünler, yeniden doğrulamaların otomatik olarak teslimi kolaylaştırmadığı (kargo dahil değil) yazılım lisansları, içerik üyelikleri gibi abonelikler için harikadır.
- Elde ettiğiniz bir ürün türü (örneğin, bir paket veya özelleştirilebilir bir ürün) abonelik olarak satılmayacaksa, bunun yerine basitleştirilmiş Basit ya da Dijital bir eşdeğerinin abonelik olarak satılabileceğini düşünün.