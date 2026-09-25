import sqlite3

from pyfiglet import figlet_format
from rich.console import Console
from rich.panel import Panel
from rich.style import Style
from rich.table import Table

import sys

import database as db

console = Console()

error_style = Style(color="red", bold=True, blink=True)
check_style = Style(color="green", blink=True)






def menu_empleado_ascci():
    """
    Muestra el titulo del menu al que hace referencia utilizando pyfiglet

    Toma el texto a utilizar y con pyfiglet lo hace en arte ascci estandar.

    Args:
        No requiere argumentos.

    Returns:
        None.

    Raises:
        Puede dar error al no encontrar la libreria correspondiente

    Examples:
        convierte MENU a ASCCI
    """
    try:
        print(figlet_format("MENU  DE", font="standard"))
        print(figlet_format("EMPLEADO", font="standard"))
    except Exception as e:
        console.print(
            f"Error al generar el título ASCII: {e}", style=error_style
        )


def opciones_empleado():
    """
    Abre el menú utilizando rich para abrir el menú.

    Toma las opciones y con ayuda de panel puede crear el menú de manera ordenada.

    Args:
        No requiere argumentos

    Returns:
        None.

    Raises:
        Puede dar error al no encontrar la libreria correspondiente

    Examples:
        Abre el menu de opciones para el empleado con rich panel.
    """
    try:
        console.print(
            Panel(
                "[bold white]1. Ingresar Libro\n2. Modificar Libro\n3. Borrar Libro\n4. Ver Inventario\n5. Ver Solicitudes de Prestamos\n6. Salir[/bold white]",
                title="OPCIONES",
                border_style="cyan",
                expand=False,
            )
        )
    except Exception as e:
        console.print(f"Error al mostrar el menú: {e}", style=error_style)


def ver_inventario(conexion):
    """
    Abre el inventario y lo imprime en una tabla con rich.

    Toma los datos de la base de datos y con ayuda de rich puede crear una tabla para mostrar el inventario.

    Args:
        conexion: Requiere conexion a la base de datos para poder obtener los datos del inventario.

    Returns:
        None.

    Raises:
        Puede dar error al no encontrar la libreria correspondiente o al no poder conectarse a la base de datos.

    Examples:
        Abre el inventario de libros y lo muestra en una tabla con rich.
    """
    try:
        cursor = conexion.execute(
            "SELECT id, titulo, autor, ejemplares FROM libros ORDER BY id"
        )
        filas = cursor.fetchall()

        if not filas:
            console.print("No hay libros registrados.", style=error_style)
        else:
            tabla = Table(
                title="[bold white]Inventario de Libros[/bold white]"
            )
            tabla.add_column("ID", justify="center", style="green")
            tabla.add_column("Título", justify="center", style="blue")
            tabla.add_column("Autor", justify="center", style="magenta")
            tabla.add_column("Ejemplares", justify="center", style="yellow")

            for fila in filas:
                id_libro = f"{int(fila['id']):04d}"
                tabla.add_row(
                    id_libro,
                    str(fila["titulo"]),
                    str(fila["autor"]),
                    str(fila["ejemplares"]),
                )
            console.print(tabla)
    except sqlite3.Error as e:
        console.print(
            f"Error de base de datos al consultar el inventario: {e}",
            style=error_style,
        )
    except Exception as e:
        console.print(
            f"Error inesperado al ver inventario: {e}", style=error_style
        )


