#include <Wire.h>
#include <Adafruit_BMP280.h>

Adafruit_BMP280 bmp; // I2C arayüzü için

void setup() {
  Serial.begin(9600);
  
  // BMP280 sensörünün başlatılması
  if (!bmp.begin(0x76)) {  // I2C adresi genellikle 0x76 veya 0x77'dir
    Serial.println("BMP280 sensörü bulunamadı!");
    while (1);
  }
  
  // Sensör ayarları (opsiyonel)
  bmp.setSampling(Adafruit_BMP280::MODE_NORMAL,     // Çalışma modu
                  Adafruit_BMP280::SAMPLING_X2,      // Sıcaklık örnekleme
                  Adafruit_BMP280::SAMPLING_X16,     // Basınç örnekleme
                  Adafruit_BMP280::FILTER_X16,       // Filtreleme
                  Adafruit_BMP280::STANDBY_MS_500);  // Bekleme süresi
}

void loop() {
  // Sensör verilerini oku
  float sicaklik = bmp.readTemperature();
  float basinc = bmp.readPressure() / 100.0F; // Pa'dan hPa'ya çevirme
  float yukseklik = bmp.readAltitude(1013.25); // Deniz seviyesi basıncı referans alınır
  
  // JSON formatında veri gönderme
  Serial.print("{");
  Serial.print("\"sicaklik\":");
  Serial.print(sicaklik);
  Serial.print(",\"basinc\":");
  Serial.print(basinc);
  Serial.print(",\"yukseklik\":");
  Serial.print(yukseklik);
  Serial.println("}");
  
  delay(1000); // 1 saniye bekle
} 