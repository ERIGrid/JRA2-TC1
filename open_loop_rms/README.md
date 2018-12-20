# ERIGrid JRA2 TC1: Open-loop RMS converter

A detailed description of test case TC1 can be found in [ERIGrid deliverable D-JRA2.2](https://erigrid.eu/dissemination/).

## Prerequisits (Windows)

- **Python** (tested with Python 2.7 32-bit) with packages [**matplotlib**](https://matplotlib.org/users/installing.html) and [**fmipp**](https://pypi.org/project/fmipp/)  installed
- **MATLAB/Simulink** (tested with MATLAB R2014b 32-bit) and the [**FMI Kit for Simulink**](https://www.3ds.com/products-services/catia/products/dymola/fmi/)


**ATTENTION**: The co-simulation toolchain needs to be completely in either 32-bit or 64-bit.
For TC1 it was decided to use consistently **32-bit** for Windows setups.
Therefore, be sure to install **32-bit versions of all tools** (Python, PowerFactory, MATLAB/Simulink)!


## Running the simulation

1. Install all prerequisites as described above.

2. In the command line, run script *openLoop.py*:
```
    python openLoop.py
```

3. At t=1 a voltage dip should occur, causing the current setpoints to change.
