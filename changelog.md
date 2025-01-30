# Changelog

## [0.2.0] - 2024-03-XX

### Güvenlik Uyumluluk Denetleyicisi

#### Eklenen Özellikler
- Linux ve Windows sistemleri için güvenlik kuralları eklendi
  - Parola politikaları
  - Dosya sistemi güvenliği
  - Ağ güvenliği
  - Loglama ve denetim
  - Servis güvenliği
  - Güvenlik duvarı yapılandırması
- Sistem tipi otomatik tespit özelliği
- Kural yükleme ve değerlendirme mekanizması
- Komut çalıştırma ve sonuç değerlendirme
- JSON ve metin formatında rapor oluşturma
- CLI arayüzü
  - Denetim çalıştırma
  - Rapor formatı seçimi (JSON/Text)
  - Kategori ve seviye filtreleme
  - Detaylı loglama
  - Rapor analizi
- Kapsamlı test altyapısı
  - Birim testler
  - CLI testleri
  - Mock ve fixture kullanımı

#### Yapılacaklar
- Daha fazla güvenlik kuralı ekleme
- Özel kural dosyası desteği geliştirme
- HTML rapor formatı ekleme
- Zamanlanmış denetim desteği
- Uzak sistem denetimi desteği
- Merkezi raporlama sistemi entegrasyonu

## [0.1.0] - 2024-03-XX

### SQL Injection Scanner

#### Eklenen Özellikler
- SQL Injection payload üreteci
  - Boolean-based payloadlar
  - Time-based payloadlar
  - Error-based payloadlar
  - UNION-based payloadlar
- Ana tarama modülü
  - Farklı SQL injection türlerini tespit etme
  - DBMS tespiti
  - WAF bypass teknikleri
- CLI arayüzü
  - URL ve parametre belirtme
  - Cookie desteği
  - JSON rapor çıktısı
  - Detaylı loglama
- Test altyapısı
  - Birim testler
  - Test web uygulaması

### XSS Scanner

#### Eklenen Özellikler
- XSS payload üreteci
  - HTML context payloadları
  - Attribute context payloadları
  - JavaScript context payloadları
  - URL context payloadları
  - DOM-based payloadları
- Ana tarama modülü
  - Context tespiti
  - Payload test
  - WAF bypass
- CLI arayüzü
  - URL ve parametre belirtme
  - Cookie desteği
  - JSON rapor çıktısı
  - Detaylı loglama
- Test altyapısı
  - Birim testler
  - Test web uygulaması

### SSRF Scanner

#### Eklenen Özellikler
- SSRF payload üreteci
  - Basic payloadlar
  - Blind payloadlar
  - DNS payloadları
  - Cloud metadata payloadları
  - Internal network payloadları
- Ana tarama modülü
  - SSRF tespiti
  - Cloud metadata erişim testi
  - Internal network discovery
- CLI arayüzü
  - URL ve parametre belirtme
  - Cookie desteği
  - JSON rapor çıktısı
  - Detaylı loglama
- Test altyapısı
  - Birim testler
  - Test web uygulaması

### Başlangıç
- Proje başlatıldı
- Temel dosya yapısı oluşturuldu
- Changelog.md dosyası eklendi
- Proje kategorileri belirlendi:
  1. Zafiyet Tarama Projeleri
  2. Özel Güvenlik Araçları

### Eklenen Özellikler
- Temel proje yapısı oluşturuldu
- Proje dizin yapısı kategorilere göre düzenlendi
- Gerekli Python paketleri requirements.txt'ye eklendi

### SQL Injection Scanner [0.1.0]
#### Eklenen Özellikler
- Payload üreteci modülü geliştirildi
  - Boolean-based payloadlar
  - Error-based payloadlar
  - Time-based payloadlar
  - Union-based payloadlar
  - Veritabanı parmak izi payloadları
- Ana tarayıcı modülü geliştirildi
  - Veritabanı türü tespiti
  - Boolean-based SQL injection tespiti
  - Error-based SQL injection tespiti
  - Time-based SQL injection tespiti
  - Union-based SQL injection tespiti
- CLI arayüzü eklendi
  - Komut satırı parametreleri
  - JSON formatında rapor çıktısı
  - Detaylı loglama desteği
- Test altyapısı oluşturuldu
  - Birim testler
  - Entegrasyon testleri
  - Test web uygulaması

#### Yapılacaklar
- [x] Daha fazla payload eklenmesi
- [x] Blind SQL injection desteği
- [x] Otomatik WAF tespiti
- [x] Proxy desteği
- [x] HTML rapor formatı

