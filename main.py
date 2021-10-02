import json
import datetime
import os
import pathlib
from os.path import isfile
from tkinter import *
from tkinter import ttk
import sys
import shutil
import hashlib


addons = []
with open("config.json") as file:
    global config
    config = json.load(file)


class Window(Frame):
    pos = [0, 0]

    def __init__(self, master=None, no_close_button=False):
        super().__init__(master)
        self.titleBar = Frame(self, bg="#00F")
        self.titleBar.pack(fill=X)
        self.titleText = Label(self.titleBar, text="SubWindow", bg="#00f", fg="#eee", font="Helvetica 10 bold")
        self.titleText.pack(padx=4, pady=2, side=LEFT)
        self.titleBar.bind("<B1-Motion>", self.move)
        self.titleBar.bind("<Button-1>", self.start_move)
        self.titleText.bind("<B1-Motion>", self.move)
        self.titleText.bind("<Button-1>", self.start_move)
        if not no_close_button:
            self.closeButton = Label(self.titleBar, text="X", bg="#f00", fg="#eee", font="Helvetica 10 bold")
            self.closeButton.pack(side=RIGHT, padx=4, pady=2)
            self.closeButton.bind("<ButtonRelease-1>", self.close)
        self.content = Frame(self)
        self.content.pack()

    def close(self, _=""):
        self.master.windows.remove(self)
        self.destroy()

    def move(self, e):
        target = [self.winfo_x() + e.x - self.pos[0], self.winfo_y() + e.y - self.pos[1]]
        if target[0] + self.winfo_width() > self.master.winfo_width():
            target[0] = self.master.winfo_width() - self.winfo_width()
        if target[1] + self.titleBar.winfo_height() > self.master.winfo_height():
            target[1] = self.master.winfo_height() - self.titleBar.winfo_height()
        if target[0] < 0:
            target[0] = 0
        if target[1] < 0:
            target[1] = 0
        self.place(x=target[0], y=target[1])

    def start_move(self, e):
        self.pos = [e.x, e.y]
        self.tkraise()

    def update_pos(self):
        target = [self.winfo_x(), self.winfo_y()]
        if target[0] + self.winfo_width() > self.master.winfo_width():
            target[0] = self.master.winfo_width() - self.winfo_width()
        if target[1] + self.titleBar.winfo_height() > self.master.winfo_height():
            target[1] = self.master.winfo_height() - self.titleBar.winfo_height()
        if target[0] < 0:
            target[0] = 0
        if target[1] < 0:
            target[1] = 0
        self.place(x=target[0], y=target[1])

    def title(self, title: str):
        self.titleText.config(text=title)


class Applications(Window):
    def __init__(self, master=None):
        super().__init__(master, True)
        self.title("Apps")
        self.consoleButton = Button(self.content, text="Console", command=self.console_button_click)
        self.consoleButton.grid(row=0, column=0, sticky=W)
        self.fileExplorerButton = Button(self.content, text="File Explorer", command=self.file_explorer_button_click)
        self.fileExplorerButton.grid(row=1, column=0, sticky=W)
        self.notepadButton = Button(self.content, text="Notepad", command=self.notepad_button_click)
        self.notepadButton.grid(row=2, column=0, sticky=W)
        self.addonManagerButton = Button(self.content, text="Addon Manager", command=self.addon_button_click)
        self.addonManagerButton.grid(row=3, column=0, sticky=W)
        self.logoutButton = Button(self.content, text="Logout", command=self.logout)
        self.logoutButton.grid(row=4, column=0, sticky=W)
        self.shutdownButton = Button(self.content, text="Shutdown", command=self.shutdown_button_click)
        self.shutdownButton.grid(row=5, column=0, sticky=W)
        self.delUserButton = Button(self.content, text="Delete This User", command=self.delete_this_user)
        self.delUserButton.grid(row=6, column=0, sticky=W)

    def addon_button_click(self):
        self.master.add_window(AddonManager)

    def delete_this_user(self):
        with open("data.json") as file:
            data = json.load(file)
            if "Perms" in data:
                return
        user_dir = os.getcwd()
        os.chdir("../..")
        shutil.rmtree(user_dir)
        del user_dir
        self.close()
        self.master.add_window(Login)

    def logout(self):
        os.chdir("../..")
        self.master.close_all_windows()
        self.master.add_window(Login)

    def console_button_click(self):
        self.master.add_window(Console)

    def file_explorer_button_click(self):
        self.master.add_window(FileExplorer)

    def notepad_button_click(self):
        self.master.add_window(Notepad)

    def shutdown_button_click(self):
        self.master.quit()


