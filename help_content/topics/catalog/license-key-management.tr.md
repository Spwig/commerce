---
title: Lisans Anahtar Yönetimi
---

Lisans anahtar yönetimi, dijital ürünler satın aldığında lisans anahtarlarının nasıl oluşturulduğunu, saklandığını ve müşterilere nasıl teslim edileceğini kontrol etmenizi sağlar. Spwig, yerleşik anahtar oluşturma, önceden yüklü anahtar havuzları ve harici lisans yönetimi hizmetleriyle entegrasyonları destekler.

## Genel Bakış

Spwig'de lisans anahtarlarını yönetmenin üç yolu vardır:

| Yöntem | En iyi durumlar |
|--------|---------|
| **Lisans şablonları** | Satın alma sırasında özel bir formatta benzersiz anahtarları otomatik olarak oluşturmak için |
| **Lisans havuzları** | Toplu dağıtım için önceden bir anahtar topluluğu oluşturmak için |
| **Harici sağlayıcılar** | Keygen.sh gibi bir üçüncü taraf hizmete lisans anahtarının oluşturulmasını ve yönetimini devretmek için |

Bu yöntemler birlikte kullanılabilir – örneğin, bir havuz özel bir şablon kullanarak anahtar formatını tanımlayabilir ve oluşturulan anahtarları bir harici sağlayıcıya senkronize etmek için isteğe bağlı olarak ayarlanabilir.

## Lisans Anahtar Şablonları

Bir lisans anahtar şablonu, oluşturulan anahtarların *formatını* tanımlar. Şablonlar, Spwig tarafından oluşturma zamanında doldurulan yer tutucularla bir desen kullanır.

### Şablon Oluşturma

1. **Katalog > Lisans Anahtar Şablonları**'na gidin
2. **+ Lisans Anahtar Şablonu Ekle**'ye tıklayın
3. **Ad** girin (örneğin, `Standart Uygulama Lisansı`)
4. Şablonu yer tutucularla yapılandırın (aşağıya bakın)
5. Gerekirse **Önek** ve **Son ek** ayarlayın (örneğin, `MYAPP` öneki her anahtarın başına `MYAPP-` ekler)
6. **Ayracı** karakterini seçin (varsayılan: `-`)
7. **Karakter Seti** ayarlayın – rastgele bölümler için kullanılan karakterler. Varsayılan, `0` ve `O`, `1` ve `I` gibi belirsiz karakterleri dışlar
8. Doğrulama için **Min/Max Uzunluk** ayarlayın
9. **Kaydet**'e tıklayın

### Yer Tutucular

| Yer Tutucu | Açıklama | Örnek Çıktı |
|-------------|-------------|---------------|
| `{RANDOM:N}` | Karakter setinden N rastgele karakter | `{RANDOM:5}` → `K7JXQ` |
| `{CHECKSUM:N}` | Doğrulama için N haneli kontrol toplamı | `{CHECKSUM:2}` → `47` |
| `{PREFIX}` | Şablonun önek değeri | `MYAPP` |
| `{SUFFIX}` | Şablonun son ek değeri | `PRO` |
| `{ORDER_ID}` | Sipariş numarası | `10045` |
| `{PRODUCT_SKU}` | Ürünün SKU'su | `SOFTPRO` |
| `{DATE:FORMAT}` | Biçimlendirilmiş tarih | `{DATE:YYMMDD}` → `260318` |

**Örnek desen**: `{PREFIX}-{RANDOM:5}-{RANDOM:5}-{RANDOM:5}-{CHECKSUM:2}`

Bu, `MYAPP-K7JXQ-M3TPR-9BWKN-47` gibi anahtarlar oluşturur.

### Anahtar Önizleme

Şablonu kaydettikten sonra, şablon listesinde **Örnek Anahtar Oluştur** işlemi kullanılabilir. Bu, şablonun beklenen formatta anahtarlar üretip üretmediğini doğrulamak için kullanılabilir. Şablonu bir ürüne atamadan önce bunu kullanın.

