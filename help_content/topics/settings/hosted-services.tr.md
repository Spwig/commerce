---
title: Spwig Barındırılan Hizmetler
---

Spwig, mağazanızın hiçbir şeyi yapılandırmadan veya barındırmadan kullanabileceği üç isteğe bağlı bulut hizmeti içerir: **GeoIP**, ziyaretçilerinin nerede bulunduğunu tespit eder, **Geocoder**, müşteri adreslerini harita koordinatlarına dönüştürür ve **Push**, mobil Spwig yönetici uygulamanıza anlık bildirimler gönderir. Topluluk (ücretsiz) sürümünde, her hizmet ayda büyük bir kullanım hakkı sunar. Herhangi bir hizmet kotasına yaklaşıyorsa, Spwig yönetici panelinde size uyarı verir ve müşterilerin farkına varmadan önce yükseltme kararı vermenizi sağlar.

## Üç barındırılan hizmet

### GeoIP — ziyaretçi ülke tespiti

GeoIP, her ziyaretçinin IP adresine göre ülkesini tespit eder. Mağazanız, bu bilgiyi müşteri gelince otomatik olarak doğru para birimini göstermek ve ödeme sırasında ülkeyi otomatik doldurmak için kullanır. Örneğin, Almanya'dan gelen bir ziyaretçi euro, Japonya'dan gelen bir ziyaretçi ise yen cinsinden fiyatlar görecektir — manuel seçim yapmaya gerek kalmadan.

GeoIP bir sorgu yapan her sayfa yükleme, aylık kotasınıza sayılır. Aynı tarayıcı oturumundan tekrar ziyaretler her biri bir sorgu tüketmez; sonuç oturum için önceden önbelleğe alınır. GeoIP sorguları yalnızca mağaza ön yüzünde gerçekleşir, yönetici panelinde değil.

### Geocoder — adresi koordinatlara çevirme

Geocoder, müşteri tarafından girilen adresleri coğrafi koordinatlara (enlem ve boylam) dönüştürür. Mağazanız, bu koordinatları iki amaç için kullanır: toplama noktalarınız veya yarıçap bazlı nakliye kurallarınız varsa, mesafe bazlı nakliye ücretlerini hesaplamak ve ödeme sayfasında adres otomatik tamamlama önerilerini sağlamak, böylece müşteriler hızlıca adreslerini bulabilir.

Bir geocoder sorgusu, müşteri ödeme sırasında bir adres seçer veya onaylar. GeoIP gibi, sonuçlar önbelleğe alınır, böylece aynı adres oturum başına yalnızca bir kez sorgulanır.

### Push — yönetici uygulama bildirimleri

Push, Spwig satıcı mobil uygulamanıza anlık bildirimler gönderir. Yeni bir sipariş gelirse, stok belirli bir eşiğin altına inerse veya müşteri bir mesaj gönderirse, Push cihazınıza anlık bir bildirim gönderir ve yönetici panelini açık tutmadan yanıt vermenizi sağlar.

Cihazınıza gönderilen her bildirim, aylık kotasınıza bir push isteği olarak sayılır.

## Topluluk ücretsiz planı

Spwig Topluluk sürümünde, her hizmet aylık istek kotası kadar ücretsiz olarak dahildir. Kesin sınırlar Spwig tarafından belirlenir ve değişebilir; yönetici paneliniz her zaman yükleme için geçerli rakamları gösterir. Ödeme planları (Başlangıç, Büyüme, Pro, Pro Plus) ve ücretli lisansla barındırılan yüklemeler her hizmet için daha yüksek sınırlara sahiptir.

Bir hizmet Topluluk kotasının %100'ine ulaşırsa, bu hizmete yapılan istekler bir sonraki takvim ayı kota sayacı sıfırlanana kadar durur. Mağazanıza olan etkisi hangi hizmetin etkilendiğine bağlıdır:

| Hizmet | %100'e ulaşıldığında ne olur |
|--------|-----------------------------|
| GeoIP | Para birimi otomatik tespiti, mağazanızın varsayılan para birimine geri döner. Müşteriler hâlâ manuel olarak para birimini değiştirebilir. |
| Geocoder | Adres otomatik tamamlama önerileri durur. Müşteriler hâlâ adreslerini manuel olarak yazabilir. Nakliye ücreti hesaplaması, son bilinen koordinatlarla devam eder. |
| Push | Yeni yönetici uygulama bildirimleri kuyruğa alınır ancak bir sonraki ay veya yükseltme yapmadan teslim edilmez. |

