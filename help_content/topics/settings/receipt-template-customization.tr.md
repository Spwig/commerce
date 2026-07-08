---
title: Fatura Şablonu Özelleştirme
---

Fatura şablonları, POS terminallerinizde basılan termal faturaların görünümünü ve içeriğini kontrol eder. Başlık ve altbilgi metnini özelleştirin, logonuzu ekleyin, uygunluk alanlarını (vergi kimlikleri, iş kayıt numaraları) yapılandırın ve promosyonel QR kodlarını dahil edin. Şablonlar hedefleme kapsamı destekler - tüm mağazalar için bir varsayılan şablon oluşturun, bölgelere özel şablonlar oluşturun veya bireysel konumlara özel şablonlar oluşturun. Sistem, bir fatura basıldığında hangi şablonın uygulanacağını belirlemek için kapsam önceliği kurallarını kullanır.

Fatura şablonlarını marka tutarlılığını korumak, bölgesel uygunluk gereksinimlerini karşılamak ve promosyonel öğeler aracılığıyla müşteri etkileşimini artırmak için kullanın.

![Fatura Şablonu Listesi](/static/core/admin/img/help/receipt-template-customization/receipt-list.webp)

## Fatura Şablonu Temelleri

Fatura şablonları, ESC/POS termal yazıcılar tarafından basılan faturaların yapısını ve içeriğini tanımlar. Her şablon şu şekilde belirler:

**Fiziksel Yapılandırma**:
- Kağıt genişliği (58mm veya 80mm)
- Logo resmi (termal basım için monokrom)
- Yazı boyutu ve aralığı

**İçerik Bölümleri**:
- Başlık metni (mağaza adı, adres, iletişim bilgisi)
- Dinamik işlem verileri (ürünler, fiyatları, toplamlar, ödeme yöntemleri)
- Altbilgi metni (iade politikası, teşekkür mesajı, sosyal medya)
- Uygunluk alanları (vergi kimlikleri, iş kayıt numaraları)
- Etiketle birlikte promosyonel QR kodu

**Kapsam Hedefleme**:
- Varsayılan şablon (tüm mağazalara uygulanır, aksi halde geçersiz kılınır)
- Grup şablonu (bir gruptaki tüm mağazalara uygulanır)
- Mağaza şablonu (belirli bir mağaza/depoya uygulanır)

## Kapsam Öncelik Kuralları

Bir terminal fatura basar basmaz, sistem şu hiyerarşiyi kullanarak bir şablon seçer (en yüksek öncelikten en düşük öncelik):

| Öncelik | Kapsam | Örnek | Kullanım Durumu |
|----------|-------|---------|----------|
| **1** | Mağaza özel | Paris Mağaza şablonu | Fransa vergi uygunluk gereksinimlerine özel |
| **2** | Grup özel | Avrupa Mağazaları şablonu | Tüm Avrupa konumları için KDV gösterimi |
| **3** | Varsayılan | Global şablon | Tüm yapılandırılmamış mağazalar için varsayılan |

**Nasıl Çalışır**:
1. Mağazanın özel bir şablonu (depo özel) olup olmadığını kontrol edin
2. Yoksa, mağazanın grubunun grup şablonu olup olmadığını kontrol edin
3. Yoksa, varsayılan şablonu kullanın

**Örnek**:
- Varsayılan şablon: "Standard Fatura" (kapsam ataması yok)
- Grup şablonu: "EU Fatura" (Avrupa Mağazaları grubuna atandı) - KDV kaydı içerir
- Mağaza şablonu: "Paris Faturası" (Paris deposuna atandı) - Fransız SIRET numarası içerir

**Sonuç**:
- Paris Mağaza terminali: "Paris Faturası" kullanır (en özelleştirilmiş)
- Berlin Mağaza terminali (Avrupa Mağazaları grubunda, mağaza şablonu yok): "EU Faturası" kullanır (grup seviyesi)
- New York Mağaza terminali (grup yok, mağaza şablonu yok): "Standard Fatura" kullanır (varsayılan geri dönüş)

## Kağıt Genişliği Yapılandırması

Termal fatura yazıcıları ya 58mm ya da 80mm kağıt genişliği kullanır. Yazıcınızın donanımına göre seçim yapın:

| Kağıt Genişliği | Satır Başında Karakter Sayısı | En Uygun | Tipik Kullanım |
|-------------|---------------------|----------|-------------|
| **58mm** | ~32 karakter | Küçük ayak izi, taşınabilir | Yiyecek kamyonları, mobil POS, kiosklar |
| **80mm** | ~48 karakter | Standart perakende | Çoğu perakende mağazası, restoranlar |

