---
title: Ürün Toplu İşlemleri
---

İşte **Ürünler** listesi, her birini ayrı ayrı açmadan birden fazla ürünü aynı anda işlemeye olanak tanır. **Ürünler** listesinin üstündeki **Toplu İşlemler** menüsünden, ürünleri yayınlayabilir ya da yayından kaldırabilir, öne çıkarabilir ya da öne çıkarılmamasını sağlayabilir, verileri CSV'ye aktarabilir, uluslararası kargo için hazır olup olmadıklarını kontrol edebilir ya da silme — hepsini tek bir adımda yapabilirsiniz.

Bu işlemleri kullanmak için **Ürünler > Tüm Ürünler** sayfasına gidin.

![Ürün listesi araç çubuğu, üç adet ürün kartı seçili ve **Toplu İşlemler** menüsünün tüm seçenekleriyle birlikte, CSV'ye İhracat ve Uluslararası Kargo Hazınlığı kontrolü dahil](/static/core/admin/img/help/product-bulk-actions/bulk-actions-dropdown.webp)

## Toplu İşlemi Çalıştırma

1. Gerekirse, hangi ürünleri daraltmak istediğinizi belirlemek için filtre panelini veya **Ara** kutusunu kullanın
2. Dahil etmek istediğiniz her ürün kartının sol üst köşesindeki kutuyu işaretleyin — **Toplu İşlemler** barındağı seçili ürün sayısını gösterir
3. **Toplu İşlemler** menüsünden bir işlem seçin
4. **Uygula**'ya tıklayın

Veri değiştiren ya da dışa aktaran işlemler hemen çalışır; **Seçilenleri Sil**, listeden kolayca geri alınamayacak olan tek işlemdir, bu yüzden önce onay istenir.

## Kullanılabilir İşlemler

| İşlem | Ne yapar | 
|--------|---------------| 
| **Yayına Aç** | Seçilen ürünleri mağaza ekrânında görünür hale getiren durumlarını Yayına Aç olarak ayarlar. | 
| **Taslak Olarak Kaydet** | Seçilen ürünleri mağaza ekrânından düzenlemeye devam ederken gizleyen durumlarını Taslak olarak ayarlar. | 
| **Öne Çıkar** | Seçilen ürünleri üzerinde **Öne Çıkarılmış** özelliğini etkinleştirir. | 
| **Öne Çıkarılmamış** | Seçilen ürünleri üzerinde **Öne Çıkarılmış** özelliğini devre dışı bırakır. | 
| **CSV'ye İhracat** | Seçilen ürünleri ID'si, ismi, SKU'su, durumu, öne çıkarılmış bayrağı ve fiyatı dahil CSV dosyası olarak dışa aktarır. | 
| **İhracat İçin Veri İhracatı (CSV)** | Seçilen ürünler için ithalat bilgilerini içeren bir CSV dosyası dışa aktarır. Aşağıya bakınız. | 
| **Uluslararası Kargo Hazınlığı Kontrolü** | Seçilen ürünlerin uluslararası kargo için gerekli olan ithalat bilgilerine sahip olup olmadığını gösteren bir özet sunar. Aşağıya bakınız. | 
| **Seçilenleri Sil** | Onay istemi sonrasında seçilen ürünleri çöp kutusuna atar.

## İhracat İçin Veri İhracatı (CSV)

Bir taşıyıcıya, kuryeye ya da ithalat müdürlerine bir ithalat beyanı sayfası vermeniz gerekirse bu işlemi kullanın — örneğin, büyük bir uluslararası kargo öncesi ya da bir taşıyıcı kurulumu sırasında HS kodları ve köken bilgileri istenen yeni bir taşıyıcı ayarlaması sırasında.

Ürünleri seçin, menüden **İhracat İçin Veri İhracatı (CSV)** seçeneğini seçin ve **Uygula**'ya tıklayın. Spwig, her ürün için bir satır ve aşağıdaki sütunlarla birlikte `product_customs_data.csv` adında bir dosya indirir:

| Sütun | Kaynak | 
|--------|--------| 
| **SKU** | Ürünün SKU'su | 
| **İsim** | Ürün adı | 
| **HS Kodu** | Harmonize Sistem sınıflandırma kodu | 
| **Köken Ülkesi** | Ürünün üretildiği yer | 
| **İhracat Birim Fiyatı** | İhracat için belirtilen birim başına değer | 
| **İhracat Lisans No** | Ürün için gerekliyse bir lisans numarası | 
| **Lisans Sonu** | İhracat lisanslarının son tarihi, ayarlandıysa | 
| **Uluslararası Hazır** | `Evet` ya da `Hayır` — ürünün uluslararası kargo için gerekli minimum veriye sahip olup olmadığı (aşağıya bakınız) |

Bu alanlar ürün formunun **Uluslararası Kargo / İhracat Bilgisi** bölümünden gelir. Eğer bir ürün eksikse, dışa aktarımda o sütun boş kalır — bu dosyayı gerçek bir kargo için kullanmadan önce ürün üzerinde eksik verileri doldurun.

## Uluslararası Kargo Hazınlığı Kontrolü

Bir ürünün uluslararası kargo için gerekli olan bilgileri olup olmadığını kontrol etmek için bu işlemi kullanın, her birini ayrı ayrı açmadan ya da tam bir CSV dışa aktarımına gerek kalmadan.

Ürünleri seçin, **Uluslararası Kargo Hazınlığı Kontrolü** seçeneğini seçin ve **Uygula**'ya tıklayın. Spwig, her bir seçili ürünün üç adet gerekli alana — **HS Kodu**, **Köken Ülkesi** ve **İhracat Birim Fiyatı** — göre kontrolünü yapar ve sonucu özetleyen bir bildirim gösterir.

Tüm markdown formatını, resim yollarını, kod bloklarını ve teknik terimleri koruyun.

- Eğer seçili tüm ürünlerin üçüncü alan da doldurulmuşsa, hepsinin hazır olduğunu bildiren bir teyit görürsünüz.
- Bazıları veri eksikliği yaşıyorsa, bildirim, hangilerinin hazır olduğunu ve hangilerinin olmadığını bildirir ve eksik olan her bir ürünün hangi alanları eksik olduğunu listeler (örneğin, "Mavi Seramik Bardak (eksik: hs_code, country_of_origin)").

Eğer 10'dan fazla ürün veri eksikliği yaşıyorsa, bildirim ilk 10'u listeler ve daha fazla kaç tane daha olduğunu söyler.

Bu işlem sadece veri okur — ürünleri değiştirmeden, bu nedenle katalogdaki gümrük bilgilerini doldururken her zaman güvenlidir.

**İhracat Lisans Numarası** ve **İhracat Lisans Süresi** hazır olma kontrolünün bir parçası değildir. Bu alanlar, kontrol edilen ya da sınırlı ürünler için geçerlidir, bu nedenle bir ürün, uluslararası sevkiyat için "hazır" olabilir ama bu alanlar olmadan.

## İpuçları

- İlk uluslararası siparişinizden önce katalogdaki tüm ürünleri (ya da kategori başı başına) **Uluslararası Sevkiyat Hazır Olma Kontrolunu** çalıştırın — bir gönderi sınırda iken eksik bir HS kodu fark etmekten çok daha hızlıdır.
- Brokere ve taşıyıcıya vermek için **İhracat Gümrük Verileri (CSV)** dosyasını saklayın ve kendi iç kontrol listeniş için **Uluslararası Sevkiyat Hazır Olma Kontrolunu** kullanın — CSV bir kayıt, hazır olma kontrolü ise bir yapılacaklar listesidir.
- Yeni ürünler eklerken, ürün formunda ( **Uluslararası Sevkiyat / Gümrük** altında) **HS Kodu**, **Origin Ülkesi** ve **Gümrük Birim Fiyatı** bilgilerini doldurun, böylece daha sonra kitle olarak yapmamak için.
- Ürün kılavuzu, kaydırma işlemi yaparken daha fazla ürün yükler ve seçili kutucuklar yeni ürünler yüklenene kadar devam eder — bu nedenle bir işlem uygulamadan önce büyük bir seçim oluşturmak için yeterince kaydırabilirsiniz. Filtreleri değiştirirseniz ya da sayfayı yenilerseniz, seçim silinir, bu nedenle filtreleri ayarlamadan önce işlemi uygulayın.
- **Taslak Olarak İşaretle**, bir dizi ürünü aynı anda mağazadan çıkarmak için hızlı bir yoldur — örneğin, stok sayımından önce — ama onlarla ilgili başka hiçbir şeyi değiştirmeden.

Tüm markdown formatını, resim yollarını, kod bloklarını ve teknik terimleri koruyun.