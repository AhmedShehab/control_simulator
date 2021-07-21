import control
import control.matlab as matlab
import numpy as np
from control.lti import zero
from django.http import response
from scipy.integrate import odeint, solve_ivp

def bode_sys(sys):
    # open-loop system transfer function
    try:
        num, den = model(sys)
    except:
        # for error detection
        print("Err: system in not defined")
        return
    Gs = control.tf(num, den)

    # bode plot arrays
    omega = np.logspace(-2, 2, 2000)
    mag, phase, omega = control.bode(Gs, omega=omega)
    mag = 20 * np.log10(mag)  # mag in db
    phase = np.degrees(phase)  # phase in degrees

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
    # open-loop system transfer function
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
    # open-loop system transfer function
    try:
        num, den = model(sys)
    except:
        # for error detection
        print("Err: system in not defined")
        return
    Gs = control.tf(num, den)

    # define compensator transfer function
    # convert zero and pole to numpy arrays
    z = np.array([z])
    p = np.array([p])
    num, den = matlab.zpk2tf(z, p, k)
    Ds = matlab.tf(num, den)

    # Compensated open-loop transfer function
    DsGs = Ds*Gs

    # bode plot arrays
    omega = np.logspace(-2, 2, 2000)
    mag, phase, omega = control.bode(DsGs, omega=omega)
    mag = 20 * np.log10(mag)  # mag in db
    phase = np.degrees(phase)  # phase in degrees

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
    # open-loop system transfer function
    try:
        num, den = model(sys)
    except:
        # for error detection
        print("Err: system in not defined")
        return
    Gs = control.tf(num, den)

    # define compensator transfer function
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
    # open-loop system transfer function
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

    # bode plot arrays
    omega = np.logspace(-2, 2, 2000)
    mag, phase, omega = control.bode(DsGs, omega=omega)
    mag = 20 * np.log10(mag)  # mag in db
    phase = np.degrees(phase)  # phase in degrees

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
    # open-loop system transfer function
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
    # open-loop system transfer function
    try:
        num, den = model(sys)
    except:
        # for error detection
        print("Err: system in not defined")
        return
    Gs = control.tf(num, den)
    #print(Gs)
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
    # open-loop system transfer function
    try:
        num, den = model(sys)
    except:
        # for error detection
        print("Err: system in not defined")
        return
    Gs = control.tf(num, den)

    # define compensator transfer function
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
    # open-loop system transfer function
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

def step_cruise(final_time, setpoint):
    
    # Define engine lag
    def lag(p, t, u, extra):
        # inputs
        # u = power demand
        # p = output power
        # t = time
        extra = 0.0
        dp_dt = 2*(u - p)
        return dp_dt

    # Define car plant
    def vehicle(v, t, p, load):
        # inputs
        # v = behicle speed
        # t = time
        # p = power
        # load = cargo + passenger load

        # Car specifications and initialization data
        rho = 1.225       # kg/m3
        CdA = 0.55        # m2
        m = 1500          # kg

        # Calculate derivative of vehicle velocity
        dv_dt = (1.0/m) * (p*hp2watt/v - 0.5*CdA*rho*v**2)

        return dv_dt

    # Conversion factors
    hp2watt = 746
    mps2kmph = 3.6
    kmph2mps = 1/mps2kmph

    # simulation time parameters
    tf = final_time                           # final time for simulation
    nsteps = int(40* final_time)              # number of time steps
    t = np.linspace(0,tf,nsteps)              # linearly spaced time vector
    delta_t = t[1]                            # how long each step is
    v0_kmph = 1.0                             # car initial speed in km/h
    sp_kmph = setpoint                        # car final speed in km/h
    
    # simulate step input operation
    load = 0.0                                # passenger(s) and cargo load - in Kg
    v0 = v0_kmph*kmph2mps                     # car initial speed
    step = np.zeros(nsteps)
    sp = sp_kmph*kmph2mps
    step[0] = v0
    step[1:] = sp

    vt = np.zeros(nsteps)                     # for storing speed results - speed vector
    vt[0] = v0
    #et = np.zeros(nsteps)                    # error vector
    #ut = np.zeros(nsteps)                    # actuation vector
    #pt = np.zeros(nsteps)                    # power vector
    p0 = 0.0                                  # initial car power

    # Actuation limits - Car Physical limits
    max_power = 140
    min_power = -140

    # simulate with ODEINT
    for i in range(nsteps):
        error = step[i] - v0
        #et[i+1] = error
        u = error
        # clip input to -100% to 100%
        if u > max_power:
            u = max_power
        elif u < min_power:
            u = min_power
        #ut[i+1] = u
        p = odeint(lag, p0, [0,delta_t],args=(u,0))
        v = odeint(vehicle,v0,[0,delta_t],args=(p[-1], load))
        p0 = p[-1]
        v0 = v[-1]
        vt[i] = v0
        # pt[i] = p0

    # convert output to km/h
    vt_kmph = vt*mps2kmph
    t = list(t)
    output = list(vt_kmph)

    # round lists to 4 decimal digits
    ndigits = 4
    t = [round(num, ndigits) for num in t]
    output = [round(num, ndigits) for num in output]
    return t, output