**Genişlikler karıştırılamaz**: Aynı şablonu kullanan tüm terminaller aynı kağıt genişliği yazıcıya sahip olmalıdır. Karışık yazıcı türleriniz varsa, her genişlik için ayrı şablonlar oluşturun.

**Logo Boyut Sınırlamaları**:
- **58mm**: Maksimum genişlik 384 piksel (önerilen: 350px)
- **80mm**: Maksimum genişlik 576 piksel (önerilen: 550px)

Maksimum genişliği aşan logolar otomatik olarak ölçeklendirilir, bu da kaliteyi azaltabilir.

## Logo Yapılandırması

Fatura logoları, termal yazıcı uyumluluğu için **monokrom** (yalnızca siyah ve beyaz) olmalıdır:

**Logo Gereksinimleri**:
- Dosya formatı: PNG, JPG veya WebP
- Renk modu: Monokrom (siyah pikseller beyaz arka plan üzerinde)
- Önerilen boyutlar:
  - 58mm kağıt: 350px genişlik × 100-150px yükseklik
  - 80mm kağıt: 550px genişlik × 150-200px yükseklik
- Dosya boyutu: <100KB (termal yazıcılar sınırlı hafızaya sahiptir)

**Monokrom Logo Oluşturma**:
1. Düzenli logosunuza başlayın (renkli veya gri tonlu)
2. Resim düzenleyiciyi kullanarak siyah ve beyaza dönüştürün (gri tonlar yok)
3. Kontrastı artırın, siyah öğelerin katı olduğundan emin olun
4. Şeffaf veya beyaz arka planla birlikte PNG olarak dışa aktarın

**Logo Konumlandırma**:
- Her zaman yatay olarak merkezli
- Faturanın üst kısmında (başlık metninin üstünde)
- Otomatik boşluk ile takip edilir (içerikle çakışmayı önler)

**Logo Seçimi**:
- Şablon formunda **Medya Kütüphanesi'ni Gözat**'a tıklayın
- Monokrom logo varlığı seçin
- Önizleme, logo'nun faturada nasıl görüneceğini gösterir

**Logo Yok**: Logo alanını boş bırakın, yalnızca metin markalama tercih ediyorsanız (başlık metni mağaza adını içerebilir).

## Başlık Metni

Başlık metni, logo'nun hemen ardından (logo yoksa en üstte) görünür. Tipik içerik:

**Mağaza Adı ve Adres**:
```
Mağaza Adınız
123 Main Street
Şehir, Eyalet 12345
Telefon: (555) 123-4567
```

**İş Saatleri**:
```
 Pazartesi-Cuma: 9:00-21:00
 Cumartesi-Pazar: 10:00-18:00
```

**Slogan veya Tagline**:
```
Kaliteli Ürünler, Özenli Hizmet
```

**Biçimlendirme**:
- Bilgiyi ayırmak için satır atlamaları kullanın
- Otomatik olarak ortalanır
- Satırları kağıt genişliği için karakter sınırına uydurun (58mm için 32 karakter, 80mm için 48 karakter)

**Kullanılabilir Değişkenler** (isteğe bağlı):
- `{store_name}` - Depo adıyla değiştirilir
- `{order_date}` - İşlem tarihiyle değiştirilir
- `{order_number}` - Sipariş kimliğiyle değiştirilir

Çoğu satıcı başlık tutarlılığı için statik metin yerine değişkenleri kullanır.

## Altbilgi Metni

Altbilgi metni, işlem detayları (ürünler, toplamlar, ödeme) sonra görünür. Tipik içerik:

**İade Politikası**:
```
30 gün içinde fatura ile iade
Sadece mağaza kredisi veya değiştirme
```

**Teşekkür Mesajı**:
```
Bize alışverişiniz için teşekkür ederiz!
Bizi takip et @yourstore
```

**Müşteri Hizmeti**:
```
Sorularınız varsa, (555) 123-4567 numarasını arayın
veya support@yourstore.com adresine e-posta gönderin
```

**Biçimlendirme İpuçları**:
- En önemli bilgileri önce yerleştirin (iade politikası, iletişim)
- Okunabilirlik için satır atlamaları kullanın
- Bölümler arasında ayırıcı çizgi (`---`) eklemeyi düşünün

## Uygunluk Alanları

Çoğu yer, faturalarda özel bilgileri gerektirir:

**Vergi Kimlik Etiketi** - Vergi kimlik numarası için özelleştirilebilir etiket:
- ABD: "Vergi Kimliği" veya "EIN"
- AB: "KDV Numarası" veya "KDV Kayıt No"
- Kanada: "GST/HST Numarası"
- Avustralya: "ABN"

