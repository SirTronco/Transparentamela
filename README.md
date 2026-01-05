# Transparentamela
Utilidad simple en Python para situar una imagen con transparencia y Click-Trhough

# ¿Porqué?
Necesitaba un teclado en pantalla que se puediera ver en todo momento pero que no molestara. Pero no encontré nada que fuera fácil, sencillo y ligero. Lo podía hacer fácil con Visual Studio C# pero...¡Qué pereza! Así que le pregunté a "Chattie" si había alguna forma de hacer una aplicación Win32 en Python y me dijo:
 · ¡Claro, menda! Puedes usar QT Designer para el formulario y luego lo cargas desde el programa en Python.

 Y ale, ahí está. Obviamente hay un par de cosas que son 100% de él; evitar el cuelgue del sistema al intentar enviar pulsaciones a una ventana con click-through y cómo cargar los archivos en la temporal de la VM de Python. Pero lo demás lo he estructurado a como suelo programar (y todavía no está como quiero): Llamar a una función y que me devuelva un valor, estructura de bucle formalizada, etc (las IA detestan estas estructuras)

 # Dependencias
  - Python versión 3.12.10
  - PyInstaller versión 6.17.00

# TODO
 - Guardar preferencias (y resetearlas) y imagen de carga
 - Opción para fijar la imagen en uno de los bordes
 - Opción para "fit/stretch" de la imagen en la pantalla
