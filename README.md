# Archivo Omnitrix

Proyecto académico de análisis de opiniones sobre aliens de **Ben 10**, adaptado del taller de percepción de futbolistas. Según lo comunicado por el estudiante, en clase se permitió cambiar la temática conservando los requisitos técnicos.

## Estado

Pasos 1 a 6 completados. Los pasos 7 a 10 están implementados y pendientes de verificación ejecutable en esta copia de Windows: captura, clasificación, persistencia, consulta y exportación de opiniones. Aquí no existe `.venv` ni se encontró Python en el PATH; las comprobaciones de entorno descritas más abajo corresponden al equipo anterior. El siguiente desarrollo es el inicio gráfico (paso 11).

## Opiniones de sesión (paso 7)

Debajo de la ficha se puede enviar una opinión de 5 a 1000 caracteres, contando después de quitar espacios exteriores y sin recortar el texto. Cada envío conserva el texto original, ID y nombre del alien seleccionado. El historial permanece al cambiar de alien o sección; dos envíos iguales son independientes. Los textos rechazados quedan visibles para recuperarlos y corregirlos.

«Nueva conversación» limpia el historial y el texto rechazado, conservando la selección y las opiniones guardadas en disco. Desde el paso 8, los envíos válidos se analizan con IA cuando existe configuración; desde el paso 9, los pertinentes se guardan en `datos/opiniones.json`. El chat solo dura durante la sesión de Streamlit.

Se añadieron tres pruebas de interacción para estos flujos y se actualizó la prueba de inicio. `git diff --check` correcto; pruebas Python pendientes de ejecutar con las dependencias instaladas mediante `python -m unittest discover -s tests -v`.

## Clasificación estructurada (paso 8)

Preparación de desarrollo: copiar `.env.example` a `.env` y completar localmente `OPENAI_API_KEY` y `OPENAI_MODEL`. No pegar claves en el código, el chat o el repositorio. El modelo debe estar disponible en la cuenta y admitir Structured Outputs con `json_schema`. No se fija un modelo ni se supone que la cuenta tenga acceso. `OPENAI_TEMPERATURE=0` se usa si el modelo lo admite; dejar el valor vacío para omitir el parámetro. Las variables del sistema tienen prioridad sobre `.env`, que se lee desde la raíz del proyecto sin modificar el entorno global.

`analisis.py` compone `ChatPromptTemplate | modelo.with_structured_output(...)` e invoca el resultado completo. Pydantic exige pertinencia booleana, una de las cuatro categorías o `null`, razón no vacía de hasta 300 caracteres y coherencia: solo las opiniones pertinentes llevan sentimiento. La longitud de la razón y la relación entre campos se comprueban localmente. El prompt `omnitrix-v1` contiene reglas de ironía y separación entre instrucciones y datos. El envío incluye únicamente datos del alien y texto actual, sin historial. La salida estructurada no garantiza que el juicio de sentimiento sea correcto.

La interfaz muestra el resultado o el rechazo por falta de pertinencia. Ante configuración incompleta, fallo de API o resultado inválido, conserva el comentario y muestra un error sin inventar una categoría. Cada envío válido intenta una llamada, con espera máxima de 30 segundos y sin reintentos automáticos. Navegar no repite el análisis; reenviar es un envío independiente. Se conservan modelo y versión del prompt en el registro persistente de las opiniones pertinentes.

Verificación del paso 8: cinco pruebas nuevas del contrato y la cadena, y dos nuevas de interfaz; las pruebas de chat usan dobles locales y nunca consumen API. No ejecutadas en esta copia por ausencia de Python y `.venv`. No se ha evaluado un modelo real ni confirmado acceso o credenciales. Antes de cerrar la etapa, ejecutar la suite y evaluar elogios, críticas, neutralidad, mixtos, ironía, texto ajeno e instrucciones embebidas con el modelo elegido.

