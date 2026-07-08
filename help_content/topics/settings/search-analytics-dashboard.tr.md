---
title: Arama Analitiği Panosu
---

Arama Analitiği panosu, mağazanızdaki her arama sorgusunu izler ve müşterilerin ne aradığını, hangi aramaların başarılı veya başarısız olduğunu ve arama sisteminizin ne kadar hızlı yanıt verdiğini gösterir. Bu verileri kullanarak popüler ürünleri belirleyin, eksik stokları keşfedin, eşanlamlılar oluşturun ve arama performansını optimize edin.

Analitik izleme, **Arama Ayarları > Analitik sekmesi** içinde etkinleştirilmelidir.

![Analitik Pano](/static/core/admin/img/help/search-analytics-dashboard/analytics-dashboard.webp)

## Pano Genel Bakış

**Arama > Arama Analitiği**'ne giderek panoya erişin. Sayfa şu öğeleri gösterir:

**İstatistik Kartları** - Bugün ve geçen hafta için hızlı ölçümler:
- Bugün toplam aramalar
- Bu hafta toplam aramalar
- Sıfır sonuç sorguları (hiç ürün döndüren aramalar)
- Ortalama yanıt süresi (milisaniye cinsinden)

**En Çok Aranan Sorgular Tablosu** - En sık kullanılan arama terimleri ve sonuç sayıları

**Sıfır Sonuç Sorguları** - Hiç sonuç döndüren aramalar (iyileştirme için kritik)

**Sorgu Listesi** - Tüm bireysel arama kayıtları ve filtreler

## Bugün İstatistikleri

**Bugün Toplam Aramalar** - Mağazanızın saat dilimine göre sabahın yarısından beri tüm arama isteklerinin sayısı. Hem otomatik tamamlama hem de tam arama sayfaları isteklerini içerir.

**Bugün Tekil Sorgular** - Bugün kullanılan farklı arama terimlerinin sayısı. Eğer 5 müşteri "laptop" ararsa, bu 5 toplam aramaya rağmen 1 tekil sorgu olarak sayılır.

**Bugün Sıfır Sonuç** - Bugün hiçbir ürün döndüren aramalar. Yüksek sıfır sonuç sayısı, eksik ürünleri veya kötü eşanlamlı kapsamağı gösterir.

Gerçek zamanlı veriler, aramalar gerçekleştiğinde güncellenir.

## Haftalık İstatistikler

**Hafta Toplamı** - Geçen 7 gün içindeki toplam aramalar

**Tekil Sorgular** - Bu hafta kullanılan farklı arama terimlerinin sayısı

**Hafta Üzeri Büyüme** - Geçen hafta ile karşılaştırıldığında yüzdelik değişim (gösterilirse)

Haftalık verileri eğilimleri tespit etmek için kullanın: Arama hacmindeki artış genellikle trafik artışı veya pazarlama kampanyalarıyla ilişkilidir.

## Ortalama Yanıt Süresi

⚠️ **PERFORMANCE MONITORING**

Arama sorgularını yerine getirme ortalama süresi (milisaniye cinsinden). Hedef yanıt süreleri:

| Sorgu Türü | Hedef | Uyarı Seviyesi |
|------------|--------|-------------------|
| Otomatik Tamamlama | < 200ms | Sürekli > 300ms |
| Tam Arama | < 500ms | Sürekli > 800ms |

Eğer ortalama yanıt süresi uyarı eşiğini aşıyorsa:
1. **Arama Ayarları > Önbellekleme sekmesi**'ni kontrol edin - önbellekleme TTL'lerini artırın
2. **Derin Dizinleme sekmesi**'ni gözden geçirin - pahalı özellikleri devre dışı bırakın (doküman dizinleme, büyük kataloglarda inceleme dizinleme)
3. [Arama Performansı Optimizasyonu](/en/admin/help/search-performance-optimization/) kılavuzunu inceleyin

## En Çok Aranan Sorgular

En Çok Aranan Sorgular tablosu, en sık aranan terimleri gösterir:

**Bu Verileri Kullanarak**:
- **Popüler ürünleri öne çıkarın** - Eğer "wireless headphones" en çok aranan sorguysa, bu ürünleri başta gösterin
- **Stok kararları** - Bir kategoride yüksek arama hacmi, talep olduğunu gösterir
- **Eğilimleri belirleyin** - Mevsimsel aramalar, şu anda neyin popüler olduğunu gösterir
- **İçerik yaratımı** - Sıkça aranan konular hakkında blog yazıları veya kılavuzlar yazın

Aylık olarak en çok aranan sorguları gözden geçirerek ürün satışı stratejinizi müşteri ilgi alanlarıyla hizala.

## Sıfır Sonuç Sorguları

**İYİLEŞTİRME İÇİN KRİTİK** - Sıfır sonuç sorguları, mağazanızı optimize etmek için bir altın madeni.

Sıfır sonuç sorguları, temel olarak üç ana nedenle oluşur:

### 1. Eksik Ürünler

Müşteriler, satmadığınız ürünler için arama yapar.

**Örnek**: "yoga halatları" için tekrarlayan aramalar ancak sadece fitness ekipmanları satıyorsunuz, yoga malzemeleri değil.

**Eylem**: Aramalar sık sık tekrar ediyorsa, bu ürünleri kataloğunuzda eklemeyi düşünün.

### 2. Eksik Eşanlamlılar

Müşteriler, ürün açıklamalarınızla eşleşmeyen terimleri kullanır.

**Örnek**: Müşteriler "laptop" ararken, ürünlerinizde "notebook bilgisayar" yazıyor.

**Eylem**: Müşteri terimlerini ürün dilinize eşleştiren eşanlamlı haritaları oluşturun. [Eşanlamlılar ve Yeniden Yönlendirmeleri Yönetme](/en/admin/help/managing-synonyms-redirects/) kılavuzunu inceleyin.

