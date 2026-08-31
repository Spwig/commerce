---
title: CSV'den Abonelerin Aktarılması
---

Eğer bir yerde zaten bir posta listesi varsa — eski bir e-posta aracı, bir bülten abonelikleri için bir spreadsheet, bir sergi kartı taramaları yığını — bu kişileri tek tek Spwig'e birer birer eklemenize gerek yok. Campaign Studio'nun abone aktarımı, bir CSV veya Excel dosyasını okur ve her geçerli kişiyi aynı anda kitleye ekler, her biri etiketlemek, segmentlemek ve e-posta atmak için hazır hale gelir.

## Aktarmadan önce: izin

Her aktarma, **"Bu kişilerin, benden pazarlama e-postası almayı kabul ettiğini"** onaylamak için bir kutuyu işaretlemeniz gerekir. Bu bir formalite değildir — sadece gerçekten pazarlama e-postası almayı kabul eden kişileri aktarın. İki nedenden dolayı önemlidir:

- **Çoğu yerde yasal bir zorunluluktur.** Çoğu yasada, kabul etmedikleri pazarlama e-postalarına e-posta atmak, izin yasalarını çipliğinden çipliğine kırmaktadır.
- **İletilebilirlik sorgulamasını korur.** Kabul etmeyen kişilere e-posta atmak, spam şikayetleri ve geri dönüşler oluşturur, bu da posta sağlayıcıları tarafından *herhangi* bir e-postanızın (hatta kabul eden kişilere bakan e-postalarınızın da) posta kutusuna erişip erişmediğini karar verirken kullanılır.

Eğer bir liste, kabul edilmiş abonelere ait değilse, onu aktarmayın.

## Dosyanızı hazırlama

İndirici, bir başlık satırı olan bir `.csv` veya `.xlsx` dosyasını kabul eder. Sadece bir sütun gerekli:

| Sütun | Gerekli mi? | Notlar |
|--------|-----------|-------|
| **E-posta** | Evet | Geçerli bir e-posta adresi olmalıdır. |
| **İsim** | Hayır | E-postaları kişiselleştirmek için kullanılır. |
| **Soyad** | Hayır | E-postaları kişiselleştirmek için kullanılır. |
| **Dil** | Hayır | Abonelerin tercih ettiği dil kodu (örneğin `en`, `es`). |

Sütunlar, başlık adına göre otomatik olarak bu alanlara eşleştirilir, bu yüzden önce herhangi bir şeyi yeniden adlandırmak gerekmez — `E-mail`, `Email Address`, `First Name`, `Given Name`, `Surname` veya `Locale` gibi yaygın varyasyonlar da tanımlanır.

Her aktarma, **5 MB** ve **5.000 satır** ile sınırlıdır. Listeleniz bu sınırların üzerindeyse, daha küçük dosyalara ayırın ve sırayla aktarın.

## Abonelerinizi Aktarma

