---
title: Müşteri Cüzdanı
---

Müşteri cüzdanı, her müşteri için çalışan bir bakiye takip sistemidir. Mağaza kredisi, iade, referans ödülleri, promosyon kampanyaları veya ekibiniz tarafından yapılan el ile ayarlamalar sonucu eklenebilir.

> **Cüzdan bakiyeleri ödeme sırasında harcanabilir.** Giriş yapmış bir müşteri, mağaza kredisine sahipse, bunu ödeme adımda görecektir ve tek bir tıklamayla uygulayabilir. Kredi, vergi ve kargo sonrası faturadan düşecek ve kalan tutar normal şekilde kartına yüklenir. Eğer kredi tüm siparişi kapsıyorsa, hiçbir kart gerekmez. Kredi uygulandığında rezerv edilir ve ödeme onaylandıktan sonra gerçekten düşer, bu nedenle terk edilen bir ödeme müşteriye hiçbir maliyet getirmez.

**Müşteriler > Müşteri Cüzdanları** menüsüne giderek cüzdanları görüntüleyebilir ve yönetebilirsiniz.

## Cüzdan bakiyelerini anlama

Her müşteri cüzdanı dört bakiye figürünü gösterir:

| Bakiye | Açıklama |
|---|---|
| **Kullanılabilir Bakiye** | Müşterinin mevcut ve kullanıma elverişli kredisi — bu, bu özellik aktif hale geldiğinde ödeme sırasında harcanabilecek tutar |
| **Bekleyen Bakiye** | Kullanılabilir bakiye haline gelmemiş krediler — örneğin, onay penceresi içinde olan bir iade |
| **Toplam Kredilendirme** | Bu cüzdana asla kredilendirilen toplam tutar, geçmiş tüm krediler dahil |
| **Toplam Kullanım** | Bu cüzdanın asla çekilen toplam tutar |

Kullanılabilir bakiye, ödeme harcaması aktif hale geldiğinde önemli olan rakamdır. Bekleyen krediler, bekleyen dönem sona erdiğinde kullanıma elverişli bakiyeye geçer.

## Müşteri cüzdanını görüntüleme

1. **Müşteriler > Müşteri Cüzdanları** menüsüne gidin
2. Ad ya da e-posta ile müşteriyi bulmak için arama alanını kullanın
3. Cüzdan girdisine tıklayarak detaylı görünümü açın

Detaylı görünüm, üstte mevcut bakiyeleri ve altta tam bir işlem geçmişini gösterir. **Son Kredilendirme Zamanı** ve **Son Kullanım Zamanı** zaman damgaları, cüzdanın son aktif olduğu zamanı gösterir.

### Cüzdan listesini filtreleme

**Aktif** filtresini kullanarak aktif cüzdanları donmuş olanlardan ayırabilirsiniz. Aktif olmayan bir cüzdan donmuş olur — bu cüzdana karşı kredi veya çekilmeler kaydedilemez, ancak bakiyesi korunur.

## İşlem geçmişini okuma

Her cüzdan bakiyesindeki değişiklik, bireysel bir işlem olarak kaydedilir. İşlem geçmişi, tam ve kalıcı bir defterdir — işlemler asla düzenlenmez veya silinmez. Bir hata düzeltilmesi gerekiyorsa, bunun yerine yeni bir dengeleyici işlem eklenir.

Her işlem şu alanları gösterir:

| Alan | Açıklama |
|---|---|
| **Tip** | Kredi, Çekme, Iade, Ayarlama veya Geri Alım |
| **Tutar** | Bu işlemin değeri (her zaman pozitif bir sayı olarak gösterilir) |
| **İşlem Sonrası Bakiye** | Bu işlem uygulandıktan hemen sonra cüzdan bakiyesi |
| **Kaynak** | Kredi veya çekmenin geldiği yer |
| **Durum** | Tamamlandı, Bekliyor veya Geri Alındı |
| **Açıklama** | İşlemin kısa bir açıklaması |
| **Referans Kimliği** | Kaynak kaydı (örneğin, bir sipariş numarası veya ödül kimliği) ile bağlantı kuran bir bağlantı |
| **Oluşturulma Zamanı** | İşlemin kaydedildiği zaman |

### İşlem tipleri açıklaması

- **Kredi** — cüzdana eklenen fonlar (iade, promosyon veya el ile ayarlama sonucu)
- **Çekme** — cüzdanından kaldırılan fonlar. Ödeme harcaması aktif hale geldiğinde bu, "bir siparişte harcanmış" anlamına gelecek — şu anda çekmenin tek yolu el ile ayarlama olacaktır
- **Iade** — iade edilmiş veya iptal edilmiş bir sipariş sonucu olarak özel olarak eklenen kredi
- **Ayarlama** — ekibiniz tarafından yapılan el ile düzeltme
- **Geri Alım** — daha önceki bir girdiyi iptal eden bir işlem

