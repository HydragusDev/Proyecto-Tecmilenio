"""
Módulo de Interfaz y Menú para Usuarios de la Biblioteca.

Este archivo contiene la lógica completa para los usuarios regulares
del sistema de biblioteca (lectores, alumnos y docentes). Permite
consultar el catálogo de libros, revisar cuántos ejemplares están
disponibles en tiempo real, solicitar préstamos y agendar fechas para
devolver los libros prestados.

Aspectos pedagógicos y de mantenimiento:
- Interfaz amigable en consola utilizando la librería Rich.
- Títulos artísticos en tipografía grande con PyFiglet.
- Conexión segura a base de datos SQLite con consultas parametrizadas.
- Jerarquía de menús y submenús que permite retornar en todo momento.
- Explicaciones para desarrolladores novatos y personas sin experiencia.

Convención de Better Comments utilizada en el código:
# * [Información clave]: Aspectos esenciales del funcionamiento.
# ! [Advertencia / Cuidado]: Validación crítica y control de fallos.
# ? [Explicación didáctica]: Razonamiento detrás de una decisión.
# TODO: [Mantenimiento futuro]: Sugerencias para ampliar el sistema.
"""

# * =========================================================================
# * SECCIÓN DE IMPORTACIONES Y LIBRERÍAS
# * =========================================================================
# sqlite3 es la librería estándar de Python para gestionar bases de datos
# relacionales sin necesidad de instalar servidores externos como MySQL.
# Nos proporciona métodos para ejecutar sentencias SQL y manejar tablas.
import sqlite3

# sys permite interactuar con el sistema operativo y el intérprete de
# Python, por ejemplo para cerrar el programa limpiamente con sys.exit(0).
import sys

# pyfiglet toma cadenas de texto estándar y las dibuja en letras gigantes
# formadas por caracteres ASCII (arte tipográfico en consola de texto).
from pyfiglet import figlet_format

# Rich es una biblioteca moderna para embellecer terminales con colores,
# paneles delimitados, tablas formateadas y estilos tipográficos limpios.
from rich.console import Console
from rich.panel import Panel
from rich.style import Style
from rich.table import Table

# Importamos nuestro módulo local database.py para gestionar la conexión.
# Centraliza la ruta del archivo 'bitacora.db' y la creación de tablas.
import database as db

# * Creamos la instancia principal de Console para todas las impresiones.
# A través de console.print() enviamos texto formateado a la terminal.
console = Console()

# * Estilo visual para errores: color rojo, texto en negrita y parpadeo.
# Se utiliza cuando una operación falla o el usuario comete una equivocación.
error_style = Style(color="red", bold=True, blink=True)

# * Estilo visual para aciertos: color verde con parpadeo suave.
# Se utiliza para confirmar que una acción se completó exitosamente.
check_style = Style(color="green", blink=True)


def menu_usuario_ascci():
    """
    Muestra el título del menú de usuario en arte ASCII estilizado.

    Utiliza la librería pyfiglet para transformar texto convencional en
    letras gigantes en arte ASCII con la tipografía estándar, creando
    un encabezado visualmente atractivo para el usuario.

    Args:
        No requiere argumentos.

    Returns:
        None.

    Raises:
        Exception: Puede ocurrir si pyfiglet experimenta algún error.

    Examples:
        Genera en pantalla el texto 'MENU DE USUARIO' en arte ASCII.
    """
    # * Imprimimos el título en dos llamadas para evitar desbordar ancho.
    # ? Cada llamada a figlet_format procesa la cadena como matriz ASCII.
    # Esto garantiza que el encabezado se vea imponente y bien centrado.
    try:
        print(figlet_format("MENU  DE", font="standard"))
        print(figlet_format("USUARIO", font="standard"))
    except Exception as e:
        # ! Si falla la generación gráfica, informamos sin romper el flujo.
        console.print(
            f"Error al generar el título ASCII: {e}", style=error_style
        )


def opciones_usuario():
    """
    Muestra el panel con las opciones del menú principal de usuario.

    Crea una caja rectangular con bordes de color cian usando Rich
    Panel, enlistando todas las acciones disponibles para el usuario:
    consultar libros, pedir préstamos, agendar devoluciones, cerrar
    sesión o salir del sistema por completo.

    Args:
        No requiere argumentos.

    Returns:
        None.

    Raises:
        Exception: Si Rich no puede renderizar el panel en consola.

    Examples:
        Muestra el panel de opciones principales del usuario.
    """
    # * Creamos un panel cerrado con borde cian para destacar opciones.
    # ? expand=False evita que el panel ocupe todo el ancho de la consola.
    # ? Cada opción está numerada para que el usuario elija con un dígito.
    # Dividimos el texto en varias líneas para no superar 77 caracteres.
    try:
        console.print(
            Panel(
                "[bold white]"
                "1. Ver Catalogo de Libros\n"
                "2. Hacer Solicitud de Prestamo\n"
                "3. Agendar devolución\n"
                "4. Cerrar Sesión\n"
                "5. Salir"
                "[/bold white]",
                title="OPCIONES",
                border_style="cyan",
                expand=False,
            )
        )
    except Exception as e:
        # ! Informamos si ocurre una falla al renderizar el menú.
        console.print(f"Error al mostrar el menú: {e}", style=error_style)


