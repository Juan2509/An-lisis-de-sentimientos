# Archivo Omnitrix

Proyecto académico de análisis de opiniones sobre aliens de **Ben 10**, adaptado del taller de percepción de futbolistas. Según lo comunicado por el estudiante, en clase se permitió cambiar la temática conservando los requisitos técnicos.

## Estado

Pasos 1 a 5 completados: alcance documentado, estructura inicial, catálogo validado de 20 aliens e interfaz Streamlit con navegación y selector. Se reconstruyó `.venv` y se comprobaron las dependencias en este equipo. Las fichas con imágenes, el envío, el análisis y la persistencia de opiniones siguen pendientes. El siguiente paso es mostrar fichas e imágenes (paso 6).

## Objetivo y experiencia prevista

El usuario seleccionará un alien, verá su imagen y una ficha breve, escribirá una opinión y recibirá una clasificación de sentimiento con una explicación. La opinión y su análisis se guardarán para consultarlos después de reiniciar.

La entrega tendrá una interfaz visual en navegador y un mecanismo de inicio gráfico. Las secciones serán **Analizar opinión** y **Consultar archivo**, con una estética verde y oscura inspirada en el Omnitrix.

## Alcance de la primera versión

- Catálogo de al menos 20 aliens con identificadores estables y únicos.
- Ficha e imagen local del alien, con un recurso alternativo si falta la imagen.
- Opiniones independientes de 5 a 1000 caracteres después de eliminar espacios exteriores.
- Clasificación: positivo, negativo, neutro o mixto; validación de pertinencia y justificación breve.
- Historial visual de sesión asociado al alien seleccionado en cada envío. Nueva conversación limpia solo el chat.
- Persistencia JSON con identificador, fecha UTC, alien, texto original, análisis y metadatos.
- Consulta por alien y sentimiento, tabla, recuentos y descarga JSON con filtros coherentes.
- Errores visibles, sin clasificaciones inventadas ni confirmaciones falsas de guardado.

La IA analizará solo la opinión actual. Los comentarios ajenos no se guardarán. La clasificación representa el sentimiento del comentario, no una valoración objetiva del alien; los recuentos reflejarán únicamente los datos de esta aplicación.

## Diseño técnico propuesto

Python y Streamlit para lógica e interfaz; LangChain para la clasificación; Pydantic para validar resultados; JSON para almacenamiento local de un único escritor. Las credenciales se configurarán fuera del código y del repositorio.

Los módulos son `app.py`, `analisis.py` y `almacenamiento.py`. La interfaz ya permite navegar y seleccionar aliens, y almacenamiento carga y valida `datos/aliens.json`. El análisis sigue como archivo con descripción. El tema visual se configura en `.streamlit/config.toml` y la portada en `assets/estilos.css`. `datos/opiniones.json` y las imágenes de `assets/aliens/` se incorporarán en sus etapas.

La base no incluye combate, mecánicas de videojuego, un chatbot general, cuentas de usuario, escritura concurrente, RAG ni agentes. Galerías avanzadas, gráficos y animaciones son ampliaciones opcionales.

## Criterios de entrega

Además de la aplicación, se requieren al menos 12 opiniones ficticias entre 4 aliens y las 4 categorías, versiones utilizadas, instrucciones reproducibles, evidencias reales de persistencia y consulta filtrada, registro de pruebas y reflexión sobre dos ambigüedades o errores del análisis.

Se comprobarán también entradas inválidas, ironía, mensajes ajenos, instrucciones embebidas, cambios de alien, limpieza del chat, fallos de API y escritura, archivos dañados y ausencia de duplicados al interactuar con la interfaz.

## Documentación y continuidad

- [Contexto y especificación](CONTEXTO_PROYECTO.md): requisitos completos, fuentes de clase y decisiones del usuario.
- [Plan de desarrollo](PLAN_DESARROLLO.md): etapas, verificaciones y Conventional Commits.

Para retomar en otro equipo, abrir el repositorio y compartir ambos documentos con la nueva sesión. El entorno y las credenciales se configurarán de nuevo cuando se implemente esa etapa.

## Decisiones pendientes

- Catálogo definido: nombres latinos y cinco aliens de cada una de las cuatro series, sin versiones supremas. Ver [catálogo y fuentes](datos/README.md).
- Paso 6: selección, procedencia y disponibilidad de imágenes.
- Paso 8: modelo compatible, credenciales y evaluación real.
- Paso 11: sistema operativo de entrega y mecanismo de inicio gráfico.

La configuración de IA pendiente no impide continuar con las fichas e imágenes. Si surge una duda que afecte al alcance o a las preferencias del usuario, consultarla antes de implementar lo que dependa de ella.

## Entorno de desarrollo (paso 2)

En el equipo anterior se comprobó Linux con Python 3.14.4. En esta copia se reconstruyó `.venv` con Python 3.10.12 y se instaló `requirements.txt`. Streamlit 1.67.0 exige Python 3.11 o superior; por eso requirements selecciona Streamlit 1.65.0 para Python 3.10 y conserva 1.67.0 para Python 3.11+. Las dependencias transitivas son resueltas por pip; este archivo no es un bloqueo completo de todas ellas. El código requiere Python 3.10 o superior.

