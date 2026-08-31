---
title: Abone Etiketleri
---

Etiketler, Kampanya Stüdyosu abone kitlenizi düzenlemek için kendi etiketlerinizdir — `VIP`, `toptancı`, veya `etkinlik-2026` gibi kısa işaretleyiciler, hangi abonelerin uygun olduğunu belirleyip onlara uyguladığınız şeydir. Bir etiket var olduktan sonra, abone listesini ona göre filtreleyebilir, herhangi sayıda kişiyi aynı anda etiketleyebilir ve - en yararlı olanı - bir Segment oluştururken koşul olarak kullanabilirsiniz, bu sayede kampanyalarınız ve yollarınız sadece etiketlediğiniz kişileri hedefleyebilir.

## Etiketler neye yarar?

Bir etiket, sadece seçtiğiniz bir isimdir. Spwig, herhangi bir yerleşik etiket içermemektedir ve bir etiketi otomatik olarak uygulamaz — neyin ismini vereceğinizi ve kime verileceğini siz kararlaştırırsınız. Bu, Spwig'in zaten takip ettiği bir duruma harici olarak, kendi işinize özel olan her şey için iyi bir uygundur: bir mukayese seviyesi, bir toptancı hesabı, bir fuar etkinliğinde kaydolan herkes ya da `etkinlik-2026` gibi tek seferlik bir etkinlik listesi.

Her etiket için bir de **Kısa Yol** (slug) olur — isminizin basitleştirilmiş, URL'ye uygun hali — etiketi oluşturduğunuzda otomatik olarak oluşturulur. Segmentler ve filtreler, içlerinde slug kullanır; satıcı olarak neredeyse hiçbir zaman ona bakmanız gerekmez.

## Etiket Oluşturma

Etiketlerin kendi yönetimi vardır. **Kampanya Stüdyosu > Aboneler**'e açın, sayfanın en üstündeki **Kampanya Stüdyosu**'na tıklayın ve Kampanya Stüdyosu bölümlerinin tamamını görmek için, **Abone Etiketleri**'ni seçin.

1. **Abone Etiketi Ekle**'ye tıklayın.
2. **İsim** girin — kısa ve özel okunması en iyisidir, örneğin `VIP`, `Toptancı`, veya `Etkinlik 2026`.
3. Spwig, yazarken eşleşen bir **Kısa Yol** (slug) doldurur. Oluşturulanı olduğu gibi bırakabilirsiniz.
4. **Renk** alanı da mevcuttur, kendi referansınız için bir hex rengi (örneğin `#2563eb`) kaydetmek isterseniz.
5. **Kaydet**'e tıklayın.

Herhangi bir şeyi bırakmak zorunda değilsiniz — herhangi bir abonenin kendi düzenleme sayfasındaki **Etiketler** alanının yanında yeşil bir **+** simgesi, aynı "etiket ekle" formunu bir popup içinde açar. Ve eğer hiç etiket oluşturmadan abone etiketleme işlemini yapmaya çalışırsanız, etiket seçimi, hemen oraya giden bir **Etiket Oluştur** kısayolu sunar.

## Abonelere Etiketleme

Bir etiketin uygulanması en yaygın yolu, Aboneler listesinden toplu olarakdır:

1. **Kampanya Stüdyosu > Aboneler**'e açın.
2. etiketlemek istediğiniz her bir abone için onay kutusunu işaretleyin (veya bu sayfadaki **Tümünü Seç**).
3. **Toplu Eylemler** menüsünden **Seçilenlere Etiket Ekle...** (veya **Seçilenlerden Etiketi Kaldır...**) seçin.
4. **Git**'e tıklayın.
5. Listedeki etiketi seçin ve **Etiket Ekle** (veya **Etiketi Kaldır**) 'a tıklayın.

![Dört abone için "Seçilenlere Etiket Ekle" seçildikten sonra toplu etiket seçimi](/static/core/admin/img/help/subscriber-tags/bulk-tag-picker.webp)

