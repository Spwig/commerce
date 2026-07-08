---
title: AI SEO Üretici
---

AI SEO Üretici, ürününüz için meta başlıklar, meta açıklamaları ve diğer SEO içeriğini bir AI sağlayıcısı kullanarak otomatik olarak yazar. Her ürün için manuel olarak SEO metni yazmak yerine, tek bir eylemle doğruluğu ve optimize edilmiş içeriği topluca oluşturabilirsiniz.

Mağazanız, ürün verilerinizden deterministik olarak SEO içeriği oluşturan yerleşik bir SEO üreticiye sahiptir — harici API anahtarları gerekmez. Yeni kurulumlarda otomatik olarak ana sağlayıcı olarak ayarlanır.

Aktif olduğundan emin olmak için:

1. **Pazarlama > SEO Sağlayıcıları**'na gidin
2. Yerleşik sağlayıcının **ANA** ve **AKTİF** durumlu olduğundan emin olun
3. Eğer sağlayıcı listede görünmüyorsa, **+ SEO Sağlayıcı Hesabı Ekle**'ye tıklayın ve **Sağlayıcı Anahtarı** alanını `deterministic` olarak ayarlayın

## SEO üreticisinin nasıl çalıştığı

SEO üreticisi, ürününüzün adını, açıklamasını, kategorisini ve özniteliklerini okuyor ve yapılandırılmış AI sağlayıcısını kullanarak o ürüne özel SEO içeriği yazar. Oluşturulan içerik doğrudan ürünün SEO alanlarına kaydedilir.

Bir ürün için SEO içeriği, ürün düzenleme sayfasından oluşturulabilir ya da ürün listesindeki birden fazla ürün için toplu olarak oluşturulabilir.

## SEO sağlayıcısını ayarlama

### Yerleşik sağlayıcıyı kullanma

Mağazanız, ürün verilerinizden deterministik olarak SEO içeriği oluşturan yerleşik bir SEO sağlayıcısına sahiptir — harici API anahtarları gerekmez. Yeni kurulumlarda otomatik olarak ana sağlayıcı olarak ayarlanır.

Aktif olduğundan emin olmak için:

1. **Pazarlama > SEO Sağlayıcıları**'na gidin
2. Yerleşik sağlayıcının **ANA** ve **AKTİF** durumlu olduğundan emin olun
3. Eğer sağlayıcı listede görünmüyorsa, **+ SEO Sağlayıcı Hesabı Ekle**'ye tıklayın ve **Sağlayıcı Anahtarı** alanını `deterministic` olarak ayarlayın

### AI sağlayıcı bileşenini bağlama

Daha zengin ve bağlamaya dayalı SEO içeriği oluşturmak için, Spwig bileşen pazar yerinden bir AI sağlayıcı bileşeni (örneğin OpenAI veya Claude tabanlı bir sağlayıcı) yükleyebilirsiniz.

1. Bileşen güncelleme sistemi aracılığıyla sağlayıcı bileşenini yükleyin (mağaza yöneticinize danışın)
2. **Pazarlama > SEO Sağlayıcıları**'na gidin
3. **+ SEO Sağlayıcı Hesabı Ekle**'ye tıklayın
4. Formu doldurun:

**Sağlayıcı Bilgileri bölümü:**
- **Site** — mağazanızı seçin
- **Sağlayıcı Bileşeni** — yüklediğiniz AI sağlayıcı bileşenini seçin
- **Sağlayıcı Anahtarı** — bileşen tabanlı sağlayıcı kullanırken boş bırakın
- **Hesap Adı** — `OpenAI SEO Sağlayıcısı` gibi tanımlayıcı bir ad

**Ayarlar bölümü:**
- **AKTİF mi?** — bu sağlayıcıyı etkinleştirmek için işaretleyin
- **ANA mı?** — bu sağlayıcıyı tüm SEO üretimi için varsayılan sağlayıcı olarak kullanmak için işaretleyin
- **Öncelik** — düşük sayılar, öncelik sırasında önce denenecek sağlayıcılar için kullanılır
- **Ayarlar** — sağlayıcıya özel ayarlar olarak bir JSON nesnesi (örneğin, model adı, ton, dil)

5. **Kaydet**'e tıklayın

Yalnızca bir sağlayıcı ana olarak ayarlanabilir. Eğer yeni bir sağlayıcıyı ana olarak işaretlerseniz, önceki ana sağlayıcı otomatik olarak düşük öncelikli hale gelir.

### Sağlayıcı öncelik sırası

