import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import mplanimations as ans
import random

G = .00001 # The gravitational constant is set at this value for convenience
dt = 1/100

class Objects:

    def __init__(self):

        self.mass = np.random.random()*10
        self.pos = np.array([np.random.random()*2, np.random.random()*2], dtype=float)
        self.v = np.array([[-1,1][random.randrange(2)]*np.random.random()/50, [-1,1][random.randrange(2)]*np.random.random()/50], dtype=float)

        
    def update(self, objs):

        self.force = np.array([0, 0], dtype=float)
        
        for obj in objs:
            self.seperation = np.hypot(self.pos[0]-obj.pos[0], self.pos[1]-obj.pos[1])
            
            if self.seperation > .1: # Turning off gravity if the objects get too close together
                self.force += np.array([(G*self.mass*obj.mass/(self.seperation**2))*
                                        ((np.absolute(obj.pos[0] - self.pos[0]))/self.seperation)*
                                        float(np.where(obj.pos[0]-self.pos[0] != 0, (obj.pos[0]-self.pos[0])/(np.absolute(obj.pos[0]-self.pos[0])), 0)),
                                        (G*self.mass*obj.mass/(self.seperation**2))*
                                        ((np.absolute(obj.pos[1] - self.pos[1]))/self.seperation)*
                                        float(np.where(obj.pos[1]-self.pos[1] != 0, (obj.pos[1]-self.pos[1])/(np.absolute(obj.pos[1]-self.pos[1])), 0))])
                self.acceleration = self.force/self.mass
                self.v += (self.acceleration*dt)
                self.pos += self.v*dt
                
        else:
            self.pos += self.v*dt

            
    def center_of_mass(positions, masses):
        cm = 0
        for i in range(len(masses)):
            cm += positions[i]*masses[i]
        cm = cm/np.sum(masses)
        return cm


plt.style.use('dark_background')

fig, ax = plt.subplots()

ax.set_aspect('equal')
ax.set_xlim(-.5, 8)
ax.set_ylim(-.5, 2)
ax.axis('off')

objects = [Objects() for i in range(5)]

scatters = [ax.scatter(obj.pos[0], obj.pos[1], s=5) for obj in objects]

es = [ans.Effects() for i in range(len(objects))]

def animate(i):
    for i in range(10):
        for obj in objects:
            obj.update(objects)
        
    for i in range(len(scatters)):
        es[i].tail([objects[i].pos[0]], [objects[i].pos[1]], scatters[i], plt.get_cmap('hsv')(i/len(scatters)), 30)
    
    cm = Objects.center_of_mass([obj.pos for obj in objects], [obj.mass for obj in objects])
    ax.set_xlim(cm[0]-2.5, cm[0]+2.5)
    ax.set_ylim(cm[1]-2.5, cm[1]+2.5)

animation = animation.FuncAnimation(fig, animate, interval=10, frames=2000, repeat=False)

plt.show()