def opciones_ver_catalogo():
    """
    Muestra el submenú de opciones para explorar el catálogo de libros.

    Presenta las diferentes modalidades de consulta de libros en panel
    verde: ver catálogo completo, ver solo ejemplares disponibles,
    realizar una búsqueda específica o regresar al menú principal.

    Args:
        No requiere argumentos.

    Returns:
        None.

    Raises:
        Exception: Si ocurre un error al dibujar el panel en terminal.

    Examples:
        Despliega las 4 opciones de navegación del catálogo de libros.
    """
    # * Panel verde que representa el primer nivel de submenú.
    # ? La opción 4 permite al usuario deshacer su paso y volver atrás.
    # ? El diseño jerárquico evita que el usuario quede atrapado sin salida.
    # Mantener las líneas de texto breves asegura compatibilidad visual.
    try:
        console.print(
            Panel(
                "[bold white]"
                "1. Ver Catalogo Completo\n"
                "2. Ver Unicamente Disponibles\n"
                "3. Busqueda Especifica\n"
                "4. Volver Al Menu Principal"
                "[/bold white]",
                border_style="green",
                expand=False,
            )
        )
    except Exception as e:
        # ! Notificamos en caso de falla de dibujo en terminal.
        console.print(f"Error al mostrar el catálogo: {e}", style=error_style)


def opciones_busqueda_especifica():
    """
    Muestra el submenú para filtrar búsquedas de libros por campo.

    Genera un panel amarillo que permite al usuario escoger entre
    buscar un libro por su título o por el nombre de su autor, o bien
    retornar al submenú anterior de opciones de catálogo.

    Args:
        No requiere argumentos.

    Returns:
        None.

    Raises:
        Exception: Si ocurre un error de renderizado en Rich.

    Examples:
        Muestra opciones: 1. Título, 2. Autor, 3. Volver a Catálogo.
    """
    # * Submenú de segundo nivel para criterios específicos de filtrado.
    # ? El color amarillo ayuda al usuario a distinguir este submenú.
    # ? La opción 3 devuelve el control al submenú de opciones de catálogo.
    # Esto cumple con la regla de retornar al menú padre correspondiente.
    try:
        console.print(
            Panel(
                "[bold white]"
                "1. Busqueda por Titulo\n"
                "2. Busqueda por Autor\n"
                "3. Volver a Opciones de Catálogo"
                "[/bold white]",
                border_style="yellow",
                expand=False,
            )
        )
    except Exception as e:
        # ! Si falla la interfaz de búsqueda, notificamos en pantalla.
        console.print(f"Error en menú de búsqueda: {e}", style=error_style)


def ver_inventario(conexion):
    """
    Consulta y muestra todos los libros registrados en la base de datos.

    Ejecuta una consulta SQL SELECT sobre la tabla libros y presenta
    los resultados organizados en una tabla estilizada de Rich con
    columnas para ID, Título y Autor.

    Args:
        conexion (sqlite3.Connection): Conexión activa a bitacora.db.

    Returns:
        None.

    Raises:
        sqlite3.Error: Si ocurre un problema al consultar la base de datos.
        Exception: Si ocurre un error inesperado en el procesamiento.

    Examples:
        Muestra una tabla con todos los libros existentes en el sistema.
    """
    # * Bloque try para capturar cualquier anomalía de conexión o lectura.
    # ? En bases de datos relacionales, una consulta SELECT lee registros
    # sin modificar el contenido de las tablas en el disco duro.
    try:
        # ? SELECT id, titulo, autor solicita solo las columnas deseadas.
        # ? ORDER BY id ordena los libros de menor a mayor por su código.
        cursor = conexion.execute(
            "SELECT id, titulo, autor FROM libros ORDER BY id"
        )
        # fetchall() extrae todas las filas que coincidieron con la consulta.
        filas = cursor.fetchall()

        # ! Si no hay registros, informamos amablemente en color rojo.
        if not filas:
            console.print("No hay libros registrados.", style=error_style)
        else:
            # * Creamos una tabla de Rich con columnas coloreadas.
            tabla = Table(
                title="[bold white]Inventario de Libros[/bold white]"
            )
            # Definimos nombre de columna, alineación y estilo de texto.
            # Cada color facilita distinguir la naturaleza de cada dato.
            tabla.add_column("ID", justify="center", style="green")
            tabla.add_column("Título", justify="center", style="blue")
            tabla.add_column("Autor", justify="center", style="magenta")

            # ? Iteramos sobre cada libro obtenido de la base de datos.
            for fila in filas:
                # Formateamos el ID a cuatro dígitos con ceros a la izquierda.
                # Ejemplo: el número 3 se muestra elegantemente como '0003'.
                id_libro = f"{int(fila['id']):04d}"
                tabla.add_row(
                    id_libro,
                    str(fila["titulo"]),
                    str(fila["autor"]),
                )
            # Imprimimos la tabla formateada directamente en la consola.
            console.print(tabla)
    except sqlite3.Error as e:
        # ! Notificamos si la base de datos SQLite arrojó una excepción.
        # Esto ocurre por ejemplo si la tabla no existe o el archivo falló.
        console.print(
            f"Error de base de datos al ver inventario: {e}",
            style=error_style,
        )
    except Exception as e:
        # Capturamos cualquier otro error inesperado para no detener la app.
        console.print(f"Ha ocurrido el error: {e}", style=error_style)


