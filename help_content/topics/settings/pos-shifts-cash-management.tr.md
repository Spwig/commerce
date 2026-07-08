---
title: POS Dönüşümü ve Nakit Yönetimi
---

POS dönüşümleri kasiyer iş sürelerini izler ve doğru nakit muhasebesini sağlar. Her dönüşüm, bir kasiyerin terminaldeki zamanını temsil eder—kasayı açmak ve başlangıç nakit sayımını yapmakten, dönüşümü kapatmak ve son sayım ile dengelemekten oluşan. Sistem, gerçek nakit satışlarına dayalı beklenen nakiti otomatik olarak hesaplar ve fiziksel sayım ile karşılaştırır, bu farkları inceleme için vurgular. Dönüşümler sırasında nakit hareketleri (dönüşüm eklemeleri, küçük nakit çekimleri) tam bir denetim izi oluşturmak için nedenlerle izlenir.

**POS > Dönüşümler** menüsüne giderek tüm dönüşümleri görüntüleyin, aktif dönüşümleri izleyin, nakit dengeleme raporlarını inceleyin ve geçmiş etkinlikleri denetleyin.

![Dönüşüm Listesi](/static/core/admin/img/help/pos-shifts-cash-management/shift-list.webp)

## POS Dönüşümlerini Anlamak

Bir dönüşüm, bir kasiyerin bir terminalde çalıştığı iş periyodudur. Dönüşümler nakit sorumluluğunu zorunlu kılar—her kasiyer, dönüşüm süresince kasasındaki nakit için sorumludur.

**Dönüşüm Yaşam Döngüsü**:
1. **Açma** - Kasiyer dönüşümü başlatır, kasayı açar, miktarı kaydeder
2. **Dönüşüm Sırasında** - Satışları işler, ödemeleri kabul eder, iadeler verir
3. **Kapanış** - Kasiyer nakit sayar, kapanış miktarını kaydeder, sistem farkı hesaplar
4. **Dengeleme** - Dönüşüm denetim amaçlı kilitlenir ve sonlandırılır

**İzlenen Ana Metrikler**:
- **Açma Nakiti** - Dönüşüm başlangıcında kasadaki başlangıç nakiti
- **Kapanış Nakiti** - Dönüşüm sonunda kasadaki fiziksel nakit
- **Beklenen Nakit** - Hesaplanan: Açma nakiti + nakit satışları - nakit iadeleri + nakit hareketleri
- **Nakit Farkı** - Fark: Kapanış nakiti - beklenen nakit (pozitif = fazlalık, negatif = eksiklik)
- **Toplam Satışlar** - Dönüşüm sırasında yapılan tüm satış işlemleri toplamı
- **Toplam İadeler** - Dönüşüm sırasında yapılan tüm iade işlemleri toplamı
- **İşlem Sayısı** - İşlem yapılan sipariş sayısı

## Dönüşüm Listesi Görünümü

Dönüşüm listesi, ana bilgilerle birlikte tüm dönüşümleri görüntüler:

**Dönüşüm Durumu**:
- **Açık** (yeşil etiket) - Şu anda aktif olan dönüşüm
- **Kapalı** (gri etiket) - Tamamlanmış dönüşüm
- **Dengeleme** (mavi etiket) - Denetim için kilitlenmiş ve sonlandırılmış dönüşüm

**Terminal** - Dönüşümün yapıldığı POS terminali

**Kasiyer** - Dönüşümü yapan personel

**Açma Nakiti** - Başlangıç nakit miktarı

**Kapanış Nakiti** - Bitiş nakit miktarı (dönüşüm hâlâ açık ise boş)

**Beklenen Nakit** - İşlemlere dayalı sistem tarafından hesaplanan beklenen miktar

**Nakit Farkı** - Fark (negatifse kırmızı, pozitifse yeşil, sıfır ise siyah olarak vurgulanır)

**Süre** - Dönüşüm süresi (başlangıç zamanından bitiş zamanına kadar)

