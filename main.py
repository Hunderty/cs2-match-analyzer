from analyzer import veri_yukle, istatistik_goster, harita_analizi, grafik_ciz, kazanma_tahmini, harita_kazanma

df = veri_yukle()
istatistik_goster(df)
harita_analizi(df)
kazanma_tahmini(df)
harita_kazanma(df)
grafik_ciz(df)