def ver_inventario_disponibles(conexion):
    """
    Calcula y muestra únicamente los libros que tienen ejemplares libres.

    Para cada libro en el inventario, calcula cuántos ejemplares están
    prestados actualmente con estado 'autorizado' y los resta del total
    de ejemplares. Si el resultado es mayor a cero, se muestra en la tabla.

    Args:
        conexion (sqlite3.Connection): Conexión activa a la base de datos.

    Returns:
        None.

    Raises:
        sqlite3.Error: Si falla la lectura de libros o préstamos.
        Exception: Si ocurre un error inesperado al calcular inventario.

    Examples:
        Muestra la tabla de libros que pueden solicitarse en préstamo.
    """
    try:
        # * Leemos todos los libros para verificar existencias totales.
        # Solicitamos la columna 'ejemplares' para saber el inventario físico.
        cursor = conexion.execute(
            "SELECT id, titulo, autor, ejemplares FROM libros ORDER BY id"
        )
        filas = cursor.fetchall()

        # ! Si no hay libros en inventario, salimos tempranamente.
        if not filas:
            console.print("No hay libros registrados.", style=error_style)
            return

        # Construimos la tabla visual con la columna 'Disponibles'.
        tabla = Table(
            title="[bold white]Inventario de Libros Disponibles[/bold white]"
        )
        tabla.add_column("ID", justify="center", style="green")
        tabla.add_column("Título", justify="center", style="blue")
        tabla.add_column("Autor", justify="center", style="magenta")
        tabla.add_column("Disponibles", justify="center", style="cyan")

        # Bandera booleana para rastrear si al menos un libro tiene copias.
        hay_disponibles = False

        # ? Recorremos cada libro para calcular disponibilidad en tiempo real.
        # Este cálculo dinámico evita inconsistencias en inventario.
        for fila in filas:
            # Contamos cuántos préstamos activos autorizados tiene este libro.
            # Una solicitud rechazada o devuelta no resta ejemplares libres.
            cursor_conteo = conexion.execute(
                "SELECT COUNT(*) FROM prestamos "
                "WHERE id_libro = ? AND estado = 'autorizado'",
                (fila["id"],),
            )
            # fetchone()[0] extrae el resultado de la función COUNT(*).
            prestados = cursor_conteo.fetchone()[0]
            # Restamos existencias totales menos los préstamos activos.
            disponibles = fila["ejemplares"] - prestados

            # * Si quedan 1 o más copias disponibles, lo agregamos a la tabla.
            if disponibles > 0:
                hay_disponibles = True

                id_libro = f"{int(fila['id']):04d}"
                tabla.add_row(
                    id_libro,
                    str(fila["titulo"]),
                    str(fila["autor"]),
                    str(disponibles),
                )

        # Si encontramos ejemplares imprimimos la tabla, sino una advertencia.
        if hay_disponibles:
            console.print(tabla)
        else:
            console.print("No hay ejemplares disponibles.", style=error_style)
    except sqlite3.Error as e:
        # ! Advertencia de error en la consulta relacional de SQLite.
        console.print(
            f"Error de base de datos en disponibles: {e}",
            style=error_style,
        )
    except Exception as e:
        console.print(f"Ha ocurrido el error: {e}", style=error_style)


