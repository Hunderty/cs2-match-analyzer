@echo off
echo CS2 Mac Analizci basliyor...
python -m streamlit run app.py --server.maxUploadSize 1000
pause