class Notepad(Window):
    def __init__(self, master=None, file=None):
        super().__init__(master)
        self.title("Notepad")
        self.text = Text(self.content)
        self.file = file
        if file is not None:
            self.title("Notepad - "+file)
            with open(file, "r") as file:
                self.text.insert("1.0", file.read())
        self.text.grid(row=0, column=0)
        self.text.bind("<Control-Key-s>", self.save)

    def save(self, _=""):
        if self.file is None:
            return
        with open(self.file, "w") as file:
            file.write(self.text.get("1.0", END))


class FileCreateDialog(Window):
    def __init__(self, master=None, _dir=None):
        super().__init__(master)
        if _dir is None or isfile(_dir):
            self.close()
            return
        self.title("Create File in "+_dir)
        self.dir = _dir
        self.entry = Entry(self.content)
        self.entry.grid(row=0, column=0)
        self.button = Button(self.content, text="Create", command=self.create)
        self.button.grid(row=0, column=1)

    def create(self):
        wd = os.getcwd()
        os.chdir(self.dir)
        open(self.entry.get(), "w").close()
        os.chdir(wd)
        self.close()


class FolderCreateDialog(Window):
    def __init__(self, master=None, _dir=None):
        super().__init__(master)
        if _dir is None or isfile(_dir):
            self.close()
            return
        self.title("Create Folder in "+_dir)
        self.dir = _dir
        self.entry = Entry(self.content)
        self.entry.grid(row=0, column=0)
        self.button = Button(self.content, text="Create", command=self.create)
        self.button.grid(row=0, column=1)

    def create(self):
        os.mkdir(self.dir+"/"+self.entry.get())
        self.close()


class FileExplorer(Window):
    fileFormats = {
        "txt": "Plain Text",
        "py": "Python",
        "wos": "WOS Script"
    }

    def __init__(self, master=None):
        super().__init__(master)
        self.title("File Explorer")
        self.createFileButton = Button(self.content, text="Create File", command=self.create_file)
        self.createFileButton.grid(row=0, column=0, sticky=W)
        self.createFolderButton = Button(self.content, text="Create Folder", command=self.create_folder)
        self.createFolderButton.grid(row=0, column=1, sticky=W)
        self.deleteFileButton = Button(self.content, text="Delete", command=self.delete_file)
        self.deleteFileButton.grid(row=0, column=2, sticky=W)
        self.refreshButton = Button(self.content, text="Refresh", command=self.refresh)
        self.refreshButton.grid(row=0, column=3, sticky=W)
        self.tree = ttk.Treeview(self.content, columns=("#1", "#2", "#3"))
        self.tree.heading("#1", text="File Name")
        self.tree.heading("#2", text="File Extension")
        self.tree.heading("#3", text="File Size")
        self.tree.grid(row=1, column=0, columnspan=4)
        self.tree.bind("<<TreeviewOpen>>", self.open_file)
        self.do_base_dir()

    def create_file(self):
        if len(self.tree.selection()) > 0:
            self.master.add_window(FileCreateDialog, self.tree.selection()[0])

    def create_folder(self):
        if len(self.tree.selection()) > 0:
            self.master.add_window(FolderCreateDialog, self.tree.selection()[0])

    def refresh(self):
        self.tree.delete(*self.tree.get_children())
        self.do_base_dir()

    def get_file_format(self, file):
        ext = file.split(".")[-1]
        if ext in self.fileFormats:
            return self.fileFormats[ext]
        else:
            return "Unknown"

    def do_sub_dir(self, _dir):
        for file in os.listdir("my_stuff/" + _dir):
            if isfile("my_stuff/" + _dir + "/" + file):
                self.tree.insert("my_stuff/" + _dir, END, "my_stuff/"+_dir+"/"+file, text="|",
                                 values=(file, self.get_file_format(file),
                                         str(os.stat("my_stuff/" + _dir + "/" + file)
                                         .st_size) + " Bytes"))
            else:
                self.tree.insert("my_stuff/" + _dir, END, "my_stuff/"+_dir+"/"+file, text=file)
                self.do_sub_dir(_dir+"/"+file)

    def open_file(self, _):
        if isfile(self.tree.selection()[0]):
            self.master.add_window(Notepad, self.tree.selection()[0])

    def delete_file(self):
        if len(self.tree.selection()) > 0:
            if isfile(self.tree.selection()[0]):
                os.remove(self.tree.selection()[0])
            else:
                shutil.rmtree(self.tree.selection()[0])
        self.refresh()

    def do_base_dir(self):
        self.tree.insert("", END, "my_stuff", text="My Stuff", open=True)
        for file in os.listdir("my_stuff"):
            if isfile("my_stuff/"+file):
                self.tree.insert("my_stuff", END, "my_stuff/"+file, text="|",
                                 values=(file, self.get_file_format(file),
                                         str(os.stat("my_stuff/"+file).st_size)+" Bytes"))
            else:
                self.tree.insert("my_stuff", END, "my_stuff/"+file, text=file)
                self.do_sub_dir(file)


