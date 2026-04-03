import pandas as pd
import matplotlib.pyplot as plt

def veri_yukle():
    df = pd.read_csv("data/matches.csv")
    return df

def istatistik_goster(df):
    print("=== CS2 Maç İstatistikleri ===")
    print(f"Toplam maç: {len(df)}")
    print(f"Ortalama kill: {df['kill'].mean():.1f}")
    print(f"Ortalama death: {df['death'].mean():.1f}")
    print(f"En iyi maç (kill): {df['kill'].max()}")
    print(f"K/D oranı: {(df['kill'].sum() / df['death'].sum()):.2f}")

def harita_analizi(df):
    print("\n=== Harita Bazlı Performans ===")
    harita = df.groupby("harita")[["kill", "death"]].mean().round(1)
    print(harita)

def grafik_ciz(df):
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
    
    # Kill/Death grafiği
    ax1.plot(df["mac"], df["kill"], label="Kill", marker="o", color="green")
    ax1.plot(df["mac"], df["death"], label="Death", marker="o", color="red")
    ax1.set_title("Maç Başına Kill/Death")
    ax1.set_xlabel("Maç")
    ax1.set_ylabel("Sayı")
    ax1.legend()
    
    # Harita bazlı kill ortalaması
    harita_kill = df.groupby("harita")["kill"].mean()
    ax2.bar(harita_kill.index, harita_kill.values, color=["blue", "orange", "green"])
    ax2.set_title("Harita Bazlı Ortalama Kill")
    ax2.set_xlabel("Harita")
    ax2.set_ylabel("Ortalama Kill")
    
    plt.tight_layout()
    plt.show()