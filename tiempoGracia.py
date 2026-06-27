def botonTiempoDeGracia(tiempoDeGracia):
    app = tk.Toplevel()
    app.title("Modificar tiempo de gracia")
    app.geometry("300x200")
    app.resizable(False, False)
    tk.Label(app, text="Tiempo de gracia (minutos): ").pack(pady=10)
    entryTiempo = tk.Entry(app)
    entryTiempo.insert(0, str(tiempoDeGracia[0]))
    entryTiempo.pack(pady=5)
    tk.Button(app, text="Confirmar", bg="#0d7703", fg="white", command=lambda: confirmarTiempoGracia(entryTiempo, tiempoDeGracia, app)).pack(pady=10)

def confirmarTiempoGracia(entryTiempo, tiempoDeGracia, app):
    valor = entryTiempo.get().strip()
    if not valor.isdigit():
        messagebox.showwarning("Error", "Ingrese un número válido.")
        return ""
    confirmarCambio = messagebox.askyesno("Confirmar", f"¿Cambiar tiempo de gracia a {valor} minutos?")
    if confirmarCambio:
        tiempoDeGracia[0] = int(valor)
        messagebox.showinfo("Éxito", "Tiempo de gracia actualizado correctamente.")
        app.destroy()
