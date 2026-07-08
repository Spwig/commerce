---
title: Arka Plan Düzenleyici
---

Arka plan düzenleyici, katman arka planlarını dört türle tam kontrol sağlar: katı renk, gradyan, resim ve video. Ayrıca, Normal ve Hover durumlarını ayrı ayrı destekler, böylece etkileşimli görsel efektler yaratabilirsiniz. Herhangi bir öğenin **Stil sekmesini** açın ve **Arka Plan** bölümüne bakın, düzenleyiciye erişebilirsiniz.

![Arka Plan Düzenleyici](/static/core/admin/img/help/background-editor/background-editor.webp)

## Normal ve Hover Durumları

Arka plan düzenleyicinin üst kısmında, **Normal** ve **Hover** durumları arasında geçiş yapan bir anahtar vardır. Her durum kendi bağımsız arka plan yapılandırması ile gelir:

- **Normal** — Sayfa yüklendiğinde gösterilen varsayılan arka plan
- **Hover** — Ziyaretçi imleci öğe üzerine getirdiğinde uygulanan arka plan

Anahtarın yanındaki iki küçük önizleme bloğu, mevcut Normal ve Hover arka planlarını yan yana gösterir, böylece kontrastı hızlıca görebilirsiniz. Önce Normal durumu yapılandırın, ardından Hover'a geçerek isterseniz etkileşimli bir efekt ekleyebilirsiniz.

## Arka Plan Türleri

Düzenleyici panelinin üst kısmındaki ikon satırından bir arka plan türü seçin:

| Tür | Açıklama |
|------|-------------|
| **Renk** | Tek bir renk değeri kullanarak katı bir doldurma. Uygulamak hızlı ve hafif. |
| **Gradyan** | Doğrusal veya radial olacak şekilde iki veya daha fazla renk arasında akıcı bir karışım. Deniz, Güneş Batımı, Orman ve Meşe gibi yerleşik ön ayarlar içerir. Gelişmiş gradyan düzenlemesi için [Gradyan Oluşturucu](gradient-creator) konusuna bakın. |
| **Resim** | Yüklenecek bir resim veya medya kütüphanesinden seçilecek bir resim. Konumlandırma, boyutlandırma ve tekrar kontrollerini destekler. |
| **Video** | Yükleme sırasında veya mobil cihazlarda gösterilecek bir arka plan video URL'si ve isteğe bağlı bir poster resmi. |

Her durum için bir tür aynı anda aktif olabilir. Türleri değiştirmek önceki yapılandırmayı silmez — geri dönebilir ve ayarlarınız korunur.

## Renk Arka Planları

Renk seçildiğinde:

- **Hex Girişi** — Doğrudan bir hex kodu girin (örneğin, `#1A1A2E`)
- **Renk Örnekleri** — Hızlı seçim için bir önceden ayarlanmış örnek seçin. Örnekler temaya duyarlıdır ve aktif tema paletini yansıtır.
- **Düzenle Butonu** — Spektrum, kaydırıcılar ve format seçenekleriyle tam renk seçicisini açar (bkz. [Renk Seçici](color-picker) konusu)

Renk arka planları anında işlenir ve performans üzerinde hiçbir etkisi yoktur, bu nedenle bölümler, kartlar ve kapsayıcılar için idealdir.

## Gradyan Arka Planları

Gradyan seçildiğinde:

- **Önceden Ayarlanmış Gradyanlar** — Deniz, Güneş Batımı, Orman, Meşe ve diğerleri gibi yerleşik gradyanlardan birini seçin
- **Özel Gradyan** — **Düzenle**'ye tıklayarak gradyan oluşturucuyu açın ve yön, tür (doğrusal veya radial) ve renk duraklarını ayarlayabilirsiniz
- **Açı Kaydırıcısı** — Doğrusal gradyanlar için gradyan yönünü ayarlamak için (0-360 derece)

Gradyanlar, görsel derinlik eklerken resim varlıklarını gerektirmeden ve her ekran boyutuna mükemmel şekilde ölçeklenebilir.

## Resim Arka Planları

Resim seçildiğinde:

- **Yükle veya Medya Kütüphanesi** — Resim yer tutucuğuna tıklayarak yeni bir resim yükleme veya medya kütüphanesinden birini seçin
- **Boyut** — **Kapla** (öğeyi doldurur, kesilebilir), **İçine Al** (öğenin içine sığar) veya özel boyut seçin
- **Konum** — 9 nokta ızgara (sol üst, merkez, sağ alt vb.) kullanarak odak noktasını ayarlayın veya özel X/Y yüzdelik değerleri girin
- **Tekrar** — Tekrarı aç veya kapat. Karakterli desenler için kullanışlıdır
- **Örtü** — Resmin üzerine renk örtüsü ekleyin, şeffaflığı ayarlayarak metnin okunabilirliğini sağlar

Resimleri yüklemeden önce her zaman optimize edin. Büyük, sıkıştırılmamış resimler sayfa yükleme sürelerini yavaşlatır.

## Video Arka Planları

Video seçildiğinde:

- **Video URL'si** — MP4 veya WebM video dosyasına doğrudan bir URL girin
- **Poster Resmi** — Video yüklendiği sırada ve videoyu otomatik oynatmayan cihazlarda gösterilecek bir alternatif resim yükleyin
- **Otomat Oynat / Döngü / Sessiz** — Video arka planları varsayılan olarak otomatik oynatılır, döngüye alınır ve sessizdir, tarayıcı politikalarına uygun olmak için

Arka plan videolarını kısa tutun (10-30 saniye), sıkıştırın ve görsel olarak ince tutun.

İçerikten dikkat dağıtmadan bölüme katkı sağlayacak şekilde olmalılar.

## Nerede Görünür

Arka plan düzenleyici, arka planları destekleyen her öğede kullanılabilir:

- **Sayfa Oluşturucu** — Bölümler, konteynerler, sütunlar ve bireysel öğelerin tümü, Stil sekmesinde bir Arka Plan bölümüne sahiptir
- **Başlık/Açılış Oluşturucu** — Satır arka planları ve bireysel widget arka planları
- **Menü Oluşturucu** — Menü konteyneri ve açılır panel arka planları

Aynı düzenleyici arayüzü her yerde kullanılır, bu nedenle oluşturucular arasında iş akışınız tutarlı kalır.

## İpuçları

- Görsel arka planlarda, metnin okunabilirliğini görselin içeriğinden bağımsız olarak sağlamak için yarım şeffaf bir renk örtüsü kullanın.
- Gradyan ön ayarları, görsel ilgi eklemek için hızlı bir yoldur — birini uygulayın, ardından açısını veya renkleri markanızla eşleştirmek için özelleştirin.
- Etkileşimli kartlara Normal ve Hover arka planlarını ayarlayarak ziyaretçilerin içeriklerini keşfederken net görsel geri bildirim sağlayın.
- Görsel arka planlar için her zaman bir odak noktası ayarlayın, böylece en önemli görsel kısmı tüm ekran boyutlarında görünür kalır.
- Yukarıda kalan içerik gibi yükleme hızı kritik olan bölümlerde, görsellerden ziyade renk veya gradyan arka planlarını tercih edin.
- Video arka planlarını mobil cihazlarda test edin — çoğu mobil tarayıcı, videonun oynanması yerine poster görüntüsünü gösterecektir.