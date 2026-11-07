"""Comprobaciones del lanzador sin abrir ventanas, navegador ni Streamlit."""

import subprocess
import sys
import unittest
from unittest.mock import MagicMock, patch

from iniciar import RAIZ, comando_servidor, detener_proceso, servidor_listo


class PruebasInicio(unittest.TestCase):
    def test_comando_usa_interprete_actual_ruta_absoluta_y_red_local(self):
        comando = comando_servidor(18501)
        self.assertEqual(comando[:5], [sys.executable, "-m", "streamlit", "run", str(RAIZ / "app.py")])
        self.assertIn("--server.address=127.0.0.1", comando)
        self.assertIn("--server.port=18501", comando)
        self.assertIn("--server.headless=true", comando)

    @patch("iniciar.build_opener")
    def test_salud_exige_respuesta_de_streamlit(self, construir):
        respuesta = construir.return_value.open.return_value.__enter__.return_value
        respuesta.status = 200
        respuesta.read.return_value = b"ok"
        self.assertTrue(servidor_listo("http://127.0.0.1:18501"))
        construir.return_value.open.assert_called_with("http://127.0.0.1:18501/_stcore/health", timeout=0.3)
        respuesta.read.return_value = b"otro servidor"
        self.assertFalse(servidor_listo("http://127.0.0.1:18501"))
        construir.return_value.open.side_effect = OSError("No disponible")
        self.assertFalse(servidor_listo("http://127.0.0.1:18501"))

    def test_detener_termina_solo_el_proceso_recibido(self):
        proceso = MagicMock()
        proceso.poll.return_value = None
        detener_proceso(proceso)
        proceso.terminate.assert_called_once()
        proceso.wait.assert_called_once_with(timeout=5)
        proceso.kill.assert_not_called()

    def test_cierre_es_idempotente_si_el_proceso_ya_termino(self):
        proceso = MagicMock()
        proceso.poll.return_value = 0
        detener_proceso(proceso)
        proceso.terminate.assert_not_called()
        proceso.kill.assert_not_called()
        detener_proceso(None)

    def test_cierre_forzado_si_el_servidor_no_termina(self):
        proceso = MagicMock()
        proceso.poll.return_value = None
        proceso.wait.side_effect = [subprocess.TimeoutExpired("streamlit", 5), 0]
        detener_proceso(proceso)
        proceso.terminate.assert_called_once()
        proceso.kill.assert_called_once()


if __name__ == "__main__":
    unittest.main()
