---
title: Arama Performansı Optimizasyonu
---

Arama performansı doğrudan müşteri deneyimi ve dönüşümleri üzerinde etkili olur. Yavaş aramalar müşterileri kızdırır ve geri dönüş oranlarını artırır. Bu kapsamlı kılavuz, Spwig'in veritabanı doğasına özgü arama sistemindeki yaygın performans tıkanıklıklarını belirler, optimizasyon stratejileri sağlar ve performans hedefleri koyar. Bu kılavuzu, arama yanıt süreleri kabul edilebilir eşiği aşarsa veya katalog büyümesi için planlama yaparsanız kullanın.

Hedef yanıt süreleri: <200ms otomatik tamamlama, <500ms tam arama. Aşağıdaki optimizasyon kontrol listesini izleyerek bu hedefleri elde edin.

## Performans Metriklerini Anlamak

**Arama > Arama Analitiği** içinde bu metrikleri izleyin:

**Yanıt Süresi** - Bir arama sorgusunu yürütmek için gerekli milisaniye (yalnızca sunucu tarafı, ağ gecikmesi hariç)

**Önbellek Hit Oranı** - Önbellekten sunulan arama yüzdesi (önbellek vs veritabanı)

**Sorgu Sayısı** - Her arama için veritabanı sorguları sayısı (daha az daha iyidir)

**Veritabanı Sorgu Süresi** - Veritabanında geçirilen süre vs uygulama kodu

## Performans Hedefleri

| Sorgu Türü | Hedef | Kabul Edilebilir | Optimizasyon Gerektiren |
|------------|--------|------------|----------------------|
| Otomatik Tamamlama | <200ms | 200-300ms | >300ms sürekli |
| Tam Arama | <500ms | 500-800ms | >800ms sürekli |
| Yönetici Araması | <1000ms | 1000-1500ms | >1500ms sürekli |

Ortalama yanıt süreleriniz "Optimizasyon Gerektiren" eşiği aşıyorsa, aşağıdaki stratejileri uygulayın.

## Performansı İzleme

**Analitik Dashboard Ortalama Yanıt Süresi**

**Arama > Arama Analitiği**'ne giderek tüm aramaların ortalama yanıt süresini görüntüleyin. Bu, ana performans izleme metriğinizdir.

**İnceleme Zamanı**: Otomatik tamamlama için ortalama yanıt süresi >300ms veya tam arama için >800ms, birden fazla günde sürekli.

**Haftalık İzleme**: Her Pazartesi analitikleri gözden geçirerek performans düşüşünü erken fark edin.

## Bilinen Performans Tıkanıklıkları

Spwig'in veritabanı doğasına özgü arama sisteminin birkaç belgelenmiş tıkanıklığı vardır ve bunlardan kaçınmak gerekir:

### CTR Hesaplama N+1 Sorguları

**Ne Olduğunu**: AnalitikServis'teki tıklama oranı hesaplaması, her toplu sonuç öğesi için ayrı sorgular çalıştırır.

**Etkisi**: Yüksek trafiğe sahip mağazalarda ve birçok izlenen sorguya sahip olanlarda ciddi.

**Kod Konumu**: `search/services/analytics_service.py` - `get_click_through_rate()` yöntemi

**Düzelme**: Üretimde CTR hesaplamalarını çağırma. Bu, genellikle yönetici analitikleri bir özelliğidir ve müşteri odaklı istekler sırasında değil, asenkron olarak hesaplanmalıdır.

### Stok Toplamlama

**Ne Olduğunu**: `with_stock_totals()` her ürün için tüm depolardaki on_hand miktarlarını hesaplar.

**Etkisi**: 1.000'den fazla ürün olan kataloglarda pahalı. `in_stock` filtresi kullanıldığında veya stok durumu otomatik tamamlamada gösterildiğinde çağrılır.

**Triger**: **Arama Ayarları > Otomatik Tamamlama** - "Stok Durumu Göster" seçeneği

**Öneri**: Büyük kataloglarda asla stok durumunu otomatik tamamlamada etkinleştirin. Her istek başına 200-500ms ekler.

### Variant Birleşimleri

**Ne Olduğunu**: SKU aramaları, variantlar tablosunda JOIN çalıştırarak variant SKU'larını aramak için tetiklenir.

**Etkisi**: 10'dan fazla variant olan ürünlerde 2-3 kat daha yavaş.

