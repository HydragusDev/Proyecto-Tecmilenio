import sqlite3

from rich.console import Console
from rich.panel import Panel
from rich.progress import BarColumn, Progress, SpinnerColumn, TextColumn
from rich.prompt import Prompt

import database as db  # Módulo para conectar con la base de datos y consultar libros

console = Console()

console.print(r"""[bold white]
 __  __ _____ _   _ _   _  
|  \/  | ____| \ | | | | |
| |\/| |  _| |  \| | | | |
| |  | | |___| |\  | |_| |
|_|  |_|_____|_| \_|\___/  
 _____ __  __ ____  _     _____    _    ____   ___
| ____|  \/  |  _ \| |   | ____|  / \  |  _ \ / _ \
|  _| | |\/| | |_) | |   |  _|   / _ \ | | | | | | |
| |___| |  | |  __/| |___| |___ / ___ \| |_| | |_| |
|_____|_|  |_|_|   |_____|_____/_/   \_\____/ \___/
[/bold white]""")

console.print(
    Panel(
        "[bold white]1. Ingresar Libro\n2. Modificar Libro\n3. Borrar Libro\n4. Ver Inventario\n5. Ver Solicitudes de Prestamos\n6. Salir [/bold white]",
        title="OPCIONES",
        border_style="yellow",
        expand=False,
    )
)
console.print()
while True:
    try:
        opcion_menu = input("Ingresa la opción deseada: ")
        if opcion_menu == "1":
            conexion = db.conectar()
            conexion.row_factory = sqlite3.Row
            console.print(
                "Opción 1 Seleccionada:\n[bold white]Ingresar Libro[/bold white]"
            )
            titulo_nuevo = (
                input("Ingresa el tiitulo del libro: ").strip().title()
            )
            autor_nuevo = (
                input("Ingresa el nombre del autor del libro: ")
                .strip()
                .title()
            )
            ejemplares_nuevo = int(
                input(
                    "Ingresa los ejemplares que tenemos en existencia de este libro: "
                )
            )
            conexion.execute(
                "INSERT INTO libros (titulo, autor, ejemplares) VALUES (?, ?, ?)",
                (titulo_nuevo, autor_nuevo, ejemplares_nuevo),
            )
            conexion.commit()
            conexion.close()
        elif opcion_menu == "2":
            console.print(
                "Opción 2 Seleccionada:\n[bold white]Modificar Libro[/bold white]"
            )
        elif opcion_menu == "3":
            console.print(
                "Opción 3 Seleccionada:\n[bold white]Borrar Libro[/bold white]"
            )
        elif opcion_menu == "4":
            conexion = db.conectar()
            conexion.row_factory = sqlite3.Row
            console.print(
                "Opción 4 Seleccionada:\n[bold white]Ver Inventario[/bold white]"
            )
            try:
                cursor = conexion.execute(
                    "SELECT id, titulo, autor, ejemplares FROM libros ORDER BY titulo"
                )
                filas = cursor.fetchall()

                if not filas:
                    console.print("[red]No hay libros registrados.[/red]")
                else:
                    console.print(
                        f"[bold green]{'ID':^6}[/bold green][bold blue]{'Titulo':^18}[/bold blue][bold magenta]{'Autor':^25}[/bold magenta][bold yellow]Ejemplares[/bold yellow]"
                    )
                    for fila in filas:
                        console.print(
                            f"[green]{fila['id']:>3}[/green] [blue]{fila['titulo'][:18]:^18}[/blue][magenta]{fila['autor'][:25]:^25}[/magenta] [yellow]{fila['ejemplares']}[/yellow]"
                        )
                    console.print(
                        "\n[bold cyan]==== FIN DEL INVENTARIO ====[/bold cyan]\n"
                    )
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
            console.print("Ingresa una opción valida")
    except ValueError:
        console.print("[red]Por favor, ingresa un número entero válido.[/red]")
    except KeyboardInterrupt:
        print("\nPrograma interrumpido por el usuario.")
        break
