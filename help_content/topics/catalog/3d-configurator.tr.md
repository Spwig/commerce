---
title: 3D Ürün Yapılandırıcısı
---

3D Yapılandırıcı, müşterilerin ürün sayfasında etkileşimli bir 3D görüntüleyici üzerinden yapılandırılabilir ürünleri görüntülemesine olanak tanır. Müşteriler renkler, malzemeler veya bileşen varyasyyonları gibi seçenekleri seçerken, 3D model anında güncellenerek seçimlerini yansıtır. Desteklenen mobil cihazlarda müşteriler, satın almadan önce ürünün kendi alanlarında sanal olarak yerleştirilmesini sağlayarak artırılmış gerçeklik (AR) ile de ürününüzü görebilir.

3D Yapılandırıcı, yapılandırılabilir ürünlerle çalışır. Her yapılandırılabilir ürün, ürünün yapılandırma seçeneklerine bir GLB model dosyası bağlayan bir 3D sahne yapılandırması olabilir.

## Başlamadan Önce

3D sahne ayarlamak için ihtiyacınız olanlar:

- Zaten kataloğunuzda oluşturulan bir **yapılandırılabilir ürün**
- Katalogunuzun Medya Kütüphanesine yüklenmiş bir **temel 3D model** — bu, varsayılan olarak görünen monte edilmiş modeldir
- Seçenek olarak, geometri değişimleri için ek GLB dosyaları (örneğin, farklı yakak şekilleri) ve malzeme varyasyonları için doku görüntülerini

Eğer yapılandırılabilir ürün ve yapılandırma seçeneklerini henüz oluşturmadıysanız, 3D sahneyi ayarlamadan önce bunu yapın.

## Sahne Yapılandırması Oluşturma

1. **Katalog > 3D Sahne Yapılandırmaları**'na gidin
2. **+ 3D Sahne Yapılandırması Ekle**'ye tıklayın
3. Bu sahnenin ait olduğu **Ürün**'ü seçin — sadece yapılandırılabilir ürünler mevcuttur
4. Medya Kütüphanenizden **Temel 3D Model**'i seçin — bu, varsayılan olarak yüklenen GLB dosyasıdır
5. Görüntüleyici ayarlarını yapılandırın (aşağıya bakın)
6. Kaydınızı kaydedin

Kaydettikten sonra **Düğüm Ağacı** alanı otomatik olarak doldurulur. Bu, GLB dosyanızdan çıkarılan sahne grafiği — modelin içindeki her isimlendirilmiş düğümün listesini içerir ve düğüm eşlemeleri eklerken bunları referans alacaksınız.

## Görüntüleyici Ayarları

Bu ayarlar, 3D görüntüleyicinin ürün sayfasında nasıl görüneceğini kontrol eder.

### Kamera ve Işıklandırma

| Alan | Açıklama | Varsayılan |
|------|---------|-----------|
| **Kamera Yörüngesi** | Başlangıç kamera pozisyonu `açı yükseklik mesafe` formatında (örneğin, `0deg 75deg 2m`) | `0deg 75deg 2m` |
| **Kamera Hedefi** | Kamera tarafından bakılan nokta, model merkezinden metre cinsinden (örneğin, `0m 0m 0m`) | `0m 0m 0m` |
| **Çevre Görüntüsü** | Medya Kütüphanenizden alınan bir HDR görüntüsü, görüntü tabanlı aydınlatma için kullanılır — daha gerçekçi yansımalara ve gölgelere neden olur | Yok |
| **Aydınlık** | Sahnenin genel parlaklığı — düşük değerler daha karanlık, yüksek değerler daha parlak | `1.0` |

### Gölgeler

| Alan | Açıklama | Varsayılan |
|------|---------|-----------|
| **Gölge Yoğunluğu** | Modelin altındaki gölgenin ne kadar güçlü olduğunun belirtimi — `0` hiç gölge, `1` tam yoğunluk | `0.5` |
| **Gölge Bulanıklığı** | Gölge kenarlarının ne kadar bulanık olduğunun belirtimi — `0` keskin, `1` çok bulanık | `0.5` |

### Renk Gradyanı

