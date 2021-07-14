import control
import control.matlab as matlab
import numpy as np
from control.lti import zero
from django.http import response


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
    
    # round lists to 6 decimal floating digits
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
    
    # round lists to 6 decimal floating digits
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
    
    # round lists to 6 decimal floating digits
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
    nsteps = 40 * final_time   # number of time steps
    t = np.linspace(initial_time, final_time, round(nsteps))
    output, t = matlab.step(Ts, t)
    output = setpoint*output

    # covert numpy arrays to lists
    t = list(t)
    output = list(output)

    # round lists to 6 decimal digits
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
    nsteps = 40 * final_time   # number of time steps
    t = np.linspace(initial_time, final_time, round(nsteps))
    output, t = matlab.step(Ts, t)
    output = setpoint*output

    # covert numpy arrays to lists
    t = list(t)
    output = list(output)

    # round lists to 6 decimal digits
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
    nsteps = 40 * final_time     # number of time steps
    t = np.linspace(initial_time, final_time, round(nsteps))
    output, t = matlab.step(Ts, t)
    output = setpoint*output

    # covert numpy arrays to lists
    t = list(t)
    output = list(output)

    # round lists to 6 decimal digits
    ndigits = 6
    t = [round(num, ndigits) for num in t]
    output = [round(num, ndigits) for num in output]

    return t, output

def action_sys(sys, final_time, setpoint):
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
    nsteps = 40 * int(final_time)   # number of time steps
    t = np.linspace(initial_time, final_time, round(nsteps))
    print(t)
    print("====")
    output, t = matlab.step(Ts, t)
    print(t)
    print("****")
    output = setpoint*output

    # calculate list of error
    setpoint_arr = setpoint * np.ones(nsteps)
    err = setpoint_arr - output
    
    # calculate control action
    action = err

    # covert numpy arrays to lists
    t = list(t)
    print(t)
    print("&&&")
    action = list(action)

    # round lists to 6 decimal digits
    ndigits = 6
    t = [round(num, ndigits) for num in t]
    action = [round(num, ndigits) for num in action]
    print(t)
    print("$$$$")
    # calculate maximum control action
    max_action = max(action)
    min_action = min(action)
    return t, action, min_action, max_action

def action_pid(sys, final_time, setpoint, Kp, Ki, Kd):
    ## open-loop system transfer function
    try:
        num, den = model(sys)
    except:
        # for error detection
        print("Err: system in not defined")
        return
    Gs = control.tf(num, den)
    s = matlab.tf('s')
    Ds = Kp + Ki/s + Kd*s
 
    # closed-loop unity-feedback transfer function
    Ts = control.feedback(Ds*Gs, 1)

    # simulation time parameters
    initial_time = 0
    nsteps = 40 * int(final_time)   # number of time steps
    t = np.linspace(initial_time, final_time, round(nsteps))

    output, t = matlab.step(Ts, t)
    output = setpoint*output

    # calculate list of error
    setpoint_arr = setpoint * np.ones(nsteps)
    err = setpoint_arr - output
    action= []
    sum = 0
    for i in range(len(err)):
        if i == 0:
        
            action.append(Kp*err[i] +Kd*(err[i]-0)/t[1] )   
        else:
            sum += t[1]*(err[i]+err[i-1])/2 
            action.append(Kp*err[i] +Kd*(err[i]-err[i- 1])/t[1] +Ki* sum)

    # round lists to 6 decimal digits
    ndigits = 6
    t = [round(num, ndigits) for num in t]
    action = [round(num, ndigits) for num in action]
  
    # calculate maximum control action
    max_action = max(action)
    min_action = min(action)
    return t, action, min_action, max_action

def action_zpk(sys, final_time, setpoint, z, p, k):
    ## open-loop system transfer function
    try:
        num, den = model(sys)
    except:
        # for error detection
        print("Err: system in not defined")
        return
    Gs = control.tf(num, den)
    z = np.array([z])
    p = np.array([p])
    num, den = matlab.zpk2tf(z, p, k)
    Ds = matlab.tf(num, den)
    # closed-loop unity-feedback transfer function
    Ts = control.feedback(Ds*Gs, 1)

    # simulation time parameters
    initial_time = 0
    nsteps = 40 * int(final_time)   # number of time steps
    t = np.linspace(initial_time, final_time, round(nsteps))

    output, t = matlab.step(Ts, t)
    output = setpoint*output
 
    # calculate list of error
    setpoint_arr = setpoint * np.ones(nsteps)
    err = setpoint_arr - output
    
    # calculate control action
    action = matlab.lsim(Ds, err, t)

    # covert numpy arrays to lists
    t = list(t)
    action = list(action[0])

    # round lists to 6 decimal digits
    ndigits = 6
    t = [round(num, ndigits) for num in t]
    action = [round(num, ndigits) for num in action]

    # calculate maximum control action
    max_action = max(action)
    min_action = min(action)
    return t, action, min_action, max_action

def stepinfo_sys(sys,setPoint):
    ## open-loop system transfer function
    try:
        num, den = model(sys)
    except:
        # for error detection
        print("Err: system in not defined")
        return
    Gs = control.tf(num, den)
    
    # closed-loop unity-feedback transfer function
    Ts = control.feedback(Gs, 1) * setPoint
    try:
        spec = matlab.stepinfo(Ts, SettlingTimeThreshold=0.02, RiseTimeLimits=(0.1, 0.9))
    except:
        spec = "Unstable response"
    
    return spec

def stepinfo_zpk(sys, z, p, k,setPoint):
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
    Ts = control.feedback(DsGs, 1) * setPoint
    try:
        spec = matlab.stepinfo(Ts, SettlingTimeThreshold=0.02, RiseTimeLimits=(0.1, 0.9))
    except:
        spec = "Unstable response"

    return spec

def stepinfo_pid(sys, Kp, Ki, Kd,setPoint):
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
    Ts = control.feedback(DsGs, 1) * setPoint
    try:
        spec = matlab.stepinfo(Ts, SettlingTimeThreshold=0.02, RiseTimeLimits=(0.1, 0.9))
    except:
        spec = "Unstable response"

    return spec

def model(sys):

    # check if sys is a transfer function
    if type(sys) == type(control.tf(1, 1)):
        # return num and den directly
        num = list(sys.num[0][0])
        den = list(sys.den[0][0])   

    if sys == 'cruise':
        num = 0.02107
        den = [0.5, 1.003, 0.00584]
    
    elif sys == 'servo':
        num = 36
        den = [1, 3.6, 0]
    
    return num, den
    
def tf(sys):
    if sys == 'cruise':
        num = "0.02107"
        den = "0.5s^2 + 1.003s + 0.00584"
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
                    s+=f"s"
                else:
                    s+=f"s^{i}"
            else:
                if i==0:
                    s+=f"{val}"
                elif i==1:
                    s+=f"{val}s"
                else:
                    s+=f"{val}s^{i}"
        i-=1
    return s

def format(num):
    mag = 0
    while abs(num)>=1000:
        mag += 1
        num /= 1000.0
        if mag > 6 and num > 0:
            return "inf"
        elif mag > 6 and num < 0:
            return "-inf"
    return '%.2f%s' % (num, ['', 'K', "M", "G", "T","P","E"][mag])
    
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
