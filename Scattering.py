import pygame
import sys
import random
import numpy as np

class dot:
    dim = [1000, 800]
    def __init__(self,dim):
        #Choose a random spot on the screen to "spawn" the planet
        self.x = random.randint(50,dim[0]-50)
        self.y = random.randint(50, dim[1] - 50)

        #Choose a random mass and velocity
        self.m = random.randint(1,3)
        self.vx = random.uniform(-3,3)/self.m
        self.vy = random.uniform(-3, 3) / self.m
        self.vz = random.uniform(-3, 3) / self.m

        #define radius by its mass
        self.rad = self.m*5+5

    def update(self,xnew,ynew, vxnew, vynew,):
        self.x, self.y, self.vx, self.vy = xnew, ynew, vxnew, vynew


class Run:
    def __init__(self,screen,n_planets,dim,time_step):
        self.screen = screen
        self.n_planets = n_planets
        self.dim = dim
        self.time_step = time_step
        self.run()

    def change(self):
        #function that calculates the new acceleration, velocity and position and updates each planets position on the screen.
        for i, dot1 in enumerate(self.dots):
            r1 = np.array([dot1.x, dot1.y])
            for j, dot2 in enumerate(self.dots[(i+1)::]):
                r2 = np.array([dot2.x, dot2.y])
                r = r1-r2
                r_norm = np.linalg.norm(r2-r1)
                angle = np.arctan2(r[1], r[0])
                a1 = 5000*dot2.m*r_norm**(-2)
                a2 = 5000 * dot1.m * r_norm ** (-2)
                #Split the acceleration into x,y components
                ax1, ay1 = a1*np.array([np.cos(angle+np.pi),np.sin(angle+np.pi)])
                ax2, ay2 = a2 * np.array([np.cos(angle), np.sin(angle)])
                #Forward Euler to obtain velocity
                dvx1, dvy1 = np.array([ax1, ay1])*self.time_step
                dvx2, dvy2 = np.array([ax2, ay2]) * self.time_step
                #Forward Euler to obtain position
                dx1, dy1 = 0.5*np.array([dvx1, dvy1])*self.time_step
                dx2, dy2 = 0.5 * np.array([dvx2, dvy2]) * self.time_step

                #Update planets position
                dot1.update(dot1.x+dot1.vx*self.time_step+dx1/dot1.m, dot1.y+dot1.vy*self.time_step+dy1/dot1.m, dot1.vx+dvx1, dot1.vy+dvy1)
                dot2.update(dot2.x+dot2.vx*self.time_step+dx2/dot1.m, dot2.y+dot2.vy*self.time_step+dy2/dot1.m, dot2.vx+dvx2, dot2.vy+dvy2)

    def find_rad(self):
        for num,i in enumerate(self.dots):
            for j in self.dots[(num+1)::]:
                #vectorize the velocity
                v1 = np.array([i.vx,i.vy])
                v2 = np.array([j.vx,j.vy])
                #vectorize the position
                r_b1 = np.array([i.x,i.y])
                r_b2 = np.array([j.x,j.y])
                r1 = r_b2-r_b1
                r2 = r_b1-r_b2
                #Directional vector

                if np.linalg.norm(r1) < i.rad+j.rad:
                    print("Collision!")
                    #Find the parallel velocity vector for each planet v_para1 og v_para2
                    v_para1 = np.dot(v1,r1)/np.dot(r1,r1)*r1
                    v_para2 = np.dot(v2,r2)/np.dot(r2,r2)*r2
                    #Find the perpendicular velocities
                    v_perp1 = v1-v_para1
                    v_perp2 = v2-v_para2
                    #Find the parallel velocities after the collision
                    v_parallel1 = (v_para1*(i.m-j.m)+2*j.m*v_para2)/(i.m+j.m)
                    v_parallel2 = (v_para2*(i.m-j.m)+2*i.m*v_para1)/(i.m+j.m)

                    #Update each ball with the new velocity
                    v1_new = v_perp1+v_parallel1
                    v2_new = v_perp2+v_parallel2
                    i.vx, i.vy = v1_new[0], v1_new[1]
                    j.vx, j.vy = v2_new[0], v2_new[1]

    def drawdot(self):
        #Draw the planets on the screen
        for i in self.dots:
            pygame.draw.circle(self.screen, (255, 255, 255), (int(i.x), int(i.y)), i.rad, 5)

    def CM(self):
        #Calculate the centor of mass
        M = np.array([o.m for o in self.dots])
        x = np.array([o.x for o in self.dots])
        y = np.array([o.y for o in self.dots])
        CMx = np.sum(x*M)/np.sum(M)
        CMy = np.sum(y*M)/np.sum(M)
        return CMx, CMy

    def updateCM(self,CMx,CMy):
        #Move all the planets, such that their center of mass is in the center of the screen.
        for i in self.dots:
            i.x += -(CMx-self.dim[0]/2)
            i.y += -(CMy-self.dim[1]/2)


    def run(self):
        #Updates the program continously.
        while True:
            self.screen.fill((100, 41, 254))

            #Generate new planets for each new system
            self.dots = [dot(self.dim) for _ in range(self.n_planets)]
            # Adjusts center of mass, such that it starts in the center of the screen.
            CMx, CMy = self.CM()
            self.updateCM(CMx, CMy)

            t = True
            while t:
                CMx, CMy = self.CM()

                #Checks of center of mass is located at the center of the screen. If not something has gone wrong and it loads a new system.
                if ((CMx>(self.dim[0]/2-1) and CMx < (self.dim[0]/2+1)) and (CMy>(self.dim[1]/2-1) and CMy < (self.dim[1]/2+1))):
                    for event in pygame.event.get():
                        print(pygame.K_RIGHT)
                        if event.type == pygame.QUIT: sys.exit()
                        if event.type == pygame.KEYDOWN:
                            if event.key == pygame.K_RIGHT: t = False #Right arrow to load a new system.
                            if event.key == pygame.K_ESCAPE: sys.exit() #Esc to quit the interface.
                    self.screen.fill((100, 41, 254))


                    #Find the radial distance between each planet
                    self.find_rad()
                    #Calculate their new positions
                    self.change()
                    #Update the center of mass position
                    self.updateCM(CMx, CMy)
                    #Draw the planets
                    self.drawdot()
                    pygame.display.flip()
                else:
                    break

def main():
    #Initialize Pygame window
    pygame.init()

    # Set the resolution of the window
    resolution = [1920, 1080]

    # Set Fullscreen mode or window mode
    FULLSCREEN = True
    if FULLSCREEN:
        screen = pygame.display.set_mode(resolution, pygame.FULLSCREEN)
    else:
        screen = pygame.display.set_mode(resolution, pygame.FULLSCREEN)

    dim = screen.get_size()
    #font = pygame.font.SysFont('Times New Roman', 50)

    time_step = 0.05
    #Choose the number of planets to simulate
    n_planets = 3

    #Run the sim
    Run(screen,n_planets,dim,time_step)

if __name__ == '__main__':
    main()
