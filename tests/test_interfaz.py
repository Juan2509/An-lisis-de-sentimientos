"""Pruebas de interacción con el motor de pruebas de Streamlit."""

from copy import deepcopy
from hashlib import sha256
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from PIL import Image
from streamlit.testing.v1 import AppTest

from almacenamiento import ErrorCatalogo, ErrorOpiniones, RAIZ_PROYECTO, cargar_aliens, cargar_opiniones
from analisis import ErrorAnalisis


class PruebasInterfaz(unittest.TestCase):
    def setUp(self):
        temporal = tempfile.TemporaryDirectory()
        self.addCleanup(temporal.cleanup)
        self.ruta_opiniones = Path(temporal.name) / "opiniones.json"
        parche_ruta = patch("almacenamiento.RUTA_OPINIONES", self.ruta_opiniones)
        parche_ruta.start()
        self.addCleanup(parche_ruta.stop)
        self.resultado = {
            "analisis": {"es_pertinente": True, "sentimiento": "positivo", "razon": "Expresa agrado."},
            "modelo": "modelo-de-prueba", "version_prompt": "prueba",
        }
        parche = patch("analisis.analizar_opinion", return_value=self.resultado)
        self.analizar = parche.start()
        self.addCleanup(parche.stop)

    def iniciar(self):
        app = AppTest.from_file(str(RAIZ_PROYECTO / "app.py"), default_timeout=15)
        app.run()
        self.assertFalse(app.exception)
        return app

    def test_inicio_muestra_catalogo_y_funciones_pendientes(self):
        app = self.iniciar()
        self.assertEqual(app.title[0].value, "Archivo Omnitrix")
        self.assertEqual(app.radio[0].value, "Analizar opinión")
        self.assertEqual(len(app.selectbox[0].options), 20)
        self.assertEqual(app.subheader[0].value, "Fuego")
        self.assertIn("archivo local", app.info[0].value)
        self.assertEqual(len(app.chat_input), 1)

    def test_opiniones_conservan_alien_texto_y_no_se_duplican_al_navegar(self):
        app = self.iniciar()
        texto = "  Me encanta su diseño.  "
        app.chat_input[0].set_value(texto).run()
        app.selectbox[0].select("a002").run()
        app.chat_input[0].set_value("Sus cristales son increíbles.").run()
        app.radio[0].set_value("Consultar archivo").run()
        app.radio[0].set_value("Analizar opinión").run()
        self.assertFalse(app.exception)
        historial = app.session_state["opiniones_sesion"]
        self.assertEqual(len(historial), 2)
        self.assertEqual({campo: historial[0][campo] for campo in (
            "alien_id", "alien_nombre", "opinion_original",
        )}, {
            "alien_id": "a001", "alien_nombre": "Fuego", "opinion_original": texto,
        })
        self.assertEqual(historial[1]["alien_id"], "a002")
        self.assertEqual(len(app.chat_message), 4)
        self.assertEqual(self.analizar.call_count, 2)
        self.assertEqual(self.analizar.call_args_list[0].args[0]["id"], "a001")
        self.assertEqual(self.analizar.call_args_list[0].args[1], texto)

    def test_longitud_se_valida_sin_truncar_y_conserva_texto_rechazado(self):
        app = self.iniciar()
        for texto in ("   ", "abcd", "x" * 1001):
            with self.subTest(longitud=len(texto)):
                app.chat_input[0].set_value(texto).run()
                self.assertFalse(app.exception)
                self.assertTrue(app.error)
                self.assertEqual(app.session_state["opiniones_sesion"], [])
                self.analizar.assert_not_called()
                self.assertIn(texto, [elemento.value for elemento in app.text])
        for texto in ("  abcde  ", "x" * 1000):
            app.chat_input[0].set_value(texto).run()
            self.assertFalse(app.error)
        self.assertEqual(len(app.session_state["opiniones_sesion"]), 2)

    def test_envios_identicos_independientes_y_limpieza_sin_escritura(self):
        app = self.iniciar()
        ruta = self.ruta_opiniones
        for _ in range(2):
            app.chat_input[0].set_value("Me gusta su diseño.").run()
        self.assertEqual(len(app.session_state["opiniones_sesion"]), 2)
        registros = cargar_opiniones(ruta)
        self.assertEqual(len(registros), 2)
        self.assertNotEqual(registros[0]["id"], registros[1]["id"])
        anterior = ruta.read_bytes()
        app.selectbox[0].select("a003").run()
        app.chat_input[0].set_value("mal").run()
        app.button(key="nueva_conversacion").click().run()
        self.assertFalse(app.exception)
        self.assertFalse(app.chat_message)
        self.assertFalse(app.error)
        self.assertEqual(app.selectbox[0].value, "a003")
        self.assertEqual(app.session_state["opiniones_sesion"], [])
        self.assertEqual(ruta.read_bytes() if ruta.exists() else None, anterior)

    def test_error_de_analisis_conserva_comentario_sin_reintento_al_navegar(self):
        self.analizar.side_effect = ErrorAnalisis("No se pudo obtener un análisis válido.")
        app = self.iniciar()
        app.chat_input[0].set_value("Me gusta Fuego.").run()
        app.selectbox[0].select("a002").run()
        self.assertFalse(app.exception)
        self.assertIn("análisis válido", app.error[0].value)
        opinion = app.session_state["opiniones_sesion"][0]
        self.assertEqual(opinion["opinion_original"], "Me gusta Fuego.")
        self.assertNotIn("analisis", opinion)
        self.assertEqual(self.analizar.call_count, 1)
        self.assertFalse(self.ruta_opiniones.exists())

    def test_opinion_ajena_se_muestra_sin_categoria(self):
        self.analizar.return_value = {
            **self.resultado,
            "analisis": {"es_pertinente": False, "sentimiento": None, "razon": "Habla del clima."},
        }
        app = self.iniciar()
        app.chat_input[0].set_value("Hoy está lloviendo.").run()
        self.assertFalse(app.exception)
        self.assertIn("no pertinente", app.warning[0].value)
        self.assertFalse(any("Sentimiento:" in m.value for m in app.markdown))
        self.assertFalse(self.ruta_opiniones.exists())

    def test_reintentar_guardado_conserva_id_y_no_repite_analisis(self):
        app = self.iniciar()
        with patch("almacenamiento.guardar_opinion", side_effect=ErrorOpiniones("Error de escritura")):
            app.chat_input[0].set_value("Me encanta Fuego.").run()
        self.assertFalse(app.exception)
        self.assertFalse(app.success)
        self.assertIn("Error de escritura", app.error[0].value)
        registro = dict(app.session_state["opiniones_sesion"][0]["registro"])
        app.selectbox[0].select("a002").run()
        app.button(key=f"guardar_{registro['id']}").click().run()
        self.assertFalse(app.error)
        self.assertEqual(len(app.success), 1)
        self.assertEqual(cargar_opiniones(self.ruta_opiniones), [registro])
        self.assertEqual(self.analizar.call_count, 1)

    def test_seleccion_de_todos_los_aliens(self):
        app = self.iniciar()
        for alien in cargar_aliens():
            with self.subTest(alien=alien["id"]):
                app.selectbox[0].select(alien["id"]).run()
                self.assertFalse(app.exception)
                self.assertEqual(app.subheader[0].value, alien["nombre"])
                self.assertEqual(app.text[0].value, alien["serie_origen"])
                self.assertEqual(app.text[1].value, alien["nombre_original"])
                self.assertIn(alien["descripcion"], [m.value for m in app.markdown])
                self.assertEqual(
                    app.get("image")[0].proto.imgs[0].caption,
                    f"Imagen de {alien['nombre']}",
                )

    def test_imagen_ausente_o_danada_muestra_alternativa_y_permite_cambiar(self):
        with tempfile.TemporaryDirectory(dir=RAIZ_PROYECTO) as carpeta:
            danada = Path(carpeta) / "danada.png"
            danada.write_bytes(b"archivo que no es una imagen")
            for ruta in (None, "assets/aliens/no-existe.png", str(danada.relative_to(RAIZ_PROYECTO))):
                with self.subTest(ruta=ruta):
                    datos = deepcopy(cargar_aliens())
                    datos[0]["imagen"] = ruta
                    with patch("almacenamiento.cargar_aliens", return_value=datos):
                        app = self.iniciar()
                        imagen = app.get("image")[0].proto.imgs[0]
                        self.assertEqual(imagen.caption, "Imagen no disponible")
                        self.assertTrue(imagen.url.startswith("data:image/svg+xml;base64,"))
                        self.assertIn(datos[0]["descripcion"], [m.value for m in app.markdown])
                        app.selectbox[0].select("a002").run()
                        self.assertFalse(app.exception)
                        self.assertEqual(app.subheader[0].value, "Diamante")

    def test_imagen_sin_permiso_no_bloquea_ficha(self):
        with patch("PIL.Image.open", side_effect=PermissionError):
            app = self.iniciar()
        self.assertEqual(app.get("image")[0].proto.imgs[0].caption, "Imagen no disponible")
        self.assertEqual(app.subheader[0].value, "Fuego")

    def test_ficha_funciona_sin_red(self):
        with patch("requests.sessions.Session.request", side_effect=AssertionError("Sin red")) as peticion:
            app = self.iniciar()
            app.selectbox[0].select("a020").run()
            peticion.assert_not_called()
        self.assertFalse(app.exception)
        self.assertEqual(app.subheader[0].value, "Escarabola")

    def test_recursos_del_catalogo_tienen_procedencia_y_archivos_validos(self):
        fuentes = json.loads((RAIZ_PROYECTO / "assets/aliens/fuentes.json").read_text(encoding="utf-8"))
        por_id = {fuente["id"]: fuente for fuente in fuentes["imagenes"]}
        self.assertEqual(set(por_id), {alien["id"] for alien in cargar_aliens()})
        for alien in cargar_aliens():
            with self.subTest(alien=alien["id"]):
                fuente = por_id[alien["id"]]
                self.assertEqual(alien["imagen"], fuente["archivo_local"])
                ruta = RAIZ_PROYECTO / alien["imagen"]
                self.assertEqual(sha256(ruta.read_bytes()).hexdigest(), fuente["sha256"])
                self.assertTrue(fuente["pagina"].startswith("https://"))
                self.assertTrue(fuente["url"].startswith("https://"))
                with Image.open(ruta) as imagen:
                    self.assertEqual(imagen.format, "PNG")
                    self.assertEqual(imagen.size, (fuente["ancho"], fuente["alto"]))
                    imagen.verify()

    def test_navegar_conserva_el_alien_seleccionado(self):
        app = self.iniciar()
        app.selectbox[0].select("a020").run()
        app.radio[0].set_value("Consultar archivo").run()
        self.assertFalse(app.exception)
        self.assertEqual(app.header[0].value, "Consultar archivo")
        self.assertIn("los filtros y la descarga siguen pendientes", app.info[0].value)
        self.assertFalse(app.selectbox)
        app.radio[0].set_value("Analizar opinión").run()
        self.assertFalse(app.exception)
        self.assertEqual(app.selectbox[0].value, "a020")
        self.assertEqual(app.subheader[0].value, "Escarabola")

    def test_error_de_catalogo_visible_y_sin_selector(self):
        for mensaje in ("No se encontró el catálogo.", "JSON inválido.", "ID repetido."):
            with self.subTest(mensaje=mensaje):
                with patch("almacenamiento.cargar_aliens", side_effect=ErrorCatalogo(mensaje)):
                    app = self.iniciar()
                self.assertIn(mensaje, app.error[0].value)
                self.assertFalse(app.selectbox)

    def test_consulta_accesible_aunque_falle_catalogo(self):
        app = self.iniciar()
        with patch("almacenamiento.cargar_aliens", side_effect=ErrorCatalogo("Error")) as cargar:
            app.radio[0].set_value("Consultar archivo").run()
            cargar.assert_not_called()
        self.assertFalse(app.exception)
        self.assertFalse(app.error)
        self.assertEqual(app.header[0].value, "Consultar archivo")


if __name__ == "__main__":
    unittest.main()
