"""
Módulo de Gestión y Menú para Empleados de la Biblioteca.

Este archivo concentra la interfaz administrativa y operativa destinada
al personal de la biblioteca (bibliotecarios, auxiliares y administradores).
Permite gestionar el catálogo físico de libros (ingreso de nuevos títulos,
modificación de información existente, eliminación de bajas de inventario y
consulta de existencias), así como supervisar el flujo de préstamos (revisar
solicitudes pendientes, autorizarlas verificando existencias, rechazarlas con
motivo justificado y registrar las devoluciones efectivas).

Estructura y diseño pedagógico:
- Interfaz gráfica en consola desarrollada con la biblioteca Rich.
- Encabezados decorativos en arte ASCII con PyFiglet.
- Conexión relacional robusta con SQLite mediante el módulo database.
- Manejo transaccional (commit/rollback) para garantizar consistencia.
- Arquitectura de navegación con retorno seguro en todos los submenús.

Convención de Better Comments utilizada en el código:
# * [Información clave]: Conceptos y operaciones estructurales del sistema.
# ! [Advertencia / Cuidado]: Puntos de validación y control de errores.
# ? [Explicación didáctica]: Detalles formativos para no programadores.
# TODO: [Mantenimiento futuro]: Mejoras recomendadas a mediano plazo.
"""

# * =========================================================================
# * SECCIÓN DE IMPORTACIONES Y LIBRERÍAS
# * =========================================================================
# sqlite3 permite interactuar con el motor de base de datos embebido.
# Maneja tablas relacionales (libros, usuarios, prestamos) localmente.
import sqlite3

# sys ofrece utilidades del sistema operativo e intérprete, como sys.exit(0)
# para terminar el proceso de manera controlada y sin errores.
import sys

# pyfiglet transforma cadenas de texto simples en arte tipográfico ASCII.
from pyfiglet import figlet_format

# Rich es una biblioteca moderna para estilizar texto en la terminal:
# proporciona paneles decorativos, tablas estructuradas y estilos cromáticos.
from rich.console import Console
from rich.panel import Panel
from rich.style import Style
from rich.table import Table

# Importamos nuestro propio módulo de base de datos para la conexión.
import database as db

# * Creamos la instancia principal de la consola de Rich.
# Todas las salidas visuales con colores pasarán por este objeto console.
console = Console()

# * Estilo visual para errores: color rojo en negrita con parpadeo suave.
# Alerta visualmente al operador cuando un dato ingresado no es válido.
error_style = Style(color="red", bold=True, blink=True)

# * Estilo visual para confirmaciones: color verde con parpadeo suave.
# Se usa para notificar que un registro fue guardado o actualizado con éxito.
check_style = Style(color="green", blink=True)


def menu_empleado_ascci():
    """
    Muestra el título del menú de empleado en arte ASCII con PyFiglet.

    Toma el texto representativo y mediante pyfiglet lo transforma en
    un encabezado gráfico de gran tamaño visible en la terminal.

    Args:
        No requiere argumentos.

    Returns:
        None.

    Raises:
        Exception: Si pyfiglet no puede renderizar la tipografía estándar.

    Examples:
        Imprime 'MENU DE EMPLEADO' en arte ASCII.
    """
    # * Imprimimos el título en dos bloques para respetar el ancho estándar.
    # ? Cada bloque dibuja una palabra completa con la fuente 'standard'.
    try:
        print(figlet_format("MENU  DE", font="standard"))
        print(figlet_format("EMPLEADO", font="standard"))
    except Exception as e:
        # ! Si falla la generación artística, informamos sin romper el flujo.
        console.print(
            f"Error al generar el título ASCII: {e}", style=error_style
        )


def opciones_empleado():
    """
    Despliega el menú principal con las opciones para el empleado.

    Construye un panel delimitado en color cian mediante Rich Panel,
    mostrando las siete acciones disponibles: gestión de libros,
    revisión de préstamos, cierre de sesión y salida definitiva.

    Args:
        No requiere argumentos.

    Returns:
        None.

    Raises:
        Exception: Si ocurre un error al dibujar el panel en terminal.

    Examples:
        Muestra el panel de opciones de empleado del 1 al 7.
    """
    # * Panel cian con las opciones principales de administración.
    # ? Dividimos el texto en fragmentos cortos para no rebasar 77 columnas.
    try:
        console.print(
            Panel(
                "[bold white]"
                "1. Ingresar Libro\n"
                "2. Modificar Libro\n"
                "3. Borrar Libro\n"
                "4. Ver Inventario\n"
                "5. Ver Solicitudes de Prestamos\n"
                "6. Cerrar Sesión\n"
                "7. Salir"
                "[/bold white]",
                title="OPCIONES",
                border_style="cyan",
                expand=False,
            )
        )
    except Exception as e:
        # ! Notificamos al usuario si la consola de Rich experimenta un fallo.
        console.print(f"Error al mostrar el menú: {e}", style=error_style)


