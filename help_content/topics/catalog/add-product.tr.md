---
title: Ürün Ekleme
---

Bu, daha uzun bir belgeden dört bölümden biridir.

İçerik:

<!-- ekran görüntüleri gerekli:
- url: /admin/catalog/product/<id>/change/
  filename: envanter-sekmesi.webp
  açıklama: Fiziksel Özellikler, Nakliye,
    ve Gelecek Tarihli Sipariş kartlarını birlikte gösteren envanter sekmesi (Nakliye seçili, Tercihi Nakliye Paketi seçili ve Gelecek Tarihli Sipariş seçili ve bir teslim tarihi ve mesajı girilmiş, bu nedenle tüm yeni alanlar tek seferde görünür).
  kaydet: core/static/core/admin/img/help/add-product/
  görünüm alanı: 1440x900
  notlar: Daha önceki envanter-sekmesi.webp'yi değiştirir, Nakliye
    ve Gelecek Tarihli Sipariş kartları ile eşleşmiyor ve artık canlı form ile eşleşmiyor.
- url: /admin/catalog/product/<id>/change/
  filename: etiket-kartı.webp
  açıklama: Temel Bilgi sekmesi, etiket kartına sahip ve ürün için etiket seçiciye zaten birkaç etiket eklenmiş.
  kaydet: core/static/core/admin/img/help/add-product/
  görünüm alanı: 1440x900
- url: /admin/catalog/product/<id>/change/
  filename: gelişmiş-sekmesi.webp
  açıklama: Gelişmiş sekmesi, Ürün Sayfası Ayarları kartını (Sayfa Şablonu
    açılır menüsünde varsayılan olmayan bir seçenek seçili) ve altında
    Teknik Detaylar kartını gösterir.
  kaydet: core/static/core/admin/img/help/add-product/
  görünüm alanı: 1440x900
-->

Bu kılavuz, mağazanızaki yeni bir ürün oluşturmanıza yardımcı olur. Ürün formu, temel bilgi, medya, fiyat, envanter, SEO ve daha fazlasını kapsayan bölümler halinde düzenlenmiştir. - hepsini bir seferde doldurabilir ya da daha sonra bölümleri tamamlamak için geri dönebilirsiniz.

## Başlangıç

Yan menüden, ürün kataloğunuza bakmak için **Ürünler > Tüm Ürünler**'e gidin. Üst sağ köşede **+ Ürün Ekle** butonuna tıklayarak ürün oluşturma formunu açın.

![Ürün listesi sayfası](/static/core/admin/img/help/add-product/product-list-page.webp)

## Temel Bilgiler

**Temel Bilgiler** kısmı, ürününüzün temel kimliğini tanımladığınız bölümdür.

![Ürün ekleme formu](/static/core/admin/img/help/add-product/add-product-form.webp)

### Zorunlu alanlar

- **İsim** — Müşterilere gösterilen ürün adı. Diğer diller için çeviri eklemek için küresel ikonuna tıklayın.
- **Slug** — İsimle aynı URL'ye uygun hali (otomatik olarak üretilir). Gerekirse özelleştirin.
- **SKU** — İçsel stok takip birimi kodunuz.
- **Ürün Türü** — Aşağıdakilerden birini seçin: Basit, Değişken, Dijital, Paket, Hediye Kartı, Özelleştirilebilir, Yapılandırılamaz, veya Rezervasyon.
- **Kategori** — Ürünü organize etme ve mağaza arayüzünde navigasyon için bir kategoriye atayın.

### Durum ve görünürlük

Formun en altında bulunan **Durum** bölümünde:

- **Durum** — Çalışırken **Taslak** olarak ayarlayın, satılmaya hazır iken **Yayında** yapın, ya da artık sunulmayan ürünleri için **Kaldırıldı** olarak ayarlayın.
- **Öne Çıkarılmış** — Mağaza arayüzünde bu ürünü vurgulamak için işaretleyin.
- **Dijital Ürün** — Bu ürünün dijital indirilmeleri (dosyalar, lisanslar) içerip içermediğini belirtin. Herhangi bir ürün türüyle birlikte olabilir.
- **Mağaza Arayüzünden Kaldır** — Ürünü katalog listelerinden gizleyin, ancak yapılandırıcı seçeneği ya da paket bileşeni olarak hâlâ mevcut tutun.

### Opsiyonel alanlar

- **Marka** — Uygunsa bir marka ile ilişkilendirin.
- **Etiketler** — Bu sekmedeki **Etiketler** kartında bir ya da daha fazla etiket atayın. Etiketler, koleksiyonlardan farklıdır - ürünleri organize etme ve filtreleme için hızlı, serbest formlu etiketlerdir, ancak ticari gruplandırma değildir. Zaten mevcut bir etiket aramak için yazmaya başlayın, ya da anında yeni bir isim girerek bir tane oluşturun. Bkz. **Ürün Etiketleri** yardım konusu, etiketleri doğrudan oluşturmak, yeniden adlandırmak ve toplu olarak silmek için.

### Ürün tanımlamaları

- **Kısa Açıklama** — Ürün listelerinde ve kartlarında görünür. Kısa ve yaratıcı tutun.
- **Tam Açıklama** — Ürün detay sayfasında gösterilen detaylı ürün açıklaması. Zengin metin düzenleyicisini kullanarak biçimlendirme, resim, video ve tablo ekleyin.

Her iki açıklama alanı da çeviri özelliğini destekler - diğer dillerde içerik sağlamak için küresel ikona tıklayın.

### Özellikler ve spesifikasyonlar

Tüm markdown formatlamasını, resim yollarını, kod bloklarını ve teknik terimleri koruyun.

Ürün Detayları