| Alan | Açıklama |
|------|---------|
| **Tone Mapping** | Sahneye uygulanan renk gradyanı algoritması. **Ticaret** ürün dostu, canlı renkler üretir. **Nötr**, renk doğruluğu sağlar. **ACES**, sinematik film görünümü sağlar. |
| **Işıklık Gücü** | Modelin ışık yayan (kendi ışığını yayan) bölümlerine ışık etkisi ekler. `0` ışık etkisini devre dışı bırakır. `1` ile `5` arasındaki değerler ince ile dramatik ışık etkileri sağlar. |

### Davranış ve Arka Plan

| Alan | Açıklama | Varsayılan |
|------|---------|-----------|
| **Otomatik Döndür** | Modelin yüklendiğinde yavaşça döner ve müşterinin dikkatini çeker | Açık |
| **AR Etkin** | Desteklenen cihazlarda müşterilerin **AR'de Görüntüle** butonunu görmesini sağlar | Açık |
| **Arka Plan** | Görüntüleyicinin arka plan rengi veya CSS gradyanı — bir heksa desimal renk (örneğin, `#f5f5f5`) veya bir CSS gradyan değeri girin | `#ffffff` |

### Kullanıcı Görüntüsü

**Kullanıcı Görüntüsü** alanı, 3D görüntüleyicinin önizleme ekran görüntüsünü tutar ve görüntüleyici yüklenebilir hale gelmeden önce gösterilir. Canlı ürün sayfasından bir ekran görüntüsü çekebilir ve bunu Medya Kütüphanenize yükleyebilir, ardından sayfa yükleme deneyimini daha akıcı hale getirmek için buraya bağlayabilirsiniz.

## 3D Görüntüleyiciyi Etkinleştirme ve Devre Dışı Bırakma

**Etkin** anahtar, 3D görüntüleyicinin ürün sayfasında gösterilip gösterilmeyeceğini kontrol eder.

Devre dışı bırakıldığında, ürün standart 2D görsel yapılandırıcıya geri döner.

Bu, yapılandırmayı müşterilere göstermeden önce bir senaryo yapılandırması yapmanı sağlar.

## Yapılandırma seçeneklerini 3D eylemlere bağlama

Temel senaryo yapılandırıldıktan sonra, her yapılandırma yuvası seçeneğini 3D modelde görsel bir değişikliğe bağlayabilirsiniz. Bu bağlantılar **Düğüm Haritalamaları** olarak adlandırılır ve senaryo yapılandırma formunun altındaki **Düğüm Haritalamaları** bölümünde eklenir.

### Düğüm haritalama alanları

| Alan | Açıklama |
|-------|-------------|
| **Yuva Seçeneği** | Bu değişikliği tetikleyen yapılandırma seçeneği (örneğin, "Kırmızı Deri") |
| **Eylem Türü** | Hangi görsel değişikliğin gerçekleştiğini belirtir (aşağıdaki eylem türlerine bakın) |
| **Hedef Düğüm** | Değişen senaryo ağ ağacındaki düğümün adı — **Düğüm Ağacı**'ndaki listelenen adlardan seçin |
| **Eylem Verisi** | Renk heksa kodu, doku URL'si veya GLB dosyası URL'si gibi eyleme özel veri |
| **Sıra Numarası** | Aynı seçeneğin birden fazla haritalamasının uygulanma sırasını kontrol eder |

### Eylem türleri

| Eylem | Ne yapar |
|--------|-------------|
| **Malzeme Rengi** | Hedef düğümdeki bir malzemenin rengini değiştirir — **Eylem Verisi**'nde bir heksa renk sağlayın |
| **Malzeme Doku** | Bir malzeme üzerindeki dokuyu değiştirir — **Eylem Verisi**'nde bir doku görsel varlığına bağlantı sağlayın |
| **Geometri Değiştirme** | Modelin bir kısmını farklı bir GLB dosyasıyla değiştirir — farklı bir tutamaç şekli gibi yapısal değişiklikler için kullanışlıdır |
| **Görünürlük** | Senaryodaki bir düğümü gösterir veya gizler — **Eylem Verisi**'nde `görünür: true` veya `görünür: false` ayarlayın |

Bir yuva seçeneği için birden fazla haritalama eklenabilir. Örneğin, "Mavi Jean" seçildiğinde, malzeme rengi *ve* deri kenar düğümünü aynı anda gizleyebilir.

## Geometri varlıkları

