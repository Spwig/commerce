---
title: Sosyal Paylaşım
---

Sosyal paylaşım butonları, müşterilerin ürünlerinizi, blog gönderilerinizi ve sayfalarınızı doğrudan mağazanızdan sosyal ağlara paylaşmasına olanak tanır. Butonların hangi platformlarda görüneceğini, nasıl görüneceğini, nerede yer alacağını ve paylaşım etkinliğinin izlenecek ve sayılacağına karar verirsiniz.

## Sosyal paylaşım ayarlarını yapılandırma

Tüm sosyal paylaşım davranışları tek bir ayar sayfasından kontrol edilir. **Pazarlama > Sosyal Paylaşım Ayarları**'na gidin (sayfa otomatik olarak ayar formuna yönlendirilir — sadece bir ayar kaydı vardır).

### Konum: butonların nerede görüneceği

**Konum** bölümü, paylaşım butonlarının hangi içerik türlerinde otomatik olarak görüneceğini kontrol eder.

| Ayar | Açıklama |
|---------|-------------|
| **Ürünlerde Etkinleştir** | Ürün detay sayfalarında paylaşım butonlarını göster |
| **Kategorilerde Etkinleştir** | Kategori listeleme sayfalarında paylaşım butonlarını göster |
| **Blog Gönderilerinde Etkinleştir** | Blog gönderi sayfalarında paylaşım butonlarını göster |
| **Özel Sayfalarda Etkinleştir** | Özel mağaza sayfalarında paylaşım butonlarını göster |

Butonların görüneceği içerik türlerini seçin. Herhangi bir kombinasyonu etkinleştirebilirsiniz — örneğin sadece ürünler ve blog gönderileri.

**Konum Pozisyonu**, butonların sayfada nerede görüneceğini kontrol eder:

| Seçenek | Açıklama |
|--------|-------------|
| **İçerik Altında** (varsayılan) | Ana içerikten sonra gösterilir |
| **İçerik Üzerinde** | Ana içerikten önce gösterilir |
| **Yan Menü** | Sayfa yan menüsinde gösterilir |
| **Yoklukta (sabit)** | Ziyaretçi kaydırırken ekranın yan tarafına yapışır |

### Görünüm: butonların nasıl görüneceği

**Görünüm** bölümü, hangi platformların gösterileceğini ve butonların nasıl stillendirileceğini kontrol eder.

**Etkinleştirilmiş Platformlar** — boş bırakılırsa tüm desteklenen platformlar gösterilir, ya da bir JSON dizi girmek suretiyle hangi platformların görüneceğini kısıtlayabilirsiniz:

```json
["facebook", "twitter", "pinterest", "whatsapp", "email"]
```

Desteklenen platform anahtarları: `facebook`, `twitter`, `linkedin`, `pinterest`, `whatsapp`, `telegram`, `email`

**Buton Stili** seçenekleri:

| Stil | Açıklama |
|-------|-------------|
| **Sadece Simge** (varsayılan) | Sadece platform simgesi gösterilir |
| **Simge + Etiket** | Simge ve platform adı gösterilir |
| **Sadece Etiket** | Sadece platform adı olarak metin gösterilir |

**Buton Boyutu** — tasarımınıza uygun **Küçük**, **Orta** (varsayılan) veya **Büyük** boyut seçin.

**Düzen Yönü** — butonları **Yatay** (varsayılan, yan yana) veya **Dikey** (yığın halinde) olarak düzenleyin.

**Başlık Göster** — işaretliyken, buton grubunun üstünde "Paylaş" başlığı görünür.

**Mobil Görünürlük**, küçük ekranlarda butonların görünümünü kontrol eder:

| Seçenek | Açıklama |
|--------|-------------|
| **Her Zaman Göster** (varsayılan) | Tüm cihazlarda butonlar görünür |
| **Mobilde Gizle** | Mobil cihazlarda butonlar gizlenir |
| **Sadece Mobil** | Butonlar sadece mobil cihazlarda görünür |

### Takip Ayarları

**Paylaşım Sayılarını Göster** — işaretliyken, her butonun üzerinde o platformun kaç kez paylaşımı olduğunu gösteren bir sayı etiketi görünür. Sayılar paylaşım kaydedildikçe anlık olarak güncellenir.

**Paylaşımı Takip Et** — işaretliyken, her paylaşım tıklaması paylaşım analitiklerinde kaydedilir. Bu seçeneği devre dışı bırakmak yeni kayıtların kaydedilmesini durdurur ancak mevcut verileri silmez. Takip ayrıca, paylaşım yapan müşterilere (loyalty programı aktifse) sadakat etiketleri verir.

Formun altındaki **Kaydet**'e tıklayarak değişikliklerinizi uygulayın. Ayarlar hemen etkin olur.