def insertar_libro(conexion):
    """
    Permite al empleado ingresar un nuevo libro al inventario.

    Toma los datos del libro y con ayuda de la conexion a la base de datos ademas de la función SQL insert puede insertar un nuevo libro al inventario.

    Args:
        conexion: Requiere conexion a la base de datos para poder obtener los datos del inventario.

    Returns:
        None.

    Raises:
        Puede dar error al no encontrar la libreria correspondiente o al no poder conectarse a la base de datos.

    Examples:
        Permite al empleado ingresar un nuevo libro al inventario y te imprime un mensaje de que el libro fue agregado correctamente y te pregunta si deseas agregar otro libro.
    """
    libros_agregados = 0
    while True:
        try:
            titulo_nuevo = (
                input("Ingresa el título del libro: ").strip().title()
            )
            autor_nuevo = (
                input("Ingresa el nombre del autor del libro: ")
                .strip()
                .title()
            )

            try:
                ejemplares_nuevo = int(
                    input("Ingresa los ejemplares que tenemos en existencia: ")
                )
            except ValueError:
                console.print(
                    "Debes ingresar un número válido.", style=error_style
                )
                continue

            conexion.execute(
                "INSERT INTO libros (titulo, autor, ejemplares) VALUES (?, ?, ?)",
                (titulo_nuevo, autor_nuevo, ejemplares_nuevo),
            )
            conexion.commit()
            libros_agregados += 1
            console.print("Libro agregado correctamente", style=check_style)

            while True:
                otro_libro = (
                    input("¿Deseas ingresar otro libro? ").strip().lower()
                )
                if otro_libro in ("si", "sí", "s", "y", "yes"):
                    break
                elif otro_libro in ("no", "n"):
                    if libros_agregados > 0:
                        console.print(
                            f"Has agregado {libros_agregados} libro(s) correctamente.",
                            style=check_style,
                        )
                    return
                else:
                    console.print(
                        "Ingresa una opción válida", style=error_style
                    )
        except sqlite3.Error as e:
            conexion.rollback()
            console.print(
                f"Error de base de datos al insertar el libro: {e}",
                style=error_style,
            )
        except Exception as e:
            console.print(
                f"Error inesperado al insertar el libro: {e}",
                style=error_style,
            )


def ver_prestamos(conexion):
    """
    Abre la tabla SQL llamada prestamos para poder ver los prestamos.

    Toma los datos de la base de datos y con ayuda de rich puede crear una tabla para mostrar los prestamos.

    Args:
        conexion: Requiere conexion a la base de datos para poder obtener los datos de las solicitudes de prestamos.

    Returns:
        bool: Devuelve True si hay préstamos registrados para mostrar o False si no los hay o si ocurre algún error.

    Raises:
        Puede dar error al no encontrar la libreria correspondiente o al no poder conectarse a la base de datos.

    Examples:
        Prestamo pendiente del libro 0017 por el usuario 0003, fecha de solicitud 2024-06-01, fecha de autorización 2024-06-02, fecha de devolución 2024-06-10, motivo de rechazo "N/A"
    """
    try:
        cursor = conexion.execute(
            "SELECT id, id_libro, id_usuario, estado, fecha_solicitud, fecha_autorizacion, fecha_devolucion, motivo_rechazo FROM prestamos ORDER BY id"
        )
        filas = cursor.fetchall()

        if not filas:
            console.print("No hay préstamos registrados.", style=error_style)
            return False

        tabla = Table(title="[bold white]Menú Préstamos[/bold white]")
        tabla.add_column("ID", justify="center", style="green")
        tabla.add_column("ID Libro", justify="center", style="blue")
        tabla.add_column("ID Usuario", justify="center", style="blue")
        tabla.add_column("Estado", justify="center", style="green")
        tabla.add_column(
            "Fecha de Solicitud", justify="center", style="yellow"
        )
        tabla.add_column(
            "Fecha de Autorización", justify="center", style="yellow"
        )
        tabla.add_column(
            "Fecha de Devolución", justify="center", style="yellow"
        )
        tabla.add_column("Notas", justify="center", style="magenta")

        for fila in filas:
            id_prestamo = f"{int(fila['id']):04d}"
            tabla.add_row(
                id_prestamo,
                str(fila["id_libro"]),
                str(fila["id_usuario"]),
                str(fila["estado"]),
                str(fila["fecha_solicitud"]),
                str(fila["fecha_autorizacion"]),
                str(fila["fecha_devolucion"]),
                str(fila["motivo_rechazo"]),
            )
        console.print(tabla)
        return True
    except sqlite3.Error as e:
        console.print(
            f"Error de base de datos al consultar préstamos: {e}",
            style=error_style,
        )
        return False
    except Exception as e:
        console.print(
            f"Error inesperado al consultar préstamos: {e}", style=error_style
        )
        return False