Uygulandıktan sonra, bir etiket, abone listesindeki kartında durum ve kaynak badajları ile birlikte küçük bir çip şeklinde görünür. En az bir etiketiniz varsa, abone listesinin filtre panelinde bir **Etiket** filtresi de görünür, bu da belirli bir etikete sahip olan herkese daraltılabilir — onlarla ilgili kampanya oluşturmadan önce kimlerin bir listede olduğunu kontrol etmek için yararlıdır.

![VIP etiketine göre filtrelenmiş Abone listesi, İthalat CSV'si butonu ve etiket çipleri görünür](/static/core/admin/img/help/subscriber-tags/subscriber-list-tag-chips.webp)

Aynı **Etiketler** alanını kullanarak, herhangi bir abonenin kendi düzenleme sayfasından tek seferde etiket ekleyebilir ya da kaldırabilirsiniz.

## Segmentlerde Etiket Kullanımı

Segmentler, kampanyalarınıza ve yollarınıza yönlendirdiğiniz, kurala dayalı saklanan kitlelerdir. En az bir etiket oluşturduktan sonra, segment kural oluşturucuda **Etiketi Var** koşulu mevcut olur — etiket tanımlaması yapılmamış yeni bir kurulumda bu görünmez, bu yüzden onun yararlı olmasına kadar bir işe yaramayan bir seçenek olmayacaktır.

Kullanmak için, **Kampanya Stüdyosu > Segmentler**'e açın, bir dinamik segment ekleyin (ya da düzenleyin) ve **+ Koşul Ekle**'ye tıklayın:

1. Koşulun alanını **Etiketi Var** olarak ayarlayın.
2. **Tek bir etiket için** ya da **herhangi biri** olmak üzere bir operatör seçin.
3. Aşağıdaki menüden etiketi seçin.

[![](A "Has tag" condition set to VIP, showing a live count of matching subscribers)](/static/core/admin/img/help/subscriber-tags/segment-has-tag-rule.webp)

Kuralları oluştururken sağ üst köşede ki sayaç güncellenir, bu da şu anki uygun olan abonelerin sayısını görebilmenizi sağlar. Her bir **Has tag** koşulu şu anda yalnızca bir etiketle eşleşir — birkaç etiketin (örneğin, `VIP` veya `Wholesale`) herhangi birini içermesini istiyorsanız, her etiket için bir tane olmak üzere **Has tag** koşulu ekleyin ve **Eşleş**yi **herhangi biri** olarak ayarlayın.

Bu, etiketlerin sadece organizasyon için değil, aynı zamanda yararlı olmasının nedenidir: **Has tag** üzerine kurulan bir bölüm, bir yayın veya tekrarlayan kampanyada **Segment** olarak, ya da bir yolculukta **Sadece segment** ayarı olarak seçilebilen bir kitle oluşturur — yani "VIP etiketli herkes", kendi başlangıç serisini, kendi tekrarlayan bültenini ya da sadece bir sonraki bir defalık duyuruyu gönderirken neyi seçeceğinizi belirleyebilir.

## İpuçları

- Etiket isimlerini kısa ve spesifik tutun — abone kartlarında küçük çip şeklinde görünürler, bu yüzden `VIP`, `Very Important Person - Tier 1`'den daha iyi okunur.
- Bir bölüm ya da kampanya oluşturmadan önce kimin etiketlendiğini kontrol etmek için **Etiket** filtresini kullanın.
- Etiketleme, bir aboneden bir etiketi kaldırmanıza rağmen, onların diğer etiketlerini, durumunu, kaynağını ya da onayını asla etkilemez.
- Aynı bölüme diğer kural kurucu koşulları (örneğin, **Pazarlamaya katıldı** ya da **Toplam harcama**) ile birleştirerek, sadece bir etiketin değil, daha da fazlasını içeren daha da kesin bir kitle oluşturabilirsin.
- Bir abone, istediğiniz kadar etikete sahip olabilir — sınırlama olmadığı için, birikim seviyesi *ve* bir etkinlik listesi *ve* bir kaynak notu gibi birçok üst üste gelen amaç için kullanabilirsin.
- Bir etiket yararlılığını kaybettiğinde, **Abone etiketleri**nden silinmesi, ona uygulanan tüm abonelerden ve buna referans yapan herhangi bir bölüm kuralından kaldırılmasına neden olur — bu koşulda eşleşmeyi durduracaklardır.