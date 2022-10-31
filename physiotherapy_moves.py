import numpy as np

moves=[]

#the middle point is the angle point
def calculate_angle(p1,p2,p3):

    a = np.array([p1[1], p1[2]])
    b = np.array([p2[1], p2[2]])
    c = np.array([p3[1], p3[2]])

    ba = a - b
    bc = c - b

    cosine_angle = np.dot(ba, bc) / (np.linalg.norm(ba) * np.linalg.norm(bc))
    angle = np.arccos(cosine_angle)

    return np.degrees(angle)

def Ninety_Degrees_left(Frame_Array,rep):
    angle=calculate_angle(Frame_Array[12],Frame_Array[14],Frame_Array[16])
    if 80<angle<100:
        return 0,1
    else:
        return 1,1
def Ninety_Degrees_right(Frame_Array):
    angle = calculate_angle(Frame_Array[11], Frame_Array[13], Frame_Array[15])
    if 80 < angle < 100:
        return 0,2
    else:
        return 1,2
def one_hundred_eighty_Degrees_left(Frame_Array):
    angle = calculate_angle(Frame_Array[12], Frame_Array[14], Frame_Array[16])
    if 160 < angle < 170:
        return 0, 3
    else:
        return 1, 3
def one_hundred_eighty_Degrees_Right(Frame_Array):
    angle = calculate_angle(Frame_Array[11], Frame_Array[13], Frame_Array[15])
    if 160 < angle < 170:
        return 0, 4
    else:
        return 1, 4