**Vergi Kimlik Değeri** - Gerçek kimlik numarası:
- Şablon içinde bir kez girilir, tüm faturalarda görünür
- Örnek: "KDV Numarası: GB123456789"

**İş Kayıt Etiketi** - İş kaydı için özelleştirilebilir etiket:
- Fransa: "SIRET"
- Almanya: "Handelsregister"
- Birleşik Krallık: "Şirket Kayıt Numarası"

**İş Kayıt Değeri** - Gerçek kayıt numarası:
- Örnek: "SIRET: 123 456 789 00010"

**Spwig Tarafından Güçlendirildi** - "Spwig Tarafından Güçlendirildi" markalama gösterilmesi için anahtar:
- Varsayılan olarak etkin (platform geliştirme destekler)
- Beyaz etiketli operasyonlar için devre dışı bırak

**Bölgeye Göre Uygunluk Örnekleri**:

**Avrupa Birliği**:
- Vergi Kimlik Etiketi: "KDV Numarası"
- Vergi Kimlik Değeri: "GB123456789"
- Ülkeye göre şirket kayıt numarasını gösterin

**Birleşik Devletler**:
- Genellikle fatura vergi kimlik gereksinimi yoktur (devletler arasında değişir)
- B2B işlemleri için EIN dahil edilebilir

**Fransa (Özel)**:
- Tüm faturalarda zorunlu SIRET
- İş Kayıt Etiketi: "SIRET"
- İş Kayıt Değeri: "123 456 789 00010"

**Avustralya**:
- GST kayıtlı işletmeler için ABN önerilir
- Vergi Kimlik Etiketi: "ABN"

Göndermeden önce yerel yerin fatura gereksinimlerini kontrol edin.

## QR Kodu Promosyonları

Faturaların altına QR kodu ekleyerek müşteri etkileşimini artırın:

**QR Kodu URL'si** - Taranıldığında hedef:
- Değerlendirme talebi: `https://yourstore.com/reviews/leave-review`
- Loyalite programı: `https://yourstore.com/loyalty/join`
- Bir sonraki satın alma indirimi: `https://yourstore.com/discount/THANKYOU`
- Sosyal medya: `https://instagram.com/yourstore`
- Web sitesi anasayfası: `https://yourstore.com`

**QR Kodu Etiketi** - QR kodunun üstünde görünen metin:
- "Değerlendirme bırakın ve bir sonraki alışverişinizde %10 indirim alın"
- "Loyalite programımıza katılmak için burayı tara"
- "Instagram'da bizi takip et - burayı tara ve bağlan"
- "Deneyiminizi değerlendirin"

**QR Kodu En İyi Uygulamalar**:
- Kısa URL'ler kullanın (uzun URL'ler yoğun ve tarama zorlu kodlar oluşturur)
- Dağıtım öncesi QR kodunu birden fazla telefon kamera ile test edin
- Etikette net değer önerisi ekleyin (kullanıcının tarama karşılığı ne alacağı)
- QR kodu taramalarını izleyerek etkinliğini ölçün (izleme parametresiyle URL kullanın)

**Dinamik QR Kodları** (Gelişmiş):
- Kısaltma hizmeti (bit.ly, tinyurl) kullanarak kısa URL oluşturun
- Mevsimsel olarak farklı hedeflere yönlendirin, faturaları yeniden basmanıza gerek kalmadan
- Örnek: `https://bit.ly/yourstoreqr` → mevcut promosyona yönlendirir

## Farklı Kapsamlar İçin Şablonlar Oluşturma

**Varsayılan Şablon** (önerilen başlangıç noktası):
1. **POS > Fatura Şablonları**'na gidin
2. **+ Fatura Şablonu Ekle**'ye tıklayın
3. **Depo** ve **Mağaza Grubu** alanlarını boş bırakın (bu, varsayılan şablonu yapar)
4. Kağıt genişliğini, en yaygın yazıcı türünüzle eşleşecek şekilde yapılandırın
5. Logo, başlık, altbilgi ekleyin
6. Ana pazarınız için uygunluk alanlarını yapılandırın
7. Kaydedin

Bu şablon, tüm mağazalara uygulanır, aksi halde geçersiz kılınır.

**Grup Şablonu** (bölgesel farklılıklar için):
1. Yeni şablon oluşturun
2. **Mağaza Grubu**'nu seçin (örneğin, "Avrupa Mağazaları")
3. **Depo** alanını boş bırakın
4. Bölgenin uygunluk alanlarını ayarlayın (örneğin, KDV biçimlendirme)
5. Başlık metnini ayarlayın (örneğin, bölgesel adres)
6. Kaydedin

