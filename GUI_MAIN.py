###############################################################
# Imports
###############################################################
from tkinter import *
from tkinter import ttk, messagebox
import configFiles as CF
import mongoDB as DB
from datetime import datetime
import tkinter.font as tkFont
import Games

###1###
# red light green light game
def ChooseGame1time(window,username):

    for widgets in window.winfo_children():
        widgets.destroy()

    window.geometry("1090x600")
    window.title("red light green light game")
    window.configure(bg="#abc9ff")
    canvas = Canvas(window, bg="#abc9ff", height=600, width=1090, bd=0, highlightthickness=0, relief="ridge")
    canvas.place(x=0, y=0)

    background_img = PhotoImage(file=f"images/Tkinter_GUI/game1.png")
    background = canvas.create_image(560.0, 320.0, image=background_img)

    window.title('set game time')


    menu = StringVar()
    menu.set("90")
    options = ["60", "90", "120", "150"]
    drop = OptionMenu(window,menu,*options)
    helv30 = tkFont.Font(family='Helvetica', size=20)
    drop.config(font=helv30,bg='#ff8b8b',fg='#FFDEDE')
    drop["menu"].config(font=helv30, bg='#ff8b8b', fg='#FFDEDE')
    drop.place(x=500, y=250,width = 100,height =60)

    lets = PhotoImage(file=f"images/Tkinter_GUI/lets.png")
    let = Button(image=lets, borderwidth=0, highlightthickness=0, command=lambda:Red_Light_Green_Light(window,int(menu.get()),username), relief="flat")
    let.place(x=380, y=400,width = 350,height = 65)

    back = PhotoImage(file=f"images/Tkinter_GUI/back.png")
    backa = Button(image=back, borderwidth=0, highlightthickness=0, command=lambda:games_main_gui(window,username), relief="flat")
    backa.place(x=20, y=20, width=100, height=52)
    window.mainloop()

def Red_Light_Green_Light(window,game1_time,username):
    score=Games.game.Start_The_Game(0, 1, game1_time, True, 0)
    Games.game.reset()
    #score=Red_Light_Green_Light_Game.game.STG(game1_time)
    #Red_Light_Green_Light_Game.game.reset()
    now = datetime.now()
    score="Red Light Green Light Game SCORE: " + str(score) + str(now.strftime(" %d/%m/%Y %H:%M:%S"))
    DB.Add_Score(username,score)
    games_main_gui(window,username)

###2###
#cookie game
def Cookies_Catch(window,username):
    for widgets in window.winfo_children():
        widgets.destroy()

    window.geometry("1090x600")
    window.configure(bg="#abc9ff")
    canvas = Canvas(window, bg="#abc9ff", height=600, width=1090, bd=0, highlightthickness=0, relief="ridge")
    canvas.place(x=0, y=0)

    background_img = PhotoImage(file=f"images/Tkinter_GUI/game2.png")
    background = canvas.create_image(560.0, 320.0, image=background_img)

    window.title('cookies catch settings')
    dframe = Frame(window, bd=10)
    dframe.grid(row=3, column=2)
    Checkbutton1 = IntVar()
    Checkbutton2 = IntVar()
    Checkbutton3 = IntVar()
    Checkbutton4 = IntVar()
    Checkbutton5 = IntVar()

    Button1 = Checkbutton(window, variable=Checkbutton1,onvalue=1,offvalue=0,height=0,width=0,bg='#ff8b8b')
    Button2 = Checkbutton(window, variable=Checkbutton2,onvalue=1,offvalue=0,height=0,width=0,bg='#ff8b8b')
    Button3 = Checkbutton(window, variable=Checkbutton3,onvalue=1,offvalue=0,height=0,width=0,bg='#ff8b8b')
    Button4 = Checkbutton(window, variable=Checkbutton4,onvalue=1,offvalue=0,height=0,width=0,bg='#ff8b8b')
    Button5 = Checkbutton(window,  variable=Checkbutton5, onvalue=1, offvalue=0, height=0, width=0,bg='#ff8b8b')

    Button1.place(x=776, y=340)
    Button2.place(x=985, y=340)
    Button3.place(x=843, y=560)
    Button4.place(x=921, y=560)
    Button5.place(x=887, y=124)

    menu = StringVar()
    menu.set("90")
    options = ["60", "90", "120", "150"]
    drop = OptionMenu(window, menu, *options)
    helv30 = tkFont.Font(family='Helvetica', size=20)
    drop.config(font=helv30, bg='#ff8b8b', fg='#FFDEDE')
    drop["menu"].config(font=helv30, bg='#ff8b8b', fg='#FFDEDE')
    drop.place(x=300, y=380, width=100, height=60)

    lets = PhotoImage(file=f"images/Tkinter_GUI/lets.png")
    let = Button(image=lets, borderwidth=0, highlightthickness=0, command=lambda:Cookies_Catch_Game(window,Checkbutton1.get(),Checkbutton2.get(),Checkbutton3.get(),Checkbutton4.get(),Checkbutton5.get(),int(menu.get()),username), relief="flat")
    let.place(x=200, y=480,width = 350,height = 65)

    back = PhotoImage(file=f"images/Tkinter_GUI/back.png")
    backa = Button(image=back, borderwidth=0, highlightthickness=0, command=lambda:games_main_gui(window,username), relief="flat")
    backa.place(x=20, y=20, width=100, height=52)
    window.mainloop()

