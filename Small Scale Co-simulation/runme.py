import os
import sys
import fmipp
import optparse


# Import FMI++ Python library.

import matplotlib.pyplot as plt
import csv
import numpy as np
#------------------------------------------------------------------------------
# P L O T T I N G  P A R A M E T E R S 
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
# converter model input parameters
#------------------------------------------------------------------------------

# voltage control gain
Kv=0.0
# voltage control integrator gain
KiV=10.0
# per unit current limit of the converter
Ilim=1.1
# current limiting priority during normal operation
Iprio=2
# current limiting priority during FRT
IprioFRT=2
# current limiting priority during post-FRT
IprioPOSTFRT=1
# d-axis current slew rate (pu/s) during normal operation
RP=100
# d-axis current slew rate (pu/s) during post-FRT
POSTRP=0.5
# additional reactive current injection 'boosting' gain, kicks in during fault
KBOOST=1.0
# export results name
EXPname = "KBOOST=1_Ilim=11_PRIO=2_POSTRP=05.csv"

#------------------------------------------------------------------------------
# F M U  P A R A M E T E R S 
#------------------------------------------------------------------------------


work_dir=os.getcwd()
logging_on = False

# fmu : FMU of Powerfactory based on FMI-CS        
# fmuF: FMU of FRT controller based on FMI-ME
# fmuM: FMU of converter controller based on FMI-ME
# @TODO step_size: now 0.01, check whether both matlab models need the same dT
        

#------------------------------------------------------------------------------
# the FRT controller
#------------------------------------------------------------------------------


# so it is important to use the original MATLAB model name, in this case the flattering FRTController_mar_v2_sf. You might have to rename the FMU from the JRA2.2 model library.
model_name_F='FRTController_mar_v2_sf'
stop_before_event = False
event_search_precision = 1e-10
integrator_type = fmipp.eu

path_to_fmu_F = os.path.join(work_dir, model_name_F + '.fmu')
# Extract FMU and retrieve URI to directory.
uri_to_extracted_fmu_F= fmipp.extractFMU( path_to_fmu_F, work_dir )
# using the FMI 2.0 specification
fmuF = fmipp.FMUModelExchangeV2(uri_to_extracted_fmu_F, model_name_F, logging_on, stop_before_event, event_search_precision, integrator_type )
       
# Instantiate the FMU.
status1 = fmuF.instantiate( "my_FRT_controller" ) # instantiate model


# fmuFb = fmipp.FMUModelExchangeV2(uri_to_extracted_fmu_F, model_name_F, logging_on, stop_before_event, event_search_precision, integrator_type )
# status_b = fmuFb.instantiate( "my_FRT_controller" ) # instantiate model        

assert status1 == fmipp.fmiOK
# Initialize the FMU.
status1 = fmuF.initialize() # initialize model
assert status1 == fmipp.fmiOK




#------------------------------------------------------------------------------
# the matlab controller
#------------------------------------------------------------------------------

model_name_M='RmsConverterController_AAvdM_R2014b_sf'
stop_before_event = False
event_search_precision = 1e-10
integrator_type = fmipp.dp 

path_to_fmu_M = os.path.join(work_dir, model_name_M + '.fmu')
# Extract FMU and retrieve URI to directory.
uri_to_extracted_fmu_M= fmipp.extractFMU( path_to_fmu_M, work_dir )
# using the FMI 2.0 specification
fmuM = fmipp.FMUModelExchangeV2(uri_to_extracted_fmu_M, model_name_M, logging_on, stop_before_event, event_search_precision, integrator_type )
# Instantiate the FMU.
status1 = fmuM.instantiate( "my_RMS_controller" ) # instantiate model


assert status1 == fmipp.fmiOK


#------------------------------------------------------------------------------
# second FMI-CS from powerfactory
#------------------------------------------------------------------------------

# Specify FMI model name.
model_name = 'IEEEWPP'
time_diff_resolution = 1e-9

# Specify path to the FMU (located in subdirectory "NineBusSystem-resources" of the current working directory). 
path_to_fmu = os.path.join( work_dir, model_name + '.fmu' )

