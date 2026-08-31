---
title: Toplu Stok İşlemleri
---

Tek seferlik ayarların ötesinde, Spwig; birden fazla üründe aynı anda gerçekleşen envanter işleri için **Stok Kalemleri** listesinde üç toplu işlem sunar: stokları depolar arasında taşıma, hasarlı veya kayıp birimlerin yazılması ve fiziksel sayım sonrası stok mutabakatı. Üç işlem de aynı **İşlemler** açılır menüsünden çalıştırılır, seçtiğiniz her stok kalemine aynı miktarı uygular ve stok hareketi denetim izinde tamamen kaydedilir.

Bunları kullanmak için **Ürünler > Stok Kalemleri** bölümüne gidin.

## Toplu stok işlemi çalıştırma

1. **Stok Kalemleri** listesinde, güncellemek istediğiniz kalemleri bulmak için filtreleri veya aramayı kullanın
2. Dahil etmek istediğiniz her stok kaleminin yanındaki kutuyu işaretleyin (veya sayfadaki tüm kalemleri seçmek için başlık kutusunu kullanın)
3. **İşlemler** açılır menüsünden üç işlemden birini seçin:
   - **Stokları depoya taşı**
   - **Hasarlı/kayıp stok kaydet**
   - **Stok sayımı (fiziksel sayım)**
4. **Git** düğmesine tıklayın
5. Onay sayfasını inceleyin — seçtiğiniz her stok kalemini mevcut **elde bulunan**, **ayrılan** ve **kullanılabilir** miktarlarıyla birlikte listeler, böylece doğru kalemleri seçtiğinizi kontrol edebilirsiniz
6. İşlemin alanlarını doldurun (aşağıya bakın) ve uygulamak için gönder düğmesine tıklayın

![Toplu işlemler açılır menüsü açık olan Stok Kalemleri listesi; diğer işlemlerin yanı sıra Depoya stok taşı, Hasarlı/kayıp stok kaydet ve Stok sayımı (fiziksel sayım) seçeneklerini gösterir](/static/core/admin/img/help/stock-bulk-actions/stock-items-actions-dropdown.webp)

Girdiğiniz aynı miktar, seçilen **her** kaleme uygulanır — bu, birçok SKU arasında aynı sayıda birimi topluca taşımak, yazmak veya yeniden saymak için tasarlanmıştır (örneğin, birkaç ürünün 10 birimini yeni bir mağaza konumuna transfer etmek). Farklı bir miktara sahip tek bir kalemi için, işlemi yalnızca o kalemi seçerek tekrar çalıştırın veya bunun yerine **Stok seviyelerini ayarla** seçeneğini kullanın.

## Stokları depoya taşı

Bunu, seçilen her kalemin deposundan kullanılabilir stokları farklı bir depoya taşımak için kullanın — örneğin, ana depodan yeni bir perakende konumunu stoklamak veya bölgesel dağıtım merkezleri arasında envanteri dengelemek.

Onay sayfasında şunları doldurun:

| Alan | Açıklama |
|-------|-------------|
| **Hedef depo** | Stokun taşınacağı yer. Bu listede yalnızca aktif depolar görünür. |
| **Kalem başına miktar** | Seçilen her kalemin mevcut deposundan çıkarılacak birimler. |
| **Neden** | İsteğe bağlı not, örn. "Yeni Auckland mağazası için stok yenileme". |

Uygulamak için **Stok Taşı** düğmesine tıklayın.

![Stok Taşıma onay sayfası: elde bulunan/ayrılan/kullanılabilir rakamlarıyla üç kalemi listeyen Seçili Stok Kalemleri kartı ve hedef depo, miktar ve neden alanları doldurulmuş Taşıma Detayları formu](/static/core/admin/img/help/stock-bulk-actions/transfer-stock-confirmation.webp)

**Yalnızca ayrılmamış stok taşınabilir.** Spwig, *kullanılabilir* stoktan (elde bulunan, açık siparişlere ayrılmış birimler çıkarıldıktan sonra) transfer yapar — bir müşterinin siparişine zaten taahhüt edilen birimler, o siparişin hâlâ yerine getirilebilmesi için kaynak depoda kalır. Seçilen bir kalemin, girdiğiniz miktarı karşılayacak kadar kullanılabilir stoku yoksa, o kalem atlanır ve nedenini açıklayan bir hata mesajı gösterilir; seçimin geri kalanı yine de transfer edilir.

Seçilen bir kalem zaten seçtiğiniz hedef depoda stoklanmışsa, otomatik olarak atlanır (kendi kendine taşınacak bir şey yoktur) ve bu nedenle kaç kalemin atlandığını bildiren bir mesaj görürsünüz.

Her transfer, denetim izine eşleşen bir hareket seti yazar — kaynakta negatif bir **Depo Transferi** girişi ve hedefte eşleşen pozitif bir giriş — böylece tam iz, stokun nereden geldiğini ve nereye gittiğini tam olarak gösterir.

## Hasarlı/kayıp stok kaydet

