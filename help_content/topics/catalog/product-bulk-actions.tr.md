---
title: Ürün Toplu Eylemler
---

İşte **Ürünler** listesi, her birini ayrı ayrı açmadan birden fazla ürünü aynı anda etkileşimde bulunmanı sağlar. Ürünlerin listesi üzerindeki **Toplu Eylemler** menüsünden, ürünleri yayınlayabilir ya da yayından kaldırabilir, öne çıkarabilir ya da öne çıkarılmamasını sağlayabilir, verileri CSV'ye aktarabilir, uluslararası kargo için hazır olup olmadıklarını kontrol edebilir ya da silme — hepsini tek bir adımda yapabilirsin.

Bu eylemleri kullanmak için **Ürünler > Tüm Ürünler** sayfasına gidin.

![Ürün listesi araç çubuğu, üç ürün kartı seçili ve **Toplu Eylemler** menüsünün tüm seçenekleri, CSV'ye İhracat Verileri ve Uluslararası Kargo Hazınlığı'nı kontrol etme dahil olmak üzere gösterildiği](/static/core/admin/img/help/product-bulk-actions/bulk-actions-dropdown.webp)

## Toplu Eylemi Çalıştırma

1. Gerekirse, hangi ürünleri daraltmak istediğini belirlemek için filtre panelini veya **Ara** kutusunu kullanın
2. Dahil etmek istediğiniz her ürün kartının sol üst köşesindeki kutuyu işaretleyin — **Toplu Eylemler** barında, seçili ürün sayısını gösteren bir sayaç döner
3. **Toplu Eylemler** menüsünden bir eylem seçin
4. **Uygula**'ya tıklayın

Veri değiştiren veya dışa aktaran eylemler hemen çalışır; **Seçilenleri Sil**, listeden kolayca geri alınamayacak olan tek eylemdir, bu yüzden önce onay istenir.

## Kullanılabilir Eylemler

| Eylem | Ne yapar | 
|--------|---------------| 
| **Yayına Aç** | Seçilen ürünleri mağaza eklentisinde görünür hale getirir. | 
| **Taslak Olarak İşaretle** | Seçilen ürünleri düzenlemeye devam ederken mağaza eklentisinden gizler. | 
| **Öne Çıkar** | Seçilen ürünleri **Öne Çıkarılmış** olarak etkinleştirir. | 
| **Öne Çıkarılmamış** | Seçilen ürünleri **Öne Çıkarılmış** olarak devre dışı bırakır. | 
| **CSV'ye İhracat** | Seçilen ürünleri ID, isim, SKU, durum, öne çıkarılmış bayrak ve fiyat içeren bir CSV'si indirir. | 
| **İhracat Verilerini CSV'ye Aktar** | Seçilen ürünleri için gümrük bilgilerini içeren bir CSV'si indirir. Aşağıya bakın. | 
| **Uluslararası Kargo Hazınlığı'na Kontrol Et** | Seçilen ürünlerin uluslararası kargo için gerekli gümrük verilerine sahip olup olmadığını gösteren bir özet gösterir. Aşağıya bakın. | 
| **Seçilenleri Sil** | Onay istemi sonrasında seçilen ürünleri çöp kutusuna atar.

## İhracat Verilerini CSV'ye Aktar

İhtiyacınıza göre bir taşıyıcı, kargo şirketi veya gümrük müdürünüze bir gümrük beyanı sayfası vermeniz gerekiyorsa bu aracı kullanın — örneğin, büyük bir uluslararası kargo öncesi veya yeni bir taşıyıcı kurulumu sırasında HS kodları ve köken verileri istenirse.

Ürünleri seçin, menüden **İhracat Verilerini CSV'ye Aktar**'ı seçin ve **Uygula**'ya tıklayın. Spwig, her ürün için bir satır ve aşağıdaki sütunlarla birlikte `product_customs_data.csv` adında bir dosya indirir:

| Sütun | Kaynak | 
|--------|--------| 
| **SKU** | Ürünün SKU'su | 
| **İsim** | Ürün adı | 
| **HS Kodu** | Harmonize Sistem sınıflandırma kodu | 
| **Köken Ülkesi** | Ürünün üretildiği yer | 
| **Gümrük Birim Fiyatı** | Gümrük için bildirilen birim başına değer | 
| **İhracat Lisans No** | Ürün için bir lisans gerekirse | 
| **Lisans Sonu** | İhracat lisanslarının son tarihi, ayarlandıysa | 
| **Uluslararası Hazır** | `Evet` veya `Hayır` — ürünün uluslararası kargo için gerekli minimum veriye sahip olup olmadığı (aşağıya bakın) |

Bu alanlar, ürün formunun **Uluslararası Kargo / Gümrük** bölümünden gelir. Eğer bir ürün eksikse, bu dosyayı gerçek bir kargo için kullanmadan önce ürün üzerinde eksik verileri doldurun.

## Uluslararası Kargo Hazınlığı'na Kontrol Et

Bu, ürünleri ayrı ayrı açmadan ya da tam bir CSV dışa aktarımına ihtiyaç duymadan uluslararası kargo yapmaya başlamadan önce bir dizi ürünü denetlemek için kullanılır.

Ürünleri seçin, **Uluslararası Kargo Hazınlığı'na Kontrol Et**'i seçin ve **Uygula**'ya tıklayın. Spwig, her bir seçili ürünün üç adet zorunlu alana, **HS Kodu**, **Köken Ülkesi** ve **Gümrük Birim Fiyatı**'na göre kontrolünü yapar ve sonucu özetleyen bir bildirim gösterir.

- Seçilen tüm ürünlerin üç alanı da doluysa, hepsinin hazır olduğuna dair bir onay görürsünüz.
- Bazıları veri eksikse, bildirim kaçının hazır, kaçının hazır olmadığını bildirir ve hazır olmayan her ürünü, eksik olan alanlarıyla birlikte listeler (örneğin, "Mavi Seramik Fincan (eksik: hs_code, country_of_origin)").

10'dan fazla ürün veri eksikse, bildirim ilk 10'unu listeler ve kaç tane daha olduğunu belirtir.

Bu işlem yalnızca veri okur — ürünlerde hiçbir şeyi değiştirmez, bu nedenle kataloğunuzda gümrük bilgilerini doldururken istediğiniz kadar sık çalıştırmanız güvenlidir.

**Export License Number** ve **Export License Expiry** hazırlık kontrolünün bir parçası değildir. Yalnızca kontrollü veya kısıtlı ürünler için geçerli olduklarından, bir ürün bunlar olmadan uluslararası gönderim için "hazır" olabilir.

## İpuçları

- İlk uluslararası siparişinizden önce tüm kataloğunuzda (veya kategori bazında) **Check International Shipping Readiness** çalıştırın — bir gönderi zaten sınırdayken eksik bir HS kodunu keşfetmekten çok daha hızlıdır.
- Broker'lara ve taşıyıcılara vermek için **Export Customs Data (CSV)** dosyasını, kendi iç kontrol listeniz için ise **Check International Shipping Readiness** işlemini kullanın — CSV bir kayıttır, hazırlık kontrolü ise yapılacaklar listesidir.
- Yeni ürünler eklerken **HS Code**, **Country of Origin** ve **Customs Unit Price** alanlarını ürün formunda (**International Shipping / Customs** altında) doldurun, böylece daha sonra toplu olarak yapmak zorunda kalmazsınız.
- Ürün ızgarası kaydırdıkça otomatik olarak daha fazla ürün yükler (sonsuz kaydırma) ve yeni ürünler yüklendikçe onay kutusu seçimleriniz korunur — bu sayede bir işlem uygulamadan önce kaydırarak büyük bir seçim oluşturabilirsiniz. Ancak bir filtreyi değiştirmek veya sayfayı yeniden yüklemek seçiminizi temizler, bu nedenle filtreleri ayarlamadan önce işlemi uygulayın.
- **Mark as Draft**, örneğin bir stok sayımı öncesinde, ürünlerin hiçbir diğer özelliğini değiştirmeden birden fazla ürünü aynı anda vitrinden çekmenin hızlı bir yoludur.