# Extract FMU and retrieve URI to directory.
uri_to_extracted_fmu = fmipp.extractFMU( path_to_fmu, work_dir )

# Create an instance of class FMUCoSimulation (handle for the FMU).
fmu = fmipp.FMUCoSimulationV1( uri_to_extracted_fmu, model_name, logging_on, time_diff_resolution )

# Instantiate the FMU.
start_time = 0.
instance_name = "IEEEWPP-FMU-basis"
visible = False
interactive = False
status = fmu.instantiate( instance_name, start_time, visible, interactive )
assert status == fmipp.fmiOK

# Initialize the FMU.
stop_time = 2.0
stop_time_defined = True
step_size = 0.01

status = fmu.initialize( start_time, stop_time_defined, stop_time )
assert status == fmipp.fmiOK


# first the FRT control
# K_aRCI: boosting gain
fmuM.setRealValue("K_aRCI",KBOOST)
# R_on: rate limiter switch 1.0: on, 0.0: off
fmuM.setRealValue("R_on",1.0)
# R_p: maximum ramping rate
fmuM.setRealValue("R_p", 10.0)
# I_lim: limitation priority 1.0: d-priority, 2.0: q-priority 
fmuM.setRealValue("I_lim", Iprio)
# d-axis voltage (pu)
fmuM.setRealValue("Qpcc", fmu.getRealValue('ElmGenstat.WPP.m:Q:bus1') / 120.0)
# q-axis voltage (pu, unused)
fmuM.setRealValue("Vq", 0.0)
# RMS voltage at PCC (pu)
fmuM.setRealValue("V_pcc_RMS", fmu.getRealValue('ElmGenstat.WPP.m:u1:bus1'))
# reference value of Q (terminal)
fmuM.setRealValue("Qref_pu", fmu.getRealValue('ElmGenstat.WPP.m:Q:bus1') / 120.0)
# dc voltage (pu)
fmuM.setRealValue("Vdc_pu", 1.0)

fmuM.setRealValue("Parameters.Converter_RMS_Controller.V_nom1.Value",  fmu.getRealValue('ElmGenstat.WPP.m:u1:bus1') )
fmuM.setRealValue("Parameters.Converter_RMS_Controller.V_nom.Value",  fmu.getRealValue('ElmGenstat.WPP.m:u1:bus1') )        

# set all the limiters inside the FMU (quite a few)
maxCurrent=Ilim

fmuM.setRealValue("Parameters.Converter_RMS_Controller.Saturation.UpperLimit",maxCurrent)
fmuM.setRealValue("Parameters.Converter_RMS_Controller.Saturation.LowerLimit",-maxCurrent)
fmuM.setRealValue("Parameters.Converter_RMS_Controller.PID_Controller.Saturate.UpperLimit",maxCurrent)
fmuM.setRealValue("Parameters.Converter_RMS_Controller.PID_Controller.Saturate.LowerLimit",-maxCurrent)
# fmuM.setRealValue("Parameters.Converter_RMS_Controller.PID_Controller.Clamping_circuit.DeadZone.LowerValue",-maxCurrent)
# fmuM.setRealValue("Parameters.Converter_RMS_Controller.PID_Controller.Clamping_circuit.DeadZone.UpperValue",maxCurrent)
fmuM.setRealValue("Parameters.Converter_RMS_Controller.PID_Controller1.Saturate.UpperLimit",maxCurrent)
fmuM.setRealValue("Parameters.Converter_RMS_Controller.PID_Controller1.Saturate.LowerLimit",-maxCurrent)
# fmuM.setRealValue("Parameters.Converter_RMS_Controller.PID_Controller1.Clamping_circuit.DeadZone.LowerValue",-maxCurrent)
# fmuM.setRealValue("Parameters.Converter_RMS_Controller.PID_Controller1.Clamping_circuit.DeadZone.UpperValue",maxCurrent)
fmuM.setRealValue("Parameters.Converter_RMS_Controller.Riferimento_Q1.Saturation.UpperLimit",maxCurrent)
fmuM.setRealValue("Parameters.Converter_RMS_Controller.Riferimento_Q1.Saturation.LowerLimit",-maxCurrent)


