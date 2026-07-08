---
title: UI Çevirileri Yönetimi
---

UI Çevirileri sayfası, mağazanızın her dilinde ön uç arayüz metinlerinin—düğmeler, etiketler, hata mesajları ve diğer arayüz metinlerinin—görünümünü özelleştirmenizi sağlar. Ürün veya sayfa içerikleri çevirisinden farklı olarak, bu sabit arayüz öğeleridir ve müşterileriniz mağazanızda bunları sürekli görür. Markanızın sesini eşleştirmek için veya özel kitleleriniz için açıklığı artırmak için bunları özelleştirebilirsiniz.

Bu sayfa, tüm çevrilebilir UI metinlerini gösterir ve Spwig tarafından sağlanan varsayılan çevirileri geçersiz kılmanıza olanak tanır.

## UI Çevirilerini Anlamak

UI çevirileri, mağazanızın arayüzini oluşturan metinlerdir:

**UI Metinlerinin Örnekleri**:
- Düğmeler: "Add to Cart", "Checkout", "Search"
- Etiketler: "Price", "Quantity", "Shipping Address"
- Mesajlar: "Item added to cart", "Order confirmed", "Invalid email address"
- Gezinme: "Home", "Shop", "Contact Us"
- Form alanları: "Email", "Password", "First Name"

Spwig, tüm desteklenen dillerde yaklaşık 300 UI metni için varsayılan çeviriler içerir. UI Çevirileri sayfası, bu varsayılanları kendi özelleştirilmiş çevirilerinizle geçersiz kılmaya olanak tanır.

## UI Çevirilerini Neden Özelleştirmeli?

**Marka Sesiniz**: "Add to Cart" yerine "Buy Now" veya "Get Yours" gibi kendi marka kişiliğinize uyacak şekilde değiştirin

**Bölgesel Farklar**: Belirli pazarlar için çevirileri ayarlayın (İngilizce İngiltere vs. Amerikan İngilizcesi, Avrupa İspanyolcası vs. Latin Amerika İspanyolcası)

**Açıklık**: Varsayılan çeviri, ürününüz veya hedef kitleniz için mantıklı değilse, daha açık bir metinle değiştirin

**Sektöre Özel Terimler**: Müşterilerinizin beklentilerine uygun terimleri kullanın (örneğin, hizmet temelli mağazalar için "Book Appointment" yerine "Add to Cart")

## Metinleri Aramak

Özel UI metinlerini bulmak için arama kutusunu kullanın:

**İngilizce metinle arama**: "add to cart" yazarak bu düğmenin çevrilerini bulun

**Çeviriyle arama**: Herhangi bir dilde metin yazarak eşleşen çevirileri bulun

**Anahtarla arama**: Eğer çeviri anahtarını biliyorsanız (örneğin, `cart.add_item`), doğrudan onu arayın

Sayfa, yazarken anında güncellenir ve sadece eşleşen metinleri gösterir.

## Çeviri Detaylarını Görüntüleme

Her UI metni şu bilgileri gösterir:

**İngilizce Kaynak Metin** - Varsayılan İngilizce sürüm (referans noktası)

**Çeviri Anahtarı** - Kodda kullanılan iç tanımlayıcı (örneğin, `cart.add_to_cart`)

**Dil Sütunları** - Her etkin dil için mevcut çeviri

**Geçersizleştirme Durumu** - Çeviriyi özelleştirdiğiniz (geçersizleştirme yapıldıysa vurgulanır)

## Çeviri Geçersizleştirme Oluşturma

Bir UI metninin çevirisini özelleştirmek için:

1. **Metni bulun** (örneğin, "add to cart" arayın)
2. **Özelleştirmek istediğiniz dil hücresini tıklayın**
3. **Özelleştirilmiş çevirinizi** popup düzenleyicide girin
4. **Kaydedin** - Özelleştirme hemen etkinleşir

Orijinal varsayılan çeviri korunur - özelleştirme, önceliği sizinle olan bir geçersizleştirme oluşturur.

## Varsayılan Çevirilere Geri Dönme

Bir özelleştirilmiş geçersizleştirme kaldırıp varsayılan çeviriyi geri yüklemek için:

1. **Geçersizleme yapılan çeviriye tıklayın** (bu vurgulanır)
2. **Düzenleyicide "Varsayılan Çeviriye Geri Dön"** tıklayın
3. **Onaylayın** - Varsayılan çeviri hemen geri yüklenir

