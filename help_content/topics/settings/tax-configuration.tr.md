---
title: Vergi Yapılandırması
---

Vergi oranları, müşteri konumu ve ürün türüne göre ödeme sırasında uygulanan satış vergisi, KDV ve diğer tüketim vergilerini tanımlar—ülke/ştat/şehir düzeyindeki oranları, ürün kategorisi özel indirimleri ile birlikte yapılandırın. Spwig, bileşik vergi (vergi üzerinde vergi), öncelik tabanlı oran seçimi ve bölgesel vergi sistemlerinin hızlı kurulumu için vergi önceden tanımlanmış gruplarını destekler (AB KDV, ABD Satış Vergisi). Oranlar, belirli ürün türlerini (gıda, kitaplar, dijital mallar) veya kategorileri yerel vergi yasalarına uygun şekilde özel indirim yapabilir.

Vergi yapılandırmasını, satış yurtdışında yerel vergi toplama gereksinimlerinizle uyumlu olmak için kullanın.

## Vergi Oranı Yapılandırması

Her vergi oranı tanımlar:

**Coğrafi Kapsam**:
- Ülke (zorunludur)
- Ştat/İl (isteğe bağlı)
- Şehir (isteğe bağlı)
- Posta Kodu Deseni (isteğe bağlı, regex)

**Oran Detayları**:
- **Vergi Oranı**: Yüzde (örneğin, 8.5%)
- **Ad**: Gösterim adı (örneğin, "California Satış Vergisi")
- **Öncelik**: Birden fazla oran eşleştiğinde daha yüksek öncelik kazanır
- **Aktif**: Silmeden etkinleştirme

**İstisnalar**:
- **İstisna Ürün Türleri**: Dijital mallar, fiziksel mallar, hizmetler
- **İstisna Kategorileri**: Belirli ürün kategorileri (Gıda, Kitaplar, Tıbbi)

**Bileşik Vergi**:
- **Bileşik mi?**: Önceki vergiler üzerine bu oranı uygula (vergi üzerinde vergi)
- Örnek: Quebec PST, GST üzerine uygulanır

---

## Ortak Vergi Senaryoları

### ABD Satış Vergisi (Ştat Düzeyinde)

```
Ad: California Satış Vergisi
Ülke: ABD
Ştat: CA
Oran: 7.25%
Öncelik: 50
```

### AB KDV (Ülke Düzeyinde)

```
Ad: İngiltere KDV
Ülke: GB
Oran: 20%
Öncelik: 50

Ad: Almanya KDV
Ülke: DE
Oran: 19%
Öncelik: 50
```

### Kanada GST/PST (Bileşik)

```
Oran 1: Ulusal GST
Ülke: CA
Oran: 5%
Öncelik: 100
Bileşik mi?: Hayır

Oran 2: Quebec PST
Ülke: CA
Ştat: QC
Oran: 9.975%
Öncelik: 50
Bileşik mi?: Evet  (alt toplam + GST üzerine uygulanır)
```

### Şehir Düzeyinde Vergi

```
Ad: Seattle Satış Vergisi
Ülke: ABD
Ştat: WA
Şehir: Seattle
Oran: 10.1%
Öncelik: 100
```

---

## Vergi İstisnaları

### Ürün Türü İstisnaları

Belirli ürün türlerini istisna durumuna alabilirsiniz:

- **Dijital Mallar**: Yazılım, e-kitaplar, müzik
- **Fiziksel Mallar**: Dokunulabilir ürünler
- **Hizmetler**: Danışmanlık, kurulum

Örnek: AB KDV, tüketicilere yönelik dijital mallara uygulanmaz (bazı durumlarda)

### Kategori İstisnaları

Belirli ürün kategorilerini istisna durumuna alabilirsiniz:

- Gıda & Gıda Ürünleri (sıklıkla istisna veya indirimli oran)
- Kitaplar & Eğitim Malzemeleri
- Tıbbi Malzemeler & İlaçlar
- Giysiler (bazı yurtdışında)

