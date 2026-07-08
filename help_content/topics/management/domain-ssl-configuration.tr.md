---
title: Alan Adı & SSL Yapılandırması
---

Bu kılavuz, özel bir alan adını Spwig mağazanıza bağlamayı ve güvenli HTTPS erişimi için SSL sertifikaları kurmayı açıklar. Alan adını kurulum sırasında yapılandırabilir ya da daha sonra ekleyebilirsiniz.

## Kurulumdan Sonra Alan Adı Ekleme

Eğer Spwig'i bir alan adı olmadan (sunucunuzun IP adresi kullanılarak) kurduysanız, herhangi bir zaman ekleyebilirsiniz.

### Adım 1: DNS'yi Ayarla

Alan adı kaydedicinizle veya DNS sağlayıcınızla:

1. Alan adınız (veya alt alan adınız) için bir **A kaydı** oluşturun ve bu kaydı sunucunuzun IP adresine yönlendirin
2. `shop.example.com` gibi bir alt alan adı kullanıyorsanız, `shop` için A kaydını oluşturun
3. DNS yayılımını bekleyin — bu genellikle 5–60 dakika sürer

DNS kaydının çalışıp çalışmadığını doğrulayın:

```bash
dig +short shop.example.com
```

Bu komut, sunucunuzun IP adresini döndürmelidir.

### Adım 2: Alan adı yapılandırma betiğini çalıştırın

Sunucunuza SSH ile bağlanın ve Spwig kurulum dizininize gidin:

```bash
./configure-domain.sh
```

Betiğin yapacağılar:

1. Alan adınızı isteyecektir
2. DNS'in sunucunuza işaret edip etmediğini doğrulayacaktır
3. Mağazanın yapılandırmasını güncelleyecektir
4. Let's Encrypt'den ücretsiz bir SSL sertifikası elde edecektir
5. Web sunucusunu HTTPS kullanacak şekilde yapılandıracaktır
6. İlgili hizmetleri yeniden başlatacaktır

Mağazanız artık `https://yourdomain.com` adresinden erişilebilir olacak.

### Adım 3: Mağaza ayarlarını güncelle

Alan adınızı ekledikten sonra, yönetici paneline girin ve **Mağaza Ayarları**'na gidin. **Mağaza URL'si** yeni alan adınızla eşleştiğini doğrulayın. Bu, e-postaların, faturaların ve bağlantıların doğru adresiyle kullanılmasını sağlar.

## SSL Sertifikaları

### Otomatik SSL (Let's Encrypt)

**Tekil modda**, kurulum otomatik olarak Let's Encrypt'den ücretsiz bir SSL sertifikası alır. Bu sertifikalar:

- Tüm büyük tarayıcılar tarafından güvenilir
- 90 gün geçerlidir
- Otomatik olarak yenilenir — günlük olarak yenileme kontrolü yapılır ve sertifikalar 30 günden az kala yenilenir
- Tam olarak alan adınızı kapsar (örneğin `shop.example.com`)

Yenileme işlemini elle yönetmenize gerek yoktur.

### Kendinden İmzalı Sertifikalar

Bazı durumlarda, Spwig bir kendinden imzalı sertifika kullanır:

- **Yerel mod** kurulumları (geliştirme/test amaçlı)
- Let's Encrypt sunucunuza ulaşamadığında (80 numaralı portu engelleyen bir güvenlik duvarı, DNS henüz yayılmadıysa)
- Konfigüre edilmiş bir alan adı yoksa (yalnızca IP adresi erişimi)

Kendinden imzalı sertifikalar trafiği şifreler ancak tarayıcılar tarafından güvenilmez — ziyaretçiler bir güvenlik uyarısı görecek. Bu test amaçlı kabul edilebilir ancak üretimde kullanılmamalıdır.

### Yan Taraf Modu SSL

**Yan taraf modunda**, mevcut web sunucunuz (Apache, Nginx, Caddy vb.) SSL sonlandırma işlemini üstlenir. Spwig, proxy'niz arkasında HTTP portu üzerinden çalışır. Ana web sunucunuzda SSL'i normal şekilde yapılandırın.

Yükleyici, proxy yapılandırması bloğu oluşturur ve bunu web sunucunuza ekleyebilirsiniz. Nginx için şöyle görünebilir:

```nginx
location / {
    proxy_pass http://127.0.0.1:8080;
    proxy_set_header Host $host;
    proxy_set_header X-Real-IP $remote_addr;
    proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    proxy_set_header X-Forwarded-Proto $scheme;
}
```

## Alan Adınızı Değiştirme

Farklı bir alan adına geçmek için:

1. Yeni alan adı için DNS'yi ayarlayın (sunucunuza işaret eden A kaydı)
2. Yeni alan adıyla `./configure-domain.sh` betiğini tekrar çalıştırın
3. Betik tüm yapılandırmaları günceller, yeni bir sertifika alır ve hizmetleri yeniden başlatır
4. Yönetici panelindeki **Mağaza Ayarları**'nı yeni URL ile güncelleyin

Eski alan adı yapılandırma güncellendiğinde artık çalışmaz.

## Sorun Giderme

### "DNS doğrulama başarısız"

Configure-domain betiği, sertifika isteği yapmadan önce alan adının sunucunuza işaret edip etmediğini kontrol eder. Bu kontrol başarısız olursa:

- `dig +short yourdomain.com` ile A kaydının doğru olup olmadığını kontrol edin
- DNS yayılımını birkaç dakika daha bekleyin
- Yapılandırdığınız alan adının veya alt alan adının tamamını kontrol edin (wildcard değil)

### "Let's Encrypt oran limiti aşıldı"

Let's Encrypt, haftada bir alan adı için 5 sertifika isteğine izin verir. Bu limiti aşırsanız:



- 7 gün bekleyin ve tekrar denemeyi unutmayın
- Bu süre zarfında farklı bir alt etki alanı kullanın
- Beklerken mağaza HTTP üzerinden veya kendi imzalı sertifika ile erişilebilir kalır

### "80 numaralı port erişilebilir değil"

Let's Encrypt, etki alan sahipliğini doğrulamak için sunucunuzdaki 80 numaralı porta bağlanmalıdır. Aşağıdakileri kontrol edin:

- Yangın duvarınız 80 numaralı gelen TCP trafiğini izin veriyor olmalı
- 80 numaralı portu engelleyen başka bir uygulama bulunmamalı
- Bulut sağlayıcınızın güvenlik grubu veya ağ yangın duvarı 80 numaralı portu izin veriyor olmalı

### Sertifika yenileme hataları

Eğer otomatik yenileme başarısız olursa, sertifika 90 gün sonra sona erecektir. Manuel olarak yenilemek için:

```bash
docker exec spwig_nginx certbot renew
docker exec spwig_nginx nginx -s reload
```

Bu işlem başarısız olursa, yenileme günlüklerini inceleyin. En yaygın neden, ilk kurulumdan sonra yangın duvarı değişikliğiyle 80 numaralı portun engellenmesidir.