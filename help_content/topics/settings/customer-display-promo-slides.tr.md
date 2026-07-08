---
title: Müşteri Ekranı Promosyon Kaydırıcıları
---

Promosyon kaydırıcıları, POS terminali boşta iken (aktif bir işlem yok) müşteriye yönelik ekran üzerinde görüntülenir. Mevsimsel indirimler, yeni ürün tanıtımı, mağaza politikaları, yaklaşan etkinlikler ve sadakat programı avantajlarını gösteren bir kaydırıcı galerisi oluşturun. Kaydırıcılar, kapsam ataması kullanılarak belirli mağazalara veya gruplara hedeflenebilir - sadece ABD mağazalarında tatil promosyonlarını çalıştırın veya sadece ilgili konumlarda yerel etkinlik bilgilerini görüntüleyin. Aktif kaydırıcılar, 5-10 saniyede bir otomatik olarak döngüye girer, müşterilerin işlem yaparken bilgilendirilmesini sağlar ve etkileyici dijital bir tanıtım oluşturur.

Promosyon kaydırıcılarını, mevcut indirimlerin farkındalığını artırarak, politikalar hakkında müşterilere bilgi vererek ve sadakat programları ve etkinliklerle etkileşimi artırarak kullanın.

![Promo Slide List](/static/core/admin/img/help/customer-display-promo-slides/promoslide-list.webp)

## Müşteri Ekranı Davranışı

Bir POS terminali boşta iken (kasiyerde müşteri yok, işlem yok), müşteriye yönelik ekran aşağıdaki şeyleri gösterir:

**Kaydırıcı Modu**:
- Tüm aktif kaydırıcıları döngüye girer
- Her kaydırıcı 5-10 saniye boyunca gösterilir (terminal başına yapılandırılabilir)
- Kaydırıcılar arasında yumuşak geçişler
- İşlem başlayana kadar sürekli döngüye girer

**İşlem Sırasında**:
- Kaydırıcı anında durur
- Ekran işlem görünümüne geçer (ürünler, toplam, ödeme istekleri)
- İşlem tamamlandığında ve terminal tekrar boşta iken kaydırıcı yeniden başlatılır

**Hiçbir Kaydırıcı Yapılandırılmadığında**:
- Ekran, mağaza markalaşmasıyla birlikte "Hoş geldiniz" mesajı gösterir
- Statik ekran (hiçbir kaydırıcı yok)

**Teknik Gereksinimler**:
- Müşteri ekranı, ayrı bir monitör olabilir veya kasiyerin (POS uygulaması picture-in-picture modunu destekler) aynı ekranı olabilir
- Ekran BroadcastChannel API (aynı cihazda iletişim) veya WebSocket (ayrı cihazlarda ekranlar) ile senkronize edilir

## Kapsam Hedefleme

Fiş şablonları gibi, promosyon kaydırıcıları kapsam tabanlı hedefleme destekler (öncelik en yüksekten en düşüğe):

| Öncelik | Kapsam | Örnek | Kullanım Durumu |
|----------|-------|---------|----------|
| **1** | Mağaza özel | Paris Mağaza kaydırıcıları | Paris yaz festivali etkinlik kaydırıcısı |
| **2** | Grup özel | Avrupa Mağazaları kaydırıcıları | Sadece AB için GDPR gizlilik politikası kaydırıcısı |
| **3** | Tüm Mağazalar | Küresel kaydırıcılar | "50$'dan fazla siparişlerde ücretsiz kargo" (şirket genelinde promosyon) |

**Kapsam Nasıl Çalışır**:
- Terminal, mağaza kapsamına uygun kaydırıcıları gösterir (mağaza özel kaydırıcıları)
- Ayrıca, grup kapsamına uygun kaydırıcıları gösterir (mağaza bir gruba aitse)
- Ayrıca, kapsam ataması olmayan kaydırıcıları (küresel kaydırıcılar) gösterir
- Sonuç: Mağaza, 3-5 kaydırıcı gösterebilir (kapsamlı ve küresel karışım)

**Örnek**:
- Küresel kaydırıcı: "Yeni Sadakat Programı - Bugün Katıl!" (kapsam yok)
- Grup kaydırıcı: "Memorial Day Satış - %30 İndirim" (yalnızca ABD Mağazaları grubu)
- Mağaza kaydırıcı: "Büyük Açılış - NYC Ana Mağaza" (yalnızca NYC Mağazası)

