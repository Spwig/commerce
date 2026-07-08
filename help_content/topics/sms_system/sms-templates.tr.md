---
title: SMS Şablonları
---

SMS şablonları, mağazanızın müşterilere SMS yoluyla gönderdiği tüm bildirimlerin metnini kontrol eder. Her şablon, bir sipariş onayı veya sevkiyat güncellemesi gibi belirli bir olayla ilişkilidir ve Spwig, mesaj gönderilirken bu şablonlarda yer alan {değişken} yer tutucularını gerçek sipariş detaylarıyla değiştirir.

**SMS Sistemi > SMS Şablonları**'na giderek şablonlarınızı görüntüleyebilir ve düzenleyebilirsiniz.

![SMS şablonları listesi](/static/core/admin/img/help/sms-templates/templates-list.webp)

## Kullanılabilir şablon türleri

Spwig, aşağıdaki yerleşik şablon türlerini içerir:

| Şablon Türü | Ne zaman gönderilir |
|---------------|-----------------|
| Sipariş Onayı | Bir müşteri bir sipariş verdiğinde |
| Sevkiyat Güncellemesi | Bir siparişin takip durumu değiştiğinde |
| Teslimat Bildirimi | Bir sipariş teslim edildiğinde |
| Şifre Sıfırlama | Bir müşteri şifre sıfırlama isteğinde bulunduğunda |
| Doğrulama Kodu | Hesap doğrulaması için tek seferlik bir kod gerekli olduğunda |
| POS Faturası | Bir satış noktası terminalinde bir satış işlemi yapıldığında |
| Pazarlama | Pazarlama kampanyaları için (ayrı bir onay gerekir) |
| Özel | Kendi oluşturduğunuz herhangi bir bildirim için |

## Şablonu Düzenleme

1. **SMS Sistemi > SMS Şablonları**'na gidin
2. Düzenlemek istediğiniz şablonu tıklayın
3. **Mesaj** alanını istenen metinle güncelleyin
4. {değişken} yer tutucularını kullanarak sipariş özel bilgilerini ekleyin (aşağıdaki değişkenleri görün)
5. **Aktif** kutusunu işaretleyerek şablonu etkinleştirin — etkin olmayan şablonlar gönderilmemektedir
6. **Kaydet**'e tıklayın

![Bir SMS şablonunu düzenleme](/static/core/admin/img/help/sms-templates/template-edit.webp)

## Değişkenleri Kullanma

Değişkenler, {değişken} gibi süslü parantezler içinde yazılan yer tutuculardır. Spwig, mesajı gönderdiğinde her bir yer tutucuyu ilgili müşteri veya sipariş için gerçek değere değiştirir.

### Yaygın Değişkenler

| Değişken | Değiştirilir |
|----------|---------------|
| `{name}` | Müşterinin adı |
| `{order_number}` | Sipariş referans numarası |
| `{total}` | Sipariş toplam tutarı |
| `{tracking_number}` | Sevkiyat takip numarası |
| `{store_name}` | Mağazanızın adı |
| `{code}` | Doğrulama veya sıfırlama kodu |

**Örnek mesaj:**

```
Merhaba {name}, siparişiniz #{order_number} onaylandı. Toplam: {total}. Sevkiyat yapıldığında size bilgi vereceğiz. - {store_name}
```

Gönderildiğinde bu şu hale gelir:

```
Merhaba Sarah, siparişiniz #10045 onaylandı. Toplam: $89.00. Sevkiyat yapıldığında size bilgi vereceğiz. - The Garden Shop
```

> Belirli bir şablon türü için kullanılabilir olan değişkenleri yalnızca ekleyin. Örneğin, {tracking_number} Sevkiyat Güncellemesi şablonunda kullanılabilir ancak Şifre Sıfırlama şablonunda kullanılamaz. Kullanılamayan bir değişken kullanırsanız, mesajda olduğu gibi (değiştirilmemiş) görünür.

## Karakter Sınırları ve Mesaj Uzunluğu

Standart SMS mesajları, tek bir segment için **160 karakter** sınırına sahiptir. Daha uzun mesajlar, birden fazla segmente bölünür ve birleştirilmiş SMS olarak gönderilir, ancak operatörler her segmenti ayrı ayrı faturalandırır.

**Sınıra uymak için ipuçları:**
- Mesajları kısa tutun — her mesajda bir amaç olsun
- Doğal görünen yaygın ifadeleri kısaltın (örneğin, "Ord" yerine "Order")
- Gerekmedikçe gereksiz doldurucu kelimelerden kaçının

Spwig, düzenleyicide zorunlu bir karakter sınırı uygulamaz, bu yüzden kaydetmeden önce karakter sayısını (değişken değerlerini de dahil ederek) sayın.

## Şablonları Etkinleştirme ve Devre Dışı Bırakma

Her şablon üzerindeki **Aktif** anahtar, o bildirim türünün gönderilip gönderilmeyeceğini kontrol eder. Eğer bir şablon etkin değilse, Spwig o bildirimi tamamen göndermez — mesaj SMS Çıkış Kutusunda **Atlandı** olarak görünür ve neden `template_inactive` olur.

Bir şablonu etkinleştirmek için:
1. Şablonu açın
2. **Aktif** onay kutusunu işaretleyin
3. Kaydedin

Bir şablonu devre dışı bırakmak (bildirim türünü göndermeyi durdurmak ancak şablonu silmek istememek için):
1. Şablonu açın
2. **Aktif** onay kutusunu kaldırın
3. Kaydedin

## İpuçları

Tüm markdown biçimlendirmesini, resim yollarını, kod bloklarını ve teknik terimleri koruyun.

- Markanızın aynı ses tonunu kullanın — SMS, doğrudan ve kişisel bir kanaldır, bu yüzden dostane bir ton iyi çalışır
- Mesajlarda daima mağazanızın adını ekleyin, böylece müşterilerinize kimin yazdığı anlaşılır olur
- Sipariş onay mesajlarını kısa tutun: sipariş numarası, toplam ve bir sonraki adımlar hakkında not yeterlidir
- Kendi mağazanızda bir test siparişi vererek (kontrol ettiğiniz bir telefon numarası kullanarak) müşterilerin ne aldığını tam olarak görmek için mesajları test edin
- Eğer bir bildirim karışıklığa veya şikayetlere neden oluyorsa, şablonu devre dışı bırakın ve onu silmek yerine yeniden düzenleyin — bu şekilde güncellendikten sonra tekrar etkinleştirebilirsiniz
- Pazarlama şablonları, çoğu ülkede telekomünikasyon düzenlemelerine göre SMS pazarlamasına açık olan müşterilere yalnızca gönderilmelidir