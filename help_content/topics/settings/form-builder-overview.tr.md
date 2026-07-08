---
title: Form Builder Genel Bakış
---

Form Builder, veri toplamak için özel formlar oluşturur—temas formları, anketler, uygulamalar, kayıtlar ve daha fazlası. Görsel olarak sürükleyip bırakarak alanlarla formlar oluşturun, doğrulama kurallarını yapılandırın, çok adımlı iş akışlarını etkinleştirin ve detaylı analitiklerle yanıtları toplayın. Formlar, Sayfa Oluşturucu öğeleriyle tüm site üzerinde herhangi bir yerde gömülür. Tüm gönderiler, analiz ve dışa aktarma için tam meta verilerle (IP adresi, tarayıcı, tamamlanma süresi) veritabanında saklanır.

Form Builder'ı, müşterilerden yapılandırılmış veri toplamak gerektiğinde kullanın, basit temas bilgileri veya karmaşık çok sayfalı uygulamalar olsun.

## Form Builder Nedir?

Form Builder, kod olmadan özel formlar oluşturmak için görsel sürükleyip bırakma aracıdır:

**Desteklenen Form Türleri**:
- Temas formları (ad, e-posta, mesaj)
- Müşteri anketleri (puanlamalar, geri bildirim, NPS)
- Ürün kayıtları (garanti, destek)
- İş başvuruları (öge yükleme, çok adımlı)
- Etkinlik kayıtları (katılımcı bilgileri, tercihler)
- Hizmet talepleri (detaylı gereksinimler)
- Haberleşme listesi kaydı (tercihler için onay kutuları)

**Ana Özellikler**:
- **22 alan türü** - Metin, e-posta, telefon, dosya yükleme, puanlamalar, ürün seçicileri ve daha fazlası
- **Çok adımlı formlar** - Uzun formları mantıklı adımlara bölün ve ilerleme izleme ile
- **Koşullu mantık** - Kullanıcı yanıtına göre alanları göster/gizle
- **Doğrulama kuralları** - Gerekli alanlar, min/max uzunluk, özel regex desenleri
- **Spam koruma** - HoneyPot alanları veya Google reCAPTCHA v3
- **Yanıt analitiği** - Tamamlanma süresini, IP adresini, tarayıcıyı, refereri izleme
- **CSV dışa aktarma** - Excel/Google Sheets'te analiz için tüm yanıtları indirin
- **Çok dilli** - Form etiketlerini ve mesajlarını tüm etkin dillere çevirin

## İlk Formunuzu Oluşturma

**Ayarlar > Sayfalar > Formlar**'a giderek form yöneticisine erişin:

**Adım 1: Yeni Form Oluştur**
- **+ Yeni Form Oluştur**'a tıklayın
- Form adı girin (iç tanımlayıcı, müşterilere gösterilmez)
- Form başlığı girin (formun üstünde gösterilen başlık)
- Opsiyonel: Açıklama ekleyin (başlığın altına gösterilen yardım metni)

**Adım 2: Alanlar Ekle**
- **Form Tasarımını Düzenle**'ye tıklayarak görsel oluşturucuyu açın
- Sol kenar çubuğundan alan türlerini canvas'a sürükleyin
- Alanı tıklayarak sağ panelde yapılandırın
- Etiket, yer tutucu, yardım metni ayarlayın
- Gerekli durumunu aç/kapat
- Doğrulama kuralları ekleyin

**Adım 3: Form Ayarlarını Yapılandır**
- Gönder butonu metnini ayarlayın (varsayılan: "Gönder")
- Başarı mesajını özelleştirin (gönderimden sonra gösterilir)
- Spam korumasını seçin (HoneyPot önerilir)
- Gerekirse "Giriş Gerekiyor" durumunu aç
- Karmaşık formlar için "Çok Adımlı Form" özelliğini etkinleştirin

**Adım 4: Formu Etkinleştir**
- **Etkin** durumunu aç
- Sadece etkin formlar gönderimleri kabul eder
- Formu kaydedin

**Adım 5: Sayfa Oluşturucuda Kullan**
- Herhangi bir sayfaya **Form** öğesi ekleyin
- Dropdown'tan formunuzu seçin
- Form, sayfa stilini miras alır
- Gönderimler otomatik olarak arka uç gönderilir

## Tek Sayfa vs Çok Adımlı Formlar

**Tek Sayfa Formları** (varsayılan):
- Tüm alanlar bir kez gösterilir
- Kaydırarak tüm alanları görebilirsiniz
- Gönder butonu en altında
- En iyi: Temas formları, kısa anketler, basit veri toplama

**Çok Adımlı Formlar**:
- Alanlar numaralandırılmış adımlara bölünmüştür
- İlerleme çubuğu mevcut adımı gösterir
- Geri/İleri navigasyon butonları
- Sadece son adımda gönder
- Opsiyonel: Kısmi yanıtları kaydet (taslak modu)
- En iyi: İş başvuruları, kayıtlar, karmaşık anketler, ödeme akışları

