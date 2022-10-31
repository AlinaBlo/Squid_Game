###############################################################
# Imports
###############################################################
import tkinter
from tkinter import *
import GUI_MAIN
import mongoDB as DB
import re

# The games:
def Main_Gui_Window(window):

    for widgets in window.winfo_children():
        widgets.destroy()

    window.geometry("1090x600")
    window.title("Squid Login")
    window.configure(bg="#abc9ff")
    canvas = Canvas(window, bg="#abc9ff", height=600, width=1090, bd=0, highlightthickness=0, relief="ridge")
    canvas.place(x=0, y=0)

    # center the window on display
    # Login_window_Wight = window.winfo_reqwidth()
    # Login_window_Height = window.winfo_reqheight()
    # positionRight = int(window.winfo_screenwidth() / 2 - Login_window_Wight / 2)
    # PositionDown = int(window.winfo_screenheight() / 2 - Login_window_Height / 2)
    # window.geometry("+{}+{}".format(positionRight, PositionDown))

    # background image
    background_img = PhotoImage(file=f"images/Tkinter_GUI/background.png")
    background = canvas.create_image(580.0, 240.0, image=background_img)

    # Login button
    img0 = PhotoImage(file=f"images/Tkinter_GUI/login.png")
    b0 = Button(image=img0, borderwidth=0, highlightthickness=0, command=lambda:Login_GUI(window), relief="flat")
    b0.place(x=400, y=320, width=273, height=66)

    # Sign up button
    img1 = PhotoImage(file=f"images/Tkinter_GUI/signup.png")
    b1 = Button(image=img1,borderwidth=0, highlightthickness=0, command=lambda:Signup_GUI(window), relief="flat")
    b1.place(x=400, y=420, width=273, height=66)

    window.resizable(False, False)
    window.mainloop()

def Login_GUI(window):

    for widgets in window.winfo_children():
        widgets.destroy()

    window.geometry("1090x600")
    window.configure(bg="#abc9ff")
    canvas = Canvas(window, bg="#abc9ff", height=600, width=1090, bd=0, highlightthickness=0, relief="ridge")
    canvas.place(x=0, y=0)

    background_img = PhotoImage(file=f"images/Tkinter_GUI/bg_login.png")
    background = canvas.create_image(560.0, 320.0, image=background_img)

    img0 = PhotoImage(file=f"images/Tkinter_GUI/redlogin.png")
    b0 = Button(image=img0, borderwidth=0, highlightthickness=0, command=lambda:Login_Validation(window,entry0.get(),entry1.get()), relief="flat")
    b0.place(x=650, y=400, width=274, height=66)

    img1 = PhotoImage(file=f"images/Tkinter_GUI/back.png")
    b0 = Button(image=img1, borderwidth=0, highlightthickness=0, command=lambda:Main_Gui_Window(window), relief="flat")
    b0.place(x=20, y=20, width=160, height=52)

    entry0_img = PhotoImage(file=f"images/Tkinter_GUI/textBox.png")
    entry0_bg = canvas.create_image(660, 220,image=entry0_img)
    entry1_bg = canvas.create_image(660, 320, image=entry0_img)

    entry0 = Entry(bd=0, bg="#FFDEDE",highlightthickness=0, font=('Georgia 18'), fg="#EB4747")
    entry0.place(x=470, y=195, width=375.0, height=47)

    entry1 = Entry(bd=0, show="*", bg="#FFDEDE", highlightthickness=0, font=('Georgia 18'), fg="#EB4747")
    entry1.place(x=470, y=295, width=375.0, height=47)

    window.resizable(False, False)
    window.mainloop()

