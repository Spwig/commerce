---
title: WooCommerce'dan Göç
---

Mağazanız şu anda WooCommerce üzerinde çalışıyorsa, Spwig'in göç asistanı, ürünleri, müşterileri, siparişleri ve içeriği WooCommerce'nin REST API'si üzerinden doğrudan içeri aktarabilir. Bu kılavuz, API kimlik bilgilerini alma, içeri aktarma işlemini başlatma ve iki WooCommerce özel özelliğin hakkında bilgi verir: seçmeli Göç Köprüsü eklentisi (affiliate verileri için) ve birkaç popüler WooCommerce eklentisi için yerleşik destek.

## Başlamadan Önce

WooCommerce, göç asistanında desteklenen en kapsamlı kaynak platformudur. Aşağıdaki veriler temiz bir şekilde içeri aktarılır: kategoriler (hiyerarşisiyle), ürünler, resimler ve varyasyonlar, müşteriler ve adresler, siparişler, incelemeler, kuponlar ve blog gönderileri (kategorileri, etiketleri ve resimleriyle birlikte).

Affiliate profilleri, komisyon kayıtları ve ödeme geçmişi de içeri aktarılabilir, ancak bunun için önce Spwig Göç Köprüsü eklentisini yüklemeniz gerekir — aşağıya bakın. Onun olmadan bu veriler sadece atlanır.

Ayrıca unutmayın:

- Belirli WooCommerce eklentilerinden (abonelikler, paketler, rezervasyonlar, hediye kartları) gelen ürünler, Spwig'in eşleşen özelliğine taşınır, ancak her detayın geçmediği olabilir — aşağıda **WooCommerce eklenti desteği** bölümüne bakın.
- Ürünleriniz, müşterileriniz ve siparişlerinizdeki özel alanlar otomatik olarak algılanır ve daha sonra bir adımda haritalanması gerekir. [Göç Alanı Haritalama](migration-field-mapping) bölümüne bakın.
- Asistanın **Vergi Ayarlarını İçe Aktar** ve **Kargo Bölgesi ve Yöntemlerini İçe Aktar** seçenekleri, içeri aktarılan verilere uygulanmaz. Spwig'de vergi oranlarını ve kargo yöntemlerini kendiniz ayarlayın — [Göçün Sonrası](after-migration-review) bölümüne bakın.
- Aynı adımdaki **Fiyat Ayarı** seçeneği, WooCommerce içeri aktarımları için etkili olur ve ürünün temel fiyatını oluştururken değiştirir. Eğer her fiyatın kaydırılmasını istemiyorsanız, bunu **Hiçbiri** olarak bırakın.

WordPress admin oturumunuzu hazır tutun ve içeri aktarıyor olduğunuz ürün, müşteri ve sipariş sayısını yaklaşık olarak bilmelisiniz, böylece asistanın size gösterdiği sayıları mantıklı bir şekilde kontrol edebilirsiniz.

## REST API Kimlik Bilgilerini Almak

Spwig, WordPress admin panelinizden oluşturulan bir REST API anahtarı kullanarak WooCommerce ile iletişim kurar. Bu anahtar sadece **Okuma** erişimine sahip olmalıdır — Spwig, göç sırasında sadece mağazanızdan okur, hiçbir şeyi geri yazmaz.

1. WordPress'te **WooCommerce > Ayarlar > Gelişmiş > REST API**'ye gidin
2. **Anahtar Ekle**'ye tıklayın
3. Açıklama yazın (örneğin, `Spwig Göç`) ve **İzinler** alanını **Okuma** olarak ayarlayın
4. **API Anahtarı Oluştur**'a tıklayın
5. **Tüketici Anahtarı** (`ck_...`) ve **Tüketici Gizli** (`cs_...`) değerlerini güvenli bir yere kopyalayın

> **Önemli:** WooCommerce, Tüketici Gizli sadece bir kez, oluşturduğunuz anda gösterir. Eğer kopyalamadan önce sayfadan ayrılmışsanız, yeni bir anahtar oluşturmanız gerekir.

## Mağazanızı Bağlama

Spwig admin panelinde **Veri İçeri Aktarma & Dışarı Aktarma > Yeni Göç Başlat**'a gidin ve 1. adımda **WooCommerce**'i seçin. 2. adımda aşağıdaki bilgileri girin:

- **Mağaza URL'si** — mağazanızın tam web adresi, örneğin `https://mystore.com`
- **Tüketici Anahtarı** ve **Tüketici Gizli** — yukarıda kopyaladığınız değerler

