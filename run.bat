@echo off
setlocal EnableDelayedExpansion

REM Vérifier si Python 3.10 est installé
where python >nul 2>nul
if errorlevel 1 (
    echo [ERREUR] Python n'est pas installé ou non détecté dans le PATH.
    pause
    exit /b
)

REM Vérifier si le venv existe
if not exist venv (
    echo [INFO] Création de l'environnement virtuel...
    py -3.10 -m venv venv
    if errorlevel 1 (
        echo [ERREUR] Échec de création de l'environnement virtuel.
        pause
        exit /b
    )
)

REM Activation de l'environnement virtuel
call .\venv\Scripts\activate.bat

REM Installer les dépendances
echo [INFO] Installation des dépendances...
python -m pip install --upgrade pip
python -m pip install -r requirements.txt

REM Lancement du script
if "%~1"=="" (
    echo [INFO] Lancement en mode Gradio...
    python reverse_video.py
) else (
    echo [INFO] Lancement en mode CLI avec les paramètres : %*
    python reverse_video.py %*
)

REM Garder la fenêtre ouverte à la fin
echo.
echo [FIN] Appuyez sur une touche pour quitter...
pause