#cookie game with choices
def Cookies_Catch_Game(window,lh,rh,ll,rl,h,game2_time,username):
    choosed_body_array=[lh,rh,ll,rl,h] # [0,1,0,1,0]
    if choosed_body_array==[0,0,0,0,0]:
        messagebox.showinfo("pick error", "you didn't pick any body part to play with!")
        games_main_gui(window, username)
    else:
        regular_body=[CF.left_hand,CF.right_hand,CF.left_leg,CF.right_leg,CF.head]
        body_parts_playing=[]

        for count, item in enumerate(choosed_body_array):
            if choosed_body_array[count] == 1:
                body_parts_playing.append((regular_body[count].tolist()))
        print(body_parts_playing)
        score=Games.game.Start_The_Game(body_parts_playing, 2, game2_time, True, 0)
        Games.game.reset()
        #score=Cookie_Game.game.Start_The_Game(body_parts_playing,game2_time)
        #Cookie_Game.game.reset()
        now = datetime.now()
        score="Cookies Catch Game SCORE: " + str(score) + str(now.strftime(" %d/%m/%Y %H:%M:%S"))
        DB.Add_Score(username, score)
        games_main_gui(window,username)

###3###
# Cookies Catch Physiotherapy Mode
def Cookies_Catch_Physiotherapy_Mode(window,Game_List,username):
    score=Games.game.Start_The_Game(0, 3, 0, True, Game_List)
    Games.game.reset()
    #game = Cookie_Game_mode_Physiotherapy.physiotherapy_game(Game_List)
    print(Game_List)
    #game.Start_The_Game()
    #game.reset([])
    now = datetime.now()
    score="Cookies Catch Physiotherapy Mode : " + str(now.strftime(" %d/%m/%Y %H:%M:%S"))
    DB.Add_Score(username,score)
    games_main_gui(window,username)

def Cookies_Catch_Choose_Settings(window,username):
    for widgets in window.winfo_children():
        widgets.destroy()

    window.geometry("1090x600")
    window.configure(bg="#abc9ff")
    canvas = Canvas(window, bg="#abc9ff", height=600, width=1090, bd=0, highlightthickness=0, relief="ridge")
    canvas.place(x=0, y=0)

    background_img = PhotoImage(file=f"images/Tkinter_GUI/game3.png")
    background = canvas.create_image(560.0, 320.0, image=background_img)

    options = []
    newList=[]
    exe_list=[[1,['16,18,20,22'],'left hand 90 degree'],[2,['15,17,19,21'],'right hand 90 degree'],[3,['16,18,20,22'],'left hand 180 degree'],[4,['15,17,19,21'],'right hand 180 degree']]

    menu = StringVar()
    for count, item in enumerate(exe_list):
        options.append(item[2])
    menu.set(options[1])

    dropCombo = ttk.Combobox(window,value=options,height=5, width=20,font=('Century 16'))
    dropCombo.place(x=780,y=85)

    Reputation = Entry(window,text="",font=('Century 16'))
    Reputation.place(x=440,y=157,height=30,width=50)

    Listboxs=Listbox(window,height=15, width=60)
    Listboxs.place(x=550,y=300)

    img0 = PhotoImage(file=f"images/Tkinter_GUI/list.png")
    img1 = PhotoImage(file=f"images/Tkinter_GUI/lets.png")
    insert = Button(image=img0, borderwidth=0, highlightthickness=0, command=lambda:Add_To_Exercise(dropCombo.current(),Reputation.get(),0,newList,Listboxs), relief="flat")
    start = Button(image=img1, borderwidth=0, highlightthickness=0, command=lambda:Cookies_Catch_Physiotherapy_Mode(window,newList,username), relief="flat")
    insert.place(x=700, y=150, width=250, height=52)
    start.place(x=150, y=500, width=350, height=52)

    back = PhotoImage(file=f"images/Tkinter_GUI/back.png")
    backa = Button(image=back, borderwidth=0, highlightthickness=0, command=lambda:games_main_gui(window,username), relief="flat")
    backa.place(x=20, y=20, width=100, height=52)
    window.mainloop()

