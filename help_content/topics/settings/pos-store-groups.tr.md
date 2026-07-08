---
title: POS Mağaza Grupları
---

Mağaza grupları, ortak yapılandırmalara sahip birden fazla perakende konumunu organize eder. Her terminali ayrı ayrı yapılandırmak yerine, bölgelere, franşizalara veya konum türlerine göre terminal gruplarını oluşturun ve grup düzeyinde ayarlar uygulayın. Gruplar ayarların devralınmasını destekler—para birimi, dil, saat dilimi, fatura şablonları ve promosyonel içerik gruptan bireysel mağazalara aktarılır. Bu, çok konumlu satıcıların yönetimini basitleştirirken, gerekirse mağaza özelinde geçersiz kılma esnekliğini korur.

Birden fazla perakende konumu, franşizalar veya farklı operasyonel gereksinimlerle birlikte çalışan bölgesel pazarlarda çalışıyorsanız mağaza gruplarını kullanın.

![Mağaza Grup Listesi](/static/core/admin/img/help/pos-store-groups/storegroup-list.webp)

## Mağaza Grupları Nedir?

Mağaza grupları, ortak özelliklere sahip depolar ve terminal için organize konteynerlerdir:

**Ortak Gruplama Stratejileri**:
- **Coğrafi**: Kuzey Bölgesi, Güney Bölgesi, Batı Kıyısı, Doğu Kıyısı
- **Franşizalı**: Franşizör A Mağazaları, Franşizör B Mağazaları, Şirket Mağazaları
- **Format**: Galleri Konumları, Bağımsız Mağazalar, Pop-Up Mağazalar
- **Pazar**: Yerel Mağazalar, Avrupa Mağazaları, Asya Pasifik Mağazaları

Gruplar terminalin fiziksel operasyonunu değiştirmez—ölçekle yönetimini basitleştiren bir yapılandırma katmanı sağlar.

## Mağaza Gruplarını Ne Zaman Kullanmalısınız

**Tek Konum** - Gruplara gerek yok. Terminali doğrudan yapılandırın.

**2-3 Aynı Ayarlarla Konum** - Gruplar isteğe bağlıdır. Terminali doğrudan yapılandırmak daha kolay olabilir.

**4+ Konum** - Gruplar güçlü tavsiye edilir. Merkezi yapılandırma zaman kazandırır.

**Çok Ulusal İşlemler** - Gruplar zorunludur. Farklı para birimleri, diller ve saat dilimleri grup düzeyinde geçersiz kılma gerektirir.

**Franşizalı İşlemler** - Gruplar kritik. Her franşizör bağımsız ayarlara ihtiyaç duyarken marka tutarlılığını korumak gerekir.

## Ayarlar Devralma Hiyerarşisi

Spwig POS, 4 seviyeli ayarlar kaskadı (en yüksek öncelikten en düşük):

| Seviye | Öncelik | Örnek | Kullanım Durumu |
|--------|--------|-------|------------------|
| **Terminal** | 1 (En Yüksek) | Terminal 5, kağıt genişliğini 58mm olarak geçersiz kılar | Tek terminalin benzersiz yazıcı donanımı vardır |
| **Mağaza** | 2 | Mağaza 2, para birimini GBP olarak geçersiz kılar | ABD'deki çoğunlukla ABD mağazaları arasında UK konumu |
| **Grup** | 3 | Avrupa Grubu, saat dilimini CET olarak ayarlar | Birden fazla mağaza boyunca bölgesel tutarlılık |
| **Site** | 4 (En Düşük) | Küresel varsayılan: USD, İngilizce, UTC | Yapılandırılmamış tüm ayarlar için varsayılan |

**Nasıl Çalışır**:
- Sistem ilk olarak Terminal ayarlarını kontrol eder
- Ayarlanmamışsa, Mağaza ayarlarını kontrol eder
- Ayarlanmamışsa, Grup ayarlarını kontrol eder
- Ayarlanmamışsa, Site varsayılanlarını kullanır