**Toplam Satışlar** - Dönüşüm sırasında elde edilen gelir

Filtreleri kullanarak görüntüleyin:
- Sadece açık dönüşümler (aktif terminalleri izleme)
- Farklılıklar olan dönüşümler (nakit farkı ≠ 0)
- Tarih aralığına göre dönüşümler (günlük dengeleme raporları)
- Kasiyerlere göre dönüşümler (performans denetimi)

## Dönüşüm Açma

Kasiyerler POS terminalinden doğrudan dönüşüm açar (admin'den açılamaz). Terminaldeki iş akışı:

1. **Personel Giriş Yapar** - Terminali erişmek için kimlik bilgilerini girer

2. **Açma Nakit Sayımı** - Kasadaki tüm nakitleri fiziksel olarak sayar (banknotlar ve madenî paralar)

3. **Açma Miktarını Girer** - Sayılan miktarı POS uygulamasında kaydeder

4. **Dönüşüm Başlar** - Terminal satışları işlemek için hazırdır

**Açma Nakiti Kılavuzu**:
- Standart açma nakiti (dönüşüm) genellikle $100-$300 arasında değişir, mağaza boyutuna bağlı olarak
- Sayımı iki kez yaparak doğruluğu sağlayın—başlangıç hataları kapanış farklılıklarına yayılır
- Eğer kasada hiçbir şey yoksa, açma nakiti $0.00'dır (dönüşüm sırasında nakit hareketi ile eklenir)
- $50'den fazla banknotları ayrı ayrı belgeleyin, hareketlerini izlemek için

![Dönüşüm Ekleme Formu](/static/core/admin/img/help/pos-shifts-cash-management/shift-add-form.webp)

## Dönüşüm Sırasında

Dönüşüm açıkken, sistem otomatik olarak izler:

**Nakit Satışları** - Müşteri fiziksel nakit ödemeleri yapan her işlem (beklenen nakiti artırır)

**Nakit İadeleri** - Nakit ile verilen her iade (beklenen nakiti azaltır)

**Kart Satışları** - Kredi/borç kartı işlemleri (nakit üzerinde hiçbir etkisi yok)

**Kısmi Ödeme** - Kısmi nakit + kısmi kart (yalnızca nakit kısmı beklenen nakiti etkiler)

**Hediye Kartları & Vadesiz Çekler** - Nakit dışı ödeme yöntemleri (nakit üzerinde hiçbir etkisi yok)

Kasiyerler satışları normal şekilde işler. Sistem, beklenen nakit için arka planda sürekli bir hesaplama yapar.

## Nakit Hareketleri

Dönüşüm sırasında kasadaki ayarlamalar:

**Dönüşüm Ekleme** - Kasaya nakit eklemek:
- Neden: "Büyük banknotlar için para eklemek"
- Miktar: +$100.00
- Beklenen nakit $100.00 artar

**Küçük Nakit Çekimi** - Giderler için kasadan nakit çıkarma:
- Neden: "Ofis malzemesi satın alma"
- Miktar: -$25.00
- Beklenen nakit $25.00 azalır

**Banka Atışı** - Güvenlik için fazla nakit çıkarma:
- Neden: "Güvenlik atışı - kasada $500'dan fazla"
- Miktar: -$300.00
- Beklenen nakit $300.00 azalır

**Terminalde Nakit Hareketlerini Kaydetme**:
1. **Menüye** dokunun > **Nakit Hareketi**
2. Türü seçin: Ekleme veya Çıkarma
3. Miktarı girin
4. Nedeni girin (denetim izi için gerekli)
5. Onaylayın

Tüm nakit hareketleri, zaman damgaları, miktarlar ve nedenlerle birlikte dönüşüm detay raporunda görünür.

## Dönüşüm Kapatma

Kasiyer iş periyodunu tamamladığında dönüşümü kapatır:

1. **Kapat Dönüşüm** - Terminal menüsünde

2. **Kalan İşlemleri İşleyin** - Park edilmiş sepetleri veya bekleyen satışları tamamlayın

3. **Kapanış Nakit Sayımı** - Kasadaki tüm nakiti fiziksel olarak sayın
   - Banknotları cinsine göre sayın ($100, $50, $20, $10, $5, $1)
   - Madenî paraları türüne göre sayın (25 kuruş, 10 kuruş, 5 kuruş, 1 kuruş)
   - Toplam = kapanış nakit miktarı

4. **Kapanış Miktarını Girin** - Sayılan toplamı kaydedin

5. **Sistem Farkı Hesaplar**:
   - Beklenen nakit = Açma nakiti + nakit satışları - nakit iadeleri + nakit hareketleri
   - Nakit farkı = Kapanış nakiti - beklenen nakit
   - Örnek: Kapanış $485.00 - Beklenen $480.00 = +$5.00 fazlalık

6. **Farkı İnceleyin** - Terminal farkı görüntüler:
   - **Tam ($0.00)** - İdeal dengeleme
   - **Küçük fazlalık (+$1 ile +$5)** - Kabul edilebilir yuvarlama veya müşteri ipotek
   - **Küçük eksiklik (-$1 ile -$5)** - Küçük sayım hatası, kabul edilebilir
   - **Büyük fark (>$5)** - Tekrar sayım gerekir

7. **Gerekirse Tekrar Sayın** - Fark büyük (>$10) ise, kasiyer kapanış nakitini tekrar saymalı

8. **Dönüşümü Sonlandırın** - Kapanış miktarını onaylayın, dönüşüm durumu "Kapalı" olarak değişir

9. **Dönüşüm Raporunu Yazdırın** - Terminal kasiyer kayıtları için nakit dengeleme fişini yazdırır

![Dönüşüm Detayı](/static/core/admin/img/help/pos-shifts-cash-management/shift-detail.webp)

## Nakit Dengeleme Formülü

Sistem beklenen nakiti bu formül kullanarak hesaplar:

```
Beklenen Nakit = Açma Nakiti
                + Nakit Satışları
                - Nakit İadeleri
                + Nakit Ekleme (hareketler)
                - Nakit Çıkarma (hareketler)
```

**Örnek**:
- Açma Nakiti: $200.00
- Nakit Satışları: $450.00 (15 işlem)
- Nakit İadeleri: -$30.00 (1 iade)
- Nakit Ekleme: +$100.00 (dönüşüm sırasında eklenen dönüşüm)
- Nakit Çıkarma: -$50.00 (küçük nakit çekimi)
- **Beklenen Nakit: $200 + $450 - $30 + $100 - $50 = $670.00**

Eğer kasiyer kapanışta $675.00 sayarsa:
- Nakit Farkı: $675.00 - $670.00 = **+$5.00 fazlalık**

## Dönüşüm Raporlama ve Denetim

Dönüşüm raporları, detaylı dengeleme bilgileri sağlar:

**Özet Bölümü**:
- Açma ve kapanış nakiti
- Beklenen nakit hesaplaması
- Nakit farkı (fazlalık/eksiklik)
- Toplam satışlar ve iadeler
- İşlem sayısı
- Dönüşüm süresi

**İşlem Detayı**:
- Dönüşüm sırasında tüm satışlar (sipariş kimlikleri, miktarlar, ödeme yöntemleri)
- Tüm iadeler
- Her işlem için zaman damgası

**Nakit Hareketi Günlüğü**:
- Tüm ekleme ve çıkarma işlemleri
- Sağlanan nedenler
- Zaman damgaları

**Kullanım Durumları**:
- **Günlük dengeleme** - İş gününün sonunda tüm dönüşümleri inceleyin
- **Kasiyer performansı** - Kullanıcıya göre eksiklik desenlerini belirleyin
- **Suç tespiti** - Sürekli büyük eksiklikler hırsızlık gösterebilir
- **Eğitim ihtiyaçları** - Sık sık küçük eksiklikler sayım doğruluğu sorunlarını gösterir
- **Denetim izi** - Muhasebe ve vergi amaçlı tam kayıt

## Çoklu Terminal Nakit Yönetimi

Birden fazla terminalde çalışan mağazalar için:

**Ayrı Kasalar**: Her terminal kendi kasasına sahiptir—dönüşümler bağımsızdır. Terminal 1'deki Kasiyer A ve Terminal 2'deki Kasiyer B ayrı dönüşümlerle ve ayrı dengelemelerle çalışır.

**Paylaşılan Kasalar**: Bazı mağazalar birden fazla terminal arasında bir kasa paylaşır (önerilmez). Eğer bu şekilde yapılıyorsa:
- Paylaşılan kasa için her zaman sadece bir dönüşüm açık olabilir
- Kasiyerler bir sonraki kasiyere devrettiğinde dönüşümü kapatmalıdır
- Nakit hareketleri devirler sırasında tüm ekleme/çıkarma işlemlerini izler
- Farklar özel kasiyerlere atamak daha zordur

**En İyi Uygulama**: Her terminal için bir kasa, her oturumda bir kasiyer için bir dönüşüm. Bu, açık hesaplı ve basit dengeleme sağlar.

## Farkları Eleme

Kapanış nakiti beklenen nakite uymuyorsa:

**Küçük Farklar (<$5)**:
- Yuvarlama, sayım hataları veya müşteri ipotekleri nedeniyle kabul edilebilir
- Farkları dönüşüm notlarında belgeleyin
- Eğer desen ortaya çıkarsa başka bir eylem gerekmez

**Orta Farklar ($5-$20)**:
- Dönüşümü sonlandırmadan önce nakiti tekrar sayın
- İşlem günlüğünü inceleyin (yanlış para verilmesi, iptal edilen işlem işlenmemesi)
- Farkları dönüşüm notlarında belgeleyin
- Yönetici incelemesi önerilir

**Büyük Farklar (>$20)**:
- Zorunlu tekrar sayım
- Dönüşümü kapatmak için yönetici onayı gerekir
- Tüm işlemleri ve nakit hareketlerini inceleyin
- Potansiyel nedenleri araştırın (hırsızlık, kasa dokunuşu, yanlış açma nakiti)
- Duruma göre disiplinli eylem gerekebilir

**Sürekli Eksiklikler**:
- Aynı kasiyerden sürekli negatif farklar = eğitim sorunu veya hırsızlık
- Ekstra denetim uygulayın (işlem sırasında yönetici kontrolü)
- POS eğitimi prosedürlerini gözden geçirin
- Nakit yönetimi politikalarını güncelleyin

## İpuçları

- **Açma nakitini iki kez sayın** - Açma hataları kapanış farklarına yayılır; başlangıçta doğruluk, sonunda sorunları önler
- **Nakit hareketlerini hemen kaydedin** - Kapanışta float ekleme veya küçük nakit çekimlerini belgelemek için beklemeyin
- **Her zaman hareket nedenlerini belirtin** - "$100 eklendi" denetim için yararlı değildir; "$100 eklendi (5 dolar banknotları az)", işlem için etkin bir açıklama sağlar
- **Fark >$10 ise tekrar sayın** - Büyük fark olmadan dönüşümü sonlandırma
- **Günlük olarak dönüşüm raporlarını yazdırın** - Muhasebe için günlük dengeleme belgelerine ekleyin
- **Desenleri değil bireysel farkları inceleyin** - -$3.00 eksiklik iyi olabilir; beş ardışık -$3.00 eksiklik sorun yaratır
- **Gün sonunda dönüşümleri kapatın** - Dönüşümleri gece boyu açık bırakmayın; yeni farklar daha kolay araştırılabilir
- **Kasiyerleri banknot sayımı konusunda eğitmen** - En çok hata banknot sayımından kaynaklanır (5 doların 10 dolar olduğuna inanmak)
- **Madenî para sarmalayıcılarını kullanın** - Hazır sarmalanan madenî paralar sayım hatalarını azaltır ve dengelemeyi hızlandırır

