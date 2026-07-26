---
title: Ayarlamalı Program
---

Ayarlamalı program, mevcut müşterilerinin arkadaşlarıyla akrabalarıyla paylaşabileceği benzersiz bir referans bağlantısı sağlar. Referans verilen bir arkadaşın ilk geçerli satın alımını yaptıktan sonra hem referans veren hem de yeni müşteri ödüllendirilebilir — bu da sözlü tanıtım aracılığıyla yeni müşteri kazanımını sağlar.

## Referans programının nasıl çalıştığı

1. Bir müşteri, benzersiz referans bağlantısını (veya kodunu) bir arkadaşına paylaşır.
2. Arkadaş bağlantıya tıklar ve 30 gün (ayarlanabilir) boyunca bir çerezle izlenir.
3. Arkadaş kaydolur ve ilk geçerli siparişi verir.
4. Sistem bir referans ataması kaydı oluşturur ve dolandırıcılık ve elverişlilik kontrollerini çalıştırır.
5. Atama onaylandıysa, her iki taraf da ödüllendirilir.

Mağazanızda tek bir referans programı yapılandırması vardır. Ayarlamak için **Pazarlama > Referans Programı**'na gidin.

## Referans programınızı ayarlama

### Program durumu

Program üç durumda olabilir:

- **Taslak** — Program yapılandırılıyor ama henüz canlı değil. Referans bağlantıları etkin değil.
- **Aktif** — Program canlı. Müşteriler bağlantıları paylaşabilir ve ödüller kazanabilir.
- **Durduruldu** — Program geçici olarak durduruldu. Mevcut atamalar hala işlenir, ancak yeni referanslar izlenmez.

Hazırsanız **Durum**'u **Aktif** olarak ayarlayın. Herhangi bir zaman durdurabilirsiniz.

### Ödül yapılandırması

Bir referansın dönüştüğü zaman verilecek ödülleri tanımlayın. Program **çift taraflı ödüller** destekler — yani referans veren (bağlantıyı paylaşan müşteri) ve referans alınan (bağlantıyı kullanan yeni müşteri) her ikisine de ödül verebilirsiniz.

**Ödül Yapılandırması** alanına her alıcı için ödülleri yapılandırın. Kullanılabilir ödül türleri:

| Ödül Türü | Açıklama |
|-------------|-------------|
| **Mağaza Kredisi** | Müşterinin cüzdanına kredi ekler, gelecekteki siparişlerde kullanılabilir |
| **Kupon Kodu** | Benzersiz bir indirim kuponu kodu oluşturur |
| **Yüzde İndirimi** | Ödeme sırasında kullanılacak bir yüzde indirimi verir |
| **Özel Avantaj** | Özel bir avantaj (örneğin, ücretsiz hediye, öncelikli erişim) — ödül açıklaması alanında tanımlanır |

Kupon Kodu ve Yüzde İndirimi ödülleri, onları kazanan müşteriye kilitlenir — kupon kodu sadece o müşteri giriş yaptıktan sonra çalışır. Eğer referans veren kişi, referans bağlantısı yerine ödül kodunu başkalarıyla paylaşır, arkadaş bu kodu kullanamaz; sadece referans bağlantısı paylaşılmalıdır.

**Örnek yapılandırma** — referans verene $10 mağaza kredisi ve yeni müşteriye $10 indirim:

```json
{
  "referrer": {"kind": "credit", "amount": 10},
  "referee": {"kind": "discount", "amount": 10},
  "double_sided": true
}
```

Sadece referans verene ödül vermek istiyorsanız `"double_sided": false` ayarlayın.

### Elverişlilik kuralları

Elverişlilik kuralları, hangi referansların ödüllendirileceğini belirler. Bu kuralları **Elverişlilik Kuralları** alanında yapılandırın:

| Kural | Ne yapar |
|------|--------------|
| `new_customer_only` | Eğer `true` ise, referans verilen arkadaş yeni bir müşteri olmalıdır (önceki siparişi yok) |
| `min_order_value` | Referans verilen arkadaşın harcaması gereken minimum sipariş tutarı (mağaza para biriminde) |
| `exclude_discounts` | Eğer `true` ise, referans verilen müşteri bir kupon kullandığı siparişler elverişli değildir |
| `exclude_staff` | Eğer `true` ise, personel hesapları referans veren veya referans alınan kişiler olamaz |

