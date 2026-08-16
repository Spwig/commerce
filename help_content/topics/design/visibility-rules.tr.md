---
title: Görünürlük Kuralları
---

# Görünürlük Kuralları

Görünürlük kuralları, birinin ziyaret ettiği yer ve kim olduğuna göre mağazanızın parçalarını göstermenizi veya gizlememenizi sağlar. Aynı koşullarla **sayfa elemanlarını**, **menü öğelerini** ve **başlık/altlık eklentilerini** kapatabilirsiniz: bir müşterinin pazarı veya bölgesi, ne zaman görüntülediği dil veya para birimi, günün ne zamanı, ya da bir ziyaretçiye ait sinyaller, örneğin oturum açıp açmadığı.

Her şey **kural gruplarından** oluşturulur: bir veya daha fazla koşul içeren, isimlendirilmiş, tekrar kullanılabilir bir dizi kural. Bir kural grubu oluşturursunuz (örneğin, "Yeni Zelanda pazarı" veya "Oturum açmış üyeler") ve ardından onu kontrol etmek istediğiniz herhangi bir eleman, menü öğesi veya eklentiye eklersiniz. Hiçbir kural grubu eklenmemiş bir öğe her zaman görünür.

## Görünürlüğün nasıl kararlaştırıldığı

Bir öğeye birden fazla kural grubu eklenmişse, **herhangi** bir ekli grup eşleşirse öğe gösterilir (OR ile birleştirilir). Tek bir grupta, **hepsi** ya da **herhangi** birinin eşleşmesi gerektiğini seçersiniz.

Kurallar iki aileye ayrılır ve Spwig, mağazanızın hızlı ve arama motoru dostu kalmasını sağlamak için bunları farklı şekilde işler:

- **Pazar kuralları** — bölge/pazar, dil, para birimi ve zaman temelli koşullar. Bu türler, her pazar URL'si için sunucuda kararlaştırılır, bu yüzden aynı sayfa, bu adresdeki her ziyaretçi (ve her arama motoru) için aynı şekilde teslim edilir. Bu, sayfaların önbelleklenebilir ve SEO güvenli kalmasını sağlar.
- **Bireysel ziyaretçi kuralları** — oturum açma durumu, sepet içeriği, cihaz ve kesin konum. Bu türler, bireysel ziyaretçiye bağlıdır, bu yüzden sayfa yüklendikten sonra her kişi için özel olarak çözülür. Bunlar, paylaşılan, önbelleklenebilir bir sayfaya asla eklenmez.

Bir kural grubunu devre dışı bırakırsanız, basitçe uygulanmaz — ona eklediğiniz öğe tekrar görünür hale gelir. Bir grubu devre dışı bırakmak, bir şeyi gizlemek için bir yol değildir.

## Kuralların oluşturulması ve eklenmesi

Kural gruplarıyla çalışmak için iki yol vardır.

### Tasarım esnasında ekleyin

İçeriği kapatmak için kullanabileceğiniz her yerde, bir **görünürlük kontrolü** (göz ikonu) göreceksiniz:

- **Sayfa Oluşturucu** — bir eleman seçin, özelliklerini açın ve görünürlük kontrolünü kullanın.
- **Menü Oluşturucu** — bir menü öğesi seçin ve **Görünürlük** sekmesini açın. Bu, **herhangi** bir öğe için çalışır, örneğin başka bir öğenin altındaki bir alt menü (açılır menü) öğesi — bir çocuktaki bir kural, sadece o çocuğu gizler, menünün geri kalanını bozmadan bırakır.
- **Başlık & Altlık Oluşturucu** — bir eklenti seçin ve ayarlarının **Görünürlük Kuralları** bölümünü açın.

Bireysel ziyaretçiye dayalı kurallar — oturum açıp açmadıkları, sepetlerinde ne olduğu ya da cihazları — mağazanızı yavaşlatmadan veya arama motorlarını etkilemeden her müşteri için çözülür. Mağazanız hızla kalır ve önbelleklenebilir kalır ve her ziyaretçi, onlar için tasarlanmış menüyü görür.

Görünürlük düzenleyicisinde şunları yapabilirsiniz:

- **Var olan** kural gruplarından herhangi birini seçerek ekleyin.
- **Hızlı kural** — mevcut bir kural grubu oluşturun (örneğin, "sadece üyeler", tek bir pazar, para birimi, cihaz veya minimum sepet değeri) ve tek adımda ekleyin.
- **Kural gruplarını yönetin** — gelişmiş kurallar için tam yapılandırıcıya gidin.

**Uygula**'yı tıklayın ve öğe anında kapatılır.

### Gelişmiş kurallar oluşturun

Birçok koşulu birleştirmek, grupları iç içe koymak ya da ince ayarlı operatörler kullanmak gibi daha karmaşık işlemler için **Tasarım → Görünürlük Kuralları**'na (kural grupları) gidin. Burada AND/OR mantığı ile kurallar oluşturabilir ve bunları mağazanızın tümünde tekrarlayabilirsiniz.

## Sık Karşılşılan Koşullar

Tüm markdown formatını, resim yollarını, kod bloklarını ve teknik terimleri koruyun.

| Condition | Use it to… |
|-----------|------------|
| **Bölge / pazar** | Belirli bir pazar (örneğin Yeni Zelanda) ziyaretçisi olanlara yalnızca bir blok göster |
| **Seçilmiş döviz** | Belirli bir döviz aktifken fiyat notlarını veya teklifleri göster |
| **Seçilmiş dil** | Belirli bir dilde içerik göster |
| **Tarih / saat / gün / iş saatleri** | Bir satış penceresinde veya yalnızca açık saatlerde bir bülten çalıştır |
| **Giriş yapmış durum** | Üyelere özel içerikleri veya ziyaretçilere bir kayıt olma istemi göster |
| **Cihaz türü** | Mobil, tablet veya masaüstü üzerinde neyin gösterilip gizlenmesini sağla |
| **Sepet değeri / ürün sayısı** | Sepet belirli bir eşiği geçtiğinde ücretsiz kargo ipucu göster |

## Önizleme

Sayfa Oluşturucu önizleme ekranında, her bir kullanıcıya ne göstereceğini tam olarak görmek için **bir pazar gibi** ve **bir ziyaretçi gibi** (giriş yapmış veya giriş yapmamış, örnek sepet ile) önizleme yapabilirsiniz — ziyaretçiye özel kurallar normalde özel olarak çözülür.

## İpuçları

- "Yeni Zelanda pazarı", "Üyeler", "Sadece Mobil" gibi iyi isimlendirilmiş kural grupları oluşturun ve bunları her yerde tekrar kullanın — tek seferlik kurallardan daha kolay yönetilir.
- Pazar kuralları, herhangi bir pazar URL'sindeki herkes için aynı sonucu verdiğinden, arama motorları tarafından indekslenen her şey için güvenli bir seçimdir.
- Bir ürün beklenmedik şekilde kaybolursa, onunla ilişkilendirilmiş kural gruplarını kontrol edin — bir ürün, aktif bir grup varsa ve şu anki ziyaretçinin gruplarından hiçbirine uymuyorsa gizlenir.