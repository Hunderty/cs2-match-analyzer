from analyzer import veri_yukle, istatistik_goster, harita_analizi, grafik_ciz

df = veri_yukle()
istatistik_goster(df)
harita_analizi(df)
grafik_ciz(df)