Ürün stokta olmadığı sürece bir ürünü satmak için **Ön Sipariş** kartını kullanın - ürününüzün tanıtımından önce sipariş almak istediğiniz yeni bir ürün için yararlıdır:

- **Ön Sipariş** — Ürün stokta değilken de müşterilerin bu ürünü satın almasına izin verin.
- **Ön Sipariş Açılış Tarihi** — Müşterilere gösterilecek olan beklenen mevcut tarihi.
- **Ön Sipariş Mesajı** — Müşterilere kısa bir özel mesaj gösterin, 200 karaktere kadar (örneğin: "Mart 2026'da kargo verilecek").

### Ürün tanımlayıcıları

Pazarlık listeleri ve envanter sistemleri için standart ürün kodları:

- **GTIN** — Küresel Ticaret Ürün Numarası
- **EAN** — Avrupa Ürün Numarası
- **UPC** — Evrensel Ürün Kodu (ABD)
- **ISBN** — Kitaplar için
- **ASIN** — Amazon kimliği
- **MPN** — Üretici Parça Numarası

### Uluslararası kargo / gümrük

Uluslararası kargo için gerekli (**Uluslararası Kargo / Gümrük** bölümünü genişletin):

- **HS Kodu** — Harmonize Sistem sınıflandırma kodu
- **Menşei Ülkesi** — Ürünün üretildiği yer
- **Gümrük Birim Fiyatı** — Gümrük için bildirilen birim başına fiyat
- **İhracat Lisans Numarası** — Sadece kontrol edilen ya da sınırlı ürünler için gerekli
- **İhracat Lisans Süresi** — İhracat lisanslarının sona erme tarihi

## SEO

Ürününüzün arama motoru görünümünü optimize edin.

![SEO sekmesi](/static/core/admin/img/help/add-product/seo-tab.webp)

- **Meta Başlığı** — Arama motoru sonuçlarında gösterilen başlık. Çevirmek için dünya simgesine tıklayın.
- **Meta Açıklaması** — Arama sonuçları için kısa bir açıklama (en fazla 160 karakter). Çevirmek için dünya simgesine tıklayın.
- **Otomatik SEO Oluştur** — Ürün kaydedildiğinde SEO içeriğini otomatik olarak oluşturmak için kontrol edin.

Google arama sonuçlarında ürününüzün nasıl görüneceğini gösteren canlı bir **Arama Sonucu Örneği** vardır.

## Ürün sayfası ayarları

**Gelişmiş** sekmesindeki **Ürün Sayfası Ayarları** kartı, bu ürünün mağaza sayfasının nasıl görüneceğini kontrol etmenize olanak tanır:

- **Sayfa Şablonu** — Bu ürün için sitenin varsayılan ürün sayfası düzenini geçersiz kılın: Klasik, Tam Genişlik, Galeri Vurgusu, ya da Dijital. Tasarım ayarlarınızın belirttiği herhangi bir düzenin devralınmasını sağlamak için **Site Varsayılanını Kullan**'ı tercih edin — çoğu ürün varsayılan üzerinde kalmalıdır, böylece şablon değişiklikleri orada otomatik olarak uygulanır.
- **İlgili Ürünleri Göster** — sayfanın altına ilgili ürünleri gösterin.
- **Yorumları Göster** — müşteri yorumlarını gösterin.
- **Özellikleri Göster** — Özellikler sekmesini gösterin.

**Galery Türü** alanı — ürün resimlerinin nasıl görüntüleneceğini kontrol eder (Standart Galeri, Karousel, Grid Yapısı, Zoom Galerisi, ya da 360° Görünüm) — ayrı bir **Medya** sekmesinde ayarlanır.

## Satış kanalı

**Satış Kanalı** alanı (Durum bölümünde), ürünün nerede satılabileceğini kontrol eder:

- **Tüm Kanallar** — Online ve mağaza içi (POS) olarak mevcut.
- **Sadece Online** — POS terminallerinden satış yapılmaz.
- **Sadece Mağaza** — Online olarak listelenmez; sadece fiziksel mağazanızda mevcuttur.

POS barkod okuma alanı için bir **Barkod** alanı da mevcuttur.

## Ürününüzü Kaydedin

Hazır olduğunuzda, sağ üst köşedeki kaydet butonlarını kullanın. Ürününüzün durumu **Yayında** olarak ayarlandığında mağaza üzerinde görünecektir.

## İpuçları

Tüm markdown formatlamasını, resim yollarını, kod bloklarını ve teknik terimleri koruyun.

- **Taslak** durumu ile başlayın, böylece müşterilerinize göstermeden önce ürününüzü geliştirin.
- Farklı fotoğraflara sahip ürünler daha fazla dönüşüm sağlar, bu nedenle birden fazla resim yükleyin.
- Arama motorlarında tanımlanabilirliği artırmak için **SEO** alanlarını doldurun.
- Müşterilerin katalogunuza erişimini kolaylaştırmak için **Kategoriler**, **Markalar** ve **Etiketler** kullanın.
- Değişken ürünler (örneğin, farklı boyutlar veya renkler) için **Değişken Ürün** türünü seçin ve kaydettikten sonra varyant ekleyin.
- Ürün sayfasındaki özel sekme olarak görünen yapılandırılmış ürün verilerini eklemek için **Özellikler** ve **Özellikler** kullanın.
- **Kargo Gerektirir** seçili kalmazsa, **Ürün Türü** ne bakın - Spwig, fiziksel olarak gönderilmeyen dijital, rezervasyon ve hediye kartı ürünlerinde kargoyu otomatik olarak kapatır.
- Her zaman aynı kutuda sevk edilen ürünler için bir **İlk Sıra Kargo Paketi** belirleyin - bu, ürününüzün ağırlığını ve boyutlarını aslında kullandığınız kutu ile senkronize etmekten kurtulmanıza yardımcı olur.