def busqueda_especifica(conexion, criterio_busqueda, busqueda):
    """
    Busca libros que coincidan con un término en título o autor.

    Ejecuta una consulta SQL con la cláusula LIKE para encontrar
    coincidencias parciales. Protege contra inyecciones SQL validando
    que el campo pertenezca a una lista blanca permitida.

    Args:
        conexion (sqlite3.Connection): Conexión activa a la base de datos.
        criterio_busqueda (str): Campo de búsqueda ('titulo' o 'autor').
        busqueda (str): Cadena de texto que el usuario desea buscar.

    Returns:
        bool: True si la búsqueda se completó con éxito, False si falló.

    Raises:
        sqlite3.Error: Si surge un error en la sintaxis o consulta SQL.
        Exception: Si ocurre un error inesperado al procesar los datos.

    Examples:
        busqueda_especifica(con, 'titulo', 'Quijote') busca por título.
    """
    try:
        # ! Lista blanca de campos seguros para prevenir ataques de inyección.
        # Solo permitimos filtrar por 'titulo' o 'autor', nada más.
        # En ciberseguridad, nunca se concatena directamente texto sin validar.
        allowed_fields = {"titulo": "titulo", "autor": "autor"}
        campo_seguro = allowed_fields.get(criterio_busqueda)

        # Si el criterio no coincide con la lista blanca, rechazamos.
        if campo_seguro is None:
            console.print("Campo de búsqueda inválido.", style=error_style)
            return False

        # ? LIKE con los comodines % busca coincidencias en cualquier posición.
        # Usamos el parámetro ? para que SQLite sanitice la entrada del usuario.
        cursor = conexion.execute(
            f"SELECT id, titulo, autor FROM libros "
            f"WHERE {campo_seguro} LIKE ?",
            (f"%{busqueda}%",),
        )

        filas = cursor.fetchall()

        # Si la lista de resultados está vacía, avisamos que no hubo éxito.
        if not filas:
            console.print(
                f"\n[red]No se encontraron libros con "
                f'{criterio_busqueda}: "{busqueda}"[/red]\n'
            )
            return False

        # * Mostramos los libros encontrados en una tabla de resultados.
        tabla = Table(title="[bold white]Resultados de Búsqueda[/bold white]")
        tabla.add_column("ID", justify="center", style="green")
        tabla.add_column("Título", justify="center", style="blue")
        tabla.add_column("Autor", justify="center", style="magenta")

        # Poblamos la tabla con los libros coincidentes.
        for fila in filas:
            id_libro = f"{int(fila['id']):04d}"
            tabla.add_row(
                id_libro,
                str(fila["titulo"]),
                str(fila["autor"]),
            )

        console.print(tabla)
        return True

    except sqlite3.Error as e:
        # ! Informamos si hubo un problema al ejecutar la sentencia SQL.
        console.print(
            f"Error de base de datos en búsqueda: {e}",
            style=error_style,
        )
        return False
    except Exception as e:
        console.print(f"Ha ocurrido el error: {e}", style=error_style)
        console.print("Repite la búsqueda", style=error_style)
        return False


def asegurar_usuario_demo(conexion, id_usuario):
    """
    Verifica que el usuario exista en la tabla users antes de operar.

    Evita errores de clave foránea al solicitar préstamos. Si el ID no
    está registrado en la base de datos, inserta un registro de prueba
    de forma transparente para permitir la continuidad del flujo.

    Args:
        conexion (sqlite3.Connection): Conexión activa a la base de datos.
        id_usuario (int): Identificador numérico único del usuario.

    Returns:
        bool: True si el usuario existe o fue creado, False en error.

    Raises:
        sqlite3.Error: Si falla la inserción o consulta del usuario.
        Exception: Si ocurre un error inesperado en la verificación.

    Examples:
        asegurar_usuario_demo(con, 1) garantiza que el usuario 1 exista.
    """
    try:
        # * Primero verificamos en la tabla oficial 'users' de database.py.
        # Buscamos si existe una fila cuyo ID coincida con el usuario actual.
        # Las claves foráneas requieren que el registro padre exista.
        cursor = conexion.execute(
            "SELECT id FROM users WHERE id = ?",
            (id_usuario,),
        )
        # fetchone() devuelve la primera fila o None si no hubo coincidencia.
        if cursor.fetchone() is not None:
            # ? El usuario ya está debidamente registrado en el sistema.
            return True

        # ! Si no existe, creamos un registro base con rol de usuario.
        # Esto previene errores de clave foránea (FOREIGN KEY constraint failed).
        # Los bytes b"demo" actúan como hash simulado para pruebas locales.
        conexion.execute(
            "INSERT INTO users (id, username, mail, hashed_password, "
            "role, accepted_terms) VALUES (?, ?, ?, ?, ?, 1)",
            (
                id_usuario,
                "usuario_demo",
                "usuario.demo@biblioteca.local",
                b"demo",
                "user_role",
            ),
        )
        # Guardamos los cambios permanentemente en el archivo de la BD.
        conexion.commit()
        return True
    except Exception:
        # ? Respaldo de compatibilidad por si se utiliza un esquema alterno.
        try:
            cursor = conexion.execute(
                "SELECT id FROM usuarios WHERE id = ?",
                (id_usuario,),
            )
            return cursor.fetchone() is not None
        except Exception as e:
            console.print(f"Ha ocurrido el error: {e}", style=error_style)
            return False


