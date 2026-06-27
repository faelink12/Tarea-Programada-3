def botonAcercaDe():
    app = tk.Toplevel()
    app.title("Acerca de")
    app.geometry("400x380")
    app.resizable(False, False)
    tk.Label(app, text="Acerca del Sistema", font=("SansSerif", 16, "bold")).pack(pady=15)
    info = (
        "Instituto Tecnológico de Costa Rica\nIngeniería en Computación\n"
    "Curso: Taller de Programación\nI Semestre 2026\nDesarrolladores:\nSebastián Rodriguez Vega y Fabián Eduarte Linkimer\n"
    "Github: \ngithub.com/sebastianrvg | github.com/faelink12"
    )
    tk.Label(app, text=info, font=("SansSerif", 10), justify="center").pack(pady=10)
    tk.Button(app, text="Regresar", bg="#770303", fg="white", font=("SansSerif", 10, "bold"), width=15, relief="flat", command=app.destroy).pack(pady=15)