Eğer ana sağlayıcınız başarısız olursa (örneğin, API kesilmesi nedeniyle), mağazanız öncelik sırasına göre bir sonraki aktif sağlayıcıya otomatik olarak geçer. Bu, bir sağlayıcının geçici olarak kullanılamaması durumunda bile SEO üretiminin devam etmesini sağlar.

## Bir ürün için SEO içeriği oluşturma

### Bireysel ürün

1. **Ürünler > Ürünler**'e gidin ve herhangi bir ürünü açın
2. Ürün formunun **SEO** bölümünü kaydırın
3. **SEO Üret** butonuna tıklayın
4. AI sağlayıcısı, ürünün ayrıntılarına göre meta başlık ve meta açıklama oluşturur
5. Oluşturulan içeriği inceleyin ve gerekirse düzenleyin
6. Değişiklikleri uygulamak için **Kaydet**'e tıklayın

### Toplu üretim

Birden fazla ürün için SEO içeriği oluşturmak veya güncellemek için:

1. **Ürünler > Ürünler**'e gidin
2. Güncellemek istediğiniz ürünleri onay kutularıyla seçin veya tümünü seçin
3. **Eylem** açılır menüsünü açın
4. **SEO İçeriği Üret** (veya benzer eylem adı — açılır menüde tam etiketi kontrol edin) seçin
5. **Git**'e tıklayın

Spwig, üretim görevlerini kuyruğa alır ve arka planda işler. Birkaç dakika sonra ürün listesini yenileyin ve güncellenmiş SEO alanlarını görün.

## SEO kapsama inceleme

SEO üreticisi, hangi ürünlerin zaten SEO içeriği içerdiğini izler. SEO içeriği hâlâ gerekli olan ürünleri belirlemek için:

1.

**Ürünler > Ürünler**'e gidin
2.


SEO Durum filtresini (mevcut olduğunda) kullanarak eksik meta başlık veya açıklamalara sahip ürünleri gösterin
3.

Bu ürünleri seçin ve toplu üretim eylemini çalıştırın

## Sağlayıcı ayarları

Bir SEO sağlayıcı hesabı üzerindeki **Ayarlar** alanı, sağlayıcıya özel yapılandırmaları içeren bir JSON nesnesi kabul eder. Ortak seçenekler şunlardır:

```json
{
  "language": "en",
  "tone": "professional",
  "max_title_length": 60,
  "max_description_length": 160
}
```

Bu ayarlar sağlayıcı bileşenine göre değişebilir. Sağlayıcının belgelerine bakarak kullanılabilir seçeneklerin tam listesini inceleyin.

## Birden fazla sağlayıcıyı yönetme

Birden fazla SEO sağlayıcı hesabı yapılandırılmışsa, sağlayıcı listesi onların durumunu genel bir bakışla gösterir:

- **PRIMARY etiketi** — bu sağlayıcı, tüm SEO üretimi için varsayılan olarak kullanılır
- **ACTIVE etiketi** — sağlayıcı etkinleştirilmiştir
- **INACTIVE etiketi** — sağlayıcı devre dışı bırakılmıştır ve kullanılmayacaktır

Hangi sağlayıcının primary (öncelikli) olduğunu değiştirmek için, önceliklendirmek istediğiniz sağlayıcı hesabını açın, **Primary mi?** kutusunu işaretleyin ve kaydedin. Sistem, herhangi bir zaman yalnızca bir sağlayıcının primary bayrağını tutmasını garanti altına alır.

## İpuçları

- Yeni ürünler oluşturduğunuzda, onlar için SEO içeriğini hemen oluşturun — sadece birkaç saniye alır ve arama motorlarına hemen faydalı bir şey indexlemeleri için bir şey sağlar
- Ürünlerinizin adları anormal ya da teknikselse, yayınlandırmadan önce AI tarafından oluşturulan meta açıklamalarını gözden geçirin; üretici, açık ve tanımlayıcı ürün isimleriyle en iyi şekilde çalışır
- Sağlayıcı ayarlarında "max_title_length": 60 ve "max_description_length": 160 ayarlayarak Google'ın önerdiği karakter sınırlarında kalın
- Büyük bir ürün kataloğunu içeri aktardıktan sonra toplu SEO üretimini çalıştırın, böylece tüm SEO alanlarını hızlıca doldurabilirsiniz
- Ürün açıklamasını önemli ölçüde güncellediyseniz, SEO içeriğini yeniden oluşturun, böylece meta etiketlerini yeni metinle hizalayabilirsiniz
- Dahili deterministik sağlayıcı, başlangıç için iyi bir seçimdir; kataloğunuz kurulduktan ve daha zengin, daha doğal sesli SEO metni istiyorsanız, bir AI'li bileşene yükseltin