def Add_To_Exercise(exercise,Reputation,cb_new_exercise,newList,Listbox):
    exe_list=[[1,['16,18,20,22'],'left hand 90 degree'],[2,['15,17,19,21'],'right hand 90 degree'],[3,['16,18,20,22'],'left hand 180 degree'],[4,['15,17,19,21'],'right hand 180 degree']]
    new_exercise = exe_list[exercise]
    new_exercise.insert(1, int(Reputation))
    newList.append(new_exercise)
    tmp=[]
    for i in range(len(newList)):
        t = str(newList[i][3]) +" "+ str(newList[i][1]) + " Times"
        tmp.append(t)
    Listbox.insert(int(len(newList)), t)

#score
def show_score(username,Score):
    DB.Add_Score(username,Score)

def Show_My_Games(window, username):
    for widgets in window.winfo_children():
        widgets.destroy()

    window.geometry("1090x600")
    window.configure(bg="#abc9ff")
    canvas = Canvas(window, bg="#abc9ff", height=600, width=1090, bd=0, highlightthickness=0, relief="ridge")
    canvas.place(x=0, y=0)

    Listboxs=Listbox(window,height=20, width=100)
    Listboxs.place(x=200,y=100)

    my_Games=DB.Get_Score(username)
    for i in range(len(my_Games)):
        Listboxs.insert(i, my_Games[i])

    back = PhotoImage(file=f"images/Tkinter_GUI/back.png")
    backa = Button(image=back, borderwidth=0, highlightthickness=0, command=lambda:games_main_gui(window,username), relief="flat")
    backa.place(x=20, y=20, width=100, height=52)
    window.mainloop()

def games_main_gui(window,username):

    for widgets in window.winfo_children():
        widgets.destroy()

    window.geometry("1090x600")
    window.configure(bg="#abc9ff")
    canvas = Canvas(window, bg="#abc9ff", height=600, width=1090, bd=0, highlightthickness=0, relief="ridge")
    canvas.place(x=0, y=0)

    background_img = PhotoImage(file=f"images/Tkinter_GUI/GUI_MAIN_BG.png")
    background = canvas.create_image(560.0, 320.0, image=background_img)

    window.title('Game')
    dframe = Frame(window, bd=10)
    dframe.grid(row=3, column=2)
    img0 = PhotoImage(file=f"images/Tkinter_GUI/RLGL.png")
    b0 = Button(image=img0, borderwidth=0, highlightthickness=0, command=lambda:ChooseGame1time(window,username), relief="flat")
    b0.place(x=270, y=150, width=540, height=66)

    img1 = PhotoImage(file=f"images/Tkinter_GUI/cookieG.png")
    b1 = Button(image=img1, borderwidth=0, highlightthickness=0, command=lambda:Cookies_Catch(window,username), relief="flat")
    b1.place(x=270, y=250, width=540, height=66)

    img2 = PhotoImage(file=f"images/Tkinter_GUI/Pyh.png")
    b2 = Button(image=img2, borderwidth=0, highlightthickness=0, command=lambda:Cookies_Catch_Choose_Settings(window,username), relief="flat")
    b2.place(x=270, y=350, width=540, height=66)

    img3 = PhotoImage(file=f"images/Tkinter_GUI/scores.png")
    b3 = Button(image=img3, borderwidth=0, highlightthickness=0, command=lambda:Show_My_Games(window, username), relief="flat")
    b3.place(x=270, y=450, width=540, height=66)

    window.mainloop()
