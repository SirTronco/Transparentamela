from PySide6.QtWidgets import QApplication, QWidget, QSlider, QLabel, QGroupBox, QSpinBox, QFileDialog, QPushButton
from PySide6.QtUiTools import QUiLoader
from PySide6.QtCore import QFile, Qt, QAbstractNativeEventFilter, QTimer
from PySide6.QtGui import QColor, QPalette, QPixmap, QIcon

import sys
import ctypes
import os
from ctypes import wintypes

# Constants de Windows per a hotkeys
MOD_ALT = 0x0001
VK_F3 = 0x72  # F3
WM_HOTKEY = 0x0312

#======================================================
# Funció per a determinar ruta temmporal
#======================================================
def ruta_recurso(ruta):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, ruta)
    return os.path.join(os.path.abspath("."), ruta)



# ======================================================
# FILTRO NATIVU QT PER A CAPTURAR WM_HOTKEY (I.A. 100%)
# ======================================================
class HotkeyFilter(QAbstractNativeEventFilter):
    def __init__(self, callback, hotkey_id):
        super().__init__()
        self.callback = callback
        self.hotkey_id = hotkey_id

    def nativeEventFilter(self, eventType, message):
        if eventType == "windows_generic_MSG":
            msg = wintypes.MSG.from_address(message.__int__())
            if msg.message == WM_HOTKEY and msg.wParam == self.hotkey_id:
                #self.callback()
                # per a evitar que Windows flipe intentat enviar missatges a una finestra que no existeix
                QTimer.singleShot(50, self.callback)
                return True, 0
        return False, 0


