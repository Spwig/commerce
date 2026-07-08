---
title: İlgili Ağırlıklar ve Derin Dizinleme
---

İlgili ağırlıklar ve derin dizinleme, arama sonuçlarının sıralanışını ve hangi ürün verilerinin aranacağını kontrol eder. Ağırlıklar, önem çarpanlarıdır - 2,0 ağırlığı, o alandaki eşleşmelerin 1,0 ağırlığındakilerden iki kat daha önemli olduğunu ifade eder. Derin dizinleme, aramanın temel ürün isimlerini aşıp SKU'lar, öznitelikler, incelemeler ve hatta belge içeriklerine kadar uzayıp uzamayacağını belirler. Bu kılavuz, her iki sistemi, ne zaman ayarlamalığınızı ve kritik performans sonuçlarını açıklar.

Varsayılan ayarlar, çoğu e-ticaret mağazaları için iyi çalışır. Sadece özel sıralama veya dizinleme ihtiyaçlarınız varsa ayarlamalar yapın.

![Weights Tab](/static/core/admin/img/help/search-settings-overview/search-settings-weights.webp)

## Ağırlıkları Anlamak

Ağırlıklar, farklı alanlarda metin eşleşmeleri bulunduğunda uygulanan çarpanlardır (0,0-2,0 ölçeğinde). Daha yüksek ağırlıklar, o alandaki eşleşmelerin sonuçlarda daha yüksek sıralanmasını sağlar.

**Örnek**: Eğer bir ürünün hem isminde (ağırlık 1,50) hem de açıklamasında (ağırlık 0,80) "laptop" varsa:
- İsim eşleşmesi, ilgililik puanına 1,50 katkı sağlar
- Açıklama eşleşmesi, 0,80 katkı sağlar
- Toplam puan, diğer ürünlerle kıyaslandığında sıralamayı belirler

Ağırlıklar, arama sonuçlarını sıralarken belirli alanları diğerlerine göre önceliklendirmenizi sağlar.

## Ağırlık Kategorileri ve Varsayılanlar

**Arama Ayarları > Ağırlıklar sekmesi**'ne giderek tüm ağırlık ayarlarını görüntüleyin:

| Alan | Varsayılan Ağırlık | Sebep |
|-------|---------------|-----------|
| **weight_name** | 1.50 | Ürün isimleri en önemlidir - müşteriler genellikle isim eşleşmelerini en üstte görmek ister |
| **weight_sku** | 1.20 | SKU'lar özel tanımlayıcılar - B2B ve tekrarlayan müşteriler için önemlidir |
| **weight_description** | 0.80 | Açıklamalar bağlam sağlar ancak isim eşleşmelerinden daha az önemlidir |
| **weight_categories** | 0.80 | Kategori eşleşmeleri tarif etmeye yardımcı olur ancak isim/SKU kadar özgün değildir |
| **weight_attributes** | 0.70 | Renk, boyut, malzeme aramaları - faydalı ancak destekleyici bilgi |
| **weight_brands** | 0.70 | Marka filtrelemesi önemlidir ancak çoğu mağaza için temel arama kriteri değildir |
| **weight_blog_posts** | 0.60 | Blog içerikleri e-ticaret odaklı aramalarda daha az önemlidir (en düşük öncelik) |
| **weight_reviews** | 0.50 | Kullanıcı oluşturulan içerikler en az kontrol edilir - en düşük ağırlık |

Bu varsayılanlar, ürün keşfi temel arama hedefi olan tipik bir e-ticaret mağazasını varsayar.

## Ağırlıkları Ne Zaman Ayarlamalısınız

Mağazanızın öncelikleri tipik e-ticaret desenlerinden farklı olduğunda ağırlıkları ayarlayın:

**SKU'ya Dayalı Mağazalar (B2B, Toptan Satış)** - `weight_sku`'u 1,8-2,0'ye çıkarın, böylece ürün kodu aramaları sonuçlarda öne çıkar. B2B müşterileri genellikle tam SKU ile arama yapar.

**Markaya Odaklı Mağazalar** - Müşterilerin çoğunun markaya göre alışveriş yaptığı durumlarda (`weight_brands`'ı 1,2-1,5'ye çıkarın) (tasarım kıyafetleri, lüks ürünler).

**İçerik Yoğun Mağazaları** - Blog içeriklerinin ürünler kadar önemli olduğu içerik yayıncısı veya eğitim mağazalarıysanız, `weight_blog_posts`'u 0,9-1,2'ye çıkarın.

**Öznitelik Yoğun Mağazaları (Moda)** - Müşterilerin sık sık renk, boyut, tarz özniteliklerine göre arama yaptığı durumlarda `weight_attributes`'ı 1,0-1,2'ye çıkarın.

## Ağırlık Ayarlamaları Örneği