## Lisans Havuzları

Bir lisans havuzu, bir ürün için önceden oluşturulan bir anahtar topluluğudur. Havuzlar şu durumlarda faydalıdır:
- Fiziksel ambalaj (retail kutuları, basılı kartlar) için anahtarlara ihtiyaç duyuyorsanız
- Rekabetçi satıcılarla çalışıyorsanız ve toplu anahtarlar gerekliyse
- Anahtarların talep üzerine değil, önceden oluşturulmasını istiyorsanız

### Lisans Havuzu Oluşturma

1. **Katalog > Lisans Havuzları**'na gidin
2. **+ Lisans Havuzu Ekle**'ye tıklayın
3. Havuz detaylarını doldurun:

| Alan | Açıklama |
|-------|-------------|
| **Ad** | Açıklamalı bir ad (örneğin, `Retail Pack Q1 2026`) |
| **Ürün** | Bu anahtarların için olan ürün |
| **Lisans Şablonu** | Anahtar formatı için şablon (varsayılan olarak ürünün şablonu) |
| **Toplam Anahtar Sayısı** | Oluşturulacak anahtar sayısı |
| **Anahtar Türü** | Süresiz, abonelik veya deneme |
| **Maksimum Aktivasyonlar** | Her anahtarın kaç cihazda aktive edilebileceği |
| **Gün Sonra Süresi Bitiyor** | İlk aktivasyon sonrasında lisansın süresi bitmesine kadar geçen gün sayısı (boş bırakmak için süresiz olur) |
| **Havuz Süresi Bitiyor** | Bu havuzdan kullanılmayan anahtarların geçersiz hale gelmesi için tarih |
| **Sağlayıcıya Senkronize Et** | Oluşturulan anahtarları bir harici lisans sağlayıcısına isteğe bağlı olarak senkronize et |

4. **Kaydet**'e tıklayın – Spwig, anahtarları arka planda oluşturur

### Havuz Durumu

| Durum | Anlamı |
|--------|---------|
| **Oluşturuluyor** | Anahtarlar arka planda oluşturuluyor |
| **Hazır** | Tüm anahtarlar oluşturuldu ve dağıtım için hazır |
| **Tükendi** | Tüm anahtarlar siparişlere atanmış |
| **Süresi Dolmuş** | Havuzun son kullanma tarihi geçmiş |

### Havuzun Takibi

Havuz listesi, dağıtılan anahtar sayısının toplam oluşturulan anahtar sayısına karşı nasıl olduğunu gösterir. Bir havuzu açarak tüm anahtarların ve bireysel durumlarının listesine erişebilirsiniz.

## Dış Lisans Sağlayıcıları

Dış sağlayıcılar, anahtar oluşturma ve etkinleştirme takibini üstlenen üçüncü taraf lisans yönetimi hizmetleridir. Müşteri bir satın alma tamamladığında, Spwig sağlayıcı ile iletişim kurar ve anahtarı oluşturup kaydeder.

### Desteklenen Sağlayıcılar

| Sağlayıcı | Tür |
|----------|------|
| **Spwig Yerel Lisans Sunucusu** | Yerel — dış hesap gerekmez |
| **Keygen.sh** | Bulut tabanlı lisans yönetimi API'si |
| **LicenseSpring** | Kurumsal lisans yönetimi |
| **Cryptlex** | Çevrimdışı desteği olan lisans yönetimi |
| **Özel API** | Herhangi bir REST tabanlı lisans sistemi |

### Sağlayıcıyı Bağlama

1. **Katalog > Lisans Sağlayıcıları** menüsüne gidin
2. **+ Lisans Sağlayıcısı Ekle**'ye tıklayın
3. Sağlayıcı detaylarını doldurun:

