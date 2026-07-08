---
title: Bono Kısıtlamaları
---

Bono kısıtlamaları, bir bononun kimin, ne zaman ve ne sıklıkta kullanılabileceğini kontrol eder. Bu ayarları **Pazarlama > Bono** bölümünde bir bono oluştururken veya düzenlerken yapılandırın.

![Kısıtlama Kuralları](/static/core/admin/img/help/voucher-restrictions/restriction-rules.webp)

## Kullanım Sınırlamaları

Bono formunun **Kullanım Sınırlamaları** bölümünde genel ve müşteri başına sınırlamalar ayarlayın.

- **Toplam maksimum kullanım** — Bu bononun tüm müşteriler arasında kullanılabilmesinin maksimum sayısı. Boş bırakınca sınırsız olur.
- **Müşteri başına maksimum kullanım** — Bir müşteri bu bonoyu kaç kez kullanabilir. Çoğu kampanya için 1 olarak ayarlayın.

| Desen | Toplam Maksimum | Müşteri Başına | Kullanım Durumu |
|-------|------------------|----------------|------------------|
| Sınırlı kampanya | 100 | 1 | "İlk 100 müşteri" eksikliği |
| Sınırsız paylaşılabilir kod | (boş) | 1 | Sürekli pazarlama kodu |
| Sınırsız çok kez kullanılabilir | (boş) | (boş) | İçerik/şirket içi indirim |
| Tek kullanımlık benzersiz kodlar | 1 | 1 | Toplu oluşturulan kampanya kodları |

## Minimum Sipariş Değeri

**Min sipariş değeri** alanı, bononun uygulanabilmesi için sepet toplamını zorunlu kılar ve kâr marjınızı korur. Örnek: "50$ üzerindeki siparişlere 10$ indirim" ile küçük siparişlerin kârın dışı olmasına engel olursunuz.

| İndirim | Önerilen Minimum | Oran |
|--------|------------------|------|
| 5$ indirim | 30$+ | ~6:1 |
| 10$ indirim | 50$+ | ~5:1 |
| 20$ indirim | 100$+ | ~5:1 |
| 15% indirim | 40$+ | Kataloga bağlı |

## İndirim Sınırlaması (Maksimum İndirim Tutarı)

**Maksimum indirim tutarı** alanı, **İndirim Yapılandırması** bölümünde, yüzdelik bir bononun ne kadar indirim yapabileceğini sınırlar. Bu yalnızca yüzdelik türdeki bonolara uygulanır ve yüksek değerli sepetlerde aşırı indirimleri önler.

Örnek: "20% indirim, maksimum 50$ indirim"
- 200$ sepet = 40$ indirim (20%)
- 300$ sepet = 50$ indirim (sınırlı)
- 1000$ sepet = hâlâ 50$ indirim (sınırlı)

Herhangi bir yüzdelik bonoyu halka açık hale getirirken bir indirim sınırı ekleyin.

## Kombinasyon Kuralları

**Kısıtlamalar & Kurallar** alanı (açmak için tıklayın), bonoların diğer indirimlerle nasıl etkileştiğini kontrol eden onay kutularını içerir.

| Ayar | Ne Yapar | Ne Zaman Etkinleştirilir |
|------|----------|--------------------------|
| **Satış ürünleri hariç tut** | Bono, zaten indirimli olan ürünleri atlar | Çoğu kampanya — satış kâr marjlarını korur |
| **Diğer bonolarla birlikte kullanılamaz** | Her siparişte yalnızca bir bono | Çoğu bono için varsayılan |
| **Satış ürünleri ile birlikte kullanılamaz** | Sepette herhangi bir satış ürünü varsa bono engellenir | Bono, satış fiyatını değiştirirken çok sıkı kampanyalar |
| **Yalnızca ilk kez müşteriler için** | Önceki siparişi olmayan müşteriler | Hoş geldiniz/kampanya kazanımı |

## Müşteri Kısıtlamaları

Basit hedefleme için **Yalnızca ilk kez müşteriler için** seçeneğini **Kısıtlamalar & Kurallar** alanında işaretleyin.

İleri düzey hedefleme için, formun alt kısmındaki **Bono Kısıtlamaları** satır içi tablosunu kullanın. **+ Başka bir Bono Kısıtlaması Ekle**'ye tıklayarak satır ekleyin. Her kısıtlama üç alan içerir:

- **Tip** — Kısıtlama kategorisi (açılır menü)
- **Değer** — Eşleşen değer (virgülle ayrılmış veya JSON)
- **Dahil mi** — İşaretli = müşteri eşleşmelidir; işaretsiz = müşteri eşleşmemelidir

| Tip | Değer | Dahil | Etki |
|-----|-------|------|------|
| user_email_domain | @company.com | Evet | Sadece şirket çalışanları kullanabilir |
| shipping_country | US,CA | Evet | Sadece ABD ve Kanada müşterileri |
| shipping_country | RU | Hayır | Rusya hariç herkes |
| day_of_week | monday,tuesday | Evet | Sadece Pazartesi ve Salı geçerlidir |
| payment_method | stripe | Evet | Sadece Stripe ödemeleri için |

Katmanlı kısıtlamalar için birden fazla satırı birleştirin. Bono uygulanabilmesi için tüm dahil kısıtlamalar eşleşmelidir ve hiçbir dışlamalı kısıtlama eşleşmemelidir.

## Süre Sonu Stratejileri

Tarih ve geçerlilik alanlarını kullanarak bir bononun ne zaman sonlanacağını kontrol edin.

- **Bitiş tarihi** — Sert bir tarih sınırı (örneğin, 2026 Aralık 31).

Bono, gece yarısında çalışmaz.
- **Geçerli gün sayısı** — Bono oluşturulmasından veya ilk kullanımından itibaren kayar geçerlilik.

Ayarlanırsa bitiş tarihini geçersiz kılar.


Hoş geldiniz kodları için kullanışlı: "Alındıktan sonra 30 gün geçerlidir."