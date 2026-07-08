---
title: Müşteri Segmentleri
---

Müşteri segmentleri, müşterilerinizi satın alma davranışlarına göre anlamlı gruplara otomatik olarak sınıflandırmaya olanak tanır. Müşteriler segmentlere ayrıldıktan sonra, bu grupları kullanarak pazarlama çabalarınızı odaklayabilirsiniz — örneğin, VIP müşterilere sadakat ödülleri sunmak veya uzun süredir satın alma yapmayan müşterilere geri dönüş kampanyaları göndermek.

Spwig, her müşterinin ölçümlerini segment kriterleriyle karşılaştırır ve müşterinin uygun olduğu en yüksek öncelikli segmente atar. Bu işlem, müşteri verileri güncellendiğinde otomatik olarak gerçekleşir.

## Mevcut segment türleri

Spwig, bir dizi yerleşik segment türüyle gelir. Her segment türü sabit bir iç kimliğe sahiptir, ancak görüntüleme adını, açıklamayı, kriterleri ve rengi, müşterilerinizi nasıl düşündüğünüzle uyumlu hale getirebilirsiniz.

| Segment Türü | Tipik Kullanım |
|---|---|
| **Misafir Müşteri** | Hesap oluşturmadan ödeme yapan müşteriler |
| **Yeni Müşteri** | İlk satın alma yapan yeni müşteriler |
| **Düzenli Müşteri** | Sürekli satın alma geçmişine sahip müşteriler |
| **Sık Müşteri** | Sık satın alan müşteriler (siparişler arası kısa süre) |
| **Yüksek Değer** | Toplam harcaması yüksek müşteriler |
| **VIP Müşteri** | En değerli ve sadık müşterileriniz |
| **İndirim Avcısı** | Satış dönemlerinde satın alma eğiliminde olan müşteriler |
| **Risk Altında** | Uzun süredir satın alma yapmayan müşteriler |
| **Aktif Değil** | Uzun süredir aktif olmayan müşteriler |

## Segment kriterlerini anlama

Her segment, kriterlerin bir kombinasyonuyla tanımlanır. Spwig, bu kriterleri her müşterinin depolanan ölçümleriyle karşılaştırır. Bir segment içindeki tüm kriterler birleştirilir — bir müşteri, segmente dahil olmak için belirlenen tüm koşulları karşılamalıdır.

### Harcama kriterleri

- **Min Toplam Harcama** — müşteri, tüm tamamlanmış siparişler üzerinden en az bu miktarda harcama yapmış olmalıdır
- **Max Toplam Harcama** — müşteri, bu miktardan fazla harcama yapmamalıdır

Bir harcama aralığı kullanarak belirli bir seviyeyi hedefleyebilirsiniz. Örneğin, Min 500 $ ve Max 2.000 $ olarak ayarlarsanız, orta seviye müşterileri hedeflemiş olursunuz.

### Sipariş sayısı kriterleri

- **Min Sipariş Sayısı** — müşteri, en az bu kadar tamamlanmış siparişe sahip olmalıdır
- **Max Sipariş Sayısı** — müşteri, bu kadar tamamlanmış siparişe sahip olmamalıdır

Min Sipariş Sayısı ile bir harcama minimumu birleştirmek, VIP müşterileri tanımlamak için güvenilir bir yoldur: sık satın alıyorlar *ve* çok harcıyorlar.

### Yenilik kriterleri

- **Min Son Satın Alma Gün Sayısı** — müşterinin en son siparişi en az bu kadar gün önce olmalıdır
- **Max Son Satın Alma Gün Sayısı** — müşterinin en son siparişi bu kadar gün içinde olmalıdır

Yenilik kriterleri, risk altındaki ve aktif olmayan segmentler için önemlidir. Örneğin, Min Günleri 90 ve Max Günleri 365 olarak ayarlarsanız, sessizleşmiş ama tamamen kaybolmamış müşterileri tanımlarsınız.

## Segment önceliği

Bir müşteri birden fazla segmente uysa, **en yüksek öncelik** değeri olan segment kazanır. Her segmentin önceliğini, segment formunun **Görünüm Ayarları** bölümünde ayarlayabilirsiniz.

**Misafir Müşteri** segmenti, öncelik sırasından bağımsız olarak her zaman ilk değerlendirilir, çünkü misafir durumu, satın alma kriterleri yerine hesap türü tarafından belirlenir.

## Segmentleri görüntüleme ve yönetme

**Müşteriler > Müşteri Segmentleri**'ne giderek tüm yapılandırılmış segmentlerinizi görebilirsiniz. Liste, her segmentin görüntüleme adını, iç türünü, atanan rengi, önceliğini, eşleşen müşterilerin mevcut sayısını ve segmentin aktif olup olmadığını gösterir.

![Müşteri Segmentleri Listesi](/static/core/admin/img/help/customer-segments/segments-list.webp)

### Bir segment oluşturma veya düzenleme

1.

