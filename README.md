# 🛡️ İleri Sızma Testi Projesi

## 📝 Proje Hakkında
Bu proje, web uygulamalarında yaygın olarak karşılaşılan güvenlik açıklarını otomatik olarak tespit etmek için geliştirilmiş bir güvenlik tarama aracıdır. Şu anda aşağıdaki modülleri içermektedir:

### 🔍 Zafiyet Tarayıcıları
- 💉 SQL Injection Scanner
- 🔍 XSS (Cross-Site Scripting) Scanner  
- 🌐 SSRF (Server-Side Request Forgery) Scanner

### 🛠️ Güvenlik Araçları
- 📊 Pentest Reporter: Otomatik penetrasyon testi raporu oluşturma aracı
- ✅ Compliance Checker: Sistem güvenlik uyumluluk denetleyicisi
- 📈 Metrics Dashboard: Güvenlik metriklerini görselleştirme paneli

## 🚀 Özellikler

### SQL Injection Scanner
- Boolean, Error, Time ve Union tabanlı SQL Injection tespiti
- Blind SQL Injection desteği
- WAF (Web Application Firewall) tespiti ve bypass teknikleri
- HTML ve JSON formatında raporlama
- Proxy desteği

### XSS Scanner
- Reflected, Stored ve DOM tabanlı XSS tespiti
- Farklı XSS bağlamları için özel payload'lar (HTML, JavaScript, URL, vb.)
- Encoding/Decoding desteği
- WAF bypass teknikleri
- Detaylı HTML raporlama

### SSRF Scanner
- Temel SSRF açıklarının tespiti
- Cloud metadata servislerine erişim kontrolü
- İç ağ taraması
- Protokol bazlı testler (HTTP, FTP, File, vb.)
- WAF bypass teknikleri
- HTML raporlama

### Pentest Reporter
- Kapsamlı ve özelleştirilebilir raporlama
- Çoklu format desteği (HTML, PDF, JSON)
- Zafiyet risk skorlaması
- Detaylı PoC ve çözüm önerileri
- Yönetici özeti ve teknik detaylar
- Grafik ve istatistikler

### Compliance Checker
- Windows ve Linux sistemleri için güvenlik kontrolleri
- CIS Benchmark uyumluluk denetimi
- Güvenlik politikası kontrolleri
- Otomatik düzeltme önerileri
- Detaylı uyumluluk raporları
- Kategori ve seviye bazlı filtreleme

### Metrics Dashboard
- Gerçek zamanlı güvenlik metrikleri
- Zafiyet trend analizi
- Risk skorlama ve göstergeleri
- Özelleştirilebilir gösterge panelleri
- Periyodik raporlama
- Metrik karşılaştırma ve analiz

## 🛠️ Kurulum

1. Gerekli Python paketlerini yükleyin:
```bash
pip install -r requirements.txt
```

2. Test ortamını başlatın (opsiyonel):
```bash
cd tests/vulnerability_scanners/test_app
python app.py
```

## 📖 Kullanım

### Zafiyet Tarayıcıları

#### SQL Injection Taraması
```bash
python -m src.vulnerability_scanners.sql_injection.cli scan http://example.com --parameter id --output report.html --format html
```

#### XSS Taraması
```bash
python -m src.vulnerability_scanners.xss_scanner.cli scan http://example.com --parameter search --output xss_report.html --format html
```

#### SSRF Taraması
```bash
python -m src.vulnerability_scanners.ssrf_scanner.cli scan http://example.com --parameter url --output ssrf_report.html --format html
```

### Güvenlik Araçları

#### Pentest Raporu Oluşturma
```bash
python -m src.security_tools.pentest_reporter.cli generate zafiyet_raporu.json --output pentest_raporu.html --format html
```

#### Güvenlik Uyumluluk Denetimi
```bash
python -m src.security_tools.compliance_checker.cli denetle --output uyumluluk_raporu.json
```

#### Güvenlik Metrikleri Görüntüleme
```bash
python -m src.security_tools.metrics_dashboard.cli raporla metrikler.json --cikti-dizini dashboard/
```

### Ortak Parametreler
- `--parameter, -p`: Test edilecek parametre
- `--cookies, -c`: Cookie değerleri (JSON formatında)
- `--proxy, -x`: Proxy URL (örn: http://127.0.0.1:8080)
- `--output, -o`: Rapor çıktı dosyası
- `--format, -f`: Rapor formatı (json veya html)
- `--verbose`: Detaylı loglama

## 📊 Raporlama
Tarama ve analiz sonuçları HTML veya JSON formatında kaydedilebilir. HTML raporları şunları içerir:
- Tespit edilen zafiyetlerin özeti
- Risk seviyelerine göre dağılım
- Zafiyet türlerine göre grafikler
- Her zafiyet için detaylı bilgiler ve PoC
- WAF tespiti ve bypass bilgileri
- Güvenlik metrikleri ve trendler
- Uyumluluk durumu ve öneriler

## 🔒 Güvenlik Notları
- Bu aracı yalnızca izin verilen sistemlerde kullanın
- Üretim ortamlarında dikkatli kullanın
- Hassas verileri içeren raporları güvenli şekilde saklayın

## 🤝 Katkıda Bulunma
1. Bu depoyu fork edin
2. Yeni bir branch oluşturun (`git checkout -b feature/yeniOzellik`)
3. Değişikliklerinizi commit edin (`git commit -am 'Yeni özellik: XYZ'`)
4. Branch'inizi push edin (`git push origin feature/yeniOzellik`)
5. Pull Request oluşturun

## 📄 Lisans
Bu proje MIT lisansı altında lisanslanmıştır. Detaylar için [LICENSE](LICENSE) dosyasına bakın.

## ✨ Gelecek Özellikler
- [ ] Daha fazla payload desteği
- [ ] Otomatik payload üreteci
- [ ] API entegrasyonları
- [ ] Daha fazla test ortamı
- [ ] Gelişmiş raporlama özellikleri
- [ ] Yeni güvenlik modülleri
- [ ] Entegre edilmiş güvenlik araçları
- [ ] Otomatik güvenlik düzeltmeleri
- [ ] Cloud güvenlik kontrolleri
- [ ] Container güvenlik taraması

## 📞 İletişim
Sorularınız ve önerileriniz için Issues bölümünü kullanabilirsiniz. 