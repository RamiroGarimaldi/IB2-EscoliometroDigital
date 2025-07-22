import sqlite3
from tkinter import *
import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
from Container import pacientes

db_name = "DataClinica.db"
IdMedico = None

class login(tk.Frame):

    def __init__(self, padre, controlador):
        super().__init__(padre)
        self.pack()
        self.place(x=0, y=0, width=1100, height=650)
        self.controlador = controlador
        self.widgets()
    
    def validacion(self, usuario, con):
        return len(usuario) > 0 and len(con) > 0

    def login(self):
        usuario = self.usuario.get()
        con = self.con.get()
        global IdMedico

        if self.validacion(usuario, con):
            consulta = "SELECT * FROM medicos WHERE Usuario = ? AND Contraseña = ?"
            parametros = (usuario, con)

            try:
                with sqlite3.connect(db_name) as conn:
                    cursor = conn.cursor()
                    cursor.execute(consulta, parametros)
                    result = cursor.fetchall()

                    if result:
                        id, _, _, _, _, _ = result[0]
                        IdMedico = id
                        self.controlInicio()
                    else:
                        self.usuario.delete(0, "end")
                        self.con.delete(0, "end")
                        messagebox.showerror(title="Error", message="Usuario y/o contraseña incorrecta")
            
            except sqlite3.Error as e:
                messagebox.showerror(title="Error", message="No se conectó a la base de datos: {}".format(e))
        
        else:
            messagebox.showerror(title="Error", message="Todos los campos deben estar completos")

    def controlInicio(self):
        self.usuario.delete(0, "end")
        self.con.delete(0, "end")
        self.controlador.show_frame(pacientes) #Aca debería ir a la pestaña de pacientes luego de iniciar sesión con el médico
    
    def controlRegistro(self):
        self.usuario.delete(0, "end")
        self.con.delete(0, "end")
        self.controlador.show_frame(registro)
    
    def widgets(self):
        fondo = tk.Frame(self, bg="#C6D9E3")
        fondo.pack()
        fondo.place(x=0, y=0, width=1100, height=650)

        self.imagen_fondo = Image.open("Imagenes/FondoPrincipal.jpg")
        self.imagen_fondo = self.imagen_fondo.resize((1100, 650))
        self.imagen_fondo = ImageTk.PhotoImage(self.imagen_fondo)
        self.label_fondo = ttk.Label(fondo, image=self.imagen_fondo)
        self.label_fondo.place(x=0, y=0, width=1100, height=650)

        self.mensaje_inicio = tk.Label(fondo, text="Haga click para comenzar", bg="#C6D9E3", fg="#FFFFFF", font=("Arial", 22, "bold"))
        self.mensaje_inicio.place(x=350, y=600, width=400, height=40)
        self.animar_mensaje()

        self.label_fondo.bind("<Button-1>", self.mostrar_frame_inicio)
        self.mensaje_inicio.bind("<Button-1>", self.mostrar_frame_inicio)
        
        self.frame_inicio = tk.Frame(self, bg="#FFFFFF", highlightbackground="black", highlightthickness=1)
        self.frame_inicio.place(x=350, y=70, width=400, height=560)
        self.frame_inicio.lower()

        self.imagen_medico = Image.open("Imagenes/Medico.jpg")
        self.imagen_medico = self.imagen_medico.resize((200, 200))
        self.imagen_medico = ImageTk.PhotoImage(self.imagen_medico)
        self.label_medico = ttk.Label(self.frame_inicio, image=self.imagen_medico, background="#FFFFFF")
        self.label_medico.place(x=100, y=20 )

        usuario = tk.Label(self.frame_inicio, text="Usuario", font="arial 16 bold", bg="#FFFFFF")
        usuario.place(x=100, y=250)
        self.usuario = ttk.Entry(self.frame_inicio, font="arial 16 bold")
        self.usuario.place(x=80, y=290, width=240, height=40)

        con = tk.Label(self.frame_inicio, text="Contraseña", font="arial 16 bold", bg="#FFFFFF")
        con.place(x=100, y=340)
        self.con = ttk.Entry(self.frame_inicio, show="*", font="arial 16 bold")
        self.con.place(x=80, y=380, width=240, height=40)

        boton1 = tk.Button(self.frame_inicio, text="Ingresar", font="arial 16 bold", command=self.login) 
        boton1.place(x=80, y=440, width=240, height=40)

        boton2 = tk.Button(self.frame_inicio, text="Nuevo Médico", font="arial 16 bold", command=self.controlRegistro)
        boton2.place(x=80, y=500, width=240, height=40)
    
    def animar_mensaje(self):
        if not hasattr(self, "color_step"):
            self.color_step = 20
            self.subiendo = True

        if self.subiendo:
            self.color_step += 5
            if self.color_step >= 150:
                self.color_step = 150
                self.subiendo = False
        else:
            self.color_step -= 5
            if self.color_step <= 20:
                self.color_step = 20
                self.subiendo = True

        color = f"#{self.color_step:02x}{self.color_step:02x}{self.color_step:02x}"
        self.mensaje_inicio.config(fg=color)
        self.after(50, self.animar_mensaje)
    
    def mostrar_frame_inicio(self, event):
        self.mensaje_inicio.place_forget()
        self.frame_inicio.lift()

