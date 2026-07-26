---
title: AI Alışveriş
---

AI Alışveriş, AI alışveriş asistanlarının ürünlerinizi bulmasına ve sizin onlar adına mağazanızdan alışveriş yapmasına olanak tanır. Bu özellik **varsayılan olarak kapatılmıştır** — bunu açmak bir amaçlı seçimdir ve bunu yapmadığınız sürece mağazanız bu asistanlara hiçbir şey ifşa etmez.

## Açma

**Ayarlar → AI Alışveriş** menüsünü açın ve **Ajentik ticaret etkin** anahtarını açın. Bu noktadan sonra Universal Commerce Protocol'u destekleyen asistanlar mağazanızı bulabilir ve kataloğunuzu okuyabilir. Normal mağazanızla ilgili hiçbir şey değişmez.

## Hazırlık paneli

AI Alışveriş sayfasının üst kısmı, şu an bir cümle ile tek bir soruyu yanıtlar: **AI asistanlarının şu anda mağazanızdan gerçekten alışveriş yapabilir mi?**

- **"AI asistanları mağazanızdan alışveriş yapabilir"** — bir alışveriş için gereken her şey mevcuttur.
- **"AI asistanları mağazanızı tarayabilir, ama henüz alışveriş yapamaz"** — mağazanız keşfedilebilir, ancak bir alışveriş tamamlanabilmesi için bir şey eksik (genellikle bağlı bir ödeme sağlayıcısı).
- **"Acil durum durdurma aktif"** ya da **"Ajentik ticaret kapatılmış"** — asistanlara hiçbir şey sunulmuyor.

Karar vermenin altına kısa bir kontrol listesi yer alır — ödeme sağlayıcısı bağlı, kargo ücreti verilebilir, ürünler asistanlara görünür — herhangi bir dikkat gerektiren şeyin yanında bir ipucu vardır. Sayıcılar, asistanların satabileceği ürün sayısı, onlardan gizlediğiniz ürün sayısı, ziyaret eden asistan sayısı ve engellediğiniz asistan sayısını gösterir.

Bu kontrol listesi **yaşamakta olan** ayarlarınızı yansıtır: bir ödeme sağlayıcısını bağlayın veya bir kargo yöntemi ekleyin ve karar verme, sayfayı tekrar açtığınızda güncellenir.

## Acil durum durdurma

**Acil durum durdurma**, ana anahtardan ayrı bir anahtardır. Onu kullanarak, yapılandırmayı bozmadan tüm asistan etkinliklerini hemen durdurabilirsiniz — örneğin bir şeyin yanlış gibi görünmesi durumunda. Temizleyin ve devam edin. Ana anahtarı "Bu özellik yapılandırılmış mı?" olarak düşünün ve acil durum durdurmayı "Şimdi her şeyi durdur" olarak düşünün.

## Asistanların ne yapabileceği

İki seviye erişim, ayrı ayrı kontrol edilir:

- **Okuma** (keşif ve tarayış) daha düşük risklidir. Bir asistan, mağazanızı bulabilir ve ürün detaylarını okuyabilir.
- **Ödeme** (aslında alışveriş yapma) daha yüksek risklidir ve doğrulanmamış asistanlar için kapatıktır, bunu izin vermedikçe.

Bir mağaza keşfedilebilir ama satın alınabilir olmayabilir — bu, başlamak için faydalı bir yoldur.

## Belirli ürünlerin gizlenmesi

Her ürünün **AI alışveriş ajentlerine görünür** ayarı vardır (varsayılan olarak açık). Bu ayarı kapatın ve bir ürünü asistanlardan gizleyin, ancak ürün mağazanızda hala görünür olur — kendi sitenizden sadece satmak istediğiniz ürünler için kullanışlıdır.

## Bireysel asistanları yönetme

Bir asistan ilk kez alışveriş yapar ya da denemeye çalışırsa, Spwig bunu **AI Alışveriş → Ajent Kimlikleri** altında kaydeder. Her girdi, asistanın doğrulanmış evini (imza verdiği dizin) ve yaptığı istek sayısını gösterir. Asistanın sunduğu isim ve logoda yalnızca *iddia edilen* detaylar yer alır — bunları bir etiket olarak, kimlik kanıtı olarak değil, düşünün; doğrulanmış ev, güvenilir olan kısım.

Yeni asistanlar başlangıçta **sınırlı** olarak başlatılır: alışveriş yapabilirler, ancak sınırlar içinde. Birini durdurmak için onu seçin ve **Seçili asistanları engelle**'yi seçin — açık ödeme işlemlerini sonlandırır ve asistan artık alışveriş yapamaz, ancak alınan ödemeler aksatılmaz. **Seçili asistanları engellemeyi kaldır** onu sınırlı duruma geri döndürür (asla doğrudan sınırsız olmaz — sınırları kaldırma her zaman ayrı ve amaçlı bir adımdır).

## Aktivite kaydı

**AI Alışveriş → Ajent Olayları**, asistanların ne yaptığını gösteren bir izlenemez kayıttır — her doğrulanmış istek, her engellenen deneme, her değişiklik. Bu sadece okunabilir ve düzenlenemez veya silinemez, bu nedenle bir asistanın yaptığı bir alışveriş tartışılırsa, bu sizin kanıt izinizdir.

## Asistan platformları hakkında bir not

Bu asistanları işleten şirketler (ve onlarda görünmek için gereken kurallar) yeni ve sık sık değişmektedir.

Bazıları, ürünlerinizin onlar aracılığıyla satın alınabilmesi için başvurmanızı veya bölgesel koşulları karşılamanızı gerektirir.



Spwig mağazanızı hazır hale getirir; belirli bir asistanın size bir liste oluşturup oluşturmayacağı, o asistanın kararına bağlıdır.