def Signup_GUI(window):

    for widgets in window.winfo_children():
        widgets.destroy()

    window.geometry("1090x600")
    window.configure(bg = "#abc9ff")
    canvas = Canvas(window,bg = "#abc9ff",height = 600,width = 1090,bd = 0,highlightthickness = 0,relief = "ridge")
    canvas.place(x = 0, y = 0)

    background_img = PhotoImage(file = f"images/Tkinter_GUI/bg_signup.png")
    background = canvas.create_image(560.0, 320.0,image=background_img)

    entry0_img = PhotoImage(file = f"images/Tkinter_GUI/textBox.png")
    entry0_bg = canvas.create_image(690, 172,image = entry0_img)
    entry1_bg = canvas.create_image(690, 255,image = entry0_img)
    entry2_bg = canvas.create_image(690, 338,image = entry0_img)
    entry3_bg = canvas.create_image(690, 421,image = entry0_img)

    entry0 = Entry(bd = 0,bg = "#ffdede",highlightthickness = 0,font=('Georgia 18'), fg="#EB4747")
    entry0.place( x=500, y=145,width = 380.0,height = 47)
    entry1 = Entry(bd = 0,bg = "#ffdede",highlightthickness = 0,font=('Georgia 18'), fg="#EB4747")
    entry1.place(x = 500, y = 228,width = 380.0,height = 47)
    entry2 = Entry(bd = 0,show="*",bg = "#ffdede",highlightthickness = 0,font=('Georgia 18'), fg="#EB4747")
    entry2.place( x = 500, y = 311,width = 380.0,height = 47)
    entry3 = Entry(bd = 0,bg = "#ffdede",highlightthickness = 0,font=('Georgia 18'), fg="#EB4747")
    entry3.place(x = 500, y = 394,width = 380.0,height = 47)

    img0 = PhotoImage(file = f"images/Tkinter_GUI/redSignup.png")
    b0 = Button(image = img0,borderwidth = 0,highlightthickness = 0,command=lambda: Signup_Validation(window,entry0.get(),entry1.get(),entry2.get(),entry3.get()),relief = "flat")

    b0.place(x = 420, y = 500,width = 273,height = 66)

    img1 = PhotoImage(file = f"images/Tkinter_GUI/back.png")
    b1 = Button(image = img1,borderwidth = 0,highlightthickness = 0,command=lambda:Main_Gui_Window(window),relief = "flat")

    b1.place(x=20, y=20, width=160, height=52)

    window.resizable(False, False)
    window.mainloop()

def Signup_Validation(window,username,email,password,age):
    # regular expretion
    print("Signup_Validation:",username,email,password,age)
    validation_RE=check_RE(username,email,age)
    print(validation_RE)
    if validation_RE == 1:
        ans = DB.New_User(username, email, password, age)
        if ans == 1:
            tkinter.messagebox.showinfo("Login error", "username in use")
        elif ans == 2:
            tkinter.messagebox.showinfo("Login error", "email in use")
        elif ans == 0:
            tkinter.messagebox.showinfo("Login success", "New user success")
            Main_Gui_Window(window)

def check_RE(username,email,age):
    regex_username = '^[a-zA-Z0-9.-_ ]{4,16}$'
    if(re.search(regex_username,username)):
        print("Valid username")
    else:
        print("Invalid username")
        tkinter.messagebox.showinfo("Invalid username", "Invalid username please use minimum 4 up to 16 characters")
        return 0

    regex_email = '^[a-zA-Z0-9]+[\._]?[a-zA-Z0-9]+[@]\w+[.]\w{2,3}$'
    if(re.search(regex_email,email)):
        print("Valid Email")
    else:
        tkinter.messagebox.showinfo("Invalid email", "Invalid email please use a valid email format")
        return 0

    regex_age = '^(?:[1-9][0-9]|[1-9])$'
    if (re.search(regex_age, age)):
        print("Valid age")
    else:
        tkinter.messagebox.showinfo("Invalid age", "Invalid age please enter num")
        return 0

    return 1

def Login_Validation(window,username, password):
    print("Login_Validation",username, password)
    S_username,S_password=DB.login_User(username, password)
    print("Login_Validation 2", S_username, S_password)
    if S_username == "" and S_password == "":
        return tkinter.messagebox.showinfo("Login error","The usrename or the password in not right")
    else:
        return GUI_MAIN.games_main_gui(window,S_username)

# game selection GUI
def on_closing():
    if  tkinter.messagebox.askokcancel("Quit", "Do you want to quit?"):
        Login_window.destroy()

Login_window = tkinter.Tk()
Login_window.protocol("WM_DELETE_WINDOW", on_closing)
Main_Gui_Window(Login_window)