def ver_inventario(conexion):
    """
    Consulta y despliega el inventario completo de libros en una tabla.

    Ejecuta un SELECT sobre la tabla libros y genera una tabla estilizada
    de Rich con columnas para ID, Título, Autor y Ejemplares totales.

    Args:
        conexion (sqlite3.Connection): Conexión activa a bitacora.db.

    Returns:
        None.

    Raises:
        sqlite3.Error: Si ocurre un error en la lectura de la base de datos.
        Exception: En caso de cualquier error imprevisto de ejecución.

    Examples:
        Muestra la tabla completa de libros registrados en la biblioteca.
    """
    try:
        # ? Consultamos ID, título, autor y existencias ordenados por ID.
        # ORDER BY id garantiza una presentación cronológica y ordenada.
        cursor = conexion.execute(
            "SELECT id, titulo, autor, ejemplares FROM libros ORDER BY id"
        )
        filas = cursor.fetchall()

        # ! Si la tabla no contiene registros, informamos amablemente.
        if not filas:
            console.print("No hay libros registrados.", style=error_style)
        else:
            # * Creamos la estructura visual de la tabla de inventario.
            tabla = Table(
                title="[bold white]Inventario de Libros[/bold white]"
            )
            # Definimos cada columna con su nombre, alineación y color.
            tabla.add_column("ID", justify="center", style="green")
            tabla.add_column("Título", justify="center", style="blue")
            tabla.add_column("Autor", justify="center", style="magenta")
            tabla.add_column("Ejemplares", justify="center", style="yellow")

            # ? Iteramos sobre los registros convirtiendo cada campo a texto.
            for fila in filas:
                # El formato :04d rellena con ceros a la izquierda (ej. 0005).
                id_libro = f"{int(fila['id']):04d}"
                tabla.add_row(
                    id_libro,
                    str(fila["titulo"]),
                    str(fila["autor"]),
                    str(fila["ejemplares"]),
                )
            # Imprimimos la tabla formateada en la terminal.
            console.print(tabla)
    except sqlite3.Error as e:
        # ! Capturamos fallos específicos de la base de datos SQLite.
        console.print(
            f"Error de base de datos al consultar el inventario: {e}",
            style=error_style,
        )
    except Exception as e:
        # Capturamos cualquier otra excepción general para no colapsar.
        console.print(
            f"Error inesperado al ver inventario: {e}", style=error_style
        )


def insertar_libro(conexion):
    """
    Permite al empleado dar de alta nuevos libros en el inventario.

    Solicita título, autor y cantidad de ejemplares, ejecuta un INSERT
    en la tabla libros y confirma la transacción. Permite registrar
    múltiples libros consecutivamente o cancelar para volver al menú.

    Args:
        conexion (sqlite3.Connection): Conexión activa a la base de datos.

    Returns:
        None.

    Raises:
        sqlite3.Error: Si la sentencia INSERT falla en la base de datos.
        Exception: En caso de errores inesperados durante la captura.

    Examples:
        Ingresa el libro 'Cien Años de Soledad' de 'Gabriel García Márquez'.
    """
    # Contador de libros registrados durante esta sesión de captura.
    libros_agregados = 0

    # * Bucle principal de captura que permite agregar varios libros seguidos.
    while True:
        try:
            # * 1. Solicitamos el título con opción explícita de cancelar.
            # ? Escribir '0' o 'volver' retorna inmediatamente al menú padre.
            titulo_input = input(
                "Ingresa el título del libro "
                "(o '0'/'volver' para regresar al menú principal): "
            ).strip()
            if titulo_input.lower() in ("0", "volver", "cancelar", "salir"):
                console.print("Regresando al menú principal...")
                return
            if not titulo_input:
                console.print(
                    "El título no puede estar vacío.", style=error_style
                )
                continue
            # .title() pone en mayúscula la primera letra de cada palabra.
            titulo_nuevo = titulo_input.title()

            # * 2. Solicitamos el nombre del autor de la obra.
            autor_input = input(
                "Ingresa el nombre del autor del libro "
                "(o 'cancelar' para volver): "
            ).strip()
            if autor_input.lower() in ("0", "volver", "cancelar", "salir"):
                console.print(
                    "Operación cancelada. Regresando al menú principal..."
                )
                return
            if not autor_input:
                console.print(
                    "El autor no puede estar vacío.", style=error_style
                )
                continue
            autor_nuevo = autor_input.title()

            # * 3. Solicitamos la cantidad de ejemplares físicos disponibles.
            try:
                ejemplares_nuevo = int(
                    input("Ingresa los ejemplares que tenemos en existencia: ")
                )
                if ejemplares_nuevo < 0:
                    console.print(
                        "Los ejemplares no pueden ser negativos.",
                        style=error_style,
                    )
                    continue
            except ValueError:
                # ! Validamos que el empleado ingrese un número entero real.
                console.print(
                    "Debes ingresar un número válido.", style=error_style
                )
                continue

            # * 4. Ejecutamos la inserción SQL con parámetros seguros (?).
            # Usar '?' previene que caracteres especiales rompan la consulta.
            conexion.execute(
                "INSERT INTO libros (titulo, autor, ejemplares) "
                "VALUES (?, ?, ?)",
                (titulo_nuevo, autor_nuevo, ejemplares_nuevo),
            )
            # Guardamos los cambios definitivamente en el archivo de base de datos.
            conexion.commit()
            libros_agregados += 1
            console.print("Libro agregado correctamente", style=check_style)

            # * 5. Preguntamos si el empleado desea registrar otro libro más.
            while True:
                otro_libro = (
                    input("¿Deseas ingresar otro libro? (s/n): ")
                    .strip()
                    .lower()
                )
                if otro_libro in ("si", "sí", "s", "y", "yes"):
                    # Rompe el sub-bucle y vuelve al inicio del bucle while.
                    break
                elif otro_libro in ("no", "n", "volver", "salir", "0"):
                    # Si no desea agregar más, informamos total y salimos.
                    if libros_agregados > 0:
                        console.print(
                            f"Has agregado {libros_agregados} "
                            "libro(s) correctamente.",
                            style=check_style,
                        )
                    return
                else:
                    console.print(
                        "Ingresa una opción válida", style=error_style
                    )
        except sqlite3.Error as e:
            # ! En caso de error revertimos la transacción para evitar datos corruptos.
            conexion.rollback()
            console.print(
                f"Error de base de datos al insertar el libro: {e}",
                style=error_style,
            )
        except Exception as e:
            console.print(
                f"Error inesperado al insertar el libro: {e}",
                style=error_style,
            )


