#!/usr/bin/env python3
"""
Yer İstasyonu v2.0
Roket telemetri sistemi ana uygulaması.

Bu uygulama roket ve görev yükünden gelen telemetri verilerini
seri port üzerinden alır, işler ve görselleştirir.

Kullanım:
    python main.py

Gereksinimler:
    - Python 3.7+
    - PyQt5
    - pyserial
    - PyOpenGL
"""

import sys
import os

# Proje kök dizinini Python path'ine ekle
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)

from src.ground_station.main_window import main

if __name__ == '__main__':
    main()