Diğer dillerdeki özelleştirmelerinizi etkilemeden bireysel dil geçersizleştirmelerini geri alabilirsiniz.

## Geçersizleştirme Durumuna Göre Filtreleme

Filtre açılır menüsünü kullanarak:

**Tüm Metinler** - Sistemdeki tüm UI metinleri (~300 toplam)

**Sadece Geçersizleştirilmişler** - Kendi özelleştirilmiş çevirilerinizi oluşturduğunuz metinler

**Sadece Varsayılanlar** - Spwig'ın varsayılan çevirilerini hala kullanan metinler

Bu, hangi metinleri özelleştirdiğinizi gözden geçirmenize ve eksiklikleri belirlemenize yardımcı olur.

## Ortak Özelleştirme Örnekleri

| İngilizce Varsayılan | Özelleştirilmiş Geçersizleştirme | Kullanım Durumu |
|----------------|----------------|----------|
| Add to Cart | Buy Now | Daha doğrudan çağrı yap |
| Checkout | Secure Checkout | Güvenliği vurgulamak |
| Search | Find Products | E-ticaret için daha spesifik |
| Contact Us | Get in Touch | Daha dostlu ton |
| Subscribe | Join Our Newsletter | Daha açık değer teklifi |

## Çeviri Doğrulama

Özelleştirilmiş çeviriler girdiğinizde doğrulayın:

**Uzunluk, UI alanına uyu** - Çeviriler İngilizce'den uzun ya da kısa olabilir (Almanca kelimeler genellikle daha uzundur, örneğin)

**Anlamı koru** - Çeviride işlevselliği değiştirmeyin ("Cancel" düğmesi "Delete" dememeli)

**Tutarlı terimler kullan** - Arayüzde tekrar eden terimler için aynı çeviri kullanın

**Uygun formaliteyi kullan** - Hedef pazarınızın tonuna uyun (formel vs. samimi)

## Çok Dilli Tutarlılık

Birden fazla dil için bir metni özelleştirmek istiyorsanız:

1. **Varsayılan diliyle başlayın** - Temelini ayarlayın
2. **Diğer dilleri özelleştirin** aynı niyeti koruyarak
3. **Her dilde test edin** düzenlemeyi ve anlamı doğrulayın
4. **Mümkünse yerli konuşanları kullanın** non-English özelleştirmeleri gözden geçirin

Diller arasında tutarsız özelleştirmeler, müşterilerinizi kışkırtıcı bir deneyim yaratır.

## Toplu Dışa Aktarma/İçeri Aktarma

Geniş kapsamlı özelleştirmeler için dışa aktarma/içeri aktarma iş akışını kullanın:

1. **Mevcut çevirileri JSON veya CSV olarak dışa aktarın**
2. **Yazılım tablosunda veya metin düzenleyicide düzenleyin** (toplu değişiklikler için daha kolay)
3. **Güncellenmiş çevirileri sistemde tekrar içeri aktarın**

Bu iş akışı, büyük ölçekli çeviri projelerini yönetmek için Çeviri İşleri sayfası üzerinden kullanılabilir.

## İpuçları

- **Özelleştirmeden önce arama yapın** - Düzenlediğiniz metnin doğru olduğundan emin olun; bazı benzer metinler farklı amaçlar için hizmet verir
- **Kaydetmeden sonra ön uçta test edin** - Özelleştirilmiş çevirinin gerçekten UI'da doğru şekilde görünür olduğundan emin olun
- **Çevirileri kısa tutun** - Düğmeler ve etiketler için genellikle daha kısa olanlar daha iyidir
- **Özelleştirmelerinizi belgeleyin** - Neden özel metinleri özelleştirdiğinizle ilgili notlar tutun, gelecekteki referanslar için
- **Tutarlı terimler kullanın** - Eğer "Cart"'ı "Basket" olarak özelleştiriyorsanız, ilgili tüm metinlerde bunu tutarlı şekilde kullanın
- **Mobil düzenlemeleri göz önünde bulundurun** - Uzun çeviriler küçük ekranlarda sarmalayabilir veya kısaltılabilir
- **Dil güncellemelerinden sonra gözden geçirin** - Spwig yeni varsayılan çeviriler eklerse, tutarlılığı korumak için bunları gözden geçirin ve özelleştirin

Unutmayın: Tüm markdown biçimlendirmesini, resim yollarını, kod bloklarını ve teknik terimleri gösterilen koruma kurallarına uygun şekilde koruyun.