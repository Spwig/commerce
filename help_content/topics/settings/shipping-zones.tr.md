---
title: Kargo Bölgeleri
---

Kargo bölgeleri, hedeflenmiş kargo ücretleri için coğrafi bölgeleri tanımlar—ülkeleri, eyaletleri veya posta kodlarını bölgelere gruplandırın, ardından kargo yöntemlerini belirli bölgelere bağlayarak hassas ücret kontrolü sağlayın. Bir adres birden fazla bölgeye uysa bölgeler öncelik tabanlı eşleşir (en yüksek öncelik kazanır). Bu sistem, ileri düzey fiyatlandırma stratejilerini mümkün kılar: uzak bölgelere daha fazla ücret, ulusal kargo ücretsiz, belirli bölgeler için indirimli oranlar gibi.

Bölgeleri farklı coğrafi bölgeler için farklı kargo ücretleri gerektiğinde kullanın, basit ulusal vs. uluslararası bölümlendirme'den karmaşık çok bölgeli katmanlı fiyatlandırma'ya kadar.

## Kargo Bölgelerini Anlamak

**Bölgeler Nedir**: Ülkeye, eyalet/iller ve posta kodu desenlerine göre tanımlanmış isimli coğrafi bölgeler.

**Bölgeler Nasıl Çalışır**:
1. Müşteri checkout'ta kargo adresini girer
2. Sistem tüm aktif bölgeleri değerlendirir
3. Müşterinin adresiyle eşleşen bölgeler adaylar olarak belirlenir
4. Birden fazla bölge eşleşiyorsa en yüksek öncelikli bölge kazanır
5. Kazanan bölgeye bağlı kargo yöntemleri gösterilir
6. Herhangi bir bölgeye bağlı olmayan (veya eşleşen bölgeye bağlı olan) yöntemler gösterilir

**Bölge Bileşenleri**:
- **İsim**: Bölge tanımlayıcısı (örneğin, "Ulusal", "AB", "Uzak Bölgeler")
- **Ülkeler**: Dahil edilen ülke kodlarının listesi (boş = tüm ülkeler)
- **Eyaletler/İller**: Belirli ülkeler için eyalet kısıtlamaları (isteğe bağlı)
- **Posta Kodu Desenleri**: ZIP/posta kodu eşleşmesi için regex desenleri (isteğe bağlı)
- **Öncelik**: Daha yüksek sayı = birden fazla bölge eşleştiğinde daha yüksek öncelik

---

## Bölge Eşleştirme Mantığı

Bölgeler, adreslerle eşleşmek için **ileriye yönelik daraltma** kullanır:

### Seviye 1: Ülke Eşleşmesi

**Boş ülke listesi** → Bölge tüm ülkelere eşleşir

**Ülke listesi sağlanmış** → Adres ülkesi listede olmalıdır

Örnek:
```
Bölge: "Ulusal"
Ülkeler: ["US"]
→ Eşleşir: Herhangi bir ABD adresi
→ Eşleşmez: Kanada, İngiltere vb.
```

### Seviye 2: Eyalet/İl Eşleşmesi

**Tanımlanmamış eyaletler** → Bölge, izin verilen ülkelerdeki tüm eyaletlere eşleşir

**Belirli ülkeler için tanımlanmış eyaletler** → Adres eyaleti eşleşmelidir

Örnek:
```
Bölge: "Batı Kıyısı"
Ülkeler: ["US"]
Eyaletler: {"US": ["CA", "OR", "WA"]}
→ Eşleşir: Kaliforniya, Oregon, Washington adresleri
→ Eşleşmez: New York, Texas vb.
```

### Seviye 3: Posta Kodu Eşleşmesi

**Tanımlanmamış desenler** → Bölge, izin verilen ülke/eyaletlerdeki tüm posta kodlarına eşleşir

**Tanımlanmış desenler** → Adres posta kodu en az bir desene eşleşmelidir

Örnek:
```
Bölge: "Los Angeles Metrosu"
Ülkeler: ["US"]
Eyaletler: {"US": ["CA"]}
Posta Kodu Desenleri: ["^90[0-9]{3}$", "^91[0-9]{3}$"]
→ Eşleşir: 90001, 91210, 90245
→ Eşleşmez: 94102 (San Francisco)
```

**Regex Desen Örnekleri**:
- `^90[0-9]{3}$` - Los Angeles bölgesi (90000-90999)
- `^[A-Z][0-9][A-Z] [0-9][A-Z][0-9]$` - Kanadalı posta kodu formatı (K1A 0B1)
- `^SW[0-9]{1,2}` - Londra UK posta kodları SW ile başlayanlar