def step_zpk_cruise(final_time, setpoint, z, p, k):
    
    # Define engine lag
    def lag(p, t, u, extra):
        # inputs
        # u = power demand
        # p = output power
        # t = time
        extra = 0.0
        dp_dt = 2*(u - p)
        return dp_dt

    # Define car plant
    def vehicle(v, t, p, load):
        # inputs
        # v = behicle speed
        # t = time
        # p = power
        # load = cargo + passenger load

        # Car specifications and initialization data
        rho = 1.225       # kg/m3
        CdA = 0.55        # m2
        m = 1500          # kg

        # Calculate derivative of vehicle velocity
        dv_dt = (1.0/m) * (p*hp2watt/v - 0.5*CdA*rho*v**2)

        return dv_dt

    # Conversion factors
    hp2watt = 746
    mps2kmph = 3.6
    kmph2mps = 1/mps2kmph

    # simulation time parameters
    tf = final_time                          # final time for simulation
    nsteps = int(40* final_time)             # number of time steps
    t = np.linspace(0,tf,nsteps)             # linearly spaced time vector
    delta_t = t[1]                           # how long each step is
    v0_kmph = 1.0                            # car initial speed in km/h
    sp_kmph = setpoint                       # car final speed in km/h

    # simulate step input operation
    load = 0.0                               # passenger(s) and cargo load - in Kg
    v0 = v0_kmph*kmph2mps                    # car initial speed
    step = np.zeros(nsteps)
    sp = sp_kmph*kmph2mps
    step[0] = v0
    step[1:] = sp
    vt = np.zeros(nsteps)                    # for storing speed results - speed vector
    vt[0] = v0
    et = np.zeros(1)                         # error value
    #ut = np.zeros(nsteps)                   # actuation vector
    #pt = np.zeros(nsteps)                   # power vector
    p0 = 0.0                                 # initial car power

    # Actuation limits - Car Physical limits
    max_power = 140
    min_power = -140

    # Controller TF
    z = np.array([z])
    p = np.array([p])
    num, den = matlab.zpk2tf(z, p, k)
    Ds = matlab.tf(num, den)

    # simulate with ODEINT
    for i in range(nsteps):
        error = step[i] - v0
        et[0] = error
        q = matlab.lsim(Ds, [0, et[0]], [0, t[i]])
        q = list(q[0])
        u = q[1]
        # clip input to -100% to 100%
        if u > max_power:
            u = max_power
        elif u < min_power:
            u = min_power
        # ut[i+1] = u
        p = odeint(lag, p0, [0,delta_t],args=(u,0))
        v = odeint(vehicle,v0,[0,delta_t],args=(p[-1], load))
        p0 = p[-1]
        v0 = v[-1]
        vt[i] = v0
        # pt[i+1] = p0

    # convert output to km/h
    vt_kmph = vt*mps2kmph
    t = list(t)
    output = list(vt_kmph)

    # round lists to 4 decimal digits
    ndigits = 4
    t = [round(num, ndigits) for num in t]
    output = [round(num, ndigits) for num in output]
    return t, output