### İşlem kaynakları açıklaması

- **Sipariş Iadesi** — bir sipariş iade edildiğinde cüzdana verilen kredi
- **Referans Ödülü** — referans programı aracılığıyla kazanılan kredi
- **Promosyon** — pazarlama kampanyası kapsamında verilen kredi
- **El ile Ayarlama** — bir personel tarafından doğrudan eklenen veya kaldırılan kredi
- **Sipariş Ödemesi** — bir sipariş için ödeme sırasında harcanan fonlar. Şu anda kullanılmıyor — ödeme harcaması aktif hale geldiğinde rezerv edilir


## El ile cüzdan ayarlamaları

Yönetim panelinden fon ekleyemez veya kaldırılamaz — cüzdan işlemleri, onlara ait olan süreçler tarafından oluşturulur: iade işlemleri, sadakat ödülleri ve referans ödülleri. Bu amaçlıdır. Her hareket, onu yaratan şeyle bir bağlantı taşır ve gece boyu bir kontrol, her cüzdanın bakiyesini kendi geçmişine göre doğrular; elle girilen satırlar bu zinciri bozar.

İyi niyetli kredi — bir hizmet şikayeti, bir sorun sonrası bir el sıkışma — için bunun yerine el ile bir **hediye kartı** çıkarın (bkz. **Hediye Kartları** yardım konusu). Hediye kartı, bunun için tasarlanmıştır: değerini siz kontrol edersiniz, müşteri e-posta yoluyla bir kod alır ve mağaza kredisi gibi ödeme sırasında harcanır.

## Cüzdanı dondurma

Bir müşteriye ait cüzdanın kullanımını engellemek gerekiyorsa — dolandırıcılık soruşturması sırasında gibi — onu silmeden veya bakiyeyi kaldırmeden devre dışı bırakabilirsiniz.

1. Müşterinin cüzdan detay görünümünü açın
2. **Aktif** anahtarını kaldırın
3. **Kaydet**'e tıklayın

Bakiye korunur ve cüzdan herhangi bir zaman tekrar etkinleştirilebilir. Etkin olmayan bir cüzdana ait yeni krediler veya borçlar — elle girilen veya aksi takdirde — kaydedilemez.

## Tüm işlemleri görüntüleme

Cüzdan aktivitesi için mağaza genelinde bir görünüm elde etmek için **Müşteriler > Cüzdan İşlemleri**'ne gidin. Bu liste, tüm müşteri cüzdanlarının her işlemini gösterir ve aşağıdaki filtrelerle:

- **İşlem Türü** — kredi, borç, ayarlama vb. ile filtreleyin
- **Kaynak** — işlemlerin nereden geldiğini filtreleyin
- **Durum** — tamamlandı, bekliyor veya iptal edildi ile filtreleyin
- **Tarih** — üstteki tarih hiyerarşisini kullanarak belirli bir gün, ay veya yıla inin

İşlem listesi sadece okunabilir — bu görünümde işlemler düzenlenemez veya silinemez.

## İpuçları

- **Ömür boyu kredi** ile **Ömür boyu kullanılmış** karşılaştırın, müşteri mağaza kredisini ne kadar aktif kullandığını anlamanıza yardımcı olur — büyük bir kullanılmamış bakiye, müşteri bunun var olduğunu unuttuğunu gösterebilir
- Eğer bir müşteri bakiyesinin yanlış göründüğünü bildirirse, tam işlem geçmişini inceleyerek bakiyenin zaman içinde nasıl değiştiğini izleyin; her girdideki **İşlem Sonrası Bakiye** sütunu bunu kolaylaştırır
- Büyük bir kullanılmamış bakiye, bir uyarı değerindedir — müşteriler hesap panosunda ve ödeme adımında mağaza kredisini görürler, ancak onu belirten kısa bir e-posta genellikle bir siparişe dönüşür
- Donmuş cüzdanlar bakiyelerini kalıcı olarak tutar; bir son kullanma tarihi yoktur — bir cüzdanı geçici olarak devre dışı bırakırsanız, sorun çözüldüğünde tekrar etkinleştirmeyi unutmayın
- Her işlemdeki **Referans Kimliği**, orijinal kayda geri döner, bu da kredi veya borç uygulandığının nedenini doğrulamak için başka yerde arama yapmadan kolayca anlaşılır