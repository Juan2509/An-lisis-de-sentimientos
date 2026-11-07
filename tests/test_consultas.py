"""Filtros puros sobre opiniones ficticias; sin API ni dependencias externas."""

from copy import deepcopy
import unittest

from almacenamiento import ErrorOpiniones, consultar_opiniones


class PruebasConsultas(unittest.TestCase):
    def setUp(self):
        # Estos datos solo prueban filtros, no representan análisis de un modelo.
        self.registros = [
            {"alien_id": alien, "alien_nombre": "Nombre compartido", "sentimiento": categoria}
            for alien in ("a001", "a002")
            for categoria in ("positivo", "negativo", "neutro", "mixto")
        ]

    def test_combinaciones_de_filtros_conservan_orden_y_usan_ids(self):
        for alien_id in (None, "a001", "a002", "inexistente"):
            for sentimiento in (None, "positivo", "negativo", "neutro", "mixto"):
                with self.subTest(alien_id=alien_id, sentimiento=sentimiento):
                    resultado = consultar_opiniones(self.registros, alien_id, sentimiento)
                    cantidad = (2 if alien_id is None else 0 if alien_id == "inexistente" else 1) * (4 if sentimiento is None else 1)
                    self.assertEqual(len(resultado), cantidad)
                    self.assertTrue(all(alien_id is None or r["alien_id"] == alien_id for r in resultado))
                    self.assertTrue(all(sentimiento is None or r["sentimiento"] == sentimiento for r in resultado))
        self.assertEqual(consultar_opiniones(self.registros), self.registros)

    def test_no_modifica_entrada_y_devuelve_copias(self):
        anterior = deepcopy(self.registros)
        resultado = consultar_opiniones(self.registros)
        resultado[0]["alien_nombre"] = "Otro nombre"
        resultado.pop()
        self.assertEqual(self.registros, anterior)

    def test_lista_vacia_y_categoria_invalida(self):
        self.assertEqual(consultar_opiniones([], "a001", "positivo"), [])
        with self.assertRaises(ErrorOpiniones):
            consultar_opiniones(self.registros, sentimiento="desconocido")


if __name__ == "__main__":
    unittest.main()