def opciones_solicitud_prestamo():
    """
    Abre las opciones que se puede realizar ante una solicitud de préstamo.

    Abre las opciones que se puede realizar ante una solicitud de préstamo y con ayuda de rich puede crear un panel para mostrar las opciones.

    Args:
        No requiere argumentos

    Returns:
        None.

    Raises:
        Puede dar error al no encontrar la libreria correspondiente.

    Examples:
        Autorizar, Rechazar, Cancelar
    """
    try:
        console.print(
            Panel(
                "[bold white]1. Autorizar\n2. Rechazar\n3. Cancelar[/bold white]",
                title="SOLICITUD DE PRÉSTAMO",
                border_style="green",
                expand=False,
            )
        )
    except Exception as e:
        console.print(
            f"Error al mostrar las opciones de préstamo: {e}",
            style=error_style,
        )


def gestionar_solicitudes(conexion):
    """
    Permite gestionar las solicitudes de prestamos y dependiendo del estado del prestamos permite hacer una u otra opción.

    Permite gestionar las solicitudes de prestamos y dependiendo del estado del prestamos permite hacer una u otra opción, además de poder ver el inventario de libros.

    Args:
        conexion: Requiere conexion a la base de datos para poder obtener los datos de las solicitudes de prestamos.

    Returns:
        None.

    Raises:
        Puede dar error al no encontrar la libreria correspondiente o al no poder conectarse a la base de datos.

    Examples:
        Prestamo pendiente del libro 0017 por el usuario 0003, fecha de solicitud 2024-06-01, fecha de autorización 2024-06-02, fecha de devolución 2024-06-10, motivo de rechazo "N/A"
    """
    solicitudes_atendidas = 0
    while True:
        try:
            hay_prestamos = ver_prestamos(conexion)
            if not hay_prestamos:
                return

            try:
                id_prestamo = int(
                    input(
                        "\nIngresa el ID de la solicitud que deseas atender: "
                    )
                )
            except ValueError:
                console.print(
                    "Por favor, ingresa un número entero válido.",
                    style=error_style,
                )
                continue

            cursor = conexion.execute(
                """
                SELECT p.id, p.id_libro, p.id_usuario, p.estado, 
                       p.fecha_solicitud, p.fecha_autorizacion, p.fecha_devolucion, 
                       l.titulo AS titulo_libro
                FROM prestamos p
                LEFT JOIN libros l ON p.id_libro = l.id
                WHERE p.id = ?
                """,
                (id_prestamo,),
            )
            fila = cursor.fetchone()

            if fila is None:
                console.print(
                    "No se ha encontrado una solicitud con ese ID.",
                    style=error_style,
                )
                continue

            titulo = (
                fila["titulo_libro"]
                if fila["titulo_libro"]
                else "(Libro no encontrado)"
            )

            if fila["estado"] == "rechazado":
                console.print(
                    f'La solicitud {int(fila["id"]):04d} ya está en estado "{fila["estado"]}".',
                    style=error_style,
                )
                continue

            elif fila["estado"] == "autorizado":
                console.print(
                    f'La solicitud {int(fila["id"]):04d} del usuario {fila["id_usuario"]} para el libro "{titulo}" ya está autorizada.'
                )
                devuelto = (
                    input(
                        f'¿Confirmas que el libro "{titulo}" fue devuelto? (s/n): '
                    )
                    .strip()
                    .lower()
                )

                if devuelto in ("si", "sí", "s", "y", "yes"):
                    conexion.execute(
                        "UPDATE prestamos SET estado = 'devuelto', "
                        "motivo_rechazo = 'Devuelto correctamente el ' || strftime('%d/%m/%Y', 'now') "
                        "WHERE id = ?",
                        (fila["id"],),
                    )
                    conexion.commit()
                    console.print(
                        "Libro marcado como devuelto exitosamente.",
                        style=check_style,
                    )
                    solicitudes_atendidas += 1

            else:
                console.print(
                    f'La solicitud seleccionada es la {int(fila["id"]):04d} del usuario {fila["id_usuario"]} para el libro "{titulo}".'
                )

                cancelado = False
                while True:
                    opciones_solicitud_prestamo()
                    try:
                        opcion_solicitud = int(input("¿Qué deseas hacer? "))
                    except ValueError:
                        console.print(
                            "Por favor, ingresa un número entero válido.",
                            style=error_style,
                        )
                        continue

                    if opcion_solicitud == 1:
                        if autorizar_prestamo(conexion, fila):
                            solicitudes_atendidas += 1
                        break
                    elif opcion_solicitud == 2:
                        if rechazar_prestamo(conexion, fila):
                            solicitudes_atendidas += 1
                        break
                    elif opcion_solicitud == 3:
                        console.print("Atención de solicitudes cancelada.")
                        cancelado = True
                        break
                    else:
                        console.print(
                            "Ingresa una opción válida", style=error_style
                        )

                if cancelado:
                    return

            otra_solicitud = (
                input("\n¿Deseas atender otra solicitud? (s/n): ")
                .strip()
                .lower()
            )
            if otra_solicitud not in ("si", "sí", "s", "y", "yes"):
                if solicitudes_atendidas > 0:
                    console.print(
                        f"Has atendido {solicitudes_atendidas} solicitud(es) correctamente.",
                        style=check_style,
                    )
                break
        except sqlite3.Error as e:
            conexion.rollback()
            console.print(
                f"Error de base de datos al gestionar solicitudes: {e}",
                style=error_style,
            )
        except Exception as e:
            console.print(
                f"Error inesperado al gestionar solicitudes: {e}",
                style=error_style,
            )


