---
title: Fiyat Çarpması Kuralları
---

Fiyat çarpması (bazı yerlerde psikolojik fiyatlandırma olarak da bilinir) ürün fiyatlarını, müşterilere daha çekici gelen belirli rakamlarla otomatik olarak ayarlar. Örneğin, $20.00 fiyatını göstermek yerine, fiyat çarpması $19.99 gibi daha düşük görünen bir fiyat gösterir — bu yaygın olarak kullanılan bir tekniktir.

Spwig, mağazanızda her para birimi için fiyat çarpması kurallarını otomatik olarak uygular, bu nedenle her kuralı yalnızca bir kez ayarlamanız yeterlidir.

## Fiyat çarpmasının nasıl çalıştığı

Bir ürün fiyatı hesaplandığında (promosyonlar veya indirimler sonrasında da dahil), Spwig o para birimi için aktif bir fiyat çarpması kuralının olup olmadığını kontrol eder. Eğer varsa, fiyat müşteriye gösterilmeden önce ayarlanır. Bu ayarlama, seçtiğiniz minimum eşik değerinden yüksek fiyatlara uygulanır.

Mağazanızın kabul ettiği her para birimi için ayrı ayrı kurallar yapılandırabilirsiniz. Örneğin, USD için `.99` bitimlerini kullanabilir, JPY için ise en yakın `¥10`'a yuvarlayabilirsiniz.

## Fiyat çarpması kuralı oluşturma

1. **Katalog > Fiyat Çarpması Kuralları**'na gidin
2. **+ Fiyat Çarpması Kuralı Ekle**'ye tıklayın
3. Bu kuralın uygulanacağı **Para Birimi**'ni seçin (örneğin, `USD`, `EUR`, `NZD`)
4. **Kural Türü**'nü seçin (aşağıdaki tabloya bakın)
5. Seçici olarak **Minimum Fiyat Eşik Değeri**'ni ayarlayarak çok düşük fiyatlı ürünler için çarpmayı atlayabilirsiniz
6. Ürünler satılıyken da çarpmayı uygulamak istiyorsanız, **Satış Fiyatlarına Uygula**'yı işaretleyin
7. **Aktif** kutusunun işaretli olduğundan emin olun
8. **Kaydet**'e tıklayın

Her para birimi için yalnızca bir kural olabilir. Bir kuralı değiştirmek istiyorsanız, mevcut olanı düzenleyin.

## Kural türleri

| Kural Türü | Örnek | En iyi uygulandığı yer |
|-----------|---------|----------|
| **.99 bitimi çarpması** | $20.50 → $19.99 | Çoğu perakende ürün — klasik psikolojik fiyat |
| **.95 bitimi çarpması** | $20.50 → $19.95 | .99 bitimine göre hafifçe daha yumuşak bir alternatif |
| **.90 bitimi çarpması** | $20.50 → $19.90 | Yuvarlak hissi verir ama bir sonraki doların altındadır |
| **Aşağıya Yuvarla** | $19.50 → $19.00 | Tam sayıları tercih eden mağazalar |
| **Yukarıya Yuvarla** | $19.50 → $20.00 | Temiz görüntü için hafifçe yukarı yuvarlama |
| **En yakın 5'e Yuvarla** | $23.00 → $25.00 | Yüksek trafiğe sahip perakende ve pazarlar |
| **En yakın 10'a Yuvarla** | $23.00 → $20.00 | Buzdolabı gibi daha yüksek fiyatlı ürünler |
| **En yakın 100'e Yuvarla** | $1,234 → $1,200 | Mobilya veya elektronik gibi yüksek değerli ürünler |
| **Özel bitim** | Herhangi biri — aşağıda belirtin | Markanızın özel bir bitimi kullanıyorsa, örneğin `.88` |

### Özel bitimler

**Özel bitim** seçerseniz, **Özel Bitim** alanına bitim değerini girin. Örneğin, `0.88` girerek tüm fiyatların `.88` bitiminde sona ermesini sağlayabilirsiniz (bazı Asya pazarlarında yaygın bir uygulamadır).

## Minimum fiyat eşik değeri

**Minimum Fiyat Eşik Değeri** alanını kullanarak, fiyat çarpmasının çok düşük fiyatlı ürünlerde uygulanmasını atlayabilirsiniz. Örneğin, eşik değerini `5.00` olarak ayarlarsanız, $5'ten düşük fiyatlı ürünlerin gerçek hesaplanan fiyatlarını, hiçbir çarpmayla gösterirsiniz.

`0` bırakarak tüm fiyatlara çarpmayı uygulayabilirsiniz.

## Satış fiyatları

Varsayılan olarak, çarpması hem normal hem de satış fiyatlarına uygulanır. Satış fiyatlarının tam olarak hesaplanan değerlerini göstermek istiyorsanız (örneğin, sınırlı süreli promosyon fiyatlarında tam rakamların önemli olduğu durumlarda), **Satış Fiyatlarına Uygula** kutusunu kaldırın.

## Kuralı devre dışı bırakma

Kuralları silmeden geçici olarak çarpmayı durdurmak istiyorsanız, **Aktif** kutusunu kaldırın ve kaydedin. Kural korunur ve herhangi bir zamanda yeniden etkinleştirilebilir.

## İpuçları

Tüm markdown biçimlendirmesini, resim yollarını, kod bloklarını ve teknik terimleri koruyun.

- Emir belirsizsen, .99 bitişli fiyatlarla başla — bu, en yaygın olarak tanınan psikolojik fiyatlandırma tekniğidir ve çoğu ürün türü için iyi çalışır.
- Düşük maliyetli ürün satarlarsan (5 doların altında), bir $3.50 ürünün $2.99’a düşmesini önlemek için bir minimum eşik ayarlayın.
- Yeni bir kural etkinleştirdikten sonra, mağazanın ön yüzünde bir ürün görüntüleyerek fiyatlarınızı kontrol edin — şarj edilmiş fiyatlar anında görüntülenir.
- Japon Yeni ve benzeri tam sayı para birimleri, **10’a Yuvarla** veya **100’e Yuvarla** ile en iyi şekilde çalışır, çünkü ondalık bitişler garip görünür.
- Fiyat şarjlaması, tüm indirimler ve kampanyalar uygulandıktan sonra yapılır, bu nedenle satış fiyatlarınız da şarjlanacaktır, ancak **Satış Fiyatlarına Uygula** seçeneğini kaldırırsanız bu durum değişebilir.
- Farklı para birimleri için farklı kural türlerine sahip olabilirsiniz, bu da farklı fiyatlandırma geleneklerine sahip birden fazla pazar için faydalıdır.