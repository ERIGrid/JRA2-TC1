# ERIGrid JRA2 LSS1: Upscaled Co-simulation using PowerFactory

A detailed description of test case LSS1 can be found in [ERIGrid deliverable D-JRA2.3](https://erigrid.eu/dissemination/).

## Prerequisits (Windows)

- **Python** (tested with Python 2.7 32-bit) with packages [**matplotlib**](https://matplotlib.org/users/installing.html) and [**fmipp**](https://pypi.org/project/fmipp/)  installed
- **PowerFactory** (tested with PowerFactory 2017 SP3 x86) and the [**FMI++ PowerFactory FMU Export Utility**](https://sourceforge.net/projects/powerfactory-fmu/)
- **MATLAB/Simulink** (tested with MATLAB R2014b 32-bit) and the [**FMI Kit for Simulink**](https://www.3ds.com/products-services/catia/products/dymola/fmi/)
- add the PowerFactory and MATLAB binary directories to the PATH variable


**ATTENTION**: The co-simulation toolchain needs to be completely in either 32-bit or 64-bit.
For TC1 it was decided to use consistently **32-bit** for Windows setups.
Therefore, be sure to install **32-bit versions of all tools** (Python, PowerFactory, MATLAB/Simulink)!

## Running the simulation

This folder contains the co-simulation experiment of upscaled TC1 (also referred to as LSS1).
The 32 individual wind turbines are all FMUs based on the Simulink RMS model.
It showcases the upscaled co-simulation.

1. Install all prerequisites as described above.

2. File *codegen.py* is the Python script that generates the Python code for running the co-simulation. (The resulting simulation script is around 6500 lines long, hence it would be tedious to write it without automation). In the command line, switch to subfolder *Small Scale Co-simulation* and run script *codegen.py* to generate *upscaled.py*:
```
    python codegen.py
```

3. Finally, run *upscaled.py* from the command line:
```
    python upscaled.py
```

4. Plots will be saved in a subfolder as listed in *codegen.py* (there should be 162 plots in total).
