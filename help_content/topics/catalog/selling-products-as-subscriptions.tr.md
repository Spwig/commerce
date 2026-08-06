---
title: Ürünleri Abonelik Şeklinde Satma
---

Herhangi bir Basit, Değişken ya da Dijital ürün artık tek seferlik bir satın alma ile birlikte - ya da yerine - sadece periyodik olarak satılabilir. Bu kılavuz, bir ürün için abonelikleri açma, müşterilerin seçebileceği planları seçme ve müşterilerin ne sattığını ne gördüğünü kapsar.

<!-- screenshots-needed:
- url: /admin/catalog/product/{id}/change/
  filename: subscriptions-tab.webp
  description: Ürün düzenleme formu ile "Abonelikler" sekmesi aktif, "Abonelik Aç" onay kutusu seçili, "Abonelik Planları" alanında bir ya da daha fazla plan seçili ve "Tek Seferlik Alışveriş / Abonelik Olarak Varsayılan" onay kutuları görünür.
  save-to: core/static/core/admin/img/help/selling-products-as-subscriptions/
  viewport: 1440x900
- url: (mağaza arayüzü) abonelikli bir ürünün detay sayfası
  filename: subscribe-and-save-selector.webp
  description: Mağaza arayüzünde "Tek seferlik Alışveriş" ile "Abone Ol ve Korumak" seçimi, indirimli seviyelerdeki bir teslim sıklığı seviye listesiyle birlikte, indirimli seviyelerde %X Korumak etiketiyle genişletildi.
  save-to: core/static/core/admin/img/help/selling-products-as-subscriptions/
  viewport: 1440x900
  notes: Abonelikli bir ürünle birlikte en az bir tane aktif kamuya açık plan ve fiyatlandırma seviyesine sahip olmalı, yönetici yerine mağaza arayüzünden incelenmeli.
-->

## Hangi Ürün Türleri Abonelik Şeklinde Satılabilir

Abonelikler sadece şu ürün türleri için mevcuttur:

| Uygun | Uygun Değil |
|------|-------------|
| Basit Ürün | Ürün Paketi |
| Değişken Ürün | Hediye Kartı |
| Dijital Ürün | Özelleştirilebilir Ürün |
| | Yapılandırılamaz Ürün |
| | Rezervasyon Ürünü |

Neden teslimat, fiyatlandırma değil: bir abonelik, her döngüde müşteriye yeniden faturalandırır ve her seferinde yeni bir siparişle ürünün yeniden teslim edilmesini sağlar. Spwig, Basit ya da Değişken ürünün yeniden sevki ve her yenilemede Dijital ürünün indirimi veya lisansının yeniden verilmesini bilir — ancak bir hediye kartının yeniden oluşturulması, çok bileşenli bir paket, bir müşterinin kayıtlı özelleştirmesi, bir yapılandırıcı kurulumu veya bir rezervasyon yeri için tekrarlayan bir düzene göre güvenli bir şekilde yeniden çalıştırma imkanı yoktur. Bu tür ürünleri abonelik şeklinde satmaya izin vermek, 2. döngüde müşteri parasını alırken hiçbir şey teslim edememe riskini doğurur.

**Abonelik Aç** onay kutusu, uygun olmayan türler için gizli veya gri çıkarılmamıştır — her ürün üzerinde teknik olarak işaretlenebilir. Abonelikler açıkken Hediye Kartı, Paket, Özelleştirilebilir, Yapılandırılamaz ya da Rezervasyon ürünü gibi bir ürünün kaydını denerseniz, Spwig, bu ürün türünün abonelik şeklinde satılamayacağını açıklayan bir doğrulama hatası ile kaydı reddedecektir. Önce **Ürün Türü** 'nü değiştirin (Temel Bilgiler sekmesi), ya da bu ürün için abonelikleri kapatın.

## Ürün Üzerinde Abonelikleri Açma

1. **Ürünler > Tüm Ürünler** 'e gidin ve abonelik şeklinde satmak istediğiniz ürünü açın (ya da yeni bir tane oluşturun).
2. Temel Bilgiler sekmesindeki **Ürün Türü** 'nü Basit, Değişken ya da Dijital olduğundan emin olun.
3. **Abonelikler** sekmesine tıklayın.
4. **Abonelik Aç** 'ı seçin.
5. **Abonelik Planları** alanında, bu ürünün sunduğu planları seçin. Henüz bir plan oluşturmadıysanız, önce [Abonelik Planları](/help/subscription-plans) 'a bakın.
6. Aşağıdaki iki satın alma modu onay kutusunu yapılandırın.
7. **Kaydet** 'e tıklayın.

## Abonelik Planlarını Bağlama

Bir **Abonelik Planı**, ödeme sıklığı seçenekleri, deneme, kurulum ücreti, iptal kuralları gibi - bir kez oluşturduğunuz ve herhangi bir sayıda uygun ürüne bağlayabileceğiniz bir şablondur. Ürünün **Abonelikler** sekmesindeki **Abonelik Planları** alanı, ürünün plan(lar) ile ne tür bir abonelikle satılacağını bağlamak içindir.

Aynı produkte birden fazla planı bağlayabilirsiniz.

Örneğin, aynı item için "Standart" ve "Premium" tekrarlayan seviyeleri sunmak isterseniz, her planın kendi fiyatlandırma seviyeleri, deneme ve iptal politikası olabilir.

Tüm markdown formatını, resim yollarını, kod bloklarını ve teknik terimleri koruyun.