loggerOpen = False


class Logger(Window):
    def __init__(self, master=None):
        super().__init__(master)
        global loggerOpen
        loggerOpen = True
        self.title("Logger")
        self.text = Text(self.content, state=DISABLED)
        self.text.grid(row=0, column=0)
        sys.stdout = self

    def close(self, _=""):
        sys.stdout = stdout
        global loggerOpen
        loggerOpen = False
        super().close()

    def write(self, s):
        self.text["state"] = NORMAL
        self.text.insert("end", s)
        stdout.write(s)
        self.text["state"] = DISABLED

    def flush(self):
        self.text["state"] = NORMAL
        self.text.delete("1.0", "end")
        self.text["state"] = DISABLED

    def read(self, n):
        self.text["state"] = self.text["state"]
        stdout.read(n)


class Console(Window):
    inputStart = "end"
    inputActive = False

    def __init__(self, master=None):
        super().__init__(master)
        self.title("Console")
        self.text = Text(self.content, state=DISABLED)
        self.text.grid(row=0, column=0)
        self.text.bind("<Return>", self.end_input)
        self.text.bind("<Key>", self.input)
        self.print("WOS Console v1.0")
        self.start_input()
        self.text.focus()

    def print(self, text: str):
        old_state = self.text["state"]
        self.text["state"] = NORMAL
        self.text.insert(END, text+"\n")
        self.text["state"] = old_state

    def start_input(self):
        self.inputActive = True
        self.text["state"] = NORMAL
        self.text.insert(END, "\n>")
        self.inputStart = self.text.index(INSERT)

    def end_input(self, _=""):
        if self.text.index(INSERT) > self.text.index(self.inputStart):
            self.inputActive = False
            command = self.text.get(self.inputStart, END)[:-1]
            self.handle_command(command)
            self.start_input()
        return "break"

    def cancel_input(self):
        self.inputActive = False
        self.text["state"] = DISABLED
        self.inputStart = END
        self.print("")

    def input(self, _=""):
        if self.text.index(INSERT) < self.text.index(self.inputStart):
            return "break"

    def handle_command(self, command: str):
        args = command.split(" ")
        if args[0] == "fullscreen":
            self.master.attributes("-fullscreen", args[1] != "0")
            return
        if args[0] == "logger" and not loggerOpen:
            self.master.add_window(Logger)
            return
        if args[0] == "log":
            print(*args[1:])
            return
        if args[0] == "help":
            self.print("\n-- Commands --")
            self.print("fullscreen <0, 1>")
            self.print("logger - opens logger (only one can be open at a time)")
            self.print("log * - prints things to console / logger")
            self.print("close - close console (for wos scripts)")
            self.print("open - opens a window (for wos scripts)")
            self.print("script - starts a script")
            self.print("shutdown")
            return
        if args[0] == "open":
            windows = {
                "Notepad": Notepad,
                "FileExplorer": FileExplorer
            }
            self.master.add_window(windows[args[1]])
            return
        if args[0] == "close":
            self.close()
            return
        if args[0] == "script":
            console = self
            with open("my_stuff/"+" ".join(args[1:]), "r") as file:
                lines = file.readlines()
                console.cancel_input()
                closed = False
                for line in lines:
                    console.print("script>" + line[:-1])
                    console.handle_command(line[:-1])
                    if line[:-1] == "close":
                        closed = True
                        break
                if not closed:
                    console.start_input()
            return
        if args[0] == "shutdown":
            self.master.quit()
            return
        self.print(f"\nINVALID COMMAND \"{args[0]}\"")
        self.print("use help for a list of commands")