**Çok Adımlı Etkinleştirme**:
1. Form ayarlarında "Çok Adımlı Form" durumunu aç
2. Sağ paneldeki "Adımlar" sekmesine tıklayın
3. Adım ekleyin (örneğin, "Kişisel Bilgiler", "İletişim Bilgileri", "Tercihler")
4. Alanı düzenlerken adım dropdown'ından alanları adımlara atayın
5. Adımları sürükleyerek sıralayın
6. Adım özellikleri: başlık, açıklama, atla

**Çok Adımlı Faydaları**:
- Form terkini azaltır (psikolojik: "bu sayfada sadece 3 soru")
- Mantıklı gruplama UX'yi iyileştirir
- İlerleme göstergesi tamamlamayı teşvik eder
- Uzun formlar için isteğe bağlı taslak kaydetme

## Form Ayarlarını Açıklama

**Temel Ayarlar**:
- **İç Ad** - Yönetici panelinde formu nasıl tanımlarsınız (müşterilere görünmez)
- **Slug** - URL dostu tanımlayıcı (otomatik olarak oluşturulur, API uç noktalarında kullanılır)
- **Form Başlığı** - Formun üstünde gösterilen başlık
- **Açıklama** - Başlığın altına gösterilen isteğe bağlı yardım metni
- **Gönder Butonu Metni** - Buton etiketini özelleştirin (örneğin, "Mesaj Gönder", "Şimdi Başvur")

**Mesajlar**:
- **Başarı Mesajı** - Başarılı gönderimden sonra gösterilir (varsayılan: "Gönderiminiz için teşekkür ederiz!")
- **Hata Mesajı** - Gönderim başarısız olduğunda gösterilir (varsayılan: "Bir hata oluştu. Lütfen tekrar deneyin.")

**Güvenlik & Erişim**:
- **Etkin** - Sadece etkin formlar gönderimleri kabul eder (etkin olmayan formlar "Form mevcut değil" gösterir)
- **Giriş Gerekiyor** - Sadece kimliği doğrulanmış kullanıcılar için kısıtla (anonim kullanıcılar giriş istemi görür)

**Spam Koruma**:
- **Hiçbiri** - Hiçbir koruma (önerilmez, botlar spam yapar)
- **HoneyPot Alanı** - Görünmez alan botları yakalar (çoğu satıcı için önerilir)
- **Google reCAPTCHA v3** - Google'dan site anahtarı ve gizli anahtar gerekir (en güçlü koruma)

**Gelişmiş Özellikler**:
- **Çok Adımlı Form** - Adım adım iş akışı etkinleştir
- **Kısmi Yanıtları Kaydet** - Kullanıcılara ilerlemeyi kaydetmelerine ve daha sonra devam etmelerine izin ver (sadece çok adımlı)

## Spam Koruma Seçenekleri

**HoneyPot Alanı (Tavsiye Edilir)**:
- Forma görünmez bir alan eklenir
- Botlar bunu doldurur (insanlar bunu göremez)
- HoneyPot doldurulmuş gönderimler reddedilir
- Yapılandırma gerekmez
- Kullanıcılar için CAPTCHA frustrasyonu yok
- 95%+ spam botlarına karşı etkili

**Google reCAPTCHA v3**:
- Arka plan skoru (0.0-1.0)
- "Trafik ışıklarını tıkla" zorlaması yok
- Yapılandırma gerekir:
  1. google.com/recaptcha/admin'da hesap oluşturun
  2. Site anahtarı ve gizli anahtar oluşturun
  3. Anahtarları form oluşturucu ayarlarına girin
- HoneyPot'tan daha güçlü
- HoneyPot yetersiz olduğunda kullanın

**Hiçbiri**:
- Spam koruması yok
- Sadece iç formlar veya test için kullanın
- Kamu formları yoğun spam alır

## Form Yanıtını Yönetme

**Ayarlar > Sayfalar > Formlar > [Form Adı] > Yanıtlar**'da tüm gönderimleri görüntüleyin:

**Yanıt Listesi Görünümü**:
- Durum: taslak, gönderildi, tamamlandı
- Gönderen: e-posta (giriş yapmışsa) veya "Anonim"
- IP adresi ve konum (GeoIP etkinse)
- Gönderim tarihi/saati
- Tamamlanma süresi (saniye)

**Yanıt Detayı**:
- Tüm alan değerleri etiketleriyle birlikte
- Meta veriler: tarayıcı, referer, dil
- İlerleme izleme (çok adımlı): mevcut adım, tamamlanan adımlar
- Eylem sonuçları (form eylemleri tetiklendiğinde)

**Yanıt Filtreleme**:
- Form, durum, tarih aralığına göre filtrele
- Gönderen e-postasına veya IP adresine göre ara
- Gönderim tarihine göre sırala, tamamlanma süresine göre sırala

**Yanıt Dışa Aktarma**:
- **CSV'ye Dışa Aktar** butonuna tıklayın
- "{form-slug}_responses_{date}.csv" indirilir
- Başlık satırı: Gönderim Zamanı, Kullanıcı, IP, Durum, [Alan Etiketleri]
- Her yanıt bir satırda
- Excel, Google Sheets veya veri analiz araçlarında aç

