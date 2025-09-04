"""
Ana Pencere
Yer istasyonu uygulamasının ana arayüzü.
"""

import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                            QHBoxLayout, QTabWidget, QFrame, QStyleFactory, QLabel)
from PyQt5.QtCore import QTimer, Qt
from PyQt5.QtGui import QFont

from .rocket_3d import RocketGLWidget
from .serial_communication import SerialManager, HYIProtocol
from .data_models import TelemetryData, RocketData, PayloadData
from .ui_components import (SerialConnectionWidget, TelemetryDisplayWidget, 
                          DebugConsole, StatusIndicator, ControlPanel)


class GroundStationMainWindow(QMainWindow):
    """Ana yer istasyonu penceresi"""
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Yer İstasyonu v2.0 - Roket Telemetri Sistemi")
        self.setGeometry(100, 100, 1400, 900)
        
        # Veri yöneticileri
        self.serial_manager = SerialManager()
        self.telemetry_data = TelemetryData()
        
        # Timer'lar
        self.data_timer = QTimer()
        self.data_timer.timeout.connect(self.update_data)
        
        # UI'yi başlat
        self.setup_ui()
        self.setup_connections()
        self.setup_styles()
        
        # İlk port taraması
        self.refresh_ports()
        
    def setup_ui(self):
        """Kullanıcı arayüzünü oluşturur"""
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        main_layout = QHBoxLayout(central_widget)
        main_layout.setContentsMargins(10, 10, 10, 10)
        main_layout.setSpacing(15)
        
        # Sol panel - 3D görselleştirme
        left_panel = self.create_3d_panel()
        main_layout.addLayout(left_panel, 60)
        
        # Sağ panel - Kontrol ve veri
        right_panel = self.create_control_panel()
        main_layout.addWidget(right_panel, 40)
        
    def create_3d_panel(self) -> QVBoxLayout:
        """3D görselleştirme panelini oluşturur"""
        layout = QVBoxLayout()
        layout.setSpacing(15)
        
        # 3D görselleştirme
        view_frame = QFrame()
        view_frame.setFrameShape(QFrame.StyledPanel)
        view_frame.setLineWidth(1)
        view_layout = QVBoxLayout(view_frame)
        view_layout.setContentsMargins(5, 5, 5, 5)
        
        self.rocket_3d = RocketGLWidget()
        view_layout.addWidget(self.rocket_3d)
        
        layout.addWidget(view_frame)
        
        # Roket durumu
        status_group = QFrame()
        status_group.setStyleSheet("""
            QFrame {
                background-color: #2C3E50;
                border-radius: 10px;
                padding: 10px;
            }
        """)
        status_layout = QVBoxLayout(status_group)
        
        # Başlık
        title_label = QLabel("🚀 Roket Durumu")
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet("""
            QLabel {
                color: white;
                font-size: 16px;
                font-weight: bold;
                margin-bottom: 10px;
            }
        """)
        status_layout.addWidget(title_label)
        
        # Rotasyon bilgileri
        rotation_layout = QHBoxLayout()
        self.x_rot_label = QLabel("X: 0°")
        self.y_rot_label = QLabel("Y: 0°")
        self.z_rot_label = QLabel("Z: 0°")
        
        for label in [self.x_rot_label, self.y_rot_label, self.z_rot_label]:
            label.setStyleSheet("color: white; font-weight: bold;")
            rotation_layout.addWidget(label)
        
        status_layout.addLayout(rotation_layout)
        
        # Durum göstergesi
        self.status_indicator = StatusIndicator("Hazır")
        status_layout.addWidget(self.status_indicator)
        
        layout.addWidget(status_group)
        
        return layout
        
    def create_control_panel(self) -> QTabWidget:
        """Kontrol panelini oluşturur"""
        tab_widget = QTabWidget()
        tab_widget.setTabPosition(QTabWidget.West)
        
        # Bağlantılar sekmesi
        connections_tab = self.create_connections_tab()
        tab_widget.addTab(connections_tab, "🔌 Bağlantılar")
        
        # Telemetri sekmesi
        telemetry_tab = self.create_telemetry_tab()
        tab_widget.addTab(telemetry_tab, "📊 Telemetri")
        
        # Kontroller sekmesi
        controls_tab = self.create_controls_tab()
        tab_widget.addTab(controls_tab, "🎮 Kontroller")
        
        # Debug sekmesi
        debug_tab = self.create_debug_tab()
        tab_widget.addTab(debug_tab, "🐛 Debug")
        
        return tab_widget
        
    def create_connections_tab(self) -> QWidget:
        """Bağlantılar sekmesini oluşturur"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setContentsMargins(5, 5, 5, 5)
        
        # Seri port bağlantıları
        self.rocket_connection = SerialConnectionWidget("🚀 Roket Telemetri", "rocket")
        self.payload_connection = SerialConnectionWidget("📦 Görev Yükü Telemetri", "payload")
        self.hyi_connection = SerialConnectionWidget("📡 HYI Telemetri", "hyi")
        
        layout.addWidget(self.rocket_connection)
        layout.addWidget(self.payload_connection)
        layout.addWidget(self.hyi_connection)
        layout.addStretch()
        
        return widget
        
    def create_telemetry_tab(self) -> QWidget:
        """Telemetri sekmesini oluşturur"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        # Roket telemetrisi
        rocket_fields = [
            ("sayac", "Sayaç"),
            ("MSIrtifa", "MS İrtifa (m)"),
            ("RoketGPSIrtifa", "GPS İrtifa (m)"),
            ("Enlem", "Enlem"),
            ("Boylam", "Boylam"),
            ("Hiz", "Hız (m/s)"),
            ("Gx", "Gyro X"),
            ("Gy", "Gyro Y"),
            ("Gz", "Gyro Z"),
            ("Ax", "Aks X"),
            ("Ay", "Aks Y"),
            ("Az", "Aks Z"),
            ("aci", "Açı"),
            ("durum", "Durum")
        ]
        
        self.rocket_telemetry = TelemetryDisplayWidget("🚀 Roket Telemetrisi", rocket_fields)
        layout.addWidget(self.rocket_telemetry)
        
        # Görev yükü telemetrisi
        payload_fields = [
            ("GorevYukuIrtifa", "İrtifa (m)"),
            ("GorevYukuEnlem", "Enlem"),
            ("GorevYukuBoylam", "Boylam"),
            ("GorevYukuBasinc", "Basınç (hPa)"),
            ("GorevYukuSicaklik", "Sıcaklık (°C)"),
            ("GorevYukuNem", "Nem (%)")
        ]
        
        self.payload_telemetry = TelemetryDisplayWidget("📦 Görev Yükü Telemetrisi", payload_fields)
        layout.addWidget(self.payload_telemetry)
        
        layout.addStretch()
        return widget
        
    def create_controls_tab(self) -> QWidget:
        """Kontroller sekmesini oluşturur"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        self.control_panel = ControlPanel("🎮 Kontrol Paneli")
        layout.addWidget(self.control_panel)
        
        return widget
        
    def create_debug_tab(self) -> QWidget:
        """Debug sekmesini oluşturur"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        self.debug_console = DebugConsole()
        layout.addWidget(self.debug_console)
        
        return widget
        
    def setup_connections(self):
        """Sinyal bağlantılarını kurar"""
        # Seri port bağlantıları
        self.rocket_connection.connect_button.clicked.connect(
            lambda: self.connect_serial("rocket")
        )
        self.rocket_connection.disconnect_button.clicked.connect(
            lambda: self.disconnect_serial("rocket")
        )
        
        self.payload_connection.connect_button.clicked.connect(
            lambda: self.connect_serial("payload")
        )
        self.payload_connection.disconnect_button.clicked.connect(
            lambda: self.disconnect_serial("payload")
        )
        
        self.hyi_connection.connect_button.clicked.connect(
            lambda: self.connect_serial("hyi")
        )
        self.hyi_connection.disconnect_button.clicked.connect(
            lambda: self.disconnect_serial("hyi")
        )
        
        # Kontrol paneli
        self.control_panel.send_hyi_button.clicked.connect(self.send_hyi_packet)
        self.control_panel.load_map_button.clicked.connect(self.load_map)
        
    def setup_styles(self):
        """Uygulama stillerini ayarlar"""
        self.setStyleSheet("""
            QMainWindow {
                background-color: #34495E;
            }
            QWidget {
                background-color: #34495E;
                color: white;
            }
            QPushButton {
                background-color: #3498DB;
                border: none;
                color: white;
                padding: 8px 16px;
                border-radius: 5px;
                font-size: 14px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #2980B9;
            }
            QPushButton:pressed {
                background-color: #2574A9;
            }
            QPushButton:disabled {
                background-color: #7F8C8D;
            }
            QComboBox {
                background-color: #2C3E50;
                border: 2px solid #3498DB;
                border-radius: 5px;
                padding: 8px;
                color: white;
                min-width: 150px;
                font-size: 14px;
            }
            QComboBox:hover {
                border-color: #2980B9;
                background-color: #34495E;
            }
            QLineEdit {
                background-color: #2C3E50;
                border: 2px solid #3498DB;
                border-radius: 5px;
                padding: 8px;
                color: white;
                font-size: 14px;
            }
            QLineEdit:focus {
                border-color: #2980B9;
            }
            QGroupBox {
                font: bold 12px;
                border: 2px solid #3498DB;
                border-radius: 10px;
                margin-top: 10px;
                padding-top: 10px;
                background-color: #2C3E50;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px;
                color: #3498DB;
            }
            QTabWidget::pane {
                border: 1px solid #3498DB;
                background-color: #2C3E50;
            }
            QTabBar::tab {
                background-color: #34495E;
                color: white;
                padding: 8px 16px;
                margin-right: 2px;
                border-top-left-radius: 5px;
                border-top-right-radius: 5px;
            }
            QTabBar::tab:selected {
                background-color: #3498DB;
            }
            QTabBar::tab:hover {
                background-color: #2980B9;
            }
        """)
        
    def refresh_ports(self):
        """Mevcut seri portları tarar"""
        ports = self.serial_manager.get_available_ports()
        
        for connection_widget in [self.rocket_connection, self.payload_connection, self.hyi_connection]:
            connection_widget.port_combo.clear()
            for port in ports:
                connection_widget.port_combo.addItem(port)
        
        self.debug_console.log(f"Port taraması tamamlandı: {len(ports)} port bulundu")
        
    def connect_serial(self, connection_type: str):
        """Seri porta bağlanır"""
        if connection_type == "rocket":
            widget = self.rocket_connection
        elif connection_type == "payload":
            widget = self.payload_connection
        elif connection_type == "hyi":
            widget = self.hyi_connection
        else:
            return
            
        port = widget.get_port()
        baud_rate = widget.get_baud_rate()
        
        if self.serial_manager.connect(port, baud_rate, connection_type):
            widget.set_connected(True)
            self.debug_console.log(f"{connection_type} bağlantısı başarılı: {port}")
            
            # Veri okumayı başlat
            if not self.data_timer.isActive():
                self.data_timer.start(100)  # 100ms'de bir güncelle
        else:
            self.debug_console.log(f"{connection_type} bağlantı hatası: {port}")
            
    def disconnect_serial(self, connection_type: str):
        """Seri port bağlantısını keser"""
        if self.serial_manager.disconnect(connection_type):
            if connection_type == "rocket":
                self.rocket_connection.set_connected(False)
            elif connection_type == "payload":
                self.payload_connection.set_connected(False)
            elif connection_type == "hyi":
                self.hyi_connection.set_connected(False)
                
            self.debug_console.log(f"{connection_type} bağlantısı kesildi")
            
            # Tüm bağlantılar kesildiyse timer'ı durdur
            if not any(self.serial_manager.is_connected(conn_type) 
                      for conn_type in ["rocket", "payload", "hyi"]):
                self.data_timer.stop()
                
    def update_data(self):
        """Veri güncellemelerini yapar"""
        # Roket verilerini oku
        if self.serial_manager.is_connected("rocket"):
            rocket_data = self.serial_manager.read_data("rocket")
            if rocket_data:
                self.process_rocket_data(rocket_data)
                
        # Görev yükü verilerini oku
        if self.serial_manager.is_connected("payload"):
            payload_data = self.serial_manager.read_data("payload")
            if payload_data:
                self.process_payload_data(payload_data)
                
    def process_rocket_data(self, data: str):
        """Roket verilerini işler"""
        try:
            # CSV formatında veri geliyorsa
            if ',' in data:
                self.telemetry_data.rocket = RocketData.from_csv_line(data)
            else:
                # JSON formatında veri geliyorsa
                import json
                json_data = json.loads(data)
                if 'rocket' in json_data:
                    self.telemetry_data.rocket = RocketData.from_dict(json_data['rocket'])
                    
            # UI'yi güncelle
            self.update_rocket_display()
            self.update_3d_visualization()
            self.update_status()
            
        except Exception as e:
            self.debug_console.log(f"Roket veri işleme hatası: {e}")
            
    def process_payload_data(self, data: str):
        """Görev yükü verilerini işler"""
        try:
            # CSV formatında veri geliyorsa
            if ',' in data:
                self.telemetry_data.payload = PayloadData.from_csv_line(data)
            else:
                # JSON formatında veri geliyorsa
                import json
                json_data = json.loads(data)
                if 'payload' in json_data:
                    self.telemetry_data.payload = PayloadData.from_dict(json_data['payload'])
                    
            # UI'yi güncelle
            self.update_payload_display()
            
        except Exception as e:
            self.debug_console.log(f"Görev yükü veri işleme hatası: {e}")
            
    def update_rocket_display(self):
        """Roket telemetri ekranını günceller"""
        rocket_data = self.telemetry_data.rocket.to_dict()
        self.rocket_telemetry.update_all_fields(rocket_data)
        
    def update_payload_display(self):
        """Görev yükü telemetri ekranını günceller"""
        payload_data = self.telemetry_data.payload.to_dict()
        self.payload_telemetry.update_all_fields(payload_data)
        
    def update_3d_visualization(self):
        """3D görselleştirmeyi günceller"""
        rocket = self.telemetry_data.rocket
        self.rocket_3d.update_rotation(rocket.Gx, rocket.Gy, rocket.Gz)
        
        # Rotasyon etiketlerini güncelle
        self.x_rot_label.setText(f"X: {rocket.Gx:.1f}°")
        self.y_rot_label.setText(f"Y: {rocket.Gy:.1f}°")
        self.z_rot_label.setText(f"Z: {rocket.Gz:.1f}°")
        
    def update_status(self):
        """Durum göstergesini günceller"""
        rocket = self.telemetry_data.rocket
        status_map = {
            0: ("Hazır", "#27AE60"),
            1: ("Fırlatma Bekliyor", "#F39C12"),
            2: ("Yükseliyor", "#3498DB"),
            3: ("Alçalıyor", "#9B59B6"),
            4: ("Paraşüt Açık", "#E74C3C"),
            5: ("Yere İndi", "#2ECC71")
        }
        
        status_text, status_color = status_map.get(rocket.durum, ("Bilinmeyen", "#95A5A6"))
        self.status_indicator.set_status(status_text, status_color)
        
    def send_hyi_packet(self):
        """HYI paketi gönderir"""
        if self.serial_manager.is_connected("hyi"):
            team_id = self.control_panel.get_team_id()
            packet = HYIProtocol.create_packet(
                team_id,
                self.telemetry_data.rocket.sayac,
                self.telemetry_data.rocket.to_dict(),
                self.telemetry_data.payload.to_dict()
            )
            
            if self.serial_manager.write_data("hyi", packet):
                self.debug_console.log(f"HYI paketi gönderildi (Takım ID: {team_id})")
                self.control_panel.update_hyi_status("Paket Gönderildi")
            else:
                self.debug_console.log("HYI paket gönderme hatası")
        else:
            self.debug_console.log("HYI bağlantısı yok")
            
    def load_map(self):
        """Harita yükleme işlemi"""
        lat, lon = self.control_panel.get_coordinates()
        self.debug_console.log(f"Harita yüklendi: Enlem={lat:.6f}, Boylam={lon:.6f}")
        
    def closeEvent(self, event):
        """Pencere kapatılırken çağrılır"""
        self.serial_manager.close_all()
        event.accept()


def main():
    """Ana fonksiyon"""
    app = QApplication(sys.argv)
    app.setStyle(QStyleFactory.create('Fusion'))
    
    window = GroundStationMainWindow()
    window.show()
    
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
