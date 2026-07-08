---
title: Vergi Yapılandırması
---

Mağazanız için vergi kurallarını yapılandırın, böylece müşteri konumuna göre siparişlere otomatik olarak doğru vergiler uygulanacaktır. Bölgesel ön ayarları bir tıklamayla yükleyebilir veya herhangi bir ülke, eyalet, şehir veya posta kodu için özel kurallar oluşturabilirsiniz.

![Vergi Dashboard](/static/core/admin/img/help/tax-configuration/tax-dashboard.webp)

## Vergi Dashboard

**Siparişler > Gönderimler > Vergi Oranları**'na giderek vergi dashboard'ını açın. Sayfa şunları gösterir:

- **İstatistikler paneli** — Toplam Kurallar, Etkin Kurallar, Kapsanan Ülkeler ve Kullanılan Vergi Türleri görüntüleyen dört kart
- **Filtreler** — İsim, ülke veya eyalet üzerinden arama yapın ve ülke, vergi türü (Satış Vergisi, KDV, GST, Özel) veya durum (Etkin/Devre Dışı) üzerinden filtreleyin
- **Vergi kuralı kartları** — Her kart, ülke bayrağı, kural adı, konum, oran yüzdesi, vergi türü etiketi, durum etiketi, öncelik ve muafiyet sayısını gösterir

## Vergi Ön Ayarlarını Yükleme

**Ön Ayarları Yükle**'ye tıklayarak ön ayarlar modal penceresini açın. Ön ayarlar, bir bölgede standart vergi oranlarının toplu halidir ve mağazanıza tek bir tıklamayla yükleyebilirsiniz.

![Ön Ayarları Yükle](/static/core/admin/img/help/tax-configuration/tax-presets-modal.webp)

Ön ayarlar dünya bölgelerine göre düzenlenmiştir:

| Bölgesel | Ön Ayar Grupları |
|----------|------------------|
| **Afrika** | Afrika KDV (25 oranı) |
| **Asya Pasifik** | Asya-Pasifik KDV/GST (24 oranı), Orta Asya KDV (6 oranı) |
| **Avrupa** | AB KDV Oranları, İngiltere KDV, Diğer Avrupa KDV |
| **Latin Amerika** | Latin Amerika KDV |
| **Orta Doğu** | Orta Doğu KDV |
| **Kuzey Amerika** | ABD Eyaletleri Satış Vergisi, Kanada GST/HST |
| **Okyanusya** | Okyanusya GST/KDV |

### Ön Ayarların Nasıl Çalıştığı

1. İstediğiniz ön ayar grubu üzerinde **Yükle**'ye tıklayın
2. Sistem, o gruptaki her ülke veya eyalet için vergi kuralları oluşturur
3. Aynı ülke, eyalet ve vergi türüne sahip mevcut kurallar otomatik olarak atlanır, böylece çoğalma önlenir
4. Yükleme tamamlandıktan sonra her kural tamamen düzenlenebilir — oranları ayarlayabilir, muafiyetler ekleyebilir veya ihtiyaç duyulmayan kuralları devre dışı bırakabilirsiniz

Birden fazla ön ayar grubu yükleyebilirsiniz. Örneğin, Avrupa genelinde müşterilere satış yaparsanız hem AB KDV hem de İngiltere KDV'yi yükleyebilirsiniz.

## Manuel Vergi Kuralları Oluşturma

**Vergi Oranı Ekle**'ye tıklayarak özel bir kural oluşturun. Form, dört bölümden oluşur:

![Vergi Oranı Formu](/static/core/admin/img/help/tax-configuration/tax-rate-form.webp)

### Temel Bilgiler

| Alan | Açıklama |
|------|----------|
| **Ad** | Kuralın görüntülenecek adı (örneğin, "Kaliforniya Satış Vergisi") |
| **Etkin** | Kuralı etkinleştirmek veya devre dışı bırakmak için anahtar |
| **Vergi Türü** | Satış Vergisi, KDV, GST veya Özel Vergi |
| **Oran (%)** | Vergi oranı yüzdesi olarak (örneğin, 8.25 için 8.25 girin) |
| **Öncelik** | Aynı konum için birden fazla kural eşleştiğinde daha yüksek sayılar önceliklidir |

### Coğrafi Kapsam

| Alan | Açıklama |
|------|----------|
| **Ülke** | ISO 3166-1 alfa-2 kodu (örneğin, US, GB, DE) |
| **Eyalet** | Eyalet veya eyalet (boş bırakın, tüm ülkeye uygulanacak) |
| **Şehir** | Şehir adı (isteğe bağlı, şehir düzeyinde vergi kuralları için) |
| **Posta Kodları** | Belirli posta kodlarının listesi (isteğe bağlı, posta kodu düzeyinde kurallar için) |

Kurallar en spesifikten en az spesifik olanlara eşleşir. Belirli bir posta kodu için bir kural, aynı eyalet için bir kuraldan daha önceliklidir, bu da ülke genelindeki kurallardan daha önceliklidir.

