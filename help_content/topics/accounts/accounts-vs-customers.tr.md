---
title: Hesaplar vs. Müşteriler
---

Satıcılar sık sık sorar: "Bir hesap ve bir müşteri arasındaki fark nedir?" Bu karışıklık yaygın çünkü her müşteri bir hesaptır, ancak her hesap bir müşteri değildir. Bu kılavuz, farkı açıklar ve her admin arayüzünün ne zaman kullanılacağını açıklar.

![Kullanıcı Listesi](/static/core/admin/img/help/accounts-vs-customers/user-list.webp)

## Bir Hesap Nedir?

Bir **hesap**, Spwig'de merkezi kimlik doğrulama nesnesidir. Platformunuza giriş yapabilen herkes — çalışan veya müşteri — bir hesaba sahiptir. Hesaplar Spwig kimlik doğrulama sistemi tarafından yönetilir ve `User` modelinde saklanır.

Tüm hesaplarda:
- **E-posta adresi** — Temel kimlik belirteci ve oturum açma kimlik bilgisi
- **Kullanıcı adı** — Benzersiz bir kullanıcı adı (varsayılan olarak e-postadan otomatik olarak oluşturulur)
- **Şifre** — Hashlenmiş ve güvenli şekilde saklanır
- **is_staff bayrağı** — Hesabın yönetici arka uçuna erişip erişemeyeceğini belirler

Hesaplar ayrıca **Ayarlar > Kimlik Doğrulama** bölümünde yapılandırılmış OAuth sağlayıcıları (Google, Facebook vb.) aracılığıyla kimlik doğrulaması yapabilir.

## Bir Müşteri Nedir?

Bir **müşteri**, `is_staff=False` olan özel bir hesaptır. Müşteriler mağazanızda alışveriş yapar, sipariş verir ve profillerini yönetir. Her müşteri hesabı otomatik olarak genişletilir:

- **Müşteri Profili** — Tercihleri, haber bülteni aboneliği durumu ve özel alan değerlerini saklar
- **Müşteri Metrikleri** — Hayat boyu değer (LTV), RFM puanlarını, sipariş geçmişini ve segmentasyon verilerini izler
- **Sipariş Geçmişi** — Bu müşterinin verdiği tüm siparişlere bağlantı sağlar

Müşteriler olabilir:
- **Kayıtlı müşteriler** — Mağaza kaydı veya yönetici arayüzü üzerinden oluşturulmuş
- **Misafir kullanıcılar** — Misafir ödeme sırasında oluşturulan geçici hesaplar (kullanıcı adı `guest_` ile başlar)
- **İçe aktarılmış müşteriler** — CSV içeri aktarma ile diğer platformlardan geçirilmiş

## Ana Fark

| Özellik | Hesap | Müşteri |
|-----------|---------|----------|
| **Amaç** | Kimlik doğrulama ve yetkilendirme | Alışveriş, siparişler ve analiz |
| **Kapsam** | Çalışanlar ve müşteriler | Sadece müşteriler |
| **is_staff bayrağı** | True veya False | Her zaman False |
| **Genişletilmiş veri** | Yok (sadece çekirdek alanlar) | Müşteri Profili + Müşteri Metrikleri |
| **Yönetim konumu** | Ayarlar > Kullanıcılar | Müşteriler > Müşteri Profilleri |
| **Oturum açabilir** | Evet | Evet |
| **Sipariş verebilir** | Sadece CustomerProfile varsa | Evet |
| **Yönetici arayüzüne erişebilir** | Sadece is_staff=True ise | Hayır |

Kısaca:
- Bir **hesap**, oturum açabilen herkes için kullanılır
- Bir **müşteri**, alışveriş yapabilen ve sipariş verebilen bir hesaptır

## Çalışanlar da Hesaplardır

Çalışanlar, `is_staff=True` olan hesaplardır. Yönetici arka ucuna oturum açabilirler ve atanan **Çalışan Rolü** izinlerine göre eylemler yapabilirler.

Çalışanların isteğe bağlı olarak bir **Müşteri Profili** olabilir, eğer aynı zamanda mağaza ön yüzünde alışveriş yaparsa. Örneğin, kendi mağazanızda bir test siparişi verirseniz, çalışan hesabınız için bir Müşteri Profili oluşturulur. Bu, yönetici erişiminizi etkilemez.

Çalışan izinleri şu şekilde kontrol edilir:
- **Çalışan Rolü** — Çalışanın erişebileceği yönetici bölümlerini ve eylemleri tanımlar
- **is_superuser bayrağı** — Sınırsız erişim sağlar (dikkatli kullanın)

Çalışanları **Ayarlar > Çalışan Yönetimi** bölümünde yönetin.

## Misafir Kullanıcılar