def solicitar_prestamo(conexion, id_usuario):
    """
    Gestiona el flujo completo para que un usuario solicite un préstamo.

    Muestra los libros disponibles, solicita el ID del libro deseado,
    comprueba su existencia y disponibilidad, y registra la solicitud
    en la tabla 'prestamos' con estado 'pendiente'. Permite cancelar.

    Args:
        conexion (sqlite3.Connection): Conexión activa a la base de datos.
        id_usuario (int): ID del usuario que realiza la solicitud.

    Returns:
        bool | None: None si se cancela o falla, False si no existe.

    Raises:
        sqlite3.Error: Si ocurre un fallo al insertar el préstamo.
        Exception: Si ocurre un error inesperado durante el trámite.

    Examples:
        Permite al usuario solicitar el libro 0002 en préstamo.
    """
    try:
        # * 1. Garantizamos que el usuario exista para no violar foreign keys.
        # Si la verificación falla, detenemos el proceso para evitar errores.
        if not asegurar_usuario_demo(conexion, id_usuario):
            console.print(
                "No se pudo usar el usuario para la solicitud.",
                style=error_style,
            )
            return

        # * 2. Mostramos al usuario los libros que tienen stock disponible.
        # Esto le permite ver los IDs válidos antes de ingresar su elección.
        ver_inventario_disponibles(conexion)

        # * 3. Solicitamos el ID del libro con opción de volver al menú.
        # ? Escribir '0', 'cancelar' o 'volver' retorna al menú de usuario.
        # Usamos .strip() para limpiar espacios accidentales al inicio o fin.
        id_input = input(
            "Ingresa el ID del libro que deseas solicitar "
            "(o '0'/'volver' para cancelar): "
        ).strip()
        if id_input.lower() in ("0", "cancelar", "volver", "salir", ""):
            console.print(
                "Solicitud cancelada. Regresando al menú principal..."
            )
            return

        # Intentamos convertir la entrada del usuario a número entero.
        try:
            id_libro = int(id_input)
        except ValueError:
            # ! Si ingresa letras o símbolos inválidos, informamos error.
            console.print("El ID ingresado no es válido.", style=error_style)
            return

        # * 4. Verificamos que el libro exista realmente en el catálogo.
        cursor = conexion.execute(
            "SELECT ejemplares FROM libros WHERE id = ?", (id_libro,)
        )
        fila_libro = cursor.fetchone()

        # Si el libro no está en la base de datos, notificamos al usuario.
        if fila_libro is None:
            console.print(
                f"\n[red]No se encontró el libro con ID: "
                f"{id_libro:04d}[/red]\n"
            )
            return False

        # * 5. Verificamos en tiempo real si quedan ejemplares libres.
        # Contamos cuántos préstamos autorizados están en curso para este libro.
        cursor_conteo = conexion.execute(
            "SELECT COUNT(*) FROM prestamos "
            "WHERE id_libro = ? AND estado = 'autorizado'",
            (id_libro,),
        )
        prestados = cursor_conteo.fetchone()[0]
        disponibles = fila_libro["ejemplares"] - prestados

        # Si no quedan ejemplares libres, no se puede realizar el préstamo.
        if disponibles <= 0:
            console.print(
                "No hay ejemplares disponibles de este libro.",
                style=error_style,
            )
            return

        # * 6. Insertamos la solicitud de préstamo en la base de datos.
        # ? Por defecto el estado queda en 'pendiente' hasta autorización.
        # Un empleado revisará la solicitud en el menú de empleados.
        conexion.execute(
            "INSERT INTO prestamos (id_libro, id_usuario) VALUES (?, ?)",
            (id_libro, id_usuario),
        )
        # Confirmamos la transacción en la base de datos SQLite.
        conexion.commit()

        console.print(
            "Solicitud de préstamo enviada. Espera autorización.",
            style=check_style,
        )
    except sqlite3.Error as e:
        # En caso de fallo de BD revertimos la transacción para consistencia.
        # rollback() deshace cualquier cambio pendiente y previene bloqueos.
        conexion.rollback()
        console.print(
            f"Error de base de datos en préstamo: {e}",
            style=error_style,
        )
    except Exception as e:
        console.print(f"Ha ocurrido el error: {e}", style=error_style)


