---
title: Çeviri İşleri
---

Çeviri İşleri, büyük miktarda içerik için toplu çeviri işlemini otomatikleştirir. Ürünleri tek tek manuel olarak çevirmek yerine, tüm kataloğunuza veya belirli alt kümelerinizi arka planda çeviren bir iş oluşturun. İşler asenkron olarak çalışır, bu yüzden yüzlerce veya binlerce alanın otomatik olarak çevrilmesi sırasında çalışmaya devam edebilirsiniz.

Yeni diller etkinleştirildiğinde, yeni ürünler içeri aktarıldığında veya çevrilmiş olmayan içerikte takipte kalmak gerektiğinde çeviri işlerini kullanın.

## Çeviri İşleri Nedir?

Çeviri işi, aşağıdaki işlemleri yapan bir arka plan görevidir:

1. **İçerik tarama** (ürünler, sayfalar, blog gönderileri vb.) çevrilebilir alanları için
2. **Çevrilmemiş veya güncel olmayan alanları tanımlama**, iş kapsamına göre
3. **Alanları çeviri motoruna gönderme** (yerel AI modeli veya harici sağlayıcı)
4. **Çevirileri içerikte kaydetme**
5. **Tamamlanma raporu** ile çevrilen alanlar hakkında istatistikler

İşler Celery görev kuyruğu üzerinden çalışır, bu yüzden yönetici arayüzünüzü engellemez.

## Çeviri İşlerini Ne Zaman Kullanmalısınız

**Yeni Bir Dil Başlatma**:
- Almanca yeni bir dil olarak etkinleştirin
- İş oluşturun: Tüm ürünleri İngilizceden Almanca'ya çevirin
- Sonuç: Katalogunun tamamı dakikalar/saatler içinde Almanca olarak kullanılabilir (boyutuna bağlı olarak)

**Yeni Ürün İçe Aktarma**:
- 500 yeni İngilizce ürün içe aktarın
- İş oluşturun: Yeni ürünleri tüm etkin dillere çevirin
- Sonuç: Yeni stok tüm pazarlarda hemen kullanılabilir

**Boşlukları Tutmak**:
- Kapsam raporu, Ürünlerin sadece %60'ı Fransızca çevrildiğini gösteriyor
- İş oluşturun: Sadece eksik Fransızca ürün alanlarını çevirin
- Sonuç: Fransızca kapsama %100'e kadar artar

**Kullanılamayan Çevirileri Güncellemek**:
- Çeviri modeli geliştirildi veya yeni bir sağlayıcı mevcut
- İş oluşturun: Tüm ürünleri İspanyolca'ya yeniden çevirin
- Sonuç: Katalogda daha yüksek kaliteli İspanyolca çeviriler

## Çeviri İşi Oluşturma

**Ayarlar > Çeviri İşleri**'ne gidin ve **+ İş Oluştur**'a tıklayın.

### İş Yapılandırması

**İş Adı** - Açıklamalı etiket (örneğin, "Ürünleri Almanca'ya çevir", "Yeni blog gönderileri - tüm diller")

**İçerik Türü** - Ne çevireceksiniz:
- Ürünler
- Ürün kategorileri
- Sayfalar
- Blog gönderileri
- SEO meta verileri
- E-posta şablonları
- Tüm içerik türleri

**Kaynak Dili** - Çevirmek istediğiniz dil (genellikle varsayılan dili)

**Hedef Dil(ler)** - Çevireceğiniz bir veya daha fazla dil (çoklu seçim için paralel çeviri)

**Kapsam** - İçerik hangi alt kümedir:
- **Tüm öğeler** - Mevcut çevirileri göz ardı ederek her şeyi çevirin
- **Sadece Çevrilmemiş** - Zaten çevirileri olan alanları atla
- **Tarihinden Sonra Oluşturuldu/Değiştirildi** - Sadece yeni veya yakın zamanda değiştirilen içerik
- **Belirli öğeler** - Bireysel ürünleri/sayfaları seçin (ileri filtreleme)