class UserCreate(Window):
    def __init__(self, master=None):
        super().__init__(master)
        self.title("Create User")
        Label(self.content, text="Username:").grid(row=0, column=0)
        self.Username = Entry(self.content)
        self.Username.grid(row=0, column=1)
        Label(self.content, text="Password (Leave blank for none):").grid(row=1, column=0)
        self.Password = Entry(self.content)
        self.Password.grid(row=1, column=1)
        self.Button = Button(self.content, text="Create", command=self.create_user)
        self.Button.grid(row=2, column=0)

    def create_user(self):
        if pathlib.Path("users/"+self.Username.get()).exists():
            return
        os.mkdir("users/"+self.Username.get())
        os.mkdir("users/"+self.Username.get()+"/my_stuff")
        with open("users/"+self.Username.get()+"/data.json", "w") as file:
            data = {
                "LastLogOn": "Never"
            }
            if self.Password.get() != "":
                data["Password"] = hashlib.md5(bytes(self.Password.get(), "utf-8")).hexdigest()
            json.dump(data, file)
        self.close()


class Login(Window):
    def __init__(self, master=None):
        super().__init__(master, True)
        self.title("Login")
        self.tree = ttk.Treeview(self.content, columns=("#1", "#2"))
        self.tree.heading("#1", text="Last log on")
        self.tree.heading("#2", text="Has Password")
        for user in os.listdir("users"):
            with open("users/"+user+"/data.json") as file:
                data = json.load(file)
                self.tree.insert("", END, user, text=user, values=(data["LastLogOn"], self.yn_string(data, "Password")))
        self.password = Entry(self.content, show="\u200b")
        if config["PasswordFieldUse*"]:
            self.password.config(show="*")
        self.password.grid(row=2, column=1, sticky=W)
        Label(self.content, text="Password:").grid(row=2, column=0, sticky=W)
        self.tree.bind("<<TreeviewOpen>>", self.login)
        self.tree.grid(row=1, column=0, columnspan=4)
        self.button = Button(self.content, text="Create User", command=self.open_create_user)
        self.button.grid(row=0, column=0)
        self.refresh = Button(self.content, text="Refresh Users", command=self.refresh_users)
        self.refresh.grid(row=0, column=1)
        self.shutdownButton = Button(self.content, text="Shutdown", command=self.shutdown)
        self.shutdownButton.grid(row=0, column=2)

    def shutdown(self):
        self.close()
        self.master.quit()

    def open_create_user(self):
        self.master.add_window(UserCreate)

    def refresh_users(self):
        self.tree.delete(*self.tree.get_children())
        for user in os.listdir("users"):
            with open("users/"+user+"/data.json") as file:
                data = json.load(file)
                self.tree.insert("", END, user, text=user, values=(data["LastLogOn"], self.yn_string(data, "Password")))

    def yn_string(self, data, s):
        if s in data:
            return "Yes"
        return "No"

    def login(self, _):
        with open("users/"+self.tree.selection()[0]+"/data.json") as file:
            data = json.load(file)
            if "Password" in data and hashlib.md5(bytes(self.password.get(), "utf-8")).hexdigest() != data["Password"]:
                return
        os.chdir("users/"+self.tree.selection()[0])
        self.master.add_window(Applications)
        self.close()
        self.data = {}
        with open("data.json") as file:
            self.data = json.load(file)
        with open("data.json", "w") as file:
            self.data["LastLogOn"] = datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
            json.dump(self.data, file)
        del self.data
        if pathlib.Path.exists(pathlib.Path("my_stuff/autoexec.wos")):
            self.master.add_window(Console)
            console = self.master.windows[-1]
            with open("my_stuff/autoexec.wos", "r") as file:
                lines = file.readlines()
                console.cancel_input()
                closed = False
                for line in lines:
                    console.print("autoexec>"+line[:-1])
                    console.handle_command(line[:-1])
                    if line[:-1] == "close":
                        closed = True
                        break
                if not closed:
                    console.start_input()


