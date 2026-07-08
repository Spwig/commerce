---
title: Abonelik İndirimleri
---

Abonelik indirimleri, bireysel müşteri aboneliklerine fiyat indirimleri uygulamanıza olanak tanır — örneğin, sadık aboneleri ödüllendirmek, promosyon kuponlarını onaylamak veya iyi niyet kredisini kullanarak fatura anlaşmazlıklarını çözmek. Plan seviyesi fiyat katmanlarından farklı olarak, bu indirimler belirli bir abonelik doğrudan uygulanır.

## Abonelik indirimlerini görüntüleme

**Abonelikler > Abonelik İndirimleri**'ne giderek tüm aboneliklerinize uygulanan indirimleri görebilirsiniz.

Her girdi, abonelik ait olduğu, indirim türü ve değeri, ne kadar süreyle devam ediyor ve hâlâ aktif olup olmadığını gösterir.

Bir abonelikle ilişkili indirimleri bulmak için **Abonelikler > Müşteri Abonelikleri**'ni açın, bir abonelik üzerine tıklayın ve detay sayfasının altındaki **İndirimler** bölümüne kaydırın.

## Bir abonelik için indirim ekleme

Yeni bir indirim eklemek için:

1. **Abonelikler > Abonelik İndirimleri**'ne gidin
2. **+ Abonelik İndirimi Ekle**'ye tıklayın
3. İndirimi uygulamak istediğiniz **Abonelik**'i seçin
4. İndirim ayarlarını yapılandırın (aşağıda açıklanmıştır)
5. **Kaydet**'e tıklayın

İndirim, bir sonraki fatura döngüsünde etkin olur.

## İndirim türleri

İndirimin nasıl hesaplandığını seçin:

| İndirim Türü | Nasıl Çalışır | Örnek |
|---------------|--------------|---------|
| **Yüzde İndirimi** | Faturayı bir yüzde oranıyla azaltır | `20` 50 dolarlık faturayı 40 dolar yapar |
| **Sabit Tutar İndirimi** | Faturadan sabit bir tutar çıkarır | `10` 50 dolarlık faturayı 40 dolar yapar |
| **Sabit Fiyat Üzerine Yaz** | Aboneliği, normal plan fiyatına bakılmaksızın belirli bir fiyata ayarlar | `29` faturayı 29 dolar/dönem yapar |

**İndirim Değeri** alanını, seçtiğiniz tür (yüzde, dolar tutarı veya sabit fiyat) ile ilgili sayıya ayarlayın.

### Örnek: müşteri koruma teklifi

Bir müşteri, iptal etmek istediğini söylüyor. Ona 3 ay boyunca %25 indirimle kalmayı teklif ediyorsunuz:

| Alan | Değer |
|-------|-------|
| İndirim Türü | Yüzde İndirimi |
| İndirim Değeri | `25` |
| Süre Türü | Tekrar Eden |
| Süre (Ay) | `3` |

## İndirim Süresi

İndirimin gelecekteki fatura döngüleri için ne kadar süreyle uygulanacağını kontrol edin:

| Süre Türü | Ne Zaman Uygulanır |
|---------------|-----------------|
| **Bir Kere Uygula** | Sadece bir sonraki fatura döngüsünü azaltır, sonra otomatik olarak sona erer |
| **Süresiz** | Gelecekteki tüm fatura döngülerine uygulanır, manuel olarak devre dışı bırakılana kadar |
| **Tekrar Eden** | Belirli bir ay sayısı için uygulanır, sonra sona erer |

**Tekrar Eden** indirimler için, **Süre (Aylar)** alanını, indirimin ne kadar süreyle devam edeceğine karşılık gelen ay sayısına ayarlayın. **Kalan Döngüler** alanı, kalan döngü sayısını izler — her fatura döngüsüyle birlikte sayıcı azalır.

## Kupon Kodları

İndirim, promosyonel bir kupon kodu tarafından tetiklendiyse, **Kupon Kodu** alanına girin. Bu bilgilidir — hangi promosyonun indirimi kaynaklandığını kendi izleme amaçlarınız için kaydeder.

## İndirimi Devre Dışı Bırakma

İndirimin doğal sonuna ulaşmadan durdurmak istiyorsanız, indirim kaydını açın ve **Aktif** onay kutusunu kaldırın, sonra kaydedin. İndirim, gelecekteki fatura döngüleri için artık uygulanmaz. Abonelik, bir sonraki fatura döngüsünde normal plan fiyatına döner.

İndirimi oluştururken, **Sona Eriş Tarihi** alanına bir tarih ayarlayabilirsiniz — sistem, bu tarihten sonra otomatik olarak indirimi devre dışı bırakır.

## İpuçları

- **Bir Kere Uygula** indirimlerini, tek seferlik iyi niyetli davranışlar için kullanın (örneğin, bir hizmet kesilmesi nedeniyle bir aboneyi telafi etmek).

Temiz ve kendiliğinden sona erenlerdir.
- **Yüzde İndirimi** indirimleri, değişken fiyatlı abonelikler için **Sabit Tutar İndirimi**'den daha güvenlidir, çünkü indirim, gerçek fatura tutarına göre ölçeklenir.
- Bir müşteri koruma teklifi sunarken, **Tekrar Eden** ve 3 aylık bir süre kullanın — müşterilere kalma nedeni sağlar ancak gelirinizi kalıcı olarak azaltmaz.
- **Kupon Kodu** alanını, müşterilerin kullandığı kodla tutarlı tutun.