| Mağaza Türü | Önerilen Ayarlamalar |
|-----------|------------------------|
| **B2B Toptan Satış** | weight_sku: 2.0, weight_name: 1.3, weight_description: 0.6 - Ürün kodlarını önceliklendirin |
| **Moda Butiği** | weight_attributes: 1.2, weight_brands: 1.2, weight_name: 1.4 - Renk/stil/marka önemlidir |
| **İçerik Yayıncısı** | weight_blog_posts: 1.2, weight_name: 1.3, weight_reviews: 0.7 - İçerik ürün kadar önemlidir |
| **Genel E-ticaret** | Varsayılanları kullanın - Tipik çevrimiçi mağazalar için dengeli |

Her seferinde sadece bir ağırlığı ayarlayıp, diğer değişiklikler yapmadan önce test edin.

## Derin Dizinleme Genel Bakış

⚠️ **PERFORMANS UYARISI** - Her derin dizinleme seçeneği, sorgu karmaşıklığını ve ek yükü artırır.

Derin dizinleme, temel ürün isim/açıklama aramasını, ek verilere kadar genişletir:

![Derin Dizinleme Sekmesi](/static/core/admin/img/help/search-settings-overview/search-settings-deep-indexing.webp)

**Arama Ayarları > Derin Dizinleme sekmesi**'ne giderek yapılandırın.

## SKU'ları Dizinle

**Varsayılan**: AÇIK, **Performans Etkisi**: Düşük

Arama dizinine ürün ve varyasyon SKU'larını dahil eder. Varyasyon JOIN'ini tetikler (küçük maliyet).

**AÇIK tutun**: B2B mağazalarında müşteriler ürün kodlarını bildiği için kritik öneme sahiptir. Önceki siparişlerden SKU'yu hatırlayan geri dönen müşterilere de yardımcı olur.

**Kapat**: Sadece SKU'ya sahip olmuyorsanız. Performans etkisi ihmal edilebilir.

## Öznitelikleri Dizinle

**Varsayılan**: AÇIK, **Performans Etkisi**: Orta

Arama dizinine ürün özniteliklerini (renk, boyut, malzeme, özel öznitelikler) dahil eder. Öznitelikler tablosuna JOIN yapar.

**AÇIK tutun**: Giyim, yapılandırılabilir ürünler veya müşterilerin ürün özelliklerine göre arama yapan ("kırmızı elbise", "büyük t-shirt") herhangi bir mağazada önemlidir.

**Kapat**: 20.000'den fazla ürün olan kataloglarda ve ürün başına birçok öznitelik varsa 50-100 ms ek yükü olabilir. Performans kritik ve müşteriler özniteliklerle arama yapmıyorsa kapatın.

## Özel Alanları Dizinle

**Varsayılan**: AÇIK, **Performans Etkisi**: Orta

Arama dizinine satıcı tarafından tanımlanmış özel alanları JSONField'den dahil eder. JSONField gezintisi gerekir.

**AÇIK tutun**: Özel alanları arama için ürün verisi olarak kullanıyorsanız (garanti bilgisi, teknik özellikler, uyumluluk detayları).

**Kapat**: Özel alanları kullanmıyorsanız veya özel alanlar arama dışı veri içeriyorsa (iç notlar, muhasebe kodları). Kapatmak JSONField işleme ek yükünü tasarruf eder.

## İncelemeleri Dizinle

**Varsayılan**: AÇIK, **Performans Etkisi**: Orta-Yüksek

Onaylanmış inceleme başlıklarını ve yorumlarını arama dizinine dahil eder. İncelemeler tablosuna JOIN yapar ve metin arama ek yükünü ekler.

**AÇIK tutun**: İncelemeye dayalı kataloglarda, müşteriler ürünleri inceleme içeriğine göre arıyor ("su geçirmez laptop çantası" gibi ifadeler inceleme metninde görülebilir).

**Kapat**: 20.000'den fazla ürün olan kataloglar veya ürün başına birçok incelemesi olan mağazalar. Büyük kataloglarda 100-200 ms ek yükü ekler.

## Belgeleri Dizinle

**Varsayılan**: KAPALI, **Performans Etkisi**: ÇOK YÜKSEK 🚨

**KASITLI OLARAK AÇMA** - En pahalı arama özelliği.

Belge dizinleme, dijital ürünlerle eklenen PDF, DOCX ve XLSX dosyalarından metni çıkarır ve dosya içeriklerini arama yapmaya olanak tanır.