**NYC Mağaza Terminali**, tüm 3 kaydırıcıyı gösterir (mağaza + grup + küresel)
**London Mağaza Terminali**, yalnızca küresel kaydırıcıyı gösterir (ABD Mağazaları grubunda değil, NYC mağazası değil)

## Görsel Gereksinimleri

Promosyon kaydırıcıları, müşteri ekranı monitörleri için optimize edilmiş tam ekran görsellerdir:

**Yakınlaştırma Oranı**: 16:9 (geniş ekran)

**Önerilen Çözünürlük**: 1920×1080 piksel (Full HD)
- Çoğu modern ekran için temiz yakınlaştırma
- Kalite ve yükleme hızı arasındaki dengesi

**Kabul Edilen Çözünürlükler**:
- Minimum: 1280×720 (HD)
- Optimal: 1920×1080 (Full HD)
- Maksimum: 3840×2160 (4K) - önerilmez (büyük dosya boyutu, yavaş yükleme)

**Dosya Formatı**: JPG, PNG veya WebP
- Fotoğraflar için JPG
- Şeffaflıkla grafikler için PNG (arka planlar önerilir)
- En küçük dosya boyutu için WebP

**Dosya Boyutu**: Kaydırıcı başına <500KB
- Daha büyük dosyalar, kaydırıcı yükleme hızını yavaşlatır
- Yüklemeden önce görselleri sıkıştırın (Media Library optimizasyonu kullanın)

**Tasarım Önerileri**:
- Uzak mesafeden okunabilirlik için yüksek kontrast (müşteriler ekranın 2-6 ayak uzaklığındadır)
- Büyük yazı (vücut metni için minimum 48pt, başlık için 72pt+)
- Kalın yazı tipleri (bazı ekranlarda ince yazılar kaybolur)
- Küçük detaylardan kaçının (müşteri görüş açısından görünmez)
- Eylem çağrısı (müşterinin ne yapması gerektiğini belirtin: "Kasiyere detaylar için sorun", "Bugün kayıt olun")

## Promosyon Kaydırıcısı Oluşturma

**POS > Promosyon Kaydırıcıları**'na gidin ve **+ Promosyon Kaydırıcısı Ekle**'ye tıklayın:

![Promo Slide Add Form](/static/core/admin/img/help/customer-display-promo-slides/promoslide-add-form.webp)

**Görsel** - Yükle veya Medya Kütüphanesinden seç:
- **Medya Kütüphanesini Gözat**'a tıklayarak mevcut bir görsel seçin
- Veya yukarıdaki gereksinimleri karşılayan yeni bir görsel yükle
- Önizleme, görselin ekran üzerinde nasıl görüneceğini gösterir

**Başlık** (Opsiyonel) - Kaydırıcının üst kısmında metin örtüsü:
- Maksimum 60 karakter (uzun metin kısaltılır)
- Görselin üst kısmında yarım şeffaflıktaki koyu bir çubukta görünür
- Kaydırıcının başlığı için kullanın ("Yaz mevsimi indirimi", "Yeni Ürünler")
- Görsel başlık metni içeriyorsa boş bırakın

**Alt Başlık** (Opsiyonel) - Başlık altında metin örtüsü:
- Maksimum 120 karakter
- Başlığın hemen altındaki aynı yarım şeffaflıktaki çubukta görünür
- Desteleyici detaylar için kullanın ("Up to 50% off", "Free gift with purchase")
- Görsel kendi başına yeterliyse boş bırakın

**Aktif mi?** - Kaydırıcının etkinleştirilip etkinleştirilmeyeceğini kontrol eder:
- Sadece aktif kaydırıcılar kaydırıcı galerisinde görünür
- Mevsimsel etkinleştirmek için kullanın (promosyon bittikten sonra kapatın)
- Devre dışı bırakmak, kaydırıcıyı gelecekteki yeniden etkinleştirme için saklar

**Sıra Numarası** - Kaydırıcının galerideki konumunu kontrol eder:
- Düşük numaralar, döngüde daha önce görünür
- 10, 20, 30 gibi onluk katları kullanın (mevcut kaydırıcılar arasında yeni kaydırıcı eklemeyi sağlar)
- Örnek: Tatil satışları (sıra numarası 10) genel sadakat programından (sıra numarası 20) önce gösterilir

