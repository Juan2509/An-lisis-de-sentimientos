Option Explicit

Dim archivos, shell, raiz, python, lanzador, faltantes, comprobar, codigo
Set archivos = CreateObject("Scripting.FileSystemObject")
Set shell = CreateObject("WScript.Shell")
raiz = archivos.GetParentFolderName(WScript.ScriptFullName)
python = archivos.BuildPath(raiz, ".venv\Scripts\python.exe")
lanzador = archivos.BuildPath(raiz, "iniciar.py")
comprobar = WScript.Arguments.Named.Exists("comprobar")
faltantes = ""

If Not archivos.FileExists(python) Then faltantes = faltantes & vbCrLf & "- .venv\Scripts\python.exe"
If Not archivos.FileExists(lanzador) Then faltantes = faltantes & vbCrLf & "- iniciar.py"
If Not archivos.FileExists(archivos.BuildPath(raiz, "app.py")) Then faltantes = faltantes & vbCrLf & "- app.py"
If Not archivos.FileExists(archivos.BuildPath(raiz, "requirements.txt")) Then faltantes = faltantes & vbCrLf & "- requirements.txt"

If faltantes <> "" Then
    If comprobar Then
        WScript.Echo "Entorno sin preparar. Faltan:" & faltantes
    Else
        MsgBox "No se puede iniciar Archivo Omnitrix. Faltan:" & faltantes & vbCrLf & vbCrLf & _
            "Prepara el entorno de Windows siguiendo README.md (Inicio grafico). " & _
            "El lanzador no instala Python ni dependencias automaticamente.", vbExclamation, "Archivo Omnitrix"
    End If
    WScript.Quit 2
End If

If comprobar Then
    WScript.Echo "Archivos de inicio presentes. Este diagnostico no comprueba dependencias ni abre la aplicacion."
    WScript.Quit 0
End If

shell.CurrentDirectory = raiz
' El proceso se ejecuta oculto; iniciar.py presenta los controles graficos.
On Error Resume Next
codigo = shell.Run(Chr(34) & python & Chr(34) & " " & Chr(34) & lanzador & Chr(34), 0, True)
If Err.Number <> 0 Then
    MsgBox "No se pudo ejecutar el Python del proyecto. Revisa el entorno .venv y README.md.", vbExclamation, "Archivo Omnitrix"
    WScript.Quit 1
End If
On Error GoTo 0
If codigo <> 0 Then
    MsgBox "El inicio no se completo. Revisa la ventana de aviso y el archivo inicio.log, si existe.", vbExclamation, "Archivo Omnitrix"
End If
WScript.Quit codigo
