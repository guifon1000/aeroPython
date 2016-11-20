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
        self.u_inf=Vinf*np.cos(self.alpha)
        self.v_inf=Vinf*np.sin(self.alpha)

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





class Particule:
    def __init__(self,x=10000.,y=10000.,omega=0.,t=0.):
        self.x = x
        self.y = y
        self.omega = omega
        self.t = t
    def influence(self,x,y):
        d = np.sqrt((self.x-x)**2.+(self.y-y)**2.)
        vec = [-self.x + x,-self.y-y]
        if d ==0.:
            F=[0.,0.]
        else :
            fac = self.omega / (2 * np.pi *d**2.)
            F =  [-vec[1]*fac,vec[0]*fac]
        return F
    
    
    
def particuleVelocity(part,x,y):
    for (i,p) in enumerate(part):
        return [p.influence(x,y)[0],p.influence(x,y)[1]]


def profile(name):
    alp = 0.
    f = open(name,'r').readlines()
    plt.clf()
    x_ends=[]
    y_ends=[]
    for l in f[1:]:
        xloc = float(l.split()[0])
        yloc = float(l.split()[1])

        x_ends.append(xloc*(np.cos(alp))+yloc*np.sin(alp))
        y_ends.append(-xloc*(np.sin(alp))+yloc*np.cos(alp))
    teex = [x_ends[0],y_ends[0]]
    tein = [x_ends[-1],y_ends[-1]]
    teed=[0.5*(teex[0]+tein[0]),0.5*(teex[1]+tein[1])]
    leed = [x_ends[(len(x_ends)-1)/2],y_ends[(len(x_ends)-1)/2]]
    plt.plot(x_ends,y_ends)
    plt.axis('equal')
    #plt.show()
    plt.clf()
    u_inf=1.0  

    N_panels=len(x_ends)-1
    # radius
    # defining the end-points of the panel# defining the panels
    panels = np.empty(N_panels, dtype=object)
    for i in xrange(N_panels):
        panels[i] = Panel(x_ends[i], y_ends[i], x_ends[i+1], y_ends[i+1])
   

    # looking for the trailing edge vortex intensity
    gamma0 = -1



    plt.grid(True)
    Vinf=freeStream(1.0,0.)
    tab = []
    tab.append(vortex(gamma0,teed[0],teed[1]))

    A = build_matrix(panels)            # computes the singularity matrix
    b = build_rhs(panels, Vinf) # computes the freestream RHS

    # solves the linear system
    sigma = np.linalg.solve(A, b)

    for i, panel in enumerate(panels):
        panel.sigma = sigma[i]
    # defines a mesh grid
    Nx, Ny = 10, 10              # number of points in the x and y directions
    val_x, val_y = 0.,0.
    x_min, x_max = min( panel.xa for panel in panels ), max( panel.xa for panel in panels )
    y_min, y_max = min( panel.ya for panel in panels ), max( panel.ya for panel in panels )
    x_start, x_end = x_min-val_x*(x_max-x_min), x_max+val_x*(x_max-x_min)
    y_start, y_end = y_min-val_y*(y_max-y_min), y_max+val_y*(y_max-y_min)
    x_start, x_end = -0.5,1.5
    y_start, y_end = -1.,1.

    X, Y = np.meshgrid(np.linspace(x_start, x_end, Nx), np.linspace(y_start, y_end, Ny))

    # computes the velicity field on the mesh grid
    u, v = get_velocity_field(panels, Vinf, X, Y)
    # plots the velocity field

    dt =0.1
    teta = 0.
    f = 5
    facR = 1.1
    part = [] 
    dpart = [] 
    for it in range(1):
        for p in part:
            Up = particuleVelocity(part,p.x,p.y)
            p.x+=(Up[0]+Vinf.u_inf)*dt
            p.y+=(Up[1]+Vinf.v_inf)*dt
        vte = vortex(gamma0,teed[0],teed[1])
        uvort=vte.get_velocity(X,Y)
        R=1.0
        particule  = Particule(x=teed[0],y=teed[1],omega = 10.*teta,t=it*dt)
        part.append(particule)
        plt.clf()
        size=10
        plt.figure(figsize=(size, (y_end-y_start)/(x_end-x_start)*size))
        print it
        teta = (np.pi/4)*np.cos(f*float(it)*dt)
        plt.xlabel('x', fontsize=16)
        plt.ylabel('y', fontsize=16)
        for p in part:
            plt.scatter(p.x,p.y)
        plt.streamplot(X, Y, uvort[0]+u, uvort[1]+v, density=5, linewidth=1, arrowsize=1, arrowstyle='->')
        plt.plot(x_ends, y_ends, color='b', linestyle='-', linewidth=1)
        #plt.fill([panel.xc for panel in panels], 
         #[panel.yc for panel in panels], 
         #color='k', linestyle='solid', linewidth=2, zorder=2)
        plt.xlim(1.5*x_start, 1.5*x_end)
        plt.ylim(1.5*y_start,1.5*y_end)
        #plt.ylim(y_start, y_end)
        plt.savefig('img_'+str(it)+'.png')
        plt.clf()
    return panels