## Sayfalar içinde Form Kullanımı

**Formları Gömme**:
1. Sayfayı Sayfa Oluşturucu'da açın
2. Elemanlar panelinden **Form** öğesini ekleyin
3. Dropdown'tan formu seçin
4. Form kapsülü stilini özelleştirin (arka plan, dolgu, kenarlık)
5. Sayfayı kaydedin ve yayınlayın

**Formunun Gösterimi**:
- Form başlığı ve açıklaması (form ayarlarından)
- Tüm alanlar sırayla (tek sayfa) veya mevcut adım (çok adımlı)
- Özel metinle gönder butonu
- Gönderimden sonra başarı/hata mesajları

**Stil Mirası**:
- Formlar, sayfa temalarını miras alır
- Butonlar, tema buton stillerini kullanır
- Giriş alanları, tema giriş stillerini kullanır
- Alanlara özel CSS sınıfı ekleyerek özel stiller için

## Form Builder Arayüzü

**Sol Kenar Çubuğu - Alan Kütüphanesi**:
- Kategoriye göre düzenlenmiştir (Metin, Seçim, Puanlama, Gelişmiş)
- Alanı canvas'a sürükleyin veya tıklayarak ekleyin
- Alan türlerini hızlıca bulmak için arama yapın

**Ana Canvas - Alan Düzenleyici**:
- Alanı yeniden sıralamak için sürükleyici (≡)
- Alanı tıklayarak seçin ve düzenleyin
- Her alana silme butonu (×)
- Yapılandırılmış alanın görsel önizlemesi
- Boş durumda drop zone talimatları

**Sağ Kenar Çubuğu - Özellikler Paneli**:
- **Form Ayarları Sekmesi** - Temel bilgiler, mesajlar, spam koruma
- **Alan Ayarları Sekmesi** - Seçili alanı yapılandırın (etiket, doğrulama vb.)
- **Adımlar Sekmesi** - Adımları yönetin (sadece çok adımlı formlar için)
- **Koşullu Kurallar Sekmesi** - Yanıtlara göre göster/gizle mantığı ekleyin

**Araç Çubuğu Özellikleri**:
- **Geri Al/İleri Al** - Tam düzenleme geçmişi
- **Önizleme** - Form işlevselliğini test edin
- **Kaydet** - Düzenleme sırasında her 3 saniyede bir otomatik kaydedilir
- **Çeviriler** - Form metnini diğer dillere çevirin

## Ortak Form Örnekleri

**Temas Formu**:
- Alanlar: Tam Ad (gerekli), E-posta (gerekli), Telefon, Mesaj (gerekli)
- Gönder butonu: "Mesaj Gönder"
- Başarı: "Bize ulaşmak için teşekkür ederiz! 24 saat içinde yanıtlayacağız."

**Ürün Geri Bildirim Anketi**:
- Adım 1: Yıldız puanlama, Likert ölçeği anlaşması
- Adım 2: NPS puanı, iyileştirme önerileri
- Koşullu: Puan < 3 ise, iyileştirme geri bildirimi gerekli

**İş Başvurusu**:
- Adım 1: Kişisel bilgiler (ad, e-posta, telefon)
- Adım 2: Deneyim (öge yükleme, deneyim yılı, referanslar)
- Adım 3: Uygunluk (başlangıç tarihi, maaş beklentileri)
- Kısmi kaydetme etkin (başvurucular daha sonra devam edebilir)

**Tercihlerle Haberleşme Listesi Kaydı**:
- E-posta (gerekli)
- Onay kutusu grubu: İlgi alanları (Ürünler, Satışlar, Blog Güncellemeleri)
- reCAPTCHA etkin (sahte kayıtları önlemek için)

## İpuçları

- **Tek sayfa ile başlayın** - Alan sayısı 10'dan fazla olduğunda çok adımlı ekleyin
- **Önce HoneyPot kullanın** - Spam devam ediyorsa reCAPTCHA'ya yükseltin
- **Yayınlamadan önce test edin** - Önizleme modunda doğrulama ve akışı doğrulayın
- **Düzenli olarak dışa aktarın** - Haftada bir yanıt CSV'sini indirin ve yedekleme yapın
- **Tamamlanma süresini izleyin** - Ortalama >5 dakika ise form çok uzun olabilir
- **Koşullu mantık kullanın** - İlgisiz alanları gizleyerek form uzunluğunu algılamayı azaltın
- **Uzun formlar için kısmi kaydetmeyi etkinleştirin** - Çok adımlı başvurular için terkini azaltın
- **Form etiketlerini çevirin** - Çok dilli siteler için yerleşik çeviri sistemini kullanın
- **Gizli veri için giriş gerekli** - Anonim spamı önleyin, gönderimleri kullanıcı hesaplarına bağlayın
- **Başarı mesajlarını özelleştirin** - "24 saat içinde yanıtlayacağız" "Teşekkür ederiz"den daha iyidir

