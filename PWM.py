from asyncio.windows_events import NULL
from tkinter import *
import tkinter
from typing import final
import cryptocode
import requests
import json

email = ""
password = ""

apiAdress = "http://127.0.0.1:8000"
key = ""

switch = 0


class LogIn(Tk):
    register = ""

    def __init__(self):
        super().__init__()
        self.geometry("300x400")
        self.title("PWM LogIn")
        self.resizable(False, False)

        self.register = tkinter.IntVar()

        self.labelInfo = Label(self, text="E-mail")
        self.labelInfo.config(font=("Arial", 12))
        self.labelInfo.place(relx=0.28, rely=0.19, anchor="center")

        self.email = Text(self, width=20, height=1)
        self.email.config(font=("Arial", 12), wrap="none")
        self.email.place(relx=0.5, rely=0.25, anchor="center")

        self.labelInfo = Label(self, text="Password")
        self.labelInfo.config(font=("Arial", 12))
        self.labelInfo.place(relx=0.32, rely=0.34, anchor="center")

        self.passwordBox = Text(self, width=20, height=1)
        self.passwordBox.config(font=("Arial", 12), wrap="none")
        self.passwordBox.place(relx=0.5, rely=0.4, anchor="center")

        self.labelError = Label(self, text="")
        self.labelError.config(font=("Arial", 12))
        self.labelError.place(relx=0.5, rely=0.46, anchor="center")

        self.logInButton = Button(
            self, width=12, height=2, text="Log In", command=self.logIn)
        self.logInButton.config(font=("Arial", 12))
        self.logInButton.place(relx=0.5, rely=0.6, anchor="center")

        self.labelError = Label(self, text="No Enter and no Space")
        self.labelError.config(font=("Arial", 12))
        self.labelError.place(relx=0.5, rely=0.8, anchor="center")

        self.registerCheckBox = Checkbutton(
            self, text="Register", variable=self.register)
        self.registerCheckBox.config(font=("Arial", 12))
        self.registerCheckBox.place(relx=0.5, rely=0.95, anchor="s")

    # Check the Password field if all is right
    def checkPasswordField(self):
        # get input from text field
        passwordFieldOutput = self.passwordBox.get("1.0", 'end-1c')
        emailFieldOutput = self.email.get("1.0", 'end-1c')

        # get rid of spaces and enter
        passwordFieldOutput = passwordFieldOutput.replace(" ", "")
        passwordFieldOutput = passwordFieldOutput.replace("\n", "")
        emailFieldOutput = emailFieldOutput.replace(" ", "")
        emailFieldOutput = emailFieldOutput.replace("\n", "")

        # changes the text in the input field to a valid password
        self.passwordBox.delete(1.0, "end")
        self.email.delete(1.0, "end")
        self.passwordBox.insert(1.0, passwordFieldOutput)
        self.email.insert(1.0, emailFieldOutput)

    # Log in check
    def logIn(self):
        global key, email, password

        # Disable textboxes
        self.email.config(state=DISABLED)
        self.passwordBox.config(state=DISABLED)
        self.checkPasswordField()

        # get text from text fields
        emailFieldOutput = self.email.get("1.0", 'end-1c')
        pwFieldOutput = self.passwordBox.get("1.0", 'end-1c')

        areConnected = False
        jsonConnectedList = ""
        # check if connected
        try:
            # send api request to home
            areConnected = requests.get(apiAdress + "/")
            jsonConnectedList = json.loads(areConnected.text)
        except:
            # if offline
            jsonTemporarily = {"connected": False}
            jsonTemporarily = json.dumps(jsonTemporarily)
            jsonConnectedList = json.loads(jsonTemporarily)
            print("No api request could be send")

        # if not connected
        if not jsonConnectedList["connected"]:
            self.labelError.config(
                text="No internet connection\nor our servers are down", foreground="red")
            return

        # check if @ in email
        if "@" not in emailFieldOutput:
            self.labelError.config(
                text="No e-mail recognized", foreground="red")
            return

        try:
            # get key from api
            keyRequestResponse = requests.get(apiAdress + "/getKey")
            print(keyRequestResponse.text)
        except:
            print("No api request could be send No request could be send")
        # set key
        keyRequestResponse = json.loads(keyRequestResponse.text)
        key = keyRequestResponse["key"]

        # encrypt email and password
        emailFieldOutput = cryptocode.encrypt(emailFieldOutput, key)
        pwFieldOutput = cryptocode.encrypt(pwFieldOutput, key)

        # if want to register
        if self.register == 1:
            self.registerNewUser(emailFieldOutput, pwFieldOutput, key)
            return

        try:
            # request login send encrypted email and password
            loginResponse = requests.get(
                f"{apiAdress}/login?email={emailFieldOutput}&password={pwFieldOutput}")
        finally:
            print(loginResponse.text)

    def registerNewUser(email, password, key):
        try:
            # request register send encrypted email and password
            response = requests.get(
                f"{apiAdress}/register?email={email}&password={password}")
        finally:
            print
        return

    def switchWindows(self):
        global switch
        switch = 1
        self.withdraw()
        App().mainloop()

    # Encode
    def encodePW(self, encodeString, key):
        return cryptocode.encrypt(encodeString, key)

    # Decode
    def decodePW(self, decodeString, key):
        output = []
        output.insert(0, cryptocode.decrypt(decodeString, key))

        if output[0] == "":
            output.insert(1, False)
        elif output[0] != "":
            output.insert(1, True)
        return output


class App(Tk):
    def __init__(self):
        super().__init__()
        self.geometry("300x400")
        self.title("PWM Password Manager")
        self.resizable(False, False)

        self.btnPassword = Button(
            self, text="New Password", width=14, height=3, command=self.generatePassword)
        self.btnPassword.config(font=("Arial", 12))
        self.btnPassword.place(relx=0.5, rely=0.6, anchor="center")

    def generatePassword(self):
        return


if __name__ == "__main__":
    if switch == 0:
        LogIn().mainloop()
    elif switch == 1:
        App().mainloop()
