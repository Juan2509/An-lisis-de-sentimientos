"""Persistencia real en archivos temporales, sin dependencias externas ni API."""

from copy import deepcopy
from pathlib import Path
import json
import tempfile
import unittest
from unittest.mock import patch

from almacenamiento import ErrorOpiniones, cargar_opiniones, crear_registro, guardar_opinion


class PruebasOpiniones(unittest.TestCase):
    def setUp(self):
        temporal = tempfile.TemporaryDirectory()
        self.addCleanup(temporal.cleanup)
        self.ruta = Path(temporal.name) / "opiniones.json"
        self.registro = crear_registro(
            {"id": "a001", "nombre": "Fuego"}, "  Me encanta su diseño.  ",
            {"es_pertinente": True, "sentimiento": "positivo", "razon": "Expresa agrado."},
            "modelo-prueba", "omnitrix-v1",
        )

    def test_creacion_lectura_nueva_e_idempotencia(self):
        self.assertEqual(cargar_opiniones(self.ruta), [])
        self.assertFalse(self.ruta.exists())
        self.assertTrue(guardar_opinion(self.ruta, self.registro))
        antes = self.ruta.read_bytes()
        self.assertFalse(guardar_opinion(self.ruta, deepcopy(self.registro)))
        self.assertEqual(self.ruta.read_bytes(), antes)
        self.assertEqual(cargar_opiniones(Path(str(self.ruta))), [self.registro])
        self.assertIn("diseño", self.ruta.read_text(encoding="utf-8"))

    def test_envios_iguales_independientes_y_conflicto_de_id(self):
        guardar_opinion(self.ruta, self.registro)
        otro = crear_registro(
            {"id": "a001", "nombre": "Fuego"}, self.registro["opinion_original"],
            {"es_pertinente": True, "sentimiento": "positivo", "razon": "Expresa agrado."},
            "modelo-prueba", "omnitrix-v1",
        )
        guardar_opinion(self.ruta, otro)
        self.assertEqual(len(cargar_opiniones(self.ruta)), 2)
        contenido = self.ruta.read_bytes()
        with self.assertRaises(ErrorOpiniones):
            guardar_opinion(self.ruta, {**self.registro, "alien_id": "a002"})
        self.assertEqual(self.ruta.read_bytes(), contenido)

    def test_archivos_danados_se_conservan(self):
        for contenido in (b"\xff", b"{", b"[]", b'{"version": true, "opiniones": []}',
                          b'{"version": 2, "opiniones": []}'):
            with self.subTest(contenido=contenido):
                self.ruta.write_bytes(contenido)
                with self.assertRaises(ErrorOpiniones):
                    guardar_opinion(self.ruta, self.registro)
                self.assertEqual(self.ruta.read_bytes(), contenido)

    def test_registros_invalidos_y_duplicados_se_rechazan(self):
        for cambio in ({"id": "invalido"}, {"fecha_utc": "2026-11-07T12:00:00"},
                       {"sentimiento": "otro"}, {"razon": " "}, {"razon": "x" * 301},
                       {"opinion_original": "abcd"}, {"modelo": None}):
            with self.subTest(cambio=cambio), self.assertRaises(ErrorOpiniones):
                guardar_opinion(self.ruta, {**self.registro, **cambio})
        self.ruta.write_text(json.dumps({"version": 1, "opiniones": [self.registro] * 2}), encoding="utf-8")
        with self.assertRaisesRegex(ErrorOpiniones, "repetidos"):
            cargar_opiniones(self.ruta)

    def test_fallo_de_reemplazo_conserva_archivo_y_limpia_temporal(self):
        guardar_opinion(self.ruta, self.registro)
        antes = self.ruta.read_bytes()
        otro = {**self.registro, "id": "d1ba4e34-fd25-40e7-a293-317b40dbd159"}
        with patch("almacenamiento.os.replace", side_effect=PermissionError):
            with self.assertRaises(ErrorOpiniones):
                guardar_opinion(self.ruta, otro)
        self.assertEqual(self.ruta.read_bytes(), antes)
        self.assertEqual(list(self.ruta.parent.iterdir()), [self.ruta])

    def test_fallo_de_escritura_no_crea_destino_y_limpia_temporal(self):
        with patch("almacenamiento.os.fsync", side_effect=OSError):
            with self.assertRaises(ErrorOpiniones):
                guardar_opinion(self.ruta, self.registro)
        self.assertFalse(self.ruta.exists())
        self.assertEqual(list(self.ruta.parent.iterdir()), [])

    def test_rechaza_analisis_no_pertinente(self):
        with self.assertRaises(ErrorOpiniones):
            crear_registro({"id": "a001", "nombre": "Fuego"}, "Hoy llueve.",
                           {"es_pertinente": False, "sentimiento": None, "razon": "Texto ajeno."},
                           "modelo", "v1")


if __name__ == "__main__":
    unittest.main()