**İleriye geçmeden önce bağlantı testi** seçeneğini işaretli bırakın (varsayılan olarak etkin) böylece Spwig, devam etmeden önce mağazanıza ulaşabildiğini ve kimlik doğrulamasını onaylayacaktır — bu, içeri aktarma sırasında yazım hatalarını ve izin sorunlarını hemen yakalar. Başarıyla tamamlandıktan sonra **İleri**'ye tıklayın.

## Veriyi İnceleme ve Seçme

3. adımda, mağazanızdan canlı sayım alınır — kategoriler, ürünler, müşteriler, siparişler, incelemeler ve kuponlar — ayrıca ilk beş ürünün bir örneği alınır, böylece doğru site okunduğunu onaylayabilirsiniz. Her veri türünün onay kutusu, sayımı sıfırdan yüksek olduğunda otomatik olarak işaretlenir ve sıfır olduğunda devre dışı bırakılır.

**İçe Aktarma Seçenekleri:**

- **Mevcut öğeleri atla** (açık) — gelen kayıtları Spwig'de zaten ne olduğuna göre eşleştirmek (ürünler için SKU, müşteriler için e-posta) ve yinelenenleri atlar.

Bos bir mağaza başlamıyorsan bırakın.
- **Ürün resimlerini içe aktar** (açık) — daha yavaş, ama değerlidir.
- **Orijinal kimlikleri mümkünse koru** (kapalı) — sihirbaz kendisi bunu "tavsiye edilmez" olarak etiketler. WooCommerce'nin sayısal kimliklerini korumak için özel bir teknik nedeniniz varsa, aksi takdirde kapatın.
- **Toplu boyut** — 10, 25 (varsayılan), 50 veya 100 kayıt bir anda.

Daha küçük toplar, kararsız bağlantılar için uygundur; daha büyük toplar, kararlı bir bağlantıda daha hızlı bitirir.

## Spwig Göç Köprüsü Eklentisi

WooCommerce, bir ortaklık programı kavramına sahip değildir, bu nedenle eğer bir WooCommerce ortaklık eklentisi üzerinden birini çalıştırıyorsanız, bu veri standart REST API tarafından görülemeyen tablolarda yaşamaktadır. **Spwig Göç Köprüsü**, WordPress sitesinize yüklediğiniz küçük bir yardımcı eklentidir.

Köprü eklentisi şu özellikleri açar:

- **Ortaklık profilleri** — ortaklarınızın detayları ve referans kodları
- **Komisyon kayıtları** — her ortaklıkla ilişkili komisyon geçmişi
- **Ödeme geçmişi** — ortaklıklara yapılan geçmiş ödemeler

Bunu tamamen isteğe bağlıdır — Spwig'de ortaklık programı çalıştırıyorsanız veya bu geçmiş veriyi ihtiyaç duymuyorsanız atlayabilirsiniz.

> **Not:** Ortaklık verileri yalnızca aynı göçte siparişler ve müşterilerin de içe aktarılması durumunda içe aktarılabilir, çünkü komisyonlar ve ödemeler belirli siparişler ve müşterilere bağlıdır.

Yükleme için:

1. 3. adımda, eklenti zaten site üzerinde algılanmamışsa, **Köprü Eklentisini İndir** butonu ve yükleme talimatları görünecektir
2. Eklentiyi ZIP olarak indirin
3. WordPress'te **Eklentiler > Yeni Ekle > Eklenti Yükle**, ZIP'i seçin, **Şimdi Yükle**'ye tıklayın, sonra **Etkinleştir**
4. Spwig sihirbazına geri dönün ve sayfayı yenileyin — bir **Ortaklıklar** onay kutusu ve bir **Ortaklık Programı Verisi** bloğu görünecek, bulunan sayılar gösterilecektir

Göçünüz tamamlandıktan sonra WordPress'ten Köprü eklentisini devre dışı bırakabilir ve kaldırabilirsiniz.

## WooCommerce Eklenti Desteği

Mağazanız belirli popüler eklentileri kullanıyorsa, onların oluşturduğu ürünler içe aktarma sırasında tanınır ve Spwig'de eşleşen özelliklere eşlenir, yalnızca düz ürünler olarak değil:

| WooCommerce eklentisi | Konumlanır |
|---|---|
| Abonelikler | Spwig abonelik planları |
| Ürün Ekleme Seçenekleri | Spwig ürün ekleme seçenekleri |
| Ürün Paketleri | Spwig ürün paketleri |
| Hediye Kartları (WooCommerce, YITH ve PW sürümleri) | Spwig hediye kartları |
| Bileşik Ürünler | Spwig bileşik ürünler |
| Rezervasyonlar ve Konaklama Rezervasyonları | Spwig rezervasyonları |

> **Not:** Eklenti verisi içe aktarma asla temel ürünün oluşturulmasını engellemez. Eğer bir ürünün eklentiye özel verisi okunamazsa, ürün hala içe aktarılır — yalnızca bir normal ürün olarak, abonelik, paket, rezervasyon veya hediye kartı yapılandırması olmadan.

İçe aktarma sonrası abonelik, paket, rezervasyon ve hediye kartı ürünleri inceleyin, eklentiye özel ayarlarının doğru aktarıldığını doğrulayın, başarıyla içe aktarma tamamıyla tüm detayları taşıdığını varsaymak yerine.

## Özel Alanlar

WooCommerce ürünleri, müşterileri veya siparişlerinize özel meta alanlar eklediyseniz, Spwig her türden yaklaşık on kaydı örnekleyerek hangi alanların bulunduğunu tespit eder. Her birini 4. adımda Spwig özel alan yuvasına veya genel Meta Veri alanına eşleyeceksiniz. [Göç Alanı Eşleme](migration-field-mapping) tam yol göstericisini görmek için buraya tıklayın, eşlemelerin gelecekteki göçler için nasıl kaydedildiğini de içerir.

## İçeriği Aktarma

3. adımı gözden geçirdikten ve 4. adımda eşlemelerinizi onayladıktan sonra içe aktarmayı başlatın. Arka planda çalışır — tarayıcı penceresini kapatıp da devam eder. 5. adımda her veri türü (kategoriler, ürünler, müşteriler, siparişler, incelemeler, kuponlar, blog gönderileri ve Köprü eklentisi kullanılmışsa ortaklıklar/komisyonlar/ödemeler) için canlı ilerleme ve genişletilebilir aktivite günlüğü gösterir.

6. adımda sonuçlarınızı görürsünüz: ne içe aktarıldı, atlandı veya başarısız oldu, ayrıca içe aktarılan içerikte eski WooCommerce etki alanına yönelik iç bağlantılar bulunursa bir **Bağlantı Yeniden Yazma** aracı da gösterilir.

Özetleri dikkatlice inceleyin, ardından [After Your Migration](after-migration-review) başlığındaki kontrol listesini tamamlayın — bu, verilerinizi doğrulamak, vergi oranlarını ve kargonuzu ayarlamak (bu işlemi sihirbaz yapılandırmaz) ve iç bağlantıları yeniden yazmak konularını kapsar.

## API Anahtarınızı İptal Edin

Göçünüzün başarıyla tamamlandığını doğruladıktan sonra, WordPress'te **WooCommerce > Ayarlar > Gelişmiş > REST API**'ye gidin ve Spwig için oluşturduğunuz anahtarı iptal edin veya silin. Göçünüz tamamlandıktan sonra eski mağazanızda aktif bir API anahtarı bırakmak hiçbir sebep yoktur.

## İpuçları

- **API anahtarını ihtiyaç duyduğunuzda hemen oluşturun** — Tüketici Gizli anahtarı yalnızca bir kez gösterilir, bu nedenle 2. adımı başlatmadan hemen önce oluşturun, önceden oluşturmak yerine.
- **Sadece okuma hakkı yeterlidir** — Yazma veya Okuma/Yazma izinlerini asla verin; Spwig, WooCommerce mağazanızdan yalnızca okuma yapar.
- **İçe aktarma işlemine başlamadan önce Bridge eklentisini yükleyin** — İçe aktarma öncesi eklemek ve sihirbazı yeniden başlatmak gerekir, bu yüzden baştan kontrol edin, işlem sırasında değil.
- **Uzantı tabanlı ürünleri kontrol edin** — abonelikler, paketler, rezervasyonlar ve hediye kartları, içe aktarma sonrası elle kontrol edilmesi gereken en olası ürünlerdir.
- **Kısmi bir içe aktarma otomatik olarak temizlenmez** — başarısız bir içe aktarma tekrar denemeden önce [Migration Troubleshooting](migration-troubleshooting)'i inceleyin.
- **İşlem tamamlandıktan sonra API anahtarını iptal edin** — Göçten uzaklaşmış bir mağazada eski entegrasyonları aktif bırakmayın.