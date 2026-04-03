import pandas as pd
import matplotlib.pyplot as plt

# Örnek CS2 maç verisi
data = {
    "Maç": [1, 2, 3, 4, 5],
    "Kill": [15, 22, 18, 25, 20],
    "Death": [12, 10, 15, 8, 11],
    "Asist": [3, 5, 2, 7, 4]
}

df = pd.DataFrame(data)
print(df)

# K/D oranı hesapla
df["KD"] = df["Kill"] / df["Death"]
print("\nK/D Oranları:")
print(df[["Maç", "KD"]])

# Grafik çiz
plt.plot(df["Maç"], df["Kill"], label="Kill", marker="o")
plt.plot(df["Maç"], df["Death"], label="Death", marker="o")
plt.title("CS2 Maç İstatistikleri")
plt.xlabel("Maç")
plt.ylabel("Sayı")
plt.legend()
plt.show()