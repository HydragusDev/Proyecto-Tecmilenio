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
            border_style="yellow",
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

def modificar_libro(conexion):
    libros_modificados = 0
    while True:
        ver_inventario(conexion)

        try:
            id_modificar = int
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

        confirmar_delete = input("(s/n): ").lower().strip()

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
