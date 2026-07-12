---
title: Toplu Bono Kodları İçe Aktarma
---

Bono içe aktarma sihirbazı, CSV veya XLSX tablosu yükleme ile aynı anda yüzlerce bono kodu oluşturmanıza olanak tanır. Bu, önceden basılmış kodlara, üçüncü taraf sisteminizden gelen sadakat programı kodlarına veya büyük bir kampanya başlatmanız gerektiğinde her kodu elle eklemek zorunda kalmadan idealdir.

![Bono listesi ve İçe Aktarma düğmesi](/static/core/admin/img/help/voucher-import/voucher-list-import-button.webp)

## İçe Aktarma Başlatma

**Pazarlama > Bono**'ya gidin ve sayfanın sağ üst köşesindeki **İçe Aktarma** düğmesine tıklayın. Bu, üç adımlı içe aktarma sihirbazını açar.

## Adım 1: Dosyanızı Yükleme ve Toplu İndirim Ayarlarını Ayarlama

![İçe aktarma yükleme formu](/static/core/admin/img/help/voucher-import/import-upload.webp)

İlk sayfa iki bölümden oluşur: dosya yükleme ve toplu indirim ayarları.

### Dosyanızı Hazırlama

5 MB'a kadar olan bir `.csv` veya `.xlsx` dosyası yükleyin. Dosyanın ilk satırı başlık satırı olmalıdır. En düşük gereksinim, bono kodlarını içeren tek bir sütun olmalıdır — diğer tüm sütunlar isteğe bağlıdır.

İçe aktarma aracı, yaygın sütun isimlerini otomatik olarak tanır. Dosyanız aşağıdaki isimlerden herhangi birini kullanıyorsa, Spwig, bir sonraki sayfada ekstra tıklamadan doğru haritalamayı önceden seçer:

| Sütun isminiz | Haritalanır |
|-----------------|---------|
| `code`, `voucher_code`, `coupon_code`, `promo_code` | Bono kodu |
| `name`, `title`, `campaign` | İçerik adı |
| `description`, `details`, `note` | Müşteri odaklı açıklama |
| `external_id`, `member_id`, `reference` | Dış ID |