def ver_prestamos(conexion):
    """
    Consulta y muestra todos los préstamos registrados en el sistema.

    Construye una tabla informativa con ID de préstamo, ID de libro,
    ID de usuario, estado actual, fechas relevantes y notas de rechazo.

    Args:
        conexion (sqlite3.Connection): Conexión activa a la base de datos.

    Returns:
        bool: True si hay préstamos para mostrar, False si no hay o falla.

    Raises:
        sqlite3.Error: Si ocurre un problema al consultar la tabla prestamos.
        Exception: En caso de error imprevisto.

    Examples:
        Despliega la bitácora completa de préstamos y solicitudes activas.
    """
    try:
        # ? Consultamos todas las columnas necesarias de la tabla prestamos.
        cursor = conexion.execute(
            "SELECT id, id_libro, id_usuario, estado, fecha_solicitud, "
            "fecha_autorizacion, fecha_devolucion, motivo_rechazo "
            "FROM prestamos ORDER BY id"
        )
        filas = cursor.fetchall()

        # ! Si no hay registros de préstamo, informamos y retornamos False.
        if not filas:
            console.print("No hay préstamos registrados.", style=error_style)
            return False

        # * Estructuramos la tabla visual para auditoría de solicitudes.
        tabla = Table(title="[bold white]Menú Préstamos[/bold white]")
        tabla.add_column("ID", justify="center", style="green")
        tabla.add_column("ID Libro", justify="center", style="blue")
        tabla.add_column("ID Usuario", justify="center", style="blue")
        tabla.add_column("Estado", justify="center", style="green")
        tabla.add_column(
            "Fecha de Solicitud", justify="center", style="yellow"
        )
        tabla.add_column(
            "Fecha de Autorización", justify="center", style="yellow"
        )
        tabla.add_column(
            "Fecha de Devolución", justify="center", style="yellow"
        )
        tabla.add_column("Notas", justify="center", style="magenta")

        # Poblamos cada renglón con los datos formateados del préstamo.
        for fila in filas:
            id_prestamo = f"{int(fila['id']):04d}"
            tabla.add_row(
                id_prestamo,
                str(fila["id_libro"]),
                str(fila["id_usuario"]),
                str(fila["estado"]),
                str(fila["fecha_solicitud"]),
                str(fila["fecha_autorizacion"]),
                str(fila["fecha_devolucion"]),
                str(fila["motivo_rechazo"]),
            )
        console.print(tabla)
        return True
    except sqlite3.Error as e:
        # ! Advertencia en caso de fallo al leer préstamos.
        console.print(
            f"Error de base de datos al consultar préstamos: {e}",
            style=error_style,
        )
        return False
    except Exception as e:
        console.print(
            f"Error inesperado al consultar préstamos: {e}",
            style=error_style,
        )
        return False


def opciones_solicitud_prestamo():
    """
    Abre las opciones para gestionar una solicitud de préstamo concreta.

    Despliega un panel verde con las tres decisiones que un empleado puede
    tomar ante un préstamo pendiente: autorizarlo (si hay stock libre),
    rechazarlo (especificando motivo) o volver a la lista de solicitudes.

    Args:
        No requiere argumentos.

    Returns:
        None.

    Raises:
        Exception: Puede dar error si Rich no puede renderizar el panel.

    Examples:
        Muestra: 1. Autorizar, 2. Rechazar, 3. Volver a Solicitudes.
    """
    # * Panel verde para la toma de decisiones sobre préstamos.
    # ? La opción 3 permite cancelar la acción actual y volver al listado.
    try:
        console.print(
            Panel(
                "[bold white]"
                "1. Autorizar\n"
                "2. Rechazar\n"
                "3. Volver a Solicitudes"
                "[/bold white]",
                title="SOLICITUD DE PRÉSTAMO",
                border_style="green",
                expand=False,
            )
        )
    except Exception as e:
        console.print(
            f"Error al mostrar las opciones de préstamo: {e}",
            style=error_style,
        )