Misafir ödeme, `guest_` ile başlayan otomatik olarak oluşturulan kullanıcı adlarıyla geçici hesaplar oluşturur. Bu hesaplarda:
- `is_staff=False` (onlar müşterilerdir)
- Bir Müşteri Profili vardır (sipariş ilişkilendirmesi için)
- Rastgele bir şifre vardır (misafir oturum açamaz, çünkü kayıtlı olmazsa)
- Varsayılan olarak müşteri analizlerinden hariç tutulurlar

Misafir kullanıcılar şu şekilde kayıtlı müşteriye dönüşebilir:
1. Aynı e-posta ile mağaza ön yüzünde bir hesap oluşturarak
2. E-posta adresini doğrulayarak
3. Sistem, misafir sipariş geçmişini yeni kayıtlı hesaba birleştirir

Misafir dönüş ayarlarını **Ayarlar > Ödeme > Misafir Ödeme** bölümünde yönetin.

## Her Birini Nerede Bulursunuz

| Yönetici Konumu | Ne Yönetiyorsunuz | Ana Kullanım Durumları |
|----------------|-----------------|---------------|
| **Ayarlar > Kullanıcılar** | Tüm hesaplar (çalışanlar + müşteriler) | Şifreleri sıfırla, hesapları etkinleştir / devre dışı bırak, çalışan izinlerini atayın |
| **Ayarlar > Çalışan Yönetimi** | Sadece çalışan hesaplar (is_staff=True) | Rol atama, ekip üyesi erişimini yönetme, izinleri yapılandırma |
| **Müşteriler > Müşteri Profilleri** | Sadece müşteri hesapları (is_staff=False) | Müşteri tercihlerini inceleyin, sipariş geçmişini, LTV, RFM puanlarını, segmentleri |
| **Müşteriler > Analiz** | Müşteri metrikleri ve segmentleri | Müşteri davranışlarını analiz etme, pazarlama segmentlerini oluşturma, tutumları izleme |

![Müşteri Profili Listesi](/static/core/admin/img/help/accounts-vs-customers/customer-profile-list.webp)

## Her Arayüzü Ne Zaman Kullanmalısınız

**Ayarlar > Kullanıcılar** arayüzünü kullanın:
- Bir müşterinin şifresini sıfırlamak için
- Tehdit altında olan bir hesabı devre dışı bırakmak için
- Manuel olarak bir müşteri hesabı oluşturmak için
- OAuth oturum açma bağlantılarını görmek için
- Tüm hesapları (çalışanlar + müşteriler) tek bir listede görmek için

**Ayarlar > Çalışan Yönetimi** arayüzünü kullanın:
- Yeni bir ekip üyesi eklemek için
- Bir çalışanın rolünü atamak veya değiştirmek için
- İnce taneli izinleri yapılandırmak için
- Çalışan etkinlik günlüklerini denetlemek için

**Müşteriler > Müşteri Profilleri** arayüzünü kullanın:
- Bir müşterinin sipariş geçmişini incelemek için
- Müşteri tercihlerini ve özel alan değerlerini görmek için
- Haber bülteni aboneliği durumunu kontrol etmek için
- Müşteri LTV ve RFM puanlarını incelemek için
- Müşteri segmentlerini yönetmek için

**Müşteriler > Analiz** arayüzünü kullanın:
- Yüksek değerli müşterileri tanımlamak için
- Pazarlama segmentleri oluşturmak için (örneğin, "90 günde sipariş vermemiş müşteriler")
- Müşteri yaşam boyu değer eğilimlerini analiz etmek için
- Kampanyalar için müşteri listelerini dışa aktarmak için

## İpuçları

- **Müşteri profilleri otomatik olarak oluşturulur** — Bir müşteri ilk siparişini (misafir veya kayıtlı) verdiğinde, Spwig analiz için bir Müşteri Profili ve Müşteri Metrikleri kaydı oluşturur.
- **Çalışanlar da müşteriler olabilir** — Eğer bir çalışan mağaza ön yüzünde bir sipariş verirse, bir Müşteri Profili alır. Bu normaldir ve yönetici erişimini etkilemez.
- **Misafir hesaplar kullanıcı listesini kirletir** — Gerçek ve etkileşimli müşterileri odaklanmak için müşteri profili arayüzünü kullanın. Kullanıcı listesi tüm misafir hesapları içerir.
- **is_staff=False ile segmentle** — E-posta kampanyaları için müşteri listesini dışa aktarırken, her zaman `is_staff=False` için filtreleme yapın, böylece ekip üyeleri dışlanır.
- **OAuth hesapları da hesaplardır** — Bir müşteri Google veya Facebook üzerinden oturum açarsa, Spwig bir hesap oluşturur ve onu OAuth profiline bağlar. E-posta alanı OAuth sağlayıcısından doldurulur.