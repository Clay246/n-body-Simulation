import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import mplanimations as ans

m1 = 1
m2 = 10
G = .00001

dt = 1/100


class Objects:

    def __init__(self, mass, x, y, vx, vy):

        self.mass = mass
        self.pos = np.array([x, y], dtype=float)
        self.v = np.array([vx, vy], dtype=float)

    def update(self, obj):
        
        self.seperation = np.hypot(self.pos[0]-obj.pos[0], self.pos[1]-obj.pos[1])
        
        if self.seperation > .1:
            self.force = np.array([   (G*self.mass*obj.mass/(self.seperation**2))*
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
ax.set_xlim(-.5, 1.5)
ax.set_ylim(-.5, 1.5)
ax.axis('off')

obj1 = Objects(m1, 0, 1, .005, 0)
obj2 = Objects(m2, 0, 0, 0, 0)

o1 = ax.scatter(obj1.pos[0], obj1.pos[1], c='cyan', s=2)
o2 = ax.scatter(obj2.pos[0], obj2.pos[1], c='yellow')
o2tail = ax.scatter(obj2.pos[0], obj2.pos[1], c='yellow', s=5)

es = [ans.Effects() for i in range(2)]

def animate(i):
    for i in range(50):
        obj1.update(obj2)
        obj2.update(obj1)
        
    o2.set_offsets(obj2.pos)
    es[0].tail([obj1.pos[0]], [obj1.pos[1]], o1, 'cyan', 50)
    es[1].tail([obj2.pos[0]], [obj2.pos[1]], o2tail, 'yellow', 50)

    cm = Objects.center_of_mass([obj1.pos, obj2.pos], [obj1.mass, obj2.mass])
    ax.set_xlim(cm[0]-.75, cm[0]+.75)
    ax.set_ylim(cm[1]-.5, cm[1]+1.5)

animation = animation.FuncAnimation(fig, animate, interval=20, frames=1000, repeat=False)

plt.show()