class AddonManager(Window):
    def __init__(self, master=None):
        super().__init__(master)
        self.title("Addon Manager")
        self.tree = ttk.Treeview(self.content)
        self.tree.heading("#0", text="Name")
        self.tree.grid(row=0, column=0)
        self.tree.bind("<<TreeviewOpen>>", self.run_addon)
        self.update_addon_list()

    def update_addon_list(self):
        self.tree.delete(*self.tree.get_children())
        for addon in os.listdir("../../addons"):
            if pathlib.Path("../../addons/"+addon+"/config.json").exists():
                self.tree.insert("", END, addon, text=addon)

    def run_addon(self, _):
        addon = self.master.add_window(AddonWindow, "../../addons/"+self.tree.selection()[0])
        addons.append(addon)


class AddonButton(Button):
    def __init__(self, master=None, text="", element_id=None, event_command=None):
        super().__init__(master, text=text)
        self.id = element_id
        self.config(command=self.click)
        self.event_command = event_command

    def click(self):
        if self.event_command is not None:
            self.event_command(self.id, "click")
            return


class AddonWindow(Window):
    elements = {}
    events = {}

    def __init__(self, master=None, addon=None):
        super().__init__(master)
        if addon is None:
            self.close()
            return
        with open(addon+"/config.json") as file:
            self.data = json.load(file)
        self.title(self.data["title"])
        elements = {
            "label": lambda data: self.new_label(data),
            "button": lambda data: self.new_button(data)
        }
        for element in self.data["content"]:
            if element["Type"].lower() in elements:
                elements[element["Type"].lower()](element)

    def new_label(self, data):
        if "id" not in data:
            label = Label(self.content, text=data["text"])
            label.grid(row=data["grid"]["y"], column=data["grid"]["x"],
                       rowspan=data["grid"]["h"], columnspan=data["grid"]["w"])
            return
        self.elements[data["id"]] = Label(self.content, text=data["text"])
        self.elements[data["id"]].grid(row=data["grid"]["y"], column=data["grid"]["x"],
                                       rowspan=data["grid"]["h"], columnspan=data["grid"]["w"])

    def new_button(self, data):
        if "id" not in data:
            return
        self.elements[data["id"]] = AddonButton(self.content, text=data["text"], element_id=data["id"],
                                                event_command=self.handle_event)
        self.elements[data["id"]].grid(row=data["grid"]["y"], column=data["grid"]["x"],
                                       rowspan=data["grid"]["h"], columnspan=data["grid"]["w"])
        if data["id"] in self.data["events"]:
            self.events[data["id"]] = self.data["events"][data["id"]]

    def handle_event(self, eid, event_type):
        actions = {
            "log": lambda args: self.log_action(args)
        }
        if eid in self.events:
            if event_type in self.events[eid]:
                if self.events[eid][event_type]["Type"] in actions:
                    actions[self.events[eid][event_type]["Type"]](self.events[eid][event_type]["args"])

    def log_action(self, args):
        print(args[0])


class App(Tk):
    pos = [0, 0]
    windows = []

    def __init__(self):
        super().__init__()
        self.geometry("1000x600")
        self.attributes("-fullscreen", True)
        if config["Background"]["Transparent"]:
            self.wm_attributes("-transparentcolor", config["Background"]["Color"])
        self.config(bg=config["Background"]["Color"])
        self.bind("<Configure>", self.update_windows)
        self.add_window(Login)
        self.mainloop()

    def add_window(self, cls, *args):
        window = cls(self, *args)
        self.windows.append(window)
        window.place(x=0, y=0)

    def update_windows(self, e):
        for window in self.windows:
            window.update_pos()

    def close_all_windows(self):
        for window in self.windows:
            window.destroy()
        self.windows = []


stdout = sys.stdout
app = App()
sys.stdout = stdout