---

## Öncelik Tabanlı Bölge Seçimi

Bir adres birden fazla bölgeye eşleşiyorsa, **öncelik** hangi bölgenin uygulanacağını belirler:

**Öncelik Nasıl Çalışır**:
- Daha yüksek sayı = daha yüksek öncelik
- Adres, öncelik 100 ve 50 olan bölgelere eşleşiyorsa, öncelik 100 kazanır
- Sadece kazanan bölgenin kargo yöntemleri kullanılabilir

**Kullanım Durumları**:

**Senaryo 1: Özel Genel'i Geçersiz Kıl**
```
Bölge A: "Uzak Alaska"
  Ülkeler: ["US"]
  Eyaletler: {"US": ["AK"]}
  Öncelik: 100

Bölge B: "Ulusal ABD"
  Ülkeler: ["US"]
  Öncelik: 50

Adres: Anchorage, AK
→ Her iki bölgeye eşleşir
→ Öncelik 100 kazanır
→ "Uzak Alaska" bölgesi uygulanır (daha yüksek kargo ücreti)
```

**Senaryo 2: Posta Kodu Eyaleti Geçersiz Kıl**
```
Bölge A: "Manhattan Premium"
  Ülkeler: ["US"]
  Eyaletler: {"US": ["NY"]}
  Posta Kodu Desenleri: ["^100[0-2][0-9]$"]
  Öncelik: 100

Bölge B: "New York Eyaleti"
  Ülkeler: ["US"]
  Eyaletler: {"US": ["NY"]}
  Öncelik: 50

Adres: New York, NY 10001
→ Her iki bölgeye eşleşir
→ Öncelik 100 kazanır
→ "Manhattan Premium" uygulanır (premium kargo hizmeti)
```

---

## Kargo Bölgeleri Oluşturma

**Adım Adım İş Akışı**:

1. **Bölgelere Git**
   - Ayarlar > Kargo > Kargo Bölgeleri'ne gidin
   - "Kargo Bölgesi Ekle"ye tıklayın

2. **Temel Yapılandırma**
   - **Ad**: Açıklayıcı tanımlayıcı (örneğin, "Avrupa Birliği", "Batı Kıyısı", "Uzak Alanlar")
   - **Öncelik**: İlişkisel önem düzeyini ayarlayın (100 özel, 50 genel, 1 varsayılan)
   - **Aktif**: Etkinleştirme/Devre dışı bırakma için anahtar

3. **Coğrafi Kapsamı Tanımlayın**

   **Seçenek A: Tüm Ülkeler** (ülke listesini boş bırakın)
   - Bölge, küresel olarak her adresle eşleşir
   - Varsayılan/varsayılan bölgeler için kullanın

   **Seçenek B: Belirli Ülkeler**
   - "Ülke Ekle"ye tıklayın
   - Aşağıdaki listeden ülkeleri seçin (ABD, CA, UK, vb.)
   - Dahil edilen tüm ülkeler için tekrar edin

   **Seçenek C: Belirli Eyaletler/İlçeler**
   - Ülkeleri ekledikten sonra, her ülkeye "Eyalet Ekle"ye tıklayın
   - Eyaletleri aşağıdan seçin
   - Örnek: ABD → CA, OR, WA Batı Kıyısı için

   **Seçenek D: Posta Kodu Desenleri** (ileri düzey)
   - Her satıra regex desenleri girin
   - Örnek posta kodlarıyla desenleri test edin
   - Desenlerin sözdizimini kontrol etmek için "Desenleri Doğrula"ya tıklayın

4. **Kargo Yöntemlerine Bağla**
   - Yöntemler, yöntemi düzenlerken (zona yapılandırma dışında) bağlanabilir
   - Veya mevcut yöntemlere bölgeleri bağlayın: Yöntemi Düzenle → Kargo Bölgeleri → Bölgeleri seçin

5. **Gösterim Önceliğini Ayarla**
   - Daha yüksek öncelikli bölgeler, birden fazla eşleştiğinde daha düşük öncelikli bölgeleri geçersiz kılar
   - Önerilen: Özel bölgeler (100), Bölgesel bölgeler (50), Varsayılan bölge (1)

6. **Bölgeyi Etkinleştir**
   - "Aktif" = Evet anahtarını çevirin
   - Kaydet

---