def step_pid_cruise(final_time, setpoint, Kp, Ki, Kd):
    
    # Define engine lag
    def lag(p, t, u, extra):
        # inputs
        # u = power demand
        # p = output power
        # t = time
        extra = 0.0
        dp_dt = 2*(u - p)
        return dp_dt

    # Define car plant
    def vehicle(v, t, p, load):
        # inputs
        # v = behicle speed
        # t = time
        # p = power
        # load = cargo + passenger load

        # Car specifications and initialization data
        rho = 1.225       # kg/m3
        CdA = 0.55        # m2
        m = 1500          # kg

        # Calculate derivative of vehicle velocity
        dv_dt = (1.0/m) * (p*hp2watt/v - 0.5*CdA*rho*v**2)

        return dv_dt

    # Conversion factors
    hp2watt = 746
    mps2kmph = 3.6
    kmph2mps = 1/mps2kmph

    # simulation time parameters
    tf = final_time                         # final time for simulation
    nsteps = int(40* final_time)            # number of time steps
    t = np.linspace(0,tf,nsteps)            # linearly spaced time vector
    delta_t = t[1]                          # how long each step is
    v0_kmph = 1.0                           # car initial speed in km/h
    sp_kmph = setpoint                      # car final speed in km/h
    
    # simulate step input operation
    load = 0.0                              # passenger(s) and cargo load - in Kg
    v0 = v0_kmph*kmph2mps                   # car initial speed
    step = np.zeros(nsteps)
    sp = sp_kmph*kmph2mps
    step[0] = v0
    step[1:] = sp
    vt = np.zeros(nsteps)                   # for storing speed results - speed vector
    vt[0] = v0
    et = np.zeros(nsteps)                   # error vector
    #ut = np.zeros(nsteps)                  # actuation vector
    #pt = np.zeros(nsteps)                  # power vector
    p0 = 0.0                                # initial car power
    #iet = np.zeros(nsteps)                 # integral of error vector
    sum_int = 0.0                           # summation of error integral

    # Actuation limits - Car Physical limits
    max_power = 140
    min_power = -140

    # controller paramaters
    kp = Kp                                 # proportional gain
    kd = Kd                                 # derivative gain
    ki = Ki                                 # intergral gain

    # simulate with ODEINT
    for i in range(nsteps-1):
        error = step[i] - v0
        et[i+1] = error
        sum_int = sum_int + error * delta_t
        # clip integrator output to 2/3 of actuation capacity
        if sum_int > 0.67*max_power:
            sum_int = 0.67*max_power
        elif sum_int < 0.67*min_power:
            sum_int = 0.67*min_power
        derivative = (et[i+1] - et[i])/delta_t
        u = kp * error + kd * derivative + ki * sum_int
        # clip input to -100% to 100%
        if u > max_power:
            u = max_power
        elif u < min_power:
            u = min_power
        #ut[i+1] = u
        p = odeint(lag, p0, [0,delta_t],args=(u,0))
        v = odeint(vehicle,v0,[0,delta_t],args=(p[-1], load))
        p0 = p[-1]
        v0 = v[-1]
        vt[i+1] = v0
        # pt[i+1] = p0
        # iet[i+1] = sum_int

    # convert output to km/h
    vt_kmph = vt*mps2kmph
    t = list(t)
    output = list(vt_kmph)

    # round lists to 4 decimal digits
    ndigits = 4
    t = [round(num, ndigits) for num in t]
    output = [round(num, ndigits) for num in output]
    return t, output

