/*
 * BMP280 Sensör Kodu
 * Sıcaklık, basınç ve yükseklik verilerini seri port üzerinden gönderir.
 * 
 * Gerekli Kütüphaneler:
 * - Adafruit BMP280 Library
 * - Wire Library (I2C için)
 * 
 * Bağlantılar:
 * - VCC -> 3.3V veya 5V
 * - GND -> GND
 * - SCL -> A5 (Arduino Uno) veya SCL pin
 * - SDA -> A4 (Arduino Uno) veya SDA pin
 */

#include <Wire.h>
#include <Adafruit_BMP280.h>

// BMP280 sensör nesnesi
Adafruit_BMP280 bmp;

// Sensör ayarları
const float SEA_LEVEL_PRESSURE = 1013.25; // Deniz seviyesi basıncı (hPa)
const unsigned long SENSOR_READ_INTERVAL = 1000; // Okuma aralığı (ms)

// Son okuma zamanı
unsigned long lastReadTime = 0;

void setup() {
  // Seri port başlatma
  Serial.begin(9600);
  
  // Başlangıç mesajı
  Serial.println("BMP280 Sensör Başlatılıyor...");
  
  // BMP280 sensörünü başlat
  if (!bmp.begin(0x76)) {  // I2C adresi (0x76 veya 0x77)
    Serial.println("HATA: BMP280 sensörü bulunamadı!");
    Serial.println("Bağlantıları kontrol edin:");
    Serial.println("- VCC -> 3.3V veya 5V");
    Serial.println("- GND -> GND");
    Serial.println("- SCL -> A5 (Uno) veya SCL pin");
    Serial.println("- SDA -> A4 (Uno) veya SDA pin");
    while (1) delay(10); // Sonsuz döngü
  }
  
  // Sensör ayarları
  bmp.setSampling(
    Adafruit_BMP280::MODE_NORMAL,     // Çalışma modu
    Adafruit_BMP280::SAMPLING_X2,     // Sıcaklık örnekleme
    Adafruit_BMP280::SAMPLING_X16,    // Basınç örnekleme
    Adafruit_BMP280::FILTER_X16,      // Filtreleme
    Adafruit_BMP280::STANDBY_MS_500   // Bekleme süresi
  );
  
  Serial.println("BMP280 sensörü başarıyla başlatıldı!");
  Serial.println("Veri formatı: JSON");
  Serial.println("Baud Rate: 9600");
  Serial.println("---");
}

void loop() {
  // Zaman kontrolü
  unsigned long currentTime = millis();
  if (currentTime - lastReadTime >= SENSOR_READ_INTERVAL) {
    readAndSendSensorData();
    lastReadTime = currentTime;
  }
  
  // Kısa bekleme
  delay(10);
}

void readAndSendSensorData() {
  // Sensör verilerini oku
  float temperature = bmp.readTemperature();
  float pressure = bmp.readPressure() / 100.0F; // Pa'dan hPa'ya çevir
  float altitude = bmp.readAltitude(SEA_LEVEL_PRESSURE);
  
  // Veri geçerliliğini kontrol et
  if (isnan(temperature) || isnan(pressure) || isnan(altitude)) {
    Serial.println("HATA: Geçersiz sensör verisi!");
    return;
  }
  
  // JSON formatında veri gönder
  sendJSONData(temperature, pressure, altitude);
}

void sendJSONData(float temp, float press, float alt) {
  Serial.print("{");
  Serial.print("\"sicaklik\":");
  Serial.print(temp, 2);
  Serial.print(",\"basinc\":");
  Serial.print(press, 2);
  Serial.print(",\"yukseklik\":");
  Serial.print(alt, 2);
  Serial.println("}");
}

// Debug fonksiyonu (isteğe bağlı)
void printSensorInfo() {
  Serial.println("=== BMP280 Sensör Bilgileri ===");
  Serial.print("Sıcaklık: ");
  Serial.print(bmp.readTemperature());
  Serial.println(" °C");
  
  Serial.print("Basınç: ");
  Serial.print(bmp.readPressure() / 100.0F);
  Serial.println(" hPa");
  
  Serial.print("Yükseklik: ");
  Serial.print(bmp.readAltitude(SEA_LEVEL_PRESSURE));
  Serial.println(" m");
  Serial.println("================================");
}