## Paylaşım Etkinliklerini Görüntüleme

### Bireysel paylaşım olayları

**Pazarlama > Sosyal Paylaşım**'a giderek kaydedilen her paylaşım olayının bir kaydını görebilirsiniz. Her giriş şu bilgileri gösterir:

- **Platform** — kullanılan sosyal ağ (renk kodlu bir etiket olarak gösterilir)
- **Paylaşılan İçerik** — paylaşılan içerik türü ve adı (örneğin, `ürün: Mavi Cihaz`)
- **Kullanıcı** — paylaşım yapan müşteri veya "Anonim" (giriş yapmamış ziyaretçiler için)
- **Cihaz Türü** — masaüstü, mobil veya tablet
- **Paylaşıldığı Zaman** — paylaşımın tarihi ve zamanı

Paylaşım günlüğü salt okunur — girişler, müşterilerin paylaşım butonlarını tıkladığında otomatik olarak oluşturulur.

Platform ve Cihaz Türü filtrelerini kullanarak paylaşım desenlerini keşfedin ve tarih hiyerarşisini kullanarak belirli zaman dönemlerini inceleyin.

### İçeriklere Göre Paylaşım Sayıları

**Pazarlama > Paylaşım Sayıları**'na giderek, içerik öğesi ve platforma göre toplu şekilde gruplandırılmış toplam paylaşım sayılarını görün. Bu görünüm, en çok paylaşılan ürünlerinizi ve gönderilerinizi tanımlamayı kolaylaştırır.

Her girdi şu bilgileri gösterir:
- **İçerik** — öğenin türü ve adı (örneğin, `ürün: Mavi Cihaz`)
- **Platform** — sosyal ağ
- **Paylaşım Sayısı** — o platformda kaydedilen toplam paylaşım sayısı
- **Son Güncellenme** — sayının son kez yeniden hesaplandığı zaman

Liste, paylaşım sayısına göre azalan şekilde sıralanmıştır, bu nedenle en viral içerikleriniz en üstte yer alır. Paylaşım sayıları, yeni bir paylaşım olayı kaydedildiğinde otomatik olarak güncellenir — bunları elle yenileme ihtiyacı yoktur.

## Paylaşımların Nasıl Takip Edildiğini Anlamak

Müşteri bir paylaşım butonuna tıkladığında, Spwig şu bilgileri kaydeder:

1. Hangi platformda paylaşım yapıldığını
2. Hangi içerik paylaşıldığını (ürün, blog yazısı, sayfa vb.)
3. Müşterinin oturum açmış olup olmadığını (eğer öyleyse, paylaşım onun hesabına bağlanır ve sadakat entegrasyonu için kaydedilir)
4. Kullanıcının cihaz türünü
5. Paylaşılan URL'yi

O platform ve içerik öğesi için paylaşım sayısı otomatik olarak artırılır. Eğer **Paylaşım Sayılarını Göster** etkinse, sayfa yenilendiğinde buton üzerinde güncellenmiş sayı görünür.

## Sadakat Entegrasyonu

Sadakat programınız aktif ve **Paylaşımları Takip Et** etkinse, oturum açmış müşteriler içerik paylaşımında sadakat puanları kazanır. Sosyal paylaşım puanı, sadakat programının eylem tabanlı kurallarının bir parçasıdır.

Puan verme kurallarını yapılandırmak için **Müşteriler > Sadakat Kuralları**'na gidin ve **Eylem Tabanlı** türünde ve **Sosyal Paylaşım** eylem türünde kuralları arayın.

## İpuçları

- Ürünler ve blog yazılarını paylaşımı ilk olarak etkinleştirin — bu içerik türleri müşterilerin en çok organik olarak paylaşmakta olduğu içeriklerdir
- Pinterest, giyim, ev dekorasyonu ve yemek gibi görsel ürün kategorileri için özellikle değerlidir — bu mağazalarda `enabled_platforms` listesinde öncelikle Pinterest'i etkinleştirin
- WhatsApp paylaşımı, mobil cihazlarda sıcak referanslardan güçlü dönüşüm sağlar; WhatsApp için **Sadece Mobil** görüntüleme modunu kullanırken diğer platformları tüm cihazlarda görünür tutmayı düşünün
- Paylaşım sayılarının şişkin olduğunu fark ederseniz, **Yönetici Trafığı** bayrağı tam olarak işlevselleştirilmeden önce test trafikinin (yönetici oturumlarından) sayıldığına bakın — paylaşım analitiğinden girdileri temizleyerek sayılara sıfırlama yapabilirsiniz
- Ayda bir kez Paylaşım Sayıları listesini gözden geçirerek en çok paylaşılan ürünleri belirleyin ve onları anasayfada veya pazarlama e-postalarında daha öne çıkarın