## Ortak Bölge Kurulumları

### Kurulum 1: Yerel vs. Uluslararası

**Hedef**: Yerel ile diğer tüm ülkelere göre farklı oranlar.

```
Bölge 1: "Yerel"
  Ülkeler: [Ülke Kodunuz]
  Öncelik: 50

Bölge 2: "Uluslararası"
  Ülkeler: [Boş bırakın veya diğer tüm ülkeleri seçin]
  Öncelik: 1
```

**Kargo Yöntemleri**:
- "Yerel Standart" → Yerel bölgeye bağlanır
- "Uluslararası Kargo" → Uluslararası bölgeye bağlanır

---

### Kurulum 2: Çok Bölgesel Uluslararası

**Hedef**: AB, Kuzey Amerika, Asya, Diğer Dünya bölgeleri için farklı oranlar.

```
Bölge 1: "Avrupa Birliği"
  Ülkeler: [AT, BE, BG, CY, CZ, DE, DK, EE, ES, FI, FR, GR, HR, HU, IE, IT, LT, LU, LV, MT, NL, PL, PT, RO, SE, SI, SK]
  Öncelik: 100

Bölge 2: "Kuzey Amerika"
  Ülkeler: [US, CA, MX]
  Öncelik: 100

Bölge 3: "Asya Pasifik"
  Ülkeler: [AU, CN, HK, IN, JP, KR, NZ, SG, TH, TW]
  Öncelik: 100

Bölge 4: "Diğer Dünya"
  Ülkeler: [Boş bırakın]
  Öncelik: 1
```

**Kargo Yöntemleri**:
- "AB Kargo" → AB bölgesi
- "Kuzey Amerika Kargo" → Kuzey Amerika bölgesi
- "Asya Pasifik Kargo" → Asya Pasifik bölgesi
- "Uluslararası Standart" → Diğer Dünya bölgesi

---

### Kurulum 3: Uzak Alanlar Ücreti

**Hedef**: Yerel bölge içindeki uzak posta kodları için ek ücret.

```
Bölge 1: "Uzak Yerel"
  Ülkeler: [US]
  Posta Desenleri: ["^99[0-9]{3}$", "^96[7-9][0-9]{2}$"]  # Alaska, Hawaii
  Öncelik: 100

Bölge 2: "Standart Yerel"
  Ülkeler: [US]
  Öncelik: 50
```

**Kargo Yöntemleri**:
- "Uzak Kargo" → Uzak Yerel bölge (daha yüksek maliyet)
- "Standart Kargo" → Standart Yerel bölge

---

### Kurulum 4: Eyalet Özel Bölgeler

**Hedef**: Her ABD bölgesi için farklı oranlar.

```
Bölge 1: "Batı Kıyısı"
  Ülkeler: [US]
  Eyaletler: {"US": ["CA", "OR", "WA"]}
  Öncelik: 100

Bölge 2: "Doğu Kıyısı"
  Ülkeler: [US]
  Eyaletler: {"US": ["NY", "NJ", "CT", "MA", "PA"]}
  Öncelik: 100

Bölge 3: "Orta Bölü"
  Ülkeler: [US]
  Eyaletler: {"US": ["IL", "IN", "OH", "MI", "WI"]}
  Öncelik: 100

Bölge 4: "Güney"
  Ülkeler: [US]
  Eyaletler: {"US": ["TX", "FL", "GA", "NC", "SC"]}
  Öncelik: 100

Bölge 5: "Diğer ABD Eyaletleri"
  Ülkeler: [US]
  Öncelik: 50
```

---

## Posta Kodu Desen Örnekleri

Posta kodları, **regex** (düzenli ifadeler) kullanarak desen eşleme için kullanılır:

### ABD (ZIP Kodları)

**Format**: 5 haneli (örneğin, 90210)

```
Kaliforniya (90000-96199):  ^9[0-6][0-9]{3}$
New York (10000-14999):    ^1[0-4][0-9]{3}$
Texas (75000-79999, 88500-88599):  ^(7[5-9]|885)[0-9]{2}$
Alaska (99500-99999):      ^99[5-9][0-9]{2}$
```

### Kanada (Posta Kodları)

**Format**: A1A 1A1 (harf-sayı-harf boşluk sayı-harf-sayı)