**Düzelme**: `.distinct()` kullanarak yinelenenleri önlemek, ek yük oluşturur. SKU işlevselliği için gerekli - SKU'lar kullanılmıyorsa devre dışı bırakmayın.

### Otomatik Tamamlamada Ürün Sayıları

**Ne Olduğunu**: Kategori/Marka otomatik tamamlama sonuçları ürün sayılarını gösterir ("Elektronik (234)")

**Etkisi**: Her içerik türü için sayılara izin verildiğinde 2 ekstra sorgu eklenir. Sorgular birleşimler ve toplamlar içerir.

**Triger**: **Arama Ayarları > Otomatik Tamamlama** - "Kategoriler/Markalar için Ürün Sayısını Göster"

**Öneri**: Ürün sayılarını devre dışı bırakın. Her otomatik tamamlama isteğinde 2-4 sorgu tasarrufu sağlar. Otomatik tamamlama için en büyük optimizasyon.

### Belge Dizinleme

**Ne Olduğunu**: Arama sorguları sırasında PDF/DOCX/XLSX dosyalarından metin çıkarma.

**Etkisi**: Çok pahalı (dosya I/O + metin çıkarma). Senkron bloke işlemleri.

**Triger**: **Arama Ayarları > Derin Dizinleme** - "Belgeleri Dizinle"

**Öneri**: Performans maliyeti neredeyse asla değerli değildir. Sadece küçük dijital ürün katalogları (<500 ürün) için, kapsamlı testlerden sonra etkinleştirin.

## Önbellek Yapılandırması

Önbellekleme, en etkili performans optimizasyonudur.

**Otomatik Tamamlama Önbelleği** - Varsayılan: 60s
- **Önerilen Aralık**: 45-90s
- **Daha Yüksek TTL (90-120s)**: Stok değişiklikleri nadir olduğunda daha iyi performans
- **Daha Düşük TTL (30-45s)**: Saatlik ürün ekleme durumunda daha güncel sonuçlar

**Sonuçlar Önbelleği** - Varsayılan: 300s (5 dakika)
- **Önerilen Aralık**: 180-600s
- **Daha Yüksek TTL (600s/10dk)**: Statik kataloglar için önemli performans iyileştirmesi
- **Daha Düşük TTL (180s)**: Ürün verileri sık sık güncelleniyorsa daha güncel sonuçlar

**Optimizasyon Stratejisi**: Aramalar yavaşsa, özelliklerin devre dışı bırakılmasından önce önbellek TTL'sini iki katına çıkarın. Otomatik tamamlama önbelleği 60s → 120s olurken veritabanı yükü yarıya iner.

## Otomatik Tamamlama Optimizasyonu Kontrol Listesi

Arama performansını maksimize etmek için bu değişiklikleri otomatik tamamlama ayarlarına uygulayın:

**1. Debounce'ı 300-400ms'ye Artırın**
- Konum: **Arama Ayarları > Otomatik Tamamlama** - "Debounce Gecikmesi"
- Etkisi: Tuşlara basma arasında daha uzun bekleme süresi ile API çağrılarını azaltır
- Çelişki: Daha az duyarlı (çoğu kullanıcı için fark yaratmayacak)

**2. Max Results'ı 8'den 5-6'ya Azaltın**
- Konum: **Arama Ayarları > Otomatik Tamamlama** - "Tip Başına Maksimum Sonuçlar"
- Etkisi: Daha küçük sonuç kümeleri = daha hızlı sorgular ve daha küçük JSON yükleri
- Çelişki: Daha az seçenek gösterilir (genellikle yeterli)

**3. Ürün Sayılarını Devre Dışı Bırakın (EN BÜYÜK KAZANÇ)**
- Konum: **Arama Ayarları > Otomatik Tamamlama** - "Kategoriler/Markalar için Ürün Sayısını Göster"i seçmeyin
- Etkisi: Her otomatik tamamlama isteğinde 2-4 sorgu tasarrufu sağlar
- Çelişki: Dropdown'da ürün sayıları yok (nadir ihtiyaç duyulur)

**4. Stok Durumunu Devre Dışı Bırakın**
- Konum: **Arama Ayarları > Otomatik Tamamlama** - "Stok Durumu Göster"i seçmeyin
- Etkisi: Pahalı stok toplamalarını kaldırır
- Çelişki: Stok etiketleri yok (otomatik tamamlama bağlamında kritik değil)

