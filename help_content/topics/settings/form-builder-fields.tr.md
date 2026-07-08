---
title: Form Builder Alanları ve Doğrulama
---

Form alanları, formlarınızın temel taşlarıdır — her alan, kullanıcılardan bir veri parçası toplar. Form Builder, basit metin girdilerinden ileri düzey puanlama ölçeklerine ve ürün seçicilerine kadar 22 farklı alan türü sunar. Alanları etiketlerle, doğrulama kurallarıyla, yardım metniyle ve koşullu mantıkla yapılandırarak, kullanıcı yanıtlarına göre uyarlanabilen dinamik formlar oluşturun. Alanlar zorunlu veya isteğe bağlı olabilir, regex desenleriyle doğrulanabilir ve özel CSS sınıflarıyla stillenebilir.

Bu kılavuzu, tüm mevcut alan türlerini, her birinin ne zaman kullanılacağı ve doğrulama ve koşullu mantığı nasıl yapılandırılacağı hakkında anlayabilmek için kullanın.

## Alan Yapılandırma Temelleri

Her alan, aşağıdaki ortak ayarlara sahiptir:

**Kimlik**:
- **Alan Adı** - Veri depolama için makine adı (boşluk olmamalı, alt çizgi kullan: `email_address`)
- **Alan Türü** - Girdi davranışını ve işleme şeklini belirler
- **Aşama Ataması** - Bu alanı hangi aşamaya ait olduğunu belirtir (çok aşamalı formlar için sadece)

**Gösterim**:
- **Etiket** - Kullanıcılara gösterilen soru veya ipucu (örneğin, "E-posta adresiniz nedir?")
- **Yer tutucu** - Girdi içindeki ipucu metni (örneğin, "you@example.com")
- **Yardım Metni** - Alanın altındaki ekstra yönlendirme (örneğin, "E-postanızı asla paylaşmayız")
- **Varsayılan Değer** - Kullanıcıların değiştirebileceği önceden doldurulmuş değer

**Düzen**:
- **Genişlik** - Form genişliğinin tamamı (100%), yarısı (50%) veya üçte biri (33%)
- **CSS Sınıfı** - Özel tasarım için ekstra stillendirme sınıfları
- **Sıra** - Aşamadaki konum (sürükleme ile sırala)

**Doğrulama**:
- **Zorunlu** - Zorunluluk durumunu aç/kapa (etiket üzerine kırmızı yıldız görünür)
- **Min/Max Uzunluk** - Karakter sınırları (metin alanları için)
- **Min/Max Değer** - Sayısal sınırlar (sayı alanları için)
- **Doğrulama Deseni** - Karmaşık doğrulama için özel regex
- **Hata Mesajı** - Doğrulama başarısız olduğunda gösterilen özel metin

## Metin Girdi Alanları

**Tek Satır Metin** (`text`):
- Kısa yanıtlar için temel metin girişi
- Doğrulama: min/max uzunluk, regex deseni
- Kullanım durumu: İsimler, adresler, ürün kodları, kısa yanıtlar
- Örnek: "Tam Ad", "Sokak Adresi", "Şirket Adı"

**Çok Satır Metin** (`textarea`):
- Uzun içerik için genişletilebilir metin alanı (3-10 satır)
- Doğrulama: min/max uzunluk
- Kullanım durumu: Yorumlar, geri bildirimler, detaylı açıklamalar, mesajlar
- Örnek: "Deneyiminizi bize anlatın", "Ek notlar"

**E-posta Adresi** (`email`):
- E-posta özel doğrulama ("@" ve alan adı gerekli)
- Mobil klavyelerde "@" tuşu öne çıkar
- Kullanım durumu: İletişim e-postası, bülten aboneliği, hesap oluşturma
- Örnek: "E-posta Adresi", "İş E-postası"

**Telefon Numarası** (`phone`):
- Telefon numaralarını otomatik olarak biçimlendirir
- Mobil klavyelerde sayısal düzen gösterir
- Doğrulama: yapılandırılabilir desen (uluslararası formatlar desteklenir)
- Kullanım durumu: İletişim telefonu, acil durum iletişim, randevu planlama
- Örnek: "Telefon Numarası", "Mobil", "İletişim Numarası"

