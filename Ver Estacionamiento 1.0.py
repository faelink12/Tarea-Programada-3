import tkinter as tk

def estacionamientoVentana():
    app = tk.Tk()
    app.title("Estacionamiento")
    app.geometry("600x600")
    app.resizable(False, False)
    app.config(bg="#2D2F33")
    espacios = [None] * 20
    botones = []
    tk.Label(app, text="Estacionamiento", bg="#2D2F33", fg="White", font=("SansSerif", 16, "bold")).grid(row=0, column=0, columnspan=5, pady=15, padx=15)
    for i in range(20):
        fila = (i // 5) + 1
        columna = i % 5
        boton = tk.Button(app, text="", bg="#6FB95D", width=6, height=4, relief="flat", bd=1)
        boton.grid(row=fila, column=columna, padx=10, pady=10)
        botones.append(boton)
    app.mainloop()
estacionamientoVentana()