def autorizar_prestamo(conexion, fila):
    """
    Verifica la disponibilidad de un libro y actualiza el estado de la solicitud a autorizado.

    Consulta la cantidad de ejemplares disponibles en el inventario y, tras confirmar la acción, actualiza la solicitud de préstamo en la base de datos.

    Args:
        conexion: Requiere conexion a la base de datos para poder modificar los datos del préstamo.
        fila: Fila con los datos del préstamo e información del libro correspondiente.

    Returns:
        bool: Devuelve True si la solicitud se autorizó exitosamente o False si se canceló o ocurrió un error.

    Raises:
        Puede dar error al no encontrar la libreria correspondiente o al no poder conectarse a la base de datos.

    Examples:
        Autoriza la solicitud del libro seleccionado actualizando su estado a 'autorizado'.
    """
    try:
        cursor = conexion.execute(
            "SELECT ejemplares FROM libros WHERE id = ?", (fila["id_libro"],)
        )
        fila_libro = cursor.fetchone()

        if fila_libro is None:
            console.print(
                "No se encontró el libro asociado a esta solicitud.",
                style=error_style,
            )
            return False

        cursor_conteo = conexion.execute(
            "SELECT COUNT(*) FROM prestamos WHERE id_libro = ? AND estado = 'autorizado'",
            (fila["id_libro"],),
        )
        prestados = cursor_conteo.fetchone()[0]
        disponibles = fila_libro["ejemplares"] - prestados

        if disponibles <= 0:
            console.print(
                "No hay ejemplares disponibles de este libro.",
                style=error_style,
            )
            return False

        while True:
            confirmar = (
                input("¿Confirmas que deseas autorizar esta solicitud? ")
                .strip()
                .lower()
            )
            if confirmar in ("si", "sí", "s", "y", "yes"):
                conexion.execute(
                    "UPDATE prestamos SET estado = 'autorizado', fecha_autorizacion = datetime('now') WHERE id = ?",
                    (fila["id"],),
                )
                conexion.commit()
                console.print(
                    "Solicitud autorizada correctamente.", style=check_style
                )
                return True
            elif confirmar in ("no", "n"):
                console.print("Autorización cancelada.")
                return False
            else:
                console.print("Ingresa una opción válida", style=error_style)
    except sqlite3.Error as e:
        conexion.rollback()
        console.print(
            f"Error de base de datos al autorizar préstamo: {e}",
            style=error_style,
        )
        return False
    except Exception as e:
        console.print(
            f"Error inesperado al autorizar préstamo: {e}", style=error_style
        )
        return False