def agendar_devolucion(conexion, id_usuario):
    """
    Permite al usuario registrar una fecha tentativa de devolución.

    Muestra únicamente los préstamos que tienen estado 'autorizado'
    pertenecientes al usuario actual, solicita el ID del préstamo y
    la fecha para actualizar el registro en la base de datos.

    Args:
        conexion (sqlite3.Connection): Conexión activa a la base de datos.
        id_usuario (int): Identificador del usuario que devolverá el libro.

    Returns:
        None.

    Raises:
        sqlite3.Error: Si falla la actualización en la tabla prestamos.
        Exception: Si ocurre un error inesperado al procesar la devolución.

    Examples:
        Registra la fecha '2026-10-15' para devolución del préstamo 0001.
    """
    try:
        # * Consultamos los préstamos del usuario que ya estén autorizados.
        # ? Los préstamos pendientes o devueltos no requieren agendar fecha.
        # Solo quien tiene el libro físico puede programar su entrega.
        cursor = conexion.execute(
            "SELECT id, id_libro, estado, fecha_solicitud, "
            "fecha_autorizacion, fecha_devolucion FROM prestamos "
            "WHERE id_usuario = ? AND estado = 'autorizado' ORDER BY id",
            (id_usuario,),
        )
        filas = cursor.fetchall()

        # ! Si no tiene préstamos activos, no hay nada que devolver.
        if not filas:
            console.print(
                "No tienes préstamos autorizados para agendar una devolución.",
                style=error_style,
            )
            return

        # * Presentamos los préstamos del usuario en tabla informativa.
        tabla = Table(
            title="[bold white]Tus Prestamos Autorizados[/bold white]"
        )
        tabla.add_column("ID", justify="center", style="green")
        tabla.add_column("ID Libro", justify="center", style="blue")
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

        # Añadimos cada préstamo autorizado a la tabla para que elija el ID.
        for fila in filas:
            id_prestamo = f"{int(fila['id']):04d}"
            tabla.add_row(
                id_prestamo,
                str(fila["id_libro"]),
                str(fila["estado"]),
                str(fila["fecha_solicitud"]),
                str(fila["fecha_autorizacion"]),
                str(fila["fecha_devolucion"]),
            )
        console.print(tabla)

        # * Solicitamos ID del préstamo a gestionar con opción de salir.
        # ? Escribir '0' o 'cancelar' permite arrepentirse y volver al menú.
        id_input = input(
            "Ingresa el ID del préstamo que deseas devolver "
            "(o '0'/'volver' para cancelar): "
        ).strip()
        if id_input.lower() in ("0", "cancelar", "volver", "salir", ""):
            console.print(
                "Operación cancelada. Regresando al menú principal..."
            )
            return

        try:
            id_prestamo = int(id_input)
        except ValueError:
            console.print("El ID ingresado no es válido.", style=error_style)
            return

        # Comprobamos que el préstamo exista y le pertenezca a este usuario.
        cursor = conexion.execute(
            "SELECT id, estado FROM prestamos WHERE id = ? AND id_usuario = ?",
            (id_prestamo, id_usuario),
        )
        fila_prestamo = cursor.fetchone()

        if fila_prestamo is None:
            console.print(
                f"\n[red]No se encontró un préstamo con ID: "
                f"{id_prestamo:04d}[/red]\n"
            )
            return

        # Solo permitimos agendar devolución si el préstamo está autorizado.
        if fila_prestamo["estado"] != "autorizado":
            console.print(
                "Solo puedes agendar devolución de préstamos autorizados.",
                style=error_style,
            )
            return

        # * Solicitamos la fecha de entrega acordada.
        fecha_devolucion = input(
            "Ingresa la fecha de devolución (o 'cancelar' para volver): "
        ).strip()
        if fecha_devolucion.lower() in ("0", "cancelar", "volver", "salir"):
            console.print(
                "Operación cancelada. Regresando al menú principal..."
            )
            return
        if not fecha_devolucion:
            console.print("Debes ingresar una fecha.", style=error_style)
            return

        # * Actualizamos la fecha de devolución en la base de datos.
        conexion.execute(
            "UPDATE prestamos SET fecha_devolucion = ? WHERE id = ?",
            (fecha_devolucion, id_prestamo),
        )
        # Guardamos la fecha permanentemente.
        conexion.commit()

        console.print(
            "Fecha de devolución enviada al empleado.",
            style=check_style,
        )
    except sqlite3.Error as e:
        # Revertimos cualquier cambio pendiente en caso de error.
        conexion.rollback()
        console.print(
            f"Error de base de datos en devolución: {e}",
            style=error_style,
        )
    except Exception as e:
        console.print(f"Ha ocurrido el error: {e}", style=error_style)


