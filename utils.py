import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import ode
from numpy import sin, cos

def ode45(f, y0, tspan, options=None):
    X,Y = [], []
    
    def solout(t_i,y_i): 
        X.append(t_i)
        Y.append(y_i)
        
    if type(tspan) == float:
        T = np.linspace(0, tspan)
    elif len(tspan)==2:
        T = np.linspace(*tspan)
    elif len(tspan) ==3:
        T = np.arange(*tspan)
    else:
        print "tspan can be tf, (t0,tf), or (t0,tf,dt)"
        return
    
    if options is not None:
        r = ode(f).set_integrator('dopri5', options)
    else:
        r = ode(f).set_integrator('dopri5')
    r.set_solout(solout)
    r.set_initial_value(y0, T[0])

    for t in T[1:]:
        if r.successful():
            solout(t, r.integrate(t, True))
        else:
            print "not successful ", t

    return np.array(X), np.array(Y)