def rechazar_prestamo(conexion, fila):
    """
    Solicita el motivo de rechazo y actualiza el estado de la solicitud en la base de datos.

    Pide al usuario ingresar el motivo de rechazo de la solicitud y actualiza los datos correspondientes tras la confirmación.

    Args:
        conexion: Requiere conexion a la base de datos para poder modificar los datos del préstamo.
        fila: Fila con los datos del préstamo a rechazar.

    Returns:
        bool: Devuelve True si la solicitud se rechazó exitosamente o False si se canceló o ocurrió un error.

    Raises:
        Puede dar error al no encontrar la libreria correspondiente o al no poder conectarse a la base de datos.

    Examples:
        Rechaza una solicitud de préstamo registrando el motivo 'Sin stock'.
    """
    try:
        motivo_rechazo = input("Ingresa el motivo del rechazo: ").strip()
        if not motivo_rechazo:
            console.print(
                "Debes ingresar un motivo de rechazo.", style=error_style
            )
            return False

        while True:
            confirmar = (
                input("¿Confirmas que deseas rechazar esta solicitud? ")
                .strip()
                .lower()
            )
            if confirmar in ("si", "sí", "s", "y", "yes"):
                conexion.execute(
                    "UPDATE prestamos SET estado = 'rechazado', motivo_rechazo = ? WHERE id = ?",
                    (motivo_rechazo, fila["id"]),
                )
                conexion.commit()
                console.print(
                    "Solicitud rechazada correctamente.", style=check_style
                )
                return True
            elif confirmar in ("no", "n"):
                console.print("Rechazo cancelado.")
                return False
            else:
                console.print("Ingresa una opción válida", style=error_style)
    except sqlite3.Error as e:
        conexion.rollback()
        console.print(
            f"Error de base de datos al rechazar préstamo: {e}",
            style=error_style,
        )
        return False
    except Exception as e:
        console.print(
            f"Error inesperado al rechazar préstamo: {e}", style=error_style
        )
        return False


def modificar_libro(conexion):
    """
    Permite seleccionar un libro del inventario para actualizar sus datos.

    Muestra el inventario disponible, solicita el ID del libro a editar y ejecuta el flujo de edición correspondiente.

    Args:
        conexion: Requiere conexion a la base de datos para obtener y modificar los datos del libro.

    Returns:
        None.

    Raises:
        Puede dar error al no encontrar la libreria correspondiente o al no poder conectarse a la base de datos.

    Examples:
        Abre la interfaz para modificar el título, autor o ejemplares de un libro.
    """
    libros_modificados = 0
    while True:
        try:
            ver_inventario(conexion)

            try:
                id_modificar = int(
                    input("Ingresa el ID del libro que deseas modificar: ")
                )
            except ValueError:
                console.print(
                    "Por favor, ingresa un número entero válido.",
                    style=error_style,
                )
                continue

            cursor = conexion.execute(
                "SELECT id, titulo, autor, ejemplares FROM libros WHERE id = ?",
                (id_modificar,),
            )
            fila = cursor.fetchone()

            if fila is None:
                console.print(
                    "No se ha encontrado un libro con ese ID.",
                    style=error_style,
                )
                continue

            console.print(
                f'El libro seleccionado es "{fila["titulo"]}", escrito por {fila["autor"]} con {fila["ejemplares"]} ejemplares.'
            )
            console.print(
                Panel(
                    "[bold white]1. Título\n2. Autor\n3. Ejemplares\n4. Cancelar Edición[/bold white]",
                    title="DATOS DEL LIBRO",
                    border_style="green",
                    expand=False,
                )
            )
            while True:
                try:
                    campo_editar = int(input("¿Qué campo deseas editar? "))
                    if campo_editar == 1:
                        campo = "titulo"
                        break
                    elif campo_editar == 2:
                        campo = "autor"
                        break
                    elif campo_editar == 3:
                        campo = "ejemplares"
                        break
                    elif campo_editar == 4:
                        console.print("Edición de libros cancelada.")
                        return
                    else:
                        console.print(
                            "Ingresa una opción válida", style=error_style
                        )
                except ValueError:
                    console.print(
                        "Por favor, ingresa un número entero válido.",
                        style=error_style,
                    )

            if edicion_libros(conexion, campo, fila, id_modificar):
                libros_modificados += 1

            otra_edicion = (
                input("¿Deseas modificar otro libro? (s/n): ").strip().lower()
            )
            if otra_edicion not in ("si", "sí", "s", "y", "yes"):
                if libros_modificados > 0:
                    console.print(
                        f"Has modificado {libros_modificados} libro(s) correctamente.",
                        style=check_style,
                    )
                break
        except sqlite3.Error as e:
            conexion.rollback()
            console.print(
                f"Error de base de datos al modificar el libro: {e}",
                style=error_style,
            )
        except Exception as e:
            console.print(
                f"Error inesperado al modificar el libro: {e}",
                style=error_style,
            )