**Müşteriler > Müşteri Segmentleri**'ne gidin
2.

Var olan bir segmenti düzenlemek için tıklayın veya **+ Müşteri Segmenti Ekle**'ye tıklayarak yeni bir segment oluşturun
3.

Tüm markdown biçimlendirmesini, görsel yollarını, kod bloklarını ve teknik terimleri koruyun.

**Segment Bilgisi** sekmesini doldurun:
   - **Ad** — segment türünü aşağı açılan listeden seçin
   - **Gösterilecek Ad** — admin'de görünen insan tarafından okunabilir ad (örneğin, "VIP Müşteriler")
   - **Açıklama** — bu segmentin neyi temsil ettiğini açıklayan kısa bir iç not
4.

İlgili sekmelere kriterleri ayarlayın:
   - **Kriterler - Harcamalar** — toplam harcama için minimum ve maksimum değer
   - **Kriterler - Siparişler** — sipariş sayısı için minimum ve maksimum değer
   - **Kriterler - Yenilik** — son satın alma tarihinden itibaren minimum ve maksimum gün sayısı
5.

**Gösterim Ayarlarını** yapılandırın:
   - **Renk** — bu segmentin listelerde görsel olarak nasıl tanımlandığını belirleyen bir heksadesimal renk
   - **Öncelik** — daha yüksek bir sayı, bu segmentin daha önce değerlendirilmesini sağlar
   - **Aktif mi?** — segmenti silmeden devre dışı bırakmak için işaretini kaldırın
6.

Değişiklikleri uygulamak için **Kaydet**'e tıklayın

### Örnek: VIP segmentini yapılandırma

Aşağıda yüksek değerli bir VIP segmenti için gerçekçi bir örnek verilmiştir:

| Alan | Değer |
|---|---|
| Ad | `vip` |
| Gösterilecek Ad | VIP Müşteriler |
| Min Toplam Harcama | $1,000 |
| Min Sipariş Sayısı | 5 |
| Max Son Satın Alma Gün Sayısı | 180 |
| Öncelik | 90 |
| Renk | `#FFD700` |

Bu, bir müşterinin en az $1,000 harcama yapmış, en az 5 sipariş vermiş ve son 6 ay içinde bir satın alma yapmışsa VIP olarak kabul edildiğini belirtir.

### Örnek: Risk Altında Olan segmentini yapılandırma

| Alan | Değer |
|---|---|
| Ad | `at_risk` |
| Gösterilecek Ad | Risk Altında |
| Min Son Satın Alma Gün Sayısı | 60 |
| Max Son Satın Alma Gün Sayısı | 180 |
| Öncelik | 30 |
| Renk | `#FF6B35` |

## Segmentleri hedefli pazarlama için kullanma

Segmentler, admin'deki müşteri profillerinde gösterilir, bu nedenle ekibiniz her müşteriye hangi seviyeye ait olduğunu hemen bilir. Bu bilgiyi şu şekilde kullanabilirsiniz:

- **Hedefli kupon kampanyaları başlatın** — belirli bir segmentteki müşterilere özel kuponlar oluşturun, ardından e-posta sisteminizi kullanarak sadece bu gruba gönderin
- **Destek önceliğini belirleyin** — VIP veya yüksek değerli müşterileri işaretleyin, böylece ekibiniz onlara öncelikli hizmet sağlayabilir
- **Yeniden etkinleştirme planlayın** — Risk Altında ve Aktif Olmayan segmentleri düzenli olarak inceleyerek yeniden etkinleştirme e-postası veya özel teklif gereken müşterileri belirleyin
- **Pazarlama harcamalarını ayarlayın** — yüksek değerli müşterilerin hangi kanallardan geldiğini analiz ederek, bu kanallara odaklanarak kazanç sağlayabilirsiniz

## İpuçları

- Kendi kriterlerinizi oluşturmadan önce yerleşik segment türlerini kullanın — bunlar kutudan çıkmadan en yaygın segmentasyon ihtiyaçlarını karşılar
- Her segmentteki müşteri sayısını düzenli olarak inceleyin; sıfır müşteri olan bir VIP segmenti veya hızla büyüyen bir Risk Altında segmenti araştırmaya değerdir
- **Öncelik** alanını dikkatli kullanın — eğer kriterler segmentler arasında çakışıyorsa (örneğin, bir müşteri hem Sık Müşteri hem de Yüksek Değerli segmentine uyguyorsa), daha yüksek öncelikli segment kazanır
- Şu an kullanmadığınız segmentleri silmeden devre dışı bırakın — daha sonra kriterleri yeniden yapılandırmadan yeniden etkinleştirebilirsiniz
- Segment kriterleri, depolanan müşteri metrikleriyle karşılaştırılır ve bu metrikler otomatik olarak yeniden hesaplanır. Eğer segment sayıları eskiyse, admin'deki Müşteri Metrikleri bölümünden metrikleri yeniden hesaplayabilirsiniz