### XSS Scanner [0.1.0]
#### Eklenen Özellikler
- Payload üreteci modülü geliştirildi
  - HTML bağlamı payloadları
  - Öznitelik bağlamı payloadları
  - Script bağlamı payloadları
  - URL bağlamı payloadları
  - Style bağlamı payloadları
  - DOM tabanlı payloadlar
- Ana tarayıcı modülü geliştirildi
  - Bağlam tespiti
  - HTML bağlamı XSS tespiti
  - Öznitelik bağlamı XSS tespiti
  - Script bağlamı XSS tespiti
  - URL bağlamı XSS tespiti
  - Style bağlamı XSS tespiti
  - DOM tabanlı XSS tespiti
- CLI arayüzü eklendi
  - Komut satırı parametreleri
  - JSON formatında rapor çıktısı
  - Detaylı loglama desteği
- Test altyapısı oluşturuldu
  - Birim testler
  - Entegrasyon testleri
  - Test web uygulaması

#### Yapılacaklar
- [x] Daha fazla payload eklenmesi
- [x] Stored XSS desteği
- [x] WAF bypass teknikleri
- [x] Encoding/decoding desteği
- [ ] HTML rapor formatı

### SSRF Scanner [0.1.0]
#### Eklenen Özellikler
- Payload üreteci modülü geliştirildi
  - Temel SSRF payloadları
  - Kör SSRF payloadları
  - DNS tabanlı SSRF payloadları
  - Cloud metadata payloadları
  - İç ağ keşif payloadları
- Ana tarayıcı modülü geliştirildi
  - Temel SSRF tespiti
  - Kör SSRF tespiti
  - DNS tabanlı SSRF tespiti
  - Cloud metadata erişim tespiti
  - İç ağ keşif tespiti
- CLI arayüzü eklendi
  - Komut satırı parametreleri
  - JSON formatında rapor çıktısı
  - Detaylı loglama desteği
- Test altyapısı oluşturuldu
  - Birim testler
  - Entegrasyon testleri
  - Test web uygulaması

#### Yapılacaklar
- [ ] Daha fazla payload eklenmesi
- [ ] Protokol desteğinin genişletilmesi
- [ ] WAF bypass teknikleri
- [ ] Proxy desteği
- [ ] HTML rapor formatı

### Özel Güvenlik Araçları
#### Automated Pentest Reporter
- [ ] Zafiyet değerlendirmesi
- [ ] Risk skorlama
- [ ] Rapor üretimi

#### Security Compliance Checker
- [ ] Policy doğrulama
- [ ] Yapılandırma denetimi
- [ ] Düzeltme önerileri

#### Security Metrics Dashboard
- [ ] KPI takibi
- [ ] Risk görselleştirme
- [ ] Trend analizi

### Yapılacaklar
- [x] Proje dizin yapısının oluşturulması
- [x] Gerekli kütüphanelerin belirlenmesi
- [x] SQL Injection Scanner için temel kod yapısının oluşturulması
- [x] XSS Scanner için temel kod yapısının oluşturulması
- [x] SSRF Scanner için temel kod yapısının oluşturulması
- [ ] Diğer modüller için temel kod yapısının oluşturulması
- [x] SQL Injection Scanner için test ortamının hazırlanması
- [x] XSS Scanner için test ortamının hazırlanması
- [x] SSRF Scanner için test ortamının hazırlanması
- [ ] Diğer modüller için test ortamlarının hazırlanması
- [ ] Dokümantasyonun geliştirilmesi

## [0.3.0] - 2024-03-XX

### Güvenlik Metrik Gösterge Paneli

#### Eklenen Özellikler
- Metrik veri toplama modülü geliştirildi
  - Zafiyet tarama sonuçlarından metrik toplama
  - Uyumluluk raporlarından metrik toplama
  - Güvenlik olaylarından metrik toplama
  - Performans metriklerini toplama
- Metrik analiz ve görselleştirme modülü geliştirildi
  - Zafiyet trend grafikleri
  - Uyumluluk durum pasta grafikleri
  - Güvenlik olayları bar grafikleri
  - Performans radar grafikleri
  - Özet rapor oluşturma
- CLI arayüzü eklendi
  - Metrik toplama komutu (topla)
    - Zafiyet raporu desteği
    - Uyumluluk raporu desteği
    - Olay ve performans metrik desteği
    - Tarih aralığı filtreleme
  - Rapor oluşturma komutu (raporla)
    - HTML formatında grafikler
    - JSON formatında özet rapor
  - Analiz komutu (analiz)
    - Metrik tipi filtreleme
    - Detaylı özet bilgiler
    - Konsol çıktısı