**Örnek** — sadece yeni müşteriler, minimum $40 sipariş, personeller hariç:

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
| `issue_on` | Ödülün ne zaman verileceği: `signup` (kayıt sırasında hemen), `first_purchase` (siparişten hemen sonra) veya `post_refund` (iade penceresi sona erdiğinde) |
| `refund_window_days` | `post_refund` kullanırken ödüllerin verilmesinden önce kaç gün beklenmesi gerekir (varsayılan: 14 gün) |


post_refund, kullanmak en dikkatli yaklaşım - ödül vermeden önce iade penceresinin geçmesini bekleme, daha sonra iade edilen siparişlere ödül verme riskini azaltır.

### Başlık ve sınırlar

Bir referans verenin sınırsız ödül kazanmasını önlemek için **Başlık & Sınırlar** alanına sınırlar ayarlayın:

| Ayar | Ne yapar |
|---------|--------------|
| `monthly_per_referrer` | Ayda, referans verene göre başarılı referansların maksimum ödüllendirilme sayısı |
| `lifetime_per_referrer` | Her zaman, referans verene göre başarılı referansların toplam maksimum ödüllendirilme sayısı |
| `max_reward_per_order` | Başarılı bir referans dönüşü için verilen maksimum ödül değeri (mağazanızın para birimi cinsinden) |

**Örnek** — Ayda 20 referans, ömür boyu 200, dönüş başına maksimum $50 ödül:

```json
{
  "monthly_per_referrer": 20,
  "lifetime_per_referrer": 200,
  "max_reward_per_order": 50
}
```

### İzleme yapılandırması

Referans bağlantılarının nasıl izleneceğini **İzleme Yapılandırması** alanında yapılandırın:

| Ayar | Ne yapar |
|---------|--------------|
| `cookie_ttl_days` | Bir arkadaş bağlantıya tıkladıktan sonra referans izleme çerezinin aktif kalma süresi (varsayılan: 30) |
| `attribution` | Attributon yöntemi — şu anda `last_touch` (en son referans bağlantısı tıklaması kredite edilir) |

### Sahtecilik politikası

Sahtecilik tespiti sistemi, onayı onaylamadan önce her referans atamasını risk açısından puanlar. Politikayı **Sahtecilik Politikası** alanında yapılandırın:

| Ayar | Ne yapar |
|---------|--------------|
| `policy` | Genel kesinlik: `strict`, `balanced` veya `lenient` |
| `auto_reject_threshold` | Otomatik olarak reddedilen atamalar için risk puanı (0–100) (varsayılan: 80) |
| `auto_approve_threshold` | Otomatik olarak onaylanan atamalar için risk puanı (varsayılan: 30) |
| `check_ip` | Eğer `true`, referans veren ve referans alınan kişi aynı IP adresine sahip olup olmadığını kontrol eder |
| `check_device` | Eğer `true`, referans veren ve referans alınan kişi arasında paylaşılan cihaz parmak izlerini kontrol eder |
| `check_velocity` | Eğer `true`, tek bir kaynaktan anormal yüksek referans oranlarını izler |
| `velocity_window_hours` | Hız kontrolü için zaman penceresi (saat cinsinden) |
| `max_referrals_per_window` | Hız penceresi içinde bir kaynaktan izin verilen maksimum referans sayısı |

Risk puanı otomatik reddetme ve otomatik onaylama eşikleri arasında kalan atamalar **Beklemede** durumuna girer ve manuel inceleme gerektirir.

### Şartlar ve koşullar

Program için herhangi bir hukuki şart ve koşulu **Şartlar & Koşullar** alanına girin. Bu metin, müşteriler referans programını görüntülediğinde onlara gösterilir. Markdown biçimlendirmesi desteklenir.

## Referans atamalarını görüntüleme

**Pazarlama > Referans Atamaları**'na giderek tüm referans durumlarını görün — bir referans veren ve referans alınan müşteri arasındaki bağlantı.

![Referans atamaları listesi](/static/core/admin/img/help/referral-program/attribution-list.webp)