Mağazanız her durumda normal şekilde çalışır — hiçbir sipariş kaybolmaz ve müşteriler hâlâ ödeme yapabilir. Etkiler yalnızca удобность özellikleriyle sınırlıdır.

## Dashboard tile'ı okuma

**Spwig hizmetleri kullanımı** tile'i yönetici paneli anasayfasında görünür. Her üç hizmet için ilerleme çubuklarını gösterir.

Tile'deki her satır aynı düzeni takip eder:

- **Hizmet adı** (sol) — GeoIP, Adres arama (Geocoder) veya Push bildirimleri.
- **İlerleme çubuğu** (orta) — kullanım arttıkça sola sağa doldurulur.

Çubuğun rengi sınırlara yaklaştıkça değişir:
  - **Yeşil** — kullanım %80'in altındadır.

Her şey normal şekilde çalışıyor.
  - **Amber** — kullanım oranı %80 ile %99 arasında.

Hizmet hâlâ çalışıyor ama limitin yaklaşıyor.
  - **Kırmızı** — kullanım oranı %100'ye ulaştı.

Bu ay için hizmet yavaşlatıldı.
- **Kullanım sayıları** (sağda) — toplam izin verilen isteklerden kullanılan tam sayı, örneğin `3.241 / 10.000`.

Parantez içindeki etiket, genellikle `(bu ay)` olan zaman penceresini gösterir.

Eğer tile, Spwig güncellemesi sunucusuna ulaşamazsa (örneğin, sunucunuzun dışa doğru internet erişimi yoksa), o hizmet için kullanım sütununda bir çizgi (`—`) gösterilir. Bu, hizmetin bozuk olduğunu değil, kullanımın geçici olarak görünmez olduğunu gösterir.

### **Yükseltme** butonu

Herhangi bir hizmet %80 veya daha fazla kullanım oranına ulaştığında, tile'nin sağ üst köşesinde bir **Yükseltme** butonu görünür. Bu butona tıkladığınızda, planları karşılaştırıp hizmet limitlerinizi artırabilmeniz için Spwig yükseltme sayfası açılır. Kullanım oranı, bir sonraki ayın başından itibaren tekrar %80'in altına inerse, buton kaybolur.

## Kotası aşıldığında uyarı şeridi

Dashboard tile'ı yanı sıra, herhangi bir hizmet %80 eşiğini geçtiğinde, admin panelinin üst kısmında bir şerit görünür. Bu şerit yalnızca Community yüklemelerinde görünür.

**Amber şeridi — limit yaklaşıyor (%80–%99)**

> **Barındırılan hizmetler kotasına yaklaşıldı:** Spwig hizmetlerinizden biri, Community seviyesi kotasının %80'ini aştı. Kotasını yükseltmek için lütfen bu ay sonuna kadar planınızı değiştirin.

Bu şerit, erken uyarıdır. Hizmetleriniz hâlâ çalışıyor ve ayın sonuna kadar planınızı yükseltmeye karar verme zamanınız var.

**Kırmızı şerit — limit aşıldı (%100)**

> **Spwig hizmetleri kotası aşıldı:** Barındırılan hizmetlerinizden biri, Community seviyesi kotasını %100'ye ulaştı. Kotasını yükseltmek için lütfen onları kesintisiz şekilde çalıştırın.

Bu şerit, en az bir hizmetin %100'e ulaştığını ve yavaşlatıldığını gösterir. Herhangi bir şeride tıkladığınızda **Yükseltme** butonu, tile butonu ile aynı yükseltme sayfasını açar.

Şerit, bir sonraki takvim ayının başından itibaren sayaçlar sıfırlanınca otomatik olarak kaybolur veya hemen bir ödemeli plana yükselttikten sonra kaybolur.

## %90'da e-posta uyarısı

Herhangi bir hizmet kotasının %90'ını aştığında, Spwig ayrıca mağazanızın ayarlarında yapılandırılmış e-posta adresine ( **Ayarlar > Mağaza Ayarları > İletişim > Yönetici E-postası** ) bir kez uyarı e-postası gönderir. Bu e-posta, her hizmet ve takvim ayı başına en fazla bir kez gönderilir, bu yüzden mesajla dolu olmazsınız. %100'e ulaşıldığında e-posta gönderilmez çünkü bu noktada admin panelindeki şerit durum zaten açıkça belirtilmiştir.

