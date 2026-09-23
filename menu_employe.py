import sqlite3

from pyfiglet import figlet_format
from rich.console import Console
from rich.panel import Panel
from rich.style import Style
from rich.table import Table

import database as db

console = Console()

error_style = Style(color="red", bold=True, blink=True)
check_style = Style(color="green", blink=True)


def menu_empleado_ascci():
    print(figlet_format("MENU  DE", font="standard"))
    print(figlet_format("EMPLEADO", font="standard"))


def opciones_empleado():
    console.print(
        Panel(
            "[bold white]1. Ingresar Libro\n2. Modificar Libro\n3. Borrar Libro\n4. Ver Inventario\n5. Ver Solicitudes de Prestamos\n6. Salir[/bold white]",
            title="OPCIONES",
            border_style="cyan",
            expand=False,
        )
    )


def ver_inventario(conexion):
    cursor = conexion.execute(
        "SELECT id, titulo, autor, ejemplares FROM libros ORDER BY id"
    )
    filas = cursor.fetchall()

    if not filas:
        console.print("No hay libros registrados.", style=error_style)
    else:
        tabla = Table(title="[bold white]Inventario de Libros[/bold white]")
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


def insertar_libro(conexion):
    libros_agregados = 0
    while True:
        titulo_nuevo = input("Ingresa el título del libro: ").strip().title()
        autor_nuevo = (
            input("Ingresa el nombre del autor del libro: ").strip().title()
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
            otro_libro = input("¿Deseas ingresar otro libro? ").strip().lower()
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
                console.print("Ingresa una opción válida", style=error_style)


def ver_prestamos(conexion):
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
    tabla.add_column("Fecha de Solicitud", justify="center", style="yellow")
    tabla.add_column("Fecha de Autorización", justify="center", style="yellow")
    tabla.add_column("Fecha de Devolución", justify="center", style="yellow")
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


def opciones_solicitud_prestamo():
    console.print(
        Panel(
            "[bold white]1. Autorizar\n2. Rechazar\n3. Cancelar[/bold white]",
            title="SOLICITUD DE PRÉSTAMO",
            border_style="green",
            expand=False,
        )
    )


def gestionar_solicitudes(conexion):
    solicitudes_atendidas = 0
    while True:
        hay_prestamos = ver_prestamos(conexion)
        if not hay_prestamos:
            return

        try:
            id_prestamo = int(
                input("Ingresa el ID de la solicitud que deseas atender: ")
            )
        except ValueError:
            console.print(
                "Por favor, ingresa un número entero válido.",
                style=error_style,
            )
            continue

        cursor = conexion.execute(
            "SELECT id, id_libro, id_usuario, estado, fecha_devolucion, fecha_autorizacion FROM prestamos WHERE id = ?",
            (id_prestamo,),
        )
        fila = cursor.fetchone()

        if fila is None:
            console.print(
                "No se ha encontrado una solicitud con ese ID.",
                style=error_style,
            )
            continue

        if fila["estado"] == "rechazado":
            console.print(
                f'La solicitud {int(fila["id"]):04d} ya está en estado "{fila["estado"]}".',
                style=error_style,
            )
            continue
        elif fila["estado"] == "autorizado":
            console.print(
                f'La solicitud {int(fila["id"])} fue autorizada el día "{fila["fecha_autorizacion"]}".'
            )
            devuelto = (
                input(
                    f"¿Confirmas que el libro fue devuelto en la fecha {fila['fecha_devolucion']}? (s/n): "
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
                break
            elif devuelto in ("no", "n"):
                break
            else:
                console.print("Ingresa una opción válida", style=error_style)
                continue

        console.print(
            f"La solicitud seleccionada es la {int(fila['id']):04d} del usuario {fila['id_usuario']} para el libro {fila['id_libro']}."
        )
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
                return
            else:
                console.print("Ingresa una opción válida", style=error_style)

        otra_solicitud = (
            input("¿Deseas atender otra solicitud? (s/n): ").strip().lower()
        )
        if otra_solicitud not in ("si", "sí", "s", "y", "yes"):
            if solicitudes_atendidas > 0:
                console.print(
                    f"Has atendido {solicitudes_atendidas} solicitud(es) correctamente.",
                    style=check_style,
                )
            break


def autorizar_prestamo(conexion, fila):
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
            "No hay ejemplares disponibles de este libro.", style=error_style
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


def rechazar_prestamo(conexion, fila):
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


def modificar_libro(conexion):
    libros_modificados = 0
    while True:
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
                "No se ha encontrado un libro con ese ID.", style=error_style
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


def edicion_libros(conexion, campo, fila, id_modificar):

    if campo not in ("titulo", "autor", "ejemplares"):
        console.print(
            "Campo no permitido para modificación.", style=error_style
        )
        return False

    if campo == "ejemplares":
        console.print(f'El número de {campo} actual es "{fila[campo]}"')
        try:
            campo_editado = int(input(f"Ingresa el nuevo número de {campo}: "))
        except ValueError:
            console.print(
                "Debes ingresar un número entero válido.", style=error_style
            )
            return False
        console.print(f"El nuevo número de ejemplares será: {campo_editado}")
    else:
        console.print(f'El {campo} actual es "{fila[campo]}"')
        campo_editado = input(f"Ingresa el nuevo {campo}: ").strip().title()
        console.print(f"El nuevo {campo} del libro será: {campo_editado}")

    while True:
        confirmar = (
            input("¿Confirmas que la edición es correcta? ").strip().lower()
        )
        if confirmar in ("si", "sí", "s", "y", "yes"):
            conexion.execute(
                f"UPDATE libros SET {campo} = ? WHERE id = ?",
                (campo_editado, id_modificar),
            )
            conexion.commit()

            cursor = conexion.execute(
                "SELECT id, titulo, autor, ejemplares FROM libros WHERE id = ?",
                (id_modificar,),
            )
            fila_actualizada = cursor.fetchone()

            console.print("Libro editado correctamente.", style=check_style)
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


def borrar_libro(conexion):
    libros_eliminados = 0
    while True:
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
                "No se ha encontrado un libro con ese ID.", style=error_style
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
            conexion.execute("DELETE FROM libros WHERE id = ?", (id_borrar,))
            conexion.commit()
            libros_eliminados += 1
            console.print("Libro borrado correctamente.", style=check_style)
        else:
            console.print("Operación de borrado cancelada.")

        while True:
            otro_borrado = input("¿Deseas borrar otro libro? ").strip().lower()
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
                console.print("Ingresa una opción válida", style=error_style)


menu_empleado_ascci()

while True:
    try:
        opciones_empleado()
        opcion_menu = input("Ingresa la opción deseada: ").strip()

        if opcion_menu == "1":
            console.print(
                "Opción 1 Seleccionada:\n[bold white]Ingresar Libro[/bold white]"
            )
            conexion = db.conectar()
            conexion.row_factory = sqlite3.Row
            try:
                insertar_libro(conexion)
            finally:
                conexion.close()

        elif opcion_menu == "2":
            console.print(
                "Opción 2 Seleccionada:\n[bold white]Modificar Libro[/bold white]"
            )
            conexion = db.conectar()
            conexion.row_factory = sqlite3.Row
            try:
                modificar_libro(conexion)
            finally:
                conexion.close()

        elif opcion_menu == "3":
            console.print(
                "Opción 3 Seleccionada:\n[bold white]Borrar Libro[/bold white]"
            )
            conexion = db.conectar()
            conexion.row_factory = sqlite3.Row
            try:
                borrar_libro(conexion)
            finally:
                conexion.close()

        elif opcion_menu == "4":
            console.print(
                "Opción 4 Seleccionada:\n[bold white]Ver Inventario[/bold white]"
            )
            conexion = db.conectar()
            conexion.row_factory = sqlite3.Row
            try:
                ver_inventario(conexion)
            finally:
                conexion.close()

        elif opcion_menu == "5":
            console.print(
                "Opción 5 Seleccionada:\n[bold white]Ver Solicitudes de Préstamo[/bold white]"
            )
            conexion = db.conectar()
            conexion.row_factory = sqlite3.Row
            try:
                gestionar_solicitudes(conexion)
            finally:
                conexion.close()

        elif opcion_menu == "6":
            console.print(
                "Opción 6 Seleccionada:\n[bold white]Salir\nGracias por utilizar el programa.[/bold white]"
            )
            break

        else:
            console.print("Ingresa una opción válida", style=error_style)

    except KeyboardInterrupt:
        console.print(
            "\nPrograma interrumpido por el usuario.", style=error_style
        )
        break
