@echo off
title ROBO DE COBRANCA BRASIL HOSP (NAO FECHAR)
color 0A

echo ==========================================
echo    INICIANDO MONITOR DE COBRANCA V2
echo    Modo: Watchdog + Google Drive
echo ==========================================

:loop
:: Chama o Python específico (3.14) para rodar o script
:: Aspas são importantes se houver espaços no caminho da pasta
"C:\Python314\python.exe" "C:\Users\Dell\Desktop\Bryan\Demandas Tech\disparo-wpp\monitor_pasta.py"

:: Se o script Python fechar (erro ou crash), o BAT continua aqui:
echo.
echo [ALERTA] O robo parou inesperadamente.
echo Reiniciando em 10 segundos...
timeout /t 10

:: Volta para o inicio (Loop Infinito)
goto loop