import tkinter as tk


def procesar():
    nombre = entrada.get()
    resultado.config(text=f"Hola, {nombre}!")


ventana = tk.Tk()
ventana.title("Formulario simple")

tk.Label(ventana, text="Nombre:").grid(row=0, column=0, padx=10, pady=10)
entrada = tk.Entry(ventana)
entrada.grid(row=0, column=1, padx=10, pady=10)

tk.Button(ventana, text="Enviar", command=procesar).grid(
    row=1, column=0, columnspan=2, pady=10
)

resultado = tk.Label(ventana, text="")
resultado.grid(row=2, column=0, columnspan=2)

ventana.mainloop()
