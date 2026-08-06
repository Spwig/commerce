---
title: Hediyelik Kartlar
---

Hediyelik kartlar, müşterilerin başkaları için ya da kendileri için satın alabileceği mağaza kredisidir. Bu kartlar, benzersiz bir kupon kodu olarak e-posta ile gönderilir. Ayrıca, bir müşteri satın alma olmadan admin panelinden doğrudan bir hediyelik kartı da çıkarabilirsiniz.

Hediyelik kartları satışa sunulmuştur. Bir müşteri bir hediyelik kartı satın alırsa, ödeme onaylandıktan sonra kart otomatik olarak oluşturulur ve e-posta ile gönderilir. Ödemenin başarısız olması durumunda hiçbir kişi bir kod alamaz.

Bir hediyelik kartı ürününü etkinleştirmeden önce bazı önemli noktaları öğrenmelisiniz:

- **Hediyelik kartları para, bir indirim değildir.** Vergi ve kargo ücretlerinden sonra fatura üzerinden düşer ve vergi borcunuzu azaltmaz. Bu, ürün fiyatını düşüren bir kuponun aksine çalışır.
- **Kartlar tek bir para birimine sahiptir.** Avroda satın alınan bir kart sadece avroluk bir siparişte kullanılabilir. Birden fazla para birimiyle satış yaparsanız, her biri için ayrı bir hediyelik kartı ürünü oluşturun. Bu, bir yıl boyunca harcanmayan bir bakiyeye döviz kuru değişimlerinden korur.
- **Hediyelik kartları indirimle birlikte kullanılamaz.** Bir kupon, hediyelik kartı satırına uygulanamaz çünkü 100 £ kredi 80 £ karşılığında satmak her satışta 20 £ kaybetmenize neden olur.
- **Bir hediyelik kartı başka bir hediyelik kartı satın alamaz.** Bu, çalınan kart bilgilerini yıkamak için kullanılan bir yolu kapatır.
- **Bir hediyelik kartı satın almak sadakat puanı kazandırmaz.** Puanlar, kartın ürünlerde harcanmasıyla kazanılır, bu nedenle aynı para ile iki kez puan kazanmak mümkün değildir.

![Hediyelik kart yönetimi](/static/core/admin/img/help/gift-cards/gift-card-list.webp)

## Miktar Türleri

Bu ayarlar, bir müşteri hediyelik kartı satın alırken miktarı nasıl seçebileceğini kontrol eder:

| Tür | Açıklama |
|------|-------------|
| **Sabit Miktarlar** | Müşteriler, önceden belirlenmiş miktarlardan (örneğin, $25, $50, $100) seçim yapar |
| **Özel Miktar** | Müşteriler, belirli bir min/max aralığı içinde herhangi bir miktar girer |
| **Her İkisi** | Önceden belirlenmiş miktarlar ve özel miktar seçeneği sunulur |

## Hediyelik Kartı Ürünü Oluşturma

Her hediyelik kartı, sonunda satılacak ya da bugün elle verilecek olsa bile, arkasında bir Hediyelik Kartı türünden ürün olmalıdır.

### Adım 1: Ürünü Ayarla

1. **Ürünler > Tüm Ürünler** menüsüne gidin ve **+ Ürün Ekle**'ye tıklayın
2. **Ürün Türünü** **Hediyelik Kartı** olarak ayarlayın
3. Ürün adını ve açıklamasını doldurun
4. Miktar ayarlarını yapılandırın:
   - **Miktar Türünü** seçin (Sabit, Özel veya Her İkisi)
   - Sabit için, kullanılabilir miktarları ayarlayın
   - Özel için, **Minimum** ve **Maksimum** izin verilen miktarları ayarlayın
5. **Sonuç Günlüğü** (0 = asla bitmez) ayarlayın — bu, hediyelik kartlarının satın alınmasından sonra geçerli olduğu süreyi belirler
6. Ürünü kaydedin ve yayınlayın

### Adım 2: Yayınla

Ürünü satmaya hazır olduğunuzda yayınlayın. Müşteriler, mağazanızın ön yüzünden hemen satın alabilirler ve ödeme onaylandıktan sonra kart otomatik olarak e-posta ile gönderilir.

