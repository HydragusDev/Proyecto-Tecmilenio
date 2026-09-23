"""
Archivo principal.

Punto de entrada del sistema de biblioteca. Aqui vive el flujo de
arranque (pantalla de carga) y el menu inicial (login / registro /
<<<<<<< HEAD
salir).
"""

import time

from email_validator import EmailNotValidError, validate_email
=======
salir)."""
#Imports


#Ther's not an email validator?????? What is this
#from email_validator import EmailNotValidError, validate_email
>>>>>>> 34c42708b804dd71823fb673c846df56362d3f6c
from rich.console import Console
from rich.panel import Panel
from rich.progress import BarColumn, Progress, SpinnerColumn, TextColumn
from rich.prompt import Prompt

import database as db

<<<<<<< HEAD
console = Console()


=======
#Allows to run other files
import os
import runpy

console = Console()

# For time out function
import threading
import sys
import time


#Time out function configuration.
inactivity_timer =None
TIMEOUT_MINUTES = 5.0
TIMEOUT_SECONDS = TIMEOUT_MINUTES * 60

#Timeout Function
def exit_on_timeout():
    print("No interaction in 5 minutes detected, closing program")
    sys.exit(0)

#Resets Timeout function timer on interaction
def reset_timer():
    global inactivity_timer

    if inactivity_timer is not None:
        inactivity_timer.cancel()

    #Creates new timer thread
    inactivity_timer = threading.Timer(TIMEOUT_SECONDS, exit_on_timeout)
    inactivity_timer.daemon = True #Allows exit smoothly out the multithread
    inactivity_timer.start()


#Loading Screen function
>>>>>>> 34c42708b804dd71823fb673c846df56362d3f6c
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

<<<<<<< HEAD

=======
#Main Menu
>>>>>>> 34c42708b804dd71823fb673c846df56362d3f6c
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
<<<<<<< HEAD
    return Prompt.ask("Elige una opcion", choices=["1", "2", "3"])


=======
    option = Prompt.ask("Elige una opcion", choices=["1", "2", "3"])
    if option == "1":

        iniciar_sesion()

    elif option == "2":

        registrarse()

    elif option == "3":

        console.print("[bold red]Cerrando el sistema...[/bold red]")
    return option

"""
#Password (old)
>>>>>>> 34c42708b804dd71823fb673c846df56362d3f6c
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


<<<<<<< HEAD
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
=======

"""

#Missing functions iniciar_Sesion()
def iniciar_sesion():
    print(f"'iniciar_sesion():' has been called")

    #Runs verification
    runpy.run_path(os.path.join(os.path.dirname(__file__), "hash_password_verification.py"))


    input_menu = int(input("""Choose an Option. 1- Employee Menu.  2- User menu. > """))

    #Runs employee menu
    if input_menu == 1:
        print("Running Employee menu")
        runpy.run_path(os.path.join(os.path.dirname(__file__), "menu_employe.py"))

    #Runs user menu
    elif input_menu == 2:
        print("Running User menu")
        runpy.run_path(os.path.join(os.path.dirname(__file__), "menu_user.py"))
    
    


def registrarse():
    print(f"'registrarse()' has been called")



#Main
def main() -> None:
    db.crear_tablas()
    mostrar_pantalla_carga()
    print(f"Note, this program will close in {TIMEOUT_MINUTES} minutes of inactivity")

    while True:
        try:
            # Main loop with timer active.
            #2. Runs main menu.
            
            #Runs menu_inicial and checks for option clicked
            option = menu_inicial()
            print("Exiting Program")
            if inactivity_timer:
                inactivity_timer.cancel()
                sys.exit


                break
            break
                

        except (KeyboardInterrupt, SystemExit):
        #ctrl+c or sys.exit trigger cleanup:
            if inactivity_timer:
                    inactivity_timer.cancel()
        #Exits
        break

sys.exit

if __name__ == "__main__":
    main()




>>>>>>> 34c42708b804dd71823fb673c846df56362d3f6c
