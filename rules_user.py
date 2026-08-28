"""
Archivo con los terminos y condiciones ademas del check.
"""

import tkinter as tk
from tkinter import messagebox


def validar_aceptacion():
    if aceptar_var.get() == 1:
        messagebox.showinfo("Gracias por aceptar las reglas.")
    else:
        messagebox.showwarning(
            "Atención", "Debes aceptar las reglas para continuar"
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
label_cliente.pack(pady=5)
label_textoclien = tk.Label(
    root,
    text="k",
    font=("Arial", 12),
)
label_textoclien.pack(pady=5)
root.mainloop()