Bu ürün, elle bir kart çıkarırken seçebileceğiniz şeydir — bu nedenle, sadece her zaman kartlar vermek planladığınız için bile bir tane oluşturmak değerlidir.

## Elle Hediyelik Kartı Oluşturma

Şu anda bir fonlanmış hediyelik kartı oluşturmanın tek yolu budur ve bugün tamamen çalışır.

1. **Ürünler > Hediyelik Kartlar** menüsüne gidin ve **+ Hediyelik Kartı Ekle**'ye tıklayın
2. **Ürünü** seçin — bu, mevcut bir Hediyelik Kartı türünden ürün olmalıdır (yukarıdaki adımları bkz.)
3. **Başlangıç Değeri** girin — başlangıç bakiyesi, istediğiniz herhangi bir miktar olabilir. Müşteri satın almasından farklı olarak, bu ürünün miktar ayarlarına sınırlı değildir
4. İsteğe bağlı olarak bir **Son Kullanım Tarihi** belirleyin ve **Aktif** kutusunu işaretleyin, böylece kartın kupon olarak kullanılabilir olur
5. Aynı sayfada daha aşağıda yer alan **Alıcı** bölümüne bilgileri girin:
   - **Alıcı E-postası** — zorunludur; gönderilecek e-posta adresi
   - **Alıcı Adı**, **Gönderen Adı** ve **Kişisel Mesaj** — hepsi isteğe bağlıdır
   - **Planlı Gönderim Tarihi** — isteğe bağlıdır; boş bırakın ve her zaman gönderin ya da gelecekte bir tarih ve saat belirleyin (örneğin, bir doğum günü)
6. **Kaydet**'e tıklayın

Kupon kodu otomatik olarak oluşturulur ve başlangıç bakiyesi, Başlangıç Değeri'nden ayarlanır — bunlardan hiçbiri kendiniz tarafından doldurulmaz.

**Kartı kaydetmek e-posta göndermez.** Göndermek için hediye kartı listesine geri dönün, kartın onay kutusunu seçin, **Hediye kartı e-postaları gönder** seçeneğini **Eylemler** açılır menüsünden seçin ve **Devam**'a tıklayın.

Aynı eylem, daha sonra e-postayı yeniden göndermek isterseniz e-postayı yeniden gönderir.

## Yönetici Panelinde Hediye Kartlarını Yönetme

**Ürünler > Hediye Kartları**'na giderek tüm hediye kartlarını yönetin:

### İstatistikler Paneli

Sayfanın üst kısmında, dört kart ana ölçüleri gösterir:

- **Toplam Hediye Kartları** — Verilen toplam hediye kartları sayısı
- **Aktif** — Mevcut bakiyesi olan aktif kartlar
- **Toplam Bakiye** — Tüm kartlardaki kalan bakiyelerin toplamı
- **Kısmen Kullanılmış** — Kısmen kuponlanan kartlar

### Filtreler

Hediye kartlarını aşağıdaki kriterlere göre filtreleyin:

- **Arama** — Kod, e-posta veya alıcı adı ile arama yapın
- **Durum** — Aktif, Pasif, Süresi Dolmuş, Tamamen Kullanılmış veya Kısmen Kullanılmış
- **Bakiye** — Bakiye Var veya Bakiyesiz
- **Oluşturulma Tarihi** — Zaman aralığı (Bugün, Bu Hafta, Bu Ay, Bu Yıl)

### Hediye Kartı Detayları

Her hediye kartı aşağıdaki bilgileri gösterir:

- **Kod** — Tekil kupon kodu (örneğin, GC-XXXX-XXXX-XXXX)
- **Alıcı** — E-posta ve isim
- **Durum etiketleri** — Renk kodlamalı mevcut durum
- **Bakiye / Başlangıç / Kullanılan** — Yüzdelik kullanım ile finansal özeti
- **Ana tarihler** — Oluşturulma, verilme, ilk kullanım tarihi
- **Gönderen** — Hediye kartını satın alan (veya veren) kişi

### Eylemler

- Bir hediye kartını seçerek **düzeltme** detaylarını ve tam **işlem geçmişini** aynı sayfada inline olarak görüntüleyin
- Bir veya daha fazla kartı seçin ve **Eylemler** açılır menüsünü kullanarak **Hediye kartı e-postaları gönder** (gönderir veya e-postayı yeniden gönderir) veya **Seçilen hediye kartlarını pasif yap** (pasif hale getirir — bakiye korunur ancak kart artık kuponlanamaz)

