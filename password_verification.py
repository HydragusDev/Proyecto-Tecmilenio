import gc
import sys

import pwinput
from rich.console import Console
from rich.prompt import Prompt
from rich.style import Style

import database as db
from password_hasher import verify_password

console = Console()

error_style = Style(color="red", bold=True, blink=True)
check_style = Style(color="green", blink=True)


def verify_login_main_loop() -> dict | None:
    attempts = 0

    while True:
        try:
            console.print(
                "=== SISTEMA DE INICIO DE SESIÓN ===", style="bold blue"
            )
            input_mail = Prompt.ask("Correo electrónico").strip().lower()

            if not input_mail:
                console.print(
                    "El correo no puede estar vacío.", style=error_style
                )
                continue

            input_username = Prompt.ask("Nombre de usuario").strip()

            if not input_username:
                console.print(
                    "El nombre de usuario no puede estar vacío.",
                    style=error_style,
                )
                continue

            try:
                user_temp = db.obtain_from_mail(input_mail)
            except Exception as e:
                console.print(
                    f"Error al conectar con la base de datos: {e}",
                    style=error_style,
                )
                continue

            # FIX: Changed user_temp.get() to user_temp[] for sqlite3.Row compatibility
            if (
                user_temp is None
                or user_temp["username"] != input_username
            ):
                attempts += 1
                console.print(
                    f"Acceso denegado: Datos inválidos. Le quedan {3 - attempts} intentos.",
                    style=error_style,
                )
                if attempts >= 3:
                    console.print(
                        "Demasiados intentos fallidos. Saliendo del sistema...",
                        style=error_style,
                    )
                    sys.exit(1)
                continue

            password_input_bytes = pwinput.pwinput(
                "Contraseña > ", mask="*"
            ).encode("utf-8")

            stored_hash = user_temp["hashed_password"]

            if isinstance(stored_hash, (bytes, bytearray)):
                stored_hash = stored_hash.decode("utf-8", errors="ignore")

            verified = verify_password(stored_hash, password_input_bytes)

            if verified:
                console.print(
                    "\nAcceso concedido. Bienvenido al sistema.",
                    style=check_style,
                )
                return dict(user_temp)

            attempts += 1
            console.print(
                f"Acceso denegado: Datos inválidos. Le quedan {3 - attempts} intentos.",
                style=error_style,
            )

            if attempts >= 3:
                console.print(
                    "Demasiados intentos fallidos. Saliendo del sistema...",
                    style=error_style,
                )
                sys.exit(1)

        except KeyboardInterrupt:
            console.print("\nInicio de sesión cancelado.", style=error_style)
            sys.exit(0)

        finally:
            if "password_input_bytes" in locals():
                del password_input_bytes
            gc.collect()


if __name__ == "__main__":
    usuario = verify_login_main_loop()
    if usuario is not None:
        console.print(
            f"Sesión iniciada correctamente como: {usuario['role']} ({usuario['mail']})",
            style=check_style,
        )
