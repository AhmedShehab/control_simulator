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

    ## bode plot arrays
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
    ## open-loop system transfer function
    try:
        num, den = model(sys)
    except:
        # for error detection
        print("Err: system in not defined")
        return
    Gs = control.tf(num, den)
    
    # phase & gain margins
    gm, pm, wg, wp = control.margin(Gs)

    # round phase & gain margin variables
    no_digits = 2
    gm = round(gm, no_digits)
    pm = round(pm, no_digits)
    wg = round(wg, no_digits)
    wp = round(wp, no_digits)

    return gm, pm, wg, wp


def bode_zpk(sys, z, p, k):
    ## open-loop system transfer function
    try:
        num, den = model(sys)
    except:
        # for error detection
        print("Err: system in not defined")
        return
    Gs = control.tf(num, den)

    ## define compensator transfer function
    # convert zero and pole to numpy arrays
    z = np.array([z])
    p = np.array([p])
    num, den = matlab.zpk2tf(z, p, k)
    Ds = matlab.tf(num, den)

    # Compensated open-loop transfer function
    DsGs = Ds*Gs

    ## bode plot arrays
    omega = np.logspace(-2,2,2000)
    mag, phase, omega = control.bode(DsGs, omega=omega)
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

def margin_zpk(sys, z, p, k):
    ## open-loop system transfer function
    try:
        num, den = model(sys)
    except:
        # for error detection
        print("Err: system in not defined")
        return
    Gs = control.tf(num, den)

    ## define compensator transfer function
    # convert zero and pole to numpy arrays
    z = np.array([z])
    p = np.array([p])
    num, den = matlab.zpk2tf(z, p, k)
    Ds = matlab.tf(num, den)

    # Compensated open-loop transfer function
    DsGs = Ds*Gs

    # phase & gain margins
    gm, pm, wg, wp = control.margin(DsGs)

    # round phase & gain margin variables
    no_digits = 2
    gm = round(gm, no_digits)
    pm = round(pm, no_digits)
    wg = round(wg, no_digits)
    wp = round(wp, no_digits)

    return gm, pm, wg, wp


def bode_pid(sys, Kp, Ki, Kd):
    ## open-loop system transfer function
    try:
        num, den = model(sys)
    except:
        # for error detection
        print("Err: system in not defined")
        return
    Gs = control.tf(num, den)

    # PID Controller
    s = matlab.tf('s')
    Ds = Kp + Ki/s + Kd*s

    # Compensated open-loop transfer function
    DsGs = Ds*Gs

    ## bode plot arrays
    omega = np.logspace(-2,2,2000)
    mag, phase, omega = control.bode(DsGs, omega=omega)
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


def margin_pid(sys, Kp, Ki, Kd):
    ## open-loop system transfer function
    try:
        num, den = model(sys)
    except:
        # for error detection
        print("Err: system in not defined")
        return
    Gs = control.tf(num, den)

    # PID Controller
    s = matlab.tf('s')
    Ds = Kp + Ki/s + Kd*s

    # Compensated open-loop transfer function
    DsGs = Ds*Gs

    # phase & gain margins
    gm, pm, wg, wp = control.margin(DsGs)

    # round phase & gain margin variables
    no_digits = 2
    gm = round(gm, no_digits)
    pm = round(pm, no_digits)
    wg = round(wg, no_digits)
    wp = round(wp, no_digits)

    return gm, pm, wg, wp

def step_sys(sys, final_time, setpoint):
    ## open-loop system transfer function
    try:
        num, den = model(sys)
    except:
        # for error detection
        print("Err: system in not defined")
        return
    Gs = control.tf(num, den)
    
    # closed-loop unity-feedback transfer function
    Ts = control.feedback(Gs, 1)

    # simulation time parameters
    initial_time = 0
    nsteps = 2000   # number of time steps
    t = np.linspace(initial_time, final_time, nsteps)
    output, t = matlab.step(Ts, t)
    output = setpoint*output

    # covert numpy arrays to lists
    t = list(t)
    output = list(output)

    # round lists to 5 decimal digits
    ndigits = 6
    t = [round(num, ndigits) for num in t]
    output = [round(num, ndigits) for num in output]

    return t, output

def step_zpk(sys, final_time, setpoint, z, p, k):
    ## open-loop system transfer function
    try:
        num, den = model(sys)
    except:
        # for error detection
        print("Err: system in not defined")
        return
    Gs = control.tf(num, den)
    
    ## define compensator transfer function
    # convert zero and pole to numpy arrays
    z = np.array([z])
    p = np.array([p])
    num, den = matlab.zpk2tf(z, p, k)
    Ds = matlab.tf(num, den)

    # Compensated open-loop transfer function
    DsGs = Ds*Gs

    # closed-loop unity-feedback transfer function
    Ts = control.feedback(DsGs, 1)

    # simulation time parameters
    initial_time = 0
    nsteps = 2000   # number of time steps
    t = np.linspace(initial_time, final_time, nsteps)
    output, t = matlab.step(Ts, t)
    output = setpoint*output

    # covert numpy arrays to lists
    t = list(t)
    output = list(output)

    # round lists to 5 decimal digits
    ndigits = 6
    t = [round(num, ndigits) for num in t]
    output = [round(num, ndigits) for num in output]

    return t, output

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