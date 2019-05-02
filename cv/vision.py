import cv2
import multiprocessing
import threading
import time
import numpy as np

surfaces = ['RFDLUFDFR', 'FDBURBLRU', 'BRURFFFDF',
            'DBUUDBFRB', 'UDLLLUDLL', 'RLBUBBLDR']
face_number=0
grid_colors=[]
_update_flag=0
_update_flag_A=0
_update_flag_B=0
_show_select_face_flag=0

def update_surfaces():
    global _update_flag
    _update_flag=1

def update_surfaces_A():
    global _update_flag_A
    _update_flag_A=1

def update_surfaces_B():
    global _update_flag_B
    _update_flag_B=1

def show_select_face(flag):
    global _show_select_face_flag
    if flag==0 and _show_select_face_flag!=0:
        _show_select_face_flag=-1
        return
    _show_select_face_flag=flag
    
class VisionProcess(threading.Thread):
    def __init__(self):
        super(VisionProcess, self).__init__()
        self.daemon = True

    def run(self):
        cap=cv2.VideoCapture(0)
#        cap.set(cv2.CAP_PROP_BRIGHTNESS,0.1)
#        cap.set(cv2.CAP_PROP_SATURATION,0.4)
        red_orange = 0.5  # type: int  555!
        global _update_flag
        global _update_flag_A
        global _update_flag_B
        global face_number
        global grid_colors
        global _show_select_face_flag
        while 1:
            _, image = cap.read()
            image = image[140:450, 180:550]
            k = 8 
            grid_colors_A = [0] * 9
            grid_colors_B = [0] * 9
            face_number_A = 0
            face_number_B = 0
            grid_center_list = [[(59 , 91 ), (95 , 84 ), (142, 66 ), 
                                 (62 , 156), (99 , 152), (147, 148), 
                                 (66 , 223), (102, 227), (152, 229)],
                                [(203, 66 ), (242, 79 ), (285, 76 ),
                                 (203, 148), (244, 144), (292, 138),
                                 (203, 229), (249, 221), (293, 212)]]
            for major in range(2):
                grid_center = grid_center_list[major]
                grid_colors = [0] * 9
                grids = [0] * 9
                for i in range(9):
                    center=grid_center[i]
                    x1=center[0]-k
                    x2=center[0]+k
                    y1=center[1]-k
                    y2=center[1]+k 
                    grids[i]=image[y1:y2,x1:x2]
                    grid=grids[i]*1
                    b=int(np.average(grid[:,:,0]))
                    g=int(np.average(grid[:,:,1]))
                    r=int(np.average(grid[:,:,2]))
                    red_flag=0
                    green_flag=0
                    white_flag=0
                    if r+b+g<250:
                        red_flag=1
                    if r<80:
                        green_flag=1
                    if min([r,g,b])/(max([r,g,b])+0.01)>0.80:
                        white_flag=1
                    grid[:,:]=(b,g,r)
                    cvt=cv2.cvtColor(grid, cv2.COLOR_BGR2HSV)
                    h=cvt[0,0,0]
                    s=cvt[0,0,1]
                    # v=cvt[0,0,2]
                    if (white_flag):
                        grids[i][:,:]=(0,0,0)
                        grid_colors[i]='D'       
                    else:
                        if (h>=0 and h<25) or (h>=165 and h<180):
                            if red_flag:
                                grids[i][:,:]=(0,0,255)
                                grid_colors[i]='F'
                            else:
                                grids[i][:,:]=(204,50,153)
                                grid_colors[i]='B'
                        if h>=25 and h<100:
                            if green_flag:
                                grids[i][:,:]=(0,255,0)
                                grid_colors[i]='R'
                            else:
                                grids[i][:,:]=(0,255,255)
                                grid_colors[i]='U'
                        if h>=100 and h<165:
                            grids[i][:,:]=(255,0,0)
                            grid_colors[i]='L'
                if grid_colors[4] == 'D': face_number = 3  # white
                if grid_colors[4] == 'F': face_number = 2  # red
                if grid_colors[4] == 'B': face_number = 5  # orange
                if grid_colors[4] == 'U': face_number = 0  # yellow
                if grid_colors[4] == 'R': face_number = 1  # green
                if grid_colors[4] == 'L': face_number = 4  # blue
                if major == 0:
                    grid_colors_A = grid_colors
                    face_number_A = face_number 
                else:
                    grid_colors_B = grid_colors
                    face_number_B = face_number 

            if _update_flag:
                surfaces[face_number_A] = grid_colors_A
                surfaces[face_number_B] = grid_colors_B
                cv2.imwrite("record_image/"+str(face_number_A+1)+".JPEG",image)
                cv2.imwrite("record_image/"+str(face_number_B+1)+".JPEG",image)
                _update_flag=0 

            if _update_flag_A:
                surfaces[face_number_A] = grid_colors_A
                cv2.imwrite("record_image/"+str(face_number_A+1)+".JPEG",image)
                _update_flag_A=0 

            if _update_flag_B:
                surfaces[face_number_B] = grid_colors_B
                cv2.imwrite("record_image/"+str(face_number_B+1)+".JPEG",image)
                _update_flag_B=0 

            if _show_select_face_flag==-1:
                cv2.destroyWindow('face_record')
                _show_select_face_flag=0
            if _show_select_face_flag!=0:
                cv2.imshow('face_record',
                           cv2.imread("record_image/"+str(_show_select_face_flag)+".JPEG"))
            
            #cv2.imshow('frame2', image)
            cv2.waitKey(20)


vision = VisionProcess()
vision.start()
print("vision module start working!")
