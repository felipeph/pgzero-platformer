@echo off
SETLOCAL EnableDelayedExpansion

REM --- Configuracao ---
SET "baseName=hero_idle"
SET "extension=png"
REM --------------------

ECHO Iniciando a criacao dos arquivos para fechar o ciclo da animacao...
ECHO.

REM O loop vai de 8 para 1 (nossos arquivos de origem, em ordem reversa)
FOR /L %%S IN (8, -1, 1) DO (
    REM Para cada valor de %%S (8, 7, 6...), calculamos o numero do arquivo de destino.
    REM A logica e: Destino = 18 - Origem
    REM Ex: Quando a Origem (%%S) e 8, o Destino e 18 - 8 = 10
    REM Ex: Quando a Origem (%%S) e 7, o Destino e 18 - 7 = 11
    SET /A "destIndex=18-%%S"

    REM Monta os nomes completos dos arquivos de origem e destino
    SET "sourceFile=!baseName!_%%S.!extension!"
    SET "destFile=!baseName!_!destIndex!.!extension!"

    REM Verifica se o arquivo de origem realmente existe antes de copiar
    IF EXIST "!sourceFile!" (
        ECHO Copiando "!sourceFile!" para "!destFile!"...
        COPY "!sourceFile!" "!destFile!"
    ) ELSE (
        ECHO AVISO: O arquivo de origem "!sourceFile!" nao foi encontrado. Pulando.
    )
)

ECHO.
ECHO Processo concluido!
PAUSE