def edicion_libros(conexion, campo, fila, id_modificar):
    """
    Realiza la actualización de un campo específico del libro en la base de datos.

    Toma el valor actual, solicita el nuevo dato al usuario y realiza el UPDATE en la tabla libros tras su confirmación.

    Args:
        conexion: Requiere conexion a la base de datos para realizar la actualización.
        campo (str): El nombre del campo a editar ('titulo', 'autor' o 'ejemplares').
        fila: Fila con los datos actuales del libro.
        id_modificar (int): ID del libro a editar.

    Returns:
        bool: Devuelve True si el libro se editó correctamente o False si la edición se canceló o falló.

    Raises:
        Puede dar error al no encontrar la libreria correspondiente o al no poder conectarse a la base de datos.

    Examples:
        Edita el campo 'titulo' actualizándolo con un nuevo valor.
    """
    try:
        allowed_fields = {
            "titulo": "titulo",
            "autor": "autor",
            "ejemplares": "ejemplares",
        }
        campo_seguro = allowed_fields.get(campo)

        if campo_seguro is None:
            console.print(
                "Campo no permitido para modificación.", style=error_style
            )
            return False

        if campo_seguro == "ejemplares":
            console.print(
                f'El número de {campo_seguro} actual es "{fila[campo_seguro]}"'
            )
            try:
                campo_editado = int(
                    input(f"Ingresa el nuevo número de {campo_seguro}: ")
                )
            except ValueError:
                console.print(
                    "Debes ingresar un número entero válido.",
                    style=error_style,
                )
                return False
            console.print(
                f"El nuevo número de ejemplares será: {campo_editado}"
            )
        else:
            console.print(
                f'El {campo_seguro} actual es "{fila[campo_seguro]}"'
            )
            campo_editado = (
                input(f"Ingresa el nuevo {campo_seguro}: ")
                .strip()
                .title()
            )
            console.print(
                f"El nuevo {campo_seguro} del libro será: {campo_editado}"
            )

        while True:
            confirmar = (
                input("¿Confirmas que la edición es correcta? ")
                .strip()
                .lower()
            )
            if confirmar in ("si", "sí", "s", "y", "yes"):
                conexion.execute(
                    f"UPDATE libros SET {campo_seguro} = ? WHERE id = ?",
                    (campo_editado, id_modificar),
                )
                conexion.commit()

                cursor = conexion.execute(
                    "SELECT id, titulo, autor, ejemplares FROM libros WHERE id = ?",
                    (id_modificar,),
                )
                fila_actualizada = cursor.fetchone()

                console.print(
                    "Libro editado correctamente.", style=check_style
                )
                console.print("Sus datos ahora son:")
                console.print(f"Título: {fila_actualizada['titulo']}")
                console.print(f"Autor: {fila_actualizada['autor']}")
                console.print(
                    f"Número de Ejemplares: {fila_actualizada['ejemplares']}"
                )
                return True
            elif confirmar in ("no", "n"):
                console.print("Edición cancelada.")
                return False
            else:
                console.print("Ingresa una opción válida", style=error_style)
    except sqlite3.Error as e:
        conexion.rollback()
        console.print(
            f"Error de base de datos durante la edición: {e}",
            style=error_style,
        )
        return False
    except Exception as e:
        console.print(
            f"Error inesperado durante la edición: {e}", style=error_style
        )
        return False


