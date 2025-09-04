"""
Seri Port İletişim Modülü
Roket ve görev yükü ile seri port üzerinden iletişim kurar.
"""

import serial
import struct
from serial.tools import list_ports
from typing import Optional, List, Dict, Any


class SerialManager:
    """Seri port yöneticisi"""
    
    def __init__(self):
        self.connections: Dict[str, Optional[serial.Serial]] = {
            'rocket': None,
            'payload': None,
            'hyi': None
        }
        
    def get_available_ports(self) -> List[str]:
        """Mevcut seri portları listeler"""
        ports = list_ports.comports()
        return [port.device for port in ports]
    
    def connect(self, port_name: str, baud_rate: int, connection_type: str) -> bool:
        """
        Seri porta bağlanır
        
        Args:
            port_name: Port adı (örn: 'COM3', '/dev/ttyUSB0')
            baud_rate: Baud hızı
            connection_type: Bağlantı türü ('rocket', 'payload', 'hyi')
            
        Returns:
            bool: Bağlantı başarılı ise True
        """
        try:
            if connection_type in self.connections:
                # Mevcut bağlantıyı kapat
                self.disconnect(connection_type)
                
                # Yeni bağlantı aç
                self.connections[connection_type] = serial.Serial(
                    port_name, 
                    baud_rate, 
                    timeout=1
                )
                return True
        except Exception as e:
            print(f"Seri port bağlantı hatası ({connection_type}): {e}")
            return False
    
    def disconnect(self, connection_type: str) -> bool:
        """
        Seri port bağlantısını kapatır
        
        Args:
            connection_type: Bağlantı türü
            
        Returns:
            bool: Bağlantı kapatıldı ise True
        """
        try:
            if (connection_type in self.connections and 
                self.connections[connection_type] and 
                self.connections[connection_type].is_open):
                
                self.connections[connection_type].close()
                self.connections[connection_type] = None
                return True
        except Exception as e:
            print(f"Seri port kapatma hatası ({connection_type}): {e}")
        return False
    
    def is_connected(self, connection_type: str) -> bool:
        """Bağlantı durumunu kontrol eder"""
        return (connection_type in self.connections and 
                self.connections[connection_type] and 
                self.connections[connection_type].is_open)
    
    def read_data(self, connection_type: str) -> Optional[str]:
        """
        Seri porttan veri okur
        
        Args:
            connection_type: Bağlantı türü
            
        Returns:
            str: Okunan veri, hata durumunda None
        """
        try:
            if self.is_connected(connection_type):
                connection = self.connections[connection_type]
                if connection.in_waiting:
                    return connection.readline().decode('utf-8').strip()
        except Exception as e:
            print(f"Veri okuma hatası ({connection_type}): {e}")
        return None
    
    def write_data(self, connection_type: str, data: bytes) -> bool:
        """
        Seri porta veri yazar
        
        Args:
            connection_type: Bağlantı türü
            data: Yazılacak veri
            
        Returns:
            bool: Yazma başarılı ise True
        """
        try:
            if self.is_connected(connection_type):
                self.connections[connection_type].write(data)
                return True
        except Exception as e:
            print(f"Veri yazma hatası ({connection_type}): {e}")
        return False
    
    def close_all(self):
        """Tüm bağlantıları kapatır"""
        for connection_type in self.connections:
            self.disconnect(connection_type)


class HYIProtocol:
    """HYI protokolü için paket oluşturma ve gönderme"""
    
    @staticmethod
    def create_packet(team_id: int, counter: int, rocket_data: Dict[str, Any], 
                     payload_data: Dict[str, Any]) -> bytearray:
        """
        HYI paketi oluşturur
        
        Args:
            team_id: Takım ID'si
            counter: Sayaç
            rocket_data: Roket verileri
            payload_data: Görev yükü verileri
            
        Returns:
            bytearray: HYI paketi
        """
        packet = bytearray(78)
        
        # Başlık
        packet[0] = 0xFF
        packet[1] = 0xFF
        packet[2] = 0x54
        packet[3] = 0x52
        
        # Takım ID ve sayaç
        packet[4] = team_id
        packet[5] = counter
        
        # Roket verileri
        packet[6:10] = struct.pack('<f', rocket_data.get('MSIrtifa', 0.0))
        packet[10:14] = struct.pack('<f', rocket_data.get('RoketGPSIrtifa', 0.0))
        packet[14:18] = struct.pack('<f', rocket_data.get('Enlem', 0.0))
        packet[18:22] = struct.pack('<f', rocket_data.get('Boylam', 0.0))
        
        # Görev yükü verileri
        packet[22:26] = struct.pack('<f', payload_data.get('GorevYukuIrtifa', 0.0))
        packet[26:30] = struct.pack('<f', payload_data.get('GorevYukuEnlem', 0.0))
        packet[30:34] = struct.pack('<f', payload_data.get('GorevYukuBoylam', 0.0))
        
        # Gyro verileri
        packet[46:50] = struct.pack('<f', rocket_data.get('Gx', 0.0))
        packet[50:54] = struct.pack('<f', rocket_data.get('Gy', 0.0))
        packet[54:58] = struct.pack('<f', rocket_data.get('Gz', 0.0))
        
        # İvme verileri
        packet[58:62] = struct.pack('<f', rocket_data.get('Ax', 0.0))
        packet[62:66] = struct.pack('<f', rocket_data.get('Ay', 0.0))
        packet[66:70] = struct.pack('<f', rocket_data.get('Az', 0.0))
        
        # Açı ve durum
        packet[70:74] = struct.pack('<f', rocket_data.get('aci', 0.0))
        packet[74] = rocket_data.get('durum', 0)
        
        # Kontrol toplamı
        checksum = sum(packet[4:75]) % 256
        packet[75] = checksum
        
        # Footer
        packet[76] = 0x0D
        packet[77] = 0x0A
        
        return packet
