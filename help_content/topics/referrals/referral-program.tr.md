---
title: Ayarlamalı Program
---

Ayarlamalı program, mevcut müşterilerinin arkadaşlarıyla ve aileleriyle paylaşabileceği benzersiz bir referans bağlantısı sağlar. Referans verilen bir arkadaşın ilk geçerli satın alımını yaptıktan sonra, hem referans veren hem de yeni müşteri ödüllendirilebilir — bu da sözlü tanıtım aracılığıyla yeni müşteri kazanımını sağlar.

## Referans programı nasıl çalışır

1. Bir müşteri, benzersiz referans bağlantısını (veya kodunu) bir arkadaşına paylaşır.
2. Arkadaş bağlantıya tıklar ve 30 gün (ayarlanabilir) boyunca bir çerezle izlenir.
3. Arkadaş kaydolur ve ilk geçerli siparişi verir.
4. Sistem bir referans ataması kaydı oluşturur ve dolandırıcılık ve elenebilirlik kontrollerini çalıştırır.
5. Atama onaylandıysa, her iki taraf da ödüllendirilir.

Mağazanızda tek bir referans programı yapılandırması vardır. Ayarlamak için **Pazarlama > Referans Programı**'na gidin.

## Referans programınızı ayarlama

### Program durumu

Program üç durumda olabilir:

- **Taslak** — Program yapılandırılıyor ama henüz canlı değil. Referans bağlantıları etkin değil.
- **Aktif** — Program canlı. Müşteriler bağlantıları paylaşabilir ve ödüller kazanabilir.
- **Durduruldu** — Program geçici olarak durduruldu. Mevcut atamalar hala işlenir, ancak yeni referanslar izlenmez.

Hazır olduğunuzda **Durum**'u **Aktif** olarak ayarlayın. Herhangi bir zaman durdurabilirsiniz.

### Ödül yapılandırması

Bir referansın dönüştüğü zaman verilecek ödülleri tanımlayın. Program **çift taraflı ödüller** destekler — yani referans veren (bağlantıyı paylaşan müşteri) ve referans alınan (bağlantıyı kullanan yeni müşteri) her ikisine de ödül verebilirsiniz.

**Ödül Yapılandırması** alanına her alıcı için ödülleri yapılandırın. Kullanılabilir ödül türleri:

| Ödül Türü | Açıklama |
|-------------|-------------|
| **Mağaza Kredisi** | Müşterinin cüzdanına kredi ekler, gelecekteki siparişlerde kullanılabilir |
| **Kupon Kodu** | Benzersiz bir indirim kuponu kodu oluşturur |
| **Yüzde İndirimi** | Ödeme sırasında kullanılacak bir yüzde indirimi verir |
| **Özel Avantaj** | Özel bir avantaj (örneğin, ücretsiz hediye, öncelikli erişim) — ödül açıklaması alanında tanımlanır |

**Örnek yapılandırma** — referans verene 10 dolar mağaza kredisi ve yeni müşteriye 10 dolar indirim:

```json
{
  "referrer": {"kind": "credit", "amount": 10},
  "referee": {"kind": "discount", "amount": 10},
  "double_sided": true
}
```

Sadece referans verene ödül vermek istiyorsanız, `"double_sided": false` ayarlayın.

### Elenebilirlik kuralları

Elenebilirlik kuralları, hangi referansların ödüllendirileceğini belirler. Bu kuralları **Elenebilirlik Kuralları** alanına yapılandırın:

| Kural | Ne yapar |
|------|--------------|
| `new_customer_only` | Eğer `true` ise, referans verilen arkadaş yeni bir müşteri olmalıdır (önceki siparişi yok) |
| `min_order_value` | Referans verilen arkadaşın harcaması gereken minimum sipariş tutarı (mağaza para biriminde) |
| `exclude_discounts` | Eğer `true` ise, referans verilen müşteri bir kupon kullandığı siparişler elenmez |
| `exclude_staff` | Eğer `true` ise, personel hesapları referans veren veya referans alınan kişiler olamaz |

**Örnek** — sadece yeni müşteriler, minimum 40 dolar sipariş, personeller hariç:

```json
{
  "new_customer_only": true,
  "min_order_value": 40.0,
  "exclude_discounts": false,
  "exclude_staff": true
}
```