**Örnek**:
- Site varsayılanı: Para birimi = USD, Dil = İngilizce
- Grup "Avrupa Mağazaları": Para birimi = EUR, Dil = ayarlanmamış
- Mağaza "Paris Flagship": Para birimi = ayarlanmamış, Dil = Fransızca
- Terminal "Paris Register 1": Para birimi = ayarlanmamış, Dil = ayarlanmamış

**Paris Register 1 için Sonuç**:
- Para birimi: EUR (Gruptan devralınır)
- Dil: Fransızca (Mağazadan devralınır)

Bu kaskad, gerekli yerlerde genel varsayılanlarla cerrahi geçersiz kılmaları sağlar.

## Mağaza Grubu Oluşturma

**POS > Mağaza Grupları**'na gidin ve **+ Mağaza Grubu Ekle**'ye tıklayın:

![Mağaza Grubu Ekleme Formu](/static/core/admin/img/help/pos-store-groups/storegroup-add-form.webp)

### Temel Yapılandırma

**Grup Adı** - Açıklamalı etiket (örneğin, "Batı Kıyısı Mağazaları", "Avrupa Franşizaları", "Galleri Konumları")

**Kod** - Kısa ve benzersiz bir tanımlayıcı (örneğin, "WEST", "EUR", "MALL"):
- İçinde kullanılır
- Tüm gruplar arasında benzersiz olmalıdır
- 2-10 karakter, alfanümerik
- Tutarlılık için büyük harf önerilir

**Sıra Numarası** - Yönetici listelerindeki görüntü sırasını kontrol eder (düşük numaralar önce görünür):
- 10, 20, 30 gibi 10'un katlarını kullanın (mevcut gruplar arasında yeni grup eklemeyi sağlar)
- Grupları mantıklı şekilde organize etmeye yardımcı olur (coğrafi sıralama, boyut sıralaması vb.)

### Bölgesel Geçersiz Kılma

**Para Birimi Geçersiz Kılma** - Site varsayılanından farklı bir grup düzeyi para birimi ayarlayın:
- Örnek: Avrupa grubu EUR kullanır, Asya Pasifik grubu JPY kullanır
- Bu gruptaki terminaler bu para birimine varsayılan olarak ayarlanır
- Fiyat gösterimi, nakit dengeleme, raporlar üzerinde etkili

**Dil Geçersiz Kılma** - Site varsayılanından farklı bir grup düzeyi dil ayarlayın:
- Örnek: Fransız mağazaları Fransızca kullanır, Alman mağazaları Almanca kullanır
- POS arayüz dilini, fatura dilini (şablon destekliyorsa) etkiler
- Personel, bu dilde grup terminaline giriş yaparken POS arayüzünü görür

**Saat Dilimi Geçersiz Kılma** - Site varsayılanından farklı bir grup düzeyi saat dilimini ayarlayın:
- Örnek: Batı Kıyısı mağazaları America/Los_Angeles kullanır, Avrupa mağazaları Europe/Paris kullanır
- Vardiyaların zaman damgalarını, rapor planlamasını, promosyon kaydırması planlamasını etkiler
- Yerel iş saatleriyle uyumlu vardiyaların raporlarını sağlar

**Ne Zaman Geçersiz Kılma Yapılmalı**:
- **Para birimi**: Uluslararası konumlarda her zaman geçersiz kılma (farklı ödeme para birimleri)
- **Dil**: Yabancı dillerde konuşulan pazarlarda geçersiz kılma (müşteri odaklı içerik)
- **Saat dilimi**: Site varsayılanından 2 saatten fazla uzakta olan konumlarda geçersiz kılma (yerel zaman damgaları)

## Depoları Gruplarla Bağlama

Grup oluşturduktan sonra depoları ona atayın:

1. **Katalog > Depolar**'a gidin
2. Bir mağaza konumunu temsil eden depoyu düzenleyin
3. **Mağaza Grubu** alanını oluşturduğunuz gruba ayarlayın
4. Kaydedin

Bu depoya atanan tüm terminaler artık grubun ayarlarını devralır.

