---
title: Senkronizasyon Tokenı Yönetimi
---

Senkronizasyon tokenları, iki Spwig kurulumunun birbirleriyle iletişim kurmasına olanak tanıyan güvenli kimlik bilgileridir. Ayarları senkronize etmeden veya mağazalar arasında veri geçirmeden önce, **alıcı** mağazada bir token oluşturmanız ve bunu **gönderen** mağazaya sağlamanız gerekir.

## Senkronizasyon Tokenlarının Nasıl Çalıştığı

Senkronizasyon tokenı, iki Spwig kurulumu arasında istekleri doğrulayan tek seferde görülebilir bir API anahtarıdır. Bağlantıyı kurduğunuzda, uzak mağaza bu tokenı, mağazanıza okuma veya yazma izni olduğunu ispatlamak için kullanır.

- Tokenlar, **bağlanacak** olan mağazada (hedef) oluşturulur
- Her token, oluşturulmasından hemen sonra yalnızca bir kez görülebilir
- Tokenlar herhangi bir zamanda iptal edilebilir ve bu, erişimi anında keser
- Bir mağaza, farklı bağlantılar için birden fazla aktif tokena sahip olabilir

## Token Oluşturma

1. Yönetici menüsünden **Data Migration > Spwig-to-Spwig Sync** bölümüne gidin
2. Senkronizasyon panelinde **Manage Tokens** (Tokenları Yönet) seçeneğini tıklayın
3. Token için tanımlayıcı bir isim girin (örneğin, "Staging Server" veya "Production Sync")
4. **Generate Token** (Token Oluştur) seçeneğini tıklayın
5. **Tokenı hemen kopyalayın** -- tekrar gösterilmeyecektir

> **Önemli:** Tokenı güvenli bir şekilde saklayın. Kaybederseniz, yeni bir token oluşturmanız gerekir.

## Token Kullanımı

Hedef mağazadan token aldıktan sonra:

1. Bağlantıyı başlatacak olan mağazadaki **Spwig-to-Spwig Sync** paneline gidin
2. Yeni bir **Settings Sync** (Ayar Senkronizasyonu) veya **Full Migration** (Tam Veri Geçiş) başlatın
3. Bağlantı adımı sırasında, hedef mağazanın URL'sini girin ve tokenı yapıştırın
4. **Test Connection** (Bağlantıyı Test Et) seçeneğini tıklayarak çalıştığını doğrulayın
5. Bağlantı gelecekteki kullanım için kaydedilecektir

## Token İptal Etme

Tokenın ihlal edildiğini veya artık gerekli olmadığını fark ettiğinizde:

1. Senkronizasyon panelinde **Manage Tokens** (Tokenları Yönet) bölümüne gidin
2. İptal etmek istediğiniz tokenı bulun
3. **Revoke** (İptal Et) butonuna tıklayın
4. İptali onaylayın

Token iptal edildiğinde hemen etkili olur. Bu tokenı kullanan aktif bağlantılar çalışmayı bırakacak ve yeni bir tokenla yeniden yapılandırılmalıdır.

## En İyi Uygulamalar

- **Tokenları tanımlayıcı isimlerle** adlandırın, böylece her tokenın hangi bağlantıya ait olduğunu biliyorsunuz
- **Kullanılmayan tokenları iptal edin** ve güvenlik riskini minimize edin
- **Her bağlanan mağaza için ayrı tokenlar** oluşturun, birden fazla mağaza arasında tek bir token paylaşmayın
- **Periyodik olarak tokenları yeniden oluşturun**, özellikle personel değişiklikleri gibi güvenlik rutinlerinin bir parçası olarak