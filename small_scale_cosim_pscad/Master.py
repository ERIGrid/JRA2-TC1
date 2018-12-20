import os
import fmipp
import time
import matplotlib.pyplot as plt
import numpy as np

#------------------------------------------------------------------------------
#------------------------------------------------------------------------------
# P L O T T I N G  P A R A M E T E R S 
#------------------------------------------------------------------------------
#------------------------------------------------------------------------------

Set1Red='#e41a1c'
Set1Blue='#377eb8'
Set1Green='#4daf4a'
Set1Purple='#984ea3'
Set1Orange='#ff7f00'
Set1Yellow='#ffff33'
Set1Brown='#a65628'
Set1Pink='#f781bf'
Set1Gray='#999999'
lw=2
colorOM=Set1Red

#------------------------------------------------------------------------------
#------------------------------------------------------------------------------
# data containers for results
#------------------------------------------------------------------------------
#------------------------------------------------------------------------------

res_time = []   # time steps
res_V3d = [] 
res_V3q = [] 
res_V3 = [] 
res_Vdc3 = [] 
res_State = [] 
res_Kboost = [] 
res_RampRate = [] 
res_CLMode = [] 
res_Id_ref = []
res_Iq_ref = []

#------------------------------------------------------------------------------
#------------------------------------------------------------------------------
# Expected Powerflow results
#------------------------------------------------------------------------------
#------------------------------------------------------------------------------

P_0 = 0.85   # Initial WT output Active power
Q_0 = 0.22   # Initial WT output Reactive power
V_0 = 0.9457   # Steady-state voltage of WT Bus
theta_0 = 9.5   # Steady-state angle of WT Bus

#------------------------------------------------------------------------------
#------------------------------------------------------------------------------
# Time setting
#------------------------------------------------------------------------------
#------------------------------------------------------------------------------

sim_time = 0.
step_size = 0.01
Release_time = 5
stop_time = 20

#------------------------------------------------------------------------------
#------------------------------------------------------------------------------
# Call FMUs From MATLAB 
#------------------------------------------------------------------------------
#------------------------------------------------------------------------------

work_dir=os.getcwd()
logging_on = False
stop_before_event = False
event_search_precision = 1e-10
integrator_type = fmipp.eu

#------------------------------------------------------------------------------
# The First Matlab Controller (FRT)
#------------------------------------------------------------------------------

model_name_M='FRTController_mar_v2_sf'
path_to_fmu_M = os.path.join(work_dir, model_name_M + '.fmu')   # Extract FMU and retrieve URI to directory.
uri_to_extracted_fmu_M= fmipp.extractFMU( path_to_fmu_M, work_dir )   # using the FMI 2.0 specification
fmuM1 = fmipp.FMUModelExchangeV2(uri_to_extracted_fmu_M, model_name_M, logging_on, stop_before_event, event_search_precision, integrator_type )

status1 = fmuM1.instantiate( "my_FRT_controller" ) # Instantiate the FMU model
assert status1 == fmipp.fmiOK

# set all internal parameters of the second FMU 
#------------------------------------------------------------------------------ 
fmuM1.setRealValue("Parameters.StateMachine_dT", step_size)   # dT: time step size of the simulation federate
fmuM1.setRealValue("Parameters.State_Machine.state_transition_RpS3", 0.5)   #ramping rate when in state=3,, determines how long the converter will ramp up the active power and when it returns to normal operation, i.e., state=1

# Initializing the FMU model
#------------------------------------------------------------------------------ 
fmuM1.setRealValue("Udc",1.0)   # - Udc
fmuM1.setRealValue("VPCC",1.0)   # - VPCC
fmuM1.setBooleanValue("release",False)   # - release

status1 = fmuM1.initialize()
assert status1 == fmipp.fmiOK

# Getting the initialize output of the first FMU.
#------------------------------------------------------------------------------
NextState = fmuM1.getRealValue("STATE")   # - STATE
Kboost = fmuM1.getRealValue("KaRCI")   # - KaRCI
RampRate = fmuM1.getRealValue("Rp")   # - Rp
CLMode = fmuM1.getRealValue("CLMODE")   # - CLMODE