def kutta_condition(A_source, B_vortex):
    """Builds the Kutta condition array.
    
    Parameters
    ----------
    A_source: Numpy 2d array (float)
        Source contribution matrix for the normal velocity.
    B_vortex: Numpy 2d array (float)
        Vortex contribution matrix for the normal velocity.
    
    Returns
    -------
    b: Numpy 1d array (float)
        The left hand-side of the Kutta-condition equation.
    """
    b = numpy.empty(A_source.shape[0]+1, dtype=float)
    # matrix of source contribution on tangential velocity
    # is the same than
    # matrix of vortex contribution on normal velocity
    b[:-1] = B_vortex[0, :] + B_vortex[-1, :]
    # matrix of vortex contribution on tangential velocity
    # is the opposite of
    # matrix of source contribution on normal velocity
    b[-1] = - numpy.sum(A_source[0, :] + A_source[-1, :])
    return b

def build_singularity_matrix(A_source, B_vortex):
    """Builds the left hand-side matrix of the system
    arising from source and vortex contributions.
    
    Parameters
    ----------
    A_source: Numpy 2d array (float)
        Source contribution matrix for the normal velocity.
    B_vortex: Numpy 2d array (float)
        Vortex contribution matrix for the normal velocity.
    
    Returns
    -------
    A:  Numpy 2d array (float)
        Matrix of the linear system.
    """
    A = numpy.empty((A_source.shape[0]+1, A_source.shape[1]+1), dtype=float)
    # source contribution matrix
    A[:-1, :-1] = A_source
    # vortex contribution array
    A[:-1, -1] = numpy.sum(B_vortex, axis=1)
    # Kutta condition array
    A[-1, :] = kutta_condition(A_source, B_vortex)
    return A

def vortex_contribution_normal(panels):
    """Builds the vortex contribution matrix for the normal velocity.
    
    Parameters
    ----------
    panels: Numpy 1d array (Panel object)
        List of panels.
    
    Returns
    -------
    A: Numpy 2d array (float)
        Vortex contribution matrix.
    """
    A = np.empty((panels.size, panels.size), dtype=float)
    # vortex contribution on a panel from itself
    np.fill_diagonal(A, 0.0)
    # vortex contribution on a panel from others
    for i, panel_i in enumerate(panels):
        for j, panel_j in enumerate(panels):
            if i != j:
                A[i, j] = -0.5/np.pi*integral(panel_i.xc, panel_i.yc, 
                                                 panel_j,
                                                 np.sin(panel_i.beta),
                                                 -np.cos(panel_i.beta))
    return A