1. **Campaign Studio > Aboneler** sekmesini açın ve **CSV Aktar**'a tıklayın.
2. `.csv` veya `.xlsx` dosyanızı seçin.
3. Zaten listenizde olan aboneler için ne olacağını seçin — aşağıda ki [Yinelenenleri İşleme](#yinelenenleri-isleme)ye bakın.
4. İsteğe bağlı olarak, [Abone Etiketleri](/help/subscriber-tags) için daha fazlası için bu aktarımdaki herkese etiket vermek için **Aktarılan aboneleri etiketle** altında bir etiket seçin.
5. **Bu abonelerin, benden pazarlama e-postası almayı kabul ettiğini** onaylayın.
6. **Devam**'a tıklayın.

![Dosya seçili, etiket seçili ve izin onaylı bir aktarma yükleme formu](/static/core/admin/img/help/import-subscribers/import-upload-form.webp)

Spwig, hiçbir şey aktarılmadan önce bir önizleme görüntüler:

![Yeni, zaten olan ve geçersiz olarak atlanan sayıları ve nedenleri gösteren bir aktarma önizlemesi](/static/core/admin/img/help/import-subscribers/import-preview.webp)

- **Yeni aboneler** — bir abone oluşturan satırlar.
- **Zaten listenizdeki** — e-posta adresi zaten bir aboneye eşleşen satırlar.
- **Geçersiz atlandı** — okunamayan satırlar, her biri satır numarası ve nedeniyle birlikte listelenir (geçersiz bir e-posta formatı, boş bir e-posta hücresi veya aynı dosyadaki daha önceki bir satırın yineleneceği).

Bu sayıları kontrol edin, ardından aktarmayı tamamlayın ya da herhangi bir değişiklik yapmadan geri dönün.

## Yinelenenleri İşleme

Eğer bir satırın e-posta adresi, zaten sahip olduğunuz bir aboneye eşitse, bu bir yinelenen olarak kabul edilir. Yükleme formunda bu satırların nasıl ele alınacağını seçersiniz:

| Seçenek | Ne olur |
|--------|--------------|
| **Onları değişmeden bırak** *(varsayılan)* | Zaten mevcut olan abonenin ismi ve dili olduğu gibi kalır. |
| **İsim / dilini güncelle** | Zaten mevcut olan abonenin ismi, soyadı ve dili dosyadan güncellenir (dosyanın aslında sağlayacağı alanlar için sadece). |

Seçtiğiniz etiket, dosyadaki **herkese** uygulanır — dosyadaki yeni ve zaten mevcut aboneler dahil olmak üzere — hangi yinelenen seçeneğini seçerseniz seçin.

Tüm markdown formatını, resim yollarını, kod bloklarını ve teknik terimleri koruyun.

Dolayısıyla "VIP listenizi" **VIP** etiketiyle içe aktarmak, zaten sahip olduğunuz kişileri de etiketler.

Mükerrer seçeneği yalnızca mevcut bir temasın *adı ve dili* üzerine yazılıp yazılmayacağını kontrol eder.

## İçe aktarma sonrası

Bir içe aktarma ile oluşturülen her temas, kaynak olarak **İçe Aktarma** ile kaydedilir ve içe aktarmayı çalıştırdığınız anda onay verilmiş olarak işaretlenir (başka bir yerde daha önce onay vermiş olabilecekleri bir tarih değil). Ad ve soyadları — dosya bunları sağladıysa — abone kayıtlarında saklanır. Bu da kampanyalarınızda `[[first_name]]` ve `[[last_name]]` birleştirme alanlarının, bir Spwig hesabı oluşturmadılar bile olsa, onlar için de doğru şekilde kişiselleştirildiği anlamına gelir.

## İpuçları

- Yüklemeye başlamadan önce kaynak listenizi temiz bir başlık satırı olan tek sayfalı bir CSV veya `.xlsx` dosyasına dışa aktarın — ek sayfalar, birleştirilmiş hücreler veya özet satırları sütun eşleştirmesini karıştırabilir.
- Sonrasında hedeflemek isteyeceğiniz tam kitleyi hemen oluşturmak için **İçe aktarılan temasları şu şekilde etiketle** seçeneğini kullanın — bunun bir segment oluşturmak için [Abone Etiketleri](/help/subscriber-tags) bölümüne bakın.
- Bir içe aktarmada hata olduğunu varsaymadan önce her zaman **Atlanan (geçersiz)** nedenlerini okuyun — çoğu gerçek dünya listesi için açık nedenlere sahip birkaç atlanan satır normaldir.
- Aynı dosyayı yeniden çalıştırmak güvenlidir: zaten içe aktardığınız temaslar ikinci kez mükerrer olarak ele alınır, yeniden oluşturulmaz.
- Birden fazla küçük listeyi birleştiriyorsanız, her içe aktarmayı farklı etiketleyin (ör. `Import: Jan Event`, `Import: Trade Show`) böylece hepsi ana kitlenize karıştıktan sonra bile onları ayırt edebilirsiniz.
- 5.000 satırdan fazla listeler için, her partinin sonradan kolayca tanımlanabilmesi için keyfi bir kesme yerine belirgin bir sınıra (alfabetik, kaynağa veya toplanma tarihine göre) göre bölün.