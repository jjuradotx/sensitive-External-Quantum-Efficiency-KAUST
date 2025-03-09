import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy import interpolate, integrate
from scipy.integrate import cumtrapz, simps
import warnings

# Suppress warnings
warnings.filterwarnings('ignore')

# Constants
k = 1.38064852e-23  # Boltzmann constant (m^2 kg s^-2 K^-1)
h = 6.62607004e-34   # Planck constant (m^2 kg s^-1)
c = 2.99792458e8     # Speed of light (m/s)
eV = 1.6021766208e-19  # Electron volt (J)
q = 1.6021766208e-19  # Elementary charge (C)

# Load EQE data
EQE_data = pd.read_csv(r"C:\Users\José\OneDrive\Documents\KAUST\Post Doc\Colabs\Anirudh\Exported EQEpv\Sample9Pixel5.csv")
EQE_data.columns = ['WAVELENGTH', 'EQE']
EQE_data = EQE_data.astype(float)

# Load AM 1.5 Data
AM_data = pd.read_csv(r"C:\Users\José\iCloudDrive\Documents\KAUST\Post Doc\sEQE\AM1.5G.csv", sep=';')
AM_data['WAVELENGTH1'] = pd.to_numeric(AM_data['Wavelength (nm)'].str.replace(',', '.'))
AM_data['AM 1.5 G'] = pd.to_numeric(AM_data['Global tilt  W*m-2*nm-1'].str.replace(',', '.'))
AM_data = AM_data[['WAVELENGTH1', 'AM 1.5 G']].astype(float)

# Interpolate EQE data to match AM 1.5 wavelengths
interp_eqe = interpolate.interp1d(EQE_data.WAVELENGTH, EQE_data.EQE, bounds_error=False, fill_value=0)
AM_data['EQE_interp'] = interp_eqe(AM_data.WAVELENGTH1)

# Compute energy and photon flux
AM_data['Energy'] = 1240 / AM_data.WAVELENGTH1
AM_data['PF'] = AM_data['AM 1.5 G'] / AM_data['Energy']
AM_data['EQE*PF'] = AM_data['EQE_interp'] * AM_data['PF'] * 0.001

# Ideal EQE model
AM_data['Ideal_EQE'] = 100
AM_data.loc[AM_data.index[-1], 'Ideal_EQE'] = 0
AM_data['Ideal_EQE*PF'] = AM_data['Ideal_EQE'] * AM_data['PF'] * 0.001

# Calculate loss
AM_data['Loss'] = AM_data['Ideal_EQE*PF'] - AM_data['EQE*PF']

# Integration calculations
AM_data['Integrated AM 1.5 G'] = integrate.cumtrapz(AM_data['AM 1.5 G'], AM_data.WAVELENGTH1, initial=0)
AM_data['Integrated Jsc'] = integrate.cumtrapz(AM_data['EQE*PF'], AM_data.WAVELENGTH1, initial=0)
AM_data['Integrated Ideal Jsc'] = integrate.cumtrapz(AM_data['Ideal_EQE*PF'], AM_data.WAVELENGTH1, initial=0)
AM_data['Integrated Loss'] = integrate.cumtrapz(AM_data['Loss'], AM_data.WAVELENGTH1, initial=0)

# Compute Jsc using Simpson's rule
Jsc_value = simps(AM_data['EQE*PF'], x=AM_data.WAVELENGTH1)
Ideal_Jsc_value = simps(AM_data['Ideal_EQE*PF'], x=AM_data.WAVELENGTH1)

# Define energy range for calculations
New_energy_range = np.arange(0.32, 4.401, 0.002)
phi = (2 * np.pi * ((New_energy_range * eV) ** 2) * eV) / ((h ** 3) * (c ** 2) * (np.exp(New_energy_range * eV / (k * 300)) - 1))

# Cumulative flux calculations
fluxcumm = cumtrapz(phi[::-1], New_energy_range[::-1], initial=0)
fluxaboveE = -fluxcumm[::-1]
J0 = fluxaboveE * q * 0.1  # Convert from A/m^2 to mA/cm^2
J0[-1] = np.nan

# Voc Calculations
Calculated_VocSQ = (k * 300 / q) * np.log((Jsc_value / J0) + 1)
Calculated_VocRad = (k * 300 / q) * np.log((Jsc_value / (fluxaboveE * q * 0.1)) + 1)

# Improved Plotting
plt.figure(figsize=(8, 5))
plt.plot(AM_data['WAVELENGTH1'], AM_data['EQE_interp'], label='Interpolated EQE')
plt.plot(AM_data['WAVELENGTH1'], AM_data['Ideal_EQE'], linestyle='dashed', label='Ideal EQE')
plt.xlabel('Wavelength (nm)')
plt.ylabel('EQE (%)')
plt.title('EQE vs Wavelength')
plt.legend()
plt.grid()
plt.show()

# Print results
print(f"Jsc (mA/cm^2): {Jsc_value:.4f}")
print(f"Ideal Jsc (mA/cm^2): {Ideal_Jsc_value:.4f}")
print(f"VocSQ (V): {np.interp(1.4395, New_energy_range, Calculated_VocSQ):.4f}")
print(f"VocRad (V): {Calculated_VocRad[0]:.4f}")
