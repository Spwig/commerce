---
title: Gölge Düzenleyici
---

Gölge düzenleyici, yapılandırılabilir kutu gölgeleri ve metin gölgeleri ile öğelere derinlik ve boyut eklemenizi sağlar. Gölge, görsel hiyerarşi oluşturur, önemli öğelere dikkat çeker ve mağazanıza modern ve pürüzsüz bir his verir. Herhangi bir öğenin **Stil sekmesine** gidin ve **Etkiler** grubunu arayın, böylece gölge düzenleyiciye erişebilirsiniz.

![Gölge Düzenleyici](/static/core/admin/img/help/shadow-editor/shadow-editor.webp)

## Gölge Türleri

Düzenleyici, üstte iki sekme sağlar:

- **Kutu Gölgesi** — Öğenin sınırlayıcı kutasının etrafına bir gölge ekler. Kartlar, butonlar, konteynerler, resimler ve bölümler için kullanın.
- **Metin Gölgesi** — Sadece metin karakterlerinin arkasına bir gölge ekler. Başlıklar veya resimlerin üzerine yerleştirilmiş metinler için okunabilirliği artırmak için kullanın.

Her sekme kendi bağımsız yapılandırması ile gelir. Gerekirse aynı öğeye hem kutu gölgesi hem de metin gölgesi uygulayabilirsiniz.

## Gölge Özellikleri

Her gölge katmanı aşağıdaki özelliklerle tanımlanır:

| Özellik | Açıklama | Aralık |
|----------|-------------|-------|
| **X Ekseni Kayması** | Gölgenin öğeden yatay uzaklığı | -50px ile 50px |
| **Y Ekseni Kayması** | Gölgenin öğeden dikey uzaklığı | -50px ile 50px |
| **Bulanıklık Yarıçapı** | Gölge kenarının ne kadar yumuşak veya dağınık olduğunun belirtimi. Daha yüksek değerler daha yumuşak gölgeler oluşturur. | 0px ile 100px |
| **Dağılım Yarıçapı** | Gölge boyutunu öğeye göre genişletir veya daraltır (sadece kutu gölgesi) | -50px ile 50px |
| **Renk** | Gölge rengi, renk seçicisi ile tam opaklık desteği ile yapılandırılabilir | Herhangi bir alfa değeri ile renk |
| **İç Gölge** | Gölgenin öğenin içinde yer almasını sağlar (sadece kutu gölgesi) | Aç/ Kapalı |

Değerleri kaydırıcıları kullanarak ayarlayabilir veya doğrudan girdi alanlarına hassas sayıları yazabilirsiniz.

## Birden Fazla Gölge

Bir öğeye birden fazla gölge katmanı叠加 ederek karmaşık ve gerçekçi derinlik etkileri oluşturabilirsiniz:

- **+** butonuna tıklayarak yeni bir gölge katmanı ekleyin
- Her katman, gölge listesinde bir satır olarak görünür ve kendi kontrolleri vardır
- Katmanları sürükleyerek sıralayın — gölgeler, listedeki sıraya göre işlenir, ilk katman en üstte yer alır
- Herhangi bir katmanda **göz simgesini** açıp kapatarak geçici olarak gizleyebilirsiniz, yapılandırmayı silmeden
- **Çöp simgesine** tıklayarak bir katmanı kaldırın

Dar, koyu bir gölge ile geniş, yumuşak bir gölge birleşimi, fiziksel derinlik hissi yaratan doğal bir "yükselen" etki yaratır.

## Gölge Ön Ayarları

Ön ayarlar, tek bir tıklamayla yaygın gölge stillerini eklemenizi sağlar:

| Ön Ayar | Açıklama |
|--------|-------------|
| **Küçük** | Hafif, yakınlık gölgesi, hafif yükseltme için (kartlar, girdiler) |
| **Orta** | Etkileşimli öğeler için orta derinlik (butonlar, açılır menüler) |
| **Büyük** | Yüzen öğeler için dikkat çeken gölge (modaller, popüller) |
| **Yumuşak** | Geniş bulanıklık ve düşük opaklık ile hafif, dağınık bir ışık etkisi |
| **Sert** | Minimum bulanıklık ve yüksek opaklık ile keskin, tanımlı bir kenar |
| **İç Gölge** | Basılmış veya içe çökmüş bir görünüm için iç gölge |

Ön ayar uygulandıktan sonra bireysel özellikleri ayarlayarak sonucu ince ayarlayabilirsiniz.

## Mevcut vs. Yeni Önizleme

Düzenleyicinin alt kısmında, **mevcut** gölge (kaydedilmiş) ve **yeni** gölge (bekleyen değişiklikler) için iki karşılaştırma kutusu vardır. Bu yan yana görünüm, değişiklikleri onaylamadan önce farkı değerlendirmeyi kolaylaştırır. **Uygula**'ya tıklayarak onaylayabilir veya değişiklikleri atmak için başka bir yere tıklayabilirsiniz.

## Nerede Görünür

Gölge düzenleyici, aşağıdaki yerlerde kullanılabilir:

- **Sayfa Oluşturucu** — Bölüm, konteyner, sütun ve bireysel öğelerdeki **Stil** sekmesi, **Etkiler** grubu
- **Başlık/Açılış Oluşturucu** — Logo, arama çubuğu ve navigasyon öğeleri gibi öğeler için widget seviyesinde gölge ayarları

Etkiler stilleri grubunu destekleyen her öğe, gölge düzenleyici kontrollerini gösterir.

## İpuçları

- Çoğu öğe için hafif gölgeler (Küçük veya Yumuşak ön ayarları) kullanın — ağırlıklı gölgeler, bir tasarımın kalabalık hissine neden olabilir.
- Yakın, koyu bir gölge ile uzak, hafif bir gölge birleşimi, en doğal görünen yükseltme etkisini yaratır.
- Giriş alanları ve konteynerlerde iç gölgeler, çukur bir panel etkisi yaratmak için iyi çalışır.
- Metin gölgeleri minimal olmalıdır — 1px kayma ile hafif bulanıklık, resim arka planlarında okunabilirliği artırır ve eski bir görünüm yaratmaz.
- Temanız karanlık modu geçişini destekliyorsa, gölgelerin hem açık hem karanlık arka planlarda test edilmesi önerilir.