def gestionar_solicitudes(conexion):
    """
    Permite al empleado atender solicitudes de préstamo activas.

    Muestra el listado de préstamos, solicita el ID del préstamo a gestionar,
    evalúa su estado actual (rechazado, devuelto, autorizado o pendiente)
    y permite autorizar, rechazar o registrar la devolución del libro.

    Args:
        conexion (sqlite3.Connection): Conexión activa a la base de datos.

    Returns:
        None.

    Raises:
        sqlite3.Error: Si ocurre un problema de base de datos al actualizar.
        Exception: En caso de error general en la interacción.

    Examples:
        Gestiona la solicitud 0003 autorizando o devolviendo el ejemplar.
    """
    # Contador de solicitudes atendidas durante la sesión del empleado.
    solicitudes_atendidas = 0

    # * Bucle para revisar y atender varias solicitudes consecutivamente.
    while True:
        try:
            # Primero mostramos la tabla completa de préstamos.
            hay_prestamos = ver_prestamos(conexion)
            if not hay_prestamos:
                # Si no hay préstamos, salimos hacia el menú de empleado.
                return

            # * Solicitamos el ID de la solicitud con opción explícita de volver.
            # ? Escribir '0' o 'volver' retorna al menú principal de empleado.
            id_input = input(
                "\nIngresa el ID de la solicitud que deseas atender "
                "(o '0'/'volver' para regresar al menú principal): "
            ).strip()

            if id_input.lower() in ("0", "cancelar", "volver", "salir"):
                console.print("Regresando al menú principal...")
                return

            try:
                id_prestamo = int(id_input)
            except ValueError:
                # ! Validamos entrada numérica para prevenir fallos.
                console.print(
                    "Por favor, ingresa un número entero válido.",
                    style=error_style,
                )
                continue

            # ? Consultamos el préstamo uniendo (LEFT JOIN) el título del libro.
            # Esto permite saber qué libro físico corresponde al préstamo.
            cursor = conexion.execute(
                "SELECT p.id, p.id_libro, p.id_usuario, p.estado, "
                "p.fecha_solicitud, p.fecha_autorizacion, "
                "p.fecha_devolucion, l.titulo AS titulo_libro "
                "FROM prestamos p "
                "LEFT JOIN libros l ON p.id_libro = l.id "
                "WHERE p.id = ?",
                (id_prestamo,),
            )
            fila = cursor.fetchone()

            if fila is None:
                console.print(
                    "No se ha encontrado una solicitud con ese ID.",
                    style=error_style,
                )
                continue

            # Extraemos el título del libro o un valor de respaldo si es nulo.
            titulo = (
                fila["titulo_libro"]
                if fila["titulo_libro"]
                else "(Libro no encontrado)"
            )

            # * Caso A: La solicitud ya había sido rechazada previamente.
            if fila["estado"] == "rechazado" or fila["estado"] == "devuelto":
                console.print(
                    f"La solicitud {int(fila['id']):04d} ya está en "
                    f'estado "{fila["estado"]}".',
                    style=error_style,
                )
                continue

            # * Caso C: El libro está autorizado y en posesión del usuario.
            elif fila["estado"] == "autorizado":
                console.print(
                    f"La solicitud {int(fila['id']):04d} del usuario "
                    f'{fila["id_usuario"]} para el libro "{titulo}" '
                    "ya está autorizada."
                )
                # Preguntamos si el libro ya fue entregado físicamente.
                devuelto = (
                    input(
                        f'¿Confirmas que el libro "{titulo}" fue devuelto? '
                        '(s/n, o "volver" para cancelar): '
                    )
                    .strip()
                    .lower()
                )

                if devuelto in ("si", "sí", "s", "y", "yes"):
                    # ? Actualizamos el estado a 'devuelto' y guardamos fecha.
                    conexion.execute(
                        "UPDATE prestamos SET estado = 'devuelto', "
                        "motivo_rechazo = 'Devuelto correctamente el ' || "
                        "strftime('%d/%m/%Y', 'now') WHERE id = ?",
                        (fila["id"],),
                    )
                    conexion.commit()
                    console.print(
                        "Libro marcado como devuelto exitosamente.",
                        style=check_style,
                    )
                    solicitudes_atendidas += 1
                else:
                    # Cancelamos y regresamos al listado de préstamos.
                    console.print(
                        "Operación cancelada. "
                        "Regresando a la lista de solicitudes..."
                    )
                    continue

            # * Caso D: La solicitud está pendiente de aprobación.
            else:
                console.print(
                    f"La solicitud seleccionada es la {int(fila['id']):04d} "
                    f"del usuario {fila['id_usuario']} para el libro "
                    f'"{titulo}".'
                )

                # Sub-bucle para que el empleado decida: autorizar o rechazar.
                cancelado = False
                while True:
                    opciones_solicitud_prestamo()
                    opcion_input = input("¿Qué deseas hacer? (1-3): ").strip()
                    # ? Si elige 3, 'cancelar' o 'volver', regresa al listado.
                    if opcion_input.lower() in (
                        "3",
                        "cancelar",
                        "volver",
                        "salir",
                    ):
                        console.print(
                            "Atención de solicitud cancelada. "
                            "Regresando a la lista de solicitudes..."
                        )
                        cancelado = True
                        break

                    try:
                        opcion_solicitud = int(opcion_input)
                    except ValueError:
                        console.print(
                            "Por favor, ingresa un número entero válido.",
                            style=error_style,
                        )
                        continue

                    # 1. Autorizar la solicitud
                    if opcion_solicitud == 1:
                        if autorizar_prestamo(conexion, fila):
                            solicitudes_atendidas += 1
                        break
                    # 2. Rechazar la solicitud
                    elif opcion_solicitud == 2:
                        if rechazar_prestamo(conexion, fila):
                            solicitudes_atendidas += 1
                        break
                    else:
                        console.print(
                            "Ingresa una opción válida", style=error_style
                        )

                # Si canceló, volvemos a mostrar el listado de préstamos.
                if cancelado:
                    continue

            # Preguntamos si desea gestionar otra solicitud más.
            otra_solicitud = (
                input("\n¿Deseas atender otra solicitud? (s/n): ")
                .strip()
                .lower()
            )
            if otra_solicitud not in ("si", "sí", "s", "y", "yes"):
                if solicitudes_atendidas > 0:
                    console.print(
                        f"Has atendido {solicitudes_atendidas} "
                        "solicitud(es) correctamente.",
                        style=check_style,
                    )
                # Retorna al menú principal de empleado.
                break
        except sqlite3.Error as e:
            conexion.rollback()
            console.print(
                f"Error de base de datos al gestionar solicitudes: {e}",
                style=error_style,
            )
        except Exception as e:
            console.print(
                f"Error inesperado al gestionar solicitudes: {e}",
                style=error_style,
            )


