# Work in progress



from tkinter import *
import cryptocode
import os

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


class LogIn(Tk):
    def __init__(self):
        super().__init__()
        self.geometry("300x400")
        self.title("PWM LogIn")
        self.resizable(False, False)

        self.labelInfo = Label(self, text="Min PW lenght 12 no spaces")
        self.labelInfo.config(font=("Arial", 12))
        self.labelInfo.place(relx=0.5, rely=0.3, anchor="center")

        self.textInput = Text(self, width=20, height=1)
        self.textInput.config(font=("Arial", 12), wrap="none")
        self.textInput.place(relx=0.5, rely=0.4, anchor="center")

        self.labelError = Label(self, text="")
        self.labelError.config(font=("Arial", 12))
        self.labelError.place(relx=0.5, rely=0.8, anchor="center")

        self.logInButton = Button(
            self, width=12, height=3, text="Log In", command=self.logIn)
        self.logInButton.config(font=("Arial", 12))
        self.logInButton.place(relx=0.5, rely=0.6, anchor="center")

        self.after(800, self.checkPasswordField)

    # Check the Password field if all is right
    def checkPasswordField(self):
        # get input from text field
        passwordFieldOutput = self.textInput.get("1.0", 'end-1c')

        # get rid of spaces and enter
        passwordFieldOutput = passwordFieldOutput.replace(" ", "")
        passwordFieldOutput = passwordFieldOutput.replace("\n", "")

        # changes the text in the input field to a valid password
        self.textInput.delete(1.0, "end")
        self.textInput.insert(1.0, passwordFieldOutput)

        self.after(800, self.checkPasswordField)

    # Log in check
    def logIn(self):
        fileName = "login.txt"
        self.textInput.config(state=DISABLED)
        self.checkPasswordField()

        pwFieldOutput = self.textInput.get("1.0", 'end-1c')

        if pwFieldOutput != "" and len(pwFieldOutput) >= 12:
            if not os.path.isfile(fileName):
                with open(fileName, "x") as file:
                    file.write(self.encodePW(pwFieldOutput, pwFieldOutput))
                self.switchWindows()

            elif os.path.isfile(fileName):
                with open(fileName, "r") as file:
                    readIn = file.read()
                output = self.decodePW(readIn, pwFieldOutput)

                if output[0] == pwFieldOutput and output[1] == True:
                    self.switchWindows()

                else:
                    self.labelError.config(
                        text="!!!False Password!!!", foreground="red")
                    self.textInput.config(state=NORMAL)

        else:
            self.labelError.config(
                text="!!!Your Password is not long enough\nor it is emty!!!", foreground="red")
            self.textInput.config(state=NORMAL)

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
