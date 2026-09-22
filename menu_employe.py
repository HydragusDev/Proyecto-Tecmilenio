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
            "[bold white]1. Ingresar Libro\n2. Modificar Libro\n3. Borrar Libro\n4. Ver Inventario\n5. Ver Solicitudes de Prestamos\n6. Salir [/bold white]",
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
            console.print("[red]Debes ingresar un número válido.[/red]")
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
                console.print(
                    "Ingresa una opción válida",
                    style=error_style,
                )


def ver_prestamos(conexion):
    cursor = conexion.execute(
        "SELECT id, id_libro, id_usuario, estado, fecha_solicitud, fecha_autorizacion, fecha_devolucion, motivo_rechazo FROM prestamos ORDER BY id"
    )
    filas = cursor.fetchall()

    if not filas:
        console.print("No hay prestamos registrados.", style=error_style)
    else:
        tabla = Table(title="[bold white]Menu Prestamos[/bold white]")
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
            id = f"{int(fila['id']):04d}"
            tabla.add_row(
                id,
                str(fila["id_libro"]),
                str(fila["id_usuario"]),
                str(fila["estado"]),
                str(fila["fecha_solicitud"]),
                str(fila["fecha_autorizacion"]),
                str(fila["fecha_devolucion"]),
                str(fila["motivo_rechazo"]),
            )
        console.print(tabla)


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
                "No se ha encontrado un libro con ese ID, por favor intenta nuevamente.",
                style=error_style,
            )
            continue

        console.print(
            f'El libro seleccionado es "{fila["titulo"]}", escrito por {fila["autor"]} con {fila["ejemplares"]} ejemplares.'
        )
        console.print(
            Panel(
                "[bold white]1. Titulo\n2. Autor\n3. Ejemplares\n4. Cancelar Edición [/bold white]",
                title="DATOS DEL LIBRO",
                border_style="green",
                expand=False,
            )
        )
        while True:
            try:
                campo_editar = int(input("¿Qué campo deseas editar?"))
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
                    console.print("Edición de libros cancelada")
                    return
                else:
                    console.print(
                        "Ingresa una opción valida", style=error_style
                    )
                    continue
            except ValueError:
                console.print(
                    "Por favor, ingresa un número entero válido.",
                    style=error_style,
                )
                continue
        modificaciones = edicion_libros(conexion, campo, fila, id_modificar)
        if modificaciones:
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
    if campo == "ejemplares":
        console.print(
            f'El numero de {campo} actual del libro seleccionado es "{fila[campo]}"'
        )
        campo_editado = int(input(f"Ingresa el nuevo numero de {campo}: "))
        console.print(
            f"El nuevo  numero de ejemplares del libro será: {campo_editado}"
        )
    else:
        console.print(
            f'El {campo} actual del libro seleccionado es "{fila[campo]}"'
        )
        campo_editado = input(f"Ingresa el nuevo {campo}: ").strip().title()
        console.print(f"El nuevo {campo} del libro será {campo_editado} ")

    while True:
        confirmar_edicion = input("Confirmas que la edición es correcta? ")
        if confirmar_edicion in ("si", "sí", "s", "y", "yes"):
            conexion.execute(
                f"UPDATE libros SET {campo} = ? WHERE id = ?",
                (
                    campo_editado,
                    id_modificar,
                ),
            )
            conexion.commit()
            cursor = conexion.execute(
                "SELECT id, titulo, autor, ejemplares FROM libros WHERE id = ?",
                (id_modificar,),
            )
            fila = cursor.fetchone()
            console.print("Libro editado correctamente.", style=check_style)
            console.print("Sus datos ahora son:")
            console.print(f"Titulo: {fila['titulo']}")
            console.print(f"Autor: {fila['autor']}")
            console.print(f"Numero de Ejemplares: {fila['ejemplares']}")
            return True
        elif confirmar_edicion in ("no", "n"):
            console.print("Edición cancelada.")
            return False
        else:
            console.print("Ingresa una opción valida", style=error_style)
            continue


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
                "No se ha encontrado un libro con ese ID, por favor intenta nuevamente.",
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
                "DELETE FROM libros WHERE id = ?",
                (id_borrar,),
            )
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
                console.print(
                    "Ingresa una opción válida",
                    style=error_style,
                )


menu_empleado_ascci()

while True:
    try:
        opciones_empleado()
        opcion_menu = input("Ingresa la opción deseada: ")

        if opcion_menu == "1":
            conexion = db.conectar()
            conexion.row_factory = sqlite3.Row
            console.print(
                "Opción 1 Seleccionada:\n[bold white]Ingresar Libro[/bold white]"
            )
            try:
                insertar_libro(conexion)
            except Exception as e:
                console.print(f"[red]Ha ocurrido el error: {e}[/red]")
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
            except Exception as e:
                console.print(f"[red]Ha ocurrido el error: {e}[/red]")
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
            except Exception as e:
                console.print(f"[red]Ha ocurrido el error: {e}[/red]")
            finally:
                conexion.close()

        elif opcion_menu == "4":
            conexion = db.conectar()
            conexion.row_factory = sqlite3.Row
            console.print(
                "Opción 4 Seleccionada:\n[bold white]Ver Inventario[/bold white]"
            )
            try:
                ver_inventario(conexion)
            except Exception as e:
                console.print(f"[red]Error al cargar el inventario: {e}[/red]")
            finally:
                conexion.close()

        elif opcion_menu == "5":
            console.print(
                "Opción 5 Seleccionada:\n[bold white]Ver Solicitudes de Prestamo[/bold white]"
            )
            ver_prestamos(conexion)
        elif opcion_menu == "6":
            console.print(
                "Opción 6 Seleccionada:\n[bold white]Salir\nGracias por utilizar el programa.[/bold white]"
            )
            break

        else:
            console.print("Ingresa una opción válida")

    except ValueError:
        console.print(
            "Por favor, ingresa un número entero válido.", style=error_style
        )
    except KeyboardInterrupt:
        console.print(
            "\nPrograma interrumpido por el usuario.", style=error_style
        )
        break
