---
title: AI Alışverişi
---

AI Alışverişi, AI alışveriş asistanlarının ürünleri bulmanıza ve izin verdiğinizde, bir müşterinin adına mağazanızdan satın almasına olanak tanır. Bu özellik **varsayılan olarak kapalıdır** — açmak bilinçli bir tercihtir ve bunu yapana kadar, mağazanız bu asistanlar için hiçbir şey sunmaz.

## Açmak

**Ayarlar → AI Alışverişi**'i açın ve **Agensiyel ticaret etkin**'i açın. Bu noktadan sonra, Universal Commerce Protocol'u destekleyen asistanlar mağazanızı bulabilir ve kataloğunu okuyabilir. Kullanıcının normal mağazası hakkında hiçbir şey değişmez.

## Hazır olma panosu

AI Alışverişi sayfasının üst kısmı, tek bir cümlede bir soruya cevap verir: **AI asistanları, mağazanızdan şu an satın alabilir mi?**

- **"AI asistanları mağazanızdan satın alabilir"** — bir satın alma için gerekli her şey mevcut.
- **"AI asistanları mağazanızı inceleyebilir, ancak henüz satın alamaz"** - mağazanız mevcuttur, ancak bir satın alma tamamlanmadan önce bir şey eksik olabilir (genellikle bağlı bir ödeme sağlayıcısı).
- **"Acil durum kapatma (Emergency stop) açık"** veya **"Agensiyel ticaret kapalıdır"** - asistanlar için hiçbir şey sunulmuyor.

Yargıdan sonra kısa bir kontrol listesi görürsünüz - ödeme sağlayıcısı bağlı, kargo fiyatlandırması yapılabilir, ürünler asistanlar için görünür - herhangi birinin hâlâ dikkat çekerken bir ipucu var. Sayılar, asistanların satabileceği ürün sayısını, onlardan gizlediğiniz ürün sayısını, ziyaret eden asistan sayısını ve bloke ettiğiniz asistan sayısını gösterir.

Kontrol listesi, **canlı** kurulumunuzu yansıtır: bir ödeme sağlayıcısı bağlayın veya bir kargo yöntemi ekleyin ve bir sonraki seyahat ettiğinizde yargı güncellenir.

## Acil durum kapatması

**Acil durum kapatması**, ana anahtardan ayrı bir anahtardır. Herhangi bir şeyin yanlış göründüğü bir durumda, yapılandırmanızı çözmeden hemen tüm asistan aktivitesini durdurmak için kullanın. Temizlemek için yeniden başlatın. Ana anahtarı "bu özellik ayarlandı mı" olarak düşünün ve acil durum kapatmasını "hemen her şeyi durdur" olarak düşünün.

## Asistanların yapabileceğiler

İkisi de ayrı ayrı kontrol edilen iki erişim seviyesi:

- **Okuma** (keşfetme ve inceleme) daha düşük risklidir. Bir asistan mağazanızı bulabilir ve ürün detaylarını okuyabilir.
- **Ödeme** (aslında satın alma) daha yüksek maliyetlidir ve doğrulanmamış asistanlar için açık kalmaz, sadece izin verdiğinizler için açılır.

Bir mağaza, satın alma olanağı olmayan bir şekilde keşfedilebilir - bu, başlamak için yararlı bir yoldur.

## Belirli Ürünleri Gizleme

Her ürünün bir **AI alışveriş ajansları için görünür** ayarı vardır (varsayılan olarak açıktır). Ürünü asistanlardan uzaklaştırmak için kapatın, fakat mağazanızan devam ederken - kendi web sitemiz aracılığıyla satarak tercih ettiğiniz ürünler için yararlıdır.

## Bireysel Asistanları Yönetme

Bir asistan ilk kez satın alırsa - ya da deneseydi - Spwig bunu **AI Alışverişi → Ajans Kimlikleri** altında kaydeder. Her giriş, asistanın doğrulanmış evi (kimlik doğrulaması yapan dizin), güven seviyesi ve ne kadar istek yapmış olduğuna dair bilgileri gösterir. Bir asistanın sunduğu isim ve logo, sadece *konusu* bilgileridir - kimlik doğrulaması olarak değil, bir etiket olarak kabul edin; doğrulanmış ev, güvenilir olan kısımdır.

Her asistan, üç güven seviyesinden birinde yer alır:

| Güven seviyesi | Ne anlama gelir |
|---|---|
| **Sınırlı (doğrulanmış, sınırlı)** | Yeni bir asistan için varsayılan. Spwig, kimliğini kaydetti ve politikasında belirtilen sıralama değeri sınırı, harcama sınırı ve ödeme kısıtlamalarını taşır (aşağıya bakınız). |
| **Doğrulanmış (sınırlar kaldırıldı)** | Bu asistanı tamamen güvence altına almak için sizi bir tercih. Sıralama değeri ve günlük harcama sınırları temizlenir. |
| **Engellenmiş** | Asistan, mağazanızdan satın alamaz. Açık ödeme işlemleri sona erer, ancak zaten alınan ödeme hiçbir şey değişmeden kalır. |

Bir asistanı durdurmak için listede onu seçin ve **Seçilen Ajansları Engelle**'yi seçin. **Seçilen Ajansları Aç** her zaman onu **Sınırlı**'ya döndürür - doğrulanmış olmaya - çünkü sınırların kaldırılması ayrı bir, bilinçli adımdır.

Bir asistanın sınırlarını tamamen kaldırmak için, onu seçin ve **Doğrulanmış (sınırlar kaldırıldı) olarak yukarı çıkar**'ı seçin.

Bu, maksimum sipariş değerini ve günlük harcama sınırını kaldırır ve asistanı Verified (Doğrulanmış) durumuna geçirir.

Engellenmiş bir asistan atlanır — önce onu engelini kaldırın, ardından ilerletin.

Bu, gerçek bir güven kararı olarak kabul edilmelidir: doğrulama, yeni bir asistanın sahip olduğu koruyucu kriterleri kaldıracağı için, güvenip güvenemeyeceğiniz konusunda emin olduğunuz bir asistanı ilerletin.

## Bir asistanın sınırlarını ayarlamak

Bir asistanın ne yapmaya ne izin verdiğini ayarlamak için asistanın detay sayfasını açın ve **Politika (sınırlar ve izin verilen teklifler)** bölümünü kullanın:

| Alan | Neyi kontrol eder |
|---|---|
| **Maksimum sipariş değeri** | Bu asistanın yapabileceği en büyük tek seferdeki sipariş. Sınır koymamak için boş bırakın. |
| **Günlük harcama sınırı** | Bu asistanın bir günde tüm siparişler üzerinden harcayabileceği en fazla miktar. Sınır koymamak için boş bırakın. |
| **İndirim kodlarını kabul et** | Mağaza çıkışında kupon kodlarını uygulayabilir mi? |
| **Hediye kartlarını kabul et** | Hediye kartlarını kullanabilir mi? |
| **Dijital ürünler** | Dijital ürünler alabilir mi? |
| **Sorgu hızı (dakika başına)** | Mağazanıza olan sorgu sayısı (dakika başına). |

Yeni bir asistan, somut sipariş değeri ve harcama sınırlarıyla başlar ve indirim kodları, hediye kartları ve dijital ürünler kapalı olur — kasten tutucu varsayılan. Bu alanlardan herhangi birini değiştirin ve kaydedin; her değişiklik **Agent Events**'e kaydedilir ve önceki ve sonraki değerlerle birlikte, kimin neyi ve ne zaman değiştirdiğine dair her zaman bir kayıt olur. Bir asistanı Verified (Doğrulanmış) durumuna getirmek, onun Maksimum sipariş değerini ve Günlük harcama sınırını sizi için kaldırır — onları elle boşaltmak zorunda kalmazsınız.

## Etkinlik kaydı

**AI Shopping → Agent Events**, asistanların ne yaptığının, doğrulanmış her talep, engellenen her girişim, ve hangi değişikliği yaptığınızın kanıtlarını içeren, değiştirilemeyen ve silinemeyen bir kayıttır. Bir asistanın yaptığı bir satın alma asla tartışılmasa da, bu kanıt izni olur.

## Asistan platformları hakkında bir not

Bu asistanları çalıştıran şirketler (ve onlarda yer almak için gerekli kurallar) yeni ve sık sık değişir. Ürünlerinizin onlar aracılığıyla alınmasına izin verilmesi için bazılarının sizin bir başvuru yapmanızı veya bölgesel koşulları karşılamanızı gerektirebilir. Spwig, mağazanızı hazırlar; belirli bir asistanın sizi listelemesi onun sorumluluğundadır.

Tüm markdown biçimlendirmesini, resim yollarını, kod bloklarını ve teknik terimleri koruyun.