---
title: Kargo Paketleri
---

Kargo paketleri, ücret hesaplaması ve otomatik paketleme için önceden tanımlanmış kutu ve zarf boyutlarını tanımlar—iç boyutlar (kullanılabilir alan), duvar kalınlığı (taşıyıcı API'leri için dış boyutlar), ağırlık sınırları ve paketleme maliyeti belirtin. Taşıyıcılar, dış boyutları kullanarak boyut ağırlığını hesaplayarak doğru ücret teklifleri sunar. Paketler, sepet öğelerini uyumlu hale getirmek için otomatik olarak paket kombinasyonlarını seçmek için bin-packing algoritmaları için öncelik sıralamasına sahiptir.

Taşıyıcı API'leri ile gerçek zamanlı ücretler kullanıyorsanız veya boyut ağırlığı hesaplamaları için doğru sonuçlar gerekirse paketleri yapılandırın.

## Paket Yapılandırması

Her paket aşağıdaki öğeleri tanımlar:

**Boyutlar**:
- **İç Uzunluk**: İçinde kullanılabilir alan (cm)
- **İç Genişlik**: İçinde kullanılabilir alan (cm)
- **İç Yükseklik**: İçinde kullanılabilir alan (cm)
- **Duvar Kalınlığı**: Paketleme malzemesi kalınlığı (cm)

**Dış Boyutlar** (otomatik hesaplanır):
```
Dış Uzunluk = İç Uzunluk + (2 × Duvar Kalınlığı)
Dış Genişlik = İç Genişlik + (2 × Duvar Kalınlığı)
Dış Yükseklik = İç Yükseklik + (2 × Duvar Kalınlığı)
```

**Ağırlık & Maliyet**:
- **Boş Ağırlık**: Boş paket ağırlığı (gram)
- **Maksimum Ağırlık**: Maksimum yük kapasitesi (gram)
- **Maliyet**: Paketleme malzemesi maliyeti (maliyet optimizasyonu için)

**Özellikler**:
- **Ad**: Paket tanımlayıcısı (örnek: "Küçük Kutu", "Büyük Zarf")
- **Tip**: Kutu veya Zarf
- **Öncelik**: Otomatik paketleme seçimi sırası (düşük = yüksek öncelik)
- **Aktif**: Kullanılabilirlik durumu

---

## Dış Boyutların Önemi

Taşıyıcılar, boyut ağırlığını dış boyutlardan hesaplar:

**Boyut Ağırlığı Formülü**:
```
Boyut Ağırlığı = (Uzunluk × Genişlik × Yükseklik) / Bölücü

Ortak Bölücüler:
- DHL: 5000
- FedEx/UPS: 5000 (ulusal), 6000 (uluslararası)
```

**Örnek**:
```
Küçük Kutu:
İç: 20cm × 15cm × 10cm
Duvar Kalınlığı: 0.5cm
Dış: 21cm × 16cm × 11cm

Boyut Ağırlığı = (21 × 16 × 11) / 5000 = 0.74kg

Eğer gerçek ağırlık = 0.5kg → Taşıyıcı 0.74kg (boyut ağırlığı daha yüksek) olarak faturalandırır
```

**Doğruluk Neden Önemlidir**: Yanlış boyutlar → yanlış ücret teklifleri → müşteri fazladan veya az ödemeye zorlanır.

---

## Ortak Paket Boyutları

### Küçük Dolgu Zarfı

```
İç: 25cm × 18cm × 2cm
Duvar Kalınlığı: 0.3cm
Maksimum Ağırlık: 500g
Tip: Zarf
Kullanım: Belgeler, kitaplar, takılar
```

### Küçük Kutu

```
İç: 20cm × 15cm × 10cm
Duvar Kalınlığı: 0.5cm
Maksimum Ağırlık: 5kg
Tip: Kutu
Kullanım: Küçük elektronik cihazlar, kozmetikler, aksesuarlar
```

### Orta Kutu

```
İç: 30cm × 25cm × 20cm
Duvar Kalınlığı: 0.5cm
Maksimum Ağırlık: 15kg
Tip: Kutu
Kullanım: Giysiler, ayakkabılar, mutfağın eşyaları
```

### Büyük Kutu

```
İç: 45cm × 35cm × 30cm
Duvar Kalınlığı: 0.6cm
Maksimum Ağırlık: 30kg
Tip: Kutu
Kullanım: Toplu ürünler, çoklu ürünler, büyük elektronik cihazlar
```

---

## Otomatik Paketleme Algoritması

Sistem, sepet öğeleri için paketleri otomatik olarak seçer:

**Çalışma Şekli**:
1. Sepet öğelerinin toplam hacmini hesapla
2. Paketleri öncelik sırasına göre sırala (en düşük sayıdan başla)
3. Öğeleri tek bir pakete yerleştirme denemesi yap
4. Eğer uymazsa, bir sonraki paket boyutunu deneyin
5. Eğer hiçbir paket uymazsa, birden fazla paketi birleştir
6. `optimize_for` ayarına göre optimize et

**Optimizasyon Modları**:
- **Maliyet**: Paketleme maliyetini minimize et
- **Hacim**: Boşa giden alanı minimize et
- **Sayı**: Paket sayısını minimize et

**Örnek**:
```
Sepet Öğeleri:
- Öğe A: 10cm × 8cm × 5cm, 200g
- Öğe B: 15cm × 12cm × 8cm, 400g

Paketler (öncelik sırasına göre):
1. Küçük Kutu (20×15×10, öncelik=1)
2. Orta Kutu (30×25×20, öncelik=2)

Algoritma:
Küçük Kutuyu deneyin: Her iki öğe de uymakta
Sonuç: 1× Küçük Kutu (sayıya göre optimize edilmiş)
```

---

## Paket Önceliği

**Öncelik paketleme sırasını belirler**:

Öncelik 1 (en yüksek): Küçük paketler önce denenecek
Öncelik 10: Büyük paketler son çare

**Strateji**:
- Küçük paketler = düşük öncelik numaraları (1-3)
- Orta paketler = orta öncelik (4-6)
- Büyük paketler = yüksek öncelik numaraları (7-10)

**Neden**: En küçük paketle başla, gerekirse ölçeklendir → kargo maliyetini minimize eder.

---

## Duvar Kalınlığı Doğruluğu

Gerçek paketleme ölçümünü alın:

**Ölçüm Nasıl Yapılır**:
1. Boş bir kutu alın
2. İç boyutları ölçün (iç)
3. Dış boyutları ölçün (dış)
4. Hesapla: `(Dış - İç) / 2 = Duvar Kalınlığı`

**Örnek**:
```
İç Genişlik: 20cm
Dış Genişlik: 21cm
Duvar Kalınlığı: (21 - 20) / 2 = 0.5cm
```

**Ortak Kalınlıklar**:
- Dolgu zarfı: 0.2-0.4cm
- Tek duvarlı karton: 0.4-0.6cm
- Çift duvarlı karton: 0.8-1.0cm

---

## Paket Preset Oluşturma

**Adım Adım**:

1. Ayarlar > Kargo > Kargo Paketleri
2. "Kargo Paketi Ekle"yi tıklayın
3. Ad girin (örnek: "Orta Kutu")
4. Tipi seçin (Kutu veya Zarf)
5. İç boyutları girin (L × W × H cm cinsinden)
6. Duvar kalınlığını girin (cm)
7. Sistem dış boyutları otomatik olarak hesaplar
8. Boş ağırlığı girin (gram cinsinden boş paket ağırlığı)
9. Maksimum ağırlığı girin (gram cinsinden yük kapasitesi)
10. Opsiyonel: Maliyet girin (maliyet optimizasyonu için)
11. Önceliği ayarlayın (1-10)
12. Aktif = Evet olarak ayarlayın
13. Kaydet

---

## Paket Seçimi Testi

**El ile Test**:
1. Test sepetine ürünler ekleyin
2. Ödeme sürecine ilerleyin
3. Gerçek zamanlı kargo yöntemini seçin (paketleri kullanır)
4. Doğru ücretin döndürüldüğünü doğrulayın
5. Taşıyıcı yanıtını kontrol edin (API günlükleri seçilen paketleri gösterir)

**Otomatik Paketleme Önizleme**:
- Bazı kargo sağlayıcısı hesapları paketlerin ayrımını gösterir
- Hangi paketlerin sepet için seçildiğini görün
- Optimal paketlenmenin doğruluğunu kontrol edin

---

## İpuçları

- **Doğru şekilde ölçün** - Yanlış boyutlar → yanlış taşıyıcı ücretleri
- **Duvar kalınlığını dahil edin** - Boyut ağırlığı için kritik
- **3-4 boyut ile başlayın** - Küçük, orta ve büyük çoğu senaryoyu kapsar
- **Gerçekçi maksimum ağırlıklar ayarlayın** - Kutu kapasitesi, teorik limit değil
- **Önceliği akıllıca ayarlayın** - Küçük kutular öncelik 1, büyük kutular öncelik 10
- **Gerçek ürünlerle test edin** - Otomatik paketleme doğru boyutları seçip seçmediğini doğrulayın
- **Paketleme değişikliklerinde güncelleyin** - Yeni tedarikçi = boyutları yeniden ölçün
- **Özel ürünler için düşünün** - Kırılgan ürünler özel kutu boyutları gerektirebilir
- **Aktif paketleri az tutun** - Çok fazla seçenek otomatik paketleme algoritmasını yavaşlatır
- **Paketleme hakkında belge oluşturun** - Hangi ürünlerin hangi paketlere uyduğunu not alın