| Dependencia | Versión verificada aquí (Python 3.10.12) | Versión documentada del equipo anterior |
| --- | --- | --- |
| streamlit | 1.65.0 | 1.67.0 |
| langchain-core | 1.7.6 | 1.7.6 |
| langchain-openai | 1.7.4 | 1.7.4 |
| python-dotenv | 1.2.4 | 1.2.4 |
| pydantic | 2.14.3 | 2.14.3 |

En VS Code, abrir la paleta y elegir **Python: Select Interpreter**, seleccionando `.venv/bin/python` en Linux. En otro equipo se debe crear un entorno nuevo e instalar `requirements.txt`; no copiar `.venv`.

Referencia técnica para reconstruir el entorno (preparación de desarrollo):

```bash
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
```

Si `venv` falla por ausencia de `ensurepip`, hace falta disponer del paquete de entornos virtuales de la distribución. En esta sesión se completó el entorno instalando pip dentro de `.venv` con el pip del sistema, sin modificar los paquetes globales.

Estos comandos documentan la preparación técnica. El uso de la entrega será visual; el acceso gráfico se construirá en el paso 11. La interfaz de desarrollo se abre siguiendo las instrucciones del paso 5 que aparecen más abajo.

`datos/` y `assets/aliens/` se conservan con `.gitkeep`. El catálogo ya está en datos/aliens.json; las opiniones JSON se crearán en su etapa. `.env.example` tiene valores vacíos; al configurar el análisis se copiará a `.env` y se completará localmente. No se ha creado ninguna clave ni realizado llamadas al modelo.

Verificación realizada aquí: instalación de dependencias, `.venv/bin/python -m pip check` sin incompatibilidades e importación de las cinco bibliotecas. Se comprobaron también las pruebas del catálogo y de la interfaz; no se realizaron llamadas a la API. El aislamiento con venv sigue la [guía oficial de Streamlit](https://docs.streamlit.io/get-started/installation/command-line).

## Catálogo (paso 3)

Se añadieron 20 aliens con IDs estables, nombres latinos y alias originales. La selección incluye cinco de la serie original, cinco de Fuerza Alienígena, cinco de Supremacía Alienígena y cinco de Omniverse, sin versiones supremas. Las imágenes están pendientes y se representan con `null`. Ver [contrato de datos y fuentes](datos/README.md).

## Carga y validación del catálogo (paso 4)

`almacenamiento.cargar_aliens()` devuelve la lista de aliens validada. Comprueba la versión entera 1, un mínimo de 20 registros, campos obligatorios, textos no vacíos, IDs únicos sin espacios exteriores e imágenes `null` o rutas locales relativas con `/` y sin `..`. No exige todavía que las imágenes existan. Las rutas relativas del catálogo parten de la raíz del proyecto, independientemente del directorio de inicio.

Si falta el archivo, no puede leerse, no usa UTF-8, contiene JSON dañado o incumple el esquema, lanza `ErrorCatalogo` con un mensaje en español. La lectura no crea ni modifica archivos. La interfaz muestra estos errores y no presenta el selector cuando falla el catálogo.

Comprobación técnica, desde la raíz del repositorio y sin dependencias externas:

```bash
python3 -m unittest discover -s tests -p 'test_catalogo.py' -v
```

Resultado observado con Python 3.10.12: 19 pruebas correctas, incluyendo el catálogo real, los errores previstos, la conservación de archivos inválidos y las rutas desde otro directorio. El error de permisos se simula con `unittest.mock`. Estas pruebas no verifican todavía la interfaz ni la API.

## Navegación y selección visual (paso 5)

La interfaz tiene dos secciones: **Analizar opinión** permite seleccionar cualquiera de los 20 aliens y muestra el nombre y la serie de introducción; **Consultar archivo** informa que la consulta de opiniones sigue pendiente. La selección se conserva al cambiar de sección. No hay todavía envío de opiniones ni análisis o guardado.

El tema nativo de Streamlit usa fondo oscuro, texto claro y acento verde. La portada tiene un emblema decorativo hecho con CSS y una distribución adaptable a pantallas pequeñas. No utiliza imágenes de aliens ni recursos remotos.

Inicio técnico para desarrollo, desde la raíz del repositorio:

```bash
.venv/bin/python -m streamlit run app.py
```

Abrir la dirección local que muestre Streamlit, normalmente `http://localhost:8501`. Ejecutar desde la raíz permite cargar `.streamlit/config.toml`. El inicio mediante acceso gráfico de la entrega corresponde al paso 11.

Pruebas completas, con las dependencias instaladas:

```bash
.venv/bin/python -m unittest discover -s tests -v
.venv/bin/python -m pip check
```

Resultado del paso 5: 24 pruebas correctas (19 del catálogo y 5 de interfaz con `streamlit.testing.v1.AppTest`), sin incompatibilidades de dependencias. Se verificaron todos los aliens, conservación de selección y errores visibles. También se comprobó el servidor con HTTP 200 y se revisó la interfaz en Chrome sin ventana a 1440 y 390 píxeles, con navegación entre secciones. La compatibilidad de esta interfaz con Streamlit 1.67.0 no se volvió a ejecutar aquí.

Referencias técnicas: [tema de Streamlit](https://docs.streamlit.io/develop/api-reference/configuration/config.toml) y [pruebas de aplicaciones](https://docs.streamlit.io/develop/api-reference/app-testing).