print("The First Matlab Controller (FRTController) is ok")
print "State = ", NextState
print "Kboost = ", Kboost
print "RampRate = ", RampRate
print "CLMode = ", CLMode

#------------------------------------------------------------------------------
# The Second Matlab Controller (RmsConverterController)
#------------------------------------------------------------------------------

model_name_M='RmsConverterController_AAvdM_R2014b_sf'
path_to_fmu_M = os.path.join(work_dir, model_name_M + '.fmu')   # Extract FMU and retrieve URI to directory.
uri_to_extracted_fmu_M= fmipp.extractFMU( path_to_fmu_M, work_dir )   # using the FMI 2.0 specification

fmuM2 = fmipp.FMUModelExchangeV2(uri_to_extracted_fmu_M, model_name_M, logging_on, stop_before_event, event_search_precision, integrator_type )

status2 = fmuM2.instantiate( "my_RMS_controller" ) # Instantiate the FMU model
assert status2 == fmipp.fmiOK

## set all internal parameters of the first FMU (PID parameters and limits)
##------------------------------------------------------------------------------
#Ilim=1.1
#KiV=10
#Kv=0.0
#RP=100
#fmuM2.setRealValue("Parameters.Converter_RMS_Controller.Saturation.UpperLimit",Ilim)
#fmuM2.setRealValue("Parameters.Converter_RMS_Controller.Saturation.LowerLimit",-Ilim)
#fmuM2.setRealValue("Parameters.Converter_RMS_Controller.PID_Controller.Saturate.UpperLimit",Ilim)
#fmuM2.setRealValue("Parameters.Converter_RMS_Controller.PID_Controller.Saturate.LowerLimit",-Ilim)
#fmuM2.setRealValue("Parameters.Converter_RMS_Controller.PID_Controller.Clamping_circuit.DeadZone.UpperValue",Ilim)
#fmuM2.setRealValue("Parameters.Converter_RMS_Controller.PID_Controller.Clamping_circuit.DeadZone.LowerValue",-Ilim)
#fmuM2.setRealValue("Parameters.Converter_RMS_Controller.PID_Controller1.Saturate.UpperLimit",Ilim)
#fmuM2.setRealValue("Parameters.Converter_RMS_Controller.PID_Controller1.Saturate.LowerLimit",-Ilim)
#fmuM2.setRealValue("Parameters.Converter_RMS_Controller.PID_Controller1.Clamping_circuit.DeadZone.UpperValue",Ilim)
#fmuM2.setRealValue("Parameters.Converter_RMS_Controller.PID_Controller1.Clamping_circuit.DeadZone.LowerValue",-Ilim)
#fmuM2.setRealValue("Parameters.Converter_RMS_Controller.Riferimento_Q1.Saturation.UpperLimit",Ilim)
#fmuM2.setRealValue("Parameters.Converter_RMS_Controller.Riferimento_Q1.Saturation.LowerLimit",-Ilim)
#fmuM2.setRealValue("Parameters.Converter_RMS_Controller.PID_Controller.Integral_Gain.Gain", 1)
#fmuM2.setRealValue("Parameters.Converter_RMS_Controller.PID_Controller.Proportional_Gain.Gain",0.0)
#fmuM2.setRealValue("Parameters.Converter_RMS_Controller.PID_Controller1.Integral_Gain.Gain",KiV)
#fmuM2.setRealValue("Parameters.Converter_RMS_Controller.PID_Controller1.Proportional_Gain.Gain",Kv)
#fmuM2.setRealValue("Parameters.Converter_RMS_Controller.Ramp_limitation.Rate_Limiter.RisingSlewLimit", RP)

