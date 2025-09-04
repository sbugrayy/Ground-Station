# 🚀 Yer İstasyonu v2.0 - Roket Telemetri Sistemi

Modern ve kullanıcı dostu bir roket telemetri sistemi. Bu uygulama, roket ve görev yükünden gelen verileri seri port üzerinden alır, işler ve gerçek zamanlı olarak görselleştirir.

## 📋 İçindekiler

- [Özellikler](#-özellikler)
- [Sistem Gereksinimleri](#-sistem-gereksinimleri)
- [Kurulum](#-kurulum)
- [Kullanım](#-kullanım)
- [Proje Yapısı](#-proje-yapısı)
- [Veri Formatları](#-veri-formatları)
- [Arduino Entegrasyonu](#-arduino-entegrasyonu)
- [Geliştirme](#-geliştirme)
- [Katkıda Bulunma](#-katkıda-bulunma)
- [Lisans](#-lisans)

## ✨ Özellikler

### 🎯 Ana Özellikler
- **Gerçek Zamanlı Veri İşleme**: Seri port üzerinden gelen verileri anlık olarak işler
- **3D Roket Görselleştirmesi**: OpenGL ile roketin 3D modelini ve rotasyonunu gösterir
- **Çoklu Seri Port Desteği**: Roket, görev yükü ve HYI için ayrı bağlantılar
- **Modern Arayüz**: PyQt5 ile geliştirilmiş kullanıcı dostu arayüz
- **HYI Protokolü Desteği**: Standart HYI paket formatında veri gönderimi

### 📊 Telemetri Verileri
- **Roket Verileri**: GPS koordinatları, yükseklik, hız, gyro, ivme sensörleri
- **Görev Yükü Verileri**: Sıcaklık, basınç, nem, GPS koordinatları
- **BMP280 Sensör Desteği**: Sıcaklık, basınç ve yükseklik ölçümleri

### 🎮 Kontrol Özellikleri
- **Harita Entegrasyonu**: GPS koordinatlarını harita üzerinde görüntüleme
- **HYI Paket Gönderimi**: Takım ID'si ile özelleştirilebilir paket gönderimi
- **Debug Konsolu**: Detaylı log kayıtları ve hata takibi

## 💻 Sistem Gereksinimleri

### Minimum Gereksinimler
- **İşletim Sistemi**: Windows 10/11, macOS 10.14+, Ubuntu 18.04+
- **Python**: 3.7 veya üzeri
- **RAM**: 4 GB
- **Disk Alanı**: 500 MB
- **Seri Port**: USB veya Bluetooth seri port bağlantısı

### Önerilen Gereksinimler
- **Python**: 3.9 veya üzeri
- **RAM**: 8 GB
- **GPU**: OpenGL 3.0+ desteği (3D görselleştirme için)

## 🚀 Kurulum

### 1. Projeyi İndirin
```bash
git clone https://github.com/your-username/Ground-Station.git
cd Ground-Station
```

### 2. Python Sanal Ortamı Oluşturun (Önerilen)
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. Gereksinimleri Yükleyin
```bash
pip install -r requirements.txt
```

### 4. Uygulamayı Başlatın
```bash
python main.py
```

## 📖 Kullanım

### İlk Kurulum
1. Uygulamayı başlattıktan sonra **Bağlantılar** sekmesine gidin
2. Mevcut seri portları görmek için **Yenile** butonuna tıklayın
3. Arduino'nuzun bağlı olduğu portu seçin
4. **Bağlan** butonuna tıklayarak bağlantıyı kurun

### Veri Görüntüleme
- **Telemetri** sekmesinde gerçek zamanlı verileri görüntüleyin
- **3D Görselleştirme** panelinde roketin rotasyonunu izleyin
- **Debug** sekmesinde sistem loglarını takip edin

### HYI Paket Gönderimi
1. **Kontroller** sekmesine gidin
2. Takım ID'nizi girin
3. **HYI Paketi Gönder** butonuna tıklayın

## 📁 Proje Yapısı

```
Ground-Station/
├── main.py                          # Ana uygulama dosyası
├── requirements.txt                 # Python gereksinimleri
├── README.md                        # Bu dosya
├── src/                            # Kaynak kod dizini
│   ├── ground_station/             # Ana uygulama modülleri
│   │   ├── __init__.py
│   │   ├── __main__.py
│   │   ├── main_window.py          # Ana pencere
│   │   ├── rocket_3d.py            # 3D görselleştirme
│   │   ├── serial_communication.py # Seri port iletişimi
│   │   ├── data_models.py          # Veri modelleri
│   │   └── ui_components.py        # UI bileşenleri
│   ├── arduino/                    # Arduino kodları
│   │   ├── BMP280_sensor.ino       # BMP280 sensör kodu
│   │   └── BMP280.ino              # Eski BMP280 kodu
│   └── data/                       # Veri dosyaları
│       ├── telemetry_schema.json   # Veri şeması
│       ├── sample_data.json        # Örnek veri
│       └── datav1.2.json           # Eski veri formatı
└── docs/                           # Dokümantasyon (gelecekte)
```

## 📊 Veri Formatları

### Roket Telemetri Verisi
```json
{
  "rocket": {
    "sayac": 1,
    "MSIrtifa": 0.0,
    "RoketGPSIrtifa": 0.0,
    "Enlem": 39.5419883728027,
    "Boylam": 28.0079479217529,
    "Hiz": 0.0,
    "Gx": 0.0,
    "Gy": 0.0,
    "Gz": 0.0,
    "Ax": 0.0,
    "Ay": 0.0,
    "Az": 9.81,
    "aci": 0.0,
    "durum": 0
  }
}
```

### BMP280 Sensör Verisi
```json
{
  "sicaklik": 25.6,
  "basinc": 1013.25,
  "yukseklik": 100.5
}
```

### CSV Format (Alternatif)
```
sayac,MSIrtifa,RoketGPSIrtifa,Enlem,Boylam,Hiz,Gx,Gy,Gz,Ax,Ay,Az,aci,durum
1,0.0,0.0,39.5419883728027,28.0079479217529,0.0,0.0,0.0,0.0,0.0,0.0,9.81,0.0,0
```

## 🔧 Arduino Entegrasyonu

### BMP280 Sensör Bağlantısı
```
Arduino Uno    BMP280
---------      ------
3.3V      ->   VCC
GND       ->   GND
A4 (SDA)  ->   SDA
A5 (SCL)  ->   SCL
```

### Gerekli Kütüphaneler
Arduino IDE'de aşağıdaki kütüphaneleri yükleyin:
- **Adafruit BMP280 Library**
- **Wire Library** (I2C için)

### Kod Yükleme
1. `src/arduino/BMP280_sensor.ino` dosyasını Arduino IDE'de açın
2. Gerekli kütüphaneleri yükleyin
3. Arduino'ya yükleyin
4. Seri monitörde 9600 baud rate ile veri akışını kontrol edin

## 🛠️ Geliştirme

### Geliştirme Ortamı Kurulumu
```bash
# Geliştirme gereksinimlerini yükleyin
pip install -r requirements.txt

# Kod formatlaması için
pip install black flake8

# Test için
pip install pytest
```

### Kod Formatlaması
```bash
# Black ile kod formatlaması
black src/

# Flake8 ile kod kontrolü
flake8 src/
```

### Test Çalıştırma
```bash
# Tüm testleri çalıştır
pytest

# Belirli bir test dosyasını çalıştır
pytest tests/test_serial_communication.py
```

### Yeni Özellik Ekleme
1. Yeni modülü `src/ground_station/` dizinine ekleyin
2. Gerekli import'ları `main_window.py`'ye ekleyin
3. Test dosyalarını `tests/` dizinine ekleyin
4. Dokümantasyonu güncelleyin

## 🤝 Katkıda Bulunma

1. Bu projeyi fork edin
2. Yeni bir feature branch oluşturun (`git checkout -b feature/amazing-feature`)
3. Değişikliklerinizi commit edin (`git commit -m 'Add amazing feature'`)
4. Branch'inizi push edin (`git push origin feature/amazing-feature`)
5. Pull Request oluşturun

### Katkı Kuralları
- Kod standartlarına uyun (PEP 8)
- Test yazın
- Dokümantasyonu güncelleyin
- Açıklayıcı commit mesajları yazın

## 📝 Lisans

Bu proje MIT lisansı altında lisanslanmıştır. Detaylar için [LICENSE](LICENSE) dosyasına bakın.

## 📞 İletişim

- **Proje Sahibi**: [Your Name]
- **Email**: your.email@example.com
- **GitHub**: [@your-username](https://github.com/your-username)

## 🙏 Teşekkürler

- [Adafruit](https://www.adafruit.com/) - BMP280 kütüphanesi için
- [PyQt5](https://www.riverbankcomputing.com/software/pyqt/) - GUI framework için
- [OpenGL](https://www.opengl.org/) - 3D görselleştirme için

## 📈 Gelecek Planları

- [ ] Web tabanlı arayüz
- [ ] Veri kaydetme ve analiz
- [ ] Çoklu roket desteği
- [ ] Otomatik paraşüt açma sistemi
- [ ] Mobil uygulama
- [ ] Bulut entegrasyonu

---

**Not**: Bu proje eğitim amaçlı geliştirilmiştir. Gerçek roket fırlatmalarında kullanmadan önce güvenlik testlerini yapın.

⭐ Bu projeyi beğendiyseniz yıldız vermeyi unutmayın!