class registro(tk.Frame):
    def __init__(self, padre, controlador):
        super().__init__(padre)
        self.pack()
        self.place(x=0, y=0, width=1100, height=650)
        self.controlador = controlador
        self.widgets()
    
    def validacion(self, matricula, con):
        return len(matricula) > 0 and len(con) > 0
    
    def consulta(self, consulta, parametros=()):
        try:
            with sqlite3.connect(db_name) as conn:
                cursor = conn.cursor()
                cursor.execute(consulta, parametros)
                conn.commit()
        except sqlite3.Error as e:
            messagebox.showerror(title="Error", message="Error al ejecutar la consulta: {}".format(e))
    
    def registro(self):
        nombre = self.nombre.get()
        apellido = self.apellido.get()
        matricula = self.matricula.get()
        con = self.con.get()
        
        if not nombre or not apellido or not matricula or not con:
            messagebox.showerror(title="Error", message="Todos los campos deben estar completos")
            return
        if len(matricula) < 5:
            messagebox.showerror(title="Error", message="La matrícula debe contener al menos 5 caracteres")
            self.con.delete(0, "end")
            return
        if len(con) < 8:
            messagebox.showerror(title="Error", message="La contraseña debe contener al menos 8 caracteres")
            self.con.delete(0, "end")
            return
        
        else:
            usuario = f"{apellido.lower().strip()}{matricula.strip()}"
            consulta = "INSERT INTO Medicos (Nombre, Apellido, Matricula, Contraseña, Usuario) VALUES (?, ?, ?, ?, ?)"
            parametros = (nombre, apellido, matricula, con, usuario)
            self.consulta(consulta, parametros)
            with sqlite3.connect(db_name) as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT IdMedico FROM Medicos WHERE Usuario = ?", (usuario,))
                result = cursor.fetchone()
                if result:
                    global IdMedico
                    IdMedico = result[0]
            self.controlRegistro(usuario)
    
    def controlRegistro(self, usuario):
        messagebox.showinfo("Exito", f"Registro exitoso\nBienvenido {usuario}")
        self.controlador.show_frame(pacientes) #Si el registro es correcto pasa a la pestaña de pacientes
    
    def controlVolver(self):
        self.controlador.show_frame(login)
    
    def widgets(self):
        fondo = tk.Frame(self, bg="#C6D9E3")
        fondo.pack()
        fondo.place(x=0, y=0, width=1100, height=650)

        self.imagen_fondo = Image.open("Imagenes/FondoPrincipal.jpg")
        self.imagen_fondo = self.imagen_fondo.resize((1100, 650))
        self.imagen_fondo = ImageTk.PhotoImage(self.imagen_fondo)
        self.label_fondo = ttk.Label(fondo, image=self.imagen_fondo)
        self.label_fondo.place(x=0, y=0, width=1100, height=650)
        
        self.frame_inicio = tk.Frame(self, bg="#FFFFFF", highlightbackground="black", highlightthickness=1)
        self.frame_inicio.place(x=350, y=10, width=400, height=630)

        self.imagen_medico = Image.open("Imagenes/Medico.jpg")
        self.imagen_medico = self.imagen_medico.resize((140, 140))
        self.imagen_medico = ImageTk.PhotoImage(self.imagen_medico)
        self.label_medico = ttk.Label(self.frame_inicio, image=self.imagen_medico, background="#FFFFFF")
        self.label_medico.place(x=140, y=20 )

        nombre = tk.Label(self.frame_inicio, text="Nombre", font="arial 16 bold", bg="#FFFFFF")
        nombre.place(x=100, y=160)
        self.nombre = ttk.Entry(self.frame_inicio, font="arial 16 bold")
        self.nombre.place(x=80, y=200, width=240, height=40)
        
        apellido = tk.Label(self.frame_inicio, text="Apellido", font="arial 16 bold", bg="#FFFFFF")
        apellido.place(x=100, y=250)
        self.apellido = ttk.Entry(self.frame_inicio, font="arial 16 bold")
        self.apellido.place(x=80, y=290, width=240, height=40)

        matricula = tk.Label(self.frame_inicio, text="Matrícula", font="arial 16 bold", bg="#FFFFFF")
        matricula.place(x=100, y=340)
        self.matricula = ttk.Entry(self.frame_inicio, font="arial 16 bold")
        self.matricula.place(x=80, y=380, width=240, height=40)

        con = tk.Label(self.frame_inicio, text="Contraseña", font="arial 16 bold", bg="#FFFFFF" )
        con.place(x=100, y=430)
        self.con = ttk.Entry(self.frame_inicio, show="*", font="arial 16 bold")
        self.con.place(x=80, y=470, width=240, height=40)

        boton3 = tk.Button(self.frame_inicio, text="Registrar", font="arial 16 bold", command=self.registro)
        boton3.place(x=80, y=520, width=240, height=40)

        boton4 = tk.Button(self.frame_inicio, text="Atrás", font="arial 16 bold", command=self.controlVolver)
        boton4.place(x=80, y=570, width=240, height=40)



