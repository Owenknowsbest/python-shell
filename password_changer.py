from tkinter import *
from tkinter import ttk
from externel_windows import *
import hashlib
import json
import os


with open("config.json") as file:
    global config
    config = json.load(file)


class App(Window):
    def __init__(self):
        super().__init__("Password Changer")
        self.tree = ttk.Treeview(self.content, columns=("#1", "#2"))
        self.tree.heading("#1", text="Last log on")
        self.tree.heading("#2", text="Has Password")
        for user in os.listdir("users"):
            with open("users/" + user + "/data.json") as file:
                data = json.load(file)
                self.tree.insert("", END, user, text=user, values=(data["LastLogOn"], self.yn_string(data, "Password")))
        self.tree.grid(row=0, column=0, columnspan=4)
        self.tree.bind("<<TreeviewOpen>>", self.login)
        self.password = Entry(self.content, show="\u200b")
        if config["PasswordFieldUse*"]:
            self.password.config(show="*")
        self.password.grid(row=1, column=1, sticky=W)
        Label(self.content, text="Password:").grid(row=1, column=0, sticky=W)

        self.newpassword = Entry(self.content, show="\u200b")
        if config["PasswordFieldUse*"]:
            self.newpassword.config(show="*")
        self.newpassword.grid(row=1, column=3, sticky=W)
        Label(self.content, text="New Password:").grid(row=1, column=2, sticky=W)
        self.mainloop()

    def yn_string(self, data, s):
        if s in data:
            return "Yes"
        return "No"

    def login(self, *args):
        userdata = {}
        with open("users/"+self.tree.selection()[0]+"/data.json") as file:
            userdata = json.load(file)
        if "Password" in userdata:
            if hashlib.md5(bytes(self.password.get(), "utf-8")).hexdigest() == userdata["Password"]:
                if self.newpassword.get() == "":
                    del userdata["Password"]
                else:
                    userdata["Password"] = hashlib.md5(bytes(self.newpassword.get(), "utf-8")).hexdigest()
                with open("users/"+self.tree.selection()[0]+"/data.json", "w") as file:
                    json.dump(userdata, file)
        else:
            if self.newpassword.get() == "":
                del userdata["Password"]
            else:
                userdata["Password"] = hashlib.md5(bytes(self.newpassword.get(), "utf-8")).hexdigest()
            with open("users/" + self.tree.selection()[0] + "/data.json", "w") as file:
                json.dump(userdata, file)


app = App()
