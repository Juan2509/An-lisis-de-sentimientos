"""Pruebas de interacción con el motor de pruebas de Streamlit."""

import unittest
from unittest.mock import patch

from streamlit.testing.v1 import AppTest

from almacenamiento import ErrorCatalogo, RAIZ_PROYECTO, cargar_aliens


class PruebasInterfaz(unittest.TestCase):
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
        self.assertIn("próximas etapas", app.info[0].value)
        self.assertFalse(app.chat_input)

    def test_seleccion_de_todos_los_aliens(self):
        app = self.iniciar()
        for alien in cargar_aliens():
            with self.subTest(alien=alien["id"]):
                app.selectbox[0].select(alien["id"]).run()
                self.assertFalse(app.exception)
                self.assertEqual(app.subheader[0].value, alien["nombre"])
                self.assertEqual(app.text[0].value, alien["serie_origen"])

    def test_navegar_conserva_el_alien_seleccionado(self):
        app = self.iniciar()
        app.selectbox[0].select("a020").run()
        app.radio[0].set_value("Consultar archivo").run()
        self.assertFalse(app.exception)
        self.assertEqual(app.header[0].value, "Consultar archivo")
        self.assertIn("Todavía no se pueden guardar", app.info[0].value)
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
