def botonModificarMontoHora(montoHora):
    app = tk.Toplevel()
    app.title("Modificar monto por hora")
    app.geometry("300x200")
    app.resizable(False, False)
    tk.Label(app, text="Monto por hora (₡):").pack(pady=10)
    entryMonto = tk.Entry(app)
    entryMonto.insert(0, str(montoHora[0]))
    entryMonto.pack(pady=5)
    tk.Button(app, text="Confirmar", bg="#0d7703", fg="white", command=lambda: confirmar(entryMonto, montoHora, app)).pack(pady=10)

def confirmar(entryMonto, montoHora, app):
    valor = entryMonto.get().strip()
    if not valor.isdigit():
        messagebox.showwarning("Error", "Ingrese un número válido.")
        return ""
    confirmarCambio = messagebox.askyesno("Confirmar", f"¿Cambiar monto a ₡{valor}?")
    if confirmarCambio:
        montoHora[0] = int(valor)
        messagebox.showinfo("Éxito", "Monto actualizado correctamente.")
        app.destroy()