def step_servo(final_time, setpoint):

    # Define Servomotor by Differential Equation 
    # 36/(s^2 + 3.6s)
    def servo(y, t, u, extra):
        extra = 0.0
        dy_dt = y[1]
        dy2_dt = 36*u - 3.6* y[1]
        return [dy_dt, dy2_dt]

    # simulation time parameters
    nsteps = int(final_time*40)                  # number of time steps
    t = np.linspace(0,final_time,nsteps)         # linearly spaced time vector
    delta_t = t[1]                               # how long each step is

    # simulate step input operation
    y0 = [0.0, 0.0]                              # servo initial degree
    step = np.zeros(nsteps)
    sp = setpoint                                # set point
    step[0] = 0.0
    step[1:] = sp
    yt = np.zeros(nsteps)                        # for storing degrees results - degrees vector
    yt[0] = y0[1]
    #et = np.zeros(nsteps)                       # error vector
    #ut = np.zeros(nsteps)                       # actuation vector

    # Actuation limits
    max_ac = 5
    min_ac = -5

    # simulate with ODEINT
    for i in range(nsteps):
        error = step[i] - y0[0]
        # et[i] = error
        u = error
        # clip input to -100% to 100%
        if u > max_ac:
            u = max_ac
        elif u < min_ac:
            u = min_ac
        #ut[i] = u
        y = odeint(servo, y0, [0,delta_t],args=(u,0))
        y0 = y[-1]
        yt[i] = y0[0]
    
    t = list(t)
    output = list(yt)

    # round lists to 4 decimal digits
    ndigits = 4
    t = [round(num, ndigits) for num in t]
    output = [round(num, ndigits) for num in output]
    return t, output

def step_zpk_servo(final_time, setpoint, z, p, k):

    # Define Servomotor by Differential Equation 
    # 36/(s^2 + 3.6s)
    def servo(y, t, u, extra):
        extra = 0.0
        dy_dt = y[1]
        dy2_dt = 36*u - 3.6* y[1]
        return [dy_dt, dy2_dt]

    # simulation time parameters
    nsteps = int(final_time*40)                  # number of time steps
    t = np.linspace(0,final_time,nsteps)         # linearly spaced time vector
    delta_t = t[1]                               # how long each step is

    # simulate step input operation
    y0 = [0.0, 0.0]                              # servo initial degree
    step = np.zeros(nsteps)
    sp = setpoint                                # set point
    step[0] = 0.0
    step[1:] = sp

    yt = np.zeros(nsteps)                        # for storing degrees results - degrees vector
    yt[0] = y0[1]
    et = np.zeros(1)                             # error value
    #ut = np.zeros(nsteps)                       # actuation vector

    # Controller TF
    z = np.array([z])
    p = np.array([p])
    num, den = matlab.zpk2tf(z, p, k)
    Ds = matlab.tf(num, den)

    # Actuation limits
    max_ac = 5
    min_ac = -5

    # simulate with ODEINT
    for i in range(nsteps):
        error = step[i] - y0[0]
        et[0] = error
        q = matlab.lsim(Ds, [0, et[0]], [0, t[i]])
        q = list(q[0])
        u = q[1]
        # clip input to -100% to 100%
        if u > max_ac:
            u = max_ac
        elif u < min_ac:
            u = min_ac
        # ut[i+1] = u
        y = odeint(servo, y0, [0,delta_t],args=(u,0))
        y0 = y[-1]
        yt[i] = y0[0]
    
    t = list(t)
    output = list(yt)

    # round lists to 4 decimal digits
    ndigits = 4
    t = [round(num, ndigits) for num in t]
    output = [round(num, ndigits) for num in output]
    return t, output

def step_pid_servo(final_time, setpoint, Kp, Ki, Kd):

    # Define Servomotor by Differential Equation 
    # 36/(s^2 + 3.6s)
    def servo(y, t, u, extra):
        extra = 0.0
        dy_dt = y[1]
        dy2_dt = 36*u - 3.6* y[1]
        return [dy_dt, dy2_dt]

    # simulation time parameters
    nsteps = int(final_time*40)                  # number of time steps
    t = np.linspace(0,final_time,nsteps)         # linearly spaced time vector
    delta_t = t[1]                               # how long each step is

    # simulate step input operation
    y0 = [0.0, 0.0]                              # servo initial degree
    step = np.zeros(nsteps)
    sp = setpoint                                # set point
    step[0] = 0.0
    step[1:] = sp
    yt = np.zeros(nsteps)                        # for storing degrees results - degrees vector
    yt[0] = y0[1]
    et = np.zeros(nsteps)                        # error vector
    #ut = np.zeros(nsteps)                       # actuation vector
    #iet = np.zeros(nsteps)                      # integral of error vector
    sum_int = 0.0
    Kp = Kp
    Ki = Ki
    Kd = Kd

    # Actuation limits
    max_ac = 5
    min_ac = -5

    # simulate with ODEINT
    for i in range(nsteps-1):
        error = step[i] - y0[0]
        et[i+1] = error
        sum_int = sum_int + error * delta_t
        # clip integrator output to 1/3 of actuation capacity
        if sum_int > 0.67*max_ac:
            sum_int = 0.67*max_ac
        elif sum_int < 0.67*min_ac:
            sum_int = 0.67*min_ac
        derivative = (et[i+1] - et[i])/delta_t
        u = Kp * error + Kd * derivative + Ki * sum_int
        # clip input to -100% to 100%
        if u > max_ac:
            u = max_ac
        elif u < min_ac:
            u = min_ac
        # ut[i+1] = u
        y = odeint(servo, y0, [0,delta_t],args=(u,0))
       
        y0 = y[-1]
        yt[i+1] = y0[0]
        # iet[i+1] = sum_int
    
    t = list(t)
    output = list(yt)

    # round lists to 4 decimal digits
    ndigits = 4
    t = [round(num, ndigits) for num in t]
    output = [round(num, ndigits) for num in output]
    return t, output