**Kapsam Ataması** (Opsiyonel):
- **Depo** - Belirli bir mağazada göstermek için seçin
- **Mağaza Grubu** - Grubun içindeki mağazalarda göstermek için seçin
- **Her ikisini de boş bırakın** - Tüm mağazalarda gösterilir (küresel kaydırıcı)

## Sıra Numarası ve Kaydırıcı Akışı

**Örnek Kaydırıcı** (NYC Mağaza terminali):
- Kaydırıcı 1 (sıra numarası 10): "Büyük Açılış - NYC Ana Mağaza" (mağaza özel)
- Kaydırıcı 2 (sıra numarası 15): "Memorial Day Satış - %30 İndirim" (ABD Mağazaları grubu)
- Kaydırıcı 3 (sıra numarası 20): "Yeni Sadakat Programı - Bugün Katıl!" (küresel)
- Kaydırıcı 4 (sıra numarası 30): "Bizi @yourstore takip edin" (küresel)

Kaydırıcı döngüsü: 1 → 2 → 3 → 4 → 1 → 2 → ...

**London Mağaza Terminali** (ABD Mağazaları grubunda değil, farklı mağaza):
- Kaydırıcı 1 (sıra numarası 20): "Yeni Sadakat Programı - Bugün Katıl!" (küresel)
- Kaydırıcı 2 (sıra numarası 30): "Bizi @yourstore takip edin" (küresel)

Kaydırıcı döngüsü: 1 → 2 → 1 → 2 → ...

Sıra numarasını, döngüde en önemli içeriği önceliklendirmek için kullanın.

## Mevsimsel Etkinleştirme Stratejisi

**Problem**: Her mevsimsel promosyon için kaydırıcı oluşturmak/yok etmek zahmetli.

**Çözüm**: Kaydırıcıları bir kez oluşturun, mevsimsel olarak etkinleştirin/devre dışı bırakın:

1. **Büyük Etkinlikler İçin Kaydırıcılar Oluşturun**:
   - "Yaz İndirimi" (Aktif: Hayır, önceden oluşturuldu)
   - "Okul Dönemi Geri Dönüş" (Aktif: Hayır, önceden oluşturuldu)
   - "Kara Cuma" (Aktif: Hayır, önceden oluşturuldu)
   - "Yılbaşı İndirimi" (Aktif: Hayır, önceden oluşturuldu)

2. **İlgili Olduğunda Etkinleştirin**:
   - Haziran 1: "Yaz İndirimi" → Aktif: Evet
   - Ağustos 15: "Yaz İndirimi" → Aktif: Hayır, "Okul Dönemi Geri Dönüş" → Aktif: Evet
   - Kasım 20: "Kara Cuma" → Aktif: Evet
   - Aralık 1: "Kara Cuma" → Aktif: Hayır, "Yılbaşı İndirimi" → Aktif: Evet

3. **Etkinlik Sonrası Devre Dışı Bırakın**:
   - Kaydırıcı kütüphanesini organize eder
   - Yıllık olarak kaydırıcıları yeniden kullanın (gerekirse görseli güncelleyin, yapılandırmayı koruyun)

## Kullanım Durumu Örnekleri

**Kullanım Durumu 1: Mevsimsel İndirim**
- Görsel: Kırmızı arka plan ve beyaz metin "YAZ İNDİRİMİ - SEÇİLEN ÜRÜNLERDE %60 İNDİRİM"
- Başlık: "Yaz İndirimi"
- Alt Başlık: "Seçilen ürünlerde %50-%60 indirim. Ayrıntılar için kasiyere sorun."
- Kapsam: Tüm mağazalar (küresel)
- Sıra numarası: 10 (yaz döneminde en yüksek öncelik)
- Aktif: Haziran-Ağustos arasında sadece

**Kullanım Durumu 2: Mağaza Politikası**
- Görsel: İade politikasını gösteren bir infografik
- Başlık: "Kolay İade"
- Alt Başlık: "Fatura ile 30 gün. Soru sormadan."
- Kapsam: Tüm mağazalar (küresel)
- Sıra numarası: 40 (promosyonlardan daha düşük öncelik)
- Aktif: Tüm yıl boyunca

