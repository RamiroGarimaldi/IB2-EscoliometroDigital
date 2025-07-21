from tkinter import *
from tkinter import ttk
from Login import login
from Login import registro
from Container import pacientes
import sys
import os

class principal(Tk):
    def __init__(self, *args, **kwagrs):
        super().__init__(*args, **kwagrs)
        self.title("Escoliómetro Digital")
        self.geometry("1100x650+120+20")
        self.resizable(False, False)

        container = Frame(self)
        container.pack(side=TOP, fill=BOTH, expand=True)
        container.configure(bg="#C6D9E3")

        self.frames = {}
        for i in (login, registro, pacientes):
            frame = i(container, self)
            self.frames[i] = frame
        
        self.show_frame(login)

        self.style = ttk.Style()
        self.style.theme_use("clam")
    
    def show_frame(self, container):
        frame = self.frames[container]
        frame.tkraise()

def main():
    app = principal()
    app.mainloop()

if __name__ == "__main__":
    main()