**Örnek Kurulum**:
- Grup oluşturun: "Avrupa Mağazaları" (Para birimi: EUR, Dil: ayarlanmamış, Saat dilimi: CET)
- Depolar oluşturun: "Paris Mağazası", "Berlin Mağazası", "Roma Mağazası"
- Tüm 3 depoyu "Avrupa Mağazaları" grubuna atayın
- Terminal oluşturun: "Paris Register 1", "Berlin Register 1", "Roma Register 1"
- Her terminal, gruptan EUR para birimi ve CET saat dilimini devralır
- Dil, mağaza düzeyinde geçersiz kıl: Paris=Fransızca, Berlin=Almanca, Roma=İtalyanca

## Gruplar Tarafından Kontrol Edilen Ayarlar

Gruplar bu ayarları geçersiz kılabilir:

**İşlem Ayarları**:
- Para birimi (fiyat gösterimi ve nakit dengeleme üzerinde etkili)
- Dil (POS arayüz dilini etkiler)
- Saat dilimi (zaman damgalarını ve planlamayı etkiler)

**İçerik Ayarları** (kapsamlı modeller aracılığıyla):
- Fatura şablonları (grup özel fatura tasarımları oluşturun)
- Promosyon kaydırması (belirli gruplara yönelik promosyonlar)

**Gruplar Tarafından Kontrol Edilmeyen**:
- Terminal donanım yapılandırması (terminal bazında yapılandırılır)
- Personel atamaları (terminal bazında yapılandırılır)
- Depo stok seviyeleri (depo bazında yapılandırılır)
- Ödeme sağlayıcı hesapları (site genelinde veya sağlayıcı bazında yapılandırılır)

## Gerçek Dünya Örnekleri

### Örnek 1: Uluslararası Mod Perakendeçisi

**Kurulum**:
- 5 ülkeye yayılmış 50 mağaza
- Her ülke farklı para birimi, dil ve vergi gereksinimlerine sahiptir

**Grup Yapısı**:
- Grup: "ABD Mağazaları" (USD, İngilizce, America/New_York)
  - 20 depo (NY, LA, Chicago vb.)
  - 60 terminal
- Grup: "İngiltere Mağazaları" (GBP, İngilizce, Europe/London)
  - 10 depo (Londra, Manchester vb.)
  - 30 terminal
- Grup: "AB Mağazaları" (EUR, ayarlanmamış, Europe/Paris)
  - 15 depo (Paris, Berlin, Roma vb.)
  - 45 terminal
  - Dil, mağaza düzeyinde geçersiz kıl (Paris=Fransızca, Berlin=Almanca, Roma=İtalyanca)
- Grup: "Japonya Mağazaları" (JPY, Japonca, Asia/Tokyo)
  - 5 depo (Tokyo, Osaka vb.)
  - 15 terminal

**Avantajlar**:
- Her pazarın tüm mağazalarına uyan bir grup yapılandırması
- Gruplara özel fatura şablonları (AB için vergi formatı, ABD için satış vergisi)
- Bölgesel promosyon kaydırması (ABD: Memorial Day Satış, AB: Yaz Tatili Satış)

### Örnek 2: Kahve Çubuğu Zinciri

**Kurulum**:
- 30 konum, aynı ülke, ancak farklı formlar

**Grup Yapısı**:
- Grup: "Galleri Konumları" (ayarlanmamış, ayarlanmamış, ayarlanmamış)
  - 10 galleri tabanlı mağaza
  - 9pm'a kadar açık promosyon kaydırması
  - Galleri park doğrulama QR kodu ile fatura şablonu
- Grup: "Bağımsız Mağazalar" (ayarlanmamış, ayarlanmamış, ayarlanmamış)
  - 15 sokak önündeki mağazalar
  - Standart saat promosyon kaydırması
  - Standart fatura şablonu
- Grup: "Havaalanı Konumları" (ayarlanmamış, ayarlanmamış, ayarlanmamış)
  - 5 havaalanı mağazası
  - 24 saatlik promosyon kaydırması
  - Uçuş bilgisi QR kodu entegrasyonu ile fatura şablonu

