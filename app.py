import streamlit as st
from demoparser2 import DemoParser
import pandas as pd
import matplotlib.pyplot as plt
import tempfile
import os

st.title("CS2 Maç Analizci 🎮")
st.write("Demo dosyanı yükle, istatistiklerini gör!")

demo_file = st.file_uploader("Demo dosyasını seç (.dem)", type=["dem"])

if demo_file is not None:
    with tempfile.NamedTemporaryFile(delete=False, suffix=".dem") as tmp:
        tmp.write(demo_file.read())
        tmp_path = tmp.name

    st.info("Demo okunuyor...")

    parser = DemoParser(tmp_path)
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

    st.success("Demo okundu!")
    st.subheader("Oyuncu İstatistikleri")
    st.dataframe(stats, use_container_width=True)

    st.subheader("Kill Sıralaması")
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.barh(stats["oyuncu"], stats["kill"], color="green")
    ax.set_xlabel("Kill")
    ax.set_title("Oyuncu Bazlı Kill")
    plt.tight_layout()
    st.pyplot(fig)

    os.unlink(tmp_path)