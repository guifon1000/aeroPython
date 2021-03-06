import math
import numpy as np
import matplotlib.pyplot as plt
from scipy import integrate


class sourceSink:
    def __init__(self,strength,x,y):
        self.strength=strength
        self.x=x
        self.y=y

    def get_velocity(self, X, Y):
        """Returns the velocity field generated by a source/sink.
    
        Arguments
        ---------
        """
        u = self.strength/(2*np.pi)*(X-self.x)/((X-self.x)**2+(Y-self.y)**2)
        v = self.strength/(2*np.pi)*(Y-self.y)/((X-self.x)**2+(Y-self.y)**2)
    
        return [u, v]



    def get_stream_function(self, X, Y):
        """Returns the stream-function generated by a source/sink.
    
        Arguments
        ---------
        strength -- strength of the source/sink.
        xs, ys -- coordinates of the source/sink.
        X, Y -- mesh grid.
        """
        psi = self.strength/(2*np.pi)*np.arctan2((Y-self.y), (X-self.x))
    
        return psi

            

class doublet:
    def __init__(self,kappa,x,y):
        self.kappa=kappa
        self.x=x
        self.y=y

    def get_velocity(self,X,Y):
        dx=X-self.x
        dy=Y-self.y
        u=-self.kappa/(2*np.pi)*(dx*dx-dy*dy)/(dx**2+dy**2)**2
        v=-self.kappa/(np.pi)*dx*dy/(dx**2+dy**2)**2
        return [u,v]

    def get_stream_function(self,X,Y):
        dx=X-self.x
        dy=Y-self.y
        psi=-self.kappa/(2*np.pi)*dy/(dx**2+dy**2)**2
        return psi


class vortex:
    def __init__(self,gamma,x,y):
        self.gamma=gamma
        self.x=x
        self.y=y
    def get_velocity(self,X,Y):
        dx=X-self.x
        dy=Y-self.y
        u=self.gamma/(2*np.pi)*dy/((dx**2+dy**2)**2)
        v=-self.gamma/(2*np.pi)*dx/((dx**2+dy**2)**2)
        return [u,v]
    def get_stream_function(self,X,Y):
        dx=X-self.x
        dy=Y-self.y
        psi=self.gamma/(4*np.pi)*np.log(dx**2+dy**2)
        return psi


class freeStream:
    def __init__(self,Vinf=1.0,alpha=0.):
        self.alpha=alpha*np.pi/180.
        self.u=Vinf*np.cos(self.alpha)
        self.v=Vinf*np.sin(self.alpha)

class Panel:
    """Contains information related to a panel."""
    def __init__(self, xa, ya, xb, yb):
        """Initializes the panel.
        
        Arguments
        ---------
        xa, ya -- coordinates of the first end-point of the panel.
        xb, yb -- coordinates of the second end-point of the panel.
        """
        self.xa, self.ya = xa, ya
        self.xb, self.yb = xb, yb
        
        self.xc, self.yc = (xa+xb)/2, (ya+yb)/2       # control-point (center-point)
        self.length = math.sqrt((xb-xa)**2+(yb-ya)**2)     # length of the panel
        
        # orientation of the panel (angle between x-axis and panel's normal)
        if xb-xa <= 0.:
            self.beta = math.acos((yb-ya)/self.length)
        elif xb-xa > 0.:
            self.beta = math.pi + math.acos(-(yb-ya)/self.length)
        
        self.sigma = 0.                             # source strength
        self.vt = 0.                                # tangential velocity
        self.cp = 0.                                # pressure coefficient

    #def potential(self,x,y):
         


class pointPale:
    def __init__(self,r,teta):
       self.x=r*np.cos(teta)
       self.y=r*np.sin(teta)
       



def integral_tangential(p_i, p_j):
    """Evaluates the contribution of a panel at the center-point of another,
    in the tangential direction.
    
    Arguments
    ---------
    p_i -- panel on which the contribution is calculated.
    p_j -- panel from which the contribution is calculated.
    
    Returns
    -------
    Integral over the panel of the influence at a control-point.
    """
    def func(s):
        return ( (-(p_i.xc-(p_j.xa-math.sin(p_j.beta)*s))*math.sin(p_i.beta)
                  +(p_i.yc-(p_j.ya+math.cos(p_j.beta)*s))*math.cos(p_i.beta))
                /((p_i.xc-(p_j.xa-math.sin(p_j.beta)*s))**2
                  +(p_i.yc-(p_j.ya+math.cos(p_j.beta)*s))**2) )
    return integrate.quad(lambda s:func(s),0.,p_j.length)[0]