Bu şablon, gruptaki tüm mağazalara uygulanır.

**Mağaza Şablonu** (konum özel ihtiyaçlar için):
1. Yeni şablon oluşturun
2. **Depo**'yu seçin (örneğin, "Paris Mağazası")
3. Bu özel konum için tüm alanları ayarlayın
4. Kaydedin

Bu şablon, bu bir mağazaya uygulanır.

**Şablonları Test Etme**:
- Terminalde test işlemi yapın
- Faturayı basın
- Logo netliği, metin hizalaması, uygunluk alanları, QR kodu tarama yeteneğini doğrulayın
- Gerekirse şablonu düzenleyin ve tekrar test edin

## Ortak Fatura Düzenleri

**Minimum Fatura** (yiyecek kamyonları, pop-up):
- Logo yok (alan tasarrufu)
- Başlık: Mağaza adı ve telefon numarası sadece
- Altbilgi: Teşekkür mesajı
- QR kodu yok

**Standart Perakende Faturası**:
- Logo (monokrom marka işareti)
- Başlık: Tam mağaza adı, adres, saatler
- Uygunluk: Vergi kimliği
- Altbilgi: İade politikası, teşekkür mesajı
- QR kodu: Değerlendirme talebi

**Premium Perakende Faturası**:
- Logo (tam marka kelime işareti)
- Başlık: Slogan, adres, iletişim
- Uygunluk: Vergi kimliği, iş kaydı
- Altbilgi: İade politikası, müşteri hizmeti, sosyal medya
- QR kodu: Loyalite programı kaydı

**Çok Konumlu Zincir**:
- Varsayılan şablon: Şirket markalama, standart politikalar
- Grup şablonları: Bölgesel uygunluk (AB için KDV, Kanada için GST)
- Mağaza şablonları: Konum özel adres ve telefon

## Birden Fazla Şablonu Yönetme

**Şablon Adlandırma Kuralları**:
- Adında kapsamı kullanın: "Varsayılan Fatura", "AB Grubu Faturası", "Paris Mağaza Faturası"
- Liste incelemesi sırasında hangi şablonun nerede uygulanacağını belirlemeye yardımcı olur

**Şablon Değişiklikleri**:
- Değişiklikler gelecekteki faturalara hemen uygulanır
- Geçmiş faturalar (zaten basılmış) etkilenmez
- Tüm mağazalara dağıtmadan önce düşük trafiğe sahip terminalde değişiklikleri test edin

**Şablon Kopyalama**:
- Mevcut bir şablondan benzer yeni bir şablon oluşturuyorsanız, mevcut şablonu kopyalayın ve düzenleyin
- Sıfırdan başlamaktan kaçının

**Şablon Silme**:
- Terminaller varken varsayılan şablonu silemezsiniz (en az bir geri dönüş noktası olmalıdır)
- Grup/mağaza şablonlarını silebilirsiniz (terminaller hiyerarşinin bir sonraki seviyesine geri döner)
- Şablonu silmeden önce aktif olarak kullanılıp kullanılmadığını onaylayın

## İpuçları

- **Emniyetle 80mm kullanın** - Standart kağıt genişliği çoğu perakende için çalışır; 58mm özeldir
- **Gerçek yazıcıda logo testi yapın** - Ekran da iyi görünen logo, yazdırıldığında kötü görünebilir; erken test edin
- **Uygunluk alanlarını güncel tutun** - Faturalardaki süresiz vergi kaydı, yasal sorunlara neden olabilir
- **Değer önerisi ile QR kodları daha iyi tarama** - "%10 indirim için tara" "Burayı tara" ile 10 kat daha iyi performans gösterir
- **Karakter sınırlarını gözden geçirin** - Metin sarmalama biçimlendirmeyi bozar; dağıtım öncesi satır başına karakter sayısını sayın
- **Her kağıt genişliği için bir şablon** - 58mm yazıcıya 80mm şablonu ataymayın (logo sığmaz)
- **Aylık test faturaları basın** - Yazıcılar zamanla bozulur; kalitenin hala kabul edilebilir olduğundan emin olun
- **Değişkenleri az kullanın** - Statik metin, dinamik değişkenlerden daha güvenilir (daha az hata noktası)
- **Şablon yapılandırmasını yedekleyin** - Önemli değişikliklerden önce şablon ayarlarını ekran görüntüsü alın veya dışa aktarın (kolay geri dönüş)
- **Bölgesel uygunluk değişir** - Dağıtım öncesi yerel fatura gereksinimlerini araştırın; uygunluk eksikliği ciddi cezalara neden olabilir

