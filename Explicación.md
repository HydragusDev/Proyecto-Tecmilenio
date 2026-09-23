REQUERIMENTOS FUNCIONALES Y TIPOS DE DATOS

RF1: Registrar usuario con correo, contraseña y rol.

Tipos de datos: Cadena (str)

RF2: Validar credenciales para iniciar sesión.

Tipos de datos: Cadena (str), Booleano (bool)

RF3: Registrar libro mediante título y autor.

Tipos de datos: Cadena (str)

RF4: Buscar libro por título o autor.

Tipos de datos: Cadena (str)

RF5: Solicitar préstamo usando código del libro.

Tipos de datos: Cadena (str)

RF6: Mostrar pantalla de carga durante segundos determinados.

RF7: Consultar historial de préstamos del usuario activo.

Tipos de datos: Cadena (str)

RF8: Eliminar cuenta de usuario registrada.

Tipos de datos: Cadena (str), Booleano (bool)

RF9: Desplegar opciones de menú según el rol.

Tipos de datos: Cadena (str)

Tipos de datos: Entero (int)

OPERADORES Y ESTRUCTURAS DE CONTROL

Operadores del Lenguaje

Operador de asignación (=): Almacena los valores de nuestras variables.

Operador de comparación de igualdad (==): Evalúa si dos valores son exactamente iguales devolviendo un booleano.

Operador de comparación de desigualdad (!=): Verifica si dos valores son distintos entre sí probablemente lo usemos en una condicional.

Operador de división (/): Calcula la división exacta entre dos números para determinar los avances de la barra.

Operadores Logicos (and, or, is, not): Los usaremos junto a condicionales para verificar requisitos.

Estructuras de Control

Estructura condicional (if / elif / else): Toma decisiones en el flujo del programa según se cumplan o no ciertas condiciones, como al validar correos, o en los menus si se selecciona una opción.

Estructura de repetición (while): Ejecuta un bloque de código de forma continua mientras la condición se mantenga verdadera, la primera instancia donde lo utilizamos es al validar el correo electronico, tiene el while hasta que ingrese un correo valido y unicamente se rompe si tiene lo necesario es decir, un @, al menos un punto y 0 espacios.

La estructura de base de datos estará hecho es SQL será una base de datos local con SQLite.

Se debe disponer de las dependencias correctamente instaladas que se encuentran en requirements.txt