def infiniteSourceSheet(y_min,y_max,strength):
    # computes the velcity field generated by the source-sheet
    plt.clf()
    u_sheet = np.empty((N, N), dtype=float)
    v_sheet = np.empty((N, N), dtype=float)
    for i in xrange(N):
        for j in xrange(N):  
            integrand = lambda s : X[i,j]/(X[i,j]**2+(Y[i,j]-s)**2)
            u_sheet[i,j] = sigma/(2*np.pi)*integrate.quad(integrand, y_min, y_max)[0]
            integrand = lambda s: (Y[i,j]-s)/(X[i,j]**2+(Y[i,j]-s)**2)
            v_sheet[i,j] = sigma/(2*np.pi)*integrate.quad(integrand, y_min, y_max)[0]
# superposition of the source-sheet to the uniform flow
    u = Vinf.u + u_sheet
    v = Vinf.v + v_sheet
    plt.axvline(0.0, (y_min-y_start)/(y_end-y_start), (y_max-y_start)/(y_end-y_start),\
                color='#CD2305', linewidth=4)
    velocity = plt.contourf(X, Y, np.sqrt(u**2+v**2), levels=np.linspace(0.0, 0.1, 10))
    cbar = plt.colorbar(velocity, ticks=[0, 0.05, 0.1], orientation='horizontal')
    cbar.set_label('Velocity magnitude', fontsize=16);


def flowOverCylinder(R,N_panels):
# defines the cylinder        
    u_inf=1.0                                           # radius
    theta = np.linspace(0, 2*math.pi, 100)                           # angles in radians
    x_cylinder, y_cylinder = R*np.cos(theta), R*np.sin(theta)           
# defining the end-points of the panels
    x_ends = R*np.cos(np.linspace(0, 2*math.pi, N_panels+1))
    y_ends = R*np.sin(np.linspace(0, 2*math.pi, N_panels+1))

# defining the panels
    panels = np.empty(N_panels, dtype=object)
    for i in xrange(N_panels):
        panels[i] = Panel(x_ends[i], y_ends[i], x_ends[i+1], y_ends[i+1])
   
    # computes the source influence matrix
    A = np.empty((N_panels, N_panels), dtype=float)
    np.fill_diagonal(A, 0.5)

    for i, p_i in enumerate(panels):
        for j, p_j in enumerate(panels):
            if i != j:
                A[i,j] = 0.5/math.pi*integral_normal(p_i, p_j)

    # computes the RHS of the linear system
    b = - u_inf * np.cos([p.beta for p in panels])

    # solves the linear system
    sigma = np.linalg.solve(A, b )#the matrix of the linear system
    A = np.empty((N_panels, N_panels), dtype=float)
    np.fill_diagonal(A, 0.0)

    for i, p_i in enumerate(panels):
        for j, p_j in enumerate(panels):
            if i != j:
                A[i,j] = 0.5/math.pi*integral_tangential(p_i, p_j)

    # computes the RHS of the linear system
    b = - u_inf * np.sin([panel.beta for panel in panels])

    # computes the tangential velocity at each panel center-point
    vt = np.dot(A, sigma) + b

    for i, panel in enumerate(panels):
        panel.vt = vt[i]
        # computes the tangential velocity at each panel center-point
    vt = np.dot(A, sigma) + b
    for i, panel in enumerate(panels):
        panel.sigma = sigma[i]
    return panels

     
# plotting the panels
    plt.grid(True)
    plt.xlabel('x', fontsize=16)
    plt.ylabel('y', fontsize=16)
    plt.plot(x_cylinder, y_cylinder, color='b', linestyle='-', linewidth=1)
    plt.plot(x_ends, y_ends, color='#CD2305', linestyle='-', linewidth=2)
    plt.scatter([p.xa for p in panels], [p.ya for p in panels], color='#CD2305', s=40)
    plt.scatter([p.xc for p in panels], [p.yc for p in panels], color='k', s=40, zorder=3)
    plt.legend(['cylinder', 'panels', 'end-points', 'center-points'], 
               loc='best', prop={'size':16})
    plt.xlim(-1.1, 1.1)
    plt.ylim(-1.1, 1.1);
    plt.show()