def action_sys(sys, final_time, setpoint):
    # open-loop system transfer function
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

    output, t = matlab.step(Ts, t)

    output = setpoint*output

    # calculate list of error
    setpoint_arr = setpoint * np.ones(nsteps)
    err = setpoint_arr - output

    # calculate control action
    action = err

    # covert numpy arrays to lists
    t = list(t)
    action = list(action)

    # round lists to 6 decimal digits
    ndigits = 6
    t = [round(num, ndigits) for num in t]
    action = [round(num, ndigits) for num in action]
    
    # calculate maximum control action
    max_action = max(action)
    min_action = min(action)
    return t, action, min_action, max_action


def action_pid(sys, final_time, setpoint, Kp, Ki, Kd):
    # open-loop system transfer function
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
    action = []
    sum = 0
    for i in range(len(err)):
        if i == 0:

            action.append(Kp*err[i] + Kd*(err[i]-0)/t[1])
        else:
            sum += t[1]*(err[i]+err[i-1])/2
            action.append(Kp*err[i] + Kd*(err[i]-err[i - 1])/t[1] + Ki * sum)

    # round lists to 6 decimal digits
    ndigits = 6
    t = [round(num, ndigits) for num in t]
    action = [round(num, ndigits) for num in action]

    # calculate maximum control action
    max_action = max(action)
    min_action = min(action)
    return t, action, min_action, max_action


def action_zpk(sys, final_time, setpoint, z, p, k):
    # open-loop system transfer function
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
        num = "36"
        den  = "s^2 + 3.6s"
    
    return num, den


def arrayToString(array):
    s = ""
    for index, val in enumerate(array):
        i = len(array)-index-1
        if val != 0:
            if index > 0 and i >= 0:
                s += " + "
            if val == 1:
                if i == 0:
                    s += f"{val}"
                elif i == 1:
                    s += f"s"
                else:
                    s += f"s^{i}"
            else:
                if i == 0:
                    s += f"{val}"
                elif i == 1:
                    s += f"{val}s"
                else:
                    s += f"{val}s^{i}"
        i -= 1
    return s


def format(num):
    mag = 0
    while abs(num) >= 1000:
        mag += 1
        num /= 1000.0
        if mag > 6 and num > 0:
            return "inf"
        elif mag > 6 and num < 0:
            return "-inf"
    return '%.2f%s' % (num, ['', 'K', "M", "G", "T", "P", "E"][mag])