fmuM.setRealValue("Parameters.Converter_RMS_Controller.PID_Controller.Integral_Gain.Gain", 1)
fmuM.setRealValue("Parameters.Converter_RMS_Controller.PID_Controller.Proportional_Gain.Gain",0.0)

fmuM.setRealValue("Parameters.Converter_RMS_Controller.PID_Controller1.Integral_Gain.Gain",KiV)
fmuM.setRealValue("Parameters.Converter_RMS_Controller.PID_Controller1.Proportional_Gain.Gain",Kv)


        
status = fmuM.setRealValue("Parameters.Converter_RMS_Controller.Ramp_limitation.Rate_Limiter.RisingSlewLimit", RP)

# obtain load flow values from powerfactory

P_0 = fmu.getRealValue('ElmGenstat.WPP.m:P:bus1')
Q_0 = fmu.getRealValue('ElmGenstat.WPP.m:Q:bus1')
V_0 = fmu.getRealValue('ElmGenstat.WPP.m:u1:bus1')
theta_0 = fmu.getRealValue('ElmGenstat.WPP.m:phiu1:bus1')
Pnom= fmu.getRealValue('ElmGenstat.WPP.e:Pnom')



        
# process
i_d_0 = P_0 / Pnom / V_0
i_q_0 = - Q_0 / Pnom / V_0 


fmuM.setRealValue("Parameters.Converter_RMS_Controller.PID_Controller.Integrator.InitialCondition", i_d_0)
fmuM.setRealValue("Parameters.Converter_RMS_Controller.PID_Controller1.Integrator.InitialCondition", i_q_0)



# Initialize the converter FMU.
status1 = fmuM.initialize() # initialize model
assert status1 == fmipp.fmiOK

# Id_ref = fmuM.getRealValue("Id_ref")
# Iq_ref = fmuM.getRealValue("Iq_ref")

Id_ref = fmuM.getRealValue("Id_ref")
Iq_ref = fmuM.getRealValue("Iq_ref")

        
# FRT controller initialisation

# inputs
#
#--------------------
# - Udc
# - VPCC
# - release

fmuF.setRealValue("Udc",fmuM.getRealValue("Vdc_pu"))
fmuF.setRealValue("VPCC",V_0)
fmuF.setBooleanValue("release",True)
fmuF.setRealValue("Qref_pu",Q_0/120.0)
        

        
# parameters
#
#--------------------
# dT: time step size of the simulation federate, check compatibility with co-simulation synchronisation step size
fmuF.setRealValue("Parameters.StateMachine_dT", step_size)

# RpS1: ramping rate when in state=1 (normal operation)
fmuF.setRealValue("Parameters.State_Machine.state_transition_RpS1", RP)

# RpS2: ramping rate when in state=2 (in FRT operation)
fmuF.setRealValue("Parameters.State_Machine.state_transition_RpS2", RP)

# RpS3: ramping rate when in state=3 (in post FRT operation), determines how long the converter will ramp up the active power and when it returns to normal operation, i.e., state=1
fmuF.setRealValue("Parameters.State_Machine.state_transition_RpS3", POSTRP)

# set the current limiting strategy for each of the states. 1.0: d-priority, 2.0: q-priority 

fmuF.setRealValue("Parameters.State_Machine.state_transition_CLMODES1", Iprio)
fmuF.setRealValue("Parameters.State_Machine.state_transition_CLMODES2", IprioFRT)
fmuF.setRealValue("Parameters.State_Machine.state_transition_CLMODES3", IprioPOSTFRT)

# set the additional reactive current injection gain for each state

fmuF.setRealValue("Parameters.State_Machine.state_transition_KBS1", 0.0)
fmuF.setRealValue("Parameters.State_Machine.state_transition_KBS2", KBOOST)
fmuF.setRealValue("Parameters.State_Machine.state_transition_KBS3", KBOOST)

# outputs
#
#--------------------
# - STATE
# - CLMODE
# - KaRCI
# - Rp

State = fmuF.getRealValue("STATE")
CLM = fmuF.getRealValue("CLMODE")
KaRCI = fmuF.getRealValue("KaRCI")
Rp = fmuF.getRealValue("Rp")