**5. Ürün Açıklamalarını Devre Dışı Bırakın**
- Konum: **Arama Ayarları > Otomatik Tamamlama** - "Açıklama Göster"i seçmeyin
- Etkisi: Metin işleme ve yük boyutunu azaltır
- Çelişki: Önizleme metni daha az (ürün adı genellikle yeterli)

**6. Önbellek TTL'sini 90s'ye Artırın**
- Konum: **Arama Ayarları > Önbellekleme** - "Otomatik Tamamlama Önbelleği TTL"
- Etkisi: Daha fazla istek önbellekten hizmet verilir
- Çelişki: Sonuçlar 90 saniye kadar eski olabilir (çoğu mağaza için kabul edilebilir)

**Beklenen İyileştirme**: Tüm 6 optimizasyonun uygulanması genellikle otomatik tamamlama yanıt süresini %50-70 azaltır.

## Derin Dizinleme Optimizasyonu

Her derin dizinleme seçeneği ek yük ekler. Katalog boyutuna göre devre dışı bırakın:

| Katalog Boyutu | Önerilen Derin Dizinleme |
|--------------|---------------------------|
| **<1.000 ürün** | Tümü AÇIK (minimal etki) |
| **1.000-10.000** | SKUs, Özellikler, Özel Alanlar AÇIK; Değerlendirmeler KAPALI |
| **10.000-20.000** | SKUs, Özellikler AÇIK; Özel Alanlar, Değerlendirmeler KAPALI |
| **20.000-50.000** | SKUs AÇIK; Diğerleri KAPALI |
| **>50.000** | SKUs AÇIK; Elasticsearch geçişini değerlendirin |

**Belge Dizinleme**: Sadece kritik (araştırılabilir belgelerle dijital ürünler ve toplam <500 ürün) olduğunda AÇIK tutun.

## İçerik Türü Optimizasyonu

**Arama Ayarları > İçerik Türleri** içinde kullanılmayan içerik türlerini devre dışı bırakın:

- **Blog yok mu?** "Blog Yazıları" devre dışı bırakın - sorgular tasarrufu sağlar
- **Marka filtresi yok mu?** "Markalar" devre dışı bırakın - sorgular tasarrufu sağlar
- **Sadece mağaza mı?** "Kategoriler" ve "Blog Yazıları" devre dışı bırakın

Her devre dışı bırakılan içerik türü, her aramada veritabanı sorgularını kaldırır.

## Veritabanı Optimizasyonu

Spwig, gerekli olan dizinleri göçler aracılığıyla oluşturur. Onları inanın - profil olmadan ek dizinler oluşturmayın.

**PostgreSQL Bakımı** (PostgreSQL kullanıyorsanız):
- Haftalık olarak `VACUUM ANALYZE` çalıştırın, sorgu planlayıcı istatistiklerini güncelleyin
- Büyük kataloglar aylık `VACUUM FULL`'den faydalanır (downtime gerekir)

**Veritabanı Sorgu Süresini İzleyin**: Geliştirme sırasında, profilleme araçlarını kullanarak yavaş sorguları belirleyin. Çoğu sorgu optimizasyonu zaten uygulanmıştır:
- Ürünler için `.select_related('brand', 'category')`
- Küçük resimler için `.prefetch_related('images')`
- Variant aramaları için `.distinct()`

## Bulanık Eşleştirme Performansı

Levenshtein uzaklığı hesaplama maliyetlidir (O(m*n) karmaşıklığı):

**Eşik Optimizasyonu**:
- **Daha yüksek eşik (0.85 vs 0.80)**: Daha hızlı ancak daha az yazım hatası yakalar
- **Daha düşük eşik (0.75 vs 0.80)**: Daha yavaş ancak daha anlayışlı

**Maksimum Düzenler Optimizasyonu**:
- **Daha düşük maksimum düzenleme (1 vs 2)**: Daha hızlı ancak daha fazla yazım hatası kaçırır
- **Daha yüksek maksimum düzenleme (2 vs 3)**: Daha yavaş ancak daha fazla yazım hatası yakalar

