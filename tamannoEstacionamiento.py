def botonTamannoEstacionamiento(espaciosEstacionamiento):
    app = tk.Toplevel()
    app.title("Tamaño del estacionamiento")
    app.geometry("300x150")
    app.resizable(False, False)
    tk.Label(app, text="Tamaño del estacionamiento:").pack(pady=10)
    entryTamanno = tk.Entry(app)
    entryTamanno.insert(0, str(len(espaciosEstacionamiento)))
    entryTamanno.config(state="readonly")
    entryTamanno.pack(pady=5