print "State = ", State
print "current limit mode = ", CLM
print "boosting gain = ", KaRCI      




# Run a simulation, changing the inputs at every synchronization step. Also, save outputs for plotting.
time = 0.
# step_size = 0.001

# data containers for results
res_time = [] # time steps
res_G1_angle = [] # rotor angle of G1 relative to reference machine angle
res_G2_angle = [] # rotor angle of G2 relative to reference machine angle
res_G1_speed = [] # rotor speed of G1 relative to reference machine angle
res_G2_speed = [] # rotor speed of G2 relative to reference machine angle
res_Bus_U = []
res_WPP_P = []
res_Id_ref = []
res_Iq_ref = []
res_I_out = []
res_State = [] # value of FRT state
res_CLM = []

t0=True

while ( time < stop_time ):
    # Make co-simulation step.
    new_step = True
    tP = fmuM.integrate( time + step_size) # integrate model
    tF = fmuF.integrate( time + step_size) # integrate model    
    status = fmu.doStep( time, step_size, new_step )
    assert status == fmipp.fmiOK

    # Advance time.
    time += step_size


    controllerOut = fmuM.getRealValue("Id_ref")

    Ppcc = fmu.getRealValue('ElmGenstat.WPP.m:Psum:bus1') / 120.0
    Vpcc = fmu.getRealValue( 'ElmGenstat.WPP.m:u1:bus1' )
    Qpcc = fmu.getRealValue('ElmGenstat.WPP.m:Q:bus1') / 120.0    
    iq_out = fmuM.getRealValue("Iq_ref")
    State = fmuF.getRealValue("STATE")
    CLM = fmuF.getRealValue("CLMODE")
    KaRCI = fmuF.getRealValue("KaRCI")
    Rp = fmuF.getRealValue("Rp")

    
    
    fmuM.setRealValue("V_pcc_RMS", Vpcc)
    fmuM.setRealValue("Qpcc", Qpcc)
    status = fmuF.setRealValue( 'VPCC', Vpcc)
        
    print('|'+32*'-'+' t = %5.2f s ' %time + 32*'-' +'|')
    print('terminal voltage of WPP = %s pu' %Vpcc)
    print('|'+77*'-'+'|')    

    #@TODO: we could take Pref out of the if statement as all the logic is inside the FRT controller now..
    if time<1.18:
        Pref=P_0/Pnom
        #status = fmu.setRealValue( 'EvtParam.VREF-SLOT.vrefin', 0.0)
    else:
        Pref=P_0/Pnom

        # reference value of Q (terminal)
        # fmuM.setRealValue("Vnom_Value_pm", 1.1)

        #status = fmu.setRealValue( 'EvtParam.VREF-SLOT.vrefin', 0.01)

    # current limit mode: limitation priority 1.0: d-priority, 2.0: q-priority 
    fmuM.setRealValue("I_lim", CLM)
    # ramping rate from FRT controller to converter controller
    fmuM.setRealValue("Parameters.Converter_RMS_Controller.Ramp_limitation.Rate_Limiter.RisingSlewLimit", Rp)
    # additional reactive current injection gain from FRT controller to convertere controller
    fmuM.setRealValue("K_aRCI",KaRCI)

        
    status = fmu.setRealValue( 'EvtParam.id_ref_slot.id_ref_in', controllerOut - i_d_0)
    assert status == fmipp.fmiOK
    status = fmu.setRealValue( 'EvtParam.iq_ref_slot.iq_ref_in', iq_out - i_q_0)
    assert status == fmipp.fmiOK


    # import pdb; pdb.set_trace()        
    # status = fmu.setRealValue( 'EvtParam.id_ref_slot.id_ref_in', i_d_0 - i_d_0)
    # assert status == fmipp.fmiOK
    # status = fmu.setRealValue( 'EvtParam.iq_ref_slot.iq_ref_in', i_q_0 - i_q_0)
    # assert status == fmipp.fmiOK
        
        
        
    # set reference value of active power infeed by static generator
    fmuM.setRealValue("Parameters.Converter_RMS_Controller.Vdc_ref__V_.Value", Pref)
    # set measured value of active power infeed into FMU-ME
    fmuM.setRealValue("Vdc_pu", Ppcc)

    # Get simulation results
    res_time.append( time )
    res_WPP_P.append( fmu.getRealValue( 'ElmGenstat.WPP.m:P:bus1' ) )
    res_Bus_U.append( fmu.getRealValue( 'ElmGenstat.WPP.m:u1:bus1' ) )
    res_G1_angle.append( fmu.getRealValue( 'ElmSym.G1.s:xphi' )*180.0/3.1415 )
    res_G2_angle.append( fmu.getRealValue( 'ElmSym.G2.s:xphi' )*180.0/3.1415 )
    res_G1_speed.append( fmu.getRealValue( 'ElmSym.G1.s:xspeed' ))
    res_G2_speed.append( fmu.getRealValue( 'ElmSym.G2.s:xspeed' ))
    res_Id_ref.append(controllerOut)
    res_Iq_ref.append(iq_out)
    res_I_out.append(np.sqrt(controllerOut**2 + iq_out**2))
    res_State.append(fmuF.getRealValue("STATE"))
    res_CLM.append(fmuF.getRealValue("CLMODE"))    