| Alan | Açıklama |
|-------|-------------|
| **Ad** | Bu bağlantının etiketi (örneğin, `Keygen Üretim`) |
| **Sağlayıcı Türü** | Desteklenen sağlayıcılardan birini seçin |
| **API Uç Noktası** | Sağlayıcının API temel URL'si |
| **API Anahtarı** | Sağlayıcının kimlik doğrulama anahtarı |
| **API Gizli** | Sağlayıcı tarafından gerekliyse |

4. Senkronizasyon davranışını yapılandırın:
   - **Sipariş Üzerinden Senkronize** — Müşteri bir satın alma tamamladığında otomatik olarak senkronize edin
   - **Etkinleştirme Üzerinden Senkronize** — Cihaz etkinleştirmelerini sağlayıcıya bildirin
   - **Devre Dışı Alma Üzerinden Senkronize** — Devre dışı bırakmaları bildirin (lisans aktarımı ve iade için faydalıdır)
   - **İki Yönlü Senkronizasyon** — Sağlayıcının webhooks aracılığıyla Spwig kayıtlarını güncellemesine izin verin

5. **Kaydet**'e tıklayın, ardından **Bağlantıyı Test Et**'e tıklayarak kimlik bilgilerinin çalışıp çalışmadığını doğrulayın

### Bağlantı Durumu

Her sağlayıcı, üç bağlantı durumundan birini gösterir:

| Durum | Anlamı |
|--------|---------|
| **Test Edilmemiş** | Bağlantı henüz doğrulanmamış |
| **Bağlandı** | Son test başarılı oldu |
| **Hata** | Bağlantı testi başarısız oldu — hata mesajını kontrol edin |

### Mevcut Lisansları Senkronizasyon

Mevcut lisans anahtarlarını bir sağlayıcıya manuel olarak göndermek için (başlangıç ayarı veya başarısız senkronizasyon sonrası), sağlayıcı listesinden **Şimdi Senkronize Et** eylemini kullanın.

## Senkronizasyon Aktivitesini Takip Etme

**Katalog > Dış Lisans Senkronizasyonları** menüsüne giderek senkronizasyon günlük kaydını inceleyin. Her kayıt şu bilgileri gösterir:
- Senkronize edilen lisans anahtarı
- Anahtarın gönderildiği sağlayıcı
- Yön (Spwig → Sağlayıcı veya Sağlayıcı → Spwig)
- Durum (Beklemede, Başarılı, Başarısız)
- Başarısız senkronizasyonlar için hata detayları

Başarısız senkronizasyonlar otomatik olarak tekrar denenecektir. Ayrıca, kaydı düzenleyip hatayı temizleyerek bir tekrar deneme zorlayabilirsiniz.

## İpuçları

- Varsayılan karakter setini (`ABCDEFGHJKLMNPQRSTUVWXYZ23456789`) kullanın, müşterilerin sıkça yanlış okuyabileceği belirsiz karakterleri önlemek için — `0`, `O`, `1` ve `I` karakterlerini içermez.
- Şablon deseninize `{CHECKSUM}` segmentini ekleyin, böylece müşteriler ve destek ekibiniz hatalı yazılan anahtarları hızlıca tespit edebilir.
- Yüksek hacimli ürünler için, sipariş sırasında anahtarların anında teslim edilmesini sağlamak için havuz kullanın, talep üzerine üretim yerine.
- Mevsimsel veya zaman sınırlı anahtar toplulukları için **Havuz Süresi Bitiş Tarihi**'ni ayarlayın, böylece eski ve kullanılmayan anahtarlar otomatik olarak geçersiz hale gelir.
- Ayarlama sonrası ve herhangi bir kimlik bilgisi değişikliği sonrası her zaman sağlayıcı bağlantısını test edin — bozuk bir bağlantı, müşterilerin anahtarlarını alamamasına neden olur.
- İki yönlü senkronizasyon kullanıyorsanız, sağlayıcının webhook URL'sini mağazanızın lisans webhook uç noktasına yönlendirmek için yapılandırın.