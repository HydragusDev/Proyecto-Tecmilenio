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


def menu_usuario_ascci():
    print(figlet_format("MENU  DE", font="standard"))
    print(figlet_format("USUARIO", font="standard"))


def opciones_usuario():
    console.print(
        Panel(
            "[bold white]1. Ver Catalogo de Libros\n2. Hacer Solicitud de Prestamo\n3. Agendar devolución \n4. Salir [/bold white]",
            title="OPCIONES",
            border_style="cyan",
            expand=False,
        )
    )


def opciones_ver_catalogo():
    console.print(
        Panel(
            "[bold white]1. Ver Catalogo Completo\n2. Ver Unicamente Disponibles\n3. Busqueda Especifica\n4. Volver Al Menu Principal [/bold white]",
            border_style="green",
            expand=False,
        )
    )


def opciones_busqueda_especifica():
    console.print(
        Panel(
            "[bold white]1. Busqueda por Titulo\n2. Busqueda por Autor\n3. Volver Al Menu Principal [/bold white]",
            border_style="yellow",
            expand=False,
        )
    )


def ver_inventario(conexion):
    cursor = conexion.execute(
        "SELECT id, titulo, autor FROM libros ORDER BY id"
    )
    filas = cursor.fetchall()

    if not filas:
        console.print("No hay libros registrados.", style=error_style)
    else:
        tabla = Table(title="[bold white]Inventario de Libros[/bold white]")
        tabla.add_column("ID", justify="center", style="green")
        tabla.add_column("Título", justify="center", style="blue")
        tabla.add_column("Autor", justify="center", style="magenta")

        for fila in filas:
            id_libro = f"{int(fila['id']):04d}"
            tabla.add_row(
                id_libro,
                str(fila["titulo"]),
                str(fila["autor"]),
            )
        console.print(tabla)


def ver_inventario_disponibles(conexion):
    cursor = conexion.execute(
        "SELECT id, titulo, autor, ejemplares FROM libros ORDER BY id"
    )
    filas = cursor.fetchall()

    if not filas:
        console.print("No hay libros registrados.", style=error_style)
        return

    tabla = Table(
        title="[bold white]Inventario de Libros Disponibles[/bold white]"
    )
    tabla.add_column("ID", justify="center", style="green")
    tabla.add_column("Título", justify="center", style="blue")
    tabla.add_column("Autor", justify="center", style="magenta")
    tabla.add_column("Disponibles", justify="center", style="cyan")

    hay_disponibles = False

    for fila in filas:
        cursor_conteo = conexion.execute(
            "SELECT COUNT(*) FROM prestamos WHERE id_libro = ? AND estado = 'autorizado'",
            (fila["id"],),
        )
        prestados = cursor_conteo.fetchone()[0]
        disponibles = fila["ejemplares"] - prestados

        if disponibles > 0:
            hay_disponibles = True

            id_libro = f"{int(fila['id']):04d}"
            tabla.add_row(
                id_libro,
                str(fila["titulo"]),
                str(fila["autor"]),
                str(disponibles),
            )
    if hay_disponibles:
        console.print(tabla)
    else:
        console.print("No hay ejemplares disponibles.", style=error_style)


def busqueda_especifica(conexion, criterio_busqueda, busqueda):
    try:
        cursor = conexion.execute(
            f"SELECT id, titulo, autor FROM libros WHERE {criterio_busqueda} LIKE ?",
            (f"%{busqueda}%",),
        )

        filas = cursor.fetchall()

        if not filas:
            console.print(
                f'\n[red]No se encontraron libros con {criterio_busqueda}: "{busqueda}"[/red]\n'
            )
            return False

        tabla = Table(title="[bold white]Resultados de Búsqueda[/bold white]")
        tabla.add_column("ID", justify="center", style="green")
        tabla.add_column("Título", justify="center", style="blue")
        tabla.add_column("Autor", justify="center", style="magenta")

        for fila in filas:
            id_libro = f"{int(fila['id']):04d}"
            tabla.add_row(
                id_libro,
                str(fila["titulo"]),
                str(fila["autor"]),
            )

        console.print(tabla)

    except Exception as e:
        console.print(f"Ha ocurrido el error: {e}", style=error_style)
        console.print("Repite la búsqueda", style=error_style)


