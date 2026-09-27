"""
Archivo con los terminos y condiciones ademas del check.
"""

import tkinter as tk
from tkinter import messagebox


def mostrar_reglas_empleado() -> bool:
    root = tk.Tk()
    root.title("Términos y Condiciones")
    root.geometry("750x450")

    aceptar_var = tk.IntVar()
    acepto_terminos = False

    def validar_aceptacion():
        nonlocal acepto_terminos
        if aceptar_var.get() == 1:
            acepto_terminos = True
            messagebox.showinfo("Mensaje", "Gracias por aceptar")
            root.destroy()
        else:
            messagebox.showwarning(
                "Atención",
                "Debes aceptar los términos y condiciones para continuar.",
            )

    def on_close():
        root.destroy()

    root.protocol("WM_DELETE_WINDOW", on_close)

    label_titulo = tk.Label(
        root, text="Términos y Condiciones", font=("Arial", 14, "bold")
    )
    label_titulo.pack(pady=10)

    label_empleado = tk.Label(
        root,
        text="Empleado",
        font=("Arial", 12, "bold"),
    )
    label_empleado.pack(pady=5)

    label_textoemp = tk.Label(
        root,
        text="1. EL empleado debe iniciar sesion con un usuario validos para acceder al sistema."
        "\n2. El empleado es responsable de administrar el inventario de la biblioteca."
        "\n3. El empleado puede registrar, consultar, modificar y eliminar libros del inventario."
        "\n4. El empleado puede agregar o actualizar la cantidad de ejemplares disponibles."
        "\n5. El empleo puede registrar los prestamos y devouciones realizados por los usuarios."
        "\n6. El empleado puede consultar el estado del inventario y venificar que libros estan disponibles o prestados."
        "\n7. El empleado no puede registrar informacion incompleta de un libro.",
        font=("Arial", 12),
    )
    label_textoemp.pack(pady=5)

    checkbox = tk.Checkbutton(
        root,
        text="Acepto los términos y condiciones",
        variable=aceptar_var,
        font=("Arial", 12),
    )
    checkbox.pack(pady=15)

    boton_aceptar = tk.Button(
        root,
        text="Continuar",
        font=("Arial", 11, "bold"),
        command=validar_aceptacion,
    )
    boton_aceptar.pack(pady=5)

    root.mainloop()
    return acepto_terminos


if __name__ == "__main__":
    mostrar_reglas_empleado()