Kanada poşta kodları:  ^[A-Z][0-9][A-Z] [0-9][A-Z][0-9]$",
  "Ontario (K, L, M, N, P):    ^[KLMNP][0-9][A-Z] [0-9][A-Z][0-9]$",
  "Quebec (G, H, J):           ^[GHJ][0-9][A-Z] [0-9][A-Z][0-9]$",
  "",
  "### Birleşik Krallık (Posta Kodları)",
  "",
  "**Format**: AA1A 1AA veya A1A 1AA",
  "",
  "London (E, EC, N, NW, SE, SW, W, WC):  ^(E|EC|N|NW|SE|SW|W|WC)[0-9]{1,2}",
  "Manchester (M):                        ^M[0-9]{1,2}",
  "Birmingham (B):                        ^B[0-9]{1,2}",
  "",
  "### Avustralya (Posta Kodları)",
  "",
  "**Format**: 4 haneli (örneğin, 2000)",
  "",
  "New South Wales (1000-2999):  ^[12][0-9]{3}$",
  "Victoria (3000-3999, 8000-8999):  ^[38][0-9]{3}$",
  "Queensland (4000-4999, 9000-9999):  ^[49][0-9]{3}$",
  "",
  "### Desen Testi",
  "",
  "**Desenleri kaydetmeden önce** bilinen posta kodlarıyla test edin:",
  "1. Desen girin: `^90[0-9]{3}$`",
  "2. Test girişi: "90210" → Eşleşmelidir",
  "3. Test girişi: "10001" → Eşleşmemelidir",
  "4. Test girişi: "9021" → Eşleşmemelidir (yalnızca 4 haneli)",
  "",
  "Kompleks desenleri doğrulamak için çevrimiçi regex test araçlarını kullanın (regex101.com).",
  "",
  "---",
  "",
  "## Bölge Kapsam Özeti",
  "",
  "Bölgeler, yönetici listede **kapsam özeti** olarak gösterilir ve ne içerdiğini gösterir:",
  "",
  "**Örnekler**:",
  "- "Tüm ülkeler" → Ülke kısıtlaması yok",
  "- "US, CA, MX" → 3 ülke",
  "- "US (CA, OR, WA)" → US ile 3 eyalet",
  "- "US (90xxx-91xxx)" → US ile posta kodu desenleri",
  "",
  "**Özeti Kullanım Amacı**:",
  "- Bölge kapsamlarını açmadan hızlıca doğrulayın",
  "- Kapsamda çakışmalar veya boşluklar tespit edin",
  "- Bölge yapılandırmasını hızlıca denetleyin",
  "",
  "---",
  "",
  "## Bölgeleri Sevkiyat Yöntemlerine Bağlama",
  "",
  "Bölgeler ve yöntemler arasında **çok-çok ilişki** vardır:",
  "",
  "**Yöntem Tarafından** (Tavsiyelidir):",
  "1. Sevkiyat Yöntemini Düzenleyin",
  "2. "Sevkiyat Bölgeleri" bölümüne kaydırın",
  "3. Uygun bölgeleri seçin (çoklu seçim)",
  "4. Yöntemi kaydedin",
  "",
  "**Bölge Tarafından**:",
  "- Bölgeler doğrudan yöntemlere bağlanmaz",
  "- Bağlama her zaman yöntem yapılandırmasından yapılır",
  "",
  "**Yöntem-Bölge Davranışı**:",
  "",
  "**Hiçbir bölge bağlanmamış** → Yöntem tüm adresler için kullanılabilir",
  "",
  "**Bölgeler bağlanmış** → Yöntem yalnızca müşteri adresi en az bir bağlı bölgeyle eşleşiyorsa kullanılabilir",
  "",
  "**Örnek**:",
  "``",
  "Yöntem: "Yerel Standart"",
  "Bağlı Bölgeler: ["Yerel ABD"]",
  "→ Yalnızca ABD adreslerine gösterilir",
  "",
  "Yöntem: "Uluslararası Express"",
  "Bağlı Bölgeler: ["AB", "Asya Pasifik", "Dünya'nın Geri Kalanı"]",
  "→ Tüm ABD dışı adresler için gösterilir",
  "``",
  "",
  "---",
  "",
  "## Bölge Eşleşmesi Testi",
  "",
  "Çalışmaya başlamadan önce bölge yapılandırmasını test edin:",
  "1. **Test Siparişleri Oluşturun**",
  "- Farklı bölgelerdeki adresleri kullanın",
  "- Doğru bölge eşleşmelerini doğrulayın",
  "",
  "2. **Öncelik Çözümünü Kontrol Edin**",
  "- Birden fazla bölgeye eşleşen bir adres kullanın",
  "- En yüksek öncelikli bölge kazanır",
  "- Beklenen sevkiyat yöntemlerinin görünmesini doğrulayın",
  "",
  "3. **Kenar Durumlarını Test Edin**",
  "- Sınır posta kodları (örneğin, 90999 vs 91000)",
  "- Eyalet sınırları",
  "- Benzer posta kodları olan uluslararası adresler",
  "",
  "4. **Bölge Önizleme Aracı** Kullanın** (eğer mevcutsa)",
  "- Test adresi girin",
  "- Hangi bölge(s) eşleştiğini görün",
  "- Öncelik çözümünü görün",
  "",
  "---",
  "",
  "## Sorun Giderme",
  "",
  "**Sorun 1: Ödeme sırasında hiçbir sevkiyat yöntemi mevcut değil**",
  "",
  "**Nedenleri**:",
  "- Müşteri adresi hiçbir bölgeyle eşleşmiyor",
  "- Tüm yöntemler eşleşmeyen bölgelere bağlanmış",
  "- Herhangi bir bölge kısıtlaması olmayan yöntem yok",
  "",
  "**Çözüm**:",
  "- Yedek bölge oluşturun (tüm ülkeler, öncelik 1)",
  "- Veya en az bir yöntemden bölge kısıtlamalarını kaldırın",
  "- Bölge ülke/eyalet/posta kodu desenlerini doğrulayın",
  "",
  "---",
  "",
  "**Sorun 2: Yanlış bölge eşleşmesi**",
  "",
  "**Nedenleri**:",
  "- Düşük öncelikli bölge seçilmesine rağmen yüksek öncelikli bölge eşleşiyor",
  "- Posta kodu deseni sözdizimi hatası (desen sessizce başarısız olur)",
  "- Eyalet kodu uyuşmazlığı (CA vs California)",
  "",
  "**Çözüm**:",
  "- Öncelik değerlerini doğrulayın (daha yüksek sayı = daha yüksek öncelik)",
  "- Posta kodu desenlerini regex doğrulayıcı ile test edin",
  "- 2 harfli eyalet kodlarını kullanın (CA, California değil)",
  "",
  "---",
  "",
  "**Sorun 3: Beklenmedik yöntem gösteriliyor**",
  "",
  "**Nedenleri**:",
  "- Yöntem hiçbir bölgeye bağlanmamış (her yerde kullanılabilir)",
  "- Birden fazla bölge eşleşiyorsa, beklenmedik bölge daha yüksek önceliğe sahip",
  "- Bölge kapsamları bilinmeden çakışıyor",
  "",
  "**Çözüm**:",
  "- Yöntemin bağlı bölgelerini gözden geçirin",
  "- Eşleşen bölgelerin önceliklerini kontrol edin",
  "- Bölge kapsamları özeti için çakışmaları denetleyin",
  "",
  "---",
  "",
  "## İpuçları",
  "",
  "Tüm markdown biçimlendirmesini, resim yollarını, kod bloklarını ve teknik terimleri koruyun.

