"""
Archivo Database.

Archivo encargado de la conección con 'bitacora.db' y la creación de tablas donde se guarda la información del usuario ademas del inventario.
"""

import sqlite3
from pathlib import Path

RUTA_BD = Path(__file__).parent / "bitacora.db"

ESQUEMA = """
PRAGMA foreign_keys = ON;
 
CREATE TABLE IF NOT EXISTS usuarios (
    id               INTEGER PRIMARY KEY AUTOINCREMENT,
    correo           TEXT NOT NULL UNIQUE,
    contrasena_hash  BLOB NOT NULL,
    salt             BLOB NOT NULL,
    rol              TEXT NOT NULL CHECK (rol IN ('usuario', 'empleado')),
    acepto_terminos  INTEGER NOT NULL DEFAULT 0,
    fecha_registro   TEXT NOT NULL DEFAULT (datetime('now'))
);
 
CREATE TABLE IF NOT EXISTS libros (
    id      INTEGER PRIMARY KEY AUTOINCREMENT,
    titulo  TEXT NOT NULL,
    autor   TEXT NOT NULL,
    ejemplares INTEGER NOT NULL
);
 
"""


def conectar() -> sqlite3.Connection:

    conexion = sqlite3.connect(RUTA_BD)

    conexion.execute("PRAGMA foreign_keys = ON;")

    return conexion


def crear_tablas() -> None:
    conexion = conectar()
    try:
        conexion.executescript(ESQUEMA)

        conexion.commit()

    finally:
        conexion.close()


def existe_correo(correo: str) -> bool:
    conexion = conectar()
    try:
        cursor = conexion.execute(
            "SELECT 1 FROM usuarios WHERE correo = ?", (correo,)
        )

        return cursor.fetchone() is not None
    finally:
        conexion.close()


def registrar_usuario(
    correo: str, contrasena_hash: bytes, salt: bytes, rol: str
) -> None:
    conexion = conectar()
    try:
        conexion.execute(
            """
            INSERT INTO usuarios (correo, contrasena_hash, salt, rol, acepto_terminos)
            VALUES (?, ?, ?, ?, 1)
            """,
            (correo, contrasena_hash, salt, rol),
        )
        conexion.commit()
    finally:
        conexion.close()


def obtener_usuario_por_correo(correo: str) -> sqlite3.Row | None:
    conexion = conectar()

    conexion.row_factory = sqlite3.Row

    try:
        cursor = conexion.execute(
            "SELECT * FROM usuarios WHERE correo = ?", (correo,)
        )
        return cursor.fetchone()
    finally:
        conexion.close()


if __name__ == "__main__":
    crear_tablas()
    print(f"Tablas listas en: {RUTA_BD}")