# Initializing the FMU model
#------------------------------------------------------------------------------
Iprio=2
KBOOST=1.0
fmuM2.setRealValue("Vd", 1.0)            # d-axis voltage (pu)
fmuM2.setRealValue("Vq", 0.0)            # q-axis voltage (pu, unused)
fmuM2.setRealValue("V_pcc_RMS", 1.0)     # RMS voltage at PCC (pu)
fmuM2.setRealValue("Vdc_pu", 1.0)        # dc voltage (pu)
fmuM2.setRealValue("Qref_pu", 0.0)       # reference value of Q (terminal)
fmuM2.setRealValue("I_lim", Iprio)       # I_lim: limitation priority 1.0: d-priority, 2.0: q-priority 
fmuM2.setRealValue("R_on",1.0)           # R_on: rate limiter switch 1.0: on, 0.0: off
fmuM2.setRealValue("R_p", 10.0)          # R_p: maximum ramping rate
fmuM2.setRealValue("K_aRCI",KBOOST)      # K_aRCI: boosting gain

i_d_0 = - P_0 #/ V_0
i_q_0 = - Q_0 #/ V_0
fmuM2.setRealValue("Parameters.Converter_RMS_Controller.PID_Controller.Integrator.InitialCondition", i_d_0)
fmuM2.setRealValue("Parameters.Converter_RMS_Controller.PID_Controller1.Integrator.InitialCondition", i_q_0)

status2 = fmuM2.initialize() # initialize model
assert status1 == fmipp.fmiOK

Id_ref = -1*fmuM2.getRealValue("Id_ref")
Iq_ref = -1*fmuM2.getRealValue("Iq_ref")

print("The Second Matlab Controller (RmsConverterController) is ok")
print "Id_ref = ", Id_ref
print "Iq_ref = ", Iq_ref

#------------------------------------------------------------------------------
#------------------------------------------------------------------------------
# The FMI-CS from PSCAD
#------------------------------------------------------------------------------
#------------------------------------------------------------------------------

# import PSCAD FMI stuff
from FMI_SERVER import FMI_Server, fmu
Pscad_Server = FMI_Server()
Pscad_Server.instantiate()

# Initialize PSCAD FMU with initial values
#------------------------------------------------------------------------------
Pscad_Server.initialize([Id_ref, Iq_ref])

#------------------------------------------------------------------------------
#------------------------------------------------------------------------------
# The loop of co-simulation
#------------------------------------------------------------------------------
#------------------------------------------------------------------------------