# Satın Alma ve Abonelikler

## Satın Alma

### Satın Alma

Satın alma, kullanıcıların ürünleri satın almak için kullandığı işlem sistemidir. Spwig, ödeme işlemi için Stripe ve PayPal gibi ödeme sağlayıcılarıyla entegre olabilir. Satın alma süreci, ürün seçimi, ödeme onayı ve sipariş tamamlama gibi adımları içerir.

### Abonelikler

Abonelikler, kullanıcıların belirli bir süre boyunca ürün veya hizmete erişimi için düzenli olarak ücret ödemeleri gerektiren bir ödeme modelidir. Spwig, aboneliklerin yönetimi için Django ve PostgreSQL gibi teknolojileri kullanır. Abonelikler, kullanıcıların aboneliklerini yönetmelerine ve iptal etmelerine olanak tanır.

### Satın Alma ve Abonelikler Arasındaki İlişki

Satın alma ve abonelikler, kullanıcıların ürünleri satın almak ve hizmetlere erişmek için kullandığı iki farklı ödeme modelidir. Satın alma, tek seferlik ödeme gerektirirken, abonelikler düzenli olarak ücret ödemeleri gerektirir. Spwig, bu iki modelin yönetimi için ayrı ayrı sistemler sunar.

## Satın Alma Sistemi

### Satın Alma Sistemi

Spwig, kullanıcıların ürünleri satın almak için kullandığı işlem sistemidir. Satın alma sistemi, ürün seçimi, ödeme onayı ve sipariş tamamlama gibi adımları içerir. Spwig, ödeme işlemi için Stripe ve PayPal gibi ödeme sağlayıcılarıyla entegre olabilir.

### Ödeme Yöntemleri

Spwig, kullanıcıların ürünleri satın almak için kullandığı ödeme yöntemlerini destekler. Ödeme yöntemleri, kredi kartı, banka havalesi ve PayPal gibi farklı türlerde olabilir. Spwig, ödeme yöntemlerinin yönetimi için Django ve PostgreSQL gibi teknolojileri kullanır.

### Satın Alma Siparişleri

Spwig, kullanıcıların ürünleri satın almak için oluşturdukları siparişleri yönetir. Satın alma siparişleri, ürün seçimi, ödeme onayı ve sipariş tamamlama gibi adımları içerir. Spwig, siparişlerin yönetimi için Django ve PostgreSQL gibi teknolojileri kullanır.

## Abonelik Sistemi

### Abonelik Sistemi

Spwig, kullanıcıların belirli bir süre boyunca ürün veya hizmete erişimi için düzenli olarak ücret ödemeleri gerektiren bir ödeme modelidir. Abonelik sistemi, kullanıcıların aboneliklerini yönetmelerine ve iptal etmelerine olanak tanır. Spwig, aboneliklerin yönetimi için Django ve PostgreSQL gibi teknolojileri kullanır.

### Abonelik Planları

Spwig, kullanıcıların belirli bir süre boyunca ürün veya hizmete erişimi için düzenli olarak ücret ödemeleri gerektiren abonelik planlarını destekler. Abonelik planları, farklı fiyatlandırma seviyelerine sahip olabilir. Spwig, abonelik planlarının yönetimi için Django ve PostgreSQL gibi teknolojileri kullanır.

### Abonelik Yönetimi

Spwig, kullanıcıların aboneliklerini yönetmelerine ve iptal etmelerine olanak tanır. Abonelik yönetimi, kullanıcıların aboneliklerini düzenlemelerine ve iptal etmelerine olanak tanır. Spwig, abonelik yönetimi için Django ve PostgreSQL gibi teknolojileri kullanır.

## Satın Alma ve Abonelikler Arasındaki İlişki

### Satın Alma ve Abonelikler Arasındaki İlişki

Satın alma ve abonelikler, kullanıcıların ürünleri satın almak ve hizmetlere erişmek için kullandığı iki farklı ödeme modelidir. Satın alma, tek seferlik ödeme gerektirirken, abonelikler düzenli olarak ücret ödemeleri gerektirir. Spwig, bu iki modelin yönetimi için ayrı ayrı sistemler sunar.

### Satın Alma ve Aboneliklerin Karşılaştırılması

Satın alma ve abonelikler, kullanıcıların ürünleri satın almak ve hizmetlere erişmek için kullandığı iki farklı ödeme modelidir. Satın alma, tek seferlik ödeme gerektirirken, abonelikler düzenli olarak ücret ödemeleri gerektirir. Spwig, bu iki modelin yönetimi için ayrı ayrı sistemler sunar.

### Satın Alma ve Aboneliklerin Kullanım Alanları

Satın alma ve abonelikler, kullanıcıların ürünleri satın almak ve hizmetlere erişmek için kullandığı iki farklı ödeme modelidir. Satın alma, tek seferlik ödeme gerektirirken, abonelikler düzenli olarak ücret ödemeleri gerektirir. Spwig, bu iki modelin yönetimi için ayrı ayrı sistemler sunar.