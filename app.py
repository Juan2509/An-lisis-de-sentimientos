"""Navegación y selección visual de Archivo Omnitrix."""

import streamlit as st

from almacenamiento import ErrorCatalogo, RAIZ_PROYECTO, cargar_aliens


def conservar_seleccion():
    """Conserva el ID aunque el selector deje de mostrarse al navegar."""
    st.session_state["alien_id"] = st.session_state["selector_alien"]


def main():
    st.set_page_config(page_title="Archivo Omnitrix", page_icon="🟢", layout="wide")
    estilos = (RAIZ_PROYECTO / "assets" / "estilos.css").read_text(encoding="utf-8")
    st.markdown(f"<style>{estilos}</style>", unsafe_allow_html=True)

    with st.sidebar:
        st.markdown("### ARCHIVO :green[OMNITRIX]")
        st.caption("Un universo de transformaciones.")
        st.divider()
        seccion = st.radio(
            "Secciones",
            ("Analizar opinión", "Consultar archivo"),
            key="seccion",
        )
        st.divider()
        st.caption("Versión en desarrollo · Catálogo y selección disponibles.")

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
            <div class="omnitrix-emblema" aria-hidden="true"><span></span></div>
            <div>
                <p class="omnitrix-etiqueta">CATÁLOGO DE TRANSFORMACIONES</p>
                <p class="omnitrix-lema">Cada transformación tiene una historia.</p>
                <p class="omnitrix-invitacion">Elige cuál explorar.</p>
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

    with st.container(border=True):
        st.caption("ALIEN SELECCIONADO")
        st.subheader(alien["nombre"])
        st.text(alien["serie_origen"])

    st.info(
        "Por ahora puedes explorar la selección del catálogo. "
        "Las fichas con imágenes y el envío de opiniones estarán disponibles "
        "en próximas etapas."
    )


if __name__ == "__main__":
    main()