def solicitar_prestamo(conexion, id_usuario):
    ver_inventario_disponibles(conexion)

    try:
        id_libro = int(input("Ingresa el ID del libro que deseas solicitar: "))
    except ValueError:
        console.print("El ID ingresado no es válido.", style=error_style)
        return

    cursor = conexion.execute(
        "SELECT ejemplares FROM libros WHERE id = ?", (id_libro,)
    )
    fila_libro = cursor.fetchone()

    if fila_libro is None:
        console.print(
            f"\n[red]No se encontró el libro con ID: {id_libro:04d}[/red]\n"
        )
        return False

    cursor_conteo = conexion.execute(
        "SELECT COUNT(*) FROM prestamos WHERE id_libro = ? AND estado = 'autorizado'",
        (id_libro,),
    )
    prestados = cursor_conteo.fetchone()[0]
    disponibles = fila_libro["ejemplares"] - prestados

    if disponibles <= 0:
        console.print(
            "No hay ejemplares disponibles de este libro.", style=error_style
        )
        return

    conexion.execute(
        "INSERT INTO prestamos (id_libro, id_usuario) VALUES (?, ?)",
        (id_libro, id_usuario),
    )
    conexion.commit()

    console.print(
        "Solicitud de préstamo enviada. Espera autorización.",
        style=check_style,
    )


while True:
    try:
        opciones_usuario()
        opcion_menu = int(input("Ingresa la opción deseada: "))

        if opcion_menu == 1:
            while True:
                opciones_ver_catalogo()
                opcion_select_verCata = int(
                    input("Ingresa la opción deseada: ")
                )
                if opcion_select_verCata == 1:
                    conexion = db.conectar()
                    conexion.row_factory = sqlite3.Row
                    console.print(
                        "Opción Seleccionada:\n[bold white]Ver Catalogo Completo[/bold white]"
                    )
                    try:
                        ver_inventario(conexion)
                    except Exception as e:
                        console.print(
                            f"[red]Error al cargar el inventario: {e}[/red]"
                        )
                    finally:
                        conexion.close()

                elif opcion_select_verCata == 2:
                    conexion = db.conectar()
                    conexion.row_factory = sqlite3.Row
                    console.print(
                        "Opción Seleccionada:\n[bold white]Ver Catalogo Disponible[/bold white]"
                    )
                    try:
                        ver_inventario_disponibles(conexion)
                    except Exception as e:
                        console.print(
                            f"[red]Error al cargar disponibles: {e}[/red]"
                        )
                    finally:
                        conexion.close()

                elif opcion_select_verCata == 3:
                    console.print(
                        "Opción Seleccionada:\n[bold white]Busqueda Especifica[/bold white]"
                    )
                    while True:
                        opciones_busqueda_especifica()
                        criterio_busqueda = (
                            input("Ingresa tu opción (1-3): ").strip().lower()
                        )

                        if criterio_busqueda in ("1", "titulo", "title"):
                            campo_buscar = "titulo"
                            buscar = True
                            break
                        elif criterio_busqueda in ("2", "autor", "author"):
                            campo_buscar = "autor"
                            buscar = True
                            break
                        elif criterio_busqueda in ("3", "salir", "exit"):
                            buscar = False
                            break
                        else:
                            console.print(
                                "Ingresa una opción válida", style=error_style
                            )
                            buscar = False
                            continue

                    if buscar:
                        busqueda = input(
                            f"Ingresa el {campo_buscar} a buscar: "
                        ).strip()
                        conexion = db.conectar()
                        conexion.row_factory = sqlite3.Row
                        try:
                            busqueda_especifica(
                                conexion, campo_buscar, busqueda
                            )
                        finally:
                            conexion.close()

                elif opcion_select_verCata == 4:
                    break

        elif opcion_menu == 2:
            console.print(
                "Opción Seleccionada:\n[bold white]Hacer Solicitud de Prestamo[/bold white]"
            )
            id_usuario_demo = 1
            conexion = db.conectar()
            conexion.row_factory = sqlite3.Row
            try:
                solicitar_prestamo(conexion, id_usuario_demo)
            except Exception as e:
                console.print(f"Ha ocurrido el error: {e}", style=error_style)
            finally:
                conexion.close()

        elif opcion_menu == 3:
            console.print(
                "Opción Seleccionada:\n[bold white]Agendar Devolución[/bold white]"
            )

        elif opcion_menu == 4:
            console.print(
                "Opción Seleccionada:\n[bold white]Salir\nGracias por utilizar el programa.[/bold white]"
            )
            break

        else:
            console.print("Ingresa una opción válida", style=error_style)

    except ValueError:
        console.print(
            "Por favor, ingresa un número entero válido.", style=error_style
        )
    except KeyboardInterrupt:
        console.print(
            "\nPrograma interrumpido por el usuario.", style=error_style
        )
        break
