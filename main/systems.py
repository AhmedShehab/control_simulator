
from control.lti import zero
from django.http import response
import numpy as np
import control
import control.matlab as matlab

def bode_sys(sys):
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
    ndigits = 6
    omega = [round(num, ndigits) for num in omega]
    phase = [round(num, ndigits) for num in phase]
    mag = [round(num, ndigits) for num in mag]
    
    return omega, mag, phase

def margin_sys(sys):
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
    ndigits = 2
    gm = round(gm, ndigits)
    pm = round(pm, ndigits)
    wg = round(wg, ndigits)
    wp = round(wp, ndigits)

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
    ndigits = 6
    omega = [round(num, ndigits) for num in omega]
    phase = [round(num, ndigits) for num in phase]
    mag = [round(num, ndigits) for num in mag]
    
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
    ndigits = 2
    gm = round(gm, ndigits)
    pm = round(pm, ndigits)
    wg = round(wg, ndigits)
    wp = round(wp, ndigits)

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
    ndigits = 6
    omega = [round(num, ndigits) for num in omega]
    phase = [round(num, ndigits) for num in phase]
    mag = [round(num, ndigits) for num in mag]
    
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
    ndigits = 2
    gm = round(gm, ndigits)
    pm = round(pm, ndigits)
    wg = round(wg, ndigits)
    wp = round(wp, ndigits)

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

def step_pid(sys, final_time, setpoint, Kp, Ki, Kd):
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

def stepinfo_sys(sys):
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
    spec = matlab.stepinfo(Ts, SettlingTimeThreshold=0.02, RiseTimeLimits=(0.1, 0.9))
    
    return spec

def stepinfo_zpk(sys, z, p, k):
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
    spec = matlab.stepinfo(Ts, SettlingTimeThreshold=0.02, RiseTimeLimits=(0.1, 0.9))

    return spec

def stepinfo_pid(sys, Kp, Ki, Kd):
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

    # closed-loop unity-feedback transfer function
    Ts = control.feedback(DsGs, 1)
    spec = matlab.stepinfo(Ts, SettlingTimeThreshold=0.02, RiseTimeLimits=(0.1, 0.9))

    return spec

def model(sys):

    # check if sys is a transfer function
    if type(sys) == type(control.tf(1, 1)):
        # return num and den directly
        num = list(sys.num[0][0])
        den = list(sys.den[0][0])   

    if sys == 'cruise':
        num = None
        den = None
    
    elif sys == 'servo':
        num = 36
        den = [1, 3.6, 0]
    
    return num, den
def tf(sys):
    if sys == 'cruise':
        num = None
        den = None
    elif sys == 'servo':
        num = "1"
        den  = "s^2 + 3.6s"
    
    return num, den
def arrayToString(array):
    s=""
    for index,val in enumerate(array):
        i = len(array)-index-1
        if val !=0:
            if index>0 and i>=0:
                s+=" + "
            if val==1:
                if i==0:
                    s+=f"{val}"
                elif i==1:
                    s+=f"S"
                else:
                    s+=f"S^{i}"
            else:
                if i==0:
                    s+=f"{val}"
                elif i==1:
                    s+=f"{val}S"
                else:
                    s+=f"{val}S^{i}"
        i-=1
    return s
    
# Auto grading function for student submissions
def isPass(parameters, requirements):
    controller = parameters["Controller"]
    score= 0
    Pass="Pass"
    sim= parameters["Simulator"]
    if controller == "PID":
        p=parameters["P"]
        i=parameters["I"]
        d=parameters["D"]
        response= stepinfo_pid(sim,p,i,d)
    elif controller == "ZPK":
        z=parameters["Zero"]
        p=parameters["Pole"]
        k=parameters["Gain"]
        response= stepinfo_zpk(sim,z,p,k)
    errorPercent=(response["SteadyStateValue"]-parameters["StepInput"])*100
    if response["RiseTime"] >= 0.9 * requirements["RiseTime"] and response["RiseTime"] <= 1.1 * requirements["RiseTime"]:
        score+=1
    if response["SettlingTime"] >= 0.9 * requirements["SettlingTime"] and response["SettlingTime"] <= 1.1 * requirements["SettlingTime"]:
        score+=1
    if response["Overshoot"] >= 0.9 * requirements["Overshoot"] and response["Overshoot"] <= 1.1 * requirements["Overshoot"]:
        score+=1
    if errorPercent<= 1.1*requirements["SteadyStateError"]:
        score+=1
    if score >=2:
        Pass ="Pass"
    else:
        Pass="Fail"
    return score,Pass