from tkinter import *
import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
from datetime import datetime
import Login
import sqlite3
import socket
import threading
import calendar
import time
import sys
import os
import json
import re
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import numpy as np
import mplcursors

db_name = "DataClinica.db"
#ip = "192.168.1.15" #Casa
ip = "172.20.10.9" #Datos

class pacientes(tk.Frame):
    def __init__(self, padre, controlador):
        super().__init__(padre)
        self.pack()
        self.place(x=0, y=0, width=1100, height=650)
        self.controlador = controlador
        self.botonI = None
        self.widgets()
    
    def widgets(self):
        fondo = tk.Frame(self, bg="#C6D9E3")
        fondo.pack()
        fondo.place(x=0, y=0, width=1100, height=650)

        self.imagen_fondo = Image.open("Imagenes/FondoMenu4.png")
        self.imagen_fondo = self.imagen_fondo.resize((1100, 650))
        self.imagen_fondo = ImageTk.PhotoImage(self.imagen_fondo)
        self.label_fondo = ttk.Label(fondo, image=self.imagen_fondo)
        self.label_fondo.place(x=0, y=0, width=1100, height=650)

        #Frame pacientes
        canvas_pacientes = tk.LabelFrame(self, text="Pacientes", font="arial 14 bold", bg="#C6D9E3")
        canvas_pacientes.place(x=330, y=30, width=730, height=500)
        self.canvas = tk.Canvas(canvas_pacientes, bg="#C6D9E3")
        self.scrollbar = tk.Scrollbar(canvas_pacientes, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = tk.Frame(self.canvas, bg="#C6D9E3")

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion = self.canvas.bbox("all"))
        )

        self.canvas.create_window((0,0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        self.scrollbar.pack(side="right", fill="y")
        self.canvas.pack(side="left", fill="both", expand=True)
        
        self.labels_pacientes = []
        self.paciente_seleccionado = None

        self.cargarPacientes()

        #Frame nuevo paciente
        lblframe_Bnuevo = LabelFrame(self, bg="#C6D9E3", text="Nuevo Paciente", font="arial 14 bold")
        lblframe_Bnuevo.place(x=10, y=30, width=280, height=100)
        Bnuevo = tk.Button(lblframe_Bnuevo, text="Agregar", font="arial 14 bold", command=self.agregarPaciente)
        Bnuevo.place(x=45, y=15, width=180, height=40)
        
        #Frame busqueda pacientes
        lblframe_buscar = LabelFrame(self, text="Buscar", font="arial 14 bold", bg="#C6D9E3")
        lblframe_buscar.place(x=10, y=160, width=280, height=100)
        self.busqueda = ttk.Entry(lblframe_buscar, font="arial 14 bold")
        self.busqueda.place(x=5, y=15, width=260, height=40)
        self.busqueda.bind("<KeyRelease>", self.busquedaPacientes)

        #Agregar boton cerrar sesion
        lblframe_BCerrarSesion = LabelFrame(self, bg="#C6D9E3", font="arial 14 bold")
        lblframe_BCerrarSesion.place(x=10, y=530, width=280, height=65)
        BCerrarSesion = tk.Button(lblframe_BCerrarSesion, text="Cerrar Sesión", font="arial 14 bold", command=self.cerrarSesion)
        BCerrarSesion.place(x=45, y=10, width=180, height=40)
    
    def busquedaPacientes(self, event=None):
        filtro = self.busqueda.get()
        self.cargarPacientes(filtro)

    def cerrarSesion(self):
         self.controlador.show_frame(Login.login)
    
    def agregarPaciente(self):
        self.top = tk.Toplevel(self)
        self.top.title("Nuevo Paciente")
        self.top.geometry("700x400+200+50")
        self.top.config(bg="#C6D9E3")
        self.top.resizable(False, False)

        self.top.transient(self.master)
        self.top.grab_set()
        self.top.focus_set()
        self.top.lift()

        largoLabel = 17

        nombre = tk.Label(self.top, text="Nombre", font="arial 16 bold", bg="#C6D9E3", width=largoLabel, anchor="e")
        nombre.place(x=20, y=20)
        self.nombre = ttk.Entry(self.top, font="arial 16 bold")
        self.nombre.place(x=250, y=15, width=240, height=40)

        apellido = tk.Label(self.top, text="Apellido", font="arial 16 bold", bg="#C6D9E3", width=largoLabel, anchor="e")
        apellido.place(x=20, y=80)
        self.apellido = ttk.Entry(self.top, font="arial 16 bold")
        self.apellido.place(x=250, y=75, width=240, height=40)

        dni = tk.Label(self.top, text="DNI", font="arial 16 bold", bg="#C6D9E3", width=largoLabel, anchor="e")
        dni.place(x=20, y=140)
        self.dni = ttk.Entry(self.top, font="arial 16 bold")
        self.dni.place(x=250, y=135, width=240, height=40)

        fechaN = tk.Label(self.top, text="Fecha de Nacimiento", font="arial 16 bold", bg="#C6D9E3", width=largoLabel, anchor="e")
        fechaN.place(x=20, y=200)
        self.fechaN = ttk.Entry(self.top, font="arial 16 bold",  foreground="gray")
        self.fechaN.place(x=250, y=195, width=240, height=40)
        self.fechaN.insert(0, "dd/mm/aaaa")

        self.fechaN.bind("<FocusIn>", self.quitarPlaceholder)
        self.fechaN.bind("<FocusOut>", self.ponerPlaceholder)
        self.fechaN.bind("<KeyRelease>", self.formatoFecha)

        botonA = tk.Button(self.top, text="Guardar", font="arial 16 bold", command=self.guardarPacientes)
        botonA.place(x=250, y=300, width=240, height=40)
    
    def quitarPlaceholder(self, event):
        if self.fechaN.get() =="dd/mm/aaaa":
            self.fechaN.delete(0, tk.END)
            self.fechaN.config(foreground="black")
    
    def ponerPlaceholder(self, event):
        if not self.fechaN.get():
            self.fechaN.insert(0, "dd/mm/aaaa")
            self.fechaN.config(foreground="gray")
    
    def formatoFecha(self, event):
        texto = self.fechaN.get().replace("/", "")
        nuevoTexto = ""

        for i, c in enumerate(texto):
            if not c.isdigit():
                continue
            if len(nuevoTexto) == 2 or len(nuevoTexto) == 5:
                nuevoTexto += "/"
            nuevoTexto += c
        
        if len(nuevoTexto) > 10:
            nuevoTexto = nuevoTexto[:10]
        
        self.fechaN.delete(0, tk.END)
        self.fechaN.insert(0, nuevoTexto[:10])
    
    def guardarPacientes(self):
        nombre = self.nombre.get()
        apellido = self.apellido.get()
        dni = self.dni.get()
        fechaN = self.fechaN.get()
 
        if not nombre or not apellido or not dni or not fechaN or fechaN == "dd/mm/aaaa":
            messagebox.showerror(title="Error", message="Todos los campos deben estar completos")
            return
        if len(dni) < 8:
            messagebox.showerror(title="Error", message="El DNI debe contener al menos 8 caracteres")
            self.dni.delete(0, "end")
            return
        
        try:
            fechaNacimiento = datetime.strptime(fechaN, "%d/%m/%Y")
        except ValueError:
            messagebox.showerror(title="Error", message="La fecha es incorrecta")
            self.fechaN.delete(0, "end")
            return
        
        _, dias_del_mes = calendar.monthrange(fechaNacimiento.year, fechaNacimiento.month)
        if fechaNacimiento > datetime.today():
            messagebox.showerror(title="Error", message="La fecha es incorrecta")
            self.fechaN.delete(0, "end")
            return
        if fechaNacimiento.day > dias_del_mes:
            messagebox.showerror(title="Error", message="La fecha es incorrecta")
            self.fechaN.delete(0, "end")
            return
        
        edad = self.calcularEdad(fechaN)
        #Guardar en base de datos
        consulta = "INSERT INTO Pacientes (Nombre, Apellido, DNI, FechaNacimiento, Edad) VALUES (?, ?, ?, ?, ?)"
        parametros = (nombre, apellido, dni, fechaN, edad)
        self.consulta(consulta, parametros)

        self.cargarPacientes()
        messagebox.showinfo("Exito", "Paciente agregado correctamente")
        self.top.destroy()

    def consulta(self, consulta, parametros=()):
        try:
            with sqlite3.connect(db_name) as conn:
                cursor = conn.cursor()
                cursor.execute(consulta, parametros)
                if consulta.strip().upper().startswith("SELECT"):
                    return cursor.fetchall()
                conn.commit()

                if consulta.strip().upper().startswith("INSERT"):
                    return cursor.lastrowid
        except sqlite3.Error as e:
            messagebox.showerror(title="Error", message="Error al ejecutar la consulta: {}".format(e))
    
    def calcularEdad(self, fechaNacimiento):
        hoy = datetime.today()
        fechaNacimiento = datetime.strptime(fechaNacimiento, "%d/%m/%Y")

        edad = hoy.year - fechaNacimiento.year
        if(hoy.month, hoy.day) < (fechaNacimiento.month, fechaNacimiento.day):
            edad -= 1
        
        return edad

    def cargarPacientes(self, filtro=""):
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()
    
        if filtro:
            consulta = """
                        SELECT P.IdPaciente, P.Nombre, P.Apellido, P.DNI, P.Edad, P.FechaNacimiento, 
                            MAX(T.FechaConsulta) as UltimaVisita
                        FROM Pacientes P
                        LEFT JOIN Turnos T ON P.IdPaciente = T.IdPaciente
                        WHERE P.Nombre LIKE ? OR P.Apellido LIKE ?
                        GROUP BY P.IdPaciente
                        ORDER BY UltimaVisita IS NOT NULL, UltimaVisita DESC
                        """
            #consulta = "SELECT IdPaciente, Nombre, Apellido, DNI, Edad, FechaNacimiento FROM Pacientes WHERE Nombre LIKE ? OR Apellido LIKE ? ORDER BY Apellido, Nombre"
            parametros = (f"%{filtro}%", f"%{filtro}%")
        else:
            #consulta = "SELECT IdPaciente, Nombre, Apellido, DNI, Edad, FechaNacimiento FROM Pacientes ORDER BY Apellido, Nombre "
            consulta = """
                        SELECT P.IdPaciente, P.Nombre, P.Apellido, P.DNI, P.Edad, P.FechaNacimiento, 
                            MAX(T.FechaConsulta) as UltimaVisita
                        FROM Pacientes P
                        LEFT JOIN Turnos T ON P.IdPaciente = T.IdPaciente
                        GROUP BY P.IdPaciente
                        ORDER BY UltimaVisita IS NOT NULL, UltimaVisita DESC
                        """
            parametros = ()
        
        pacientes = self.consulta(consulta, parametros)

        if not pacientes:
            tk.Label(self.scrollable_frame, text="No hay pacientes registrados", font="arial 12", bg="#C6D9E3").pack(pady=10)
            return
        
        encabezados = ["Nombre", "Apellido", "DNI", "Edad", "Ult. Visita"]
        for col, texto in enumerate(encabezados):
            label = tk.Label(self.scrollable_frame, text=texto, font="arial 12 bold", bg="#A6C9E3", width=10)
            label.grid(row=0, column=col, padx=2, pady=2)
        
        self.labels_pacientes = []
        
        for i, (idpaciente, nombre, apellido, dni, edad, fechanacimiento, ultimavisita) in enumerate(pacientes, start=1):
            fila_labels = []

            ultima_visita = "SELECT MAX(FechaConsulta) FROM Turnos WHERE IdPaciente = ?"
            resultado = self.consulta(ultima_visita, (idpaciente,))
            ultimavisita = resultado[0][0] if resultado and resultado[0][0] else "—"

            for col, dato in enumerate([nombre, apellido, dni, edad, ultimavisita]):
                label = tk.Label(self.scrollable_frame, text=dato or "Sin visitas", font="arial 12", bg="#C6D9E3", width=12, height=2)
                label.grid(row=i, column=col, padx=5, pady=2)
                label.bind("<Button-1>", lambda e, p=(idpaciente, nombre, apellido, dni, i): self.seleccionarPaciente(p))
                fila_labels.append(label)
            
            self.labels_pacientes.append((fila_labels, (nombre, apellido, dni)))
        
        self.canvas.update_idletasks()
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def seleccionarPaciente(self, paciente):
        idpaciente, nombre, apellido, dni, fila = paciente

        if self.paciente_seleccionado:
            for lbl in self.paciente_seleccionado:
                if lbl.winfo_exists():
                    lbl.config(bg="#C6D9E3")
            if self.botonI and self.botonI.winfo_exists():
                self.botonI.destroy()
                self.botonI = None
        
        for labels, datos in self.labels_pacientes:
            if datos[:3] == (nombre, apellido, dni):
                for lbl in labels:
                    lbl.config(bg="#FFD700")
                self.paciente_seleccionado = labels
                break
        
        self.botonI = tk.Button(self.scrollable_frame, text="Ingresar", font="arial 12 bold", command=lambda: self.ventanaPacientes((nombre, apellido, dni, idpaciente)))
        self.botonI.grid(row=fila, column=5, padx=5, pady=5)
    
    def ventanaPacientes(self, paciente):
        nombre, apellido, dni, idpaciente = paciente
        ventana = tk.Toplevel(self)
        ventana.title(f"{nombre} {apellido}")
        ventana.geometry("700x400+200+50")
        ventana.config(bg="#C6D9E3")
        ventana.resizable(False, False)

        ventana.transient(self.master)
        ventana.grab_set()
        ventana.focus_set()
        ventana.lift()

        fondo = tk.Frame(ventana, bg="#C6D9E3")
        fondo.pack(fill="both", expand=True)

        frameBotones = tk.LabelFrame(fondo, text="Opciones", font="arial 14 bold", bg="#C6D9E3", width=150)
        frameBotones.pack(side="left", fill="both", expand=True, padx=7, pady=10)
        
        BnuevaM = tk.Button(frameBotones, text="Nueva Medición", font="arial 14 bold", command=lambda: self.crearTurno(idpaciente))
        BnuevaM.place(x=10, y=15, width=180, height=40)
        self.comparacion = tk.Button(frameBotones, text="Comparar", font="arial 14 bold", state="disabled", command=self.CompararMediciones)
        self.comparacion.place(x=10, y=75, width=180, height=40)
        
        canvas_mediciones = tk.LabelFrame(fondo, text="Mediciones", font="arial 14 bold", bg="#C6D9E3")
        canvas_mediciones.pack(side="right", fill="both", expand=True, padx=10, pady=10)
        self.mediciones = tk.Canvas(canvas_mediciones, bg="#C6D9E3")
        self.scrollbar_M = tk.Scrollbar(canvas_mediciones, orient="vertical", command=self.mediciones.yview)
        self.scrollable_frame_M = tk.Frame(self.mediciones, bg="#C6D9E3")

        self.scrollable_frame_M.bind(
            "<Configure>",
            lambda e: self.mediciones.configure(scrollregion = self.mediciones.bbox("all"))
        )

        self.mediciones.create_window((0,0), window=self.scrollable_frame_M, anchor="nw")
        self.mediciones.configure(yscrollcommand=self.scrollbar_M.set)
        self.scrollbar_M.pack(side="right", fill="y")
        self.mediciones.pack(side="left", fill="both", expand=True)

        self.cargarMediciones(idpaciente)
    
    def crearTurno(self, idpaciente):
        hoy = datetime.today()
        fechaConsulta = (f"{hoy.day}/{hoy.month}/{hoy.year}")
        idp = idpaciente
        idmedico = Login.IdMedico

        if idmedico == None:
            messagebox.showerror(title="Error", message="Error registrando al médico")
            return
        else:
            consulta = "INSERT INTO Turnos (FechaConsulta, IdPaciente, IdMedico) VALUES (?, ?, ?)"
            parametros = (fechaConsulta, idp, idmedico)
            idturno = self.consulta(consulta, parametros)
            print("A ver aca", idturno)

        self.cargarMediciones(idp)

        ventana = self.ventanaNuevaMedicion(fechaConsulta, idturno, idpaciente)
        
        threading.Thread(target=self.iniciarServidor, args=(ventana,), daemon=True).start()

    def iniciarServidor(self, ventana):
        try:
            server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            server_socket.bind((ip, 5055)) #Casa
            server_socket.listen(1)
            ventana.server_socket = server_socket
            print("Esperando conexión del Escoliómetro...")

            client_socket, addr = server_socket.accept()
            ventana.client_socket = client_socket
            print(f"Conectado con {addr}")
            ventana.labelConexion.config(text=f"Escoliómetro conectado!", fg="green")

            while True:
                try:
                    dato = client_socket.recv(1024).decode().strip()
                    if not dato:
                        print("Cliente desconectado.")
                        break

                    if not ventana.winfo_exists():
                        print("Ventana cerrada, terminando servidor")
                        break

                    print(f"Recibido: {dato}")
                    try:
                        datos = re.findall(r"\(([\d\.]+),(-?[\d\.]+)\)", dato)
                        lista = [[float(x), float(y)] for x, y in datos]

                        tiempo = [p[0] for p in lista]
                        angulo = [p[1] for p in lista]

                        ventana.linea.set_data(tiempo, angulo)
                        ventana.ax.relim()
                        ventana.ax.autoscale_view()
                        configurarEje(ventana.ax, angulo)
                        xmax = max(tiempo) if len(tiempo) > 0 else 10 
                        ventana.ax.set_xlim(left=0, right=xmax)
                        ventana.canvas.draw()
                    except Exception as e:
                        print(f"Error actualizando gráfico: {e}")
                    ventana.nuevaMedicion = dato

                except (ConnectionResetError, Exception) as e:
                    print(f"Error en la conexión: {e}")
                    break

            client_socket.close()
            server_socket.close()
            print("Servidor cerrado")
        
        except Exception as e:
            print(f"Error iniciando el servidor: {e}")
    
    def guardarMedicion(self, idturno, dato):
        datos = re.findall(r"\(([\d\.]+),(-?[\d\.]+)\)", dato)
        lista = [[float(x), float(y)] for x, y in datos]
        vectorjson = json.dumps(lista)

        consulta = "INSERT INTO Mediciones (Medicion, IdTurno) VALUES (?, ?)"
        parametros = (vectorjson, idturno)
        self.consulta(consulta, parametros)
        self.cargarPacientes()
    
    def ventanaNuevaMedicion(self, fechaconsulta, idturno, idpaciente):
        ventana = tk.Toplevel(self)
        ventana.title(f"{fechaconsulta}")
        ventana.geometry("700x450+200+50")
        ventana.config(bg="#C6D9E3")
        ventana.resizable(False, False)

        ventana.transient(self.master)
        ventana.grab_set()
        ventana.focus_set()
        ventana.lift()

        fondo = tk.Frame(ventana, bg="#C6D9E3")
        fondo.pack(fill="both", expand=True)

        ventana.labelConexion = tk.Label(fondo, text="Esperando conexión...", font="arial 12", bg="#C6D9E3", fg="blue")
        ventana.labelConexion.pack(pady=10)

        frameGrafico = tk.Frame(fondo, bg="#C6D9E3")
        frameGrafico.pack(fill="both", expand=True)

        ventana.fig = Figure(figsize=(6, 3), dpi=100)
        ventana.fig.subplots_adjust(bottom=0.2)
        ventana.ax = ventana.fig.add_subplot(111)
        ventana.ax.set_xlabel("Tiempo (s)")
        ventana.ax.set_ylabel("Ángulo (°)")
        ventana.ax.set_title("Ángulo de inclinación del tronco")

        ventana.linea, = ventana.ax.plot([], [], 'b-', label="Medición angular")
        ventana.ax.legend(loc="best")

        ventana.canvas = FigureCanvasTkAgg(ventana.fig, master=frameGrafico)
        ventana.canvas.draw()
        ventana.canvas.get_tk_widget().pack(pady=10)
        
        frameBotones = tk.Frame(fondo, bg="#C6D9E3")
        frameBotones.pack(pady=15)

        botonGuardar = tk.Button(frameBotones, text="Guardar", font="arial 14 bold", bg="#4CAF50", fg="white", width=12, command=lambda: self.confirmacionGuardado(ventana))
        botonGuardar.grid(row=0, column=0, padx=20)

        botonRepetir = tk.Button(frameBotones, text="Repetir", font="arial 14 bold", bg="#f44336", fg="white", width=12, command=lambda: self.repetirMedicion(ventana))
        botonRepetir.grid(row=0, column=1, padx=20)

        ventana.medicionGuardada = False
        ventana.idturno = idturno
        ventana.protocol("WM_DELETE_WINDOW", lambda: self.cerrarVentanaMedicion(ventana, idpaciente))

        return ventana

    def confirmacionGuardado(self, ventana):
        if not hasattr(ventana, "nuevaMedicion") or not ventana.nuevaMedicion:
            messagebox.showwarning("Sin datos", "No hay datos para guardar")
            return

        confirmacion = messagebox.askyesno("Guardar medición", "¿Desea guardar esta medición?")
        if confirmacion:
            self.guardarMedicion(ventana.idturno, ventana.nuevaMedicion)
            ventana.medicionGuardada = True
            messagebox.showinfo("Guardado", "Medición guardada exitosamente")
            ventana.destroy()
    
    def repetirMedicion(self, ventana):
        confirmacion = messagebox.askyesno("Repetir medición", "¿Está seguro de que desea repetir la medición?\nSe descartarán los datos actuales.")
        if not confirmacion:
            return
        
        try:    
            try:
                if hasattr(ventana, "client_socket") and ventana.client_socket:
                    ventana.client_socket.close()
            except Exception as e:
                print(f"Error cerrando client_socket: {e}")
            
            try:
                if hasattr(ventana, "server_socket"):
                    ventana.server_socket.close()
            except Exception as e:
                print(f"Error cerrando server_socket: {e}")
            
            ventana.medicionGuardada = False
            ventana.nuevaMedicion = ""
            ventana.linea.set_data([], [])
            ventana.ax.relim()
            ventana.ax.set_xlim(0, 10)
            ventana.ax.set_ylim(-7, 7)
            ventana.ax.autoscale_view()
            ventana.canvas.draw()
            ventana.labelConexion.config(text="Esperando conexión...", fg="blue")
            threading.Thread(target=self.iniciarServidor, args=(ventana,), daemon=True).start()
            
        except Exception as e:
            print(f"Error al reiniciar la medición: {e}")
            messagebox.showerror("Error", "No se pudo reiniciar la medición.")

    def cerrarVentanaMedicion(self, ventana, idpaciente):
        try:
            ventana.client_socket.close()
        except Exception as e:
            print(f"Error cerrando client_socket: {e}")
        
        try:
            ventana.server_socket.close()
        except Exception as e:
            print(f"Error cerrando server_socket: {e}")
        
        if not getattr(ventana, "medicionGuardada", False):
            consulta = "DELETE FROM Turnos WHERE IdTurno = ?"
            parametros = (ventana.idturno,)
            self.consulta(consulta, parametros)
            print(f"Turno {ventana.idturno} eliminado porque no se recibieron datos")

            self.cargarMediciones(idpaciente)

        ventana.destroy() 

    def cargarMediciones(self, idpaciente):
        for widget in self.scrollable_frame_M.winfo_children():
            widget.destroy()
        
        consulta = """
        SELECT Turnos.IdTurno, Medicos.Nombre, Medicos.Apellido, Turnos.FechaConsulta
        FROM Turnos JOIN Medicos ON Turnos.IdMedico = Medicos.IdMedico
        WHERE Turnos.IdPaciente = ?
        ORDER BY Turnos.FechaConsulta DESC;
        """
        parametros = (idpaciente,)
        
        turnos = self.consulta(consulta, parametros)

        if not turnos:
            tk.Label(self.scrollable_frame_M, text="No hay registros", font="arial 12", bg="#C6D9E3").pack(pady=10)
            return
    
        encabezados = ["Atendido por", "Fecha de la consulta"]
        for col, texto in enumerate(encabezados):
            label = tk.Label(self.scrollable_frame_M, text=texto, font="arial 12 bold", bg="#A6C9E3", width=16)
            label.grid(row=0, column=col, padx=2, pady=2)
        
        self.labels_turnos = []
        self.check_vars = {}
        self.turno_seleccionado = None
        
        for i, (idturno, nombre, apellido, fechaconsulta) in enumerate(turnos, start=1):
            nombreMedico = f"{nombre} {apellido}"
            fila_labels = []

            for col, dato in enumerate([nombreMedico, fechaconsulta]):
                label = tk.Label(self.scrollable_frame_M, text=dato, font="arial 12", bg="#C6D9E3", width=16, height=2)
                label.grid(row=i, column=col, padx=5, pady=2)
                label.bind("<Button-1>", lambda e, t=(idturno, nombreMedico, fechaconsulta, i): self.seleccionarTurno(t))
                fila_labels.append(label)
            
            var = tk.IntVar()
            check = tk.Checkbutton(self.scrollable_frame_M, variable=var, bg="#C6D9E3", command=self.ActualizarBotonComparar)
            check.grid(row=i, column=2, padx=5)
            self.check_vars[idturno] = var
            
            self.labels_turnos.append((fila_labels, (idturno, nombreMedico, fechaconsulta)))
        
        self.mediciones.update_idletasks()
        self.mediciones.configure(scrollregion=self.mediciones.bbox("all"))

    def ActualizarBotonComparar(self):
        seleccionados = [idturno for idturno, var in self.check_vars.items() if var.get() == 1]
        if len(seleccionados) >= 2:
            self.comparacion.config(state="normal")
        else:
            self.comparacion.config(state="disabled")
    
    def CompararMediciones(self):
        seleccionados = [idturno for idturno, var in self.check_vars.items() if var.get() == 1]
        if len(seleccionados) < 2:
            return
        self.VentanaComparacion(seleccionados)
    
    def seleccionarTurno(self, turnos):
        idturno, nombreMedico, fechaconsulta, fila = turnos

        if self.turno_seleccionado:
            for lbl in self.turno_seleccionado:
                if lbl.winfo_exists():
                    lbl.config(bg="#C6D9E3")
            if self.botonV and self.botonV.winfo_exists():
                self.botonV.destroy()
                self.botonV = None
        
        for labels, datos in self.labels_turnos:
            if datos[:3] == (idturno, nombreMedico, fechaconsulta):
                for lbl in labels:
                    lbl.config(bg="#FFD700")
                self.turno_seleccionado = labels
                break
        
        self.botonV = tk.Button(self.scrollable_frame_M, text="Ver", font="arial 12 bold", command=lambda: self.ventanaMediciones(idturno, fechaconsulta))
        self.botonV.grid(row=fila, column=5, padx=5, pady=5) 
    
    def ventanaMediciones(self, idturno, fechaconsulta):
        ventana = tk.Toplevel(self)
        ventana.title(f"{fechaconsulta}")
        ventana.geometry("700x400+200+50")
        ventana.config(bg="#C6D9E3")
        ventana.resizable(False, False)

        ventana.transient(self.master)
        ventana.grab_set()
        ventana.focus_set()
        ventana.lift()

        fondo = tk.Frame(ventana, bg="#C6D9E3")
        fondo.pack(fill="both", expand=True)

        tk.Label(ventana, text=f"{fechaconsulta}", font="arial 14 bold").pack(pady=20)

        consulta = "SELECT Medicion FROM Mediciones WHERE IdTurno = ?"
        resultado = self.consulta(consulta, (idturno,))

        if not resultado:
            tk.Label(fondo, text="No hay datos disponibles para este turno.", font="arial 12", bg="C6D9E3").pack()
            return
        
        try:
            vector = json.loads(resultado[0][0])
            tiempo = [p[0] for p in vector]
            angulo = [p[1] for p in vector]
        except(json.JSONDecodeError, IndexError) as e:
            tk.Label(fondo, text="Error al cargar datos.", font="arial 12", bg="C6D9E3").pack()
            return

        fig, ax = plt.subplots()
        ax.plot(tiempo, angulo, label="Medición angular")
        puntos = ax.plot(tiempo, angulo, 'o', color='blue', markersize=4)
        cursor = mplcursors.cursor(puntos, hover=True)
        cursor.connect("add", lambda sel: sel.annotation.set_text(f"{sel.target[1]:.2f}°"))
        ax.axhline(y=5, color='red', linestyle='-', linewidth=1)
        ax.axhline(y=-5, color='red', linestyle='-', linewidth=1)
        ax.axhline(y=0, color='black', linestyle='-', linewidth=1)
        ax.set_xlim(left=0)
        ax.set_xlabel("Tiempo (s)")
        ax.set_ylabel("Ángulo (°)")
        ax.set_title("Ángulo de inclinación del tronco")
        ax.legend()

        min_angle = min(angulo)
        max_angle = max(angulo)
        ymin = -7
        ymax = 7
        if min_angle < ymin:
            ymin = int(min_angle) - 1
        if max_angle > ymax:
            ymax = int(max_angle) + 1
   
        rango_y = ymax - ymin
        if rango_y <= 14:
            paso = 1
        elif rango_y <= 30:
            paso = 2
        elif rango_y <= 60:
            paso = 5
        else:
            paso = 10

        ax.set_ylim(ymin, ymax)
        neg_steps = int(np.ceil(abs(ymin) / paso))
        pos_steps = int(np.ceil(ymax / paso)) 
        ticks_g = np.arange(-neg_steps * paso, (pos_steps + 1) * paso, paso)
        ticks_p = np.arange(ymin, ymax + 1, 1)  
        ax.set_yticks(ticks_g)
        ax.set_yticks(ticks_p, minor=True)
        ax.grid(which='major', axis='y', linestyle='-', color='gray')
        ax.grid(which='minor', axis='y', linestyle=':', color='gray')

        canvas = FigureCanvasTkAgg(fig, master=fondo)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)

        def cerrarVentana():
            canvas.get_tk_widget().destroy()
            plt.close(fig)
            ventana.destroy()
        
        ventana.protocol("WM_DELETE_WINDOW", cerrarVentana)
    
    def VentanaComparacion(self, lista_idturnos):
        ventana = tk.Toplevel(self)
        ventana.title("Comparación de mediciones")
        ventana.geometry("750x450+250+80")
        ventana.config(bg="#C6D9E3")
        ventana.resizable(False, False)

        ventana.transient(self.master)
        ventana.grab_set()
        ventana.focus_set()
        ventana.lift()

        fondo = tk.Frame(ventana, bg="#C6D9E3")
        fondo.pack(fill="both", expand=True)

        tk.Label(ventana, text="Comparación de Mediciones", font="arial 14 bold").pack(pady=20)

        fig, ax = plt.subplots()

        min_global = float('inf')
        max_global = float('-inf')
        lista_puntos = []

        for i, idturno in enumerate(lista_idturnos):
            consulta = "SELECT Medicion FROM Mediciones WHERE IdTurno = ?"
            resultado = self.consulta(consulta, (idturno,))

            if not resultado:
                continue
            
            try:
                vector = json.loads(resultado[0][0])
                tiempo = [p[0] for p in vector]
                angulo = [p[1] for p in vector]

                min_global = min(min_global, min(angulo))
                max_global = max(max_global, max(angulo))

                fecha = self.consulta("SELECT FechaConsulta FROM Turnos WHERE IdTurno = ?", (idturno,))
                etiqueta = fecha[0][0] if fecha else f"Turno {idturno}"
                linea, = ax.plot(tiempo, angulo, label=etiqueta)
                color_linea = linea.get_color()
                puntos = ax.plot(tiempo, angulo, 'o', color=color_linea, markersize=4)
                lista_puntos.extend(puntos)
            except(json.JSONDecodeError, IndexError):
                continue
        
        cursor = mplcursors.cursor(lista_puntos, hover=True)
        cursor.connect("add", lambda sel: sel.annotation.set_text(f"{sel.target[1]:.2f}°"))

        ax.axhline(y=5, color='red', linestyle='-', linewidth=1)
        ax.axhline(y=-5, color='red', linestyle='-', linewidth=1)
        ax.axhline(y=0, color='black', linestyle='-', linewidth=1)
        ax.set_xlim(left=0)
        ax.set_xlabel("Tiempo (s)")
        ax.set_ylabel("Ángulo (°)")
        ax.set_title("Ángulo de inclinación del tronco")
        ax.legend()

        ymin = -7
        ymax = 7
        if min_global  < ymin:
            ymin = int(min_global) - 1
        if max_global  > ymax:
            ymax = int(max_global ) + 1

        rango_y = ymax - ymin
        if rango_y <= 14:
            paso = 1
        elif rango_y <= 30:
            paso = 2
        elif rango_y <= 60:
            paso = 5
        else:
            paso = 10

        ax.set_ylim(ymin, ymax)
        neg_steps = int(np.ceil(abs(ymin) / paso))
        pos_steps = int(np.ceil(ymax / paso)) 
        ticks_g = np.arange(-neg_steps * paso, (pos_steps + 1) * paso, paso)
        ticks_p = np.arange(ymin, ymax + 1, 1)  
        ax.set_yticks(ticks_g)
        ax.set_yticks(ticks_p, minor=True)
        ax.grid(which='major', axis='y', linestyle='-', color='gray')
        ax.grid(which='minor', axis='y', linestyle=':', color='gray')

        canvas = FigureCanvasTkAgg(fig, master=fondo)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)

        def cerrarVentana():
            canvas.get_tk_widget().destroy()
            plt.close(fig)
            ventana.destroy()

        ventana.protocol("WM_DELETE_WINDOW", cerrarVentana)


def configurarEje(ax, angulo):
    ax.axhline(y=5, color='red', linestyle='-', linewidth=1)
    ax.axhline(y=-5, color='red', linestyle='-', linewidth=1)
    ax.axhline(y=0, color='black', linestyle='-', linewidth=1)

    ymin = -7
    ymax = 7
    min_global = np.min(angulo)
    max_global = np.max(angulo)
    if min_global < ymin:
        ymin = int(min_global) - 1
    if max_global > ymax:
        ymax = int(max_global) + 1

    rango_y = ymax - ymin
    if rango_y <= 14:
        paso = 1
    elif rango_y <= 30:
        paso = 2
    elif rango_y <= 60:
        paso = 5
    else:
        paso = 10

    ax.set_ylim(ymin, ymax)
    ax.set_yticks(np.arange(ymin, ymax + 1, paso))
    ax.set_yticks(np.arange(ymin, ymax + 1, 1), minor=True)

    ax.grid(which='major', axis='y', linestyle='-', color='gray')
    ax.grid(which='minor', axis='y', linestyle=':', color='gray')
    ax.set_xlim(left=0)
    ax.set_xlabel("Tiempo (s)")
    ax.set_ylabel("Ángulo (°)")

    



       




