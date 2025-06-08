# ChatFlow client application









import customtkinter
import tkinter
import tkinter.scrolledtext
from tkinter import *
from tkinter import filedialog
from tkinter import messagebox
from PIL import Image, ImageTk

import os
import datetime
import socket
import threading

import sys
import re





customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("dark-blue")


PATH = os.path.dirname(os.path.realpath(__file__))


HOST = '127.0.0.1'
PORT = 1234


client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((HOST, PORT))
APP_NAME = "ChatFlow"




class App(customtkinter.CTk):
    """Main application window."""

    WIDTH = 500
    HEIGHT = 400

    def __init__(self):
        super().__init__()

        self.geometry(f"{App.WIDTH}x{App.HEIGHT}")
        self.title(f"Log in to {APP_NAME}")
        self.minsize(500, 400)
        self.maxsize(500, 400)
        self.protocol("WM_DELETE_WINDOW", self.on_closing)





        self.loginFrame = customtkinter.CTkFrame(master = self)
        self.loginFrame.pack(pady = 20, padx = 60, fill = "both", expand = True)

        self.loginLabel = customtkinter.CTkLabel(master = self.loginFrame, text = "Login System", text_font = ("Roboto", 24))
        self.loginLabel.pack(pady = 12, padx = 10)


        self.username = StringVar()
        self.password = StringVar()



        self.usernameLabel = customtkinter.CTkLabel(master = self.loginFrame, text = "Username:", text_font = ("Roboto", 12))
        self.usernameLabel.pack(pady = (8, 0), padx = 10)

        self.loginEntry = customtkinter.CTkEntry(master = self.loginFrame, textvariable = self.username, width = 200)
        self.loginEntry.pack(pady = 3, padx = 10)


        self.passwordLabel = customtkinter.CTkLabel(master = self.loginFrame, text = "Password:", text_font = ("Roboto", 12))
        self.passwordLabel.pack(pady = (3, 0), padx = 10)

        self.passwordEntry = customtkinter.CTkEntry(master = self.loginFrame, textvariable = self.password, width = 200, show = "*")
        self.passwordEntry.pack(pady = (3, 8), padx = 10)


        self.loginButton = customtkinter.CTkButton(master = self.loginFrame, text = "Login", hover_color = "green", command = self.login)
        self.loginButton.pack(pady = 8, padx = 5)

        self.signupLabel = customtkinter.CTkLabel(master = self.loginFrame, text = "New user? Sign up!", text_font = ("Roboto", 10))
        self.signupLabel.pack(pady = (3, 3), padx = 10)

        self.signupButton = customtkinter.CTkButton(master = self.loginFrame, text = "Sign Up", hover_color = "dark blue", command = self.SignUpPage)
        self.signupButton.pack(pady = (3, 12), padx = 5)




        self.gui_Done = False
        self.running = True





    def on_closing(self, event = 0):
        """Close the main window."""
        self.destroy()




    def login(self):

        """Authenticate user."""
        global auth_mode
        auth_mode = 'Login'

        global usernameInfo
        global passwordInfo

        usernameInfo = self.username.get()
        passwordInfo = self.password.get()

        threading.Thread(target=self.receive).start()



    def receiveFile(self, fileName):
        """Receive file from server."""
        file = open(fileName,'wb')
        l = client.recv(1024)
        while (l):
            file.write(l)
            l = client.recv(1024)
            if l == 'Completed'.encode():
                break
        file.close()



    def sendFile(self, filePath):
        """Send a file to the server."""
        file = open(filePath,'rb')
        l = file.read(1024)
        while (l):
            client.send(l)
            l = file.read(1024)
        client.send('Completed'.encode())
        file.close()
        client.send('{} : Sent a file {}'.format(usernameInfo,fileName).encode())


    def send():
        """Send raw messages to server."""
        while True:
            message = '{} : {}'.format(usernameInfo, input())
            client.send(message.encode())



    def receive(self):
        """Handle incoming messages."""

        global textArea

        while True:
            try:

                message = client.recv(1024).decode()

                if message == 'Login or Reg':
                    client.send(auth_mode.encode())

                elif message == 'USER':
                    client.send(usernameInfo.encode())

                elif message == 'PW':
                    client.send(passwordInfo.encode())

                elif message == 'EMAIL':
                    client.send(emailInfo.encode())

                elif message == 'Authenticated':
                    self.ChatWindow()

                elif message == 'Send File Name':
                    client.send(fileName.encode())

                elif message == 'Send File':
                    self.sendFile(filePath)

                elif message == 'Receive File Name':
                    receiveFileName = client.recv(1024).decode()

                elif message == 'Receive File':
                    self.receiveFile(receiveFileName)

                elif message == 'Authentication Failed':
                    print(message)
                    quit()

                else:
                    print(message)

                    textArea.config(state = 'normal')
                    textArea.insert('end\n', message)

                    textArea.yview('end')
                    textArea.config(state='disabled')



            except Exception as e:
                print(e)
                client.close()
                break




    def SignUpPage(self):
        """Open sign up window."""

        signUpWindow = customtkinter.CTkToplevel(self)
        signUpWindow.title("Sign up to ChatFlow")
        signUpWindow.geometry("500x450")
        signUpWindow.minsize(500, 450)
        signUpWindow.maxsize(500, 450)


        signUpWindow.grab_set()


        global regUser
        global regPass
        global regEmail

        regUser = StringVar()
        regPass = StringVar()
        regEmail = StringVar()



        signUpFrame = customtkinter.CTkFrame(master = signUpWindow)
        signUpFrame.pack(pady = 20, padx = 60, fill = "both", expand = True)

        signUpWindowLabel = customtkinter.CTkLabel(master = signUpFrame, text = "Sign Up to ChatFlow", text_font = ("Roboto", 24))
        signUpWindowLabel.pack(pady = (12, 10), padx = 10)


        signUpUserLabel = customtkinter.CTkLabel(master = signUpFrame, text = "Enter Username:", text_font = ("Roboto", 12))
        signUpUserLabel.pack(pady = (15, 2), padx = 10)

        usernameEntry = customtkinter.CTkEntry(master = signUpFrame, textvariable = regUser, width = 250)
        usernameEntry.pack(pady = (2, 8), padx = 10)


        signUpEmailLabel = customtkinter.CTkLabel(master = signUpFrame, text = "Enter Email:", text_font = ("Roboto", 12))
        signUpEmailLabel.pack(pady = (4, 2), padx = 10)

        emailEntry = customtkinter.CTkEntry(master = signUpFrame, textvariable = regEmail, width = 250)
        emailEntry.pack(pady = (2, 8), padx = 10)


        signUpPassLabel = customtkinter.CTkLabel(master = signUpFrame, text = "Enter Password:", text_font = ("Roboto", 12))
        signUpPassLabel.pack(pady = (4, 2), padx = 10)

        passwordEntry = customtkinter.CTkEntry(master = signUpFrame, textvariable = regPass, width = 250, show = "*")
        passwordEntry.pack(pady = (2, 20), padx = 10)


        confirmButton = customtkinter.CTkButton(master = signUpFrame, height = 35, text = "Sign Up", hover_color = "dark green", command = self.SignUp)
        confirmButton.pack(pady = 6, padx = 5)

        cancelButton = customtkinter.CTkButton(master = signUpFrame, height = 35, text = "Cancel", hover_color = "red", command = signUpWindow.destroy)
        cancelButton.pack(pady = 6, padx = 5)



    def SignUp(self):
        """Register a new user."""

        global auth_mode
        auth_mode = 'Register'

        global usernameInfo
        global passwordInfo
        global emailInfo

        usernameInfo = regUser.get()
        emailInfo = regEmail.get()
        passwordInfo = regPass.get()

        threading.Thread(target = self.receive).start()



    def ChatWindow(self):
        """Open the main chat UI."""
        print("Chat Window Opened")

        mainChat = customtkinter.CTkToplevel(self)
        mainChat.title("ChatFlow")
        mainChat.geometry("800x500")
        mainChat.minsize(600, 500)
        mainChat.maxsize(1000, 600)








        mainChat.grid_columnconfigure(1, weight = 1)
        mainChat.grid_rowconfigure(0, weight = 1)


        frame1 = customtkinter.CTkFrame(master = mainChat,
                                            width = 200,
                                            corner_radius = 0)
        frame1.grid(row = 0, column = 0, sticky = "nswe")


        frame2 = customtkinter.CTkFrame(master = mainChat, corner_radius = 10)
        frame2.grid(row = 0, column = 1, sticky = "nswe", padx = 20, pady = 20)






        frame1.grid_rowconfigure(0, minsize = 10)
        frame1.grid_rowconfigure(3, weight = 1)
        frame1.grid_rowconfigure(5, minsize = 20)
        frame1.grid_rowconfigure(8, minsize = 10)

        label1 = customtkinter.CTkLabel(master = frame1,
                                            text = "ChatFlow",
                                            text_font = ("Impact Regular", -16))
        label1.grid(row = 1, column = 0, padx = 10, pady = 10)




        aboutButton = customtkinter.CTkButton(master = frame1,
                                                    text = "ABOUT",
                                                    text_color = "white",
                                                    width = 100,
                                                    height = 30,
                                                    corner_radius = 15,
                                                    hover_color = "green",
                                                    fg_color = "dark blue",
                                                    command = self.ShowAbout)
        aboutButton.grid(row = 2, column = 0, padx = 5, pady = 20)




        exitButton = customtkinter.CTkButton(master = frame1,
                                                    text = "Logout and Exit",
                                                    text_color = "white",
                                                    width = 100,
                                                    height = 50,
                                                    corner_radius = 15,
                                                    hover_color = "dark red",
                                                    fg_color = "red",
                                                    command = self.exitMain)
        exitButton.grid(row = 5, column = 0, padx = 5, pady = 20)




        modeLabel = customtkinter.CTkLabel(master = frame1,
                                                text = "Appearance Mode:",
                                                text_font = ("Franklin Gothic", -14))
        modeLabel.grid(row = 6, column = 0, sticky = "w", padx = 20, pady = 0)

        menu1 = customtkinter.CTkOptionMenu(master = frame1,
                                                width = 100,
                                                height = 30,
                                                text_color = "white",
                                                dropdown_hover_color = "gray",
                                                button_hover_color = "dark blue",
                                                values = ["Dark", "Light", "System Default"],
                                                command = self.ChangeAppearance)
        menu1.grid(row = 7, column = 0, sticky = "s", padx = 20, pady = 10)







        frame2.rowconfigure((0, 1, 2, 3, 4), weight = 1)
        frame2.rowconfigure(6, weight = 1)
        frame2.columnconfigure((0, 1, 2, 3, 4), weight = 1)
        frame2.columnconfigure(6, minsize = 10)


        global textArea

        textArea = tkinter.scrolledtext.ScrolledText(mainChat, height = 20)
        textArea.grid(row = 0, column = 1, columnspan = 3, rowspan = 1,
                                padx = 20, pady = (20, 0), sticky = "new")
        textArea.config(state = 'disabled')



        global signal
        signal = StringVar()

        global entry1

        entry1 = customtkinter.CTkEntry(master = frame2,
                                            textvariable = signal,
                                            width = 120,
                                            placeholder_text = "Say Something...",
                                            placeholder_text_color = "gray")
        entry1.grid(row = 5, column = 0, columnspan = 3, padx = 20, pady = (20, 0), sticky = "we")



        sendButton = customtkinter.CTkButton(master = frame2,
                                                    width = 20,
                                                    height = 30,
                                                    text = "SEND",
                                                    hover_color = "red",
                                                    text_color = "white",
                                                    command = self.SendMessage)
        sendButton.grid(row = 5, column = 3, padx = 10, pady = (20, 0), sticky = "we")




        attachButton = customtkinter.CTkButton(master = frame2,
                                                    width = 20,
                                                    height = 30,
                                                    text = "ATTACH",
                                                    hover_color = "red",
                                                    text_color = "white",
                                                    command = self.AttachFile)
        attachButton.grid(row = 5, column = 4, padx = 10, pady = (20, 0), sticky = "we")











    def ShowAbout(self):
        """Display about window."""

        aboutWindow = customtkinter.CTkToplevel(self)
        aboutWindow.title("ABOUT")
        aboutWindow.geometry("400x200")
        aboutWindow.minsize(400, 200)
        aboutWindow.maxsize(400, 200)

        aboutLabel1 = customtkinter.CTkLabel(master = aboutWindow, text = "ChatFlow is a LAN based chat app built purely using Python!")
        aboutLabel1.grid(row = 0, column = 0, padx = (10, 0), pady = 10)


        aboutWindow.grab_set()












    def exitMain(self):
        """Log out and close the application."""




        exitConfirm = customtkinter.CTkToplevel(self)
        exitConfirm.title("Logout and Exit")
        exitConfirm.geometry("420x130")
        exitConfirm.minsize(420, 130)
        exitConfirm.maxsize(420, 130)


        exitConfirm.grab_set()


        exitFrame = customtkinter.CTkFrame(master = exitConfirm,
                                            width = 370,
                                            corner_radius = 5)
        exitFrame.pack(padx = 0, pady = 10)


        exitLabel = customtkinter.CTkLabel(master = exitFrame,
                                            text = "Are you sure you want to logout and exit?",
                                            text_font = ("Impact Regular", 14))
        exitLabel.grid(row = 0, column = 0, columnspan = 3, padx = 10, pady = 10)



        confirmButton = customtkinter.CTkButton(master = exitFrame,
                                                text = "Exit",
                                                text_color = "white",
                                                width = 110,
                                                height = 50,
                                                corner_radius = 15,
                                                hover_color = "red",
                                                command = self.destroy)
        confirmButton.grid(row = 1, column = 0, padx = (40, 0), pady = 10)



        cancelButton = customtkinter.CTkButton(master = exitFrame,
                                                text = "Cancel",
                                                text_color = "white",
                                                width = 110,
                                                height = 50,
                                                corner_radius = 15,
                                                hover_color = "green",
                                                command = exitConfirm.destroy)
        cancelButton.grid(row = 1, column = 1, padx = 0, pady = 10)







    def ChangeAppearance(self, newAppearance):
        """Switch between dark and light themes."""

        if newAppearance == "Light":
            customtkinter.set_appearance_mode("light")

        elif newAppearance == "System Default":
            customtkinter.set_appearance_mode("system")

        else:
            customtkinter.set_appearance_mode("dark")





    def SendMessage(self):
        """Send a chat message."""

        global textmess
        textmess = signal.get()

        msg = f"{usernameInfo}: {textmess}"
        client.send(msg.encode('ascii'))




    def AttachFile(self):
        """Select a file to send."""
        global fileName
        global filePath
        root = tkinter.Tk()
        root.withdraw()
        filePath = filedialog.askopenfilename()
        fileName = os.path.basename(filePath)
        client.send('File Transfer'.encode())






if __name__ == "__main__":
    app = App()
    app.mainloop()

