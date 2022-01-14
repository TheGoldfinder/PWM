from asyncio.windows_events import NULL
from tkinter import *
import cryptocode
import requests
import json


uppercaseLetters = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K",
                    "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z", "ß"]

lowercaseLetters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k',
                    'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', "ß"]

uppercaseUmlaut = ["Ä", "Ö", "Ü"]

lowercaseUmlaut = ["ä", "ö", "ü"]

numbers = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "0"]

specialCharacter = ["!", "\"", "/", "\'", "#", "+", "*", "~", ",", ".", "-", "_", "´", "`",
                    "?", "=", "}", ")", "]", "(", "[", "{", "&", "%", "$", "§", "^", "°", "<", ">", "|", "@", "€"]

key = ""

switch = 0

apiAdress = "http://127.0.0.1:8000"


class LogIn(Tk):
    def __init__(self):
        super().__init__()
        self.geometry("300x400")
        self.title("PWM LogIn")
        self.resizable(False, False)

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
        global key

        self.email.config(state=DISABLED)
        self.passwordBox.config(state=DISABLED)
        self.checkPasswordField()

        emailFieldOutput = self.email.get("1.0", 'end-1c')
        pwFieldOutput = self.passwordBox.get("1.0", 'end-1c')

        areConnected = False
        jsonConnectedList = ""
        try:
            areConnected = requests.get(apiAdress + "/")
            jsonConnectedList = json.loads(areConnected.text)
        except:
            areConnected = False
            jsonTemporarily = {"connected": False}
            jsonTemporarily = json.dumps(jsonTemporarily)
            jsonConnectedList = json.loads(jsonTemporarily)
            print("No api request could be send")

        if not jsonConnectedList["connected"]:
            self.labelError.config(
                text="No internet connection\nor our servers are down", foreground="red")
            return

        if "@" not in emailFieldOutput:
            self.labelError.config(
                text="No e-mail recognized", foreground="red")
            return

        try:
            keyRequestResponse = requests.get(apiAdress + "/getKey")
        except:
            print("No api request kould be sendNo request kould be send")
        keyRequestResponse = json.loads(keyRequestResponse.text)
        key = keyRequestResponse["key"]

        emailFieldOutput = cryptocode.encrypt(emailFieldOutput, key)
        pwFieldOutput = cryptocode.encrypt(pwFieldOutput, key)

        loginResponse = requests.get(
            f"{apiAdress}/login?email={emailFieldOutput}&password={pwFieldOutput}")
        print(loginResponse.text)

        # if pwFieldOutput != "" and len(pwFieldOutput) >= 12:
        # if not os.path.isfile(fileName):
        # with open(fileName, "x") as file:
        #file.write(self.encodePW(pwFieldOutput, pwFieldOutput))
        # self.switchWindows()

        # elif os.path.isfile(fileName):
        # with open(fileName, "r") as file:
        #readIn = file.read()
        #output = self.decodePW(readIn, pwFieldOutput)

        # if output[0] == pwFieldOutput and output[1] == True:
        # self.switchWindows()

        # else:
        # self.labelError.config(
        # text="!!!False Password!!!", foreground="red")
        # self.passwordBox.config(state=NORMAL)

        # else:
        # self.labelError.config(
        # text="!!!Your Password is not long enough\nor it is emty!!!", foreground="red")
        # self.passwordBox.config(state=NORMAL)

    # Switch window

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
