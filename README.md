# Sensitive EQE Measurement System & Data Analysis

This repository contains all LabVIEW **Virtual Instruments (VIs)** for the automation of a **sensitive External Quantum Efficiency (sEQE) measurement system**, as well as a **Python-based data analysis script** for processing and extracting key photovoltaic parameters.

## 🛠 **Experimental Setup**
The sEQE measurement setup is designed for high-sensitivity detection of weak photocurrents in photovoltaic materials. The system includes:

- **Light Source**: Newport 300W ozone-free xenon arc lamp
- **Chopper**: Stanford Research Systems SR540 (473 Hz)
- **Monochromator**: QD Lot MSH-300
- **Optical Delivery**: Optical fiber for in-glovebox transport, lenses, and filters for beam shaping
- **Electronics**:
  - **Current Pre-amplifier**: Stanford Research Systems 530
  - **Lock-in Amplifier**: Stanford Research Systems SR830
- **Calibration**: Newport 71619 Si/Ge detectors

## 🔧 **Automation & Control (LabVIEW VIs)**
The system is fully automated using a custom **LabVIEW control program**, which handles:
✅ **Monochromator wavelength control**  
✅ **Chopper synchronization with the lock-in amplifier**  
✅ **Automated data acquisition & real-time visualization**  
✅ **Calibration with Si/Ge detectors**  

### **Getting Started with the LabVIEW Control Program**
1. Open **`sEQE Project 2025.lvproj`** in LabVIEW.
2. Inside the project, open the main VI: **`2024_06_02_sEQE.vi`**.
3. Ensure that the **Thorlabs .dll files** from `Instrument Drivers/Filter Wheel/` are copied into the same directory as the LabVIEW project file.
4. Run the main VI to start the automated measurement routine.

## 📊 **Python Data Analysis**
A separate **Python script** is provided to analyze the EQE measurements and extract photovoltaic parameters. It performs:
- **EQE Interpolation**: Matches EQE data to the AM1.5G solar spectrum
- **Short-Circuit Current Density (Jsc) Calculation**
- **Photon Flux & Integration Analysis**
- **Voc Calculations using the Shockley-Queisser Limit**
- **Loss Analysis & Ideal EQE Comparisons**

The Python script utilizes `NumPy`, `SciPy`, `Pandas`, and `Matplotlib` for numerical analysis and visualization.

## 📂 **Repository Structure**
```
/ 
├── Instrument Drivers/    # LabVIEW control program files
├── data_analysis/        # Python scripts for EQE data processing
└── README.md              # This file
```

## 🏗 **Future Improvements**
- Further automation of calibration routines
- Change current architecture to OOP for better modularity and maintainability
- Incorporate temperature controller from cryostat to allow temperature-dependent measurements
- Machine learning for noise reduction and signal optimization

---
### 🚀 **Getting Started**
1️⃣ **LabVIEW Control**: Open `sEQE Project 2025.lvproj`, then open and run `2024_06_02_sEQE.vi`.  
2️⃣ **Python Analysis**: Run `sEQE_analysis.py` after obtaining measurement data.  

For any issues or contributions, feel free to open an issue or submit a pull request! 🛠

