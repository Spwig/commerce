---
title: POS Müşteri Ekranı Kurulumu
---

screenshots-needed

paragraph

Müşteri ekranı, satış sırasında müşterinizin karşıya çıktığı ikinci bir ekran. İşlemi işleme sırasında müşteri, tarifeli ürünleri, geçici toplamı, fiyat ve vergi analizini ve - aktif bir satış yoksa - promosyon içeriğinizin dönen bir slayt gösterisini görür.

paragraph

Bu kılavuz, müşteri ekranınızı ayarlamanın donanım ve eşleştirme yönünü kapsar: bir terminalde özelliği etkinleştirme, ekran ekranı olarak ayrı bir cihazı eşleştirme ve ortak kurulum senaryolarını ele alma. Boş zamanlarda gösterilen promosyon slaytları hakkında bilgi için [Müşteri Ekranı Promosyon Slaytları](customer-display-promo-slides) bölümüne bakın.

heading

## Müşteri ekranının ne gösterdiğini

paragraph

Bir satış aktif olduğunda, müşteri ekranı şunları gösterir:

list

paragraph

Terminal boş (aktif bir işlem yok) olduğunda, ekran promosyon slayt gösterisine geçer. Bu slaytın içeriğini ayrı olarak kontrol edersiniz - [Müşteri Ekranı Promosyon Slaytları](customer-display-promo-slides) bölümüne bakın.

heading

## Ortak donanım kurulumları

paragraph

Müşteri odaklı bir ekran ayarlamak için üç pratik yol vardır:

list

heading

## Bir terminalde müşteri ekranını etkinleştirme

paragraph

Müşteri ekranı özelliği, terminalin donanım yapılandırması aracılığıyla her terminal için etkinleştirilir.

list

image

![Terminal donanım yapılandırması, customer_display etkin](/static/core/admin/img/help/pos-customer-display-setup/terminal-capabilities-toggle.webp)

paragraph

Etkinleştirildikten sonra, o terminaldeki POS uygulaması, oturum başladığında müşteri ekranı görünümünü ikinci bir tarayıcı penceresi veya sekmesinde açar.

heading

## Ayırma cihazını ekran olarak eşleştirme

paragraph

Müşteri ekranı için ayrı bir fiziksel cihaz kullanıyorsanız (tablet, telefon veya ikinci bilgisayar), onu terminalle kısa ömürlü 6 haneli bir kod kullanarak eşleştirirsiniz.

heading

### Adım 1: Ana terminalde eşleştirme kodu oluşturun

Ana terminalinizdeki POS uygulamasını açın ve terminal arayüzinin ekran ayarları veya eşleştirme bölümüne gidin.

Yeni bir ekran eşleştirme kodu isteyin.

Kod, 6 haneli bir sayıdır ve **5 dakika** için geçerlidir.

Yeni bir kod oluşturduğunuzda, bu terminal için önceki kullanılmamış tüm kodlar otomatik olarak iptal edilir.

### Adım 2: Müşteri cihazında ekran URL'sini açın

Müşteri tarafında cihazda bir web tarayıcısı açın ve aşağıdaki adrese gidin:

```
https://your-store-domain.com/pos/display/
```

Giriş yapmaya gerek yoktur — ekran sayfası genel erişime açıktır. Bu amaçlıdır: ekran cihazı personel kimlik bilgilerine ihtiyaç duymaz ve eşleştirme kodu, ekranın doğru terminal ile bağlantısını sağlar.

![Müşteri ekranı boş durum görünümü](/static/core/admin/img/help/pos-customer-display-setup/customer-display-view.webp)

### Adım 3: Eşleştirme kodunu girin

Müşteri cihazında, ana terminalden alınan 6 haneli kodu girin. Ekran, o terminalle eşleşir ve canlı sepet verilerini göstermeye başlar.

Kod kullanıldıktan sonra hemen geçersiz hale gelir ve tekrar kullanılamaz.

## Eşleştirme kodunu yeniden oluşturmak

Eşleştirme kodu, girebileceğinizden önce zaman aşımına uğrar ya da ekran cihazını yeniden eşleme ihtiyacınız olursa (örneğin, bir ekran cihazı değiştirilir veya sıfırlanırsa), ana terminaldeki POS uygulamasından yeni bir kod oluşturun.

Yeni bir kod oluşturmak, o terminal için mevcut kullanılmamış tüm kodları otomatik olarak iptal eder. Yeni kod 5 dakika boyunca geçerlidir.

Kodun yeniden oluşturulması için yönetici panelinde değişiklik yapmanıza gerek yoktur — bu işlem POS uygulaması içinde tamamen yapılır.

## Tek bir cihazda çoklu monitör kurulumu

Ana terminaliniz bir dizüstü veya iki monitörlü bir dizüstü ise:

