# Imágenes del catálogo

Se incluyen 20 PNG de los personajes de la serie, seleccionados según la preferencia del usuario y descargados el 6 de noviembre de 2026 de la [galería comunitaria Ben 10 DB: Omniverse](https://ben10db.weebly.com/omniverse.html). Son diseños de Omniverse de las transformaciones de la continuidad clásica, sin formas supremas ni personajes del reboot. La ficha señala el diseño mostrado; `serie_origen` mantiene la serie de introducción del alien, que puede ser anterior a Omniverse.

Los archivos se guardaron tal como los entrega la fuente, sin generación con IA, recortes ni cambios de color o resolución. La aplicación limita su tamaño de presentación conservando la proporción. Algunas imágenes de la fuente son pequeñas (por ejemplo, Eco Eco y Crashhopper), por lo que su nitidez es menor. Se verificaron su formato PNG, dimensiones, correspondencia visual con el personaje e integridad.

Los personajes y diseños de Ben 10 pertenecen a sus respectivos titulares, entre ellos Cartoon Network. La galería es una fuente comunitaria y no acredita por sí sola una licencia de redistribución ni la autoría de cada render. Estos recursos se documentan como material de terceros para el proyecto académico, sin atribuirles licencia libre ni autoría propia. El SVG alternativo es una composición vectorial creada para esta aplicación, inspirada en su identidad visual.

## Correspondencia

| Archivo | Alien | Diseño |
| --- | --- | --- |
| a001.png | Fuego | Omniverse |
| a002.png | Diamante | Omniverse |
| a003.png | XLR8 | Omniverse |
| a004.png | Cuatro Brazos | Omniverse |
| a005.png | Materia Gris | Omniverse |
| a006.png | Fuego Pantanoso | Omniverse, diseño previo a su floración |
| a007.png | Eco Eco | Omniverse |
| a008.png | Humungosaurio | Omniverse |
| a009.png | Frío | Omniverse |
| a010.png | Mono Araña | Omniverse |
| a011.png | Amenaza Acuática | Omniverse |
| a012.png | Ampfibio | Omniverse |
| a013.png | Armadillo | Omniverse |
| a014.png | Tortutornado | Omniverse |
| a015.png | NRG | Omniverse, con traje de contención |
| a016.png | Feedback | Omniverse, Ben adolescente |
| a017.png | Bloxx | Omniverse |
| a018.png | Gravattack | Omniverse |
| a019.png | Crashhopper | Omniverse |
| a020.png | Escarabola | Omniverse |

El manifiesto [fuentes.json](fuentes.json) conserva para cada ID la página de procedencia, URL exacta de descarga, nombre del archivo fuente, fecha, dimensiones y SHA-256 del PNG local. Es documentación y evidencia de procedencia; la aplicación no consulta esas URLs ni necesita leer el manifiesto para mostrar las imágenes.

## Alternativa local

`sin_imagen.svg` es el recurso alternativo compartido. Se muestra con la etiqueta «Imagen no disponible» si `imagen` es `null`, el archivo falta, está dañado o no puede leerse. Si tampoco puede leerse el SVG, se conserva la ficha y aparece un aviso de texto. Ninguno de estos casos cambia el ID ni elimina los datos del alien.

Las rutas del catálogo parten de la raíz del proyecto, por ejemplo `assets/aliens/a001.png`. Para sustituir una imagen, conservar el ID, actualizar la ruta si cambia y registrar su procedencia y hash en el manifiesto. No asignar al catálogo enlaces remotos o rutas a imágenes inexistentes.

Se exploró también la API pública de Ben 10 Wiki/Fandom, pero su CDN devolvió HTTP 403 al intentar descargar los archivos. Ninguna de las imágenes entregadas se descargó desde ese CDN.
