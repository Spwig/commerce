---
title: Coğrafiye Tabanlı İş Kuralı
---

Coğrafiye tabanlı iş kuralları, ziyaretcinin belirli bir ülke, bölge veya cihaz türünden geldiğinde otomatik olarak eylemler almanızı sağlar. Kuralları, belirli bir bölgeden gelen müşterilere bir para birimi ayarlamak, ziyaretçileri yerelleştirilmiş bir sayfaya yönlendirmek, promosyonlu bir banner göstermek veya belirli içeriklere erişimi kısıtlamak için kullanabilirsiniz.

Kurallar, her ziyaretçinin oturumu kurulduğunda öncelik sırasına göre değerlendirilir. Kural eşleştiğinde, yapılandırılmış eylemler hemen uygulanır.

## İş kuralları nasıl çalışır

Her kural iki bölümden oluşur:

- **Şartlar** — kuralın tetiklenmesi için karşılanması gereken kriterler (örneğin, "ziyaretçi Almanya'dan geliyor")
- **Eylemler** — tüm şartlar karşılandığında ne olacağını belirten eylemler (örneğin, "para birimini EUR olarak ayarla")

Şartlar ve eylemler, kural formunda JSON nesneleri olarak saklanır. Spwig, tüm etkin kuralları öncelik sırasına göre (en düşük sayıdan başlayarak) değerlendirir ve eşleşenleri uygular.

## İş kurallarına erişme

**Müşteriler > İş Kuralları**'na giderek tüm yapılandırılmış kuralları görebilirsiniz. Liste, her kuralın adını, durumunu, önceliğini, kaç kez tetiklendiğini ve son tetiklendiği zamanı gösterir.

Herhangi bir kuralı görüntülemek veya düzenlemek için üzerine tıklayın veya **+ İş Kuralı Ekle**'ye tıklayarak yeni bir kural oluşturun.

## İş kuralı oluşturma

### Adım 1: temel bilgiler

Kuralın tanımlama bilgilerini doldurun:

- **Ad** — açık ve açıklayıcı bir isim (örneğin, `Euro Bölgesi için EUR Ayarla`)
- **Açıklama** — kuralın amaçlarını açıklayan isteğe bağlı notlar
- **Etkin mi** — kuralı etkinleştirmek için işaretleyin; durdurmak için kaldırın ama silmeyin
- **Öncelik** — daha düşük sayılar önce çalışır; gelecekteki kurallar için `10`, `20`, `30` kullanın

### Adım 2: şartları tanımla

**Şartlar** alanına, kuralın ne zaman tetikleneceğini açıklayan bir JSON nesnesi girin. Nesnedeki tüm şartlar doğru olduğunda kural eşleşir.

#### Kullanılabilir şart anahtarları

| Şart | Format | Örnek |
|------|--------|-------|
| `country_in` | ISO ülke kodlarının dizisi | `["DE", "FR", "IT"]` |
| `country_not_in` | ISO ülke kodlarının dizisi | `["US", "CA"]` |
| `region_in` | Bölge isimlerinin dizisi | `["Bavaria", "Catalonia"]` |
| `region_not_in` | Bölge isimlerinin dizisi | `["Quebec"]` |
| `is_mobile` | Boole | `true` |
| `is_vpn` | Boole | `false` |

#### Örnek şartlar

Almanya, Fransa veya İtalya'dan gelen ziyaretçiler:
```json
{
  "country_in": ["DE", "FR", "IT"]
}
```

Amerika Birleşik Devletleri'nden ve mobil cihazda olan ziyaretçiler:
```json
{
  "country_in": ["US"],
  "is_mobile": true
}
```

Avrupa Birliği dışından gelen ziyaretçiler:
```json
{
  "country_not_in": ["AT","BE","BG","CY","CZ","DE","DK","EE","ES","FI","FR","GR","HR","HU","IE","IT","LT","LU","LV","MT","NL","PL","PT","RO","SE","SI","SK"]
}
```

### Adım 3: eylemleri tanımla

**Eylemler** alanına, kural tetiklendiğinde ne olacağını açıklayan bir JSON nesnesi girin.

#### Kullanılabilir eylem anahtarları