def source_contribution_normal(panels):
    """Builds the source contribution matrix for the normal velocity.
    
    Parameters
    ----------
    panels: Numpy 1d array (Panel object)
        List of panels.
    
    Returns
    -------
    A: Numpy 2d array (float)
        Source contribution matrix.
    """
    A = np.empty((panels.size, panels.size), dtype=float)
    # source contribution on a panel from itself
    np.fill_diagonal(A, 0.5)
    # source contribution on a panel from others
    for i, panel_i in enumerate(panels):
        for j, panel_j in enumerate(panels):
            if i != j:
                A[i, j] = 0.5/np.pi*integral(panel_i.xc, panel_i.yc, 
                                                panel_j,
                                                np.cos(panel_i.beta),
                                                np.sin(panel_i.beta))
    return A



def get_velocity_field(panels, freestream, X, Y):
    """Returns the velocity field.
    
    Arguments
    ---------
    panels -- array of panels.
    freestream -- farfield conditions.
    X, Y -- mesh grid.
    """
    Nx, Ny = X.shape
    u, v = np.empty((Nx, Ny), dtype=float), np.empty((Nx, Ny), dtype=float)
    
    for i in range(Nx):
        for j in range(Ny):
            u[i,j] = freestream.u_inf*math.cos(freestream.alpha)\
                     + 0.5/math.pi*sum([p.sigma*integral(X[i,j], Y[i,j], p, 1, 0) for p in panels])
            v[i,j] = freestream.u_inf*math.sin(freestream.alpha)\
                     + 0.5/math.pi*sum([p.sigma*integral(X[i,j], Y[i,j], p, 0, 1) for p in panels])
    
    return u, v
     

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

def integral(x, y, panel, dxdz, dydz):
    """Evaluates the contribution of a panel at one point.
    
    Arguments
    ---------
    x, y -- Cartesian coordinates of the point.
    panel -- panel which contribution is evaluated.
    dxdz -- derivative of x in the z-direction.
    dydz -- derivative of y in the z-direction.
    
    Returns
    -------
    Integral over the panel of the influence at one point.
    """
    def func(s):
        return ( ((x - (panel.xa - math.sin(panel.beta)*s))*dxdz
                  +(y - (panel.ya + math.cos(panel.beta)*s))*dydz)
                / ((x - (panel.xa - math.sin(panel.beta)*s))**2
                   +(y - (panel.ya + math.cos(panel.beta)*s))**2) )
    return integrate.quad(lambda s:func(s), 0., panel.length)[0]


def build_matrix(panels):
    """Builds the source matrix.
    
    Arguments
    ---------
    panels -- array of panels.
    
    Returns
    -------
    A -- NxN matrix (N is the number of panels).
    """
    N = len(panels)
    A = np.empty((N, N), dtype=float)
    np.fill_diagonal(A, 0.5)
    
    for i, p_i in enumerate(panels):
        for j, p_j in enumerate(panels):
            if i != j:
                A[i,j] = 0.5/math.pi*integral(p_i.xc, p_i.yc, p_j, math.cos(p_i.beta), math.sin(p_i.beta))
    
    return A




def build_rhs(panels, freestream , tab=None,alp=0.):
    """Builds the RHS of the linear system.
    
    Arguments
    ---------
    panels -- array of panels.
    freestream -- farfield conditions.
    
    Returns
    -------
    b -- 1D array ((N+1)x1, N is the number of panels).
    """
    b = np.empty(len(panels), dtype=float)
    
    for i, panel in enumerate(panels):
        b[i] = -freestream.u_inf * math.cos(freestream.alpha - panel.beta)
    if tab != None:
        b = np.empty(len(panels), dtype=float)
        for i, panel in enumerate(panels):
            u=[0.,0.]
            for t in tab:
                uadd = t.get_velocity(panel.xc,panel.yc)
                u[0]=uadd[0]
                u[1]=uadd[1]
            unorm = np.sqrt(u[0]**2.+u[1]**2.)
            b[i] = (unorm -freestream.u_inf)* math.cos(alp - panel.beta)
    return b



profile('NACAcamber0012.dat')
