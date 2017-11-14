import matplotlib
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.animation as animation
import numpy as np

blue = (0, 0, 1, 1)
green = (0, 1, 0, 1)
red = (1, 0, 0, 1)
black = (0,0,0,1)
grey = (0.3, .3, .3, 1)
g = 9.81 #m/s^2

def startFig():
    plt.close('all')
    fig = plt.figure(figsize=[10,10])
    #ax = fig.add_subplot(111, projection='3d')
    ax = Axes3D(fig)
    return ax

def arrow( ax, (x,y,z), (u,v,w), label, color, middle=False):  
    animate = ax.quiver(x,y,z, u,v,w, arrow_length_ratio=.05,\
                  colors=[color], linewidths=[2])
    if middle:
        ex,ey,ez = x+0.5*u, y+0.5*v, z+0.5*w
        offset=True
    else:
        ex,ey,ez = x+u, y+v, z+w
        offset=False
    label =drawLabel(ax, (ex,ey,ez), label, offset)
    
    return animate#, label

def drawLabel(ax, (x,y,z),label, offset=False):
    if offset:
        z += 0.25
    return ax.text(x,y,z, label, size=20)

    
def set_bounds(ax,X):
    x2,y2,z2 = np.max(X, axis=0) + 1
    x1,y1,z1 = np.min(X, axis=0) - 1

    ax.set_xlim3d(x1, x2)
    ax.set_ylim3d(y1, y2)
    ax.set_zlim3d(z1, z2)
    
        
def plotAll(A, B, rO, rQ, rPQ, rP, ax=None, labels=True):
    if ax is None:
        ax = startFig()
    
    bounds = [rO]
    
    E1, E2, E3 = A    
    # plot frame A
        
    arrow(ax, rO, E1, 'E1', black)
    arrow(ax, rO, E2, 'E2', black)
    arrow(ax, rO, E3, 'E3', black)
    if labels:drawLabel(ax, rO, 'O')
    
    if rP is not None:
        #plot point P observed in A
        arrow(ax, rO, rP, 'rP', green, middle=True)
        if labels:drawLabel(ax, rP, 'P')
        bounds.append(rP)
    
    
    #plot frame B
    if B is not None:
        #plot frame B
        e1, e2, e3 = B 
        if labels:
            arrow(ax, rQ, e1, 'e1', grey)
            arrow(ax, rQ, e2, 'e2', grey)
            arrow(ax, rQ, e3, 'e3', grey)          
        else:
            arrow(ax, rQ, e1, '', grey)
            arrow(ax, rQ, e2, '', grey)
            arrow(ax, rQ, e3, '', grey)
        
        # Plot point Q observed in A
        arrow(ax, rO, rQ ,'rQ', blue, middle=True)
        if labels:drawLabel(ax, rQ, 'Q')

        #plot point P observed in B
        arrow(ax, rQ, rPQ, 'rPQ', blue, middle=True)
        bounds = [rO, rPQ+rQ, rP, rQ]

        
    x2,y2,z2 = np.max(bounds, axis=0) + 1
    x1,y1,z1 = np.min(bounds, axis=0) - 1

    ax.set_xlim3d(x1, x2)
    ax.set_ylim3d(y1, y2)
    ax.set_zlim3d(z1,z2)

    plt.show()
    
def plotAbsMotion(A, rO, rP, ax = None):
    plotAll(A, None, rO, None, None, rP, ax)
    
def init_animation(ax, color):
    # set up lines and points
    lines = ax.plot([], [], [], '-', c=color)   
    pts = ax.plot([], [], [], 'o', c=color)
    trajs = ax.plot([], [], [], '--', c=color)
    #label =  ax.text(0, 0, 0, label, size=20)
    
    def init():
        for items in (lines, pts, trajs):
            for item in items:
                item.set_data([] , [])
                item.set_3d_properties([])    
        return lines + pts
    
    anims =(lines, pts, trajs)

    return anims, init

def setupAnimation(name_traj_color_list):
    # create plot with fixed frame A located at (0,0,0)
    A = np.eye(3) 
    rO = np.array((0,0,0))
    ax = startFig()
    fig = plt.gcf()
    plotAbsMotion(A, rO, None, ax)
    
    X_ts = []
    inits = []
    label_names = []
    anim_funcs = []
    
    for (name, traj, color) in name_traj_color_list:
        traj = traj[0].copy(), traj[1].copy()
        anims,  init = init_animation(ax, color)
        label_names.append(name)
        X_ts.append(traj)
        inits.append(init)
        anim_funcs.append(anims)
    x_bound = [X[1] for X in X_ts]
    set_bounds(ax,np.vstack(x_bound))
    
    def init_funcs():
        res = []
        for init in inits:
            res += init()
        return res
    return ax, fig, X_ts, init_funcs, label_names, anim_funcs 


def runAnimation(ntc):
    
    ax, fig, X_ts, init_funcs, label_names, anim_funcs = setupAnimation(ntc)
    
    def animate(i):
        labels = []

        # loop
        for j in range(len(label_names)):

            x_t = np.hstack( X_ts[j])
            anims = anim_funcs[j]
            ox, oy, oz, x, y, z = x_t[i]
            x_traj = x_t[0:i, (0,1,2)] + x_t[0:i, (3,4,5)]
            lines, pts, trajs = anims

            for line, pt, traj in zip(lines, pts, trajs):
                line.set_data([ox,x+ox], [oy,y +oy])
                line.set_3d_properties([oz,z + oz])
                pt.set_data(x+ox, y+oy)
                pt.set_3d_properties(z+oz)
                traj.set_data(x_traj[:,0], x_traj[:,1])
                traj.set_3d_properties(x_traj[:,2])
                labels.append(ax.text(x+ox, y+oy, z+oz, label_names[j], size=20))

        fig.canvas.draw()
        for label in labels:
            label.set_text("")
        return lines #+ pts
    frames = len(X_ts[0][0])
    
    args = {
            'func':animate,
            'init_func':init_funcs,
            'frames':frames,
            'interval':30, 
            'blit':True
           }

    return fig, args


    