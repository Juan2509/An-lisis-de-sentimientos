# Archivo Omnitrix

Proyecto académico de análisis de opiniones sobre aliens de **Ben 10**, adaptado del taller de percepción de futbolistas. Según lo comunicado por el estudiante, en clase se permitió cambiar la temática conservando los requisitos técnicos.

## Estado

Pasos 1 a 3 completados: alcance documentado, estructura inicial, entorno aislado, dependencias verificadas y catálogo de 20 aliens. La interfaz y las funciones de la aplicación todavía están pendientes. Este README se ampliará al implementar cada etapa.

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

Los módulos previstos son `app.py`, `analisis.py` y `almacenamiento.py`, acompañados por `datos/aliens.json`, `datos/opiniones.json` y recursos en `assets/aliens/`. Aún no están implementados.

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

Estas decisiones no impiden preparar la estructura del proyecto en el paso 2. Si surge una duda que afecte al alcance o a las preferencias del usuario, consultarla antes de implementar lo que dependa de ella.

## Entorno de desarrollo (paso 2)

Comprobado en Linux con Python 3.14.4. Se creó `.venv` en la raíz y se fijaron las cinco dependencias directas en `requirements.txt`. Las dependencias transitivas son resueltas por pip; este archivo no es un bloqueo completo de todas ellas.

| Dependencia | Versión verificada |
| --- | --- |
| streamlit | 1.67.0 |
| langchain-core | 1.7.6 |
| langchain-openai | 1.7.4 |
| python-dotenv | 1.2.4 |
| pydantic | 2.14.3 |

En VS Code, abrir la paleta y elegir **Python: Select Interpreter**, seleccionando `.venv/bin/python` en Linux. En otro equipo se debe crear un entorno nuevo e instalar `requirements.txt`; no copiar `.venv`.

Referencia técnica para reconstruir el entorno (preparación de desarrollo):

```bash
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
```

Estos comandos documentan la preparación técnica. El uso de la entrega será visual; el acceso gráfico se construirá en el paso 11. Ejecutar `app.py` ahora no ofrece una aplicación: los tres módulos contienen únicamente descripciones de su responsabilidad.

`datos/` y `assets/aliens/` se conservan con `.gitkeep`. El catálogo ya está en datos/aliens.json; las opiniones JSON se crearán en su etapa. `.env.example` tiene valores vacíos; al configurar el análisis se copiará a `.env` y se completará localmente. No se ha creado ninguna clave ni realizado llamadas al modelo.

Verificación realizada: instalación de dependencias, `pip check` e importación de las cinco bibliotecas. Esto comprueba el entorno, no el funcionamiento de una aplicación ni una llamada de API. El aislamiento con venv sigue la [guía oficial de Streamlit](https://docs.streamlit.io/get-started/installation/command-line).

## Catálogo (paso 3)

Se añadieron 20 aliens con IDs estables, nombres latinos y alias originales. La selección incluye cinco de la serie original, cinco de Fuerza Alienígena, cinco de Supremacía Alienígena y cinco de Omniverse, sin versiones supremas. Las imágenes están pendientes y se representan con `null`. Ver [contrato de datos y fuentes](datos/README.md). La carga y validación desde la aplicación corresponden al paso 4.