def autorizar_prestamo(conexion, fila):
    """
    Verifica disponibilidad y actualiza el préstamo a estado 'autorizado'.

    Comprueba que el libro asociado tenga ejemplares libres antes de
    proceder. Solicita confirmación al empleado, actualiza la fecha de
    autorización al momento actual y guarda los cambios en la base de datos.

    Args:
        conexion (sqlite3.Connection): Conexión activa a la base de datos.
        fila (sqlite3.Row | dict): Datos de la solicitud y del libro.

    Returns:
        bool: True si se autorizó exitosamente, False si se canceló o falló.

    Raises:
        sqlite3.Error: Si ocurre un problema al actualizar el registro.
        Exception: En caso de error imprevisto.

    Examples:
        Autoriza la solicitud de préstamo de un libro disponible.
    """
    try:
        # * 1. Comprobamos la cantidad total de ejemplares que posee el libro.
        cursor = conexion.execute(
            "SELECT ejemplares FROM libros WHERE id = ?", (fila["id_libro"],)
        )
        fila_libro = cursor.fetchone()

        if fila_libro is None:
            console.print(
                "No se encontró el libro asociado a esta solicitud.",
                style=error_style,
            )
            return False

        # * 2. Contamos cuántos ejemplares están autorizados actualmente.
        cursor_conteo = conexion.execute(
            "SELECT COUNT(*) FROM prestamos "
            "WHERE id_libro = ? AND estado = 'autorizado'",
            (fila["id_libro"],),
        )
        prestados = cursor_conteo.fetchone()[0]
        disponibles = fila_libro["ejemplares"] - prestados

        # ! Si no hay ejemplares disponibles en físico, no se puede autorizar.
        if disponibles <= 0:
            console.print(
                "No hay ejemplares disponibles de este libro.",
                style=error_style,
            )
            return False

        # * 3. Pedimos confirmación expresa al empleado antes de autorizar.
        while True:
            confirmar = (
                input(
                    "¿Confirmas que deseas autorizar esta solicitud? (s/n): "
                )
                .strip()
                .lower()
            )
            if confirmar in ("si", "sí", "s", "y", "yes"):
                # ? Actualizamos el estado a 'autorizado' y marcamos timestamp.
                conexion.execute(
                    "UPDATE prestamos SET estado = 'autorizado', "
                    "fecha_autorizacion = datetime('now') WHERE id = ?",
                    (fila["id"],),
                )
                conexion.commit()
                console.print(
                    "Solicitud autorizada correctamente.", style=check_style
                )
                return True
            elif confirmar in ("no", "n", "cancelar", "volver"):
                console.print("Autorización cancelada.")
                return False
            else:
                console.print("Ingresa una opción válida", style=error_style)
    except sqlite3.Error as e:
        conexion.rollback()
        console.print(
            f"Error de base de datos al autorizar préstamo: {e}",
            style=error_style,
        )
        return False
    except Exception as e:
        console.print(
            f"Error inesperado al autorizar préstamo: {e}",
            style=error_style,
        )
        return False


def rechazar_prestamo(conexion, fila):
    """
    Solicita el motivo de rechazo y cambia el préstamo a estado 'rechazado'.

    Pide al empleado una justificación (por ejemplo 'Sin stock' o 'Sanción'),
    confirma la decisión y actualiza la fila correspondiente en prestamos.

    Args:
        conexion (sqlite3.Connection): Conexión activa a la base de datos.
        fila (sqlite3.Row | dict): Datos de la solicitud que será rechazada.

    Returns:
        bool: True si se rechazó exitosamente, False si se canceló o falló.

    Raises:
        sqlite3.Error: Si falla la actualización en la tabla prestamos.
        Exception: En caso de error imprevisto.

    Examples:
        Rechaza un préstamo con motivo 'El usuario tiene adeudos previos'.
    """
    try:
        # * Solicitamos al empleado una razón clara para el rechazo.
        motivo_rechazo = input(
            "Ingresa el motivo del rechazo (o 'cancelar' para volver): "
        ).strip()
        if motivo_rechazo.lower() in ("0", "cancelar", "volver", "salir"):
            console.print("Rechazo cancelado.")
            return False

        if not motivo_rechazo:
            console.print(
                "Debes ingresar un motivo de rechazo.", style=error_style
            )
            return False

        # * Pedimos confirmación antes de guardar el rechazo definitivo.
        while True:
            confirmar = (
                input("¿Confirmas que deseas rechazar esta solicitud? (s/n): ")
                .strip()
                .lower()
            )
            if confirmar in ("si", "sí", "s", "y", "yes"):
                # ? Guardamos estado = 'rechazado' y la nota explicativa.
                conexion.execute(
                    "UPDATE prestamos SET estado = 'rechazado', "
                    "motivo_rechazo = ? WHERE id = ?",
                    (motivo_rechazo, fila["id"]),
                )
                conexion.commit()
                console.print(
                    "Solicitud rechazada correctamente.", style=check_style
                )
                return True
            elif confirmar in ("no", "n", "cancelar", "volver"):
                console.print("Rechazo cancelado.")
                return False
            else:
                console.print("Ingresa una opción válida", style=error_style)
    except sqlite3.Error as e:
        conexion.rollback()
        console.print(
            f"Error de base de datos al rechazar préstamo: {e}",
            style=error_style,
        )
        return False
    except Exception as e:
        console.print(
            f"Error inesperado al rechazar préstamo: {e}",
            style=error_style,
        )
        return False


