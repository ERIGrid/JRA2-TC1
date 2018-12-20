# ERIGrid JRA2: Test case TC1 mosaik implementation

This repository contains instructions and models for running the co-simulation tests of TC1 and its upscaled version (referred to as LSS1).
A detailed description of test case TC1 can be found in [ERIGrid deliverable D-JRA2.2](https://erigrid.eu/dissemination/).
A detailed description of test case LSS1 can be found in [ERIGrid deliverable D-JRA2.3](https://erigrid.eu/dissemination/).


- folder *monolithic_model_pf*: contains a monolithic implementation of TC1 in PowerFactory
- folder *monolithic_model_pscad*: contains a monolithic implementation of TC1 in PSCAD
- folder *open_loop_rms*: contains the FMU of the controller and a script for performing an open-loop test
- folder *small_scale_cosim_pf*: co-simulation implementation of TC1 using PowerFactory
- folder *small_scale_cosim_pscad*: co-simulation implementation of TC1 using PSCAD
- folder *upscaled_cosim_pf*: co-simulation implementation of LSS1 using PowerFactory