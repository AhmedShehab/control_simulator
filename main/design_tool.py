def control():
    import numpy as np
    import control
    import control.matlab as matlab
    import sys

    # Define plant transfer function
    Gs = control.tf(36, [1, 3.6, 0])
    print(Gs)

    # Draw open-loop frequency response for the planet
    gm, pm, wg, wp = control.margin(Gs)
    print(f"Gain margin = {gm} dB")
    print(f"Phase margin = {round(pm, 2)} degrees")
    print(f"Frequency for Gain Margin = {wg} radians/sec")
    print(f"Frequecny for Phase Margin = {wp} radians/sec")
    omega = np.logspace(-3,3,2000)
    mag, phase, omega = control.bode(Gs, omega=omega)
    print(mag.shape)
    print(phase.shape)
    print(omega.shape)
    mag = 20 * np.log10(mag)
    phase= np.degrees(phase)
    omega = omega.T
    phase = phase.T
    mag = mag.T

    omega= list(omega)
    phase= list(phase)
    mag= list(mag)

    #mag = 20*np.log(mag,10)


    # Compensator in zpk form
    z = [-0.2]
    p = [-0.0336]
    k = 0.2285

    # Define Compensator transfer function
    num, den = matlab.zpk2tf(z, p, k)
    Ds = matlab.tf(num, den)
    print(Ds)

    # Draw the open-loop frequency resp. for the comp. sys
    DsGs = Ds*Gs
    gm, pm, wg, wp = control.margin(DsGs)
    print(f"Gain margin = {gm} dB")
    print(f"Phase margin = {round(pm, 2)} degrees")
    print(f"Frequency for Gain Margin = {wg} radians/sec")
    print(f"Frequecny for Phase Margin = {wp} radians/sec")
    omega_comp = np.logspace(-3,3,2000)
    mag_comp, phase_comp, omega_comp = control.bode(DsGs, omega=omega_comp)
    mag_comp = 20 * np.log10(mag_comp)
    phase_comp = np.degrees(phase_comp)
    omega_comp = omega_comp
    phase_comp = phase_comp.T
    mag_comp = mag_comp.T

    omega_comp = list(omega_comp)
    phase_comp = list(phase_comp)
    mag_comp = list(mag_comp)

    return  Gs, mag_comp, phase_comp, omega_comp, mag, phase, omega 
