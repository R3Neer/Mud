TUTORIAL = r'''
REPO-PATCHER — TUTORIAL PARA POWERSHELL
=======================================

¿Qué hace?
----------
Aplica un paquete de cambios a una repo Git. Antes de escribir comprueba que
estás en la repo correcta y que Git está limpio. Si un generador o validador
falla, vuelve automáticamente al estado anterior.

La herramienta NO crea commits ni hace push.

Instalación recomendada
-----------------------
Desde la carpeta descomprimida de repo-patcher:

    py -m pip install pipx
    py -m pipx ensurepath
    py -m pipx install .

Cierra y vuelve a abrir PowerShell. Después debe funcionar:

    repo-patcher --version

Uso normal
----------
1. Entra en tu repo:

    Set-Location "D:\Ruta\A\TuRepo"

2. Pide una explicación del paquete:

    repo-patcher explain "C:\Descargas\mi-patch.zip"

3. Comprueba que puede aplicarse sin modificar archivos:

    repo-patcher check "C:\Descargas\mi-patch.zip"

4. Aplícalo:

    repo-patcher apply "C:\Descargas\mi-patch.zip"

5. Revisa el resultado:

    git status
    git diff --stat
    git diff

6. Si todo está bien, crea tú el commit:

    git add .
    git commit -m "Descripción del cambio"

¿Y si no estoy dentro de la repo?
---------------------------------
Indica la ruta explícitamente:

    repo-patcher check "C:\Descargas\mi-patch.zip" `
        --repo "D:\Ruta\A\TuRepo"

Generar además un diff tradicional
-----------------------------------

    repo-patcher apply "C:\Descargas\mi-patch.zip" `
        --emit-diff "C:\Descargas\resultado.patch"

Paquetes con plugin Python
--------------------------
Un plugin es código. La herramienta muestra una advertencia y pide confirmar.
Usa paquetes de procedencia fiable. En automatizaciones no interactivas debes
escribir explícitamente:

    repo-patcher apply ".\mi-patch.zip" --trust-plugin

Problemas frecuentes
---------------------

«El árbol de trabajo no está limpio»
    Ejecuta git status. Confirma, guarda con git stash o descarta tus cambios.

«HEAD incompatible»
    El paquete fue preparado para otra revisión. No fuerces la aplicación sin
    revisar la divergencia. Pide una versión nueva del paquete.

«No se encontró el fragmento esperado»
    Un archivo cambió respecto al contexto del paquete. No se modificó nada.

«Falló un validador»
    La herramienta restauró automáticamente la repo. Conserva el mensaje de
    error para corregir el paquete.

Comandos disponibles
--------------------

    repo-patcher tutorial
    repo-patcher doctor [--repo RUTA]
    repo-patcher explain PAQUETE [--repo RUTA]
    repo-patcher check PAQUETE [--repo RUTA]
    repo-patcher apply PAQUETE [--repo RUTA] [--emit-diff RUTA]
    repo-patcher package-info PAQUETE
'''.strip()
