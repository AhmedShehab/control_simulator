def control():
    import numpy as np
    import control.matlab as control
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
    mag, phase, omega = control.bode(Gs)
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
    num, den = control.zpk2tf(z, p, k)
    Ds = control.tf(num, den)
    print(Ds)

    # Draw the open-loop frequency resp. for the comp. sys
    DsGs = Ds*Gs
    gm, pm, wg, wp = control.margin(DsGs)
    print(f"Gain margin = {gm} dB")
    print(f"Phase margin = {round(pm, 2)} degrees")
    print(f"Frequency for Gain Margin = {wg} radians/sec")
    print(f"Frequecny for Phase Margin = {wp} radians/sec")
    mag_comp, phase_comp, omega_comp = control.bode(Gs, DsGs)
    return Gs, mag_comp, phase_comp, omega_comp, mag, phase, omega