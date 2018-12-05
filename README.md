# ERIGrid JRA2: Test case TC1 mosaik implementation

This file contains instructions for installing the required tools and packages as well as for running the co-simulation tests of TC1 and its upscaled version (referred to as LSS1).
A detailed description of test case TC1 can be found in [ERIGrid deliverable D-JRA2.2](https://erigrid.eu/dissemination/).
A detailed description of test case LSS1 can be found in [ERIGrid deliverable D-JRA2.3](https://erigrid.eu/dissemination/).


## Prerequisits (Windows)

- **Python** (tested with Python 2.7 32-bit) with packages [**matplotlib**](https://matplotlib.org/users/installing.html) and [**fmipp**](https://pypi.org/project/fmipp/)  installed
- **PowerFactory** (tested with PowerFactory 2017 SP3 x86) and the [**FMI++ PowerFactory FMU Export Utility**](https://sourceforge.net/projects/powerfactory-fmu/)
- **MATLAB/Simulink** (tested with MATLAB R2014b 32-bit) and the [**FMI Kit for Simulink**](https://www.3ds.com/products-services/catia/products/dymola/fmi/)
- add the PowerFactory and MATLAB binary directories to the PATH variable


**ATTENTION**: The co-simulation toolchain needs to be completely in either 32-bit or 64-bit.
For TC1 it was decided to use consistently **32-bit** for Windows setups.
Therefore, be sure to install **32-bit versions of all tools** (Python, PowerFactory, MATLAB/Simulink)!

## Open-loop RMS converter

1. Install all prerequisites as described above.

2. In the command line, switch to subfolder *Open-loop-RMS* and run script *openLoop.py*:
```
    python openLoop.py
```

3. At t=1 a voltage dip should occur, causing the current setpoints to change.


## Monolithic PowerFactory Model (TC1)

1. Install all prerequisites as described above.

2. Import *monolithic.pfd* to PowerFactory and run it.

3. The simulation should run accordingly and produce time-domain simulation plots.


## Small-scale Co-simulation (TC1)

1. Install all prerequisites as described above.

2. In the command line, switch to subfolder *Small Scale Co-simulation* and run script *runme.py*:
```
    python runme.py
```

3. between t=1.0 and t=1.18 a voltage dip is emulated at the point of common coupling of the converter.


## Upscaled Co-simulation (LSS1)

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