def modificar_libro(conexion):
    """
    Permite seleccionar un libro del inventario para actualizar sus datos.

    Muestra el inventario, solicita el ID del libro deseado, despliega
    un submenú con los campos editables (Título, Autor, Ejemplares) o la
    opción de regresar al menú principal, y ejecuta la edición elegida.

    Args:
        conexion (sqlite3.Connection): Conexión activa a la base de datos.

    Returns:
        None.

    Raises:
        sqlite3.Error: Si ocurre un problema al consultar o modificar.
        Exception: En caso de error general no previsto.

    Examples:
        Permite actualizar el autor o número de copias del libro con ID 0004.
    """
    # Contador de libros editados durante la sesión actual.
    libros_modificados = 0

    # * Bucle para modificar uno o más libros sin reiniciar el menú.
    while True:
        try:
            # Desplegamos el inventario actual para referencia del empleado.
            ver_inventario(conexion)

            # * Solicitamos el ID del libro con opción de volver al menú.
            id_input = input(
                "\nIngresa el ID del libro que deseas modificar "
                "(o '0'/'volver' para regresar al menú principal): "
            ).strip()
            if id_input.lower() in ("0", "cancelar", "volver", "salir"):
                console.print("Regresando al menú principal...")
                return

            try:
                id_modificar = int(id_input)
            except ValueError:
                console.print(
                    "Por favor, ingresa un número entero válido.",
                    style=error_style,
                )
                continue

            # Consultamos la fila del libro en la base de datos.
            cursor = conexion.execute(
                "SELECT id, titulo, autor, ejemplares FROM libros WHERE id = ?",
                (id_modificar,),
            )
            fila = cursor.fetchone()

            if fila is None:
                console.print(
                    "No se ha encontrado un libro con ese ID.",
                    style=error_style,
                )
                continue

            # Mostramos los datos actuales del libro seleccionado.
            console.print(
                f'El libro seleccionado es "{fila["titulo"]}", escrito por '
                f"{fila['autor']} con {fila['ejemplares']} ejemplares."
            )

            # * Desplegamos el submenú de edición de campos con opción 4 volver.
            console.print(
                Panel(
                    "[bold white]"
                    "1. Título\n"
                    "2. Autor\n"
                    "3. Ejemplares\n"
                    "4. Volver al Menú Principal"
                    "[/bold white]",
                    title="DATOS DEL LIBRO",
                    border_style="green",
                    expand=False,
                )
            )

            # Bucle para validar la opción de campo que se va a editar.
            while True:
                campo_input = input(
                    "¿Qué campo deseas editar? (1-4): "
                ).strip()
                # ? Opción 4 o cancelar regresa al menú principal de empleado.
                if campo_input.lower() in ("4", "cancelar", "volver", "salir"):
                    console.print(
                        "Edición de libros cancelada. "
                        "Regresando al menú principal..."
                    )
                    return
                try:
                    campo_editar = int(campo_input)
                    if campo_editar == 1:
                        campo = "titulo"
                        break
                    elif campo_editar == 2:
                        campo = "autor"
                        break
                    elif campo_editar == 3:
                        campo = "ejemplares"
                        break
                    else:
                        console.print(
                            "Ingresa una opción válida", style=error_style
                        )
                except ValueError:
                    console.print(
                        "Por favor, ingresa un número entero válido.",
                        style=error_style,
                    )

            # * Ejecutamos la función auxiliar de edición para el campo elegido.
            if edicion_libros(conexion, campo, fila, id_modificar):
                libros_modificados += 1

            # Preguntamos si desea modificar otro libro más.
            otra_edicion = (
                input("¿Deseas modificar otro libro? (s/n): ").strip().lower()
            )
            if otra_edicion not in ("si", "sí", "s", "y", "yes"):
                if libros_modificados > 0:
                    console.print(
                        f"Has modificado {libros_modificados} "
                        "libro(s) correctamente.",
                        style=check_style,
                    )
                break
        except sqlite3.Error as e:
            conexion.rollback()
            console.print(
                f"Error de base de datos al modificar el libro: {e}",
                style=error_style,
            )
        except Exception as e:
            console.print(
                f"Error inesperado al modificar el libro: {e}",
                style=error_style,
            )


