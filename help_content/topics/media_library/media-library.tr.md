---
title: Medya Kütüphanesi
---

Medya Kütüphanesi, mağazanızda kullanılan tüm resimler, videolar, 3D modelleri ve dosyaların yönetilmesi için merkezi bir hub'dur. Dosyaları sürükleyip bırakarak yükleyin, klasörler ve etiketlerle organize edin ve sistem, hızlı yükleme için resimleri otomatik olarak optimize eder.

![Medya Galerisi](/static/core/admin/img/help/media-library/media-gallery.webp)

## Galeri Arayüzü

**Medya Kütüphanesi** sekmesine yan panelde tıklayarak galeriyi açın. Arayüz üç bölümden oluşur:

| Bölüm | Konum | Amaç |
|------|----------|---------|
| **Yükleme Alanı** | Sol yan panelin üstü | Dosyaları sürükleyip bırakarak yükleme (en fazla 100MB'a kadar resimler, videolar, 3D modeller) |
| **Klasörler & Etiketler** | Sol yan panelin altı | Klasörleri inceleyin, etiketlere göre filtreleyin, Geri Dönüşüm Kutusuna erişin |
| **Medya Ağı** | Ana alan | Tüm varlıklarınızı arayın, filtreleyin, inceleyin ve yönetin |

### Araç Çubuğu Kontrolleri

Medya ağı üzerindeki araç çubuğu şunları sağlar:

- **Arama** — başlık, alternatif metin, açıklama veya etiket adı ile varlıkları bulun
- **Tip Filtresi** — yalnızca Resimler, Videolar veya 3D Modelleri göster
- **Boyut Filtresi** — dosya boyutuna göre filtrele (Küçük, Orta, Büyük)
- **Toplu İşlemler** — Öğeleri Seç, Ayrıntıları Düzenle, Seçilenleri Sil
- **Görünüm Modları** — Ağı (büyük), Küçük Ağı veya Liste görünümü (oturumlar arasında kalıcı)

## Dosya Yükleme

Sol yan paneldeki **Yükle** alanına bir veya daha fazla dosyayı sürükleyin veya alanı tıklayarak dosya seçiciyi açın.

### Desteklenen Formatlar

| Tip | Formatlar |
|------|---------|
| **Resimler** | JPEG, PNG, GIF, WebP, SVG, BMP, TIFF |
| **Videolar** | MP4, WebM, MOV, MKV, AVI |
| **3D Modeller** | GLB, glTF |

### Yükleme Kuyruğu

Birden fazla dosya yükleme sırasında, yükleme kuyruğu yöneticisi görünür ve şunları gösterir:

- Her dosyanın adı ve yükleme ilerleme çubuğu
- Aynı anda yüklenebilecek eşzamanlı yüklemeler (performans için en fazla 2)
- Dosyaların yükleme sonrası optimize edilmesi durumu
- Bireysel yüklemeleri iptal etme veya tamamlanmış öğeleri temizleme seçeneği

Kuyruk sürükleyilebilir ve minimize edilebilir, böylece yüklemeler tamamlanırken çalışmaya devam edebilirsiniz.

## Otomatik Resim Optimizasyonu

Yüklediğiniz her resim otomatik olarak optimize edilir:

- **WebP dönüştürme** — orijinal dosyanın yanı sıra WebP sürümü oluşturulur (kalite %85) daha hızlı yükleme için
- **Önizleme Oluşturma** — resim ön ayarlarınıza göre birden fazla boyutta sürüm oluşturulur
- **EXIF yönlendirme** — resimler otomatik olarak doğru yönlendirme ile döndürülür

### Sistem Resim Ön Ayarları

Platform, yaygın kullanım durumlarını kapsayan 21 yerleşik ön ayar içerir:

| Ön Ayar | Boyutlar | Kesme | Kullanım Alanı |
|--------|-----------|------|---------|
| **Önizleme** | 150 x 150 | Kaplamak | Yönetici listeleri, hızlı önizleme |
| **Küçük** | 300 x 300 | Kaplamak | Küçük ürün kartları |
| **Orta** | 600 x 600 | İçermek | Ürün kartları, blog önizleme resimleri |
| **Büyük** | 1200 x 1200 | İçermek | Ürün detay sayfaları |
| **Galeri** | 800 x 800 | İçermek | Resim galerileri |
| **Anasayfa** | 1920 x 1080 | Kaplamak | Anasayfa bölümleri, sayfa bayrakları |
| **Bayrak** | 1200 x 400 | Kaplamak | Tanıtım bayrakları |
| **Kart** | 400 x 300 | Kaplamak | Özellik kartları, içerik kartları |
| **Profil Resmi** | 200 x 200 | Kesmek | Müşteri ve personel profil resimleri |
| **Ürün Listesi** | 400 x 400 | Kaplamak | Ürün ağı kartları |
| **Ürün Detayları** | 1200 x 1200 | Kaplamak | Tam ürün resimleri |
| **Ürün Önizlemesi** | 100 x 100 | Kaplamak | Variant seçicileri, mini sepetler |
| **Kategori Bayrağı** | 1920 x 480 | Kaplamak | Kategori sayfa başlıkları |
| **Kategori Önizlemesi** | 300 x 200 | Kaplamak | Kategori kartları |
| **Logo Başlığı** | 300 x 80 | Doldurmak | Site başlık logosu |
| **Logo Altyapısı** | 200 x 60 | Doldurmak | Site altyapı logosu |
| **E-posta Logosu** | 400 x 100 | Doldurmak | E-posta şablonu logosu |
| **Kare Logo** | 160 x 160 | Doldurmak | Kare logo yerleştirmeleri |
| **Marka Logosu** | 200 x 100 | Doldurmak | Marka/ortaklık logosu |
| **Duyuru Bayrağı** | 800 x 300 | Kaplamak | Duyuru resimleri |
| **Duyuru Arka Planı** | 1200 x 800 | Kaplamak | Duyuru arka planları |

Sistem ön ayarları yeniden adlandırılamaz veya silinemez. Varsayılanlar tarafından kapsanmayan boyutlara ihtiyacınız varsa, **Medya Kütüphanesi > Resim Boyutu Ön Ayarları** altında ek özel ön ayarlar oluşturabilirsiniz.

### Kesme Modları

| Mod | Davranış |
|------|----------|
| **Kaplamak** | Alanı tamamen doldurur, gerekirse kenarları keser — kartlar ve bayraklar için iyi |
| **İçermek** | Tam resmi alanı içine sığdırır, gerekirse şeffaflık alanı ekler — ürün resimleri için iyi |
| **Kesmek** | Merkezi keserek tam boyutlara uygun hale getirir |
| **Doldurmak** | Resmi sığdırır ve (şeffaf, beyaz veya siyah) kenar boşlukları ekler — logoslar için iyi |

## Dosyaları Düzenleme

### Klasörler

Klasörler oluşturarak medya dosyalarınızı mantıksal gruplara ayırın. Klasörler herhangi bir derinliğe kadar iç içe olabilir. Sol yan panelde bir klasöre tıklayarak sadece bu klasördeki varlıkları gösterebilirsiniz. **Tüm Dosyalar** bağlantısı her şeyi gösterir.

### Etiketler

Varlıklara etiketler ekleyerek kros klasör düzenlemesi için esnek bir yol sağlar. Etiketler sol yan panelde bir bulut olarak görünür. Bir etikete tıklayarak bu etikete göre varlıkları filtreleyebilirsiniz. Varlıklar birden fazla etiket içerebilir.

### Arama

Arama çubuğu başlık, alternatif metin, açıklama veya etiket adı ile varlıkları bulur. Arama, tip ve boyut filtreleriyle birlikte kullanılarak daha kesin sonuçlar elde edilebilir.

## Varlık Ayrıntıları

Bir varlığa tıklayarak, büyük bir önizleme ile birlikte tam meta verileri içeren ayrıntı görünümünü açabilirsiniz.

![Varlık Ayrıntıları](/static/core/admin/img/help/media-library/media-detail.webp)

Ayrıntı görünümü şunları gösterir:

- **Önizleme** — orijinal boyutlarla büyük resim önizlemesi
- **Dosya Bilgisi** — tip, boyutlar, dosya boyutu, yükleme tarihi
- **Düzenleme için Sekmeler**:

| Sekme | Alanlar |
|-----|--------|
| **Genel** | Başlık, Alternatif Metin, Açıklama (tümü çok dilli mağazalar için çevrilebilir) |
| **Teknik** | MIME türü, dosya hash'i, orijinal dosya adı, WebP sürüm durumu |
| **Düzenleme** | Klasör ataması, etiketler, genel/özel anahtar |
| **Gelişmiş** | Fokus noktası koordinatları, harici ID, meta veri JSON |

### Çevrilebilir Alanlar

Başlık, alternatif metin ve açıklama çevrilebilir. Her alanın yanındaki çeviri simgesine tıklayarak etkinleştirilmiş dilleriniz için çeviriler ekleyebilirsiniz. Bu, SEO ve erişilebilirlik için resimlerin doğru yerelleştirilmiş alternatif metin ve açıklamaları olduğundan emin olur.

### Kullanım Takibi

Sistem, her varlığın platformda nerede kullanıldığını izler. Altta bulunan **Medya Kullanımları** bölümü, bu varlığa atıfta bulunan tüm modelleri ve alanları gösterir, bu da değişiklikler yapmadan veya silmeden önce etkisini anlamaya yardımcı olur.

## Video Desteği

Medya kütüphanesine yüklenen videolar otomatik olarak analiz edilir:

- **Meta veri çıkarma** — uzunluk, çözünürlük, kare hızı, bit hızı ve kodlar yakalanır
- **Poster resmi** — video için bir önizleme resmi oluşturulur
- **Akış** — videolar, dosyanın tamamını indirmeden arama yapmak için aralıklı istekleri destekler
- **İsteğe Bağlı Dönüştürme** — videolar, daha hızlı teslimat için optimize edilmiş WebM/AV1 formatına dönüştürülebilir

## Geri Dönüşüm Kutusu

Bir varlık silindiğinde, kalıcı olarak kaldırılmaz, bunun yerine **Geri Dönüşüm Kutusuna** taşınır. Bu, yanlış silme işlemlerinden korur.

| Eylem | Ne Yapar |
|--------|-------------|
| **Sil** | Varlığı Geri Dönüşüm Kutusuna taşır (zayıf silme) |
| **Geri Yükle** | Silinen varlığı orijinal konumuna geri döndürür |
| **Kalıcı Sil** | Varlığı ve tüm küçük resimlerini kalıcı olarak depodan kaldırır |
| **Geri Dönüşüm Kutusunu Boşalt** | Geri Dönüşüm Kutusundaki tüm öğeleri kalıcı olarak siler |

Yan paneldeki **Geri Dönüşüm Kutusu**'na tıklayarak silinen varlıkları görüntüleyebilir ve yönetebilirsiniz.

## Medya Kütüphanesi Kullanım Alanları

Medya kütüphanesi, tüm platformda entegre edilmiştir:

| Özellik | Medya Nasıl Kullanılır |
|---------|------------------|
| **Ürün Kataloğu** | Ürün resimleri, variant resimleri, kategori bayrakları |
| **Blog** | Öne çıkan resimler, CKEditor ile içerik içinde resimler |
| **Sayfa Oluşturucu** | Resim öğeleri, anasayfa arka planları, galeri bileşenleri |
| **Başlık/Araç Çubuğu Oluşturucu** | Logo resimleri, arka plan resimleri |
| **Site Ayarları** | Site logosu ve favicon |
| **Duyurular** | Duyuru resimleri ve arka planları |
| **CKEditor** | Tüm zengin metin resim yükleme işlemleri medya kütüphanesi üzerinden yönlendirilir |
| **Loyalty Programı** | Ödül ve seviye resimleri |

Bu özelliklerden herhangi birinde bir resim seçtiğinizde, medya kütüphanesi galerisi, kolayca taranması ve seçimi için bir modal olarak açılır.

## İpuçları

- **Açıklayıcı başlıklar ve alternatif metinler kullanın** — iyi meta veriler SEO ve erişilebilirlik için iyidir. Sistem, mağaza ön tarafında tüm resim etiketlerinde alternatif metni kullanır.
- **Dosyaları yüklemeye başlamadan önce klasörlerle organize edin** — çok sayıda dosya yüklemeye başlamadan önce (örneğin, Ürünler, Blog, Bayraklar, Logolar) bir klasör yapısı oluşturun. Daha sonra organize etmek, daha sonra yeniden organize etmekten çok daha kolaydır.
- **Kesme kategorileri için etiketleri kullanın** — "mevsimsel", "indirim", "hayat tarzı" gibi etiketler, birden fazla klasörde yer alan varlıkları bulmanıza yardımcı olur.
- **Silmeden önce kullanım durumlarını kontrol edin** — kullanım izleme bölümü, bir varlığın nerede referans verildiğini gösterir. Kullanılan bir varlığı silmek, mağaza ön tarafında kırık resimler bırakabilir.
- **WebP'yi işinizi yapmaya bırakın** — otomatik WebP dönüştürmesi, JPEG'e göre dosya boyutlarını %25-35 azaltır ve görünür kalite kaybı olmadan. Yüklemeden önce resimleri manuel olarak dönüştürmenize gerek yoktur.
- **Özel ön ayarlar oluşturun** — özel bir düzenin belirli bir resim boyutuna ihtiyacı varsa, özel bir ön ayar oluşturun, resimleri manuel olarak yeniden boyutlandırmak yerine.