Yapılandırma:
```
Ad: California Satış Vergisi
Oran: 7.25%
İstisna Kategorileri: ["Gıda & İçecekler", "Reçeteli İlaç"]
```

---

## Vergi Önceden Tanımlanmış Grupları

Ortak vergi yapılandırmalarını hızlı yükleme:

**ABD Satış Vergisi Önceden Tanımlanmış Grubu**:
- Tüm 50 ştat + DC
- Ştat düzeyindeki oranlar
- Oranlar değiştiğinde otomatik olarak güncellenir

**AB KDV Önceden Tanımlanmış Grubu**:
- Tüm 27 AB üyesi ülke
- Standart KDV oranları
- B2B için ters hesap mantığı

**Önceden Tanımlanmışları Kullanmak İçin**:
1. Ayarlar > Sepet > Vergi Önceden Tanımlanmışları
2. Önceden tanımlanmış grup seçin (örneğin, "ABD Satış Vergisi 2026")
3. "Önceden Tanımlanmışı Yükle"yi tıklayın
4. Oranlar otomatik olarak içe aktarılır
5. Gerekirse özelleştirin

---

## Öncelik Çözümlemesi

Birden fazla oran eşleştiğinde en yüksek öncelik kazanır:

Örnek:
```
Seattle, WA'daki müşteri:

Oran A: ABD Ulusal (Öncelik 1) - 0%
Oran B: Washington Ştatı (Öncelik 50) - 6.5%
Oran C: Seattle Şehri (Öncelik 100) - 3.6%

Sonuç: Seattle oranı (toplam 10.1%) uygulanır
```

---

## Vergi Gösterim Seçenekleri

Ayarlar > Sepet > Vergi Ayarlarında yapılandırın:

- **Fiyatlara Vergi Dahil**: Vergi dahil fiyatlarla göster (AB stili)
- **Vergiyi Ayrı olarak Göster**: Vergiyi satır öğesi olarak göster (ABD stili)
- **Vergiyi Yuvarla**: Ürün başına veya sipariş başına
- **Vergi Başlığı**: Etiketi özelleştirin ("KDV", "Satış Vergisi", "GST")

---

## Vergi Yapılandırması Testi

Yaşamaya hazır olmadan önce:

1. Farklı yurtdışında test siparişler oluşturun
2. Doğru vergi oranının uygulandığını doğrulayın
3. Hariç tutulan kategoriler için istisnaların işlediğini kontrol edin
4. Bileşik vergi hesaplamasını test edin
5. Faturalardaki vergi satır öğelerini gözden geçirin

---

## Uyum Notları

- **ABD**: Nexus kuralları, fiziksel varlık veya ekonomik nexus olan ştatlarda vergi toplamak zorunluluğu getirir
- **AB**: KDV kayıtlı işletmeler, AB müşterilerinden KDV toplamak zorundadır
- **Kanada**: GST/HST/PST, eyaletlere göre değişir
- **Müsteşar vergi uzmanı ile görüşün**: Vergi yasaları sık sık değişir, mevcut gereklilikleri doğrulayın

---

## İpuçları

- **Önceden tanımlanmış vergileri kullanın** - Manuel girdi yerine daha hızlı, otomatik olarak güncellenir
- **Nexus eşiklerini izleyin** - ABD ekonomik nexus için eyalet bazında satışları izleyin
- **Önceliği doğru şekilde ayarlayın** - Şehir > Ştat > Ülke
- **Bileşik vergiyi test edin** - Hesaplamaların beklenen miktarlarla eşleştiğini doğrulayın
- **Yıllık olarak güncelleyin** - Vergi oranları değişebilir, her Ocakta gözden geçirin
- **İstisnaları belgeleyin** - Kategorilerin neden istisna durumunda olduğunu kaydedin
- **Açıklayıcı isimler kullanın** - "California Satış Vergisi 2026" "Vergi 1"'den daha iyidir
- **Vergiyi varsayılan olarak etkinleştirin** - Vergi uygulamayı unutmaktan daha güvenli