**Çeviri Motoru** - Hangi hizmeti kullanacağınız:
- Yerel AI modeli (varsayılan, API maliyeti yok)
- Belirli bir harici sağlayıcı (DeepL, Google, Azure, AWS)
- Otomatik seç (konfigüre edilen tercih kullanır)

**Çevirileri Kilitle** - Çevrilen alanların gelecekteki otomatik yazma işlemleri tarafından değiştirilmesini engelleyip engellemediğini belirtir (kontrol edilmiş çeviriler için faydalıdır)

### Gelişmiş Seçenekler

**Kilitli Alanları Atla** - Etkinleştirilirse, mevcut kilitli çevirileri saygılı olur (önerilir)

**Mevcutları Üzerine Yaz** - Çeviriler zaten varsa yeniden çevir (kalite iyileştirmeleri için kullan)

**Alan Filtreleri** - Sadece belirli alanları çevirin (örneğin, ürün isimleri ve açıklamaları, öznitelikleri atla)

**Toplu Boyutu** - Aynı anda işlenecek öğe sayısı (varsayılan: 50, sunucu bunu işlemek için daha hızlı işlemek istiyorsanız artırın)

**Öncelik** - Yüksek öncelikli işler, normal öncelikli işlerden önce çalışır (dikkatli kullanın)

## İş Yaşam Döngüsü ve Durumu

İşler şu durumlar aracılığıyla ilerler:

**Kuyruğa Alma** - İş oluşturuldu, çalışanın onu almasını bekliyor

**İşlem** - Çalışan aktif olarak içerikleri çeviriyor

**Tamamlandı** - Tüm çeviriler başarıyla tamamlandı

**Hata** - İş hatalarla karşılaştı (hata günlüğünü kontrol edin)

**İptal Edildi** - Yöneticiler tarafından manuel olarak durduruldu

**Duraklatıldı** - Geçici olarak duraklatıldı (yeniden başlatılabilir)

## İş İlerlemesini İzleme

İş detay sayfası şu bilgileri gösterir:

**İlerleme Çubuğu** - Tamamlanma yüzdesi

**İstatistikler**:
- Çevrilecek toplam öğeler
- Tamamlanan öğeler
- Kalan öğeler
- Kalan tahmini süre

**Gerçek Zamanlı Günlük** - Çeviri etkinliklerinin akışı (hata ayıklama için faydalıdır)

**Hata Sayısı** - Kaç alan çevrilemedi (nedenleriyle)

## İş Sonuçları ve İstatistikleri

Bir iş tamamlandığında, sonuç sayfası şu bilgileri gösterir:

**Özet**:
- Toplam işlenen alanlar
- Başarıyla çevrilenler
- Başarısız çevirimler
- Atlandı (zaten çevrildi, kilitlendi veya filtreler tarafından dışlandı)

**Öğe Başına Ayrıntılar**:
- Hangi ürünler/sayfalar çevrildi
- Öğe başına kaç alan
- Karşılıklı hatalar

**Performans Metrikleri**:
- Toplam geçen süre
- Saniyede ortalama çeviriler
- Kullanılan çeviri motoru

## Hatalı Çevirileri İşleme

Bazı çeviriler başarısız olursa:

**Hata günlüğünü inceleyin** - Hangi alanların başarısız olduğunu ve nedenini belirtir

**Yaygın hata nedenleri**:
- API hız sınırı (harici sağlayıcı)
- Çeviri motoru zaman aşımı (çok uzun metin)
- Geçersiz alan formatı (JSON ayrıştırma hatası)
- Model dil çiftini desteklemiyor

**Yeniden deneme seçenekleri**:
- Temel sorunu düzeltin
- Sadece başarısız öğeler için yeni iş oluşturun
- Farklı bir çeviri motoru kullanın

## İşleri İptal Etme ve Duraklatma

**İptal** - İş hemen durdurulur, ilerideki çeviriler atılır (başarıyla tamamlanan çeviriler kaydedilir)

