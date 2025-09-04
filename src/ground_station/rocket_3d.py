"""
3D Roket Görselleştirme Modülü
OpenGL kullanarak roketin 3D modelini çizer ve rotasyon güncellemelerini yapar.
"""

import math
from PyQt5.QtOpenGL import QGLWidget
from PyQt5.QtWidgets import QSizePolicy
from OpenGL.GL import *
from OpenGL.GLU import *


class RocketGLWidget(QGLWidget):
    """3D roket görselleştirme widget'ı"""
    
    def __init__(self, parent=None):
        super(RocketGLWidget, self).__init__(parent)
        self.x_rot = 0
        self.y_rot = 0
        self.z_rot = 0
        self.setMinimumSize(400, 400)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        
    def initializeGL(self):
        """OpenGL başlatma"""
        glClearColor(0.0, 0.0, 0.0, 0.0)
        glEnable(GL_DEPTH_TEST)
        
    def resizeGL(self, w, h):
        """Pencere boyutu değiştiğinde çağrılır"""
        glViewport(0, 0, w, h)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(60, w/h, 1, 10000)
        glMatrixMode(GL_MODELVIEW)
        
    def paintGL(self):
        """3D sahneyi çizer"""
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()
        gluLookAt(25, 0, 0, 0, 0, 0, 0, 1, 0)
        
        # Rotasyon uygula
        glRotatef(self.x_rot, 1.0, 0.0, 0.0)
        glRotatef(self.z_rot, 0.0, 1.0, 0.0)
        glRotatef(self.y_rot, 0.0, 0.0, 1.0)
        
        # Roket parçalarını çiz
        self._draw_rocket_body()
        self._draw_rocket_nose()
        self._draw_rocket_fins()
        self._draw_propeller()
        self._draw_axes()
        
    def _draw_rocket_body(self):
        """Roket gövdesini çizer"""
        self._draw_cylinder(1.0, 1.0, 5.0, 3, -5)
        
    def _draw_rocket_nose(self):
        """Roket burnunu çizer"""
        self._draw_cylinder(0.01, 0.01, 0.5, 9, 9.7)
        self._draw_cylinder(0.01, 0.01, 0.1, 5, 10)
        self._draw_cone(0.01, 0.01, 5.0, 3.0, 3, 5)
        
    def _draw_rocket_fins(self):
        """Roket kanatlarını çizer"""
        self._draw_cone(0.01, 0.01, 5.0, 2.0, -5.0, -10.0)
        
    def _draw_propeller(self):
        """Pervaneyi çizer"""
        self._draw_propeller_blades(9.0, 11.0, 0.2, 0.5)
        
    def _draw_axes(self):
        """Koordinat eksenlerini çizer"""
        glBegin(GL_LINES)
        # X ekseni (kırmızı)
        glColor3f(1.0, 0.0, 0.0)
        glVertex3f(-30.0, 0.0, 0.0)
        glVertex3f(30.0, 0.0, 0.0)
        
        # Y ekseni (yeşil)
        glColor3f(0.0, 1.0, 0.0)
        glVertex3f(0.0, -30.0, 0.0)
        glVertex3f(0.0, 30.0, 0.0)
        
        # Z ekseni (mavi)
        glColor3f(0.0, 0.0, 1.0)
        glVertex3f(0.0, 0.0, -30.0)
        glVertex3f(0.0, 0.0, 30.0)
        glEnd()
        
    def _draw_cylinder(self, step, topla, radius, dikey1, dikey2):
        """Silindir çizer"""
        glBegin(GL_QUADS)
        current_step = 0
        while current_step <= 360:
            # Renk deseni
            if (current_step // 45) % 2 == 0:
                glColor3f(1.0, 0.0, 0.0)  # Kırmızı
            else:
                glColor3f(1.0, 1.0, 1.0)  # Beyaz

            # Alt çember
            ciz1_x = radius * math.cos(math.radians(current_step))
            ciz1_y = radius * math.sin(math.radians(current_step))
            glVertex3f(ciz1_x, dikey1, ciz1_y)

            # Üst çember
            ciz2_x = radius * math.cos(math.radians(current_step + 2))
            ciz2_y = radius * math.sin(math.radians(current_step + 2))
            glVertex3f(ciz2_x, dikey1, ciz2_y)

            glVertex3f(ciz1_x, dikey2, ciz1_y)
            glVertex3f(ciz2_x, dikey2, ciz2_y)
            
            current_step += topla
        glEnd()
        
        # Kapakları çiz
        self._draw_cylinder_caps(radius, dikey1, dikey2)
        
    def _draw_cylinder_caps(self, radius, dikey1, dikey2):
        """Silindir kapaklarını çizer"""
        glBegin(GL_LINES)
        current_step = 0.1
        while current_step <= 180:
            if (current_step // 45) % 2 == 0:
                glColor3f(1.0, 0.0, 0.0)
            else:
                glColor3f(0.98, 0.98, 0.78)
                
            # Alt kapak
            ciz1_x = radius * math.cos(math.radians(current_step))
            ciz1_y = radius * math.sin(math.radians(current_step))
            glVertex3f(ciz1_x, dikey1, ciz1_y)
            
            ciz2_x = radius * math.cos(math.radians(current_step + 180))
            ciz2_y = radius * math.sin(math.radians(current_step + 180))
            glVertex3f(ciz2_x, dikey1, ciz2_y)
            
            # Üst kapak
            glVertex3f(ciz1_x, dikey2, ciz1_y)
            glVertex3f(ciz2_x, dikey2, ciz2_y)
            
            current_step += 0.1
        glEnd()
        
    def _draw_cone(self, step, topla, radius1, radius2, dikey1, dikey2):
        """Koni çizer"""
        glBegin(GL_LINES)
        current_step = 0
        while current_step <= 360:
            # Renk deseni
            if (current_step // 45) % 2 == 0:
                glColor3f(1.0, 1.0, 1.0)  # Beyaz
            else:
                glColor3f(1.0, 0.0, 0.0)  # Kırmızı

            # Alt çember
            ciz1_x = radius1 * math.cos(math.radians(current_step))
            ciz1_y = radius1 * math.sin(math.radians(current_step))
            glVertex3f(ciz1_x, dikey1, ciz1_y)

            # Üst çember
            ciz2_x = radius2 * math.cos(math.radians(current_step))
            ciz2_y = radius2 * math.sin(math.radians(current_step))
            glVertex3f(ciz2_x, dikey2, ciz2_y)
            
            current_step += topla
        glEnd()
        
        # Üst kapak
        self._draw_cone_cap(radius2, dikey2)
        
    def _draw_cone_cap(self, radius, dikey):
        """Koni kapağını çizer"""
        glBegin(GL_LINES)
        current_step = 0.1
        while current_step <= 180:
            if (current_step // 45) % 2 == 0:
                glColor3f(1.0, 0.0, 0.0)
            else:
                glColor3f(0.98, 0.98, 0.78)
                
            ciz1_x = radius * math.cos(math.radians(current_step))
            ciz1_y = radius * math.sin(math.radians(current_step))
            glVertex3f(ciz1_x, dikey, ciz1_y)
            
            ciz2_x = radius * math.cos(math.radians(current_step + 180))
            ciz2_y = radius * math.sin(math.radians(current_step + 180))
            glVertex3f(ciz2_x, dikey, ciz2_y)
            
            current_step += 0.1
        glEnd()
        
    def _draw_propeller_blades(self, yukseklik, uzunluk, kalinlik, egiklik):
        """Pervane kanatlarını çizer"""
        glBegin(GL_QUADS)
        
        # İlk kanat (kırmızı)
        glColor3f(1.0, 0.0, 0.0)
        glVertex3f(uzunluk, yukseklik, kalinlik)
        glVertex3f(uzunluk, yukseklik + egiklik, -kalinlik)
        glVertex3f(0.0, yukseklik + egiklik, -kalinlik)
        glVertex3f(0.0, yukseklik, kalinlik)
        
        # İkinci kanat (kırmızı)
        glColor3f(1.0, 0.0, 0.0)
        glVertex3f(-uzunluk, yukseklik + egiklik, kalinlik)
        glVertex3f(-uzunluk, yukseklik, -kalinlik)
        glVertex3f(0.0, yukseklik, -kalinlik)
        glVertex3f(0.0, yukseklik + egiklik, kalinlik)
        
        # Üçüncü kanat (beyaz)
        glColor3f(1.0, 1.0, 1.0)
        glVertex3f(kalinlik, yukseklik, -uzunluk)
        glVertex3f(-kalinlik, yukseklik + egiklik, -uzunluk)
        glVertex3f(-kalinlik, yukseklik + egiklik, 0.0)
        glVertex3f(kalinlik, yukseklik, 0.0)
        
        # Dördüncü kanat (beyaz)
        glColor3f(1.0, 1.0, 1.0)
        glVertex3f(kalinlik, yukseklik + egiklik, uzunluk)
        glVertex3f(-kalinlik, yukseklik, uzunluk)
        glVertex3f(-kalinlik, yukseklik, 0.0)
        glVertex3f(kalinlik, yukseklik + egiklik, 0.0)
        
        glEnd()
        
    def update_rotation(self, x, y, z):
        """Roket rotasyonunu günceller"""
        self.x_rot = x
        self.y_rot = y
        self.z_rot = z
        self.update()