while ( sim_time < stop_time ):   # Make co-simulation step.
    
    # Advance time.
    sim_time += step_size
    sim_time = round(sim_time,2)
    
    #--------------------------------------------------------------------------
    #  Wating for PSCAD to run   
    fmu.master_time = sim_time   # Report external time to PSCAD FMU
    while sim_time > fmu.cur_time:   # Wait for PSCAD fmu to advance in time
        time.sleep(0.001)
    
    #--------------------------------------------------------------------------
    # PSCAD FMU >>>>> Master
    fmu_out = fmu.outputs[fmu.cur_time]    # Get values from PSCAD FMU 
    V3d = fmu_out[0]
    V3q = fmu_out[1]
    V3 = fmu_out[2]
    Vdc3 = fmu_out[3]
    Qref = fmu_out[4]

    #--------------------------------------------------------------------------
    # Master >>>>> 1st MATLAB FMU >>>>> Master
            
    fmuM1.setRealValue("Udc",Vdc3)   # - Udc
    fmuM1.setRealValue("VPCC",V3)   # - VPCC
    if sim_time < Release_time:
        fmuM1.setBooleanValue("release",False)   # - release
    else:
        fmuM1.setBooleanValue("release",True)   # - release
    
    tP1 = fmuM1.integrate( sim_time ) # integrate the first MATLAB FMU model
    NextState = fmuM1.getRealValue("STATE")   # Get Values from Matlab controller
    Kboost = fmuM1.getRealValue("KaRCI")   # Get Values from Matlab controller
    RampRate = fmuM1.getRealValue("Rp")   # Get Values from Matlab controller
    CLMode = fmuM1.getRealValue("CLMODE")   # Get Values from Matlab controller

    #--------------------------------------------------------------------------
    # Master >>>>> 2nd MATLAB FMU >>>>> Master
    
    fmuM2.setRealValue("Vd", V3d)            # d-axis voltage (pu)
    fmuM2.setRealValue("Vq", V3q)            # q-axis voltage (pu, unused)
    fmuM2.setRealValue("V_pcc_RMS", V3)     # RMS voltage at PCC (pu)
    fmuM2.setRealValue("Vdc_pu",Vdc3)        # dc voltage (pu)
    fmuM2.setRealValue("Qref_pu", Qref)       # reference value of Q (terminal)
    fmuM2.setRealValue("I_lim", NextState)       # I_lim: limitation priority 1.0: d-priority, 2.0: q-priority 
    fmuM2.setRealValue("R_on",CLMode)           # R_on: rate limiter switch 1.0: on, 0.0: off
    fmuM2.setRealValue("R_p", RampRate)          # R_p: maximum ramping rate
    fmuM2.setRealValue("K_aRCI",Kboost)      # K_aRCI: boosting gain
    
    tP2 = fmuM2.integrate( sim_time ) # integrate the first MATLAB FMU model
    Id_ref = -1* fmuM2.getRealValue("Id_ref")       # Get Values from Matlab controller
    Iq_ref = -1*fmuM2.getRealValue("Iq_ref")       # Get Values from Matlab controller
    
     #--------------------------------------------------------------------------
    #  Master >>>>> PSCAD  
    fmu.inputs[sim_time] = [Id_ref,Iq_ref]   # Set inputs to in same orded than in PSCAD
   
    
    #--------------------------------------------------------------------------
    # Get simulation results
    res_time.append(sim_time)
    res_V3d.append(V3d)
    res_V3q.append(V3q)
    res_V3.append(V3)
    res_Vdc3.append(Vdc3)
    res_State.append(NextState)
    res_Kboost.append(Kboost)
    res_RampRate.append(RampRate)
    res_CLMode.append(CLMode)
    res_Id_ref.append(Id_ref)
    res_Iq_ref.append(Iq_ref)

    print('At t: %5.2f (%5.2f)s: terminal voltage of WPP = %5.3f pu' %(sim_time, fmu.cur_time, V3))

#------------------------------------------------------------------------------
#------------------------------------------------------------------------------
# Plot the results.
#------------------------------------------------------------------------------
#------------------------------------------------------------------------------
    
plt.figure(1)
plt.plot( res_time, res_Id_ref, 'r-',linewidth=4)
plt.plot( res_time, res_Iq_ref, 'b-',linewidth=4)
plt.xlabel( 'simulation time in s' )
plt.ylabel( 'i_ref in p.u.' )
plt.xlim( 0., stop_time)
plt.show()
     
plt.figure(2)
plt.plot( res_time, res_V3d, 'r-',linewidth=4 )
plt.plot( res_time, res_V3q, 'b-',linewidth=4 )
plt.plot( res_time, res_V3, 'k-',linewidth=2 )
plt.xlabel( 'simulation time in s' )
plt.ylabel( 'Voltages' )
plt.xlim( 0., stop_time)

plt.figure(3)
plt.plot( res_time, res_Vdc3, 'r-',linewidth=4 )
plt.xlabel( 'simulation time in s' )
plt.ylabel( 'DC voltage' )
plt.xlim( 0., stop_time)


plt.figure(4)
plt.plot( res_time, res_State, 'r-',linewidth=4 )
plt.xlabel( 'simulation time in s' )
plt.ylabel( 'State' )
plt.xlim( 0., stop_time)

plt.figure(5)
plt.plot( res_time, res_Kboost, 'r-',linewidth=4 )
plt.xlabel( 'simulation time in s' )
plt.ylabel( 'Kboost' )
plt.xlim( 0., stop_time)

plt.figure(6)
plt.plot( res_time, res_RampRate, 'r-',linewidth=4 )
plt.xlabel( 'simulation time in s' )
plt.ylabel( 'RampRate' )
plt.xlim( 0., stop_time)

plt.figure(7)
plt.plot( res_time, res_CLMode, 'r-',linewidth=4 )
plt.xlabel( 'simulation time in s' )
plt.ylabel( 'CLMode' )
plt.xlim( 0., stop_time)