def edicion_libros(conexion, campo, fila, id_modificar):
    """
    Aplica la actualización de un campo en la base de datos tras confirmación.

    Solicita el nuevo valor para el campo seleccionado (validando tipo de dato
    en el caso de ejemplares), pide confirmación al empleado y ejecuta
    la sentencia SQL UPDATE sobre la tabla libros.

    Args:
        conexion (sqlite3.Connection): Conexión activa a la base de datos.
        campo (str): Campo a modificar ('titulo', 'autor' o 'ejemplares').
        fila (sqlite3.Row | dict): Fila con la información previa del libro.
        id_modificar (int): Identificador numérico del libro a actualizar.

    Returns:
        bool: True si el campo fue actualizado, False si se canceló o falló.

    Raises:
        sqlite3.Error: Si falla la instrucción UPDATE en la base de datos.
        Exception: En caso de error imprevisto.

    Examples:
        Actualiza el número de ejemplares de un libro a 12 copias.
    """
    try:
        # ! Verificamos que el campo pertenezca a los atributos permitidos.
        if campo not in ("titulo", "autor", "ejemplares"):
            console.print(
                "Campo no permitido para modificación.", style=error_style
            )
            return False

        # * Tratamiento específico según el tipo de dato del campo.
        if campo == "ejemplares":
            console.print(f'El número de {campo} actual es "{fila[campo]}"')
            try:
                campo_editado = int(
                    input(f"Ingresa el nuevo número de {campo}: ")
                )
                if campo_editado < 0:
                    console.print(
                        "El número de ejemplares no puede ser negativo.",
                        style=error_style,
                    )
                    return False
            except ValueError:
                # ! Ejemplares debe ser estrictamente un número entero.
                console.print(
                    "Debes ingresar un número entero válido.",
                    style=error_style,
                )
                return False
            console.print(
                f"El nuevo número de ejemplares será: {campo_editado}"
            )
        else:
            # En campos textuales aplicamos .title() para capitalizar.
            console.print(f'El {campo} actual es "{fila[campo]}"')
            campo_editado = (
                input(f"Ingresa el nuevo {campo}: ").strip().title()
            )
            if not campo_editado:
                console.print(
                    "El valor editado no puede estar vacío.",
                    style=error_style,
                )
                return False
            console.print(f"El nuevo {campo} del libro será: {campo_editado}")

        # * Solicitamos confirmación explícita antes de hacer el UPDATE.
        while True:
            confirmar = (
                input("¿Confirmas que la edición es correcta? (s/n): ")
                .strip()
                .lower()
            )
            if confirmar in ("si", "sí", "s", "y", "yes"):
                # ? Ejecutamos la sentencia UPDATE modificando el campo seguro.
                conexion.execute(
                    f"UPDATE libros SET {campo} = ? WHERE id = ?",
                    (campo_editado, id_modificar),
                )
                conexion.commit()

                # Leemos la fila actualizada para confirmar el nuevo estado.
                cursor = conexion.execute(
                    "SELECT id, titulo, autor, ejemplares "
                    "FROM libros WHERE id = ?",
                    (id_modificar,),
                )
                fila_actualizada = cursor.fetchone()

                console.print(
                    "Libro editado correctamente.", style=check_style
                )
                if fila_actualizada:
                    console.print("Sus datos ahora son:")
                    console.print(f"Título: {fila_actualizada['titulo']}")
                    console.print(f"Autor: {fila_actualizada['autor']}")
                    console.print(
                        f"Número de Ejemplares: {fila_actualizada['ejemplares']}"
                    )
                return True
            elif confirmar in ("no", "n", "cancelar", "volver"):
                console.print("Edición cancelada.")
                return False
            else:
                console.print("Ingresa una opción válida", style=error_style)
    except sqlite3.Error as e:
        conexion.rollback()
        console.print(
            f"Error de base de datos durante la edición: {e}",
            style=error_style,
        )
        return False
    except Exception as e:
        console.print(
            f"Error inesperado durante la edición: {e}", style=error_style
        )
        return False


def borrar_libro(conexion):
    """
    Permite eliminar un libro del catálogo mediante su ID con confirmación.

    Muestra el inventario, pide el ID del libro, advierte sobre la
    irreversibilidad de la acción, solicita confirmación y ejecuta
    un DELETE sobre la tabla libros.

    Args:
        conexion (sqlite3.Connection): Conexión activa a la base de datos.

    Returns:
        None.

    Raises:
        sqlite3.Error: Si falla la instrucción DELETE en SQLite.
        Exception: En caso de error general imprevisto.

    Examples:
        Elimina el libro con ID 0002 tras confirmación expresa del empleado.
    """
    # Contador de libros eliminados en la sesión.
    libros_eliminados = 0

    # * Bucle para permitir borrar uno o varios libros si se desea.
    while True:
        try:
            ver_inventario(conexion)

            # * Solicitamos el ID con opción de regresar al menú principal.
            id_input = input(
                "\nIngresa el ID del libro que deseas borrar "
                "(o '0'/'volver' para regresar al menú principal): "
            ).strip()
            if id_input.lower() in ("0", "cancelar", "volver", "salir"):
                console.print("Regresando al menú principal...")
                return

            try:
                id_borrar = int(id_input)
            except ValueError:
                console.print(
                    "Por favor, ingresa un número entero válido.",
                    style=error_style,
                )
                continue

            # Comprobamos la existencia del libro antes de intentar borrar.
            cursor = conexion.execute(
                "SELECT id, titulo, autor, ejemplares "
                "FROM libros WHERE id = ?",
                (id_borrar,),
            )
            fila = cursor.fetchone()

            if fila is None:
                console.print(
                    "No se ha encontrado un libro con ese ID.",
                    style=error_style,
                )
                continue

            # * Advertencia de seguridad: borrar datos es irreversible.
            console.print(
                f'¿Estás seguro de borrar el libro "{fila["titulo"]}" '
                f"escrito por {fila['autor']}?"
            )
            console.print(
                "Esta decisión no se podrá deshacer y el libro "
                f"tiene {fila['ejemplares']} ejemplares."
            )

            confirmar_delete = input("(s/n): ").strip().lower()

            if confirmar_delete in ("si", "sí", "s", "y", "yes"):
                # ? DELETE FROM elimina definitivamente la fila de la tabla.
                conexion.execute(
                    "DELETE FROM libros WHERE id = ?", (id_borrar,)
                )
                conexion.commit()
                libros_eliminados += 1
                console.print(
                    "Libro borrado correctamente.", style=check_style
                )
            else:
                console.print("Operación de borrado cancelada.")

            # Preguntamos si desea eliminar otro libro más.
            while True:
                otro_borrado = (
                    input("¿Deseas borrar otro libro? (s/n): ").strip().lower()
                )
                if otro_borrado in ("si", "sí", "s", "y", "yes"):
                    break
                elif otro_borrado in ("no", "n", "volver", "salir", "0"):
                    if libros_eliminados > 0:
                        console.print(
                            f"Has eliminado {libros_eliminados} "
                            "libro(s) correctamente.",
                            style=check_style,
                        )
                    return
                else:
                    console.print(
                        "Ingresa una opción válida", style=error_style
                    )
        except sqlite3.Error as e:
            conexion.rollback()
            console.print(
                f"Error de base de datos al borrar el libro: {e}",
                style=error_style,
            )
        except Exception as e:
            console.print(
                f"Error inesperado al borrar el libro: {e}",
                style=error_style,
            )


