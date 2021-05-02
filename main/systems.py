import numpy as np
import control
import control.matlab as matlab

def bode_Gs(sys):
    ## open-loop system transfer function
    try:
        num, den = model(sys)
    except:
        # for error detection
        print("Err: system in not defined")
        return
    Gs = control.tf(num, den)

    ## bode plot lists
    omega = np.logspace(-2,2,2000)
    mag, phase, omega = control.bode(Gs, omega=omega)
    mag = 20 * np.log10(mag) # mag in db
    phase= np.degrees(phase) # phase in degrees

    # convert numpy arrays to lists    
    omega = list(omega)
    phase = list(phase)
    mag = list(mag)
    
    # round lists to 5 decimal floating digits
    no_digits = 5
    omega = [round(num, no_digits) for num in omega]
    phase = [round(num, no_digits) for num in phase]
    mag = [round(num, no_digits) for num in mag]
    
    return omega, mag, phase

def margin_Gs(sys):
    return

def bode_zpk(sys, z, p, k):
    return

def bode_pid(sys, p, i, d):
    return

def step_zpk(sys, z, p, k):
    return

def step_pid(sys, p, i, d):
    return

def stepinfo_Gs(sys):
    return

def stepinfo_zpk(sys, z, p, k):
    return

def stepinfo_pid(sys, p, i, d):
    return

def model(sys):
    if sys == 'cruise':
        num = None
        den = None

    elif sys == 'servo':
        num = 36
        den = [1, 3.6, 0]

    return num, den