class Formulari:
    def __init__(self, ui_file):
        # Cargar el UI
        file = QFile(ui_file)
        file.open(QFile.ReadOnly)
        loader = QUiLoader()
        self.window = loader.load(file)
        file.close()

        # Propietat global que controla si estem "activats"
        self.estat = False

         # Registrar hotkey ALT+F3
        #self.registrar_tecla(VK_F3, MOD_ALT, 1)

        # HOTKEY
        self.hotkey_id = 1
        ctypes.windll.user32.RegisterHotKey(
            None, self.hotkey_id, MOD_ALT, VK_F3
        )

        self.hotkey_filter = HotkeyFilter(
            self.alternarEstat, self.hotkey_id
        )
        QApplication.instance().installNativeEventFilter(
            self.hotkey_filter
        )

        # Handler per a la carga d'arxius
        self.btnMadafaca = self.window.findChild(QPushButton, "btnMadafaca")
        if self.btnMadafaca:
            self.btnMadafaca.clicked.connect(self.event_btnMadafaca)



        # Handlers dels objectes
        self.sldTrans = self.window.findChild(QSlider, "sldTrans")
        self.spbTrans = self.window.findChild(QSpinBox, "spbTrans")

        self.sldTamany = self.window.findChild(QSlider, "sldTamany")
        self.spbTamany = self.window.findChild(QSpinBox, "spbTamany")

        self.imatge    = self.window.findChild(QLabel, "lblImatge")

        # HARDCODED - Cargar imagen en el QLabel
        self.carregar_Imatge(ruta_recurso("Default.png"))

        # Conectar el slider Trans y su spinBox
        if self.sldTrans:
            self.sldTrans.setValue(100)     ; self.spbTrans.setValue(100)
            self.sldTrans.setRange(10, 100) ; self.spbTrans.setRange(10, 100)
            
            # Conectem el slide amb la opacitat del formulari
            self.sldTrans.valueChanged.connect(lambda v: self.window.setWindowOpacity(v / 100))
            
            # Conectem el slider y el valor del spinBox entre si
            self.sldTrans.valueChanged.connect(self.spbTrans.setValue)
            self.spbTrans.valueChanged.connect(self.sldTrans.setValue)


        # Conectar el slider Trans y su spinBox
        if self.sldTamany:
            self.sldTamany.setValue(100)     ; self.spbTamany.setValue(100)
            self.sldTamany.setRange(10, 100) ; self.spbTamany.setRange(10, 100)
            
            # Conectem el slide amb el tamany de la imatge
            self.sldTamany.valueChanged.connect(self.tamanyFormulari)
            #self.tamanyFormulari()
            
            # Conectem el slider y el valor del spinBox entre si
            self.sldTamany.valueChanged.connect(self.spbTamany.setValue)
            self.spbTamany.valueChanged.connect(self.sldTamany.setValue)



    #
    # ------ DEFINICIONS MÉTODES------
    #

    # Alternar estat i executar tots els camvis
    def alternarEstat(self):
        self.estat = not self.estat
        print("Click-through ", self.estat)

        # Mostrem la finestra amb els camvis
        self.mostrar(self.estat)

        self.click_through(self.estat)
        print("Nou estat Click-through aplicat."
        )
        # falta llevar el borde
        # falta menejar la imatge
        
        #self.show()
        


    # Registrar el evento de una tecla
    def registrar_tecla(self, tecla, tALT, idTecla):
        ctypes.windll.user32.RegisterHotKey(None, idTecla, tALT, tecla)


    def comprovar_tecla(self, idTecla):
        msg = wintypes.MSG()
        while ctypes.windll.user32.PeekMessageW(ctypes.byref(msg), None, 0, 0, 1):
            if msg.message == WM_HOTKEY and msg.wParam == idTecla:
                print("Tecla!")
                self.alternarEstat()
            ctypes.windll.user32.TranslateMessage(ctypes.byref(msg))
            ctypes.windll.user32.DispatchMessageW(ctypes.byref(msg))

    # Mostrar la finestra amb la configuració desitjada
    def mostrar(self, activar=False):
        # Per a evitar que Windows se ho flipe
        self.window.hide()

        # Amaguem la status bar, que no moleste
        self.window.setStatusBar(None)

        # Que la ventana esté siempre visible
        self.window.setWindowFlag(Qt.WindowStaysOnTopHint, True)

        # Lleva / fica el borde
        self.window.setWindowFlag(Qt.FramelessWindowHint, activar)

        # Handlers dels objectes
        grpOpcions = self.window.findChild(QWidget, "grpOpcions")
        lblImatge = self.window.findChild(QWidget, "lblImatge")

        grpOpcions.setVisible(not activar)
        lblImatge.move(0,0 if activar else 110)

        # Modificar el tamany de la finestra
        self.tamanyFormulari()

        # Per ultim mostrem la finestra
        self.window.show()

    # Actualitzar el tamany del formulari al de la imatge, fixant uns llimits
    def tamanyFormulari(self):
        # Handlers dels objectes
        lblImatge = self.window.findChild(QWidget, "lblImatge")
        grpOpcions = self.window.findChild(QWidget, "grpOpcions")

        # Anem a pillar el valor desde el slider i aplicarem percentatje partint del tamany de la imatge original
        percentatje = self.sldTamany.value() / 100
        lblImatge.resize(self.imatge.width() * percentatje, self.imatge.height() * percentatje)


        # Fixem parámetres minims per al estat NO activat
        minX = grpOpcions.width()
        minY = grpOpcions.height()

        # Si el estat es activat, els minims serán 0
        if self.estat:
            minX = 0
            minY = 0

        tamanyX = max(minX, lblImatge.width() )
        tamanyY = max(minY, lblImatge.height() + lblImatge.y())
        
        # Modificar el tamany de la finestra
        self.window.resize(tamanyX, tamanyY )

        #definicio de la variable que fará falta cuan acabe amb tot el meneo este perque també fará falta kje


    # Activar/desactivar el click a través (Per defecte apagat)
    def click_through(self, enable=False):
        hwnd = self.window.winId().__int__()  # obtener handle de Windows
        GWL_EXSTYLE = -20
        WS_EX_TRANSPARENT = 0x00000020
        WS_EX_LAYERED = 0x00080000

        estil = WS_EX_LAYERED # Si o sí el mostrem

        # Habilitem o no el click-through
        if enable:
            estil |= WS_EX_TRANSPARENT


        # Cridem a la API de Windows
        ctypes.windll.user32.SetWindowLongW(hwnd, GWL_EXSTYLE, estil)

    # Sel·leccionar una imatge
    def event_btnMadafaca(self):
        
        rutaImatge = self.obrir_Common_Dialog("Selecciona Imatge", "Imágenes (*.png *.jpg *.bmp *.gif)")
        if rutaImatge:
            self.carregar_Imatge(rutaImatge)

    # Diálogo per a buscar un arxiu.
    def obrir_Common_Dialog(self, texte, filtros="Tots els arxius (*.*)", ruta=""):
        #B(t)
        resultat = None #B(t)

        resultat, _ = QFileDialog.getOpenFileName(
            self.window,
            texte,              # Texte Benvinguda
            ruta,               # ruta inicial, vacía = default
            filtros             # filtros
        )

        # Tornem la ruta, si es cancel·la tornará valor Trivial (none) 
        return resultat
       

    # Métode per a carregar les imatges
    def carregar_Imatge(self, arxiu):
        # handler de la etiqueta
        lblImatge = self.window.findChild(QLabel, "lblImatge")

        self.imatge = QPixmap(arxiu)         # Creem objecte d'imatge
        lblImatge.setPixmap(self.imatge) # asignem el objecte al background de la etiqueta
        
        # redimensionem tant la etiqueta com la finestra
        lblImatge.resize(self.imatge.width(), self.imatge.height())
        #self.window.resize(pixmap.width(), pixmap.height())

        # Activem el stretch de la etiqueta
        lblImatge.setScaledContents(True)

        # Cridem per a reformatejar el formulari
        self.tamanyFormulari()



app = QApplication(sys.argv)
form = Formulari(ruta_recurso("Transparentamela.ui"))
form.window.setWindowIcon(QIcon(ruta_recurso("icono.ico"))) # li clavem el icono al formulari a calzo
form.mostrar()
sys.exit(app.exec())