| Eylem | Format | Açıklama |
|--------|--------|-------------|
| `set_currency` | Para birimi kodu dizesi | Ziyaretçinin için bir para birimi seçin |
| `set_language` | Dil kodu dizesi | Görünüm dilini ayarla |
| `show_banner` | Boole | Promosyonlu bir banner tetikle |
| `redirect_to` | URL yolu dizesi | Ziyaretçiyi farklı bir URL'ye yönlendir |

#### Örnek eylemler

Para birimini Euro olarak ayarla:
```json
{
  "set_currency": "EUR"
}
```

Bir yerelleştirilmiş ana sayfaya yönlendir:
```json
{
  "redirect_to": "/de/"
}
```

Para birimi ve dili birlikte ayarla:
```json
{
  "set_currency": "GBP",
  "set_language": "en"
}
```

## Pratik örnekler

### Örnek: Euro Bölgesi Para Birimi Kuralı

**Senaryo:** Euro Bölgesi ülkelerinden gelen ziyaretçilere otomatik olarak Euro fiyatlarını göster.

| Alan | Değer |
|------|-------|
| Ad | `Euro Bölgesi — EUR Ayarla` |
| Öncelik | `10` |
| Etkin mi | İşaretli |
| Şartlar | `{"country_in": ["AT","BE","DE","ES","FI","FR","GR","IE","IT","LU","NL","PT"]}` |
| Eylemler | `{"set_currency": "EUR"}` |

### Örnek: Birleşik Krallık Para Birimi Kuralı

**Senaryo:** Birleşik Krallık'tan gelen ziyaretçilere GBP fiyatlarını göster.

| Alan | Değer |
|-------|-------|
| Ad | `UK — Set GBP` |
| Öncelik | `20` |
| Etkin | İşaretli |
| Koşullar | `"{\"country_in\": [\"GB\"]}"` |
| Eylemler | `"{\"set_currency\": \"GBP\"}"` |

### Örnek: yerelleştirilmiş bir mağaza bölümüne yönlendirme

**Senaryo:** Avustralya'dan gelen ziyaretçileri özel bir Avustralya sayfasına yönlendirin.

| Alan | Değer |
|-------|-------|
| Ad | `Australia — Redirect` |
| Öncelik | `30` |
| Etkin | İşaretli |
| Koşullar | `"{\"country_in\": [\"AU\"]}"` |
| Eylemler | `"{\"redirect_to\": \/au\/}"` |

## Kural testi

Kuralların beklenen ziyaretçi profiline uyup uymadığını, gerçek trafik beklemek zorunda kalmadan doğrulayabilirsiniz:

1. İşlem Kuralları listesinde, kuralın onay kutusunu seçin
2. **Eylem** açılır menüsünü açın ve **Seçilen kuralları test et**'i seçin
3. **Git**'e tıklayın

Spwig, kuralı bir örnek ABD tabanlı ziyaretçi profiline karşı değerlendirir ve eşleşip eşleşmediğini ve hangi eylemlerin tetikleneceğini raporlar.

## Kural etkinliğini izleme

İşlem kuralları listesindeki **Triggers** sütunu, her kuralın kaç kez tetiklendiğini gösterir. Bir kuralı seçerek **İstatistikler** bölümünde **Son Tetiklenme** zaman damgasını görebilirsiniz.

Kuralları değiştirdikten sonra belirli bir tarihten itibaren ölçüm yapmak isterseniz, **İstatistikleri sıfırla** eylemini kullanarak tetikleme sayımını sıfırlayabilirsiniz.

## İpuçları

- Yeni kurallar eklemek için öncelikleri sıralı numaralar (1, 2, 3) yerine boşluklarla (10, 20, 30) ayarlayın
- Kurallar öncelik sırasına göre tetiklenir ve tüm eşleşen kurallar uygulanır — eğer iki kural da para birimi ayarlamak istiyorsa, daha düşük öncelikli (daha yüksek numaralı) kuralın eylemi son olarak uygulanır
- Promosyon sırasında bir kuralı geçici olarak durdurmak isterseniz, **Etkin** anahtarını kullanın ve yapılandırmayı silmeyin
- Her yeni kuralı canlı ortamda etkinleştirmeden önce test edin, koşulların doğru olduğundan emin olun
- VPN tespiti (`"is_vpn": true`) ziyaretçilerin konumlarını gizlemek isteyen farklı muamele uygulamak isterseniz kullanılabilir, ancak bazı geçerli müşterilerin gizlilik için VPN kullanıyor olabileceğini unutmayın