### 3. Kötü Bulanıklık Eşleme

Yazım hataları veya eksik yazımlar, bulanık arama etkin olduğunda bile eşleşmeyebilir.

**Örnek**: "accomodate" araması "accommodate" ürünleri bulamaz.

**Eylem**:
- **Arama Ayarları > Bulanıklık Eşlemesi sekmesi**'nde benzerlik eşiğini düşürün (0.80'den 0.75'e)
- Yaygın yazım hataları için tek yönlü eşanlamlılar ekleyin

**Haftalık İş Akışı**:
1. Her Pazartesi sıfır sonuç sorgularını gözden geçirin
2. Kategorize edin: Eksik ürün, eksik eşanlamlı veya yazım hataları
3. Sıkça aranan terimler için eşanlamlılar ekleyin
4. Stok planlaması için ürün eksikliklerini not alın

## Sorgu Detayları

Listedeki herhangi bir sorguyu tıklayarak tam detayları görüntüleyin:

**İzlenen Alanlar**:
- **Sorgu metni** - Müşterinin ne aradığını
- **Zaman damgası** - Aramanın gerçekleştiği zaman
- **Sonuç sayısı** - Kaç sonuç döndürüldüğü
- **Yanıt süresi** - Yürütme süresi (performans izleme)
- **Kullanıcı** - Oturum açmış müşteri (kullanıcı izleme etkinse)
- **Oturum Kimliği** - Anonim oturum tanımlayıcısı
- **Dil** - Arama sırasında mağaza dili
- **Motor** - Sorguyu işleyen arama motoru

## Filtreleme ve Arama

Belirli bölümleri analiz etmek için filtreleri kullanın:

**Tarih Hiyerarşisi** - Tarih, ay veya yıl bazında filtreleme yapın

**Dil Filtresi** - Dil bazında aramaları görün (çok dilli mağazalar için değerlidir)

**Motor Filtresi** - Farklı motorlar arasında arama davranışlarını karşılaştırın

**Sıfır Sonuç Anahtarı** - Sadece sonuç döndüren sorguları göster

**Arama Kutusu** - Belirli bir sorgu metnini bulun

## Veri İstemek

**İstemek**'e tıklayarak sorgu verilerini CSV olarak indirin ve Excel veya veri araçlarında daha derin bir analiz yapın.

**CSV içerir**:
- Tüm sorgu metinleri
- Zaman damgaları
- Sonuç sayıları
- Yanıt süreleri
- Dil ve motor verileri

İstemek için kullanın:
- Zaman içinde eğilim analizi
- Mevsimsel arama desenlerini belirleme
- Performans denetimi
- Stakeholderlara sunum

## Gizlilik Dikkatinde Olun

Arama analitiği izleme gizliliği korur:

**Kullanıcı Takibi** (isteğe bağlı) - Aramaları oturum açmış müşteri hesaplarına bağlar. GDPR/CCPA uyumlu olmak için **Arama Ayarları > Analitik sekmesi** içinde devre dışı bırakın.

**Oturum Takibi** (varsayılan) - Anonim oturum kimliklerini kullanarak müşteri tanımlamadan arama davranışlarını izler. Gizlilik dostu.

**Veri Saklama** - Arama sorguları veritabanında kalıcı olarak saklanır. Uygunluk için özel bir saklama politikası uygulayın.

## Analitikleri Kullanarak Aramayı Geliştirme

Arama analitiğinden elde edilen uygulanabilir bilgiler:

**Haftalık Görevler**:
- Sıfır sonuçları gözden geçirin ve yaygın terimler için eşanlamlılar ekleyin
- Yanıt sürelerini izleyin ve sürekli yavaşsa optimize edin
- En çok arananları belirleyin ve bu ürünlerin iyi stoklandığından emin olun

**Aylık Görevler**:
- En çok sorguları analiz ederek ürün seçimini belirleyin
- Verileri iste ve mevsimsel eğilimleri belirleyin
- Dil özel arama desenlerini gözden geçirin
- Yeniden yönlendirme vurum sayılarını izleyerek navigasyon kısayollarını optimize edin

**Çeyreklik Görevler**:
- Eşanlamlı etkinliğini denetleyin (sıfır sonuçlar azalmış mı?)
- Arama hacmi büyümesini genel trafik ile karşılaştırın
- A/B testi ağırlık değişikliklerini ve sonuçların ilgili olup olmadığını ölçün
- Arama talebine dayalı olarak yeni ürün kategorilerinin eklenmesi gerekip gerekmediğini gözden geçirin

## İpuçları

- **Sıfır sonuç sorguları iyileştirme için altın madenidir** - Onlar doğrudan size müşterilerin ne istediğini ama vermediğiniz şeyi söyler
- **Analitikleri Pazartesi sabahları gözden geçirin** - Geçen haftanın verilerine dayalı olarak haftanızı optimize etmekle başlayın
- **Yanıt süresi sürekli 300ms'den fazla ise sorunla ilgilenin** - İlk olarak önbellekleme ayarlarını kontrol edin, ardından derin dizinleme özellikleri
- **Trend analizi için CSV isteyin** - Tablo analizi, yönetici arayüzinde açık olmayan desenleri ortaya çıkarır
- **Ürünleri eklemeyi düşünmeden önce eşanlamlılar oluşturun** - Müşteriler "tablet kılıfları" ararken, "koruyucu kaplamalar" diyorlarsa, önce eşanlamlıyı ekleyin
- **Mevsimsel arama desenlerini izleyin** - Ekim ayında "kış botları", Mart ayında "deniz kıyafetleri" - stokları buna göre planlayın

