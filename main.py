"""
Archivo principal.

Punto de entrada del sistema de biblioteca. Aqui vive el flujo de
arranque (pantalla de carga) y el menu inicial (login / registro /
salir).
"""

import time

from email_validator import EmailNotValidError, validate_email
from rich.console import Console
from rich.panel import Panel
from rich.progress import BarColumn, Progress, SpinnerColumn, TextColumn
from rich.prompt import Prompt

import database as db

console = Console()


def mostrar_pantalla_carga(duracion_segundos: int = 5) -> None:

    with Progress(
        SpinnerColumn(),
        TextColumn("[bold cyan]Cargando sistema de biblioteca..."),
        BarColumn(),
        console=console,
        transient=True,
    ) as progress:
        tarea = progress.add_task("carga", total=100)
        pasos = 50
        for _ in range(pasos):
            time.sleep(duracion_segundos / pasos)
            progress.update(tarea, advance=100 / pasos)


def menu_inicial() -> str:
    console.print(
        Panel.fit(
            "[bold]1.[/bold] Iniciar sesion\n"
            "[bold]2.[/bold] Registrarse\n"
            "[bold]3.[/bold] Salir",
            title="Biblioteca - Menu inicial",
            border_style="cyan",
        )
    )
    return Prompt.ask("Elige una opcion", choices=["1", "2", "3"])


def iniciar_sesion() -> None:

    correo = Prompt.ask("Correo electronico")
    contrasena = Prompt.ask("Contrasena", password=True)

    usuario = db.obtener_usuario_por_correo(correo)

    if usuario is None:
        console.print("[red]Correo o contrasena incorrectos.[/red]")
        return

    # login_valido = verificar_contrasena(contrasena, usuario["contrasena_hash"], usuario["salt"])
    console.print(
        f"[yellow](Pendiente) Falta verificar la contrasena de {correo} "
        f"contra el hash guardado (rol: {usuario['rol']}).[/yellow]"
    )


def registrarse() -> None:
    while True:
        correo = Prompt.ask("Correo electronico")
        try:
            validate_email(correo)
            break
        except EmailNotValidError as e:
            print(str(e))
            console.print("Ingrese un correo electronico valido")
    if db.existe_correo(correo):
        console.print("[red]Ya existe una cuenta con ese correo.[/red]")
        return

    contrasena = Prompt.ask("Contrasena", password=True)
    confirmacion = Prompt.ask("Confirma tu contrasena", password=True)

    if contrasena != confirmacion:
        console.print("[red]Las contraseñas no coinciden.[/red]")
        return

    rol = Prompt.ask("Rol", choices=["usuario", "empleado"])


def main() -> None:
    db.crear_tablas()
    mostrar_pantalla_carga()

    while True:
        opcion = menu_inicial()

        if opcion == "1":
            iniciar_sesion()
        elif opcion == "2":
            registrarse()
        elif opcion == "3":
            console.print("[bold red]Cerrando el sistema...[/bold red]")
            break


if __name__ == "__main__":
    main()