### Zamanlama yapılandırması

**Zamanlama Yapılandırması** alanı, geçerli bir siparişten sonra ödüllerin ne zaman verileceğini kontrol eder:

| Ayar | Ne yapar |
|---------|--------------|
| `issue_on` | Ödülün ne zaman verileceği: `signup` (kayıt sırasında hemen), `first_purchase` (sipariş sonrası hemen) veya `post_refund` (iade penceresi sona erdiğinde) |
| `refund_window_days` | `post_refund` kullanırken ödüllerin verilmesinden önce kaç gün bekleyin (varsayılan: 14 gün) |

`post_refund` en dikkatli yaklaşım — iade penceresi geçene kadar ödüllerin verilmesini bekler, bu da daha sonra iade edilen siparişlere ödül verme riskini azaltır.

### Tavanlar ve sınırlar

Bir referans verenin sınırsız ödüller kazanmasını önlemek için **Tavanlar & Sınırlar** alanında tavanlar ayarlayın:

| Ayar | Ne yapar |
|---------|--------------|
| `monthly_per_referrer` | Ayda kişi başı ödüllendirilen başarılı referansların maksimum sayısı |
| `lifetime_per_referrer` | Her zaman kişi başı ödüllendirilen toplam başarılı referansların maksimum sayısı |
| `max_reward_per_order` | Tek bir referans dönüşü için verilen maksimum ödül değeri (mağazanızın para birimi cinsinden) |

**Örnek** — Ayda 20 referans, ömür boyu 200, dönüş başına maksimum $50 ödül:

```json
{
  "monthly_per_referrer": 20,
  "lifetime_per_referrer": 200,
  "max_reward_per_order": 50
}
```

### Takip yapılandırması

Referans bağlantılarının nasıl izleneceğini **Takip Yapılandırması** alanından yapılandırın:

| Ayar | Ne yapar |
|---------|--------------|
| `cookie_ttl_days` | Bir arkadaş bağlantıya tıkladıktan sonra referans izleme çerezinin aktif kalacağı gün sayısı (varsayılan: 30) |
| `attribution` | Attributon yöntemi — şu anda `last_touch` (en son referans bağlantısı tıklaması kredite edilir) |

### Sahtecilik politikası

Sahtecilik tespiti sistemi, onaylamadan önce her referans atibutonunu risk açısından puanlar. Politikayı **Sahtecilik Politikası** alanından yapılandırın:

| Ayar | Ne yapar |
|---------|--------------|
| `policy` | Genel kesinlik düzeyi: `strict`, `balanced` veya `lenient` |
| `auto_reject_threshold` | Attributonların otomatik olarak reddedildiği risk puanı (0–100) (varsayılan: 80) |
| `auto_approve_threshold` | Attributonların otomatik olarak onaylandığı risk puanı alt sınırı (varsayılan: 30) |
| `check_ip` | Eğer `true` ise, referans veren ve referans alanın aynı IP adresine sahip olup olmadığını kontrol eder |
| `check_device` | Eğer `true` ise, referans veren ve referans alan arasında ortak cihaz parmak izi olup olmadığını kontrol eder |
| `check_velocity` | Eğer `true` ise, tek bir kaynaktan anormal derecede yüksek referans oranlarını izler |
| `velocity_window_hours` | Hız kontrolü için zaman penceresi (saat cinsinden) |
| `max_referrals_per_window` | Hız penceresi içinde bir kaynaktan izin verilen maksimum referans sayısı |

Risk puanı otomatik reddetme ve otomatik onaylama eşikleri arasında kalan attributonlar **Beklemede** durumuna girer ve manuel inceleme gerektirir.

### Şartlar ve koşullar

Program için herhangi bir hukuki şart ve koşulu **Şartlar & Koşullar** alanına girin. Bu metin, müşterilere referans programını görüntülediklerinde gösterilir. Markdown biçimlendirmesi desteklenir.

## Referans attributonlarını görüntüleme

**Pazarlama > Referans Attributonları** alanına giderek tüm referans durumlarını görüntüleyin — bir referans veren ve referans alan müşteri arasındaki bağlantı.

![Referans attributonları listesi](/static/core/admin/img/help/referral-program/attribution-list.webp)