## Bugün Kuponlama

**Mağazada**, Satış Noktası terminalinizde:

1. Kasiyer, ödeme adımı sırasında kodu alır
2. Kod doğrulanır — aktif, süresi dolmamış, bakiye var ve satışın aynı para biriminde
3. Bakiye, ödenecek toplam tutara uygulanır, vergi ve kargo dahil
4. Eğer bakiye tüm satış tutarını karşılamıyorsa, müşteri kalan kısmı başka bir şekilde öder
5. Bakiye düşer ve işlem kaydedilir

Kasiyer, **ödeme** sırasında kodu alır, sepeti oluştururken değil. Hediye kartı, müşteri tarafından zaten verilen para olduğu için faturayı kapatır, ürünleri indirmez.

**Çevrimiçi**, ödeme adımı sırasında ödeme aşamasında hediye kartı alanı vardır. Müşteri kodunu girer, bakiye, vergi ve kargo sonrası olan tutardan düşülür ve kalan tutar kredi kartına normal şekilde tahsil edilir. Eğer kart tüm siparişi karşılıyorsa, başka bir ödeme gerekmez. Bakiye, ödeme onaylandıktan sonra gerçekten düşer, bu nedenle terk edilen bir ödeme işlemi kartı asla etkilemez.

Alıcılar, teslimat e-postasındaki bağlantı üzerinden her zaman kalan bakiyelerini kontrol edebilir.

## İade İşlemleri

Hediye kartı kullanan siparişler veya satışları iade ettiğinizde:

- **Müşteri tarafından satın alınmış, henüz kullanılmamış bir hediye kartı** — Kart pasif hale getirilir ve bakiyesi sıfırlanır, bu nedenle kredi ve iade birlikte kaybolur.
- **Müşteri tarafından satın alınmış ve kısmen harcanmış bir hediye kartı** — Bu durumda kararınıza bağlıdır. Kartı pasif hale getirmek, zaten harcanan krediyi geri alır, bu nedenle bakiye olduğu gibi bırakılır ve el ile ayarlamak için işaretlenir.
- **İade edilen siparişi ödemek için kullanılan bir hediye kartı** — İade, önce kartta yapılır, ardından herhangi bir kredi kartı veya banka ödemesi. Bankaya iade edilen para, satıcı tarafından asla toplanmamışsa daha kötü bir hata olur ve değer, geldiği yerden iade edilerek bilinen bir dolandırıcılık yolu kapatılır. Eğer orijinal kart artık süresi dolduysa veya pasif hale getirildiysa, aynı alıcıya süresiz bir kart verilir.
- **Tam iade** — İade işlemi aracılığıyla hediye kartı bakiyesine tutarı geri yazın

## İpuçları

Tüm markdown biçimlendirmesini, resim yollarını, kod bloklarını ve teknik terimleri koruyun.

- İyiliyet kredileri, müşteri hizmetleri çözümleri veya bir müşteriye mağaza kredisi vermek isteyebileceğiniz herhangi bir durumda el ile kredi verme özelliğini kullanın.
- Yerel hediye kartı düzenlemelerine uyum sağlamak için makul bir son kullanma periyodu belirleyin (örneğin 365 gün) — bazı yasal alanlar minimum geçerlilik dönemleri gerektirir.
- Kolaylık (ön tanımlı tutarlar) ve esneklik (özel bir tutar) sunmak için "Her İkisi" adı altında kredi türünü kullanın.
- Toplam Bakiye metrik değerini düzenli olarak izleyin — bu, kitabınızdaki bir borçlu durumu temsil eder.
- Bir kart çevrimiçi ve fiziksel olarak aynı şekilde harcanır — web ödeme sırasında ödeme adımı veya kasada.

Teslimat e-postası, alıcıların herhangi bir zaman bakiye kontrolü yapmak için kullanabileceği bir bağlantı içerir.
- Eğer birden fazla ülkeye müşteri satıyorsanız, belirli döviz cinslerinde hediye kartı verebilirsiniz — ayrıntılar için **Çok Dövizli Hediye Kartları** yardım konusuna bakın.