# ERIGrid JRA2 TC1: Small-scale Co-simulation using PowerFactory

A detailed description of test case TC1 can be found in [ERIGrid deliverable D-JRA2.2](https://erigrid.eu/dissemination/).

## Prerequisits (Windows)

- **Python** (tested with Python 2.7 32-bit) with packages [**matplotlib**](https://matplotlib.org/users/installing.html) and [**fmipp**](https://pypi.org/project/fmipp/)  installed
- **PowerFactory** (tested with PowerFactory 2017 SP3 x86) and the [**FMI++ PowerFactory FMU Export Utility**](https://sourceforge.net/projects/powerfactory-fmu/)
- **MATLAB/Simulink** (tested with MATLAB R2014b 32-bit) and the [**FMI Kit for Simulink**](https://www.3ds.com/products-services/catia/products/dymola/fmi/)
- add the PowerFactory and MATLAB binary directories to the PATH variable

**NOTE**: The interfaces of the tools typically change (at least slightly) with each version.
Hence, this specific setup will most likely not work in case you do not use the exact versions of Python, PowerFactory and MATLAB mentioned above! 

**ATTENTION**: The co-simulation toolchain needs to be completely in either 32-bit or 64-bit.
For TC1 it was decided to use consistently **32-bit** for Windows setups.
Therefore, be sure to install **32-bit versions of all tools** (Python, PowerFactory, MATLAB/Simulink)!

## Running the simulation

1. Install all prerequisites as described above.

2. In the command line, run script *runme.py*:
```
    python runme.py
```

3. between t=1.0 and t=1.18 a voltage dip is emulated at the point of common coupling of the converter.
