"""
Archivo Database.

Archivo encargado de la conexión con 'bitacora.db' y la creación de tablas
donde se guarda la información del usuario además del inventario.
"""

import sqlite3
from pathlib import Path

RUTA_BD = Path(__file__).parent / "bitacora.db"

DATABASE_BLUEPRINT = """
CREATE TABLE IF NOT EXISTS "libros" (
    "id"          INTEGER PRIMARY KEY AUTOINCREMENT,
    "titulo"      TEXT NOT NULL,
    "autor"       TEXT NOT NULL,
    "ejemplares"  INTEGER NOT NULL
);

CREATE TABLE IF NOT EXISTS "users" (
    "id"                    INTEGER PRIMARY KEY AUTOINCREMENT,
    "username"              TEXT NOT NULL,
    "mail"                  TEXT NOT NULL UNIQUE,
    "hashed_password"       BLOB NOT NULL, -- <-- CAMBIADO AQUÍ
    "role"                  TEXT NOT NULL CHECK("role" IN ('user_role', 'employee_role')),
    "accepted_terms"        INTEGER NOT NULL DEFAULT 0,
    "registered_date"       TEXT NOT NULL DEFAULT (datetime('now'))
);

CREATE TABLE IF NOT EXISTS "prestamos" (
    "id"                 INTEGER PRIMARY KEY AUTOINCREMENT,
    "id_libro"           INTEGER NOT NULL,
    "id_usuario"         INTEGER NOT NULL,
    "estado"             TEXT NOT NULL DEFAULT 'pendiente' CHECK("estado" IN ('pendiente', 'autorizado', 'rechazado', 'devuelto')),
    "fecha_solicitud"    TEXT NOT NULL DEFAULT (datetime('now')),
    "fecha_autorizacion" TEXT,
    "fecha_devolucion"   TEXT,
    "motivo_rechazo"     TEXT, 
    FOREIGN KEY("id_libro") REFERENCES "libros"("id"),
    FOREIGN KEY("id_usuario") REFERENCES "users"("id")
);
"""


def conectar() -> sqlite3.Connection:
    conexion = sqlite3.connect(RUTA_BD)
    conexion.execute("PRAGMA foreign_keys = ON;")
    return conexion


def crear_tablas() -> None:
    conexion = conectar()
    try:
        conexion.executescript(DATABASE_BLUEPRINT)
        conexion.commit()
    finally:
        conexion.close()


def verify_mail(mail: str) -> bool:
    """Verifica si un correo electrónico ya está registrado."""
    conexion = conectar()
    try:
        cursor = conexion.execute(
            "SELECT 1 FROM users WHERE mail = ?", (mail,)
        )
        return cursor.fetchone() is not None
    finally:
        conexion.close()


# Defines a user.
def user(
    username: str,
    mail: str,
    hashed_password: str,
    role: str,  # <-- CAMBIADO AQUÍ
) -> None:
    """Inserta un nuevo usuario en la base de datos."""
    conexion = conectar()
    try:
        conexion.execute(
            """
            INSERT INTO users (username, mail, hashed_password, role, accepted_terms) -- <-- CAMBIADO AQUÍ
            VALUES (?, ?, ?, ?, 1)
            """,
            (username, mail, hashed_password, role),
        )
        conexion.commit()
    finally:
        conexion.close()


def obtain_from_mail(mail: str) -> sqlite3.Row | None:
    """Busca y retorna toda la información de un usuario mediante su correo."""
    conexion = conectar()
    conexion.row_factory = sqlite3.Row
    try:
        cursor = conexion.execute(
            "SELECT * FROM users WHERE mail = ?", (mail,)
        )
        return cursor.fetchone()
    finally:
        conexion.close()


if __name__ == "__main__":
    crear_tablas()
    print(f"Tablas listas en: {RUTA_BD}")
