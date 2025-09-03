@echo off
REM Este script renomeia arquivos de "hero_X" para "hero_idle_X", 
REM mantendo a extensão original do arquivo.

echo Iniciando a renomeacao dos arquivos...

FOR /L %%i IN (0,1,9) DO (
    IF EXIST "hero_%%i.*" (
        ren "hero_%%i.*" "hero_idle_%%i.*"
        echo Arquivo "hero_%%i" renomeado para "hero_idle_%%i".
    )
)

echo.
echo Processo concluido!
pause