**Avantajlar**:
- Farklı formlar için farklı promosyon içerikleri
- Konuma özel fatura özelleştirmeleri
- Yönetim basitleştirildi (grup güncellemek yerine 10 bireysel mağazayı güncellemek yerine)

### Örnek 3: Franşizalı İşletme

**Kurulum**:
- 100 mağaza, 20 farklı franşizör

**Grup Yapısı**:
- Grup: "Franşizör A" (ayarlanmamış, ayarlanmamış, ayarlanmamış)
  - Franşizör A tarafından işletilen 10 mağaza
  - Franşizör A'nın iletişim bilgisi faturalarda (grup fatura şablonu aracılığıyla)
  - Franşizör A'nın promosyon içeriği (yerel etkinlikler, özel teklifler)
- Grup: "Franşizör B" (ayarlanmamış, ayarlanmamış, ayarlanmamış)
  - Franşizör B tarafından işletilen 8 mağaza
  - Franşizör B'nin iletişim bilgisi faturalarda
  - Franşizör B'nin promosyon içeriği
- (Tüm franşizörler için tekrar edin)
- Grup: "Şirket Mağazaları" (ayarlanmamış, ayarlanmamış, ayarlanmamış)
  - Şirket sahibi 5 mağaza
  - Şirket markalama ve promosyonları

**Avantajlar**:
- Her franşizör kendi grup ayarlarını yönetebilir
- Şirket varsayılanları aracılığıyla marka tutarlılığı korunur
- Franşizör bağımsızlığı grup geçersiz kılmaları aracılığıyla korunur

## Grup Ayarlarını Yönetme

**Grup Ayarlarını Değiştirme**, gruptaki tüm terminalleri etkiler:
- Para birimi değişikliği: Grup terminali yeni para birimine geçer, bir sonraki senkronizasyonda
- Dil değişikliği: Grup terminali yeni dile geçer, bir sonraki senkronizasyonda
- Saat dilimi değişikliği: Grup terminali zaman damgalarını yeniden hesaplar, bir sonraki senkronizasyonda

**Etki Dikkate Alma**:
- Grup genelinde değişiklik yapmadan önce tek bir terminalde test edin
- Personellere yaklaşan değişiklikleri bildirin (örneğin, dil geçişleri)
- Değişiklikleri yoğunluk saatlerinin dışında planlayın, disruptionu minimize edin

**Grup Silme**:
- Tüm depoları başka bir gruba atayın veya grup atamasını kaldırın
- Terminal grup düzeyinde ayarları kaybeder ve site varsayılanlarına geri döner
- Depolar hala atamalıysa grup silinemez

## İpuçları

- **Anlamlı kodlar kullanın** - "WEST", "GRP1"'den daha net bir yapılandırma incelemesi için
- **Gruplar oluşturmadan önce hiyerarşiyi planlayın** - Organizasyonel yapınızı önce düşünün; daha sonra yeniden yapılandırma zahmetli olur
- **Bir terminal ile grup ayarlarını test edin** - 50 depoyu bir gruba atamadan önce, bir terminal ile grup ayarlarını test edin
- **Mağaza düzeyinde geçersiz kılmaları az kullanın** - Çok fazla mağaza düzeyinde geçersiz kılmalar grupların amacını mahvetmez
- **Grup amaçlarını belgeleyin** - Grup adında bu grubun neyi farklı kıldığını not alın (coğrafi, format, franşizör)
- **Sıra numarasını stratejik olarak kullanın** - Önem sırasına göre grupları sıralayın (Şirket Mağazaları önce) veya coğrafi sıraya göre (Batı'dan Doğu'ya) daha kolay navigasyon için
- **Grup sayısını akıllıca tutun** - 20+ grup, aşırı segmentasyonu gösterir; konsolidasyonu göz önünde bulundurun
- **Para birimi geçersiz kılmaları kalıcıdır** - İşletme sırasında bir grubun para birimini değiştirmek muhasebe işlemini zorlaştırır; dikkatli planlayın