Abonelikler sekmesindeki iki onay kutusu, müşterilerin ürününüzü nasıl alabileceğini kontrol eder:",
    "list_1": [
      "**Bir Kez Alım İzni** — Varsayılan olarak açık. Seçildiğinde, müşteriler normal bir bir defalık alım ve abone olma arasında seçim yapar. Ürünü abonelikli hale getirmek için bunu kapatın - her satın alma, tekrarlayan bir sipariş haline gelir ve hiçbir bir defalık seçenek gösterilmez.",
      "**Abonelik Olarak Varsayılır** — Ürün sayfası açıldığında, müşterilerin aktif olarak seçim yapmasına gerek kalmadan abonelik seçeneğini (ve varsayılan plan/düzeyini) önceden seçer. Bu ayar sadece **Bir Kez Alım İzni** seçiliyken geçerlidir - bir kezlik alım kapalıysa, bu ayar ne olursa olsun ürün abonelikli olur."
    ],
    "text_2": "Tekrarlayan teslimatın doğal beklentisi olduğu ürünler (kahve, takviyeler, tüketilebilirler) için **Abonelik Olarak Varsayılır** kullanın - müşterilerin tekrar gelmesini sağlayan seçeneğe yönelmek için bir tıklamayı kaldırır, ancak bir kere satın alma yeteneklerini kademeli olarak kaldırır."
  },
  "section_2": {
    "title": "Müşterilerin Nerede Görüntülediğini",
    "sub_section_1": {
      "title": "Ürün sayfasında",
      "text": "Bir ürünün abonelikleri etkinleştirilmiş ve en az bir adet aktif, kamuya açık planı varsa, bir satın alma modu seçici ürün sayfasında görünür:",
      "list_2": [
        "Bir kezlik alım izni varsa, müşteriler **"Bir kezlik alım"** ve **"Abone Ol ve Korumak"** arasında bir seçim görür, varsayılan olarak hangi modu yapılandırdığınızdır.",
        "Ürünün birden fazla planı varsa, **"Abone Ol ve Korumak"** seçildiğinde bir plan seçici görünür.",
        "Seçilen plan için, müşteriler planın fiyatlandırma seviyelerinden oluşturulan bir **teslim sıklığı** listesi görür (örneğin, Aylık, Çeyreklik, Yıllık), her biri için **"X% Kadar Korumak"** etiketi varsa fiyatını ve bir **"X% Kadar Korumak"** etiketi görür.",
        "Trial süresi, kurulum ücreti ve planın iptal politikası (örneğin, "Her zaman iptal edilebilir") seviye listesiyle birlikte gösterilir ve ödeme yönteminin ödeme anında eklendiğine dair bir not yer alır."
      ]
    },
    "sub_section_2": {
      "title": "Sepet ve ödeme anında",
      "text": "Abonelik satırı sepette **Abonelik** etiketiyle, ödeme sıklığı (örneğin, "Her ay") ve bir trial notu varsa, müşteriye tekrar eden satırların hangileri olduğunu açıkça belirtir. Ödeme anında, müşteri normalde olduğu gibi bir ödeme sağlayıcısı seçer - bu, gelecekteki yeniden tedariklerde tahsil edilecek ödeme yöntemidir.",
      "note": "> **Bilinen sınırlama:** Bazı ödeme sağlayıcıları için müşteri kartının otomatik olarak ödeme anında yeniden tedarikler için saklanması hâlâ bağlanmaktadır. Belirli bir sağlayıcı bu özelliği desteklemeyecek olursa, bu sağlayıcı üzerinden yapılan aboneliklerin yeniden tedariklerinin otomatik olarak tahsil edilmediğini fark ettiğinizde, bir sonraki yeniden tedarikten önce müşteriye güncel ödeme bilgilerini istemek gibi ekstra takip yapmak zorunda kalabilirsiniz. İlk günden itibaren tamamen elden verilmemiş olur. Aboneliklerin yeniden tedariklerinin otomatik olarak tahsil edilmediğini fark ederseniz, ödeme sağlayıcınızla ilgili kurulumunuzu kontrol edin."
    }
  },
  "section_3": {
    "title": "İpuçları",
    "list_3": [
      "Öncelikle abonelik planını oluşturun ve test edin (fiyat seviyeleri, deneme, iptal politikası), ardından bu planı ürünleriyle ilişkilendirin - planı daha sonra birkaç ürün arasında düzeltmekten daha kolaydır.",
      "Çoğu ürün için **Bir Kez Alım İzni**'nı açık bırakın. Bir kezlik alımın gerçekten işinize yaramadığı durumlar için abonelikli ürünleri saklayın.",
      "Mevcut bir en çok satan ürünü bir abonelik seçeneğine dönüştürüyorsanız, önce müşterilerin bir kez satın alma alışkanlıklarını bozmamak için **Abonelik Olarak Varsayılır**'ı kapatın - aboneliklerin nasıl davrandığını gördükten sonra daha sonra açın.",
      "Dijital ürünler, yeniden tedarikin otomatik olarak erişimi yeniden verdiğini ve kargo içermeyen bir şey olduğu için abonelikler için harika bir uygundur (yazılım lisansları, içerik üyelikleri).",
      "Bir ürün türünün (örneğin, bir paket veya özelleştirilebilir bir ürün) tekrarlayan bir şekilde satılamayacağını düşünüyorsanız, abonelik yerine daha basit bir Basit ya da Dijital eşdeğerinin olup olmadığını düşünün.