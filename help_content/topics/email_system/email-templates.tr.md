---
title: E-posta Şablonları
---

E-posta şablonları, mağazanızın müşterilere ve size gönderdiği tüm otomatik e-postaların tasarımı ve içeriğini kontrol eder — sipariş onayları, sevkiyat güncellemeleri, şifre sıfırlamaları, iade bildirimleri ve daha birçok. Bir şablonu düzenlemek, o türdeki gelecekteki tüm e-postaları değiştirir; ancak daha önce outbox'ta olan e-postular etkilenmez.

**E-posta Sistemi > E-posta Şablonları**'na giderek şablonlarınızı görüntüleyebilir ve yönetebilirsiniz.

![E-posta şablonları listesi](/static/core/admin/img/help/email-templates/templates-list.webp)

## Şablon türleri

Mağazanız, geniş bir dizi olay için şablonlar içerir. Bunlar kategoriye göre gruplandırılmıştır:

### Müşteri odaklı sipariş e-postaları
| Şablon | Gönderilme zamanı |
|----------|-----------|
| Sipariş Onayı | Bir müşteri bir satın alma tamamladığında |
| Ödeme Onayı | Bir ödeme başarıyla işlendiğinde |
| Sipariş Sevkiyattan Çıkarıldı | Bir sipariş sevkiyattan çıkmış olarak işaretlendiğinde |
| Sevkiyat Onayı | Bir sevkiyat takip numarası eklendiğinde |
| Teslim Onayı | Bir sipariş teslim edildi olarak işaretlendiğinde |
| Sipariş İptal Edildi | Bir sipariş iptal edildiğinde |
| Sipariş Gecikme Bildirimi | Bir sipariş üzerinde gecikme kaydedildiğinde |
| İade Bildirimi | Bir iade verildiğinde |

### Hesap e-postaları
| Şablon | Gönderilme zamanı |
|----------|-----------|
| Hesap Hoş geldiniz | Bir müşteri bir hesap oluşturduğunda |
| Hesap Daveti | Bir müşteriyi bir hesap oluşturmak için davet ettiğinizde |
| E-posta Doğrulama | Bir müşteri e-posta adresini doğruladığında |
| Şifre Sıfırlama | Bir müşteri bir şifre sıfırlama talep ettiğinde |

### İade işlemleri
| Şablon | Gönderilme zamanı |
|----------|-----------|
| İade: Talep Alındı | Bir müşteri bir iade talebi sunduğunda |
| İade: Onaylandı | Bir iade talebi onaylandığında |
| İade: Reddedildi | Bir iade talebi reddedildiğinde |
| İade: Paket Alındı | İade edilen ürün, konumunuza ulaştığında |
| İade: İade Ödemesi Yapıldı | Bir iade için iade ödemesi verildiğinde |

### Yönetici bildirimleri (size gönderilen)
| Şablon | Gönderilme zamanı |
|----------|-----------|
| Yönetici: Yeni Sipariş | Yeni bir sipariş verildiğinde |
| Yönetici: Ödeme Başarısız | Bir ödeme denemesi başarısız olduğunda |
| Yönetici: Günlük Satış Raporu | Günlük satış özeti oluşturulduğunda |
| Yönetici: Stok Seviyesi Düşük Uyarısı | Bir ürün stok eşiğinin altına düştüğünde |
| Yönetici: Haftalık Özeti | Haftalık mağaza özeti oluşturulduğunda |

Ek şablonlar, sevkiyat takip aşamaları, ortaklık programı etkinlikleri, rezervasyon onayları (rezervasyon özelliği etkinse) ve sadakat programı olaylarını kapsar.

## Bir şablonu Düzenleme

1. **E-posta Sistemi > E-posta Şablonları**'na gidin
2. Düzenlemek istediğiniz şablonu bulun. Şablonu filtrelemek için sağdaki filtrelerden **Şablon Türü**, **Dil** veya **Durum** kullanabilirsiniz
3. Şablonu açmak için üzerine tıklayın
4. **Konu** satırını düzenleyin (müşterinin posta kutusında görünen e-posta konusu)
5. E-postanın tam tasarım sürümü için **HTML İçeriği**'ni düzenleyin
6. İsteğe bağlı olarak **Metin İçeriği**'ni düzenleyin — HTML desteklemeyen e-posta istemcileri için bir metin alternatifi
7. **Kaydet**'e tıklayın

> **HTML e-postaları:** HTML içerik alanı, standart HTML ve satır içi CSS içerebilir. Spwig, bunu düzgün biçimlendirilmiş bir e-posta olarak işler. MJML etiketleri kullanıyorsanız, kaydederken otomatik olarak derlenir.

## Bir şablonu Önizleme

Kaydetmeden önce, şablonun e-posta istemcisi içinde nasıl görüneceğini önizleyebilirsiniz:

1. Önizlemek istediğiniz şablonu açın
2. **Önizle** butonuna tıklayın (şablon listesinde veya şablon detay sayfasında görünür)
3. Önizleme, yeni bir tarayıcı sekmesinde açılır ve işlenmiş e-postayı gösterir

