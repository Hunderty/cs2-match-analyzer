from demoparser2 import DemoParser
import pandas as pd
import os

data_klasoru = "data"
for dosya in os.listdir(data_klasoru):
    if dosya.endswith(".dem"):
        demo_yolu = os.path.join(data_klasoru, dosya)
        break

parser = DemoParser(demo_yolu)
df = parser.parse_event("player_death")

# Kill istatistikleri
kills = df.groupby("attacker_name").size().reset_index(name="kill")
deaths = df.groupby("user_name").size().reset_index(name="death")
headshots = df[df["headshot"] == True].groupby("attacker_name").size().reset_index(name="headshot")

# Birleştir
stats = kills.merge(deaths, left_on="attacker_name", right_on="user_name", how="outer")
stats = stats.merge(headshots, on="attacker_name", how="left")
stats = stats.rename(columns={"attacker_name": "oyuncu"})
stats["kd"] = (stats["kill"] / stats["death"]).round(2)
stats["hs_oran"] = (stats["headshot"] / stats["kill"] * 100).round(1)

print("=== Oyuncu İstatistikleri ===")
print(stats[["oyuncu", "kill", "death", "kd", "hs_oran"]].sort_values("kill", ascending=False).to_string())