**Kullanım Durumu 3: Yeni Ürün Tanıtımı**
- Görsel: Yeni ürünün ana fotoğrafı
- Başlık: "YENİ: Kablolu Olmayan Kulaklık Pro"
- Alt Başlık: "Mağazada ve çevrimiçi olarak mevcut. 199,99 $"
- Kapsam: Tüm mağazalar (küresel)
- Sıra numarası: 5 (tanıtım haftasında en yüksek öncelik)
- Aktif: Tanıtım haftasında sadece, sonra devre dışı bırakın

**Kullanım Durumu 4: Yerel Etkinlik**
- Görsel: Yerel bir yardım koşusu posteri
- Başlık: "Yerel Yardım"
- Alt Başlık: "Haziran 15'te topluluk 5K'ya katılarak bize katılın!"
- Kapsam: Belirli bir mağaza (yalnızca NYC Mağazası)
- Sıra numarası: 8 (bu mağaza için öncelik)
- Aktif: Etkinlikin 2 haftası önce

**Kullanım Durumu 5: Sadakat Programı**
- Görsel: Sadakat kartı görseli ve puan örnekleri
- Başlık: "Ödül Kazanın"
- Alt Başlık: "Sadakat programımıza katılarak harcadığınız her $1 için 1 puan kazanın"
- Kapsam: Tüm mağazalar (küresel)
- Sıra numarası: 30 (daimi içerik)
- Aktif: Tüm yıl boyunca

## Kaydırıcıları Yönetme

**Kaydırıcı Listesi Görünümü**:
- Tüm kaydırıcıları görüntüler, görsel önizlemesi, başlık, kapsam, durum ile birlikte
- Aktif/Devre dışı filtreleme
- Kapsamla filtreleme (tüm küresel kaydırıcıları, tüm grup kaydırıcılarını vb. görüntüle)

**Toplu Etkinleştirme/Devre Dışı Bırakma**:
- Listede birden fazla kaydırıcı seçin
- Yönetici eylemini kullanarak tümünü bir kez etkinleştirin veya devre dışı bırakın
- Mevsimsel geçişler için kullanışlıdır (tüm yaz kaydırıcılarını devre dışı bırakın, tüm sonbahar kaydırıcılarını etkinleştirin)

**Kaydırıcıları Test Etme**:
- Kaydırıcıyı oluşturduğunuzda/güncellediğinizde POS terminaline gidin
- Terminalin boşta kalmasını sağlayın (hiçbir işlem yok)
- Kaydırıcının kaydırıcı galerisinde görünmesini doğrulayın
- Görsel kalitesini, metin örtüsünün okunabilirliğini, zamanlamayı kontrol edin

**Aktif Kaydırıcıları Güncellemek**:
- Değişiklikler, bir sonraki kaydırıcı galerisi yenilemesinde etkin olur (genellikle <30 saniye)
- Terminali yeniden başlatmaya gerek yok

## İpuçları

- **Uzaklık için Tasarım** - Müşteriler ekranı 2-6 ayak uzaklıkta görür; büyük yazı ve yüksek kontrast kullanın
- **Mesajı Basitleştirin** - Kaydırıcı 10 saniyeden kısa sürede gösterilir; her kaydırıcıda bir açık mesaj olmalı
- **Sezonel Devre Dışı Bırakma** - Bir kez oluşturun, yıllık olarak aç/kapat yerine yeniden oluşturmayın
- **Sıra Numarası ile Önceliklendirin** - En önemli promosyonlara en düşük sıra numarası verin (önce görünür)
- **Gerçek Cihazda Test Edin** - Ekran renk kalibrasyonu değişebilir; özel monitörlerinizde kaydırıcıların iyi göründüğünden emin olun
- **Aktif Kaydırıcı Sayısını Sınırlayın** - Her mağaza için 3-5 aktif kaydırıcı idealdir; 10+ kaydırıcı her birinin nadir olarak görünmesini sağlar
- **CTA (Eylem Çağrısı) Ekleme** - Müşterilere ne yapmaları gerektiğini belirtin ("Kasiyere sorun", "Web sitesini ziyaret edin", "Fişteki QR kodunu tarayın")
- **Sürekli Güncelleyin** - Geçmiş olan promosyonlar (sona eren indirimler, geçmiş etkinlikler) müşteri güvenini azaltabilir
- **Kapsamı Stratejik Olarak Kullanın** - Bölgesel promosyonlar (grup kapsamı) ve yerel etkinlikler (mağaza kapsamı), sürekli küresel içerikten daha ilgili hissedilir

