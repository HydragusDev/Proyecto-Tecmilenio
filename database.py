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
    autor   TEXT NOT NULL
);
 
CREATE TABLE IF NOT EXISTS ejemplares (
    id        INTEGER PRIMARY KEY AUTOINCREMENT,
    libro_id  INTEGER NOT NULL REFERENCES libros(id),
    estado    TEXT NOT NULL DEFAULT 'disponible'
              CHECK (estado IN ('disponible', 'prestado', 'mantenimiento'))
);
 
CREATE TABLE IF NOT EXISTS prestamos (
    id                  INTEGER PRIMARY KEY AUTOINCREMENT,
    usuario_id          INTEGER NOT NULL REFERENCES usuarios(id),
    ejemplar_id         INTEGER NOT NULL REFERENCES ejemplares(id),
    estado              TEXT NOT NULL DEFAULT 'pendiente'
                        CHECK (estado IN ('pendiente', 'autorizado', 'rechazado', 'devuelto')),
    fecha_solicitud     TEXT NOT NULL DEFAULT (datetime('now')),
    fecha_autorizacion  TEXT,
    fecha_devolucion    TEXT
);
 
CREATE INDEX IF NOT EXISTS idx_ejemplares_libro  ON ejemplares(libro_id);
CREATE INDEX IF NOT EXISTS idx_ejemplares_estado ON ejemplares(estado);
CREATE INDEX IF NOT EXISTS idx_prestamos_usuario ON prestamos(usuario_id);
CREATE INDEX IF NOT EXISTS idx_prestamos_estado  ON prestamos(estado);
"""


def conectar() -> sqlite3.Connection:
    """Abre una conexion a bitacora.db (SQLite la crea sola si no existe)."""
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