Referencias de implementación: [Structured Outputs de OpenAI](https://developers.openai.com/api/docs/guides/structured-outputs) y [salida estructurada de LangChain](https://reference.langchain.com/python/langchain-openai/chat_models/base/ChatOpenAI/with_structured_output).

## Persistencia local (paso 9)

`almacenamiento.py` implementa `crear_registro`, `cargar_opiniones` y `guardar_opinion`. El archivo parte de `{"version": 1, "opiniones": []}`; cada registro guarda UUID, fecha UTC, ID/nombre del alien capturado, opinión original, sentimiento, razón, modelo y versión del prompt. La aplicación genera UUID y fecha; el modelo no controla la identidad del envío. Solo las opiniones pertinentes con análisis válido se guardan.

Las rutas relativas parten del proyecto. Leer un archivo ausente devuelve una lista vacía sin crearlo; el primer guardado crea la estructura con su registro. Si existe, se valida versión, estructura, campos, UUID, fecha UTC, longitudes, categoría e IDs únicos antes de escribir. Los archivos ilegibles, dañados o con esquema inesperado se conservan y producen un error visible.

La escritura UTF-8 mantiene los acentos y utiliza un temporal en el mismo directorio, `flush`, `fsync` y reemplazo final. Un fallo intenta limpiar el temporal y mantiene la opinión disponible en sesión. El alcance es un único escritor local: el reemplazo atómico no resuelve actualizaciones concurrentes.

La interfaz confirma «Opinión guardada en el Archivo Omnitrix» solo después de un guardado exitoso o de comprobar que el mismo registro ya existe. Si falla, «Reintentar guardado» reutiliza UUID, fecha y análisis, sin consumir API. Un ID existente con datos distintos se rechaza; dos envíos independientes con el mismo texto conservan IDs distintos. Cambiar de alien o sección no dispara escrituras. Limpiar el chat no modifica el JSON. El chat no se reconstruye desde disco; los registros persistentes se consultan en Consultar archivo.

Verificación: siete pruebas nuevas de almacenamiento con archivos temporales y una nueva de interfaz para fallo/reintento; las pruebas de interfaz aíslan la ruta para no modificar el archivo real. Cubren lectura posterior, duplicados, conflictos, JSON/UTF-8 inválidos, fallos de escritura y reemplazo, limpieza y rechazos. No ejecutadas por ausencia de Python y `.venv`. `git diff --check` correcto. Para comprobar solo la persistencia basta Python estándar: `python -m unittest discover -s tests -p test_opiniones.py -v`; la suite completa requiere instalar `requirements.txt`. La prueba de reinicio real de la aplicación sigue pendiente.

## Consulta y exportación (paso 10)

En **Consultar archivo**, seleccionar un alien y/o un sentimiento, o dejar «Todos». El selector de aliens se construye a partir de los registros guardados e incluye el ID para distinguir nombres repetidos. Se puede consultar el archivo aunque el catálogo de aliens falle o cambie. Los nombres y textos de la tabla son los conservados al guardar cada envío.

`consultar_opiniones` combina ambos filtros con AND, conserva el orden del archivo y devuelve copias de los registros sin modificar los originales. La interfaz usa exactamente esa lista para el total, los cuatro recuentos, la tabla y la descarga. La tabla muestra fecha UTC, alien/ID, opinión original, sentimiento y razón; los recuentos solo describen los registros de esta aplicación.

«Descargar resultados filtrados (JSON)» genera UTF-8 con `version: 1` y los registros completos de la selección, incluyendo UUID y metadatos. El botón usa `on_click="ignore"` para no provocar una reejecución al descargar. Si el archivo está vacío o los filtros no encuentran coincidencias, se muestra un aviso, total y categorías en cero y se permite descargar una lista vacía. Un archivo dañado produce un error y no muestra tabla, métricas ni descarga de datos incompletos.

Consultar, filtrar y descargar no llaman al modelo ni escriben el archivo. Las opiniones se leen de nuevo en cada ejecución, sin caché. Si el ID filtrado desaparece del archivo, el selector vuelve a «Todos».

Verificación: tres pruebas nuevas de filtros puros y cuatro de interfaz para coherencia entre tabla/recuentos/exportación, lectura sin escritura ni IA, estado vacío, archivo dañado y actualización de opciones. No se ejecutaron por ausencia de Python y `.venv`; `git diff --check` correcto. Para ejecutar los filtros basta Python estándar: `python -m unittest discover -s tests -p test_consultas.py -v`. La revisión visual y descarga desde el navegador quedan pendientes junto a la suite completa. Referencias de los componentes: [tabla de Streamlit](https://docs.streamlit.io/develop/concepts/design/dataframes) y [botón de descarga](https://docs.streamlit.io/1.57.0/develop/api-reference/widgets/st.download_button).

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

Los módulos son `app.py`, `analisis.py` y `almacenamiento.py`. La interfaz presenta catálogo, fichas y chat; análisis configura el modelo y valida resultados; almacenamiento valida el catálogo y persiste opiniones en `datos/opiniones.json`. El tema visual se configura en `.streamlit/config.toml` y los estilos en `assets/estilos.css`. Las imágenes y su procedencia están en `assets/aliens/`.

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
- Imágenes definidas: personajes de la serie con diseños de Omniverse, descargados localmente y con [procedencia documentada](assets/aliens/README.md).
- Paso 8: modelo compatible, credenciales y evaluación real.
- Paso 11: sistema operativo de entrega y mecanismo de inicio gráfico.

La configuración de IA pendiente no impide continuar con la captura de opiniones del paso 7. Si surge una duda que afecte al alcance o a las preferencias del usuario, consultarla antes de implementar lo que dependa de ella.

## Entorno de desarrollo (paso 2)

En el equipo anterior se comprobó Linux con Python 3.14.4. En esta copia se reconstruyó `.venv` con Python 3.10.12 y se instaló `requirements.txt`. Streamlit 1.67.0 exige Python 3.11 o superior; por eso requirements selecciona Streamlit 1.65.0 para Python 3.10 y conserva 1.67.0 para Python 3.11+. Las dependencias transitivas son resueltas por pip; este archivo no es un bloqueo completo de todas ellas. El código requiere Python 3.10 o superior.

| Dependencia | Versión verificada aquí (Python 3.10.12) | Versión documentada del equipo anterior |
| --- | --- | --- |
| streamlit | 1.65.0 | 1.67.0 |
| langchain-core | 1.7.6 | 1.7.6 |
| langchain-openai | 1.7.4 | 1.7.4 |
| python-dotenv | 1.2.4 | 1.2.4 |
| pydantic | 2.14.3 | 2.14.3 |
| pillow | 12.3.0 | No documentada como dependencia directa |

En VS Code, abrir la paleta y elegir **Python: Select Interpreter**, seleccionando `.venv/bin/python` en Linux. En otro equipo se debe crear un entorno nuevo e instalar `requirements.txt`; no copiar `.venv`.

Referencia técnica para reconstruir el entorno (preparación de desarrollo):

```bash
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
```

Si `venv` falla por ausencia de `ensurepip`, hace falta disponer del paquete de entornos virtuales de la distribución. En esta sesión se completó el entorno instalando pip dentro de `.venv` con el pip del sistema, sin modificar los paquetes globales.

Estos comandos documentan la preparación técnica. El uso de la entrega será visual; el acceso gráfico se construirá en el paso 11. La interfaz de desarrollo se abre siguiendo las instrucciones del paso 5 que aparecen más abajo.

`datos/` y `assets/aliens/` se conservan con `.gitkeep`. El catálogo ya está en datos/aliens.json; las opiniones JSON se crearán en su etapa. `.env.example` tiene valores vacíos; al configurar el análisis se copiará a `.env` y se completará localmente. No se ha creado ninguna clave ni realizado llamadas al modelo.

Verificación realizada aquí: instalación de dependencias, `.venv/bin/python -m pip check` sin incompatibilidades e importación de las bibliotecas, incluido Pillow para las imágenes. Se comprobaron también las pruebas del catálogo y de la interfaz; no se realizaron llamadas al modelo. El aislamiento con venv sigue la [guía oficial de Streamlit](https://docs.streamlit.io/get-started/installation/command-line).

## Catálogo (paso 3)

Se añadieron 20 aliens con IDs estables, nombres latinos y alias originales. La selección incluye cinco de la serie original, cinco de Fuerza Alienígena, cinco de Supremacía Alienígena y cinco de Omniverse, sin versiones supremas. En el paso 6 se completaron las rutas de las 20 imágenes locales, manteniendo los IDs y las series de introducción. `null` sigue siendo válido si falta una imagen. Ver [contrato de datos y fuentes](datos/README.md).

## Carga y validación del catálogo (paso 4)

`almacenamiento.cargar_aliens()` devuelve la lista de aliens validada. Comprueba la versión entera 1, un mínimo de 20 registros, campos obligatorios, textos no vacíos, IDs únicos sin espacios exteriores e imágenes `null` o rutas locales relativas con `/` y sin `..`. No exige todavía que las imágenes existan. Las rutas relativas del catálogo parten de la raíz del proyecto, independientemente del directorio de inicio.

Si falta el archivo, no puede leerse, no usa UTF-8, contiene JSON dañado o incumple el esquema, lanza `ErrorCatalogo` con un mensaje en español. La lectura no crea ni modifica archivos. La interfaz muestra estos errores y no presenta el selector cuando falla el catálogo.

Comprobación técnica, desde la raíz del repositorio y sin dependencias externas:

```bash
python3 -m unittest discover -s tests -p 'test_catalogo.py' -v
```

Resultado observado con Python 3.10.12: 19 pruebas correctas, incluyendo el catálogo real, los errores previstos, la conservación de archivos inválidos y las rutas desde otro directorio. El error de permisos se simula con `unittest.mock`. Estas pruebas no verifican todavía la interfaz ni la API.

## Navegación y selección visual (paso 5)

La interfaz tiene dos secciones: **Analizar opinión** permite seleccionar cualquiera de los 20 aliens y muestra su ficha; **Consultar archivo** informa que la consulta de opiniones sigue pendiente. La selección se conserva al cambiar de sección. No hay todavía envío de opiniones ni análisis o guardado.

El tema nativo de Streamlit usa fondo oscuro, texto claro y acento verde. La portada tiene un emblema decorativo hecho con CSS y una distribución adaptable a pantallas pequeñas. La presentación usa imágenes locales, sin descargar recursos durante su uso.

La identidad visual se refinó por petición del usuario: negro predominante (`#050705`), verde neón (`#8CFF38`) y blanco para texto y detalles. La portada incluye degradado, cuadrícula y un núcleo Omnitrix con una órbita decorativa de movimiento lento. La navegación resalta la sección activa y las fichas enmarcan la imagen con iluminación verde. Los avisos informativos siguen la paleta; los errores conservan su color semántico. La animación se desactiva cuando el dispositivo solicita movimiento reducido. Todo se dibuja con CSS local.

Verificación del rediseño: 28 pruebas existentes correctas y revisión en Chrome a 1440 y 390 píxeles, con navegación, imagen local, ausencia de desbordamiento horizontal y movimiento reducido comprobados. No se añadieron funciones de opiniones. Si Streamlit ya estaba ejecutándose al cambiar el tema, reiniciarlo y recargar el navegador para comprobar la nueva configuración.

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

## Fichas e imágenes locales (paso 6)

Cada selección actualiza nombre latino, nombre original, serie de introducción, habilidades e imagen. Los textos se leen del catálogo; no se generan con IA. Los 20 PNG son diseños de Omniverse de los personajes de la continuidad clásica, según la preferencia confirmada del usuario. La ficha distingue el diseño mostrado de la serie en la que debutó el alien.

Las imágenes proceden de la [galería comunitaria Ben 10 DB](https://ben10db.weebly.com/omniverse.html). Ver [créditos, correspondencia y límites](assets/aliens/README.md) y [manifiesto de fuentes](assets/aliens/fuentes.json), con URL exacta, fecha, dimensiones y hash de cada archivo. No se generaron imágenes con IA ni se modificaron los PNG descargados; algunas fuentes tienen resolución pequeña.

`cargar_imagen_local` lee y comprueba las imágenes mediante Pillow. Si la ruta es `null`, el archivo falta, está dañado o no se puede leer, la ficha usa `assets/aliens/sin_imagen.svg` con la etiqueta «Imagen no disponible». Si tampoco puede leerse ese recurso, muestra un aviso de texto y conserva los datos y el selector. Las imágenes se ajustan visualmente conservando su proporción.

Verificación del paso 6: 28 pruebas correctas, incluidos los 20 cambios de ficha e imagen, fallos de imagen y su alternativa, integridad y procedencia de los recursos y funcionamiento sin peticiones HTTP externas. `pip check` correcto. En Chrome se comprobó la carga del PNG desde el servidor local, HTTP 200 y navegación a 1440/390 píxeles sin desbordamiento horizontal. El envío, clasificación y guardado de opiniones corresponden a las siguientes etapas.
