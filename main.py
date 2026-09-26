"""
Archivo principal.

Punto de entrada del sistema de biblioteca. Aqui vive el flujo de
arranque (pantalla de carga) y el menu inicial (login / registro /
salir)."""
# Imports

import sys
import threading
import time

#Rich system
from rich.console import Console
from rich.panel import Panel
from rich.progress import BarColumn, Progress, SpinnerColumn, TextColumn
from rich.prompt import Prompt
#Console object for rich system.


#Database and menu functions
import database as db
from menu_employee import open_main_menu_employee
from menu_user import open_main_menu_user
from password_registration import register_user
from password_verification import verify_login_main_loop


console = Console()

# For time out function
inactivity_timer = None
TIMEOUT_MINUTES = 5.0
TIMEOUT_SECONDS = TIMEOUT_MINUTES * 60


# Timeout Function(s)
def exit_on_timeout():
    print("El programa se esta cerrando debido a 5 minutos de inactividad.")
    sys.exit(0)


# Resets Timeout function timer on interaction
def reset_timer():
    global inactivity_timer

    if inactivity_timer is not None:
        inactivity_timer.cancel()

    inactivity_timer = threading.Timer(
        TIMEOUT_SECONDS, exit_on_timeout
    )  # Timer
    inactivity_timer.daemon = True  # background thread.
    inactivity_timer.start()


# Loading Screen function
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


# Main Menu
def main_menu() -> str:
    console.print(
        Panel.fit(
            "[bold]1.[/bold] Iniciar sesion\n"
            "[bold]2.[/bold] Registrarse\n"
            "[bold]3.[/bold] Salir",
            title="Biblioteca - Menu inicial",
            border_style="cyan",
        )
    )
    option = Prompt.ask("Elige una opción >", choices=["1", "2", "3"])

    # Option 1: Login
    if option == "1":
        user = (
            verify_login_main_loop()
        )  # Takes login function from password_verification

        if user is not None:
            if user["role"] == "employee_role":
                open_main_menu_employee()
            else:
                open_main_menu_user()

    # Option 2: Registering
    elif option == "2":
        register_user()  # Calls registration function from password_registration
        print("Regresando al menu principal...")

    # OPtion 3: Close
    elif option == "3":
        console.print(
            "[bold red]Cerrando el sistema...[/bold red]"
        )  # Closes program
    return option


# Main
def main() -> None:

    # Starts timer
    global inactivity_timer

    db.crear_tablas()
    mostrar_pantalla_carga()
    print(
        f"Nota: el programa se cerrará en {TIMEOUT_MINUTES} minutos de inactividad"
    )

    while True:
        try:
            # Opens main menu -> go to function
            option = main_menu()

            # otherwise
            # Closes program on choice within menu
            if option == "3":
                print("Cerrando el programa...")
                break
            
            #Cancels timer if still on by here
            if inactivity_timer is not None:
                inactivity_timer.cancel()
                inactivity_timer = None

        #Keyboard interrupt system exit.
        except (KeyboardInterrupt, SystemExit):
            if inactivity_timer is not None:
                inactivity_timer.cancel()
            break


if __name__ == "__main__":
    main()
