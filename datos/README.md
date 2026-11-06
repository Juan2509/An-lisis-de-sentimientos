# Catálogo de Archivo Omnitrix

`aliens.json` es un catálogo didáctico versionado, no una lista exhaustiva ni un ranking. El usuario confirmó nombres en español latino y representación de las cuatro series de la continuidad clásica, excluyendo por ahora las versiones supremas. La selección distribuye los 20 registros en cinco por serie.

| IDs | Serie de introducción | Selección |
| --- | --- | --- |
| a001–a005 | Ben 10, serie original | Fuego, Diamante, XLR8, Cuatro Brazos, Materia Gris |
| a006–a010 | Fuerza Alienígena | Fuego Pantanoso, Eco Eco, Humungosaurio, Frío, Mono Araña |
| a011–a015 | Supremacía Alienígena | Amenaza Acuática, Ampfibio, Armadillo, Tortutornado, NRG |
| a016–a020 | Omniverse | Feedback, Bloxx, Gravattack, Crashhopper, Escarabola |

## Contrato de datos, versión 1

La raíz contiene `version: 1` y una lista `aliens`.

| Campo por alien | Tipo | Significado |
| --- | --- | --- |
| id | string | Identidad estable; no reutilizar ni cambiar al editar el nombre |
| nombre | string | Nombre visible en español latino; algunos se conservan en inglés en el doblaje |
| nombre_original | string | Alias original para identificación; puede coincidir con nombre |
| serie_origen | string | Serie en que la transformación fue introducida al público |
| descripcion | string | Resumen breve de habilidades, redactado para la ficha |
| imagen | string o null | Ruta local relativa a la raíz del proyecto cuando exista; null mientras esté pendiente |

La serie de origen no indica todas las series donde aparece el alien. Por ejemplo, los recuerdos de Feedback en Omniverse no lo convierten en una transformación introducida en la serie original. Un rediseño posterior del mismo alien no constituye un registro nuevo. Las formas supremas y el reboot no forman parte de esta selección.

No asignar rutas ficticias a imágenes inexistentes. La interfaz deberá admitir `null` con un recurso alternativo; las imágenes y su procedencia se resolverán en el paso 6. El catálogo no requiere llamadas al modelo.

## Referencias consultadas

Consulta: 6 de noviembre de 2026. Los nombres regionales y la pertenencia a cada serie se contrastaron en las listas de alienígenas de [Ben 10](https://es.wikipedia.org/wiki/Ben_10), [Fuerza Alienígena](https://es.wikipedia.org/wiki/Ben_10:_Alien_Force), [Supremacía Alienígena](https://es.wikipedia.org/wiki/Ben_10:_Ultimate_Alien) y [Omniverse](https://es.wikipedia.org/wiki/Ben_10:_Omniverse).

Las descripciones sintetizan habilidades generales, sin estadísticas de poder, planetas, episodios ni afirmaciones de superioridad. Referencias complementarias: [aliens originales](https://en.wikipedia.org/wiki/Ben_10_(comic_series)), [Fuego Pantanoso](https://ben10.fandom.com/wiki/Swampfire), [Eco Eco](https://ben10.fandom.com/wiki/Echo_Echo), [Frío](https://ben10.fandom.com/wiki/Big_Chill_(Classic)), [Mono Araña](https://ben10.fandom.com/wiki/Spidermonkey_(Classic)), [Amenaza Acuática](https://ben10.fandom.com/wiki/Waterhazard), [Ampfibio](https://en.wikipedia.org/wiki/Ben_10_(2016_TV_series)), [Armadillo](https://ben10.fandom.com/wiki/Armodrillo), [Tortutornado](https://cartoonnetwork.fandom.com/wiki/Terraspin), [NRG](https://ben10.fandom.com/wiki/NRG), [Feedback](https://ben10.fandom.com/wiki/Feedback), [Bloxx](https://ben10.fandom.com/wiki/Bloxx_(Classic)), [Gravattack](https://ben10.fandom.com/wiki/Gravattack), [Crashhopper](https://ben10.fandom.com/wiki/Crashhopper) y [Escarabola](https://ben10.fandom.com/wiki/Ball_Weevil).

Son referencias comunitarias, no un catálogo oficial. Algunas páginas de Fandom bloquearon la apertura directa; en esos casos se consultó el contenido indexado disponible en búsqueda. Las descripciones son síntesis propias y pueden ajustarse si se detecta una discrepancia de doblaje o contenido, conservando los IDs.

## Verificación del paso 3

Se comprobó el parseo del JSON, versión 1, 20 registros, IDs y nombres únicos, campos presentes y tipos básicos, cinco registros por serie, imágenes null y ausencia de nombres de formas supremas.

## Cargador implementado en el paso 4

`almacenamiento.cargar_aliens()` devuelve la lista de registros del catálogo, sin cambiar sus datos. Valida versión entera 1, lista de al menos 20 aliens, campos obligatorios, textos no vacíos e IDs únicos sin espacios exteriores. Acepta campos adicionales para permitir ampliar las fichas; no comprueba la exactitud del contenido sobre la serie ni exige la distribución de cinco por serie, que corresponde a la selección editorial del paso 3.

`imagen` admite `null` o una ruta local relativa a la raíz del proyecto, usando `/` y sin segmentos `..`. No admite URLs ni rutas absolutas de Linux o Windows. La existencia del recurso se comprobará al mostrar la ficha, con alternativa si falta la imagen.

Las rutas relativas del archivo de catálogo también se resuelven desde la raíz del proyecto. Los errores de archivo ausente, lectura, codificación UTF-8, JSON o esquema se comunican mediante `ErrorCatalogo`, sin crear ni sobrescribir el archivo.

Verificación del catálogo: `python3 -m unittest discover -s tests -p 'test_catalogo.py' -v`, desde la raíz del proyecto. Resultado del paso 4: 19 pruebas correctas con Python 3.10.12; sin dependencias externas ni llamadas al modelo. El fallo de permisos utiliza una simulación; los casos de archivo ausente, JSON dañado y codificación inválida usan archivos temporales reales. Las pruebas completas, incluida la interfaz del paso 5, requieren el entorno con dependencias y se ejecutan con `.venv/bin/python -m unittest discover -s tests -v`.
