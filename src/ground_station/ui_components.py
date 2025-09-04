"""
UI Bileşenleri
Yer istasyonu arayüzü için özel widget'lar ve bileşenler.
"""

from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                            QComboBox, QPushButton, QLineEdit, QGroupBox, 
                            QGridLayout, QSpinBox, QTextEdit, QFrame)
from PyQt5.QtCore import Qt, QTime
from PyQt5.QtGui import QFont


class ModernLabel(QLabel):
    """Modern görünümlü etiket widget'ı"""
    
    def __init__(self, text: str, icon: str = ""):
        super().__init__(f"{icon} {text}" if icon else text)
        self.setAlignment(Qt.AlignCenter)
        self.setStyleSheet("""
            QLabel {
                background-color: #2C3E50;
                color: white;
                border-radius: 10px;
                padding: 15px;
                margin: 5px;
                font-size: 14px;
                font-weight: bold;
            }
        """)


class SerialConnectionWidget(QGroupBox):
    """Seri port bağlantı widget'ı"""
    
    def __init__(self, title: str, connection_type: str):
        super().__init__(title)
        self.connection_type = connection_type
        self.setup_ui()
        
    def setup_ui(self):
        layout = QVBoxLayout(self)
        
        # Port seçimi
        port_layout = QHBoxLayout()
        port_layout.addWidget(QLabel("Port:"))
        self.port_combo = QComboBox()
        self.port_combo.setPlaceholderText("Port Seçin...")
        port_layout.addWidget(self.port_combo)
        layout.addLayout(port_layout)
        
        # Baud rate
        baud_layout = QHBoxLayout()
        baud_layout.addWidget(QLabel("Baud Rate:"))
        self.baud_edit = QLineEdit("9600")
        baud_layout.addWidget(self.baud_edit)
        layout.addLayout(baud_layout)
        
        # Butonlar
        button_layout = QHBoxLayout()
        self.connect_button = QPushButton("🔌 Bağlan")
        self.disconnect_button = QPushButton("🔌 Bağlantıyı Kes")
        self.disconnect_button.setEnabled(False)
        
        button_layout.addWidget(self.connect_button)
        button_layout.addWidget(self.disconnect_button)
        layout.addLayout(button_layout)
        
        # Durum etiketi
        self.status_label = QLabel("Bağlantı bekleniyor...")
        self.status_label.setStyleSheet("color: #666; font-style: italic;")
        layout.addWidget(self.status_label)
    
    def get_port(self) -> str:
        """Seçili portu döndürür"""
        return self.port_combo.currentText()
    
    def get_baud_rate(self) -> int:
        """Baud rate'i döndürür"""
        try:
            return int(self.baud_edit.text())
        except ValueError:
            return 9600
    
    def set_connected(self, connected: bool):
        """Bağlantı durumunu günceller"""
        self.connect_button.setEnabled(not connected)
        self.disconnect_button.setEnabled(connected)
        
        if connected:
            self.status_label.setText("✅ Bağlı")
            self.status_label.setStyleSheet("color: green; font-weight: bold;")
        else:
            self.status_label.setText("❌ Bağlantı kesildi")
            self.status_label.setStyleSheet("color: red; font-weight: bold;")


class TelemetryDisplayWidget(QGroupBox):
    """Telemetri verilerini gösteren widget"""
    
    def __init__(self, title: str, fields: list):
        super().__init__(title)
        self.fields = fields
        self.labels = {}
        self.setup_ui()
        
    def setup_ui(self):
        layout = QGridLayout(self)
        
        for row, (field_name, field_label) in enumerate(self.fields):
            # Etiket
            label = QLabel(f"{field_label}:")
            label.setStyleSheet("font-weight: bold;")
            layout.addWidget(label, row, 0)
            
            # Değer
            value_label = QLabel("0")
            value_label.setStyleSheet("font: bold 11px; color: #2C3E50;")
            layout.addWidget(value_label, row, 1)
            
            self.labels[field_name] = value_label
    
    def update_field(self, field_name: str, value: str):
        """Belirli bir alanı günceller"""
        if field_name in self.labels:
            self.labels[field_name].setText(value)
    
    def update_all_fields(self, data_dict: dict):
        """Tüm alanları günceller"""
        for field_name, value in data_dict.items():
            if field_name in self.labels:
                self.labels[field_name].setText(str(value))


