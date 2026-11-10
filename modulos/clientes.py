import streamlit as st
from config.conexion import obtener_conexion


def cargar_clientes():
    conexion = obtener_conexion()
    if conexion is None:
        return [], []
    cursor = None
    try:
        cursor = conexion.cursor()
        cursor.execute(
            "SELECT Id_Cliente, Nombre, Telefono, Correo "
            "FROM CLIENTES ORDER BY Id_Cliente DESC"
        )
        filas = cursor.fetchall()
        columnas = [col[0] for col in cursor.description]
        return filas, columnas
    except Exception as error:
        st.error(f"Error al consultar los clientes: {error}")
        return [], []
    finally:
        if cursor is not None:
            cursor.close()
        if conexion.is_connected():
            conexion.close()


def guardar_cliente(nombre, telefono, correo):
    conexion = None
    cursor = None
    try:
        conexion = obtener_conexion()
        if conexion is None:
            return
        cursor = conexion.cursor()
        cursor.execute(
            "INSERT INTO CLIENTES (Nombre, Telefono, Correo) "
            "VALUES (%s, %s, %s)",
            (nombre, telefono, correo)
        )
        conexion.commit()
        st.success("Cliente registrado correctamente.")
    except Exception as error:
        if conexion is not None:
            conexion.rollback()
        st.error(f"Error al registrar el cliente: {error}")
    finally:
        if cursor is not None:
            cursor.close()
        if conexion is not None and conexion.is_connected():
            conexion.close()


def mostrar_clientes():
    st.header("Clientes")

    with st.form("form_cliente"):
        nombre = st.text_input("Nombre del cliente")
        telefono = st.text_input("Teléfono")
        correo = st.text_input("Correo")
        guardar = st.form_submit_button("Guardar cliente")

        if guardar:
            if nombre.strip() == "":
                st.warning("Debe ingresar el nombre del cliente.")
            else:
                guardar_cliente(nombre, telefono, correo)

    st.subheader("Listado de clientes")
    filas, columnas = cargar_clientes()
    if filas:
        st.dataframe(
            [dict(zip(columnas, fila)) for fila in filas],
            use_container_width=True
        )
    else:
        st.info("Aún no hay clientes registrados.")