E-postayı alamıyorsanız, **Ayarlar > Mağaza Ayarları** altında yönetici e-posta adresinizin doğru olduğundan emin olun.

## Planınızı yükseltme

Community'den herhangi bir ödemeli plana yükselttiğinizde, daha yüksek limitler hemen etkin olur — mağaza yeniden başlatması veya yapılandırma değişikliği gerekmez. Dashboard tile, bir sonraki yenileme sırasında (5 dakika içinde) yeni, daha yüksek limiti gösterir.

Yükseltmek için dashboard tile veya kota şeridindeki **Yükseltme** butonuna tıklayın ya da Spwig yükseltme sayfasını doğrudan ziyaret edin. Ödemeli planlar, aynı üç barındırılan hizmeti (GeoIP, Geocoder, Push) daha yüksek aylık limitlerle birlikte sunar ve Spwig barındırılan e-posta teslimatına ve öncelikli destek erişimine de sahiptir.

## Kendi kendine barındırma ve Pro lisansları

Kendi kendine barındırılan bir Spwig yüklemeniz varsa ve bir ödemeli lisansa sahipseniz, lisans seviyeniz, eşdeğer barındırılan planla aynı şekilde hizmet limitlerinizi belirler. Mağazanızın `updates.spwig.com` adresine ulaşmak için hala dışa doğru internet erişimi gerekir, böylece platform, lisans yapılandırmanızı alıp doğrulayabilir. Dashboard tile'de gösterilen kullanım sayaçları, `geoip.spwig.com`, `geocoder.spwig.com` ve `push.spwig.com` barındırılan hizmet uç noktalarından alınır.

Şu anda GeoIP, Geocoder veya Push'ı kendi kendine barındırmak için bir seçenek yok — bu hizmetler, Spwig altyapısı tarafından özel olarak sunulur ve tüm sürümlerde dahildir.

## İpuçları

Tüm markdown biçimlendirmesini, görsel yollarını, kod bloklarını ve teknik terimleri koruyun.

- **Meşgul ayların sonunda tile'ı düzenli olarak kontrol edin** — bir satış etkinliği veya kampanya, GeoIP ve Geocoder sorgularını önemli ölçüde artırabilir.

Tile, müşteriler etkilenmeden önce önceden bilgi verir.
- **Para birimi geri dönüşü, çoğu müşteri için görünmezdir** — GeoIP limitine ulaşıldığında, müşteriler mağazanızın varsayılan para birimini görür.

Bir pazarı temel olarak hizmet veren mağazalar için bu nadiren ciddi bir sorun olur; gerçekten uluslararası mağazalar için daha önemlidir.
- **Adres otomatik tamamlama, bir engel değil, bir kolaylıktır** — Geocoder kilitlendiğinde, müşteriler hâlâ adreslerini normal şekilde yazıp gönderebilir.

Sık sık yüksek ödeme trafiği çeken kampanyalar düzenliyorsanız, meşgul dönemlerden önce yükseltmeyi düşünün.
- **Kilitlendirme, bildirimleri kalıcı olarak kaybetmez** — kilitlendirme döneminden kuyruktaki bildirimler, ay sıfırlanması veya yükseltme sonrasında geriye dönük olarak teslim edilmez.

Zaman hassas sipariş uyarıları için push'a çok bağımlıysanız, limitin aşılmasından önce yükseltmek, hiçbir şeyi kaçırmamanızı sağlar.
- **5 dakikalık önbellek, tile'ın tamamen gerçek zamanlı olmadığını gösterir** — kullanım rakamları arka planda yaklaşık her beş dakikada bir yenilenir.

Düşük trafiğin ötesinde yüksek trafiğin olduğu dönemlerde, gerçek kullanım, tile'da gösterilen rakamlardan biraz önde olabilir.
- **Yönetici e-posta adresinizi ayarlayın** — %90 uyarısı e-postası, yalnızca **Ayarlar > Mağaza Ayarları > Yönetici E-postası** doldurulduğunda çalışır.

Bu ayarın doğru olduğundan emin olmak, sorunlar ortaya çıkmadan önce bilgi vermenizi sağlar.