Bunu, kırık, bozulmuş veya eksik birimleri yazmak için kullanın — örneğin, bir teslimatta hasarlı mallar bulduktan sonra veya bir uyumsuzluğu araştırırken.

Onay sayfasında şunları doldurun:

| Field | Description |
|-------|-------------|
| **Muhafaza edilecek miktar (her bir öğe için)** | Seçilen her bir öğe için eldeki stoktan kaldırılacak birim sayısı. |
| **Neden** | Opsiyonel not, örneğin "Depolama sırasında su hasarı". |

**Rezerv stok yazılabilir değildir.** Eldeki stok, açık siparişler için şu anki ayrılmış miktarın altına düşemez — Spwig, girdiğiniz miktarın ayrılmış stokları yeme riskini önler, bu yüzden bir siparişin stok eksikliğiyle kalmamasını önler. Eğer bir öğe için bu durum olursa, öğeyi ve gerçekten ne kadar stok yazılabilir olduğunu gösterecek bir hata mesajı görürsünüz.

Her bir yazım, bu stok öğesine bir **Bozulmuş/Kaybolmuş** hareketi olarak kaydedilir, negatif miktarla.

## Stok yeniden sayımı (fiziksel sayaç)


Bir fiziksel stok sayımı sonrasında eldeki miktarları gerçekten saydığınız miktarla eşleştirmek için bu aracı kullanın — depo incelemesi veya döngü sayımı sonrası birçok öğeyi eşleştirmenin en hızlı yoludur.

Onay sayfasında şunları doldurun:

| Field | Description |
|-------|-------------|
| **Sayılan eldeki miktar (her bir öğe için)** | Fiziksel olarak saydığınız miktar. Her bir öğe için eldeki miktar, eklenen veya çıkarılan bir miktar değil, bu sayıya eşit olur. |
| **Neden** | Opsiyonel not, örneğin "Q3 depo stok sayımı". |

**Apply Recount**'a tıklayın.

![Stok Yeniden Sayımı onay sayfası: Seçilen Stok Öğeleri kartı ve sayılan eldeki miktar ve nedeni doldurulmuş bir Yeniden Sayım Detayı formu](/static/core/admin/img/help/stock-bulk-actions/recount-stock-confirmation.webp)

Diğer iki eylemden farklı olarak, yeniden sayım stok hareketini her iki yönde de değiştirebilir — sistemin beklentisinden fazla sayı sayarsanız yukarı, eksik sayı sayarsanız aşağı. Girdiğiniz sayım, şu an açık siparişler için ayrılmış miktarın altına düşerse, Spwig yine de uygular (sayım bir faktördür, tartışmaya değer değildir), ancak bu öğenin **Mevcut** sayısı stok listesinde `0` olarak gösterilir ve durum simgesi Stok Tükendiğine döner — etkilenen siparişlerin hâlâ yerine getirilebilir olup olmadığına dair bir uyarı olarak kabul edilmelidir.

Her bir yeniden sayım, eski ve yeni eldeki miktarlar arasındaki düzeltmeyi (pozitif veya negatif) gösteren bir **Fiziksel Yeniden Sayım** hareketi olarak kaydedilir.

## Neyin değiştiğini inceleme

Her bir aktarım, yazım ve yeniden sayım, diğer stok değişikliklerinde olduğu gibi aynı şekilde kaydedilir:

- Bir stok öğesini açın ve **Stok Hareketleri** bölümünü inceleyin ve tarihçesini görün
- Veya **Ürünler > Stok Hareketleri** sayfasına giderek tüm öğeler arasındaki hareketleri tarayın, türüne göre filtreleyebilirsiniz

Her giriş, hareket türü, miktar değişimi, önceki ve yeni eldeki miktarlar, değişikliği yapan kişi ve girdiğiniz sebep (varsa) hakkında bilgi içerir — yani bir grup aktarımı veya yazımı, tekli manuel ayarlamalar kadar izlenebilir.

## İpuçları

- Fiziksel stok sayımı yaptıktan hemen sonra **Stok Yeniden Sayımı** işlemini yapın — sayım sayıları hafızada iken, hareket tarihçesinden sonra bu sayıları çözmekten daha kolaydır.
- Yazım ve yeniden sayım için **Neden** alanını doldurun. Altı ay sonra, "Depolama sırasında su hasarı" ifadesi, bir denetim tarihi için boş bir alandan çok daha faydalı olur.
- Stok aktarımı yapmadan önce, onay sayfasındaki **Mevcut** sütununu kontrol edin — zaten ayrılmış birimleri hesaba katarak, seçtiğiniz öğelerin birinde miktarın çok yüksek olup olmadığını anında anlayabilirsiniz.
- Bu eylemler, seçilen her bir öğeye aynı miktarı uygular. Gerçekten aynı miktarı taşımak, yazmak veya yeniden saymak istediklerini gruplayarak seçimi yapın ve istisnaları tek tek ele alın.
- Perakende bir lokasyonda POS kullanıyorsanız, depo yedek stokları online siparişler için "meydana