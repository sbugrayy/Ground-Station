"""
Veri Modelleri
Roket ve görev yükü verilerini temsil eden sınıflar.
"""

from dataclasses import dataclass
from typing import Dict, Any
import json


@dataclass
class RocketData:
    """Roket telemetri verileri"""
    sayac: int = 0
    MSIrtifa: float = 0.0
    RoketGPSIrtifa: float = 0.0
    Enlem: float = 0.0
    Boylam: float = 0.0
    Hiz: float = 0.0
    Gx: float = 0.0
    Gy: float = 0.0
    Gz: float = 0.0
    Ax: float = 0.0
    Ay: float = 0.0
    Az: float = 0.0
    aci: float = 0.0
    durum: int = 0
    
    def to_dict(self) -> Dict[str, Any]:
        """Sözlük formatına dönüştürür"""
        return {
            'sayac': self.sayac,
            'MSIrtifa': self.MSIrtifa,
            'RoketGPSIrtifa': self.RoketGPSIrtifa,
            'Enlem': self.Enlem,
            'Boylam': self.Boylam,
            'Hiz': self.Hiz,
            'Gx': self.Gx,
            'Gy': self.Gy,
            'Gz': self.Gz,
            'Ax': self.Ax,
            'Ay': self.Ay,
            'Az': self.Az,
            'aci': self.aci,
            'durum': self.durum
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'RocketData':
        """Sözlükten nesne oluşturur"""
        return cls(**data)
    
    @classmethod
    def from_csv_line(cls, line: str) -> 'RocketData':
        """CSV satırından nesne oluşturur"""
        values = line.strip().split(',')
        if len(values) >= 14:
            return cls(
                sayac=int(values[0]),
                MSIrtifa=float(values[1]),
                RoketGPSIrtifa=float(values[2]),
                Enlem=float(values[3]),
                Boylam=float(values[4]),
                Hiz=float(values[5]),
                Gx=float(values[6]),
                Gy=float(values[7]),
                Gz=float(values[8]),
                Ax=float(values[9]),
                Ay=float(values[10]),
                Az=float(values[11]),
                aci=float(values[12]),
                durum=int(values[13])
            )
        return cls()


@dataclass
class PayloadData:
    """Görev yükü telemetri verileri"""
    GorevYukuIrtifa: float = 0.0
    GorevYukuEnlem: float = 0.0
    GorevYukuBoylam: float = 0.0
    GorevYukuBasinc: float = 0.0
    GorevYukuSicaklik: float = 0.0
    GorevYukuNem: float = 0.0
    
    def to_dict(self) -> Dict[str, Any]:
        """Sözlük formatına dönüştürür"""
        return {
            'GorevYukuIrtifa': self.GorevYukuIrtifa,
            'GorevYukuEnlem': self.GorevYukuEnlem,
            'GorevYukuBoylam': self.GorevYukuBoylam,
            'GorevYukuBasinc': self.GorevYukuBasinc,
            'GorevYukuSicaklik': self.GorevYukuSicaklik,
            'GorevYukuNem': self.GorevYukuNem
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'PayloadData':
        """Sözlükten nesne oluşturur"""
        return cls(**data)
    
    @classmethod
    def from_csv_line(cls, line: str) -> 'PayloadData':
        """CSV satırından nesne oluşturur"""
        values = line.strip().split(',')
        if len(values) >= 6:
            return cls(
                GorevYukuIrtifa=float(values[0]),
                GorevYukuEnlem=float(values[1]),
                GorevYukuBoylam=float(values[2]),
                GorevYukuBasinc=float(values[3]),
                GorevYukuSicaklik=float(values[4]),
                GorevYukuNem=float(values[5])
            )
        return cls()


@dataclass
class BMP280Data:
    """BMP280 sensör verileri"""
    sicaklik: float = 0.0
    basinc: float = 0.0
    yukseklik: float = 0.0
    
    def to_dict(self) -> Dict[str, Any]:
        """Sözlük formatına dönüştürür"""
        return {
            'sicaklik': self.sicaklik,
            'basinc': self.basinc,
            'yukseklik': self.yukseklik
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'BMP280Data':
        """Sözlükten nesne oluşturur"""
        return cls(**data)
    
    @classmethod
    def from_json(cls, json_str: str) -> 'BMP280Data':
        """JSON string'den nesne oluşturur"""
        try:
            data = json.loads(json_str)
            return cls.from_dict(data)
        except json.JSONDecodeError:
            return cls()


class TelemetryData:
    """Tüm telemetri verilerini yöneten ana sınıf"""
    
    def __init__(self):
        self.rocket = RocketData()
        self.payload = PayloadData()
        self.bmp280 = BMP280Data()
    
    def to_dict(self) -> Dict[str, Any]:
        """Tüm verileri sözlük formatına dönüştürür"""
        return {
            'rocket': self.rocket.to_dict(),
            'payload': self.payload.to_dict(),
            'bmp280': self.bmp280.to_dict()
        }
    
    def to_json(self) -> str:
        """Tüm verileri JSON formatına dönüştürür"""
        return json.dumps(self.to_dict(), indent=2)
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'TelemetryData':
        """Sözlükten nesne oluşturur"""
        instance = cls()
        if 'rocket' in data:
            instance.rocket = RocketData.from_dict(data['rocket'])
        if 'payload' in data:
            instance.payload = PayloadData.from_dict(data['payload'])
        if 'bmp280' in data:
            instance.bmp280 = BMP280Data.from_dict(data['bmp280'])
        return instance
    
    @classmethod
    def from_json(cls, json_str: str) -> 'TelemetryData':
        """JSON string'den nesne oluşturur"""
        try:
            data = json.loads(json_str)
            return cls.from_dict(data)
        except json.JSONDecodeError:
            return cls()
