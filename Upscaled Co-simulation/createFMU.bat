@ECHO OFF

REM Adapt the line below to point to your installation of the FMI++ PowerFactory FMU Export Utility.
SET PF_FMU_EXPORT_UTILITY_PATH=C:\Development\erigrid\powerfactory-fmu-v0.6


D:\Python35\python.exe %PF_FMU_EXPORT_UTILITY_PATH%\powerfactory_fmu_create.py -v -m upscaled -p upscaled.pfd -i test-FMI-UPS-inputs.txt -o test-FMI-UPS-outputs.txt -r 0.001 
