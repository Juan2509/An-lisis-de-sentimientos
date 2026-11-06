"""Lectura y validación del catálogo de Archivo Omnitrix.

La persistencia y las consultas de opiniones se implementarán en otras etapas.
"""

import json
from pathlib import Path, PureWindowsPath


RAIZ_PROYECTO = Path(__file__).resolve().parent
RUTA_CATALOGO = RAIZ_PROYECTO / "datos" / "aliens.json"
CAMPOS_TEXTO = ("id", "nombre", "nombre_original", "serie_origen", "descripcion")


class ErrorCatalogo(ValueError):
    """El catálogo no se puede leer o no cumple su contrato de datos."""


def _validar_catalogo(datos: object) -> list[dict]:
    """Comprueba la versión 1 y devuelve los aliens sin modificar sus datos."""
    if not isinstance(datos, dict):
        raise ErrorCatalogo("La raíz del catálogo debe ser un objeto JSON.")

    # bool es una subclase de int en Python; true no es una versión válida.
    if type(datos.get("version")) is not int or datos["version"] != 1:
        raise ErrorCatalogo("El catálogo debe indicar version como el entero 1.")

    aliens = datos.get("aliens")
    if not isinstance(aliens, list):
        raise ErrorCatalogo("El campo 'aliens' debe ser una lista.")
    if len(aliens) < 20:
        raise ErrorCatalogo("El catálogo debe contener al menos 20 aliens.")

    ids = set()
    for posicion, alien in enumerate(aliens, start=1):
        referencia = f"Alien en la posición {posicion}"
        if not isinstance(alien, dict):
            raise ErrorCatalogo(f"{referencia}: debe ser un objeto JSON.")

        for campo in (*CAMPOS_TEXTO, "imagen"):
            if campo not in alien:
                raise ErrorCatalogo(f"{referencia}: falta el campo '{campo}'.")

        for campo in CAMPOS_TEXTO:
            valor = alien[campo]
            if not isinstance(valor, str) or not valor.strip():
                raise ErrorCatalogo(
                    f"{referencia}: '{campo}' debe ser texto no vacío."
                )

        alien_id = alien["id"]
        if alien_id != alien_id.strip():
            raise ErrorCatalogo(f"{referencia}: el ID no debe tener espacios exteriores.")
        if alien_id in ids:
            raise ErrorCatalogo(f"{referencia}: ID repetido '{alien_id}'.")
        ids.add(alien_id)

        imagen = alien["imagen"]
        if imagen is None:
            continue
        if not isinstance(imagen, str) or not imagen.strip():
            raise ErrorCatalogo(
                f"{referencia}: 'imagen' debe ser una ruta relativa o null."
            )

        ruta_imagen = Path(imagen)
        if (
            ruta_imagen.is_absolute()
            or PureWindowsPath(imagen).drive
            or "\\" in imagen
            or "\x00" in imagen
            or "://" in imagen
            or ".." in ruta_imagen.parts
        ):
            raise ErrorCatalogo(
                f"{referencia}: 'imagen' debe ser una ruta local relativa "
                "dentro del proyecto, usando '/' y sin '..'."
            )

    return aliens


def cargar_aliens(ruta: str | Path = RUTA_CATALOGO) -> list[dict]:
    """Lee un catálogo UTF-8 y devuelve su lista de aliens validada.

    Las rutas relativas se interpretan desde la raíz del proyecto. Las rutas
    absolutas permiten cargar otro catálogo, por ejemplo durante las pruebas.
    Ante errores lanza ErrorCatalogo; nunca crea ni sobrescribe archivos.
    La existencia de las imágenes se comprobará al mostrar las fichas.
    """
    ruta = Path(ruta)
    if not ruta.is_absolute():
        ruta = RAIZ_PROYECTO / ruta

    try:
        contenido = ruta.read_text(encoding="utf-8")
    except FileNotFoundError as error:
        raise ErrorCatalogo(f"No se encontró el catálogo: {ruta}.") from error
    except UnicodeError as error:
        raise ErrorCatalogo(f"El catálogo debe estar codificado en UTF-8: {ruta}.") from error
    except OSError as error:
        raise ErrorCatalogo(f"No se pudo leer el catálogo: {ruta}.") from error

    try:
        datos = json.loads(contenido)
    except json.JSONDecodeError as error:
        raise ErrorCatalogo(
            f"El catálogo contiene JSON inválido: {ruta} "
            f"(línea {error.lineno}, columna {error.colno})."
        ) from error

    return _validar_catalogo(datos)
