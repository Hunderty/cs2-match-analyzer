import sys
import os
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                              QHBoxLayout, QListWidget, QPushButton, QLabel, 
                              QTableWidget, QTableWidgetItem, QHeaderView)
from PyQt6.QtCore import Qt, QThread, pyqtSignal
from PyQt6.QtGui import QFont
from demoparser2 import DemoParser
import pandas as pd

DEMO_KLASORU = r"C:\Program Files (x86)\Steam\steamapps\common\Counter-Strike Global Offensive\game\csgo\replays"

class AnalizThread(QThread):
    tamamlandi = pyqtSignal(object)
    
    def __init__(self, demo_yolu):
        super().__init__()
        self.demo_yolu = demo_yolu
    
    def run(self):
        parser = DemoParser(self.demo_yolu)
        df = parser.parse_event("player_death")
        
        kills = df.groupby("attacker_name").size().reset_index(name="kill")
        deaths = df.groupby("user_name").size().reset_index(name="death")
        headshots = df[df["headshot"] == True].groupby("attacker_name").size().reset_index(name="headshot")
        
        stats = kills.merge(deaths, left_on="attacker_name", right_on="user_name", how="outer")
        stats = stats.merge(headshots, on="attacker_name", how="left")
        stats = stats.rename(columns={"attacker_name": "oyuncu"})
        stats["kd"] = (stats["kill"] / stats["death"]).round(2)
        stats["hs_oran"] = (stats["headshot"] / stats["kill"] * 100).round(1)
        stats = stats[["oyuncu", "kill", "death", "kd", "hs_oran"]].sort_values("kill", ascending=False)
        
        self.tamamlandi.emit(stats)

class AnaPencere(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("CS2 Maç Analizci")
        self.setMinimumSize(900, 600)
        self.setStyleSheet("background-color: #1a1a2e; color: white;")
        self.arayuz_olustur()
        self.demolari_yukle()
    
    def arayuz_olustur(self):
        merkez = QWidget()
        self.setCentralWidget(merkez)
        ana_layout = QHBoxLayout(merkez)
        
        # Sol panel - demo listesi
        sol = QVBoxLayout()
        baslik = QLabel("CS2 Maç Analizci 🎮")
        baslik.setFont(QFont("Arial", 16, QFont.Weight.Bold))
        baslik.setAlignment(Qt.AlignmentFlag.AlignCenter)
        sol.addWidget(baslik)
        
        demo_label = QLabel("Demolar:")
        demo_label.setFont(QFont("Arial", 10))
        sol.addWidget(demo_label)
        
        self.demo_listesi = QListWidget()
        self.demo_listesi.setStyleSheet("background-color: #16213e; border-radius: 5px; padding: 5px;")
        sol.addWidget(self.demo_listesi)
        
        self.analiz_btn = QPushButton("Analiz Et")
        self.analiz_btn.setStyleSheet("background-color: #e94560; color: white; padding: 10px; border-radius: 5px; font-size: 14px;")
        self.analiz_btn.clicked.connect(self.analiz_et)
        sol.addWidget(self.analiz_btn)
        
        ana_layout.addLayout(sol, 1)
        
        # Sağ panel - istatistikler
        sag = QVBoxLayout()
        self.durum_label = QLabel("Bir demo seçin ve 'Analiz Et' butonuna basın.")
        self.durum_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        sag.addWidget(self.durum_label)
        
        self.tablo = QTableWidget()
        self.tablo.setStyleSheet("background-color: #16213e; border-radius: 5px;")
        self.tablo.setColumnCount(5)
        self.tablo.setHorizontalHeaderLabels(["Oyuncu", "Kill", "Death", "K/D", "HS%"])
        self.tablo.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        sag.addWidget(self.tablo)
        
        ana_layout.addLayout(sag, 2)
    
    def demolari_yukle(self):
        if os.path.exists(DEMO_KLASORU):
            for dosya in os.listdir(DEMO_KLASORU):
                if dosya.endswith(".dem"):
                    self.demo_listesi.addItem(dosya)
        else:
            self.durum_label.setText("Demo klasörü bulunamadı!")
    
    def analiz_et(self):
        secili = self.demo_listesi.currentItem()
        if not secili:
            self.durum_label.setText("Lütfen bir demo seçin!")
            return
        
        demo_yolu = os.path.join(DEMO_KLASORU, secili.text())
        self.durum_label.setText("Analiz ediliyor...")
        self.analiz_btn.setEnabled(False)
        
        self.thread = AnalizThread(demo_yolu)
        self.thread.tamamlandi.connect(self.sonuclari_goster)
        self.thread.start()
    
    def sonuclari_goster(self, stats):
        self.tablo.setRowCount(len(stats))
        for i, row in stats.iterrows():
            self.tablo.setItem(i, 0, QTableWidgetItem(str(row["oyuncu"])))
            self.tablo.setItem(i, 1, QTableWidgetItem(str(row["kill"])))
            self.tablo.setItem(i, 2, QTableWidgetItem(str(row["death"])))
            self.tablo.setItem(i, 3, QTableWidgetItem(str(row["kd"])))
            self.tablo.setItem(i, 4, QTableWidgetItem(str(row["hs_oran"])))
        
        self.durum_label.setText("Analiz tamamlandi!")
        self.analiz_btn.setEnabled(True)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    pencere = AnaPencere()
    pencere.show()
    sys.exit(app.exec())