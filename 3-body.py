import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import mplanimations as ans

m1 = 10
m2 = 10
m3 = 10
G = .00001

dt = 1/200


class Objects:


    def __init__(self, mass, x, y, vx, vy):

        self.mass = mass
        self.pos = np.array([x, y], dtype=float)
        self.v = np.array([vx, vy], dtype=float)


    def update(self, objs):

        self.force = np.array([0, 0], dtype=float)
        
        for obj in objs:
            
            self.seperation = np.hypot(self.pos[0]-obj.pos[0], self.pos[1]-obj.pos[1])
            
            if self.seperation > .1: # Gravity is turned off if the objects are too close together.
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

obj1 = Objects(m1, 0, 1, .005, 0)
obj2 = Objects(m2, 0, 0, 0, 0)
obj3 = Objects(m3, .5, .5, .001, -.0009)

o1 = ax.scatter(obj1.pos[0], obj1.pos[1], c='cyan', s=2)
o2 = ax.scatter(obj2.pos[0], obj2.pos[1], c='yellow', s=2)
o3 = ax.scatter(obj3.pos[0], obj3.pos[1], c='magenta', s=2)

es = [ans.Effects() for i in range(3)]

def animate(i):
    for i in range(100):
        obj1.update([obj2, obj3])
        obj2.update([obj1, obj3])
        obj3.update([obj1, obj2])
    
    es[0].tail([obj1.pos[0]], [obj1.pos[1]], o1, 'cyan', 50)
    es[1].tail([obj2.pos[0]], [obj2.pos[1]], o2, 'yellow', 50)
    es[2].tail([obj3.pos[0]], [obj3.pos[1]], o3, 'magenta', 50)

    cm = Objects.center_of_mass([obj1.pos, obj2.pos, obj3.pos], [obj1.mass, obj2.mass, obj3.mass])
    
    ax.set_xlim(cm[0]-1.5, cm[0]+1.5)
    ax.set_ylim(cm[1]-1.5, cm[1]+1.5)

animation = animation.FuncAnimation(fig, animate, interval=20, frames=1000, repeat=False)

##plt.show()

plt.rcParams["animation.convert_path"] = r"C:\Program Files\ImageMagick-7.0.9-Q16\magick.exe"
animation.save(r"C:\Users\ClayK\OneDrive\Programs\3-body.gif",writer="imagemagick", extra_args="convert", fps=50)