**Kütüphane Performansı**: Spwig, `rapidfuzz` mevcutsa kullanır (pure Python'dan 10 kat hızlı). Kurulumdan emin olun: `pip install rapidfuzz`

## Sinonim ve Yönlendirme Performansı

**Sinonim Sorgu Genişlemesi**: Her sinonim, arama sorgusuna OR klausüllerini ekler. Her terim için maksimum 10-20 sinonim sınırlandırın.

**Regex Eşleştirme Türü**: Regex yönlendirmeleri, tam/contains/starts_with'dan daha yavaştır. Karmaşık desenlerden kaçının.

**Öneri**: Mümkün olduğunca basit eşleştirme türlerini kullanın. Diğer eşleştirme türleri işe yaramazsa regex için rezerv edin.

## Büyük Katalog Optimizasyonu (>10.000 ürün)

Büyük kataloglar için özel stratejiler:

**1. Agresif Önbellekleme**
- Otomatik Tamamlama: 90-120s TTL
- Sonuçlar: 600s (10dk) TTL
- Performans için eski verilere izin verin

**2. Minimum Derin Dizinleme**
- SKUs sadece (özellikler, özel alanlar, incelemeler devre dışı bırakın)
- Özelliklerle birlikte/olmadan performansı test edin

**3. Azaltılmış Otomatik Tamamlama Sonuçları**
- Her tür için maksimum 5 sonuç (8'den azaltıldı)
- Sorgu yükünü azaltır

**4. Otomatik Tamamlamada Stok Durumunu Devre Dışı Bırakın**
- Otomatik tamamlamada
- Arama sonuçlarında gösterilirse orada da

**5. 50K+ Ürünlerde Elasticsearch'i Düşünün**
- Veritabanı doğasına özgü arama, yaklaşık 50.000 ürün kadar uygundur
- 50.000'den fazla olduğunda, Elasticsearch önerilir:
  - Karmaşık facetli arama
  - Yüksek eşzamanlı arama yükü (>100 arama/sn)
  - Optimizasyon rağmen sürekli >500ms yanıt süreleri

## Çok Dilli Performans

JSONField JSONB dizinleme (PostgreSQL) çok dilli aramayı etkili kılar:

- **1-3 diller**: Minimum ek yük (5-10ms)
- **5+ diller**: Sorgu karmaşıklığında küçük artış (20-40ms)
- **10+ diller**: Gözle görülür ek yük (50-100ms)

Ek yük, dil sayısına lineer olarak ölçeklenir.

## Acil Performans Çözümleri

Aramalar kritik olarak yavaşsa (>2s yanıt süreleri), bu acil çözümleri sırayla uygulayın:

**Acil** (şimdi uygulayın):
1. Belge dizinlemesini devre dışı bırakın
2. Otomatik tamamlamada ürün sayılarını devre dışı bırakın
3. Önbellek TTL'lerini 120s otomatik tamamlama / 600s sonuçlara çıkarın

**Hızlı** (24 saat içinde uygulayın):
4. Otomatik tamamlamada stok durumunu devre dışı bırakın
5. Otomatik tamamlama maksimum sonuçlarını 5'e azaltın
6. Otomatik tamamlamada ürün açıklamalarını devre dışı bırakın

**Orta** (hafta içinde uygulayın):
7. Ürün sayısı >20K ise incelemeler dizinlemesini devre dışı bırakın
8. Kullanılmayan içerik türlerini gözden geçirin ve devre dışı bırakın
9. Debounce'ı 400ms'ye artırın

**Beklenen İyileştirme**: Bu 9 düzeltme, büyük kataloglarda genellikle yanıt sürelerini %60-80 azaltır.

## İpuçları

- **Haftalık yanıt sürelerini izleyin** - Performans düşüşünü erken fark edin
- **Önbellek artışı ilk optimizasyon** - Önbellek TTL'sini iki katına çıkarmak en kolay kazançtır
- **Otomatik tamamlamada ürün sayıları = pahalı** - Otomatik tamamlama performansı en büyük katilidir
- **Belge dizinlemesi neredeyse asla değerli değildir** - Performans maliyeti faydayı nadiren haklılaştırır
- **Bir değişiklikte bir test yapın** - Aynı anda yapılan değişikliklerle neden-sonuç ilişkisini belirleyemeyiz
- **Gerçekçi veri hacimleriyle test edin** - Üretim boyutunda kataloglarla test edin
- **Büyük kataloglarda stok toplamaları performansı yok eder** - Otomatik tamamlamada stok durumunu göstermeyin
- **50K+ ürünlerde Elasticsearch'i düşünün** - Veritabanı doğasına özgü arama sınırlamaları vardır

