---
title: Toplu Stok Eylemleri
---

Bireysel ayarlamaların ötesinde, Spwig, birden fazla ürün üzerinde aynı anda gerçekleşen envanter işleri için **Stok Ürünleri** listesinde üç adet toplu eylem sunar: depolar arası stok hareketi, hasar görmüş veya kaybolmuş birimlerin yazılması ve fiziksel sayaç sonrası stokların denetlenmesi. Üç eylem de aynı **Eylemler** menüsünden çalışır, seçtiğiniz her stok ürününde aynı miktarı uygular ve tamamen stok hareketi denetim kâğıdında kaydedilir.

Eylemleri kullanmak için **Ürünler > Stok Ürünleri** sayfasına gidin.

## Toplu stok eylemini çalıştırma

1. **Stok Ürünleri** listesinde, güncellemek istediğiniz ürünleri bulmak için filtreleri veya aramayı kullanın
2. Her stok ürününü dahil etmek için onun yanında ki kutuyu seçin (veya sayfadaki tüm ürünleri seçmek için başlık kutusunu kullanın)
3. **Eylemler** menüsünden üç eylemden birini seçin:
   - **Depoya stok aktarma**
   - **Hasarlı/kaybolmuş stok kaydı**
   - **Stok yeniden sayımı (fiziksel sayaç)**
4. **Git**'e tıklayın
5. Onay sayfasını inceleyin — seçili her stok ürününü, mevcut **eldeki**, **atandığı** ve **kullanılabilir** miktarları ile birlikte listeler, doğru ürünleri seçtiğinizden emin olun
6. Eylemin alanlarını doldurun (aşağıya bakınız) ve uygulamak için submit butonuna tıklayın

