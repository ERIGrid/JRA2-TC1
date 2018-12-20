# ERIGrid JRA2 TC1: Small-scale Co-simulation using PSCAD

A detailed description of test case TC1 can be found in [ERIGrid deliverable D-JRA2.2](https://erigrid.eu/dissemination/).


## Requirements

- **PSCAD** (tested with version *4.6.x*)
- **MATLAB/Simulink** (tested with MATLAB R2014b 32-bit) and the [**FMI Kit for Simulink**](https://www.3ds.com/products-services/catia/products/dymola/fmi/)
- **Python** (tested with versions *2.7.14 32-bit* and *3.5.4 32-bit*) with packages [**matplotlib**](https://matplotlib.org/users/installing.html) and [**twisted**](https://twistedmatrix.com/trac/)

**NOTE:** depending on OS, you might need to install [**Microsoft Visual C++ Development tools**](https://visualstudio.microsoft.com/downloads/)


## Files

- FMI_SERVER.py
- FMI_TCP.pslx
- psocket.c
- master.py


## PSCAD FMI_TCP PACKAGE

*pscad_recv*:

- set number of outputs and corresponding initialization values
- add correct amount of data taps to output side


*pscad_send*:

- array merge component should be used in inputs
- TIME block must be connected to first input port!
- check from parameters that
	1. number of input ports and number of inputs in each port match in array_merge
	2. total number of inputs match in pscad_send
- set IP Address in four parameters (127.0.0.1 is localhost)
- unused port (e.g., 8001)
- time delay (not currently used)
- time step (how often data is sent out)


## Instructions

1. check that *psocket.c* is in same folder as *FMI_TCP.pslx* project
2. *FMI_SERVER.py* should be in same folder than *master.py* OR added to Python path
3. import FMI_TCP library in PSCAD
4. add pscad_recv and pscad_send components to your project
5. connect input/output signals as wanted
6. run *master.py*
7. when master is ready, run PSCAD simulation


## TROUBLESHOOTING

### Problem

Master gives something like:
```
	ValueError: invalid null reference in method 'new_FMUModelExchangeV2', argument 1 of type 'std::string const &'
```

### Solution

Python process with loaded FMU is hanging, kill it from task manager (e.g., *python.exe* or *pythonw.exe* depending on used environment)