def integral_normal(p_i, p_j):
    """Evaluates the contribution of a panel at the center-point of another,
    in the normal direction.
    
    Arguments
    ---------
    p_i -- panel on which the contribution is calculated.
    p_j -- panel from which the contribution is calculated.
    
    Returns
    -------
    Integral over the panel of the influence at a control-point.
    """
    def func(s):
		return ( (+(p_i.xc-(p_j.xa-math.sin(p_j.beta)*s))*math.cos(p_i.beta)
                  +(p_i.yc-(p_j.ya+math.cos(p_j.beta)*s))*math.sin(p_i.beta))
                /((p_i.xc-(p_j.xa-math.sin(p_j.beta)*s))**2
                  +(p_i.yc-(p_j.ya+math.cos(p_j.beta)*s))**2) )
    return integrate.quad(lambda s:func(s), 0., p_j.length)[0]







def integral_tangential(p_i, p_j):
    """Evaluates the contribution of a panel at the center-point of another,
    in the tangential direction.
    
    Arguments
    ---------
    p_i -- panel on which the contribution is calculated.
    p_j -- panel from which the contribution is calculated.
    
    Returns
    -------
    Integral over the panel of the influence at a control-point.
    """
    def func(s):
        return ( (-(p_i.xc-(p_j.xa-math.sin(p_j.beta)*s))*math.sin(p_i.beta)
                  +(p_i.yc-(p_j.ya+math.cos(p_j.beta)*s))*math.cos(p_i.beta))
                /((p_i.xc-(p_j.xa-math.sin(p_j.beta)*s))**2
                  +(p_i.yc-(p_j.ya+math.cos(p_j.beta)*s))**2) )
    return integrate.quad(lambda s:func(s),0.,p_j.length)[0]






N = 100                                # number of points in each direction
x_start, x_end = -2.0, 2.0            # boundaries in the x-direction
y_start, y_end = -2.0, 2.0            # boundaries in the y-direction
x = np.linspace(x_start, x_end, N)    # creates a 1D-array with the x-coordinates
y = np.linspace(y_start, y_end, N)    # creates a 1D-array with the y-coordinates
Vinf=freeStream(1.0,0.)



X, Y = np.meshgrid(x, y)              # generates a mesh grid


u,v=Vinf.u,Vinf.v
psi=0.
# plots the streamlines of the pair source/sink
size = 10
plt.figure(figsize=(size, (y_end-y_start)/(x_end-x_start)*size))


# 2 doublets de part et d autre d un mur en y=0
s=[doublet(2.0,0.5,0.001),doublet(2.0,0.5,-0.01)]
s=[]


# ligne de 50 vortex
Nv=50

xv=[-0.5+ np.float(1.*i/Nv) for i in range(Nv)]
yv=[0]*Nv

s=[]
for i in range(len(xv)):
    s.append(vortex(-(1.0)**i,xv[i],yv[i]))
#plt.scatter(xv,yv)
s=[]


# ligne verticale de sources
Ns=100
xs=np.zeros(Ns, dtype=float)
ys=np.linspace(-1.0,1.0,Ns)
strength=0.1
for i in range(Ns):
    s.append(sourceSink(strength,xs[i],ys[i]))
#plt.scatter(xs,ys)
s=[]



for si in s:
    u+=si.get_velocity(X, Y)[0]
    v+=si.get_velocity(X, Y)[1]
    psi+=si.get_stream_function(X, Y)

sigma = 2.0    # strength of the source-sheet

# boundaries of the source-sheet
y_min, y_max = -1.0, 1.0


#cp = 1.0 - (u**2+v**2)/(Vinf.u**2+Vinf.v**2)

panels=flowOverCylinder(1.0,20)






plt.xlabel('x', fontsize=16)
plt.ylabel('y', fontsize=16)
plt.xlim(x_start, x_end)
plt.ylim(y_start, y_end)

wallX=[x_start, x_end]
wallY=[0. , 0.]
plt.plot(wallX,wallY,'--')


#plt.streamplot(X, Y, u, v, density=4.0, linewidth=1, arrowsize=2, arrowstyle='->')

plt.show()




