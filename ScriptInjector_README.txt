ScriptInjector

Descripción:
ScriptInjector es una herramienta ofensiva del Red Team que automatiza la inyección de payloads para detectar vulnerabilidades XSS, SQLi, LFI y SSTI en parámetros GET, POST y cabeceras HTTP.

Uso básico:
Ejemplo para probar inyección XSS en parámetros GET:

    python script_injector.py "http://victima.com/test.php?q=test" -m get -t XSS

Cómo descargarla:
Clona este repositorio:

    git clone https://github.com/tuusuario/OffSec-Tools.git

Luego navega a la carpeta ScriptInjector:

    cd OffSec-Tools/ScriptInjector

Advertencia:
Usar solo en entornos controlados y con permiso.