**Sayı** (`number`):
- Arttırma/azaltma kontrolleriyle sayısal girdi
- Doğrulama: min/max değer, artış adımı
- Yanıtlarda sayı (dize değil) döndürür
- Kullanım durumu: Miktarlar, yaşlar, deneyim yılları, bütçe miktarları
- Örnek: "Kaç çalışanınız var?", "Yaşınız", "İş hayatında kaç yıldır?"

**URL** (`url`):
- URL doğrulama (http:// veya https:// gerekli)
- Mobil klavyelerde ".com" tuşu gösterir
- Kullanım durumu: Web sitesi, LinkedIn profili, portfölyo bağlantısı
- Örnek: "Şirket Web Sitesi", "Portfölyo URL'si"

## Seçim Alanları

**Aşağıdaki Seçenekler** (`select`):
- Aşağıdaki menüden tek bir seçenek seçimi
- Yapılandırma: {value, label} seçeneklerinin dizisi
- Varsayılan seçim destekler
- Kullanım durumu: Kategoriler, durumlar/ülkeler, durum seçimi
- Örnek: "Ülkenizi seçin", "Departman", "Bizi nasıl duydunuz?"
- En iyi kullanım: 5+ seçenek (daha az seçenek için radyo kullanın)

**Radyo Butonları** (`radio`):
- Görünen tüm seçeneklerden tek bir seçim
- Yapılandırma: {value, label} seçeneklerinin dizisi
- 2-4 seçenek için select'ten daha iyi kullanıcı deneyimi
- Kullanım durumu: Evet/hayır soruları, cinsiyet, az sayıda seçenekle tercihler
- Örnek: "Bizi önerir misiniz?", "Tercih edilen iletişim yöntemi"


- Tekli anahtar checkbox (açık/kapalı)
- Yanıtlarda true/false döndürür
- Kullanım alanı: Şartlar kabulü, anlaşmalar, tek tercih
- Örnek: "Şartlar ve koşulları kabul ediyorum", "Bültenimize abone olun"

- Seçeneklerden çoklu seçim (kullanıcılar 0, 1 veya birçok seçebilir)
- Yapılandırma: {value, label} seçeneklerinin dizisi
- Seçilen değerlerin dizisini döndürür
- Kullanım alanı: Çoklu seçim tercihleri, ilgi alanları, gerekli özellikleri
- Örnek: "Hangi konuları ilgilendiriyor?", "Uygun olanları seçin"

## Değerlendirme Alanları

- Görsel yıldızlı değerlendirme ölçeği (genellikle 1-5 yıldız)
- Yapılandırma:
  - `max_stars`: 3-10 yıldız (varsayılan: 5)
  - `allow_half`: yarım yıldız değerlendirmesi için true/false
  - `icon`: fa-star (varsayılan) veya fa-heart
  - `color`: ondalık renk kodu (varsayılan: #FFD700 altın)
- Kullanım alanı: Ürün değerlendirmeleri, hizmet kalitesi, memnuniyet puanları
- Örnek: "Deneyiminizi değerlendirin", "Hizmetimiz nasıl oldu?"

- İfade değerlendirme ölçeği: "Şiddetle katılmam" → "Şiddetle katılıyorum"
- Yapılandırma:
  - `scale_type`: 5_point (1-5) veya 7_point (1-7)
  - `labels`: uç nokta metnini özelleştir (sol: "Şiddetle katılmam", sağ: "Şiddetle katılıyorum")
- Sayısal değer döndürür (1-5 veya 1-7)
- Kullanım alanı: Anket ifadeleri, katılım ölçekleri, duygusal ölçüm
- Örnek: "Ürün, ihtiyaçlarımı karşılıyor", "Müşteri hizmeti yardımcı oldu"

- 0-10 ölçeği: "Hiç olasılık yok" ile "Çok olasılık var"
- Yapılandırma:
  - `low_label`: sol uç nokta metni (varsayılan: "Hiç olasılık yok")
  - `high_label`: sağ uç nokta metni (varsayılan: "Çok olasılık var")
- 0-10 değerini döndürür (0-6 = düşmanlar, 7-8 = pasifler, 9-10 = destekçiler)
- Kullanım alanı: NPS anketleri, önerme olasılığı, sadakat ölçümü
- Örnek: "Bizi bir arkadaşa önerme olasılığınız nedir?"

## Gelişmiş Alanlar

- Tekli veya çoklu dosya yükleme
- Yapılandırma:
  - `max_size_mb`: dosya başına dosya boyutu sınırı (varsayılan: 5MB)
  - `allowed_types`: uzantıların dizisi (örneğin, ["pdf", "doc", "docx", "jpg", "png"])
  - `max_files`: maksimum dosya sayısı (1 tekli, 2+ çoklu)
- Yanıtlarda dosya yolu(ları) döndürür
- Dosyalar /media/form_uploads/{form-slug}/ içinde saklanır
- Kullanım alanı: Özgeçmiş yükleme, belge gönderimi, fotoğraf ekleme
- Örnek: "Özgeçmişinizi yükleyin", "Destekleyici belgeleri ekleyin"

- Ürün kataloğundan çoklu seçim
- Yapılandırma:
  - `category_filters`: belirli kategorilere sınırla (kategori ID'lerinin dizisi)
  - `max_selections`: 1 tek ürün için, 2+ çoklu için
  - `display_mode`: "list" (varsayılan) veya "grid" (küçük resimlerle)
- Yanıtlarda ürün ID'leri/SKU'ları döndürür
- Kullanım alanı: Ürün önerileri, istek listeleri, geri bildirim anketleri, paketler
- Örnek: "Hangi ürünleri ilgilendiriyor?", "Tercih ettiğiniz ürünleri seçin"

- Tarih seçici arayüzü (takvim popup)
- Yanıtlarda ISO formatında döndürür (YYYY-MM-DD)
- Doğrulama: min/max tarih
- Kullanım alanı: Doğum tarihleri, etkinlik tarihleri, randevu planlama, vade tarihleri
- Örnek: "Doğum Tarihi", "Tercih Edilen Randevu Tarihi"

- Saat seçici (saat ve dakika)
- Yanıtlarda ISO saat formatında döndürür (HH:MM)
- Kullanım alanı: Randevu saatleri, kullanılabilirlik pencereleri
- Örnek: "Tercih Edilen Saat", "Sonrası Kullanılabilir"

- Birlikte tarih ve saat seçici
- Yanıtlarda tam ISO tarih saatini döndürür
- Kullanım alanı: Etkinlik planlama, randevu rezervasyonu
- Örnek: "Etkinlik Başlangıç Zamanı", "Teslimat Penceresi"

## Düzenleme Alanları (Giriş Olmayan)

- Form bölümlerini organize etmek için başlık metni
- Yapılandırma: başlık seviyesi (h2, h3, h4)
- Veri toplama yok
- Kullanım alanı: Uzun formları mantıklı bölümlere ayırma
- Örnek: "Kişisel Bilgiler", "İletişim Detayları", "Tercihler"

**Açıklamalı Paragraf** (`paragraph`):\n- Talimatlar veya bilgi için zengin metin bloğu\n- Veri toplama yok\n- Temel biçimlendirme desteği (kalın, italik, bağlantılar)\n- Kullanım senaryosu: Adım talimatları, yasal uyarılar, açıklamalar\n- Örnek: Gizlilik politikası bildirimi, GDPR onayı açıklaması\n\n**Ayırıcı Çizgi** (`divider`):\n- Görsel yatay çizgi ayırıcı\n- Veri toplama yok\n- Kullanım senaryosu: Bölümler arası görsel organizasyon\n\n**Gizli Alan** (`hidden`):\n- Programatik değerle gizli alan\n- Yapılandırma: `default_value` (zorunludur)\n- Kullanıcılara etiket veya yardım metni gösterilmez\n- Kullanım senaryosu: UTM parametreleri, izleme verileri, oturum kimlikleri, referans kodları\n- Örnek: URL parametresinden değer alan gizli alan\n\n## Alan Doğrulama Kuralları\n\n**Zorunlu Alanlar**:\n- Alan ayarlarında \"Zorunlu\" onay kutusunu seçin\n- Etiketin yanına kırmızı yıldız (*) görünür\n- Gerekli alanlar boş bırakılırsa form gönderilemez\n- Özel hata: \"Bu alan zorunludur\" (veya özel mesaj)\n\n**Min/Max Uzunluk** (metin alanları):\n- Minimum karakter sayısını ayarlayın: çok kısa yanıtları önler\n- Maksimum karakter sayısını ayarlayın: aşırı girdiyi önler\n- Örnek: Mesaj alanı en az 10 karakter gerektirir (\"tamam\" yanıtlarını önler)\n\n**Min/Max Değer** (sayı alanları):\n- Minimum sayısal değeri ayarlayın: negatif yaşlar, miktarlar gibi değerleri önler\n- Maksimum sayısal değeri ayarlayın: mantıklı aralığa sınırlar\n- Örnek: Yaş alanı en az 18, en fazla 120\n\n**Doğrulama Deseni** (regex):\n- Karma doğrulama için özel düzenli ifade\n- Yaygın desenler:\n  - ZIP kodu: `^\\d{5}(-\\d{4})?$` (ABD formatı)\n  - Telefon: `^\\(\\d{3}\\) \\d{3}-\\d{4}$` (ABD formatı)\n  - Ürün kodu: `^[A-Z]{2}\\d{4}$` (2 harf, 4 rakam)\n- Desen kullanıldığında özel hata mesajı gerekir\n\n**Dosya Doğrulama**:\n- Maksimum dosya boyutu: büyük yüklemeleri önler (varsayılan 5MB)\n- İzin verilen türler: belirli uzantıları beyaz liste yapma (güvenlik)\n- Örnek: Özgeçmiş alanı, ["pdf", "doc", "docx"], maksimum 2MB\n\n## Koşullu Mantık\n\nKullanıcı yanıtına göre alanların görünmesi/gizlenmesiyle dinamik formlar oluşturun:\n\n**Koşullu Kurallar Nasıl Çalışır**:\n1. Kullanıcı \"kaynak alan\" (tetikleyici) olarak yanıt verir\n2. Sistem kuralı değerlendirir: operatör + karşılaştırma değeri\n3. Koşul doğruysa eylem çalışır (alan veya adım göster/gizle/zorunlu yap)\n4. Birden fazla kural kaskadı olabilir (kural A, kural B'yi tetikler)\n\n**Kullanılabilir Operatörler**:\n- **Eşittir** (`equals`): tam eşleşme (örneğin, ülke \"US\" eşittir)\n- **Eşit Değildir** (`not_equals`): değerden farklı her şey\n- **İçerir** (`contains`): metin alt dize içerir (küçük/büyük harfe duyarlı değil)\n- **Daha Büyük** (`greater_than`): sayısal karşılaştırma (örneğin, yaş > 18)\n- **Daha Küçük** (`less_than`): sayısal karşılaştırma (örneğin, puan < 3)\n- **Boş** (`is_empty`): alanın değeri yok\n- **Boş Değil** (`is_not_empty`): alanın herhangi bir değeri var\n- **Listede** (`in_list`): değer ["Seçenek1", "Seçenek2"]'den biri\n\n**Kullanılabilir Eylemler**:\n- **Alanı Göster** - Gizli alanı göster\n- **Alanı Gizle** - Alanı gizle (gizlenirse değer temizlenir)\n- **Alanı Zorunlu Yap** - Alanı zorunlu yap\n- **Alanı Zorunlu Yapma** - Alanı isteğe bağlı yap\n- **Değeri Ayarla** - Alanı bir değere doldur\n- **Adımı Göster** - Gizli adım göster (çok adımlı sadece)\n- **Adımı Gizle** - Adımı gizle (çok adımlı sadece)\n- **Adıma Atla** - Belirli adıma atla (çok adımlı sadece)\n\n**Örnek Kurallar**:\n- EĞER `contact_method` EŞİTSE \"phone\" OLUŞTUR `phone_number` alanı göster\n- EĞER `rating` 3'TEN KÜÇÜKSE `improvement_feedback` alanını zorunlu yap\n- EĞER `country` ["US", "CA"] LİSTESİNDESE `shipping_details` adımını göster\n- EĞER `budget` 10000'DEN BÜYÜKSE `enterprise_features` alanını göster\n\n**Koşullu Kurallar Oluşturma**:\n1. Sağ panelde \"Koşullu Kurallar\" sekmesine tıklayın\n2. \"Kural Ekle\"ye tıklayın\n3. Kaynak alanı (tetikleyici) seçin\n4. Operatör (karşılaştırma şekli) seçin\n5. Karşılaştırma değeri (karşılaştırılacak şey) girin\n6. Eylem (ne yapılacağı) seçin\n7. Hedef (etkilenen alan veya adım) seçin\n8. Opsiyonel: Öncelik ayarlayın (daha yüksek öncelikli kurallar önce değerlendirilir)\n9. Kuralı kaydedin

**Kural Önceliği**:
- Daha yüksek sayılar önce değerlendirilir (öncelik 100, öncelik 10'dan önce)
- Kural çakışmaları veya kaskad durumlarında önceliği kullanın
- Örnek: Kural A (öncelik 100) alan gösterir, Kural B (öncelik 50) onu zorunlu kılar (A önce çalışır, sonra B)

## Sık Kullanılan Alan Desenleri

**İletişim Formu**:
- Tam Ad (metin, zorunlu)
- E-posta (e-posta, zorunlu)
- Telefon (telefon)
- Konu (seçim, seçenekler: "Satış", "Destek", "Ortaklık")
- Mesaj (metin alanı, zorunlu, en az 10 karakter)

**Ürün Geri Bildirimi**:
- Ürün (ürün_seçimi, tek seçim)
- Genel Değerlendirme (yıldız_değerlendirme, 5 yıldız)
- Koşullu: EĞER değerlendirme < 3 İSE "Ne geliştirebiliriz?" (metin alanı) zorunlu kılar
- Öneri (nps_değerlendirme)

**İş Başvurusu**:
- Adım 1: Kişisel (ad, e-posta, telefon)
- Adım 2: Özgeçmiş (dosya yükleme, izin verilen ["pdf", "doc"], maks 2MB)
- Adım 3: Uygunluk (başlangıç tarihi, iş günleri için kutu grubu)
- Koşullu: EĞER "years_experience" > 5 İSE "leadership_experience" alanını göster

## İpuçları

- **Uygun alan türlerini kullanın** - E-posta alanını e-postalar için kullanın (metin değil), doğrulama ve daha iyi mobil klavye sağlar
- **Etiketleri kısa tutun** - Ayrıntılar için yardım metnini kullanın, etiketlerde değil
- **İlgili alanları gruplayın** - Görünüm organizasyonu için başlıklar ve ayırıcılar kullanın
- **Doğrulamayı test edin** - Formu önizleyin ve geçersiz veri ile göndermeye çalışın
- **Dosya yükleme boyutlarını sınırlayın** - 5MB maksimum, büyük dosyaların sunucuyu aşırı yükleme riskini önler
- **Koşullu mantığı az kullanın** - Çok fazla kural kullanıcıları karıştırır; formları basit tutun
- **Gerçekçi maksimum değerler belirleyin** - Yaş maksimum 120, miktar maksimum 100 (1000 gibi yanlış yazım riskini önler)
- **Desen örnekleri sağlayın** - Regex doğrulama kullanıyorsanız, yardım metninde örnek gösterin
- **Açıkça zorunlu alanları belirleyin** - İletişim formlarında Ad ve e-posta her zaman zorunludur
- **2-4 seçenek için radyo kullanın** - 5+ seçenek için açılır menü kullanın (kullanıcı deneyimini artırır)
- **Kısa girdiler için yarım genişlik alanları kullanın** - Telefon ve ZIP kodu yarım genişlikte olabilir, dikey alanı tasarruf eder
- **İstek listeleri için ürün seçicileri kullanın** - Müşterilerin öneriler için birden fazla ürün seçmesine izin verin