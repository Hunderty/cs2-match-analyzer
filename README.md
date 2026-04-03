# CS2 Maç Analizci 🎮

CS2 demo dosyalarını (.dem) analiz eden, oyuncu istatistiklerini ve grafiklerini gösteren bir uygulama.

## Özellikler
- Demo dosyasını yükle, istatistikleri otomatik çıkar
- Kill, death, K/D oranı, headshot oranı
- Oyuncu bazlı kill sıralaması grafiği
- Makine öğrenmesi ile kazanma tahmini

## Kurulum

1. Repoyu indir:git clone https://github.com/kullaniciadin/cs2-match-analyzer
2. Kütüphaneleri yükle:pip install -r requirements.txt
3. Uygulamayı çalıştır:streamlit run app.py
4. Tarayıcıda açılan sayfaya CS2 demo dosyanı (.dem) yükle!

## Kullanılan Teknolojiler
- Python
- Streamlit
- Pandas
- Matplotlib
- Scikit-learn
- Demoparser2