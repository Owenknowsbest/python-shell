from tkinter import *
from tkinter import ttk
import json
import os
from externel_windows import *


class App(Window):
    def __init__(self):
        super().__init__("User Auth")
        self.tree = ttk.Treeview(self.content, columns=("#1", "#2"))
        self.tree.heading("#1", text="Last log on")
        self.tree.heading("#2", text="Has Password")
        for user in os.listdir("users"):
            with open("users/" + user + "/data.json") as file:
                data = json.load(file)
                self.tree.insert("", END, user, text=user, values=(data["LastLogOn"], self.yn_string(data, "Password")))
        self.tree.grid(row=0, column=0)
        self.tree.bind("<<TreeviewOpen>>", self.edit_user)
        self.mainloop()

    def yn_string(self, data, s):
        if s in data:
            return "Yes"
        return "No"

    def edit_user(self, _):
        UserEdit(self.tree.selection()[0])
        self.tree.unbind("<<TreeviewOpen>>")
        self.after(0, lambda: self.close(""))


class Flag(Checkbutton):
    on = False

    def __init__(self, master=None, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.config(command=self.click)

    def click(self):
        self.on = not self.on

    def set(self, value: bool):
        self.on = value
        if value:
            self.select()
        else:
            self.deselect()


class UserEdit(Window):
    flags = []

    def __init__(self, user="admin"):
        super().__init__("User Edit - "+user)
        self.userData = {}
        self.user = user
        with open("users/"+user+"/data.json") as file:
            self.userData = json.load(file)
        self.flagsEnable = Flag(self.content, text="Enable Perms")
        self.flagsEnable.set("Perms" in self.userData)
        self.flagsEnable.grid(row=0, column=0, sticky=NW)
        if "Perms" not in self.userData:
            self.userData["Perms"] = 0
        self.flags.append(Flag(self.content, text="UNUSED"))
        self.flags.append(Flag(self.content, text="UNUSED"))
        self.flags.append(Flag(self.content, text="UNUSED"))
        self.flags.append(Flag(self.content, text="UNUSED"))
        self.flags.append(Flag(self.content, text="UNUSED"))
        self.flags.append(Flag(self.content, text="UNUSED"))
        self.flags.append(Flag(self.content, text="UNUSED"))
        self.flags.append(Flag(self.content, text="UNUSED"))
        row = 1
        for flag in self.flags:
            mask = 0b00000001
            mask <<= row - 1
            if self.userData["Perms"] & mask == mask:
                flag.set(True)
            flag.grid(row=row, column=0, sticky=NW)
            row += 1
        self.update_button = Button(self.content, text="Update User", command=self.save_user)
        self.update_button.grid(row=row, column=0, sticky=NW)

    def save_user(self):
        with open("users/"+self.user+"/data.json", "w") as file:
            if self.flagsEnable.on:
                perm_val = 0
                mask = 0b00000001
                for flag in self.flags:
                    if flag.on:
                        perm_val |= mask
                    mask <<= 1
                self.userData["Perms"] = perm_val
            elif not self.flagsEnable.on and "Perms" in self.userData:
                del self.userData["Perms"]
            json.dump(self.userData, file)


app = App()
