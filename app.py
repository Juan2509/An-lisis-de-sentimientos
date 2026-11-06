"""Navegación, selección y fichas de Archivo Omnitrix."""

import streamlit as st
from PIL import Image

from almacenamiento import ErrorCatalogo, RAIZ_PROYECTO, cargar_aliens


def cargar_imagen_local(ruta: str | None) -> Image.Image | None:
    """Lee una imagen del proyecto; un recurso ausente o dañado admite alternativa."""
    if ruta is None:
        return None
    try:
        archivo = (RAIZ_PROYECTO / ruta).resolve()
        if not archivo.is_relative_to(RAIZ_PROYECTO):
            return None
        with Image.open(archivo) as imagen:
            imagen.load()
            return imagen.copy()
    except (OSError, ValueError, RuntimeError, Image.DecompressionBombError):
        return None


def mostrar_ficha(alien: dict):
    """Presenta datos del catálogo e imagen local, sin consultar modelos ni la red."""
    with st.container(border=True, key="ficha_alien"):
        st.caption("ALIEN SELECCIONADO")
        st.subheader(alien["nombre"])
        columna_imagen, columna_datos = st.columns([1, 1.4], gap="large")
        with columna_imagen:
            with st.container(key="imagen_alien"):
                imagen = cargar_imagen_local(alien["imagen"])
                if imagen is not None:
                    st.image(imagen, caption=f"Imagen de {alien['nombre']}", width="stretch")
                    st.caption(
                        "Diseño de Omniverse · "
                        "[Fuente](https://ben10db.weebly.com/omniverse.html)"
                    )
                else:
                    try:
                        alternativa = (RAIZ_PROYECTO / "assets/aliens/sin_imagen.svg").read_text(
                            encoding="utf-8"
                        )
                    except (OSError, UnicodeError):
                        st.info("Imagen no disponible.")
                    else:
                        st.image(alternativa, caption="Imagen no disponible", width="stretch")
        with columna_datos, st.container(key="datos_alien"):
            st.caption("SERIE DE INTRODUCCIÓN")
            st.text(alien["serie_origen"])
            st.caption("NOMBRE ORIGINAL")
            st.text(alien["nombre_original"])
            st.markdown("**Habilidades**")
            st.write(alien["descripcion"])


def conservar_seleccion():
    """Conserva el ID aunque el selector deje de mostrarse al navegar."""
    st.session_state["alien_id"] = st.session_state["selector_alien"]


def main():
    st.set_page_config(page_title="Archivo Omnitrix", page_icon="🟢", layout="wide")
    estilos = (RAIZ_PROYECTO / "assets" / "estilos.css").read_text(encoding="utf-8")
    st.markdown(f"<style>{estilos}</style>", unsafe_allow_html=True)

    with st.sidebar:
        st.markdown(
            '<div class="omnitrix-marca"><span aria-hidden="true">⌬</span>'
            '<div>ARCHIVO<strong>OMNITRIX</strong></div></div>',
            unsafe_allow_html=True,
        )
        st.caption("Tu conexión con el universo Ben 10.")
        st.divider()
        seccion = st.radio(
            "Secciones",
            ("Analizar opinión", "Consultar archivo"),
            key="seccion",
        )
        st.divider()
        st.caption("Versión en desarrollo · Catálogo y fichas disponibles.")

    st.title("Archivo Omnitrix")
    st.caption("Explora las transformaciones de Ben 10.")

    if seccion == "Consultar archivo":
        st.header("Consultar archivo")
        st.info(
            "La consulta de opiniones estará disponible en una próxima etapa. "
            "Todavía no se pueden guardar, filtrar ni descargar opiniones."
        )
        return

    st.markdown(
        """
        <div class="omnitrix-portada">
            <div class="omnitrix-portada-texto">
                <p class="omnitrix-etiqueta">EL ARCHIVO DE LAS TRANSFORMACIONES</p>
                <p class="omnitrix-lema">El universo está<br><span>en tus manos.</span></p>
                <p class="omnitrix-invitacion">Descubre sus habilidades. Encuentra tu transformación.</p>
            </div>
            <div class="omnitrix-nucleo" aria-hidden="true">
                <div class="omnitrix-orbita"></div>
                <div class="omnitrix-emblema"><span></span></div>
                <span class="omnitrix-cruz omnitrix-cruz-superior">+</span>
                <span class="omnitrix-cruz omnitrix-cruz-inferior">+</span>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.header("Analizar opinión")

    try:
        aliens = cargar_aliens()
    except ErrorCatalogo as error:
        st.error(f"No se pudo mostrar el catálogo. {error}")
        st.info("Revisa el archivo del catálogo antes de seleccionar una transformación.")
        st.stop()

    catalogo = {alien["id"]: alien for alien in aliens}
    ids = list(catalogo)
    if st.session_state.get("alien_id") not in catalogo:
        st.session_state["alien_id"] = ids[0]

    st.caption(
        f"{len(aliens)} transformaciones · "
        f"{len({alien['serie_origen'] for alien in aliens})} series"
    )
    alien_id = st.selectbox(
        "Selecciona un alien",
        options=ids,
        index=ids.index(st.session_state["alien_id"]),
        format_func=lambda identificador: catalogo[identificador]["nombre"],
        key="selector_alien",
        on_change=conservar_seleccion,
    )
    alien = catalogo[alien_id]

    mostrar_ficha(alien)

    st.info(
        "Puedes explorar las fichas de los aliens. "
        "El envío y análisis de opiniones estarán disponibles en próximas etapas."
    )


if __name__ == "__main__":
    main()
