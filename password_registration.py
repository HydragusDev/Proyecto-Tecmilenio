import pwinput
from email_validator import EmailNotValidError, validate_email
from rich.console import Console
from rich.prompt import Prompt
from rich.style import Style

import database as db
from password_hasher import hash_password

console = Console()

error_style = Style(color="red", bold=True, blink=True)
check_style = Style(color="green", blink=True)


def register_user() -> None:
    while True:
        username = Prompt.ask("Nombre de usuario").strip()
        if not username:
            console.print(
                "El nombre de usuario no puede estar vacio.", style=error_style
            )
            continue
        break

    while True:
        mail = Prompt.ask("Correo electronico").strip().lower()

        if not mail:
            console.print("El correo no puede estar vacio.", style=error_style)
            continue

        # 1. Validar sintaxis del correo electrónico
        try:
            email_info = validate_email(mail, check_deliverability=False)
            mail = email_info.normalized
        except EmailNotValidError as e:
            console.print(
                f"Formato de correo inválido: {e}", style=error_style
            )
            continue

        # 2. Verificar existencia en la base de datos
        try:
            if db.verify_mail(mail):
                console.print(
                    "Ya existe una cuenta con ese correo.",
                    style=error_style,
                )
                continue
        except Exception as e:
            console.print(
                f"Error al verificar el correo: {e}", style=error_style
            )
            continue

        break

    while True:
        input_password = pwinput.pwinput("Contraseña > ", mask="*")
        input_confirmation = pwinput.pwinput(
            "Confirma tu contraseña > ", mask="*"
        )

        if not input_password:
            console.print(
                "La contraseña no puede estar vacia.", style=error_style
            )
            continue

        if input_password != input_confirmation:
            console.print("Las contraseñas no coinciden.", style=error_style)
            continue

        password_bytes = input_password.encode("utf-8")
        hashed_password = hash_password(password_bytes)
        break

    role = Prompt.ask("Rol >", choices=["usuario", "empleado"])
    role_map = {"usuario": "user_role", "empleado": "employee_role"}
    role = role_map[role]

    # Saved in the database within a try except block
    try:
        db.user(username, mail, hashed_password, role)
        console.print(
            f"Cuenta creada correctamente para {username}.", style=check_style
        )
    except Exception as e:
        console.print(
            f"Error al registrar el usuario en la base de datos: {e}",
            style=error_style,
        )