Her atama, referans vereni, referans alınan müşteriyi, ilk siparişini, mevcut durumu ve risk puanını gösterir.

### Atama durumları

| Durum | Ne anlama gelir |
|--------|---------------|
| **Beklemede** | İnceleme bekliyor — risk puanı manuel inceleme aralığında |
| **Onaylandı** | Referans geçerlidir — ödüller verildi veya verilecek |
| **Reddedildi** | Referans kriterleri karşılamadı veya sahtecilik olarak işaretlendi |
| **Süresi doldu** | Referans izleme penceresi içinde dönüş sağlanmadı |

### Atamaları manuel olarak onaylama veya reddetme

**Beklemede** durumunda olan atamaları, atama kaydını açıp eylem butonlarını kullanarak manuel olarak onaylayabilir veya reddedebilirsiniz. Reddetme seçeneğinde bir **Reddetme Nedeni** seçin:

- Kendi Referansı
- Yeni Müşteri Değil
- Minimum Sipariş Değeri Aşağısında
- Atık E-posta
- Sınırlama Aşındı
- Sahtecilik Riski
- Sipariş İade Edildi veya İptal Edildi
- Manuel Reddetme

Reddetme notları da kendi kayıtlarınız için ekleyebilirsiniz.

### Risk seviyesine göre filtreleme

Yan çubukta **Risk Seviyesi** filtresini kullanarak inceleme gerektiren yüksek riskli atamalara odaklanın:

- Düşük Risk (puan 0–30) — Otomatik onaylı
- Orta Risk (puan 31–70) — Manuel inceleme
- Yüksek Risk (puan 71–89) — Manuel inceleme, dikkatli davran
- Çok Yüksek Risk (puan 90+) — Otomatik reddedilir

## Verilen ödülleri görüntüleme

**Pazarlama > Verilen Ödüller** menüsüne giderek, onaylanan atamalardan kaynaklanan tüm ödülleri görebilirsiniz.

Her ödül girişi, müşteri, referans veren mi referans verilen mi, ödül türü ve miktarı ve şu anki kuponlama durumu gösterir.

### Ödül durumları

| Durum | Ne anlama gelir |
|--------|---------------|
| **Beklemede** | Ödül oluşturuldu ancak müşteriye henüz teslim edilmedi |
| **Verildi** | Ödül aktif ve müşteri tarafından kullanılabilir |
| **Kullanıldı** | Müşteri ödülü kullandı |
| **Süresi doldu** | Ödül, kullanılmadan süresi doldu |
| **İptal edildi** | Ödül manuel olarak iptal edildi (örneğin, ödül verildikten sonra orijinal sipariş iade edildiğinde) |

### Ödülü iptal etme

Bir ödülü iptal etmeniz gerekiyorsa — örneğin, kriterleri sağlayan sipariş iade edildiysse — ödülü açın ve **İptal Et** eylemini kullanın. İptal nedenini belirten bir not ekleyin.

## İpuçları

- `post_refund` zamanlama ayarıyla başlayın. Ödül vermeden önce iade penceresinin sona ermesini beklemek, sonunda iade edilen siparişlere ödül verilmesini önler.
- `balanced` dolanma politikası çoğu mağazanın için iyi bir varsayılan ayar olabilir. Eğer çok az hesaptan gelen referansların anormal bir artışını fark ederseniz `strict` olarak değiştirin.
- Gerçekçi aylık ve ömür boyu sınırlar ayarlayın. Ödül değeri yüksekse, aylık olarak her referans veren için 10–20 arasında bir tavan, kötüye kullanımın önlenmesi açısından mantıklıdır.
- Haftada bir kez **Beklemede** olan atamaları inceleyin. Onları çok uzun süre gözden geçirmeden bırakmak, ödülü bekleyen meşru referans verenleri kızdırmakta olabilir.
- Manuel inceleme kuyruğunuzu önceliklendirmek için **Risk Seviyesi** filtresini kullanın — çok yüksek riskli atamalardan başlayarak orta riskli olanlara geçin.
- Şartlar ve Koşullarınızı kısa ve basit dilde tutun. Müşteriler kuralları açıkça anladıklarında daha çok katılmaya eğilimlidir.