![Stok Ürünleri listesi, Toplu eylemler menüsünün açık haliyle, diğer eylemlerle birlikte Depo'ya stok aktarma, Hasarlı/kaybolmuş stok kaydı ve Stok yeniden sayımı (fiziksel sayaç) eylemlerini içermektedir](/static/core/admin/img/help/stock-bulk-actions/stock-items-actions-dropdown.webp)

Girdiğiniz aynı miktar, **her** seçili iteme uygulanır — bu, birkaç SKU üzerinde aynı sayıdaki birimleri aynı anda hareket ettirmek, yazmak veya yeniden saymak için tasarlanmıştır (örneğin, birkaç ürünün 10 birimini yeni bir mağaza konumuna aktarma). Tek bir ürün için farklı bir miktar varsa, eylemi sadece o ürünü seçerek tekrar çalıştırın, ya da **Stok seviyelerini ayarla** kullanın.

## Depoya stok aktarma

Her seçili ürünün deposundan farklı bir depoya mevcut stokları hareket ettirmek için bu eylemi kullanın — örneğin, ana depodan yeni bir mağaza konumuna stoklama, ya da bölgesel kargo merkezleri arasında envanterin yeniden dengelenmesi.

Onay sayfasında, şunları doldurun:

| Alan | Açıklama |
|-------|-------------|
| **Hedef depo** | Stokun taşınacağı yer. Bu listede sadece aktif depolar gösterilir. |
| **Her ürün için miktar** | Seçili ürünün mevcut deposundan çıkarılacak birim sayısı. |
| **Neden** | Opsiyonel not, örneğin "Yeni Auckland mağazası stoklama". |

**Stok Transferi**'ni uygulamak için **Stok Transferi**'ne tıklayın.

![Stok Transferi onay sayfası: eldeki/atanmış/kullanılabilir rakamları ile üç ürün içeren Seçili Stok Ürünleri kartı ve hedef depo, miktar ve neden alanları doldurulmuş bir Stok Detayı formu](/static/core/admin/img/help/stock-bulk-actions/transfer-stock-confirmation.webp)

**Sadece ayrılmamış stok taşınabilir.** Spwig, *kullanılabilir* stoktan (eldeki birimlerin açık siparişlere atandığından çıkarılmış olanlar) taşır — bir müşteri siparişine zaten vaad edilen birimler, o siparişin hâlâ yerine getirilebilmesi için kaynak depoda kalmaya devam eder. Seçili bir ürün, girdiğiniz miktarı karşılamak için yeterli kullanılabilir stoke sahip değilse, bu ürün atlanır ve nedenini açıklayan bir hata mesajı gösterilir; seçimdeki diğerleri hâlâ aktarılır.

Seçili bir ürün, seçtiğiniz hedef depoda zaten mevcutsa, otomatik olarak atlanır (kendine aktarılacak bir şey yoktur), bu nedenle bu sebepten kaç tane ürün atlandığını bildiren bir mesaj görürsünüz.

Her aktarma, denetim kâğıdında eşleştirilmiş bir hareket seti yazar — kaynakta negatif **Depo Aktarımı** girişi ve hedefte eşit pozitif giriş — bu nedenle tam denetim kâğıdı, stokun nereden geldiğini ve nereye gittiğini gösterir.

## Hasarlı/kaybolmuş stok kaydı

Hasarlı, çürümüş veya kaybolmuş birimleri yazmak için bu eylemi kullanın — örneğin, bir teslimatta hasarlı malların bulunması veya bir discrepancinin incelenmesi sonrası.

Onay sayfasında, şunları doldurun:

| Field | Description |
|-------|-------------|
| **Muhafaza edilecek miktar (her bir öğe için)** | Seçilen her bir öğe için eldeki stoktan kaldırılacak birim sayısı. |
| **Neden** | Opsiyonel not, örneğin "Depolama sırasında su hasarı". |

**Rezerv stok yazılabilir değildir.** Eldeki stok, açık siparişlere ayrılmış miktarın altına düşemez — Spwig, girdiğiniz miktarın ayrılmış stokları yeme riskini önler, bu yüzden bir siparişin stok eksikliğiyle kalmamasını engellersiniz. Eğer bir öğe için bu durum olursa, öğenin adı ve gerçekten yazılabilir ne kadar birimi olduğuna dair bir hata mesajı göreceksiniz.

Her bir yazım, o stok öğesinde **Bozulmuş/Kaybolmuş** hareketi olarak kaydedilir, negatif miktarla.

## Stok yeniden sayımı (fiziksel sayaç)


Bir fiziksel stok sayımı sonrasında eldeki miktarları gerçekten saydığınız miktarla düzeltmek için bu aracı kullanın — depo denetimi veya döngü sayımı sonrası birçok öğeyi senkronlaştırmak için en hızlı yoldur.

Onay sayfasında şunları doldurun:

| Field | Description |
|-------|-------------|
| **Sayılan eldeki miktar (her bir öğe için)** | Fiziksel olarak saydığınız miktar. Eldeki stok, her bir öğe için bu tam sayıya ayarlanır — eklenmez veya çıkarılmaz. |
| **Neden** | Opsiyonel not, örneğin "Q3 depo stok sayımı". |

**Apply Recount**'a tıklayın.

![Stok Yeniden Sayımı Onay Sayfası: Seçilen Stok Öğeleri kartı ve sayılan eldeki miktar ve nedeni dolu bir Yeniden Sayım Detayı formu](/static/core/admin/img/help/stock-bulk-actions/recount-stock-confirmation.webp)

Diğer iki eylemden farklı olarak, yeniden sayım stok hareketini her iki yönde de değiştirebilir — sistemin beklentisinden fazla sayı sayarsanız yukarı, eksik sayı sayarsanız aşağı. Girdiğiniz sayım, açık siparişlere ayrılmış miktarın altına düşerse, Spwig hâlâ onu uygular (bir sayım, tartışmaya değer bir şey değil), ancak bu öğenin **Mevcut** sayısı stok listesinde `0` olarak gösterilir ve durum simgesi Stokta Yok olarak değişir — etkilenen siparişlerin hâlâ yerine getirilebilir olup olmadığını kontrol etmek için bu durumu bir sinyal olarak kabul edin.

Her bir yeniden sayım, eski ve yeni eldeki miktarlar arasındaki düzeltmeyi (pozitif veya negatif) gösteren bir **Fiziksel Yeniden Sayım** hareketi olarak kaydedilir.

## Neyin değiştiğini inceleme

Her bir aktarım, yazım ve yeniden sayım, diğer stok değişiklikleriyle aynı şekilde kaydedilir:

- Bir stok öğesini açın ve **Stok Hareketleri** bölümünü aşağıya doğru kaydırın ve telif tarihi tarihini görün
- Veya **Ürünler > Stok Hareketleri**'ne giderek tüm öğeler arasındaki hareketleri tarayın, türüne göre filtreleyebilirsiniz

Her giriş, hareket türü, miktar değişimi, önceki ve yeni eldeki miktarlar, değişikliği yapan kişi ve girdiğiniz sebep (varsa) hakkında bilgi içerir — yani bir toplu aktarım veya yazım, tekli manuel ayarlamalar kadar izlenebilir.

## İpuçları

- Fiziksel stok sayımından hemen sonra **Stok Yeniden Sayımı**'nı çalıştırın — sayım sayıları hafızada iken, hareket tarihçesinden sonra bu sayıları çözmekten daha kolaydır.
- Yazım ve yeniden sayım için **Neden** alanını doldurun. Altı ay sonra, "Depolama sırasında su hasarı" ifadesi, bir denetim tarihi için boş bir alandan çok daha faydalı olur.
- Stok aktarımı yapmadan önce, onay sayfasındaki **Mevcut** sütununu kontrol edin — zaten ayrılmış birimleri hesaba katarak, seçtiğiniz öğelerin birinden miktarın çok yüksek olup olmadığını anında anlayacaksınız.
- Bu eylemler, her seçili öğe için aynı miktarı uygular. Gerçekten aynı miktarı taşımak, yazmak veya yeniden saymak istediklereri için gruplandırılmış öğeleri seçin ve istisnaları tek tek ele alın.
- Bir mağazada POS kullanıyorsanız, depo yedek stokları online siparişler için "meydana