- **2 bölgeyle başlayın** - Yerel ve Uluslararası, gerekirse genişletin
- **Önceliği akıllıca kullanın** - Belirli bölgeler 100, bölgesel 50, varsayılan 1
- **Posta desenlerini dikkatle test edin** - Regex hataları sessizce başarısız olur ve bölgeler eşleşmez
- **Bölge mantığını belgeleyin** - Bölgenin kapsam amaçlarını açıklayan notlar ekleyin
- **Aşırı bölgeyi kaçının** - Çok fazla bölge yapılandırma karmaşık hale getirir; karmaşık senaryolarda kargo kampanyalarını kullanın
- **Devlet kodlarını kullanın, isimlerini değil** - "CA" değil "California", "NY" değil "New York"
- **Varsayılan bölge oluşturun** - Tüm ülkeler, öncelik 1, en az bir kargo seçeneğinin her zaman mevcut olduğundan emin olun
- **Bölge performansını izleyin** - Eğer birçok müşteri "kargo mevcut değil" mesajını görürse, bölge kapsamlarını inceleyin
- **Yeni bölgeler için bölgeleri güncelleyin** - Yeni üyeler katıldığında AB bölgesine ülkeler ekleyin
- **Açıklayıcı isimler kullanın** - "AB (İngiltere Hariç)" "Bölge 3"den daha iyi bir isimdir
- **Gerçek adreslerle test edin** - Test sırasında gerçek müşteri adreslerini kullanın, hayali adresler değil