Bu, şablon canlıya geçmeden önce düzen, biçimlendirme ve yer tutucu değişkenlerinin görünümünü kontrol etmenizi sağlar.

## Şablon Değişkenleri

Değişkenler, şablonunuzdaki yer tutuculardır ve Spwig, e-postayı gönderirken bunları gerçek verilerle değiştirir. Bunlar `{{ değişken_adı }}` olarak yazılır.

Çoğu şablonda bulunan yaygın değişkenler:


| Değişken | Değiştirilir | 
|----------|---------------| 
| `{{ customer_name }}` | Müşterinin tam adı | 
| `{{ order_number }}` | Sipariş referans numarası | 
| `{{ order_total }}` | Sipariş toplam tutarı | 
| `{{ store_name }}` | Mağazanızın adı | 
| `{{ store_url }}` | Mağazanızın web adresi | 
| `{{ tracking_number }}` | Gönderim takip numarası | 
| `{{ tracking_url }}` | Gönderimi takip etmek için tıklanabilir bir bağlantı | 

Şablon türüne göre kullanılabilen değişkenler değişebilir. Siparişle ilgili bir şablon (örneğin `{{ order_number }}`) için ilgili değişkenler, hesap şablonu (örneğin Şifre Sıfırlama) için kullanılamaz. Kullanmadığınız bir değişken görünür olur ya da değiştirilmemiş olarak kalır.

## Dil desteği

Her şablon türü, mağazanızın desteklediği her dil için bir sürümü olabilir. Her şablonun **Dil** alanı, hangi dil sürümünün aktif olduğunu kontrol eder.

Spwig, gönderim sırasında müşteri dil tercihine göre otomatik olarak doğru dil sürümünü seçer. Eğer bir müşterinin diline ait bir şablon yoksa, Spwig İngilizce sürümüne geri döner.

Yeni bir dil için şablon eklemek için:
1. Mevcut bir şablonu açın
2. **Aksiyonlar** menüsünden **Şablonu Kopyala**'yı tıklayın
3. Kopyanın **Dil Kodu**'nu yeni dile ayarlayın
4. İçeriği çeviri yapın
5. Kopyalanan şablonu etkinleştirin

## Şablonları kopyalama, etkinleştirme ve devre dışı bırakma

### Şablonu kopyalama

Şablon kopyalama, şablonun tam bir kopyasını oluşturur — bu, dil varyasyonları oluşturmak veya canlı şablonu etkilemeden farklı sürümleri test etmek için yararlıdır.

1. Listede bir veya daha fazla şablonu seçin
2. **Aksiyonlar** açılır menüsünden **Seçilen şablonları kopyala**'yı seçin
3. Kopya, etkin olmayan şekilde oluşturulur — düzenleyin ve hazırsanız etkinleştirin

### Şablonları etkinleştirme ve devre dışı bırakma

Bir şablonun **Etkin** olması, gönderim için kullanılması gerekir. Her tür ve dil kombinasyonu için yalnızca bir etkin şablon kullanılır.

Toplu olarak etkinleştirme veya devre dışı bırakma için:
1. Şablonları seçin
2. **Aksiyonlar** açılır menüsünden **Seçilen şablonları etkinleştir** veya **Seçilen şablonları devre dışı bırak**'ı seçin

Ya da bireysel bir şablonu açın ve **Etkin** onay kutusunu devre dışı bırakın ya da etkinleştirin.

## Sistem şablonları

**Sistem** damgasıyla işaretlenmiş şablonlar, Spwig tarafından varsayılan olarak eklenen şablonlardır. Bu şablonlar silinemez. Onları doğrudan düzenleyebilir ya da kopyalayarak özel bir sürüm oluşturabilirsiniz.

## İpuçları

- Düzenledikten sonra her zaman bir şablonu önizleme yapın, müşterilerin onu görmesinden önce biçimlendirme sorunlarını yakalayın
- Konu satırlarını kısa ve öz tutun — `Sipariş #10045 gönderildi` gibi konular, `Mağazamızdan güncelleme` gibi genel konulara göre daha iyi çalışır
- Basit metin içeriğini de düzenleyin — bazı e-posta istemcileri yalnızca basit metin sürümünü gösterir ve bazı müşteriler bunu tercih eder
- Bir şablonun İngilizce sürümünü kopyalayarak çevrilmiş bir sürüm oluşturmadan önce başlangıç noktası olarak kullanın
- Canlı e-postaları etkilemeden bir değişiklik test etmek istiyorsanız, şablonu kopyalayın, kopyayı düzenleyin ve onaylamadan önce hem orijinali hem de kopyayı kısa süreliğine etkin bırakın — ardından orijinali devre dışı bırakın
- Yönetici bildirim şablonları (örneğin **Yönetici: Yeni Sipariş**) mağazanızın yönetici e-posta adresine gönderilir — mağazanızın ayarlarında bu e-posta adresinin doğru olduğundan emin olun