# uncomment code below to write simulation results to a csv file 
with open(EXPname, "wb") as f:
    writer = csv.writer(f)
    writer.writerow(res_time)
    writer.writerow(res_WPP_P)
    writer.writerow(res_G1_angle)
    writer.writerow(res_G2_angle)
    writer.writerow(res_G2_speed)
    writer.writerow(res_G1_speed)
    writer.writerow(res_Id_ref)
    writer.writerow(res_Iq_ref)
    writer.writerow(res_I_out)
    writer.writerow(res_Bus_U)
    writer.writerow(res_State)
    writer.writerow(res_CLM)

# Plot the results.
plt.figure(1)
plt.plot( res_time, res_G1_angle, 'b-',linewidth=4 )
plt.plot( res_time, res_G2_angle, 'r-',linewidth=4 )
plt.xlabel( 'simulation time in s' )
plt.ylabel( 'relative rotor angle of G1 and G2 in deg' )
plt.xlim( 0., stop_time)
plt.ylim( -100., 100. )


plt.figure(2)
plt.plot( res_time, res_G1_speed, 'b-',linewidth=4 )
plt.plot( res_time, res_G2_speed, 'r-',linewidth=4 )
plt.xlabel( 'simulation time in s' )
plt.ylabel( 'rotor speed deviation of G1 and G2 in pu' )
plt.xlim( 0., stop_time)
plt.ylim( 0.95 , 1.05 )


plt.figure(3)
plt.plot( res_time, res_WPP_P, 'b-',linewidth=4 )
plt.xlabel( 'simulation time in s' )
plt.ylabel( 'wind power plant output power' )
plt.xlim( 0., stop_time)
plt.ylim( 0., 140. )

plt.figure(4)
plt.plot( res_time, res_Bus_U, 'r-',linewidth=4)
plt.xlabel( 'simulation time in s' )
plt.ylabel( 'voltage at Bus GEN in p.u.' )
plt.ylim( 0., 1.5 )
plt.xlim( 0., stop_time)

plt.figure(5)
plt.plot( res_time, res_Id_ref, 'r-',linewidth=4)
plt.plot( res_time, res_Iq_ref, 'b-',linewidth=4)
plt.plot( res_time, res_I_out, 'k-',linewidth=4)
plt.xlabel( 'simulation time in s' )
plt.ylabel( 'id_ref in p.u.' )
plt.xlim( 0., stop_time)

        
# Plot the results.
plt.figure(6)
plt.plot( res_time, res_State, 'b-',linewidth=4 )
plt.xlabel( 'simulation time in s' )
plt.ylabel( 'converter FRT state' )
plt.xlim( 0., stop_time)
plt.ylim( -1., 5. )


plt.figure(7)
plt.plot( res_time, res_CLM, 'r-',linewidth=4)
plt.xlabel( 'simulation time in s' )
plt.ylabel( 'converter current limiting mode' )
plt.xlim( 0., stop_time)
plt.show()