### Uygulama Kuralları

| Alan | Açıklama |
|------|----------|
| **Gönderim için Uygulanır** | İşaretlendiğinde bu vergi gönderim ücretlerine de uygulanır |
| **Bileşik Vergi** | İşaretlendiğinde bu vergi diğer vergilerin üzerine hesaplanır (temel tutar artı önce uygulanan vergiler) |

### Ürün Muafiyetleri

| Alan | Açıklama |
|------|----------|
| **Vergiden Muaf Ürün Türleri** | Bu vergiden muaf ürün türleri (örneğin, dijital, hizmet) |
| **Vergiden Muaf Kategoriler** | Bu vergiden muaf özel ürün kategorileri |

## Vergi Türleri

| Tür | Kullanım Alanı | Örnekler |
|-----|----------------|--------|
| **Satış Vergisi** | ABD, Kanada | Eyalet ve eyalet vergileri |
| **KDV** | Avrupa, İngiltere, Asya ve Afrika'nın çoğu | Katma Değer Vergisi |
| **GST** | Avustralya, Yeni Zelanda, Hindistan, Singapur | Mal ve Hizmet Vergisi |
| **Özel Vergi** | Özel durumlar | Yerel ek ücretler, çevre vergileri, lüks vergileri |

## Vergi Hesaplama Nasıl Çalışır

Müşteri ödeme ekranına ulaştığında, sistem siparişlerin vergilerini otomatik olarak hesaplar:

1. **Coğrafi eşleştirme** — müşteri ülkesiyle eşleşen tüm etkin kuralları bulur, ardından eyalet, şehir ve posta kodu üzerinden daraltır
2. **Özelilik puanlama** — daha spesifik kurallar (posta kodu > şehir > eyalet > ülke) daha yüksek sıralanır
3. **Öncelik sıralaması** — aynı özelilik düzeyinde, daha yüksek öncelikli kurallar önceliklidir
4. **Ürün muafiyetleri** — muaf ürünler, her uygulanabilir kuraldan dışlanır
5. **Bileşik olmayan vergiler** — her ürünün temel fiyatına göre ilk olarak hesaplanır
6. **Bileşik vergiler** — temel fiyat artı tüm bileşik olmayan vergilerin uygulandığı şekilde hesaplanır
7. **Gönderim vergisi** — bir kural "Gönderim için Uygulanır" etkinse, gönderim ücreti vergi hesaplamasına dahil edilir

Vergi analizi siparişle birlikte saklanır, böylece hangi kuralların uygulandığını ve her birinin ne kadar katkı sağladığını görebilirsiniz.

## Ortak Kurulumlar

### AB Mağazası

1. **Ön Ayarları Yükle**'ye tıklayın ve **AB KDV Oranları** grubunu yükleyin
2. Bu, tüm AB üyesi ülkeler için mevcut standart oranlarla KDV kuralları oluşturur
3. AB'ye satış yaparsanız, **İngiltere KDV**'yi isteğe bağlı olarak yükleyin

### ABD Mağazası

1. **Ön Ayarları Yükle**'ye tıklayın ve **ABD Eyaletleri Satış Vergisi** grubunu yükleyin
2. Bu, satış vergisi toplayan tüm ABD eyaletleri için satış vergisi kuralları oluşturur
3. Şehir düzeyinde vergiler için, şehir alanını doldurun ve daha yüksek bir öncelik ayarlayın

### Çoklu Bölgesel Mağaza

1. Satış yaptığınız her pazar için birden fazla ön ayar grubu yükleyin
2. Sistem, her müşteri konumuna göre doğru vergiyi uygular
3. İşletmenizin özel ihtiyaçlarına göre gerekli olan bireysel kuralları ayarlayın

## İpuçları

- **Ön ayarlardan başlayın** — hedef pazarlar için ön ayar gruplarını yükleyin, ardından her kuralı sıfırdan oluşturmak yerine bireysel oranları özelleştirin.
- **Öncelikleri dikkatle ayarlayın** — daha spesifik yerel kurallar için daha yüksek öncelik değerleri ayarlayarak, daha geniş bölgesel kuralları doğru şekilde geçersiz kılabilirsiniz.
- **Bileşik vergi dikkatle kontrol edin** — bileşik vergi nadirdir. Çoğu yerel yönetmelik basit (bileşik olmayan) vergi kullanır. Yerel düzenlemelerin özellikle vergi üzerinde vergi hesaplama gerektirdiğini belirten durumlarda bileşik vergiyi etkinleştirin.
- **Kuralları etkin/devre dışı bırakın** — mevsimsel veya geçici değişiklikler için vergi kurallarını silmek yerine, onları devre dışı bırakın ve gerekli olduğunda tekrar etkinleştirin.
- **Yaşamaya hazır olunmadan test edin** — vergi kurallarınızı ayarladıktan sonra farklı adreslerden test siparişler vererek doğru vergilerin uygulandığını doğrulayın.