- Test altyapısı oluşturuldu
  - CLI komut testleri
  - Mock ve fixture kullanımı
  - Hata durumu testleri
  - Test veri setleri
- Veri formatları ve sınıflar tanımlandı
  - GüvenlikMetriği veri sınıfı
  - MetrikTipi ve MetrikSeviyesi enumları
  - JSON tabanlı veri depolama

#### Yapılacaklar
- Daha fazla metrik türü ekleme
- Özelleştirilebilir grafik temaları
- Gerçek zamanlı metrik toplama
- Metrik alarm ve uyarı sistemi
- PDF rapor formatı desteği
- Metrik karşılaştırma ve trend analizi
- Metrik hedef ve eşik değerleri
- API entegrasyonları

## [0.4.0] - 2024-03-XX

### SQL Injection Scanner

#### Eklenen Özellikler
- Blind SQL injection desteği eklendi:
  - Boolean-based blind SQL injection tespiti
  - Error-based blind SQL injection tespiti
  - Time-based blind SQL injection tespiti
  - Content-based blind SQL injection tespiti
- Blind SQL injection için yeni payload'lar eklendi
- Test web uygulamasına blind SQL injection test endpoint'leri eklendi
- Kapsamlı birim testleri eklendi
- WAF tespit ve bypass desteği eklendi:
  - Farklı WAF türlerini tespit etme (Cloudflare, Akamai, Imperva, F5 ASM, ModSecurity, FortiWeb)
  - WAF parmak izi tespiti (header, yanıt ve engelleme pattern'leri)
  - WAF türüne özel bypass teknikleri
  - Genel WAF bypass teknikleri (boşluk alternatifleri, yorum kullanımı, encoding)
  - WAF tespit ve bypass için kapsamlı test altyapısı

#### Yapılacaklar
- [x] Daha fazla payload eklenmesi
- [x] Blind SQL injection desteği
- [x] Otomatik WAF tespiti
- [x] Proxy desteği
- [x] HTML rapor formatı

### XSS Scanner

#### Yapılacaklar
- Daha fazla payload eklenmesi
- Stored XSS desteği
- WAF bypass teknikleri
- Encoding/decoding desteği
- HTML rapor formatı

### SSRF Scanner

#### Yapılacaklar
- Daha fazla payload eklenmesi
- Protokol desteğinin genişletilmesi
- WAF bypass teknikleri
- Proxy desteği
- HTML rapor formatı

### Genel Görevler
- Diğer modüller için temel kod yapısının oluşturulması
- Diğer modüller için test ortamlarının hazırlanması
- Dokümantasyonun geliştirilmesi

## [0.3.0] - 2024-03-XX

### Eklenen Özellikler
- XSS Scanner için HTML rapor formatı desteği
- XSS Scanner için encoding/decoding desteği
- XSS Scanner için WAF bypass teknikleri
- XSS Scanner için Stored XSS desteği
- SQL Injection Scanner için HTML rapor formatı desteği
- SQL Injection Scanner için proxy desteği
- SQL Injection Scanner için WAF bypass teknikleri
- SQL Injection Scanner için blind SQL injection desteği
- SSRF Scanner için HTML rapor formatı desteği
- SSRF Scanner için proxy desteği
- SSRF Scanner için WAF bypass teknikleri

### Yapılacaklar
- [x] Proje dizin yapısının oluşturulması
- [x] SQL Injection Scanner için temel kod yapısının oluşturulması
- [x] XSS Scanner için temel kod yapısının oluşturulması
- [x] SSRF Scanner için temel kod yapısının oluşturulması
- [x] SQL Injection Scanner için test ortamının hazırlanması
- [x] XSS Scanner için test ortamının hazırlanması
- [x] SSRF Scanner için test ortamının hazırlanması
- [x] SQL Injection Scanner için blind SQL injection desteği
- [x] SQL Injection Scanner için WAF tespiti
- [x] SQL Injection Scanner için proxy desteği
- [x] SQL Injection Scanner için HTML rapor formatı
- [x] XSS Scanner için Stored XSS desteği
- [x] XSS Scanner için WAF bypass teknikleri
- [x] XSS Scanner için encoding/decoding desteği
- [x] XSS Scanner için HTML rapor formatı
- [x] SSRF Scanner için WAF bypass teknikleri
- [x] SSRF Scanner için proxy desteği
- [x] SSRF Scanner için HTML rapor formatı
- [ ] Daha fazla payload eklenmesi
- [ ] Dokümantasyon hazırlanması
- [ ] Ek modüller için test ortamlarının hazırlanması 