Yapılandırmanız **Geometri Değiştirme** eylemleri içeriyorsa, değiştirme GLB dosyalarını Geometri Varlıkları olarak kaydetmeniz gerekir. Bu, senaryo yapılandırma formunun **Geometri Varlıkları** bölümünde eklenir.

| Alan | Açıklama |
|-------|-------------|
| **Etiket** | Bu geometri varlığı için tanımlayıcı bir isim, örneğin "V-Boğum Kollu" |
| **GLB Dosyası** | Medya Kütphanenizden gelen değiştirme GLB dosyası |
| **Hedef Düğüm** | Bu geometrinin temel modelde hangi düğümü değiştirdiğini belirtir |

Bir Geometri Varlığı kaydedildikten sonra, GLB'den düğüm isimleri **Düğüm Verisi**'nde ayrıştırılır ve haritalamalarınızda hedef düğümler olarak kullanılabilir hale gelir.

## Doku varlıkları

**Malzeme Doku** haritalamalarında kullanılan doku görselleri, daha kolay referans için Doku Varlıkları olarak kaydedilebilir. Bu, **Doku Varlıkları** bölümünde eklenir.

| Alan | Açıklama |
|-------|-------------|
| **Etiket** | Tanımlayıcı bir isim, örneğin "Kırmızı Deri" |
| **Doku Görseli** | Medya Kütphanenizden gelen doku görseli |
| **Doku Türü** | Bu doku uygulandığı PBR kanalı — Temel Renk, Normal Haritası, Kabalık Haritası, Metaliklik Haritası, Ortam Kapanması veya Işıklı Harita |

## Örnek: Renk seçenekleri olan yapılandırılabilir kaban

**Senaryo:** Siyah, Lüks ve Burgundi renklerinde sipariş edilebilen bir kaban, her renk kaban vücut meshine uygulanır.

**Ayarlamalar:**

1. Kaban ürün için bir senaryo yapılandırması oluşturun ve monte edilmiş kaban GLB'yi temel model olarak ayarlayın
2. **Tone Mapping**'i Commerce olarak ve **Auto Rotate**'i açık olarak ayarlayın
3. Düğüm Haritalamalarında, üç girdi ekleyin — her renk seçeneği için bir tane:

| Yuva Seçeneği | Eylem Türü | Hedef Düğüm | Eylem Verisi |
|-------------|-------------|-------------|-------------|
| Siyah | Malzeme Rengi | KabanVücut | `{"renk": "#1a1a1a"}` |
| Lüks | Malzeme Rengi | KabanVücut | `{"renk": "#1b2a4a"}` |
| Burgundi | Malzeme Rengi | KabanVücut | `{"renk": "#6b2737"}` |

Müşteri ürün sayfasında Lüks'ü seçtiğinde, izleyici anında KabanVücut malzemesini lüks rengine günceller.

## İpuçları

Tüm markdown biçimlendirmesini, görsel yollarını, kod bloklarını ve teknik terimleri koruyun.

- 3D modelinizi oluştururken GLB düğümlerinizi açık ve net şekilde adlandırın — "JacketBody" veya "CollarMesh" gibi düğüm isimleri, "Mesh_023" gibi otomatik olarak oluşturulan isimlerden çok daha kolay çalışılabilir
- Çoğu ürün için **Commerce** ton haritalamasını kullanın — bu, canlı ve cazip ürün sunumu için ayarlanmıştır
- Varsayılan kamera açısı zaten en önemli özellikleri gösteriyorsa, **Auto Rotate** özelliğini devre dışı bırakın — bu, müşteriye yükleme sırasında disoriente edebilir
- AR düğmesini tanıtma öncesi, bir mobil cihazda test edin — AR kullanılabilirliği müşteri cihazına ve tarayıcıya bağlıdır (WebXR desteği olan iOS Safari ve Android Chrome en güvenilirleridir)
- Her sahne yapılandırması için bir **Thumbnail** (Özet) resmi yükleyin — bu, 3D görüntüleyici yükleneceği sırada beyaz bir kutunun yanıp sönmemesini sağlar
- 3D görüntüleyici henüz hazır değilse, **Enabled** (Etkinleştir) anahtarını devre dışı bırakarak müşterilere standart bir resim yapılandırıcısının görülebilmesini sağlayın