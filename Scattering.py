import pygame
import sys
import random
import numpy as np

class dot:
    dim = [1000, 800]
    def __init__(self):
        self.x = random.randint(50,dim[0]-50)
        self.y = random.randint(50, dim[1] - 50)
        self.z = random.randint(50, dim[1] - 50)

        self.m = random.randint(1,3)
        self.vx = random.uniform(-3,3)/self.m
        self.vy = random.uniform(-3, 3) / self.m
        self.vz = random.uniform(-3, 3) / self.m

        self.rad = self.m*5+5
    def update(self,xnew,ynew, vxnew, vynew,):
        self.x, self.y, self.vx, self.vy = xnew, ynew, vxnew, vynew

def change(dots,time,CMx=0,CMy=0):
    for i, dot1 in enumerate(dots):
        r1 = np.array([dot1.x, dot1.y])
        for j, dot2 in enumerate(dots[(i+1)::]):
            r2 = np.array([dot2.x, dot2.y])
            r = r1-r2
            r_norm = np.linalg.norm(r2-r1)
            angle = np.arctan2(r[1], r[0])
            a1 = 5000*dot2.m*r_norm**(-2)
            ax1, ay1 = a1*np.array([np.cos(angle+np.pi),np.sin(angle+np.pi)])
            dvx1, dvy1 = np.array([ax1, ay1])*time
            dx1, dy1 = 0.5*np.array([dvx1, dvy1])*time

            #dot2
            a2 = 5000 * dot1.m * r_norm ** (-2)
            ax2, ay2 = a2 * np.array([np.cos(angle),np.sin(angle)])
            dvx2, dvy2 = np.array([ax2, ay2]) * time
            dx2, dy2 = 0.5 * np.array([dvx2, dvy2]) * time

            dot1.update(dot1.x+dot1.vx*time_step+dx1/dot1.m, dot1.y+dot1.vy*time_step+dy1/dot1.m, dot1.vx+dvx1, dot1.vy+dvy1)
            dot2.update(dot2.x+dot2.vx*time_step+dx2/dot1.m, dot2.y+dot2.vy*time_step+dy2/dot1.m, dot2.vx+dvx2, dot2.vy+dvy2)

def find_rad():
    for num,i in enumerate(dots):
        for j in dots[(num+1)::]:
            v1 = np.array([i.vx,i.vy])
            v2 = np.array([j.vx,j.vy])
            r_b1 = np.array([i.x,i.y])
            r_b2 = np.array([j.x,j.y])
            r1 = r_b2-r_b1
            r2 = r_b1-r_b2
            #retningsvektor

            if np.linalg.norm(r1) < i.rad+j.rad:
                print("Collision!")
                #finder parallelle hastigedsvektor for hver bold v_para1 og v_para2
                v_para1 = np.dot(v1,r1)/np.dot(r1,r1)*r1
                v_para2 = np.dot(v2,r2)/np.dot(r2,r2)*r2
                #finder de vinkelrette hastigheder
                v_perp1 = v1-v_para1
                v_perp2 = v2-v_para2
                #finder nu den parallelle hastighed efter støddet for hver bold
                v_parallel1 = (v_para1*(i.m-j.m)+2*j.m*v_para2)/(i.m+j.m)
                v_parallel2 = (v_para2*(i.m-j.m)+2*i.m*v_para1)/(i.m+j.m)
                #nu indsætter jeg den nye hastighed efter sammenstøddet for hver bold

                v1_new = v_perp1+v_parallel1
                v2_new = v_perp2+v_parallel2
                i.vx, i.vy = v1_new[0], v1_new[1]
                j.vx, j.vy = v2_new[0], v2_new[1]

def drawdot(surf, dot):
    for i in dot:
        pygame.draw.circle(surf, (255, 255, 255), (int(i.x), int(i.y)), i.rad, 1)

def CM(dots):
    M = np.array([o.m for o in dots])
    x = np.array([o.x for o in dots])
    y = np.array([o.y for o in dots])
    CMx = np.sum(x*M)/np.sum(M)
    CMy = np.sum(y*M)/np.sum(M)
    return CMx, CMy

def updateCM(dots,CMx,CMy):
    for i in dots:
        i.x += -(CMx-dim[0]/2)
        i.y += -(CMy-dim[1]/2)


m2 = 1
m1 = 10
pygame.init()
resolution = [1920,1080]
screen = pygame.display.set_mode(resolution,pygame.FULLSCREEN)
dim = screen.get_size()
font = pygame.font.SysFont('Times New Roman', 50)
time_step = 0.05
screen.fill((255,255,255))
random.seed(5461)
while(True):
    screen.fill((100, 41,254 ))
    dots = [dot(),dot(),dot()]
    CMx, CMy = CM(dots)
    updateCM(dots, CMx, CMy)
    timer = 0
    t = True
    while t:
        CMx, CMy = CM(dots)
        if ((CMx>0 and CMx <dim[1]) and (CMy>0 and CMy <dim[1])):
            for event in pygame.event.get():
                if event.type == pygame.QUIT: sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RIGHT: t = False
                    if event.key == pygame.K_ESCAPE: sys.exit()
            screen.fill((100, 41, 254))
            pygame.draw.rect(screen, (0, 255, 0), (CMx, CMy, 5, 5))
            updateCM(dots, CMx, CMy)
            find_rad()
            drawdot(screen,dots)
            change(dots,time_step,CMx,CMy)
            pygame.display.flip()
            timer +=1
        else:
            break
