import os

from rich.console import Console
from rich.prompt import Prompt

import database as db
from password_hasher import hash_password

console = Console()

import pwinput

def register_user() -> None:
    while True:
        username = Prompt.ask("Nombre de usuario").strip()
        if not username:
            console.print("[red]El nombre de usuario no puede estar vacio.[/red]")
            continue
        break

    while True:
        mail = Prompt.ask("Correo electronico").strip().lower()

        if not mail:
            console.print("[red]El correo no puede estar vacio.[/red]")
            continue

        if db.verify_mail(mail):
            console.print("[red]Ya existe una cuenta con ese correo.[/red]")
            continue

        break

    while True:
        # Changed to pwinput to show masking characters (e.g., *)
        input_password = pwinput.pwinput("Contrasena > ", mask="*")
        input_confirmation = pwinput.pwinput("Confirma tu contrasena > ", mask="*")

        if not input_password:
            console.print("[red]La contraseña no puede estar vacia.[/red]")
            continue

        if input_password != input_confirmation:
            console.print("[red]Las contraseñas no coinciden.[/red]")
            continue

        # Convert to bytes after confirming they match
        password_bytes = input_password.encode("utf-8")

        # Hash the password
        hashed_password = hash_password(password_bytes)

        break

    

    role = Prompt.ask(
        "Role >",
        choices=["usuario", "empleado"]
    )

    role_map = {
        "usuario": "user_role",
        "empleado": "employee_role"
    }

    role = role_map[role]

    db.user(
        username,
        mail,
        hashed_password,
        role
    )

    console.print(
        f"[green]Cuenta creada correctamente para {username}.[/green]")