def open_main_menu_user(usuario=None):
    """
    Bucle principal de control para la navegación del menú de usuario.

    Gestiona la interacción del usuario final con el sistema:
    - Despliega el título ASCII y el panel de opciones.
    - Procesa selecciones numéricas o textuales.
    - Maneja la navegación jerárquica a submenús y el retorno.
    - Permite cerrar sesión para cambiar de usuario o salir del sistema.

    Args:
        usuario (dict | int | None): Datos del usuario autenticado en login.

    Returns:
        None: Retorna cuando el usuario selecciona 'Cerrar Sesión'.

    Raises:
        SystemExit: Cuando el usuario elige salir definitivamente del sistema.

    Examples:
        open_main_menu_user({'id': 1, 'role': 'user_role'})
    """
    # * Determinamos el identificador del usuario de forma segura.
    # ? Si recibimos un diccionario de usuario tomamos su clave 'id'.
    # ? Si se ejecuta de forma independiente, usamos el ID demo 1.
    if isinstance(usuario, dict) and "id" in usuario:
        id_usuario = usuario["id"]
    elif isinstance(usuario, int):
        id_usuario = usuario
    else:
        id_usuario = 1

    # Mostramos el banner decorativo en la consola al iniciar sesión.
    menu_usuario_ascci()

    # * Bucle infinito que mantiene activo el menú hasta cerrar sesión o salir.
    # Este patrón es el estándar para aplicaciones de consola interactivas.
    while True:
        try:
            # Mostramos el panel interactivo con las 5 opciones.
            opciones_usuario()
            opcion_input = input("Ingresa la opción deseada: ").strip()

            # ? Aceptamos tanto número como palabras comunes para comodidad.
            # Esto mejora la experiencia del usuario final notablemente.
            if opcion_input.lower() in (
                "cerrar sesion",
                "cerrar sesión",
                "logout",
            ):
                opcion_menu = 4
            elif opcion_input.lower() in ("salir", "exit"):
                opcion_menu = 5
            else:
                opcion_menu = int(opcion_input)

            # * ---------------------------------------------------------
            # * OPCIÓN 1: EXPLORACIÓN DEL CATÁLOGO DE LIBROS
            # * ---------------------------------------------------------
            if opcion_menu == 1:
                # Sub-bucle para navegar entre las opciones de catálogo.
                while True:
                    try:
                        opciones_ver_catalogo()
                        opcion_input_verCata = input(
                            "Ingresa la opción deseada: "
                        ).strip()
                        if opcion_input_verCata.lower() in (
                            "volver",
                            "regresar",
                            "salir",
                            "menu principal",
                        ):
                            opcion_select_verCata = 4
                        else:
                            opcion_select_verCata = int(opcion_input_verCata)

                        # 1.1 Ver Catálogo Completo
                        if opcion_select_verCata == 1:
                            console.print(
                                "Opción Seleccionada:\n"
                                "[bold white]Ver Catalogo Completo"
                                "[/bold white]"
                            )
                            conexion = None
                            try:
                                # Abrimos conexión con row_factory activo.
                                conexion = db.conectar()
                                conexion.row_factory = sqlite3.Row
                                ver_inventario(conexion)
                            except Exception as e:
                                console.print(
                                    f"[red]Error al cargar inventario: "
                                    f"{e}[/red]",
                                    style=error_style,
                                )
                            finally:
                                # ! Siempre cerramos la conexión a la BD.
                                if conexion:
                                    conexion.close()

                        # 1.2 Ver Únicamente Disponibles
                        elif opcion_select_verCata == 2:
                            console.print(
                                "Opción Seleccionada:\n"
                                "[bold white]Ver Catalogo Disponible"
                                "[/bold white]"
                            )
                            conexion = None
                            try:
                                conexion = db.conectar()
                                conexion.row_factory = sqlite3.Row
                                ver_inventario_disponibles(conexion)
                            except Exception as e:
                                console.print(
                                    f"[red]Error al cargar disponibles: "
                                    f"{e}[/red]",
                                    style=error_style,
                                )
                            finally:
                                if conexion:
                                    conexion.close()

                        # 1.3 Búsqueda Específica (Submenú anidado)
                        elif opcion_select_verCata == 3:
                            console.print(
                                "Opción Seleccionada:\n"
                                "[bold white]Busqueda Especifica"
                                "[/bold white]"
                            )
                            # Bucle para realizar búsquedas sin salir del menú.
                            while True:
                                try:
                                    opciones_busqueda_especifica()
                                    criterio_busqueda = (
                                        input("Ingresa tu opción (1-3): ")
                                        .strip()
                                        .lower()
                                    )

                                    if criterio_busqueda in (
                                        "1",
                                        "titulo",
                                        "title",
                                    ):
                                        campo_buscar = "titulo"
                                    elif criterio_busqueda in (
                                        "2",
                                        "autor",
                                        "author",
                                    ):
                                        campo_buscar = "autor"
                                    elif criterio_busqueda in (
                                        "3",
                                        "volver",
                                        "regresar",
                                        "salir",
                                        "exit",
                                    ):
                                        # * Regresamos al menú de catálogo.
                                        console.print(
                                            "Regresando a opciones "
                                            "de catálogo..."
                                        )
                                        break
                                    else:
                                        console.print(
                                            "Ingresa una opción válida",
                                            style=error_style,
                                        )
                                        continue

                                    # Solicitamos el término a buscar.
                                    busqueda = input(
                                        f"Ingresa el {campo_buscar} a buscar "
                                        f"(o 'volver' para regresar): "
                                    ).strip()
                                    if busqueda.lower() in (
                                        "volver",
                                        "regresar",
                                        "cancelar",
                                        "salir",
                                    ):
                                        console.print("Búsqueda cancelada.")
                                        continue
                                    if not busqueda:
                                        console.print(
                                            "El término de búsqueda no "
                                            "puede estar vacío.",
                                            style=error_style,
                                        )
                                        continue

                                    conexion = None
                                    try:
                                        conexion = db.conectar()
                                        conexion.row_factory = sqlite3.Row
                                        busqueda_especifica(
                                            conexion, campo_buscar, busqueda
                                        )
                                    except Exception as e:
                                        console.print(
                                            f"Ha ocurrido el error: {e}",
                                            style=error_style,
                                        )
                                    finally:
                                        if conexion:
                                            conexion.close()

                                except Exception as e:
                                    console.print(
                                        f"Ha ocurrido el error: {e}",
                                        style=error_style,
                                    )
                                    break

                        # 1.4 Volver al Menú Principal de Usuario
                        elif opcion_select_verCata == 4:
                            console.print("Regresando al menú principal...")
                            # Rompe el sub-bucle de catálogo y vuelve al menú.
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

            # * ---------------------------------------------------------
            # * OPCIÓN 2: SOLICITUD DE PRÉSTAMO
            # * ---------------------------------------------------------
            elif opcion_menu == 2:
                console.print(
                    "Opción Seleccionada:\n"
                    "[bold white]Hacer Solicitud de Prestamo[/bold white]"
                )
                conexion = None
                try:
                    conexion = db.conectar()
                    conexion.row_factory = sqlite3.Row
                    solicitar_prestamo(conexion, id_usuario)
                except Exception as e:
                    console.print(
                        f"Ha ocurrido el error: {e}", style=error_style
                    )
                finally:
                    if conexion:
                        conexion.close()

            # * ---------------------------------------------------------
            # * OPCIÓN 3: AGENDAR DEVOLUCIÓN DE LIBRO
            # * ---------------------------------------------------------
            elif opcion_menu == 3:
                console.print(
                    "Opción Seleccionada:\n"
                    "[bold white]Agendar Devolución[/bold white]"
                )
                conexion = None
                try:
                    conexion = db.conectar()
                    conexion.row_factory = sqlite3.Row
                    agendar_devolucion(conexion, id_usuario)
                except Exception as e:
                    console.print(
                        f"Ha ocurrido el error: {e}", style=error_style
                    )
                finally:
                    if conexion:
                        conexion.close()

            # * ---------------------------------------------------------
            # * OPCIÓN 4: CERRAR SESIÓN
            # * ---------------------------------------------------------
            elif opcion_menu == 4:
                console.print(
                    "Opción Seleccionada:\n"
                    "[bold white]Cerrar Sesión[/bold white]"
                )
                console.print(
                    "[bold yellow]Cerrando sesión... "
                    "Volviendo al menú inicial.[/bold yellow]"
                )
                # ? return finaliza este menú y regresa el control a main.py.
                return

            # * ---------------------------------------------------------
            # * OPCIÓN 5: SALIR DEL SISTEMA
            # * ---------------------------------------------------------
            elif opcion_menu == 5:
                console.print(
                    "Opción Seleccionada:\n"
                    "[bold white]Salir\n"
                    "Gracias por utilizar el programa.[/bold white]"
                )
                # ! sys.exit(0) finaliza la ejecución de todo el programa.
                sys.exit(0)

            else:
                console.print("Ingresa una opción válida", style=error_style)

        except ValueError:
            # Capturamos entrada no numérica no reconocida.
            console.print(
                "Por favor, ingresa un número entero válido.",
                style=error_style,
            )
        except KeyboardInterrupt:
            # Capturamos Ctrl+C para salir ordenadamente.
            console.print(
                "\nPrograma interrumpido por el usuario.", style=error_style
            )
            sys.exit(0)
        except Exception as e:
            # Atrapamos cualquier error imprevisto.
            console.print(
                f"Ha ocurrido un error inesperado: {e}", style=error_style
            )