1. İkinci monitörü bağlayıp işletim sisteminizdeki ekran ayarlarında **genişletilmiş masaüstü** moduna ayarlayın (aynılaştırılmamalı).
2. Ana ekran üzerinde POS uygulamasını normal şekilde açın.
3. POS uygulaması, müşteri ekranını ikinci bir pencere olarak açar. Bu pencereyi ikinci monitöre sürükleyin.
4. İkinci monitörde pencereyi maksimize edin veya tam ekran yapın.

Eşleştirme koduna ihtiyaç yoktur çünkü her iki pencere de aynı cihazda çalışır ve doğrudan iletişim kurar.

## Boş durum davranışı

Aktif bir satış yoksa, müşteri ekranı promosyon resimlerinin döngüsünü gösterir. Bu slaytları **POS > Promo Slides** altında ayrı olarak oluşturup yönetirsiniz.

Slaytlar oluşturmak, belirli mağazalara hedeflemek ve mevsimsel içerikleri yönetmekle ilgili ayrıntılar için [Müşteri Ekranı Promo Slaytları](customer-display-promo-slides) bölümüne bakın.

Konfigüre edilmemiş slaytlar varsa, ekran sadece mağazanızın adını gösteren bir hoş geldiniz ekranı görüntüler.

## Sorun Giderme

**Ekran boş kaldı veya güncellenmiyor**

Ekran, ana terminalle gerçek zamanlı iletişim kurar. Bağlantı kesilirse, ekran boş kalabilir veya eski verileri gösterebilir. Müşteri cihazında tarayıcıyı yenileyin. Bu işlem işe yaramazsa, yeni bir eşleştirme kodu oluşturun ve tekrar eşleştirin.

**Ekran, yanlış terminalin sepetini gösteriyor**

Her ekran, belirli bir terminalle eşleşir. Birden fazla terminaliniz varsa, doğru terminalde eşleştirme kodunu oluşturduğunuzdan ve ekranın doğru terminalde girildiğinden emin olun. Eşleşmeyi düzeltmek için doğru terminalde yeni bir kod oluşturun ve ekran cihazını yeniden eşleştirin.

**Eşleştirme kodu, girebileceğimden önce zaman aşımına uğradı**

Kodlar 5 dakika boyunca geçerlidir. POS uygulamasından yeni bir kod oluşturun ve ekran cihazında hemen girin. Eşleştirme işlemi sırasında iki cihazı birbirine yakın tutun.

**Eşleştirme kodu girildi ancak ekran bağlanmadı**

Müşteri cihazının mağazanızın domain'ine erişip erişemediğini kontrol edin (ağ erişimi gereklidir). Ayrıca terminalin donanım yapılandırmasında "customer_display": true ayarının yapıldığını ve terminalin kaydedildiğini kontrol edin.

**Ekran URL'si bir hata döndürüyor**

Mağazanızın domain'indeki /pos/display/ adresine yönlendirildiğinizden emin olun, admin URL'sine değil. Ekran görünümü için giriş yapmaya gerek yoktur — giriş yapmanız isteniyorsa, URL'yi tekrar kontrol edin.

## İpuçları

Tüm markdown biçimlendirmesini, resim yollarını, kod bloklarını ve teknik terimleri koruyun.

- **Bağlama oturumunu kısa tutun** — bağlama kodu oluşturmadan önce müşteri cihazının hazır olduğundan ve tarayıcının `/pos/display/` adresine açık olduğundan emin olun.

5 dakikanız vardır, ancak bir dakikadan kısa sürede tamamlamak zaman aşımından kaçınmanıza yardımcı olur.

- **Açmadan önce test yapın** — ilk gerçek işleminden önce ekran bağlı olacak şekilde bir test satışını tamamlayarak müşterilerin doğru ürünleri ve toplamları göreceğini doğrulayın.

- **Ekran URL'sini favorilere ekleyin** — müşteri cihazının tarayıcısını başlangıçta `/pos/display/` adresini açacak şekilde ayarlayarak her zaman hazır olmasını sağlayın.

- **Basitlik için uzatılmış masaüstü kullanın** — terminalinizde boş bir HDMI girişi ve bir monitör mevcutsa, uzatılmış masaüstü yaklaşımı devam eden bir bağlama gerektirmez ve asla sona ermeyebilir.

- **Açmadan önce promosyon slaytları ekleyin** — sadece boş bir hoş geldiniz ekranı gösteren boş bir ekran, bir fırsat kaçırmasıdır.

Hiçbir işlem yapılmadığında bile ekranın faydalı olabilmesi için en az birkaç promosyon slaydını kurun.

Aşağıdaki [Müşteri Ekranı Promosyon Slaytları](customer-display-promo-slides) bölümüne bakın.

- **Ekran cihazını güvenli hale getirin** — ekran URL'si tasarım itibariyle genel erişime açıktır, ancak yalnızca aktif bir terminalle bağlandığında canlı sepet verilerini gösterir.

Yine de müşteri cihazında kiosk tarayıcı modunu düşünün, böylece müşterilerin başka yerlere yönlendirilmesini önleyebilirsiniz.