class DebugConsole(QTextEdit):
    """Debug mesajları için konsol widget'ı"""
    
    def __init__(self):
        super().__init__()
        self.setReadOnly(True)
        self.setMaximumHeight(150)
        self.setPlaceholderText("Debug mesajları burada görünecek...")
        self.setStyleSheet("""
            QTextEdit {
                background-color: #2C3E50;
                border: none;
                border-radius: 10px;
                padding: 10px;
                color: #BDC3C7;
                font-family: 'Consolas', 'Monaco', monospace;
                font-size: 11px;
            }
        """)
    
    def log(self, message: str):
        """Debug mesajı ekler"""
        timestamp = QTime.currentTime().toString('hh:mm:ss')
        self.append(f"[{timestamp}] {message}")
        # Otomatik scroll
        self.verticalScrollBar().setValue(
            self.verticalScrollBar().maximum()
        )


class StatusIndicator(QLabel):
    """Durum göstergesi widget'ı"""
    
    def __init__(self, text: str = "Hazır"):
        super().__init__(text)
        self.setAlignment(Qt.AlignCenter)
        self.setStyleSheet("""
            QLabel {
                background-color: #27AE60;
                color: white;
                border-radius: 15px;
                padding: 8px 16px;
                font-weight: bold;
                font-size: 12px;
            }
        """)
    
    def set_status(self, status: str, color: str = "#27AE60"):
        """Durumu günceller"""
        self.setText(status)
        self.setStyleSheet(f"""
            QLabel {{
                background-color: {color};
                color: white;
                border-radius: 15px;
                padding: 8px 16px;
                font-weight: bold;
                font-size: 12px;
            }}
        """)


class ControlPanel(QGroupBox):
    """Kontrol paneli widget'ı"""
    
    def __init__(self, title: str):
        super().__init__(title)
        self.setup_ui()
        
    def setup_ui(self):
        layout = QVBoxLayout(self)
        
        # HYI Kontrol
        hyi_group = QGroupBox("HYI Kontrol")
        hyi_layout = QGridLayout(hyi_group)
        
        hyi_layout.addWidget(QLabel("Takım ID:"), 0, 0)
        self.team_id_spin = QSpinBox()
        self.team_id_spin.setRange(0, 255)
        hyi_layout.addWidget(self.team_id_spin, 0, 1)
        
        self.send_hyi_button = QPushButton("HYI Paketi Gönder")
        hyi_layout.addWidget(self.send_hyi_button, 1, 0, 1, 2)
        
        self.hyi_status_label = QLabel("HYI Durumu: Beklemede")
        self.hyi_status_label.setStyleSheet("font: italic 10px; color: #666;")
        hyi_layout.addWidget(self.hyi_status_label, 2, 0, 1, 2)
        
        layout.addWidget(hyi_group)
        
        # Harita Kontrolleri
        map_group = QGroupBox("Harita Kontrolleri")
        map_layout = QGridLayout(map_group)
        
        map_layout.addWidget(QLabel("Enlem:"), 0, 0)
        self.latitude_edit = QLineEdit("39.5419883728027")
        map_layout.addWidget(self.latitude_edit, 0, 1)
        
        map_layout.addWidget(QLabel("Boylam:"), 1, 0)
        self.longitude_edit = QLineEdit("28.0079479217529")
        map_layout.addWidget(self.longitude_edit, 1, 1)
        
        self.load_map_button = QPushButton("Haritayı Yükle")
        map_layout.addWidget(self.load_map_button, 2, 0, 1, 2)
        
        layout.addWidget(map_group)
        layout.addStretch()
    
    def get_team_id(self) -> int:
        """Takım ID'sini döndürür"""
        return self.team_id_spin.value()
    
    def get_coordinates(self) -> tuple:
        """Koordinatları döndürür"""
        try:
            lat = float(self.latitude_edit.text())
            lon = float(self.longitude_edit.text())
            return lat, lon
        except ValueError:
            return 0.0, 0.0
    
    def set_coordinates(self, latitude: float, longitude: float):
        """Koordinatları ayarlar"""
        self.latitude_edit.setText(f"{latitude:.6f}")
        self.longitude_edit.setText(f"{longitude:.6f}")
    
    def update_hyi_status(self, status: str):
        """HYI durumunu günceller"""
        self.hyi_status_label.setText(f"HYI Durumu: {status}")
