import sqlite3
conn = sqlite3.connect("DataClinica.db")
cur = conn.cursor()

pacientes = """
    CREATE TABLE IF NOT EXISTS Pacientes(
    IdPaciente INTEGER PRIMARY KEY AUTOINCREMENT,
    Nombre TEXT,
    Apellido TEXT,
    DNI INTEGER,
    FechaNacimiento TEXT,
    Edad INTEGER
    )"""

cur.execute(pacientes)

medicos = """
    CREATE TABLE IF NOT EXISTS Medicos(
    IdMedico INTEGER PRIMARY KEY AUTOINCREMENT,
    Nombre TEXT,
    Apellido TEXT,
    Matricula INTEGER,
    Contraseña TEXT,
    Usuario TEXT
    )"""
cur.execute(medicos)

turno = """
    CREATE TABLE IF NOT EXISTS Turnos(
    IdTurno INTEGER PRIMARY KEY AUTOINCREMENT,
    FechaConsulta TEXT,
    IdPaciente INTEGER,
    IdMedico INTEGER,
    FOREIGN KEY(IdPaciente) REFERENCES Pacientes(IdPaciente),
    FOREIGN KEY(IdMedico) REFERENCES Medicos(IdMedico) 
    )"""
cur.execute(turno)

mediciones = """
    CREATE TABLE IF NOT EXISTS Mediciones(
    IdMedicion INTEGER PRIMARY KEY AUTOINCREMENT,
    Medicion TEXT,
    IdTurno INTEGER,
    FOREIGN KEY(IdTurno) REFERENCES Turnos(IdTurno) 
    )"""
cur.execute(mediciones)

print("Base de datos creada")

conn.close()