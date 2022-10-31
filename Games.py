from camera import Camera
import configFiles as CF
import cv2
import random
import time
import pygame
from pygame import mixer
mixer.init()

from tkinter import messagebox
import numpy as np
import tkinter

import math
import statistics

import physiotherapy_moves as PMO

class game():
    def __init__(self):
        self.reset()

    def reset(self):
        # Camera Frame
        self.wCam = CF.WidthCam
        self.hCam = CF.HeightCam
        self.cap = cv2.VideoCapture(CF.defaultCamera)

        # Landmarks data
        self.Frame_Array = []
        self.landmarks = []
        self.img = []

        # Game Run
        self.Game_is_running=True
        self.end_game=False

        # game time
        self.game_time = game_time()

    def Start_The_Game(self,body_part,game_name,seconds,full_screen,exercise_list):

        pre_game_setup(game,seconds)

        # game components
        doll = Doll()
        coins = Coins()
        exercise = Exercise(exercise_list)

        if game_name==1:
            self.Red_Light_Green_Light_Game(seconds,full_screen,exercise_list,doll)
        elif game_name==2:
            self.Cookie_Game(body_part,seconds,full_screen,coins)
        elif game_name==3:
            self.Cookie_Game_Physiotherapy_Mode(body_part,seconds,full_screen,coins,exercise)

        stop_and_exit_game(self)

        return doll.points


    def Red_Light_Green_Light_Game(self,seconds,full_screen,exercise_list,doll):
        while self.Game_is_running:

            update_Game_Camera_Data(self)

            in_game = check_if_player_is_detected(game)

            RLGL_UI(self.img)

            # Game Starts after 5 seconds
            if 1 > ((self.game_time.pre_game - time.time()) + 1) and (time.time() < self.game_time.pre_game):
                self.sound = mixer.Sound('sounds/Coin.wav')
                self.sound.play()

            if 0.5 < (self.game_time.total_Game_Time - time.time()) < 3:
                cv2.putText(self.img, f'{int(self.game_time.total_Game_Time - time.time()) + 1}', (640, 360),
                            cv2.FONT_HERSHEY_SIMPLEX, 5, (0, 50, 255), 6)

            if time.time() > self.game_time.pre_game:
                self.end_game = red_light_green_light(game, doll, in_game)
                if self.end_game == False:
                    doll.sound.stop()
                    game_over(self.img, doll.points)
                    game_over_win_lose(self.img, doll)
            else:
                pre_game_countdown(self)

            check_if_game_time_ended(self, doll)

            show_game(self, full_screen)

            key = cv2.waitKey(1)
            if key == 27:
                self.Game_is_running = False
                # mixer.music.stop()
                doll.sound.stop()
                break

    def Cookie_Game(self,body_part,seconds,full_screen,coins):
        background_music(self)
        while self.Game_is_running:

            update_Game_Camera_Data(self)

            in_game = check_if_player_is_detected(game)

            if time.time() > self.game_time.pre_game:
                self.img = cookie_game(self, body_part, seconds, coins)
                cv2.rectangle(self.img, (2, 2), (350, 40), (222, 224, 222), -1)
                cv2.rectangle(self.img, (1000, 2), (1350, 40), (222, 224, 222), -1)
                cv2.putText(self.img, f'coins collected:{coins.coins_collected}', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1,
                            (61, 89, 171), 3)
                cv2.putText(self.img, f'Time Left:{int(self.game_time.total_Game_Time - time.time())}', (1030, 30),
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (75, 0, 130), 3)
            else:
                pre_game_countdown(self)

            if self.game_time.total_Game_Time - time.time() <= 0:
                game_over(self.img, coins.coins_collected)

            show_game(self, full_screen)

            key = cv2.waitKey(1)
            if key == 27:
                self.Game_is_running = False
                break

    def Cookie_Game_Physiotherapy_Mode(self,body_part,seconds,full_screen,coins,exercise):
        background_music(self)
        while self.Game_is_running:

            update_Game_Camera_Data(self)

            in_game = check_if_player_is_detected(game)

            if time.time() > self.game_time.pre_game:
                ListCheck(self, exercise)
                if self.Game_is_running:
                    Check_Position(self, exercise, coins, ListCheck(self, exercise))
                    cv2.rectangle(self.img, (0, 0), (600, 80), (222, 224, 222), -1)
                    cv2.putText(self.img, f'move: {exercise.List[0][3]} ', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1,
                                (232, 51, 51), 2)
                    cv2.putText(self.img, f'repeat: {exercise.List[0][1]} times', (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 1,
                                (54, 124, 54), 1)
            else:
                pre_game_countdown(game)

            show_game(self, full_screen)

            key = cv2.waitKey(1)
            if key == 27:
                self.Game_is_running = False
                break

def show_game(game,full_screen):
    if full_screen:
        cv2.namedWindow("Game", cv2.WND_PROP_FULLSCREEN)
        cv2.setWindowProperty("Game", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
    cv2.imshow("Game", game.img)
    cv2.waitKey(1)


class game_time():
    def __init__(self):
        self.reset()

    def reset(self):
        self.total_Game_Time = 0
        self.pre_game = 0
        self.pause_Counter = 0

# Third game functions:
class Exercise():
    def __init__(self,Game_List):
        self.reset(Game_List)

    def reset(self,Game_List):
        self.List = Game_List
        self.one_second = 0

def ListCheck(game,exercise):
    if game.Game_is_running:
        # pop the move when is done
        if exercise.List[0][1] == 0:
            exercise.List.pop(0)

        # checks if the list is done
        if len(exercise.List) == 0:
            print("The exercise is over")
            game.Game_is_running = False
            exercise_done(game.img)

        if game.Game_is_running:
            # beta testing the game mechanics
            if Exercise_pose_from_list(exercise) == 1:
                return PMO.Ninety_Degrees_left(game.Frame_Array[-1], 1)
            elif Exercise_pose_from_list(exercise) == 2:
                return PMO.Ninety_Degrees_right(game.Frame_Array[-1])
            elif Exercise_pose_from_list(exercise) == 3:
                return PMO.one_hundred_eighty_Degrees_left(game.Frame_Array[-1])
            elif Exercise_pose_from_list(exercise) == 4:
                return PMO.one_hundred_eighty_Degrees_Right(game.Frame_Array[-1])

def exercise_done(img):
    cv2.rectangle(img, (340, 200), (900, 550), (222, 224, 222), -1)
    cv2.putText(img, " The exercise is done", (350, 300), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (232, 51, 51), 3)
    cv2.putText(img, "excellent job!", (370, 400), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (232, 51, 51), 2)

def Exercise_pose_from_list(exercise):
        return exercise.List[0][0]

def Check_Position(game,exercise,coins,test_movment):#,coinsList,pre_game,test_movment,Frame_Array):
    # generate new coin
    if len(coins.coinsList) == 0 and exercise.one_second < time.time():
        add_cookie(coins, test_movment[1])

    # show the coins
    for i in range(len(coins.coinsList)):
        game.img = random_cookie_placement(game.img, i, coins.coinsList)

    # checks coin life
    tmp = []
    for i in range(len(coins.coinsList)):
        if coins.coinsList[i].life > time.time():
            touch = coin_collishion_pose(game.img, coins.coinsList[i], game.Frame_Array[-1],exercise.List[0][2])
            if touch == True and test_movment[0] == 0:
                coins.coinsList[i].life = time.time()
                coins.coins_collected = coins.coins_collected + coins.coinsList[i].coin
                exercise.List[0][1] = exercise.List[0][1] - 1
                exercise.one_second = 1 + time.time()
                tmp.append(coins.coinsList[i])
        else:
            exercise.one_second = 1 + time.time()
            tmp.append(coins.coinsList[i])

    for i in range(len(tmp)):
        coins.coinsList.pop(coins.coinsList.index((tmp[i])))

def get_coordinate(game,coin_radius,test_movment):
    if test_movment == 1 or test_movment == 3:
        center_coordinates = (random.randint(coin_radius, (int(game.wCam / 2)) - coin_radius),
                              random.randint(coin_radius, int((game.hCam / 2)) - coin_radius))
        return center_coordinates  # 0,0->640,360
    elif test_movment == 2 or test_movment == 4:
        center_coordinates = (random.randint(coin_radius + (game.wCam / 2), game.wCam - coin_radius),
                              random.randint(coin_radius, (game.hCam / 2) - coin_radius))
        return center_coordinates  # 360,640->1280,360
    else:
        return (random.randint(coin_radius, CF.WidthCam - coin_radius), random.randint(coin_radius, CF.HeightCam - coin_radius))

# Second game functions :
class Coins():
    def __init__(self):
        self.reset()

    def reset(self):
        self.coins_collected = 0
        self.difficulty = 0
        self.coinsList = []

class Cookie():
    def __init__(self, center_coordinates, radius, color, thickness, life, cookie, coin):
        self.coordinates = center_coordinates
        self.radius = radius
        self.color = color
        self.thickness = thickness
        self.life = life
        self.cookie = cookie
        self.coin = coin



def background_music(game):
    if game.Game_is_running:
        pygame.init()
        pygame.mixer.music.load('sounds/background.wav')
        pygame.mixer.music.play(-1)

def cookie_game(game,body_part,seconds,coins):

    # generate new coin
    if len(coins.coinsList) < (coins.difficulty + 1) or len(coins.coinsList) == 0:
        add_cookie(coins,0)

    # add selection for hands
    #self.master_point(img, self.Frame_Array[-1], [16, 18, 20, 22])

    # checks coin life
    return checks_coin_life(game,coins,body_part,seconds)

def add_cookie(coins,test_movment):
    new_cookie=False
    coin_radius=get_cookie_radius(0.005)

    while new_cookie == False:
        center_coordinates = get_coordinate(game, coin_radius, test_movment)
        cookie_type = random.randint(0, 3)
        cookie_coin = 1

        # GOLDEN COOKIE
        if random.randint(0, 100) > 95:
            cookie_type = 4
            cookie_coin = 5

        if check_coins_collision(center_coordinates, coins.coinsList):
            if coins.difficulty == 0:
                coins.coinsList.append(
                    Cookie(center_coordinates, coin_radius, (25, 100, 100), -1, 7 + time.time(), cookie_type,
                          cookie_coin))
            if coins.difficulty == 1:
                coins.coinsList.append(
                    Cookie(center_coordinates, coin_radius - 10, (25, 100, 220), -1, 5 + time.time(), cookie_type,
                          cookie_coin))
            if coins.difficulty == 2:
                coins.coinsList.append(
                    Cookie(center_coordinates, coin_radius - 20, (25, 100, 225), -1, 3 + time.time(), cookie_type,
                          cookie_coin))
            new_cookie = True

def get_cookie_radius(num):
    serf = CF.WidthCam * CF.HeightCam * num
    return int(math.sqrt(serf / math.pi))

def check_coins_collision(center_coordinates,coinsList):
    for i in range(len(coinsList)):
        area=check_circle(coinsList[i].coordinates[0],center_coordinates[0],coinsList[i].coordinates[1],center_coordinates[1])
        if area < ((coinsList[i].radius)**2):
            return False
    return True

def check_circle(x,a,y,b):
    return (x-a)**2+(y-b)**2

def checks_coin_life(game,coins,body_part,seconds):
    tmp = []
    for i in range(len(coins.coinsList)):
        if coins.coinsList[i].life > time.time():
            touch = coin_collishion_pose(game.img, coins.coinsList[i], game.Frame_Array[-1], body_part)
            if touch == True:
                coins.coinsList[i].life = time.time()
                coins.coins_collected = coins.coins_collected + coins.coinsList[i].coin
                tmp.append(coins.coinsList[i])
                coin_sound = mixer.Sound('sounds/Coin.wav')
                coin_sound.play()
        else:
            tmp.append(coins.coinsList[i])

    for i in range(len(coins.coinsList)):
        game.img = random_cookie_placement(game.img, i, coins.coinsList)

    for i in range(len(tmp)):
        coins.coinsList.pop(coins.coinsList.index((tmp[i])))

    change_difficulty(coins,game.game_time.pre_game, seconds)

    return game.img

def coin_collishion_pose(img,coin,pose_coordinates,body_part):
    touch = False

    for j in range(len(body_part)):
        body_parts = cast_to_list(body_part[j])
        radius_circle_x, radius_circle_y = get_body_coordinates(body_parts, pose_coordinates)
        radius_circle = 80

        # Debugging
        # show the part collecting
        #cv2.circle(img, (int(radius_circle_x), int(radius_circle_y)), radius_circle, (20, 9, 229), cv2.FILLED)

        area = check_circle(radius_circle_x, coin.coordinates[0], radius_circle_y, coin.coordinates[1])
        if statistics.sqrt(area) <= (coin.radius + radius_circle):
            touch = True

    return touch

def get_body_coordinates(body_parts, pose_coordinates):
    body_part_pose_coordinates = []
    tmpX = []
    tmpY = []

    for i in body_parts:
        body_part_pose_coordinates.append(pose_coordinates[i])

    for i in range(len(body_part_pose_coordinates)):
        tmpX.append(body_part_pose_coordinates[i][1])
        tmpY.append(body_part_pose_coordinates[i][2])

    return statistics.median(tmpX),statistics.median(tmpY)

def random_cookie_placement(img, i, coinsList):

    cirC = pick_cookie(coinsList[i].cookie)
    tmp = coinsList[i].radius * 2

    x = coinsList[i].coordinates[0]
    x = x - coinsList[i].radius
    y = coinsList[i].coordinates[1]
    y = y - coinsList[i].radius

    img=PhotoTrans(img, cirC,tmp, 0, [x, y])
    return img

def pick_cookie(num):
    cookies=['images\cirS.png','images\elaS.png','images\starS.png','images\mshuS.png','images\StarB.png']
    return cookies[num]

def change_difficulty(coins,pre_game,seconds):
    if coins.coins_collected > 50 or (pre_game + (seconds * 0.333)) < time.time():
        coins.difficulty = 1
    if coins.coins_collected > 100 or (pre_game + (seconds * 0.666)) < time.time():
        coins.difficulty = 2


# First game function :
class Doll():
    def __init__(self):
        self.reset()

    def reset(self):
        self.timer=0
        self.turn=True
        self.FREEZE=[]
        self.win = 0

        self.sound = mixer.Sound('sounds/Coin.wav')

        # points
        self.points = 0
        self.negetive_points = 0
        self.health_Bar_points = 279

        # player movement
        self.no_movement = 0

    # check if the doll need to turn
    def turn_doll(self,Frame_Array):
        self.timer = random.randint(5, 15) + time.time()
        if self.turn == False:
            self.turn=True
        else:
            self.turn=False
            self.timer = random.randint(5, 15) + time.time()
        self.FREEZE=Frame_Array
        return self.turn, self.timer,self.FREEZE

    # is the doll looking at the player?
    def not_looking(self,img,Frame_Array,points,in_game):
        cv2.putText(img, f'MOVE:{int(self.timer - time.time())}', (74, 335), cv2.FONT_HERSHEY_SIMPLEX, 1,(113, 186, 101), 2)
        if in_game:
            current_points = points_Counter(camera.Find_Velocity_Diff(Frame_Array[0],Frame_Array[-1]))
            points_update(self,game,current_points)
        game_music(self)
        Points_Collected(points, img)
        Health_Bar(False, self.health_Bar_points, img)
        return True
    def looking(self,img,Frame_Array,points,negetive_points,in_game):
        cv2.putText(img, f'DONT MOVE:{int(self.timer - time.time())}', (40, 335), cv2.FONT_HERSHEY_SIMPLEX, 1,(36, 62, 145), 2)
        if in_game:
            self.negetive_points = Player_Movment_Detection(self.FREEZE, Frame_Array[-1])
            if self.negetive_points > 0:
                self.FREEZE = Frame_Array[-1]
            if self.health_Bar_points > 25 and self.negetive_points != 0:
                self.health_Bar_points = self.health_Bar_points - self.negetive_points
            if self.health_Bar_points <= 25:
                return False
        move_music(self)
        Points_Collected(points, img)
        Health_Bar(True, self.health_Bar_points, img)
        return True

def RLGL_UI(img):
    cv2.rectangle(img, (20, 18), (285, 710), (222, 224, 222), -1)
    cv2.putText(img, f'Health Bar:', (25, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)
    cv2.putText(img, f'Points collected:', (25, 130), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)
    cv2.putText(img, f'Time left:', (25, 215), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)

def red_light_green_light(game,doll,in_game):
    cv2.putText(game.img, f'{int(game.game_time.total_Game_Time - time.time())}', (25, 255), cv2.FONT_HERSHEY_SIMPLEX, 1,
                (0, 0, 0), 2)
    if doll.timer < time.time():
        doll.turn, doll.timer, doll.FREEZE = doll.turn_doll(game.Frame_Array[-1])

    if doll.turn == False:  # player is allowed to move
        game.img = PhotoTrans(game.img, 'images\ot-looking.png',0, 0.4, [50, 450])
        return doll.not_looking(game.img, game.Frame_Array, doll.points, in_game)
    else:  # player is not allowed to move
        game.img = PhotoTrans(game.img, 'images\looking.png',0, 0.4, [50, 450])
        return doll.looking(game.img, game.Frame_Array, doll.points, doll.negetive_points, in_game)

def points_Counter(VelocityArray):
    addpoints = 0
    body_part=[CF.head,CF.left_hand,CF.right_hand,CF.left_arm, CF.right_arm]
    # Head 0-10
    for i in range(len(body_part)):
        Move, Stat = check_Movment(VelocityArray, body_part[i])
        if Move == True:
            addpoints = int(addpoints + 1)

    return addpoints

def cast_to_list(body_part):
    body_part = list(body_part.split(","))
    return list(map(int, body_part))

def check_Movment(points_Array, index_Array):
        tmp = []
        for i in cast_to_list(index_Array.tolist()):
            tmp.append(points_Array[int(i)])

        if camera.Median(tmp) > 20:
            return True, camera.Median(tmp)
        else:
            return False, camera.Median(tmp)

def Player_Movment_Detection(Freeze_Fram,Fram):
    return points_Counter(camera.Find_Velocity_Diff(Freeze_Fram,Fram))

def points_update(doll,game,current_points):
    doll.points = doll.points + current_points

    if current_points == 0:
        is_player_froze(doll,game.img)
    else:
        doll.no_movement = 0

def Points_Collected(points,img):
    cv2.putText(img, f'{int(points)}', (25, 170), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)

def Health_Bar(cheat, x_for_c,img):
    cv2.rectangle(img, (25, 60), (280, 85), (113, 186, 101), -1)
    if cheat:
        cv2.rectangle(img, (int(x_for_c), 62), (279, 83), (36, 62, 145), -1)
    else:
        cv2.rectangle(img, (int(x_for_c), 62), (279, 83), (36, 62, 145), -1)

def is_player_froze(doll,img):
    if doll.no_movement == 0:
        doll.no_movement = time.time() + 2
    if doll.no_movement < time.time():
        doll.health_Bar_points = doll.health_Bar_points - 0.5
        Health_Bar(True, doll.health_Bar_points, img)

def game_music(doll):
    if (doll.timer - time.time()) <= 5.0 and (doll.timer - time.time()) > 4.9:
        doll.sound = mixer.Sound('sounds/red light green light.wav')
        doll.sound.play()

def move_music(doll):
    if (doll.timer - time.time()) < 1 and doll.turn==True:
        doll.sound = mixer.Sound('sounds/Coin.wav')
        doll.sound.play()

def game_over_win_lose(img,doll):
    if doll.health_Bar_points > 25:
        cv2.putText(img, 'You Win !!!', (500, 430), cv2.FONT_HERSHEY_SIMPLEX, 2, (50, 205, 50), 3)
    else:
        cv2.putText(img, 'You Lose ! ', (500, 430), cv2.FONT_HERSHEY_SIMPLEX, 2, (165, 42, 42), 3)

####################################################################
# basic functions for all the games

def PhotoTrans(imga,photo,tmp,re,pos=[0,0]):
    imgF=cv2.imread(photo,cv2.IMREAD_UNCHANGED)
    imgF=cv2.resize(imgF,(tmp,tmp),None,re,re)
    imgR = overlayPNG(imga,imgF,pos)
    return imgR

def overlayPNG(imgBack, imgFront, pos=[0, 0]):
    hf, wf, cf = imgFront.shape
    hb, wb, cb = imgBack.shape
    *_, mask = cv2.split(imgFront)
    maskBGRA = cv2.cvtColor(mask, cv2.COLOR_GRAY2BGRA)
    maskBGR = cv2.cvtColor(mask, cv2.COLOR_GRAY2BGR)
    imgRGBA = cv2.bitwise_and(imgFront, maskBGRA)
    imgRGB = cv2.cvtColor(imgRGBA, cv2.COLOR_BGRA2BGR)

    imgMaskFull = np.zeros((hb, wb, cb), np.uint8)
    imgMaskFull[pos[1]:hf + pos[1], pos[0]:wf + pos[0], :] = imgRGB
    imgMaskFull2 = np.ones((hb, wb, cb), np.uint8) * 255
    maskBGRInv = cv2.bitwise_not(maskBGR)
    imgMaskFull2[pos[1]:hf + pos[1], pos[0]:wf + pos[0], :] = maskBGRInv

    imgBack = cv2.bitwise_and(imgBack, imgMaskFull2)
    imgBack = cv2.bitwise_or(imgBack, imgMaskFull)

    return imgBack

def stop_and_exit_game(game):
    key = cv2.waitKey(1)
    while key != 27:
        key = cv2.waitKey(1)
    game.cap.release()
    cv2.destroyAllWindows()
    game.Game_is_running = True

    pygame.mixer.music.stop()

def pre_game_setup(game,seconds):
    game.cap.set(game.wCam, game.wCam)
    game.cap.set(game.hCam, game.hCam)

    check_if_camera_detects(game)

    game.game_time.pre_game = game_Time_CountDown(5)
    game.game_time.total_Game_Time = game_Time_CountDown(seconds + 5)

def update_Game_Camera_Data(game):
    game.landmarks, game.img = camera.Pose_And_Camera_Info()
    game.Frame_Array = camera.Landmarks_To_Array(game.landmarks, game.Frame_Array)

    if len(game.Frame_Array) > CF.FrameArray:
        game.Frame_Array = game.Frame_Array[len(game.Frame_Array) - CF.FrameArray:len(game.Frame_Array)]

def check_if_camera_detects(game):
    landmarks, img = camera.Pose_And_Camera_Info()
    flag = not np.any(landmarks)
    while flag and game.Game_is_running == True:
        flag, img = camera.Pose_And_Camera_Info()
        flag = not np.any(flag)
        answer = tkinter.messagebox.askokcancel(title=None,
                                                message="make sure your camera is on or there is a player infront of the camera")
        if answer:
            print()
        else:
            game.Game_is_running = False

def pre_game_countdown(game):
    cv2.rectangle(game.img, (510, 300), (800, 400), (131, 212, 190), -1)
    cv2.putText(game.img, f'Game starts in:{int(game.game_time.pre_game - time.time()) + 1}', (520, 360),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 84, 46), 3)

def game_Time_CountDown(seconds):
    return time.time() + seconds

def check_if_game_time_ended(game,doll):
    if time.time() > game.game_time.total_Game_Time:
        doll.sound.stop()
        game_over(game.img, doll.points)
        game_over_win_lose(game.img, doll)

def check_if_player_is_detected(game):
    # checks if the player is on the screen
    flag = not np.any(game.landmarks)
    if flag:
        # add time
        if game.game_time.pause_Counter > 5:
            cv2.rectangle(game.img, (310, 300), (1040, 400), (109, 180, 227), -1)
            cv2.putText(game.img, f'You are not in the game please come back!', (320, 360), cv2.FONT_HERSHEY_SIMPLEX, 1,(25, 47, 209), 2)
            game.game_time.total_Game_Time=game.game_time.total_Game_Time+0.05
            return False
        # get last landmarks fps=30
        if len(game.Frame_Array) != 0:
            game.landmarks = game.Frame_Array[-1]
            game.game_time.pause_Counter += 1
    else:
        game.game_time.pause_Counter = 0
        return True

def game_over(img, points):
    pygame.mixer.music.load('sounds/Game Over.wav')
    pygame.mixer.music.play()
    cv2.rectangle(img, (350, 200), (1000, 550), (222, 224, 222), -1)
    cv2.putText(img, "GAME OVER !", (350, 300), cv2.FONT_HERSHEY_SIMPLEX, 3, (0, 0, 255), 3)
    cv2.putText(img, f'Score: {str(points)}', (600, 500), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 3)
    cv2.putText(game.img, 'Please press ESC to exit the game', (360, 375), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 3)#400
    game.Game_is_running = False


camera = Camera()
game = game()

### DEBUG ###

#Game_List = [[1, 2, ['16,18,20,22'], 'left hand 90 degree'], [2, 2, ['15,17,19,21'], 'right hand 90 degree'], [3, 2, ['16,18,20,22'], 'left hand 180 degree'], [4, 2, ['15,17,19,21'], 'right hand 180 degree']]

#game.Start_The_Game([CF.left_hand.tolist(),CF.right_hand.tolist()],3,30,False,Game_List)
#game.STG2([CF.left_hand.tolist(),CF.right_hand.tolist()],2,5,False,0)
#game.STG3([CF.left_hand.tolist(),CF.right_hand.tolist()],3,5,False,Game_List)

