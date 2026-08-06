---
title: AI Alışveriş
---

AI Alışveriş, AI alışveriş asistanlarının ürünleri bulmasına ve sizin onlar adına mağazanızdan satın almasına olanak tanır. Bu özellik **varsayılan olarak kapatılmıştır** — bunu açmak bir amaçlı seçimdir ve bunu yapmadığınız sürece mağazanız bu asistanlara hiçbir şey ifşa etmez.

## Açma

**Ayarlar → AI Alışveriş** menüsünü açın ve **Ajentik ticaret etkin** anahtarını açın. Bu noktadan sonra Universal Commerce Protocol'u destekleyen asistanlar mağazanızı bulabilir ve kataloğunuzu okuyabilir. Normal mağazanızla ilgili hiçbir şey değişmez.

## Hazırlık paneli

AI Alışveriş sayfasının üst kısmı, şu an bir cümle ile tek bir soruyu yanıtlar: **AI asistanlarının şu anda mağazanızdan gerçekten satın alabiliyor mu?**

- **"AI asistanları mağazanızdan satın alabilir"** — satın alma için gereken her şey yerinde.
- **"AI asistanları mağazanızı tarayabilir, ancak henüz satın alamaz"** — mağazanız keşfedilebilir, ancak satın alma tamamlanabilmesi için bir şey eksik (genellikle bağlı bir ödeme sağlayıcısı).
- **"Acil durum durdurma açık"** ya da **"Ajentik ticaret kapatık"** — asistanlara hiçbir şey sunulmuyor.

Karar vermenin altına kısa bir kontrol listesi yer alır — ödeme sağlayıcısı bağlı, kargo ücreti verilebilir, ürünler asistanlara görünür — herhangi bir dikkat gerektiren şeyin yanında bir ipucu vardır. Sayıcılar, asistanların satabileceği ürün sayısı, onlardan gizlediğiniz ürün sayısı, ziyaret eden asistan sayısı ve engellediğiniz asistan sayısını gösterir.

Kontrol listesi, **yaşanılan** yapılandırmayı yansıtır: bir ödeme sağlayıcısı bağlayın veya bir kargo yöntemi ekleyin ve karar verme, sayfayı tekrar açtığınızda güncellenir.

## Acil durum durdurma

**Acil durum durdurma**, ana anahtardan ayrı bir anahtardır. Onu kullanarak, yapılandırmayı bozmadan tüm asistan etkinliklerini hemen durdurabilirsiniz — örneğin bir şeyin yanlış gibi görünmesi durumunda. Temizleyerek tekrar başlatılabilir. Ana anahtarı "bu özellik yapılandırılmış mı?" olarak düşünün ve acil durum durdurmayı "şimdi her şeyi durdur" olarak düşünün.

## Asistanların ne yapabileceği

İki seviye erişim, ayrı ayrı kontrol edilir:

- **Okuma** (keşif ve tarayış) daha düşük risklidir. Bir asistan, mağazanızı bulabilir ve ürün detaylarını okuyabilir.
- **Ödeme** (aslında satın alma) daha yüksek risklidir ve doğrulanmamış asistanlar için kapatlı kalır, bunu izin vermeden.

Bir mağaza keşfedilebilir ama satın alınabilir olmayabilir — bu, başlamak için yararlı bir yoldur.

## Belirli ürünlerin gizlenmesi

Her ürünün **AI alışveriş ajentlerine görünür** ayarı vardır (varsayılan olarak açık). Bunun kapatılması, bir ürünün mağazanızda görünmesine rağmen asistanlardan gizlenmesini sağlar — kendi sitenizden sadece satmak istediğiniz ürünler için kullanışlıdır.

## Bireysel asistanları yönetme

Bir asistan ilk satın alır ya da denemeye çalışırsa, Spwig bunu **AI Alışveriş → Ajent Kimlikleri** altında kaydeder. Her girdi, asistanın doğrulanmış evini (imza ettiği dizin) ve yaptığı istek sayısını gösterir. Asistanın sunduğu isim ve logoda yalnızca *iddia edilen* detaylar yer alır — bunları bir etiket olarak, kimlik kanıtı olarak değil, düşünün; doğrulanmış ev, güvenilir olan kısım.

Yeni asistanlar başlangıçta **sınırlı** olarak başlatılır: satın alım yapabilirler, ancak sınırlar içinde. Birini durdurmak için onu seçin ve **Seçili asistanları engelle**'yi seçin — açık ödeme işlemlerini sonlandırır ve asistan artık satın alamaz, ancak alınan ödemeler aksatılmaz. **Seçili asistanları engellemeyi kaldır** onu sınırlı duruma geri döndürür (asla doğrudan sınırsız olmaz — sınırları kaldırma her zaman ayrı ve amaçlı bir adımdır).

## Aktivite kaydı

**AI Alışveriş → Ajent Olayları**, asistanların ne yaptığını gösteren bir manipülasyon izi olan kayıttır — her doğrulanmış istek, her engellenen deneme, her değişiklik. Sadece okunabilir ve düzenlenemez veya silinemez, bu nedenle bir asistanın yaptığı bir satın alma her zaman için kanıt iziniz olarak kalır.

## Asistan platformları hakkında bir not

Bu asistanları işleten şirketler (ve onlarda görünmek için gereken kurallar) yeni ve sık sık değişmektedir.

Bazıları, ürünlerin onlar aracılığıyla satın alınabilmesi için başvurmanızı veya bölgesel koşulları karşılamanızı gerektirir.



Spwig mağazanızı hazır hale getirir; bir asistanın size listeleme yapıp yapmaması o asistanın kararına bağlıdır.