def borrar_libro(conexion):
    """
    Permite eliminar un libro del inventario mediante su ID.

    Muestra los libros registrados, solicita el ID del libro a eliminar y, tras confirmar la acción, lo elimina de la base de datos.

    Args:
        conexion: Requiere conexion a la base de datos para borrar el libro correspondiente.

    Returns:
        None.

    Raises:
        Puede dar error al no encontrar la libreria correspondiente o al no poder conectarse a la base de datos.

    Examples:
        Elimina el libro con ID 0005 tras confirmación del usuario.
    """
    libros_eliminados = 0
    while True:
        try:
            ver_inventario(conexion)

            try:
                id_borrar = int(
                    input("\nIngresa el ID del libro que deseas borrar: ")
                )
            except ValueError:
                console.print(
                    "Por favor, ingresa un número entero válido.",
                    style=error_style,
                )
                continue

            cursor = conexion.execute(
                "SELECT id, titulo, autor, ejemplares FROM libros WHERE id = ?",
                (id_borrar,),
            )
            fila = cursor.fetchone()

            if fila is None:
                console.print(
                    "No se ha encontrado un libro con ese ID.",
                    style=error_style,
                )
                continue

            console.print(
                f'¿Estás seguro de borrar el libro con título "{fila["titulo"]}" escrito por {fila["autor"]}?'
            )
            console.print(
                f"Esta decisión no se podrá deshacer y el libro tiene {fila['ejemplares']} ejemplares."
            )

            confirmar_delete = input("(s/n): ").strip().lower()

            if confirmar_delete in ("si", "sí", "s", "y", "yes"):
                conexion.execute(
                    "DELETE FROM libros WHERE id = ?", (id_borrar,)
                )
                conexion.commit()
                libros_eliminados += 1
                console.print(
                    "Libro borrado correctamente.", style=check_style
                )
            else:
                console.print("Operación de borrado cancelada.")

            while True:
                otro_borrado = (
                    input("¿Deseas borrar otro libro? ").strip().lower()
                )
                if otro_borrado in ("si", "sí", "s", "y", "yes"):
                    break
                elif otro_borrado in ("no", "n"):
                    if libros_eliminados > 0:
                        console.print(
                            f"Has eliminado {libros_eliminados} libro(s) correctamente.",
                            style=check_style,
                        )
                    return
                else:
                    console.print(
                        "Ingresa una opción válida", style=error_style
                    )
        except sqlite3.Error as e:
            conexion.rollback()
            console.print(
                f"Error de base de datos al borrar el libro: {e}",
                style=error_style,
            )
        except Exception as e:
            console.print(
                f"Error inesperado al borrar el libro: {e}", style=error_style
            )

#main



def open_main_menu_employee():
    menu_empleado_ascci()

    while True:
        conexion = None
        try:
            opciones_empleado()
            opcion_menu = input("Ingresa la opción deseada: ").strip()

            if opcion_menu == "1":
                console.print(
                    "Opción 1 Seleccionada:\n[bold white]Ingresar Libro[/bold white]"
                )
                try:
                    conexion = db.conectar()
                    conexion.row_factory = sqlite3.Row
                    insertar_libro(conexion)
                finally:
                    if conexion:
                        conexion.close()

            elif opcion_menu == "2":
                console.print(
                    "Opción 2 Seleccionada:\n[bold white]Modificar Libro[/bold white]"
                )
                try:
                    conexion = db.conectar()
                    conexion.row_factory = sqlite3.Row
                    modificar_libro(conexion)
                finally:
                    if conexion:
                        conexion.close()

            elif opcion_menu == "3":
                console.print(
                    "Opción 3 Seleccionada:\n[bold white]Borrar Libro[/bold white]"
                )
                try:
                    conexion = db.conectar()
                    conexion.row_factory = sqlite3.Row
                    borrar_libro(conexion)
                finally:
                    if conexion:
                        conexion.close()

            elif opcion_menu == "4":
                console.print(
                    "Opción 4 Seleccionada:\n[bold white]Ver Inventario[/bold white]"
                )
                try:
                    conexion = db.conectar()
                    conexion.row_factory = sqlite3.Row
                    ver_inventario(conexion)
                finally:
                    if conexion:
                        conexion.close()

            elif opcion_menu == "5":
                console.print(
                    "Opción 5 Seleccionada:\n[bold white]Ver Solicitudes de Préstamo[/bold white]"
                )
                try:
                    conexion = db.conectar()
                    conexion.row_factory = sqlite3.Row
                    gestionar_solicitudes(conexion)
                finally:
                    if conexion:
                        conexion.close()

            elif opcion_menu == "6":
                console.print(
                    "Opción 6 Seleccionada:\n[bold white]Salir\nGracias por utilizar el programa.[/bold white]"
                )
                sys.exit()

            else:
                console.print("Ingresa una opción válida", style=error_style)

        except KeyboardInterrupt:
            console.print(
                "\nPrograma interrumpido por el usuario.", style=error_style
            )
            break
        except Exception as e:
            console.print(
                f"Ocurrió un error inesperado en el menú principal: {e}",
                style=error_style,
            )