# Auto grading function for student submissions
def isPass(parameters, requirements):
    controller = parameters["Controller"]
    score = 0
    Pass = "Pass"
    sim = parameters["Simulator"]
    if controller == "PID":
        p = parameters["P"]
        i = parameters["I"]
        d = parameters["D"]
        response = stepinfo_pid(sim, p, i, d, requirements['setPoint'])
    elif controller == "ZPK":
        z = parameters["Zero"]
        p = parameters["Pole"]
        k = parameters["Gain"]
        response = stepinfo_zpk(sim, z, p, k, requirements['setPoint'])
    errorPercent = (response["SteadyStateValue"]-parameters["StepInput"])*100
    print(errorPercent)
    if response["RiseTime"] >= 0.9 * requirements["RiseTime"] and response["RiseTime"] <= 1.1 * requirements["RiseTime"]:
        score += 1
        print(f"{score}: + 1")
    if response["SettlingTime"] >= 0.9 * requirements["SettlingTime"] and response["SettlingTime"] <= 1.1 * requirements["SettlingTime"]:
        score += 1
        print(f"{score}: + 2")
    if response["Overshoot"] >= 0.9 * requirements["Overshoot"] and response["Overshoot"] <= 1.1 * requirements["Overshoot"]:
        score += 1
        print(f"{score}: + 3")
    if errorPercent <= 1.1*requirements['SteadyStateError']:
        score += 1
        print(f"{score}: + 4")
    if score >= 2:
        Pass = "Pass"
    else:
        Pass = "Fail"
    return score, Pass


def stepinfo_pid(sys,p, i, d,setPoint):
    if sys == "cruise":
        t, output = step_pid_cruise(500, setPoint, p, i, d)
    else:
        return

    Peak = 0
    time10 = 0  # time at 10 percent of the steady state value
    time90 = 0  # time at 90 percent of the steady state value
    counter = 0  # counter to check for how long a value stays in a certain range
    for index, element in enumerate(output):
        # determining the Peak value
        if element >= Peak:
            Peak = element
            PeakTime = t[index]

        # determining the Time to reach 10% and 90% of the set point
        if time10 == 0:  # Make sure to take the first time sample
            if abs(element - (0.1 * setPoint)) <= 0.5:
                time10 = t[index]
        if time90 == 0:
            if abs(element - (0.9 * setPoint)) <= 0.5:
                time90 = t[index]

        # Determining the settling time
        if counter <= 500:  # Check if it stays for 10 samples in the same range
            if abs(element - setPoint) <= 0.02 * setPoint:
                # Make sure to get the first time it reaches the 98% range before it stays
                if counter == 0:
                    settlingTime = t[index]
                    counter += 1
                else:
                    counter += 1
            else:
                counter = 0

    # Determining the steady state Value
    if abs(output[-1] - setPoint) <= 0.001:
        SteadyStateValue = setPoint
    else:
        SteadyStateValue= output[-1]
    
    transientResponse = {
        'RiseTime': (time90 - time10),
        'Overshoot': (Peak - setPoint)*100/setPoint,
        'SettlingTime': settlingTime,
        'Peak': Peak,
        'PeakTime':PeakTime,
        'SteadyStateValue': SteadyStateValue,
    }

    return transientResponse


def stepinfo_zpk(sys,z, p, k,setPoint):
    if sys == "cruise":
        t, output = step_zpk_cruise(500, setPoint, z,p,k)
    else:
        return

    Peak = 0
    time10 = 0  # time at 10 percent of the steady state value
    time90 = 0  # time at 90 percent of the steady state value
    counter = 0  # counter to check for how long a value stays in a certain range
    for index, element in enumerate(output):
        # determining the Peak value
        if element >= Peak:
            Peak = element
            PeakTime = t[index]

        # determining the Time to reach 10% and 90% of the set point
        if time10 == 0:  # Make sure to take the first time sample
            if abs(element - (0.1 * setPoint)) <= 0.5:
                time10 = t[index]
        if time90 == 0:
            if abs(element - (0.9 * setPoint)) <= 0.5:
                time90 = t[index]

        # Determining the settling time
        if counter <= 500:  # Check if it stays for 10 samples in the same range
            if abs(element - setPoint) <= 0.02 * setPoint:
                # Make sure to get the first time it reaches the 98% range before it stays
                if counter == 0:
                    settlingTime = t[index]
                    counter += 1
                else:
                    counter += 1
            else:
                counter = 0

    # Determining the steady state Value
    if abs(output[-1] - setPoint) <= 0.001:
        SteadyStateValue = setPoint
    else:
        SteadyStateValue= output[-1]
    
    transientResponse = {
        'RiseTime': (time90 - time10),
        'Overshoot': (Peak - setPoint)*100/setPoint,
        'SettlingTime': settlingTime,
        'Peak': Peak,
        'PeakTime':PeakTime,
        'SteadyStateValue': SteadyStateValue,
    }

    return transientResponse
