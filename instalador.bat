@echo off
@echo Compilar Transparentamelta V Alpha 2
@echo ------------------------------------
@echo Comprovant pre-requisits...
call env\Scripts\activate
py -m pip install -r prerrequisits.txt
@echo Executant la compilació...
pyinstaller --onefile --windowed --icon=icono.ico --add-data "Transparentamela.ui;." --add-data "Default.png;." --add-data "Icono.ico;." Transparentamela.py