**Duraklat** - İş geçici olarak durdurulur, daha sonra neredeyse kaldığı yerden devam edilebilir

**Devam** - Duraklatılmış bir işi devam ettirir

İşleri duraklatma/devam ettirme, sunucu kaynaklarını geçici olarak serbest bırakmak gerektiğinde kullanılır.

## Toplu İş Stratejileri

**Strateji 1: Dil Bazlı**:
- Her hedef dil için ayrı işler oluşturun
- Dil bazlı ilerlemeyi izlemek daha kolaydır
- Önemli dilleri önceliklendirebilirsiniz
- Yükü zaman içinde yaymak

**Strateji 2: Tümü Birlikte**:
- Tüm etkin dillere çeviren tek bir iş
- Genel tamamlanma daha hızlı
- İşlem sırasında daha yüksek sunucu yükü
- Daha basit iş yönetimi

**Strateji 3: İçerik Türü Bazlı**:
- İlk olarak ürünleri çevirin (en yüksek öncelik)
- Ardından kategoriler, sayfalar, blog gönderileri
- İlerleyen bir şekilde sunum sağlar
- Çevirileri test etme ve doğrulama daha kolaydır

Sunucu kapasitesine, aciliğe ve katalog boyutuna göre seçim yapın.

## İş Planlaması

Yeni içerikleri otomatik olarak işlemek için tekrar eden işleri planlayın:

**Günlük İşler** - Geçmiş 24 saatte oluşturulan/güncellenen ürünleri çevirin

**Haftalık İşler** - Haftalık olarak çeviri boşluklarını takip edin

**İçe Aktarma Sonrası** - Toplu ürün içe aktarımı sonrası işi otomatik olarak tetikleyin

**Dil Etkinleştirme Sonrası** - Yeni bir dil etkinleştirdiğinizde otomatik olarak iş oluşturun

Planlanmış işler, el ile müdahale olmadan çevirileri güncel tutar.

## Performans Dikkatleri

**Yerel AI Modeli**:
- ~100-500 çeviriler/saniye (sunucuya bağlı)
- İşlem sırasında CPU yoğunluğu
- API hız sınırları yok
- Ücretsiz (her çeviri başına ücret yok)

**Harici Sağlayıcılar**:
- Hız sınırları değişiklik gösterir (DeepL: Ücretsiz plan 500k karakter/ay)
- API gecikmeleri ek yük oluşturur
- Kalite daha iyi ancak ücretlidir
- Aynı anda istek sınırları

**Büyük İşler** (>10.000 alan):
- Zirve saatlerinden uzakta çalıştırın
- Sunucu kaynaklarını izleyin
- Küçük toplu işlere bölünmeyi düşünün
- İlk olarak bir alt kümeyle test edin

## İpuçları

- **Küçükten Başlayın** - Tam katalog çevirisini çalıştırmadan önce bir alt küme (örneğin, 10 ürün) üzerinde işleri test edin
- **"Sadece Çevrilmemiş" kapsamını kullanın** - Daha hızlıdır ve zaten iyi olan içeriği yeniden çevirmekten kaçının
- **İlk işi yakından izleyin** - Büyük işler başlatmadan önce hatalar veya kalite sorunlarını izleyin
- **Düşük trafiğe sahip saatlerde işleri planlayın** - Çeviri CPU/API yoğunluğunu artırır
- **İncelemeleri kilitleyin** - Toplu işlerin el ile düzenlemelerinizi geçersiz kılmasını önlemek için
- **İşleri odaklı tutun** - Küçük, hedefli işler, "her şeyi çevir" işlerinden daha kolay hata ayıklanabilir
- **Tamamlama sonrası örnekleri inceleyin** - İşin başarılı olduğuna karar vermeden önce rastgele çevirileri kalite açısından kontrol edin
- **Büyük işlerden önce dışa aktarma/yedekleme yapın** - Toplu değişiklikleri geri almak gerekebilir