Her attributon, referans veren kişiyi, referans alan müşteriyi, ilk verdikleri siparişi, mevcut durumu ve risk puanını gösterir.

### Attributon durumları

| Durum | Ne anlama gelir |
|--------|---------------|
| **Beklemede** | İnceleme bekliyor — risk puanı manuel inceleme aralığında |
| **Onaylandı** | Referans geçerlidir — ödüller verildi veya verilecek |
| **Reddedildi** | Referans kriterleri karşılamadı veya sahtecilik olarak işaretlendi |
| **Süresi Dolmuş** | Referans izleme penceresi içinde dönüş sağlanmadı |

### Attributonları manuel olarak onaylama veya reddetme

**Beklemede** durumunda olan attributonları, attributon kaydını açıp eylem butonlarını kullanarak manuel olarak onaylayabilir veya reddedebilirsiniz. Reddetme seçeneğinde bir **Reddetme Nedeni** seçin:

- Kendi Referansı
- Yeni Müşteri Değil
- Minimum Sipariş Değeri Aşağısında
- Atık E-posta
- Kotalar Aşıldı
- Sahtecilik Riski
- Sipariş İade Edildi veya İptal Edildi
- Manuel Reddetme

Reddetme notları eklemek için **Reddetme Notları** alanını da kullanabilirsiniz.

### Risk düzeyine göre filtreleme

Yan çubukta **Risk Düzeyi** filtresini kullanarak inceleme gerektiren yüksek riskli attributonlara odaklanın:

- Düşük Risk (puan 0–30) — Otomatik onaylandı
- Orta Risk (puan 31–70) — Manuel inceleme
- Yüksek Risk (puan 71–89) — Manuel inceleme, dikkatli olun
- Çok Yüksek Risk (puan 90+) — Otomatik reddedildi

## Verilen ödülleri görüntüleme

**Pazarlama > Verilen Ödüller** menüsüne giderek, onaylanan atamalardan kaynaklanan tüm ödülleri görebilirsiniz.

Her ödül girişi, müşteri, referans veren mi referans verilen mi, ödül türü ve miktarı ve şu anki kuponlama durumu gibi bilgileri gösterir.

### Ödül durumları

| Durum | Ne anlama gelir |
|--------|---------------|
| **Beklemede** | Ödül oluşturuldu ancak müşteriye henüz teslim edilmedi |
| **Verildi** | Ödül aktif ve müşteri tarafından kullanılabilir |
| **Kullanıldı** | Müşteri ödülü kullandı |
| **Süresi doldu** | Ödül, kullanılmadan süresi doldu |
| **İptal edildi** | Ödül manuel olarak iptal edildi (örneğin, ödül verildikten sonra orijinal sipariş iade edildiğinde) |

### Ödülün iptali

Bir ödülü iptal etmeniz gerekiyorsa — örneğin, kriterleri sağlayan sipariş iade edildi — ödülü açın ve **İptal** eylemini kullanın. İptal nedenini belirten bir not ekleyin, kayıtlarınız için.

## İpuçları

- `post_refund` zaman ayarı ile başlayın. Ödül vermeden önce iade penceresinin sona ermesini beklemek, sonunda iade edilen siparişlere ödül verilmesini önler.
- `balanced` dolanma politikası çoğu mağazanın için iyi bir varsayılan ayar olabilir. Eğer çok az hesaptan gelen referansların anormal bir artışını fark ederseniz `strict` ayarına geçin.
- Gerçekçi aylık ve ömür boyu sınırlar ayarlayın. Ödül değeri yüksekse, aylık olarak her referans veren için 10–20 arasında bir tavan, kötüye kullanımın önlenmesi açısından mantıklıdır.
- Haftada bir kez **Beklemede** olan atamaları gözden geçirin. Onları çok uzun süre gözden geçirmeden bırakmak, ödülü bekleyen meşru referans verenleri kızdırmakta olabilir.
- **Risk Seviyesi** filtresini kullanarak manuel inceleme kuyruğunuzu önceliklendirin — çok yüksek riskli atamalardan başlayarak orta riskli olanlara geçin.
- Şartlar ve Koşullarınızı kısa ve basit dilde tutun. Müşteriler kuralları açıkça anladıklarında daha fazla katılmaya eğilimlidir.