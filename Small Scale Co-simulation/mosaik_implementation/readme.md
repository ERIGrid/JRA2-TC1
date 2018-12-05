# Mosaik code for JRA2-TC1

The provided code can be used to replicate the mosaik-based implementation
of the ERIGrid JRA2 TestCase1 in the small-scale version.
Next to the given files, the following software modules are needed:

* A RMS-converter-controller, provided as a FMU as part of the ERIGrid-JRA2 open source code
* A PowerFactory simulation model, provided as a FMU as part of the ERIGrid-JRA2 open source code
* The newest version of mosaik (v2.5.0 or higher)

## Mosaik scenario and help modules

The file of interest for a user is tc1_mosaik.py, which contains the executable mosaik scenario.
The modules fault_sim.py and modif_comp.py are support modules that are integrated as additional
simulators into the setup to allow manipulation of the FMUs and the data exchange between them.

For the integration of the FMU simulators, the module mosaik_fmume_test is needed.
This module can integrate arbitrary simulators provided as FMUs into a mosaik scenario.
It can be installed locally via "pip install".
Please note that the given code presents a preliminary version. 
A slightly refactored version will likely be released on the
[mosaik-repo](https://bitbucket.org/mosaik/)
by the end of 2018.