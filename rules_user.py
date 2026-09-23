

"""
Archivo con los terminos y condiciones ademas del check.
"""

import tkinter as tk
from tkinter import messagebox


def validar_aceptacion():
    if aceptar_var.get() == 1:
        messagebox.showinfo(
            "Mensaje",
            "Gracias por aceptar"
        )
        root.destroy()
    else:
        messagebox.showwarning(
            "Atención",
            "Debes aceptar las reglas para continuar"
        )

root = tk.Tk()
root.title("Términos y Condiciones")
root.geometry("400x250")

label_titulo = tk.Label(
    root, text="Términos y Condiciones", font=("Arial", 14, "bold")
)
label_titulo.pack(pady=10)

label_cliente = tk.Label(
    root,
    text="Cliente",
    font=("Arial", 12, "bold"),
)
label_cliente = tk.Label(
    root,
    text="Cliente",
    font=("Arial", 12, "bold"),
)
label_cliente = tk.Label(
    root,
    text="Cliente",
    font=("Arial", 12, "bold"),
)

label_cliente.pack(pady=5)


label_textoclien = tk.Label(
    root,
    text="1. El usuario debe iniciar sesión para utilizar sus funciones."
         "\n2. El usuario puede consultar y buscar libros."
         "\n3. El usuario puede verificar la disponibilidad de un libro."
         "\n4. El usuario puede solicitar préstamos."
         "\n5. El usuario puede devolver los libros que tenga prestados."
         "\n6. El usuario no puede modificar ni eliminar información del inventario.",
    font=("Arial", 12),
)

label_textoclien.pack(pady=5)

aceptar_var = tk.IntVar()


checkbox = tk.Checkbutton(

    root,

    text="Acepto los términos y condiciones",

    variable=aceptar_var,

    font=("Arial", 12)

)

checkbox.pack(pady=10)


boton_aceptar = tk.Button(

    root,

    text="Continuar",

    font=("Arial", 11, "bold"),

    command=validar_aceptacion

)

boton_aceptar.pack(pady=5)


root.mainloop()