def open_main_menu_employee(usuario=None):
    """
    Bucle principal de control para el menú del empleado de biblioteca.

    Coordina todo el flujo operativo de los empleados:
    - Muestra el arte ASCII y el panel de opciones administrativas.
    - Procesa entradas de menú (tanto números 1-7 como comandos de texto).
    - Conecta con la base de datos de forma segura para cada operación.
    - Maneja la opción de cerrar sesión para regresar al menú inicial
      y permitir que otro usuario o empleado inicie sesión.
    - Ofrece salida limpia del sistema.

    Args:
        usuario (dict | int | None): Información del empleado autenticado.

    Returns:
        None: Retorna cuando el empleado decide 'Cerrar Sesión'.

    Raises:
        SystemExit: Cuando el empleado elige salir por completo del sistema.

    Examples:
        open_main_menu_employee({'id': 2, 'role': 'employee_role'})
    """
    # Mostramos el encabezado decorativo en tipografía grande ASCII.
    menu_empleado_ascci()

    # * Bucle infinito que mantiene activo el menú hasta cerrar sesión o salir.
    while True:
        conexion = None
        try:
            # Mostramos el panel de opciones de empleado.
            opciones_empleado()
            opcion_menu = input("Ingresa la opción deseada: ").strip()

            # * -------------------------------------------------------------
            # * OPCIÓN 1: INGRESAR NUEVO LIBRO AL INVENTARIO
            # * -------------------------------------------------------------
            if opcion_menu == "1":
                console.print(
                    "Opción 1 Seleccionada:\n"
                    "[bold white]Ingresar Libro[/bold white]"
                )
                try:
                    # Conectamos y activamos row_factory para mapear columnas.
                    conexion = db.conectar()
                    conexion.row_factory = sqlite3.Row
                    insertar_libro(conexion)
                finally:
                    # ! Garantizamos el cierre de conexión pase lo que pase.
                    if conexion:
                        conexion.close()

            # * -------------------------------------------------------------
            # * OPCIÓN 2: MODIFICAR DATOS DE UN LIBRO EXISTENTE
            # * -------------------------------------------------------------
            elif opcion_menu == "2":
                console.print(
                    "Opción 2 Seleccionada:\n"
                    "[bold white]Modificar Libro[/bold white]"
                )
                try:
                    conexion = db.conectar()
                    conexion.row_factory = sqlite3.Row
                    modificar_libro(conexion)
                finally:
                    if conexion:
                        conexion.close()

            # * -------------------------------------------------------------
            # * OPCIÓN 3: ELIMINAR UN LIBRO DEL INVENTARIO
            # * -------------------------------------------------------------
            elif opcion_menu == "3":
                console.print(
                    "Opción 3 Seleccionada:\n"
                    "[bold white]Borrar Libro[/bold white]"
                )
                try:
                    conexion = db.conectar()
                    conexion.row_factory = sqlite3.Row
                    borrar_libro(conexion)
                finally:
                    if conexion:
                        conexion.close()

            # * -------------------------------------------------------------
            # * OPCIÓN 4: CONSULTAR INVENTARIO COMPLETO
            # * -------------------------------------------------------------
            elif opcion_menu == "4":
                console.print(
                    "Opción 4 Seleccionada:\n"
                    "[bold white]Ver Inventario[/bold white]"
                )
                try:
                    conexion = db.conectar()
                    conexion.row_factory = sqlite3.Row
                    ver_inventario(conexion)
                finally:
                    if conexion:
                        conexion.close()

            # * -------------------------------------------------------------
            # * OPCIÓN 5: GESTIÓN DE SOLICITUDES DE PRÉSTAMO
            # * -------------------------------------------------------------
            elif opcion_menu == "5":
                console.print(
                    "Opción 5 Seleccionada:\n"
                    "[bold white]Ver Solicitudes de Préstamo[/bold white]"
                )
                try:
                    conexion = db.conectar()
                    conexion.row_factory = sqlite3.Row
                    gestionar_solicitudes(conexion)
                finally:
                    if conexion:
                        conexion.close()

            # * -------------------------------------------------------------
            # * OPCIÓN 6: CERRAR SESIÓN (CAMBIAR DE USUARIO)
            # * -------------------------------------------------------------
            elif opcion_menu in (
                "6",
                "cerrar sesion",
                "cerrar sesión",
                "logout",
            ):
                console.print(
                    "Opción 6 Seleccionada:\n"
                    "[bold white]Cerrar Sesión[/bold white]"
                )
                console.print(
                    "[bold yellow]Cerrando sesión... "
                    "Volviendo al menú inicial.[/bold yellow]"
                )
                # ? return rompe la ejecución de este menú y regresa a main.py.
                # En main.py se vuelve a desplegar el menú para iniciar sesión.
                return

            # * -------------------------------------------------------------
            # * OPCIÓN 7: SALIR DEFINITIVAMENTE DEL SISTEMA
            # * -------------------------------------------------------------
            elif opcion_menu in ("7", "salir", "exit"):
                console.print(
                    "Opción 7 Seleccionada:\n"
                    "[bold white]Salir\n"
                    "Gracias por utilizar el programa.[/bold white]"
                )
                # ! sys.exit(0) finaliza el intérprete y detiene el programa.
                sys.exit(0)

            else:
                console.print("Ingresa una opción válida", style=error_style)

        except KeyboardInterrupt:
            # Captura Ctrl+C para finalizar de forma ordenada.
            console.print(
                "\nPrograma interrumpido por el usuario.", style=error_style
            )
            sys.exit(0)
        except Exception as e:
            # Atrapa errores inesperados evitando que el menú se cierre solo.
            console.print(
                f"Ocurrió un error inesperado en el menú principal: {e}",
                style=error_style,
            )
