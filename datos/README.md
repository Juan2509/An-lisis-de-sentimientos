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

Se comprobó el parseo del JSON, versión 1, 20 registros, IDs y nombres únicos, campos presentes y tipos básicos, cinco registros por serie, imágenes null y ausencia de nombres de formas supremas. Esta comprobación estática no implementa todavía el cargador ni su manejo de archivos inválidos: corresponden al paso 4.
