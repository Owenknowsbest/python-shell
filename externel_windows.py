from tkinter import *


class Window(Tk):
    pos = [0, 0]

    def __init__(self, title):
        super().__init__()
        self.overrideredirect(True)
        self.attributes('-topmost', True)
        self.titleBar = Frame(self, bg="#00F")
        self.titleBar.pack(fill=X)
        self.titleText = Label(self.titleBar, text=title, bg="#00f", fg="#eee", font="Helvetica 10 bold")
        self.titleText.pack(padx=4, pady=2, side=LEFT)
        self.titleBar.bind("<B1-Motion>", self.move)
        self.titleBar.bind("<Button-1>", self.start_move)
        self.titleText.bind("<B1-Motion>", self.move)
        self.titleText.bind("<Button-1>", self.start_move)
        self.closeButton = Label(self.titleBar, text="X", bg="#f00", fg="#eee", font="Helvetica 10 bold")
        self.closeButton.pack(side=RIGHT, padx=4, pady=2)
        self.closeButton.bind("<ButtonRelease-1>", self.close)
        self.content = Frame(self)
        self.content.pack()

    def close(self, _=""):
        self.destroy()

    def move(self, e):
        self.geometry(f"+{self.winfo_x() + e.x - self.pos[0]}+{self.winfo_y() + e.y - self.pos[1]}")

    def start_move(self, e):
        self.pos = [e.x, e.y]
        self.tkraise()