**Teknik Detaylar**:
- PyPDF2, python-docx ve openpyxl kütüphanelerini kullanır
- Arama sırasında senkron dosya I/O ve metin çıkarımı yapar
- Dosyaları MD5 checksum ile izler (dosya değiştiğinde sadece yeniden dizinlendirir)
- Büyük dosyalar (>10MB PDF'ler) üzerinde zaman aşımı riski vardır

**Performans Etkisi**:
- Çok pahalı başlangıç dizinleme (büyük kütüphaneler için dakikalar veya saatler)
- Anlamlı sorgu ek yükü (100-500 ms ek gecikme)
- Büyük belgeler için hafıza yoğunluğu

**Sadece şu durumlarda etkinleştirin**:
- Dijital ürün satıyorsanız ve belgelerde arama yapmak istiyorsanız (e-kitaplar, raporlar, el kitapları)
- Kataloğunuz küçük (<500 dijital ürün)
- Sunucunuz yeterli kaynaklara sahip
- Etkisini tam olarak test etmişsiniz

**Dijital ürün mağazaları için**: Müşterilerin gerçekten belge içeriklerini arama ihtiyacı olup olmadığını değerlendirin, yoksa ürün isim/açıklama araması yeterli olabilir.

## Performans Etkisi Tablosu

| Özellik | Varsayılan | Etki | Ne Zaman Kullanın |
|---------|---------|--------|----------|
| SKU'ları Dizinle | AÇIK | Düşük | Her Zaman (B2B için kritik) |
| Öznitelikleri Dizinle | AÇIK | Orta | Yapılandırılabilir Ürünler |
| Özel Alanları Dizinle | AÇIK | Orta | Özel Alanları Kullanıyorsanız |
| İncelemeleri Dizinle | AÇIK | Orta-Yüksek | İncelemeye Dayalı Mağaza |
| Belgeleri Dizinle | KAPALI | Çok Yüksek | Sadece Dijital Ürünler (Önce Test Edin) |

Etki, tipik katalogları varsayar. Büyük kataloglar (>50.000 ürün) orantılı olarak daha yüksek bir ek yükü yaşar.

## Ağırlık Değişikliklerini Test Etme

Ağırlıkları ayarlamak için şu test akışını izleyin:

1. **Bir ağırlığı bir seferde değiştirin** - Aynı anda birden fazla ağırlığı ayarlamayın; sonuçlara neden olan değişikliği belirleyemeyeceksiniz
2. **Küçük artışlar** - Her seferinde ±0,2 (örneğin, 1,0 → 1,2, değil 1,0 → 1,8) ile ayarlayın
3. **Gerçek sorgularla test edin** - Analitiklerden gerçek müşteri arama terimlerini kullanın, rastgele testlerden kaçının
4. **Analitikleri izleyin** - En çok kullanılan sorguları kullanarak değişiklik öncesi ve sonrası sonuç ilgililiklerini karşılaştırın
5. **1-2 hafta bekleyin** - Müşterilerin yeni sıralamalarla etkileşim kurmasına zaman tanıyın
6. **Tıklama oranlarını ölçün** - Müşteriler sonuçlara daha fazla/daha az tıklıyor mu?

## Performans ve Doğruluk Arasındaki Denge

Daha fazla dizinleme = daha iyi arama sonuçları ancak daha yavaş performans:

**Senaryo: Küçük Katalog (<1.000 ürün)**
- Tüm dizinleme seçeneklerini etkinleştirin (SKU'lar, öznitelikler, özel alanlar, incelemeler)
- Performans etkisi minimal
- kapsamlı arama yetenekleri

**Senaryo: Orta Katalog (1.000-10.000 ürün)**
- SKU'ları, öznitelikleri, özel alanları AÇIK tutun
- Ürün başına 10'dan fazla inceleme varsa incelemeleri kapatmayı düşünün
- Yanıt sürelerini izleyin

**Senaryo: Büyük Katalog (>10.000 ürün)**
- SKU'ları AÇIK tutun (düşük etki)
- İnceleme dizinleme işlemini KAPATIN (yüksek etki)
- Kullanılmayan özel alanları KAPATIN
- **Dijital ürün dizinleme asla etkinleştirilmesin**
- 50.000'den fazla ürün için Elasticsearch'i düşünün

Katalog boyutunuz ve sunucu kaynaklarınız temelinde dengelenebilir.

## Motor Özel Ağırlık Geçersizleştirme

Arama motoru oluştururken (3. Adım), o özel motor için küresel ağırlıkları geçersiz kılabilirsiniz.

**Kullanım Durumu**: Blog odaklı motor
- "blog" motoru oluşturun
- `weight_blog_posts`'u 1,5'e geçersiz kılın (küresel 0,60'a göre)
- Blog içeriği, blog motoru aramalarında daha yüksek sıralanır

Çoğu motor ağırlıkları geçersiz kılmasın - boş bırakın ve küresel ayarları devralın.

## İpuçları

- **Belge dizinleme asla etkinleştirilmesin, mutlaka kritik değilse** - Tüm arama özellikleri arasında en yüksek performans maliyeti
- **B2B mağazaları: weight_sku'yu 2,0'ye çıkarın** - Ürün kodları temel arama yöntemidir
- **Düşük trafiğe sahip saatlerde ağırlık değişikliklerini test edin** - Zirve saatlerinden önce performans etkisini gözlemleyin
- **Dizinleme etkinleştirdikten sonra yanıt sürelerini izleyin** - Analitikler panelinde yavaşlamaları kontrol edin
- **20K'den fazla ürün olan kataloglarda inceleme dizinleme işlemini kapatın** - Performans kaybı önemli
- **Test için bir ağırlık değişikliği seferinde** - Aynı anda yapılan değişikliklerle neden-sonuç belirleyemeyebilirsiniz
- **Belge çıkarımı için PyPDF2/docx/openpyxl gereklidir** - Belge dizinleme etkinleştirmeden önce bu kütüphanelerin yüklü olduğundan emin olun