**İpucu:** İlk olarak XLSX şablonunu indirin (aşağıdaki [Bono Şablonu Olarak Dışa Aktarma](#exporting-vouchers-as-a-template) bölümüne bakın) — bu, içe aktarma aracı tarafından beklenen tam olarak sütun isimlerini kullanır, bu nedenle sütun haritalama otomatiktir.

### Dosya Sınırlamaları

- Maksimum dosya boyutu: **5 MB**
- İçe aktarma başına maksimum satır sayısı: **5.000 kod**

### Toplu İndirim Ayarlarını Ayarlama

Topludaki her bono, bu sayfada yapılandıracağınız aynı indirim ayarlarını paylaşacaktır. Tek bir bono oluştururkenki gibi alanları doldurun:

**İndirim Bölümü**

| Alan | Açıklama |
|-------|-------------|
| **İndirim Türü** | Yüzde, Sabit Tutar veya Ücretsiz Kargo |
| **İndirim Değeri** | Kesilecek yüzde (0–100) veya sabit tutar |
| **Maksimum İndirim Tutarı** | Yüzdelik indirimler için isteğe bağlı tavan (örneğin, 20% indirimi $50'e tavanla sınırla) |
| **Uygulama Kapsamı** | Tamamı Sepet, Belirli Ürünler veya Belirli Kategoriler |

**Geçerlilik Bölümü**

| Alan | Açıklama |
|-------|-------------|
| **Başlangıç Tarihi** | Kodların etkin hale geldiği tarih (boş bırakılırsa varsayılan olarak şu an) |
| **Bitiş Tarihi** | Kodların sona erdiği tarih (boş bırakılırsa süresiz) |
| **Geçerlilik Süresi** | Bitiş tarihi yerine alternatif — kodlar bu kadar gün sonra sona erer |

**Kullanım Sınırlamaları Bölümü**

| Alan | Açıklama |
|-------|-------------|
| **Toplam Kullanım Sayısı** | Tüm müşteriler için toplam kupon kullanım sayısı (boş bırakılırsa sınırsız) |
| **Müşteri Başına Maksimum Kullanım Sayısı** | Bir müşteri bu toplu kodlardan birini kaç kez kullanabilir |
| **Minimum Sipariş Değeri** | Kuponun uygulanabilmesi için gereken minimum sepet toplamı |

**Kısıtlamalar**

Aşağıdakilerin herhangi bir kombinasyonunu işaretleyin:
- **Satış ürünlerine uygulanamaz** — zaten indirimli ürünlerle birlikte kullanılamayan kodu engeller
- **Diğer bonolarla birlikte kullanılamaz** — müşterilerin aynı siparişte iki kod kullanmasını engeller
- **Satış ürünleriyle birlikte kullanılamaz** — yukarıdakilerle benzer ancak satış fiyatlı ürünlerle hedeflenir
- **Sadece ilk kez müşteriler için** — kodu önceki tamamlanmış siparişi olmayan müşterilere sınırlar
- **Hemen etkin hale gelir** — işaretlenmiş bırakın, kodların içe aktarıldığı anda hemen etkin hale gelmesini sağlar

Ayarlarla memnun olduğunuzda **Önizleme için Devam Et**'e tıklayın.

## Adım 2: Sütunları Haritala ve Gözden Geçir

![Sütun haritalama ve önizleme sayfası](/static/core/admin/img/help/voucher-import/import-preview.webp)

Önizleme sayfası, üstte dört özet sayaç gösterir:

- **Açıklanan satırlar** — dosyanızda bulunan toplam veri satırları

- **İçe aktarılacak** — yeni oluşturulacak kodlar

- **Yinelenenler** — kataloğunuzda zaten bulunan kodlar

- **Atlanacak (geçersiz)** — doğrulama hataları nedeniyle reddedilen satırlar (boş kod, kod çok uzun, vb.)

### Sütun eşlemesi

**Sütun eşlemesi** tablosu, hangi sütunun her kupon alanına karşılık geldiğini Spwig'e bildirmenizi sağlar. Spwig yaygın başlık adlarını otomatik olarak algılar (yukarıdaki tabloyu inceleyin), ancak her satırda bulunan açılır listeden herhangi bir eşlemeyi değiştirebilirsiniz.

**Kupon kodu** sütunu zorunludur. Diğer alanlar — **İç isim**, **Müşteriye yönelik açıklama** ve **Dış Kimlik** — isteğe bağlıdır. Onları atlayırsanız, Spwig mantıklı varsayılanlar kullanır (iç isim varsayılan olarak "Imported voucher {code}" olur).

### Yinelenen kod stratejisi

Dosyanızdaki herhangi bir kod zaten kataloğunuzda varsa, onlarla nasıl başa çıkacağınızı seçmeniz gerekir:

| Strateji | Ne olur |

|----------|-------------|

| **Yinelenenleri atla** | Mevcut kodlar olduğu gibi bırakılır. Sadece yeni kodlar oluşturulur. |

| **Ayarları üzerine yaz** | Mevcut kodlar bu partinin indirim ayarlarıyla güncellenir. Kodları, kullanım sayıları ve yaratım tarihleri korunur. |

| **İçe aktarımdan vazgeç** | Hatta bir yinelenen bile bulunursa tüm içe aktarma iptal edilir. Mevcut kodların hiçbirine zarar vermeden emin olmak istediğinizde bunu kullanın. |

Bulunan herhangi bir yinelenen kod, karar vermeden önce incelemek için genişletilebilir bir panelde listelenir.

### Veri önizleme tablosu

Sayfanın alt kısmında dosyanızın ilk 20 satırı gösterilir, bu sayede onaylamadan önce sütun eşlemesinin doğru olduğundan emin olabilirsiniz. Mevcut kodlara uyan satırlar vurgulanır.

Her şey doğru göründüğünde, partiyi onaylamak için **N kupon içe aktar**'a tıklayın.

## Adım 3: Sonucu incele

![İçe aktarma sonucu sayfası](/static/core/admin/img/help/voucher-import/import-result.webp)

İçe aktarma tamamlandıktan sonra aşağıdaki özeti göreceksiniz:

- **İçe aktarıldı** — başarıyla oluşturulan kodlar

- **Atlandı** — oluşturulmayan kodlar (yinelenenler veya geçersiz satırlar)

- **İşlenen satırlar** — dosyanızdan değerlendirilen toplam satırlar

- **Başarısız** — beklenmeyen bir hata ile karşılaştı satırlar

**İçe aktarılan kuponları görüntüle**'ye tıklayarak bu partiden gelen kodlara filtrelenmiş kupon listesini açabilirsiniz. Bu, sonucu kontrol etmek veya yeni kodları toplu olarak etkinleştirmek için kolaylaştırır.

Herhangi bir şey yanlış görünüyorsa — örneğin yanlış indirim türü uygulanmışsa — kodları silmek ve yeniden oluşturmak zorunda kalmadan, yeniden içe aktarma üzerinde **Ayarları üzerine yaz** stratejisini kullanarak partiyi düzeltebilirsiniz.

**Başka bir partiyi içe aktar**'a tıklayarak yeni bir yükleme başlatın veya **Kupon listesine geri dön**'e tıklayarak tam kataloğunuzda olun.

## Kuponları şablon olarak dışa aktarma

Kupon listesi, içe aktarıcı tarafından beklenen tam olarak aynı sütun sırasına sahip bir dosya üretmek için XLSX dışa aktarma eylemini destekler. Bu, doğru biçimde bir şablon almanın en kolay yolu:

1. **Pazarlama > Kuponlar**'a gidin

2. Dışa aktarmak istediğiniz kuponları seçin (veya tümünü seçin)

3. **Eylem** açılır listeden **Seçilen kuponları XLSX olarak dışa aktar**'ı seçin

4. **Git**'e tıklayın

İndirilen dosya, içe aktarıcı tarafından anlaşılan tüm 21 sütunu içerir, bunlar içe aktarma sihirbazında partiyi düzeyinde olan alanlar da dahil (indirim türü, tarihler, kullanım sınırları vb.). Bu dosyayı bir referans olarak kullanabilir veya mevcut kodlarınızı düzenle → yeniden içe aktarma döngüsünü kullanarak **Ayarları üzerine yaz** stratejisini kullanarak geçiş yapabilirsiniz.

## İpuçları

Tüm markdown biçimlendirmesini, resim yollarını, kod bloklarını ve teknik terimleri koruyun.

- İlk olarak bir XLSX dışa aktarımı indirerek şablon olarak kullanın — sütun isimleri önceden biçimlendirilmiştir, bu nedenle önizleme sayfasında herhangi bir ayar yapmadan otomatik eşleme yapılır.
- Büyük miktarda kod içeri aktarılmadan önce 5–10 kodla küçük bir test partisi çalıştırın — sütun eşlemeyi ve partisi ayarlarınızı doğrulamak için.
- Kodların zaman içinde dağıtılacağı durumlarda **Geçerlilik Süresi** yerine sabit bir **Bitiş Tarihi** kullanın — böylece her kodun son kullanma tarihi, içeri aktarıldığı zamandan itibaren sayılır, tek bir takvim tarihi yerine.
- Üçüncü taraf sadakat sistemi üzerinden kod alıyorsanız, tedarikçinin üyenin veya müşterinin referansını **Dış ID** sütununa eşleyin — daha sonra kırmızımların dengelemesini yapabilirsiniz.
- Büyük bir içeri aktarma yaptıktan sonra, sonuç sayfasında **İçeri Aktarılan Bono'ları Görüntüle**'ye tıklayarak yalnızca yeni partiyi filtreleyin — ardından onları grup olarak toplu olarak düzenleyebilir, etkinleştirebilir veya devre dışı bırakabilirsiniz.
- Başarısız bir içeri aktarma (**Fail** yinelenen stratejisi kullanılarak) kataloğunuzu değiştirmez, bu nedenle dosyayı düzeltip gereken kadar tekrar denemek güvenlidir.