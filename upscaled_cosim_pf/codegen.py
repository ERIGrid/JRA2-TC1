#Put local path where you want to create yur new python file1
file1= open(r"upscaled.py",'w')

#Basic Plotting Parameters
file1.write("import os\n")
file1.write("import sys\n")
file1.write("import fmipp\n")
file1.write("import optparse\n\n")
file1.write("# Import FMI++ Python library.\n\n")
file1.write("import matplotlib.pyplot as plt\n")
file1.write("import csv\n")
file1.write("import numpy as np\n\n")
file1.write("Set1Red='#e41a1c'\n")
file1.write("Set1Blue='#377eb8'\n")
file1.write("Set1Green='#4daf4a'\n")
file1.write("Set1Purple='#984ea3'\n")
file1.write("Set1Orange='#ff7f00'\n")
file1.write("Set1Yellow='#ffff33'\n")
file1.write("Set1Brown='#a65628'\n")
file1.write("Set1Pink='#f781bf'\n")
file1.write("Set1Gray='#999999'\n")
file1.write("lw=2\n")
file1.write("colorOM=Set1Red\n\n")
file1.write("# voltage control gain\n")
file1.write("Kv=0.0\n")
file1.write("# voltage control integrator gain\n")
file1.write("KiV=10\n")
file1.write("# per unit current limit of the converter\n")
file1.write("Ilim=1.1\n")
file1.write("# current limiting priority during normal operation\n")
file1.write("Iprio=2\n")
file1.write("# current limiting priority during FRT\n")
file1.write("IprioFRT=2\n")
file1.write("# current limiting priority during post-FRT\n")
file1.write("IprioPOSTFRT=1\n")
file1.write("# d-axis current slew rate (pu/s) during normal operation\n")
file1.write("RP=100\n")
file1.write("# d-axis current slew rate (pu/s) during post-FRT\n")
file1.write("POSTRP=0.5\n")
file1.write("# additional reactive current injection 'boosting' gain, kicks in during fault\n")
file1.write("KBOOST=1.0\n")
file1.write("# export results name\n")
file1.write("EXPname = 'KBOOST=1_Ilim=11_PRIO=2_POSTRP=05.csv'\n")
file1.write("# F M U  P A R A M E T E R S\n")
file1.write("work_dir=os.getcwd()\n")
file1.write("logging_on = False\n\n")


#Creating all 33 instances of FRT Controllers
for i in range(1,33):
    file1.write("#FRT Controller for WT_%i\n"%(i))
    file1.write("model_name_F_%i='FRTController_mar_v2_sf'\n"%(i))
    file1.write("stop_before_event = False\n")
    file1.write("event_search_precision = 1e-10\n")
    file1.write("integrator_type = fmipp.eu\n")

for i in range(1,33):
    file1.write("path_to_fmu_F_%i = os.path.join(work_dir, model_name_F_%i + '.fmu')\n"%(i,i))

for i in range(1,33):
    file1.write("# Extract FMU and retrieve URI to directory.\n")
    file1.write("uri_to_extracted_fmu_F_%i= fmipp.extractFMU( path_to_fmu_F_%i, work_dir )\n"%(i,i))

for i in range(1,33):
    file1.write("# using the FMI 2.0 specification\n")
    file1.write("fmuF_%i = fmipp.FMUModelExchangeV2(uri_to_extracted_fmu_F_%i, model_name_F_%i, logging_on, stop_before_event, event_search_precision, integrator_type )\n"%(i,i,i))

for i in range(1,33):
    file1.write("# Instantiate the FMU.\n")
    file1.write("status%i = fmuF_%i.instantiate( 'my_FRT_controller') # instantiate model\n"%(i,i))

for i in range(1,33):
    file1.write("assert status%i == fmipp.fmiOK\n"%(i))

for i in range(1,33):
    file1.write("# Initialize the FMU%i\n"%(i))
    file1.write("status%i = fmuF_%i.initialize() # initialize model\n"%(i,i))
    file1.write("assert status%i == fmipp.fmiOK\n\n\n"%(i))

#Creating all 33 instances of MATLAB Controllers
for i in range(1,33):
    file1.write("#Converter Controller for WT_%i\n"%(i))
    file1.write("model_name_M_%i='RmsConverterController_AAvdM_R2014b_sf'\n"%(i))
    file1.write("stop_before_event = False\n")
    file1.write("event_search_precision = 1e-10\n")
    file1.write("integrator_type = fmipp.dp\n")

for i in range(1,33):
    file1.write("path_to_fmu_M_%i = os.path.join(work_dir, model_name_M_%i + '.fmu')\n"%(i,i))

for i in range(1,33):
    file1.write("# Extract FMU and retrieve URI to directory.\n")
    file1.write("uri_to_extracted_fmu_M_%i= fmipp.extractFMU( path_to_fmu_M_%i, work_dir )\n"%(i,i))

for i in range(1,33):
    file1.write("# using the FMI 2.0 specification\n")
    file1.write("fmuM_%i = fmipp.FMUModelExchangeV2(uri_to_extracted_fmu_M_%i, model_name_M_%i, logging_on, stop_before_event, event_search_precision, integrator_type )\n"%(i,i,i))

for i in range(1,33):
    file1.write("status%i = fmuM_%i.instantiate( 'my_RMS_controller') # instantiate model\n"%(i,i))

for i in range(1,33):
    file1.write("assert status%i == fmipp.fmiOK\n\n\n"%(i))


#Creating PowerFactory FMU
file1.write("#Second FMI-CS from PowerFactory\n")
file1.write("model_name = 'upscaled'\n")
file1.write("time_diff_resolution = 1e-9\n")
file1.write("# Specify path to the FMU (located in subdirectory 'NineBusSystem-resources' of the current working directory).\n")
file1.write("path_to_fmu = os.path.join( work_dir, model_name + '.fmu' )\n")
file1.write("# Extract FMU and retrieve URI to directory.\n")
file1.write("uri_to_extracted_fmu = fmipp.extractFMU( path_to_fmu, work_dir )\n")
file1.write("# Create an instance of class FMUCoSimulation (handle for the FMU).\n")
file1.write("fmu = fmipp.FMUCoSimulationV1( uri_to_extracted_fmu, model_name, logging_on, time_diff_resolution )\n")
file1.write("# Instantiate the FMU.\n")
file1.write("start_time = 0.\n")
file1.write("instance_name = 'upscaled'\n")
file1.write("visible = False\n")
file1.write("interactive = False\n")
file1.write("status = fmu.instantiate( instance_name, start_time, visible, interactive )\n")
file1.write("assert status == fmipp.fmiOK\n")
file1.write("# Initialize the FMU.\n")
file1.write("stop_time = 2\n")
file1.write("stop_time_defined = True\n")
file1.write("step_size = 0.005\n")
file1.write("status = fmu.initialize( start_time, stop_time_defined, stop_time )\n")
file1.write("assert status == fmipp.fmiOK\n")
for i in range(1,33):
    file1.write("Pn_%i= fmu.getRealValue('ElmGenstat.WT_%i.e:Pnom')\n"%(i,i))

#FRT Control Parameters
for i in range(1,33):
    file1.write("# WT_%i FRT control\n"%(i))
    file1.write("# K_aRCI: boosting gain\n")
    file1.write("fmuM_%i.setRealValue('K_aRCI',KBOOST)\n"%(i))
    file1.write("# R_on: rate limiter switch 1.0: on, 0.0: off\n")
    file1.write("fmuM_%i.setRealValue('R_on',1.0)\n"%(i))
    file1.write("# R_p: maximum ramping rate\n")
    file1.write("fmuM_%i.setRealValue('R_p', 10.0)\n"%(i))
    file1.write("# I_lim: limitation priority 1.0: d-priority, 2.0: q-priority \n")
    file1.write("fmuM_%i.setRealValue('I_lim', Iprio)\n"%(i))
    file1.write("# d-axis voltage (pu)\n")
    file1.write("fmuM_%i.setRealValue('Qpcc', fmu.getRealValue('ElmGenstat.WT_%i.m:Q:bus1') / Pn_%i)\n"%(i,i,i))
    file1.write("# q-axis voltage (pu, unused)\n")
    file1.write("fmuM_%i.setRealValue('Vq', 0.0)\n"%(i))
    file1.write("# RMS voltage at PCC (pu)\n")
    file1.write("fmuM_%i.setRealValue('V_pcc_RMS', fmu.getRealValue('ElmGenstat.WT_%i.m:u1:bus1'))\n"%(i,i))
    file1.write("# reference value of Q (terminal)\n")
    file1.write("fmuM_%i.setRealValue('Qref_pu', fmu.getRealValue('ElmGenstat.WT_%i.m:Q:bus1') / Pn_%i)\n"%(i,i,i))
    file1.write("# dc voltage (pu)\n")
    file1.write("fmuM_%i.setRealValue('Vdc_pu', 1.0)\n"%(i))

#Limiter Values
file1.write("maxCurrent=Ilim\n")
for i in range(1,33):
    file1.write("fmuM_%i.setRealValue('Parameters.Converter_RMS_Controller.Saturation.UpperLimit',maxCurrent)\n"%(i))
    file1.write("fmuM_%i.setRealValue('Parameters.Converter_RMS_Controller.Saturation.LowerLimit',-maxCurrent)\n"%(i))
    file1.write("fmuM_%i.setRealValue('Parameters.Converter_RMS_Controller.PID_Controller.Saturate.UpperLimit',maxCurrent)\n"%(i))
    file1.write("fmuM_%i.setRealValue('Parameters.Converter_RMS_Controller.PID_Controller.Saturate.LowerLimit',-maxCurrent)\n"%(i))
    file1.write("fmuM_%i.setRealValue('Parameters.Converter_RMS_Controller.PID_Controller1.Saturate.UpperLimit',maxCurrent)\n"%(i))
    file1.write("fmuM_%i.setRealValue('Parameters.Converter_RMS_Controller.Riferimento_Q1.Saturation.UpperLimit',maxCurrent)\n"%(i))
    file1.write("fmuM_%i.setRealValue('Parameters.Converter_RMS_Controller.Riferimento_Q1.Saturation.LowerLimit',-maxCurrent)\n"%(i))
    file1.write("fmuM_%i.setRealValue('Parameters.Converter_RMS_Controller.V_nom.Value', fmu.getRealValue('ElmGenstat.WT_%i.m:u1:bus1'))\n\n"%(i,i))
    file1.write("fmuM_%i.setRealValue('Parameters.Converter_RMS_Controller.PID_Controller.Integral_Gain.Gain', 1)\n"%(i))
    file1.write("fmuM_%i.setRealValue('Parameters.Converter_RMS_Controller.PID_Controller.Proportional_Gain.Gain',0.0)\n"%(i))
    file1.write("fmuM_%i.setRealValue('Parameters.Converter_RMS_Controller.PID_Controller1.Integral_Gain.Gain',KiV)\n"%(i))
    file1.write("fmuM_%i.setRealValue('Parameters.Converter_RMS_Controller.PID_Controller1.Proportional_Gain.Gain',Kv)\n"%(i))
    file1.write("status%i = fmuM_%i.setRealValue('Parameters.Converter_RMS_Controller.Ramp_limitation.Rate_Limiter.RisingSlewLimit', RP)\n"%(i,i))

#Obtaining Vnom values
file1.write("#Obtaining Vnom values\n")
for i in range(1,33):
     file1.write("Vnom_%i = fmuM_%i.getRealValue('Parameters.Converter_RMS_Controller.V_nom.Value')\n"%(i,i))

#Obtaining Loadflow values from PowerFactory
file1.write("#Obtaining Loadflow values from PowerFactory\n")
for i in range(1,33):
    file1.write("P_0_%i = fmu.getRealValue('ElmGenstat.WT_%i.m:P:bus1')\n"%(i,i))
    file1.write("Q_0_%i = fmu.getRealValue('ElmGenstat.WT_%i.m:Q:bus1')\n"%(i,i))
    file1.write("V_0_%i = fmu.getRealValue('ElmGenstat.WT_%i.m:u1:bus1')\n"%(i,i))
    file1.write("theta_0_%i = fmu.getRealValue('ElmGenstat.WT_%i.m:phiu1:bus1')\n"%(i,i))
    file1.write("Pnom_%i= fmu.getRealValue('ElmGenstat.WT_%i.e:Pnom')\n"%(i,i))

#processes
file1.write("#processes\n")
for i in range(1,33):
    file1.write("i_d_0_%i = P_0_%i / Pnom_%i/ V_0_%i\n"%(i,i,i,i))
    file1.write("i_q_0_%i = - Q_0_%i / Pnom_%i / V_0_%i\n"%(i,i,i,i))

for i in range(1,33):
    file1.write("fmuM_%i.setRealValue('Parameters.Converter_RMS_Controller.PID_Controller.Integrator.InitialCondition', i_d_0_%i)\n"%(i,i))
    file1.write("fmuM_%i.setRealValue('Parameters.Converter_RMS_Controller.PID_Controller1.Integrator.InitialCondition', i_q_0_%i)\n"%(i,i))

#Initialisation of FMU's
file1.write("#Initialisation of FMU's\n")
for i in range(1,33):
    file1.write("status%i = fmuM_%i.initialize()\n"%(i,i))
    file1.write("assert status%i == fmipp.fmiOK\n"%(i))
    file1.write("Id_ref_%i = fmuM_%i.getRealValue('Id_ref')\n"%(i,i))
    file1.write("Iq_ref_%i = fmuM_%i.getRealValue('Iq_ref')\n"%(i,i))

#Controller Initialisation
file1.write("#Controller Initialisaton\n")
for i in range(1,33):
    file1.write("fmuF_%i.setRealValue('Udc',fmuM_%i.getRealValue('Vdc_pu'))\n"%(i,i))
    file1.write("fmuF_%i.setRealValue('VPCC',V_0_%i)\n"%(i,i))
    file1.write("fmuF_%i.setBooleanValue('release',True)\n"%(i))
    file1.write("fmuF_%i.setRealValue('Qref_pu',Q_0_%i/Pn_%i)\n"%(i,i,i))

file1.write("# dT: time step size of the simulation federate, check compatibility with co-simulation synchronisation step size\n")
for i in range(1,33):
    file1.write("fmuF_%i.setRealValue('Parameters.StateMachine_dT', step_size)\n"%(i))

file1.write("# RpS1: ramping rate when in state=1 (normal operation)\n")
for i in range(1,33):
    file1.write("fmuF_%i.setRealValue('Parameters.State_Machine.state_transition_RpS1', RP)\n"%(i))

file1.write("# RpS2: ramping rate when in state=2 (in FRT operation)\n")
for i in range(1,33):
    file1.write("fmuF_%i.setRealValue('Parameters.State_Machine.state_transition_RpS2', RP)\n"%(i))

file1.write("# RpS3: ramping rate when in state=3 (in post FRT operation), determines how long the converter will ramp up the active power and when it returns to normal operation, i.e., state=1\n")
for i in range(1,33):
    file1.write("fmuF_%i.setRealValue('Parameters.State_Machine.state_transition_RpS3', POSTRP)\n"%(i))

file1.write("# set the current limiting strategy for each of the states. 1.0: d-priority, 2.0: q-priority\n")
for i in range(1,33):
    file1.write("fmuF_%i.setRealValue('Parameters.State_Machine.state_transition_CLMODES1', Iprio)\n"%(i))
    file1.write("fmuF_%i.setRealValue('Parameters.State_Machine.state_transition_CLMODES2', IprioFRT)\n"%(i))
    file1.write("fmuF_%i.setRealValue('Parameters.State_Machine.state_transition_CLMODES3', IprioPOSTFRT)\n"%(i))

file1.write("# set the additional reactive current injection gain for each state\n")
for i in range(1,33):
    file1.write("fmuF_%i.setRealValue('Parameters.State_Machine.state_transition_KBS1', 0.0)\n"%(i))
    file1.write("fmuF_%i.setRealValue('Parameters.State_Machine.state_transition_KBS2', KBOOST)\n"%(i))
    file1.write("fmuF_%i.setRealValue('Parameters.State_Machine.state_transition_KBS3', KBOOST)\n"%(i))

#Outputs
file1.write("#Outputs\n")
for i in range(1,33):
    file1.write("State_%i = fmuF_%i.getRealValue('STATE')\n"%(i,i))
    file1.write("CLM_%i = fmuF_%i.getRealValue('CLMODE')\n"%(i,i))
    file1.write("KaRCI_%i = fmuF_%i.getRealValue('KaRCI')\n"%(i,i))
    file1.write("Rp_%i = fmuF_%i.getRealValue('Rp')\n"%(i,i))
    file1.write("print 'State = ', State_%i\n"%(i))
    file1.write("print 'current limit mode = ', CLM_%i\n"%(i))
    file1.write("print 'boosting gain = ', KaRCI_%i\n\n"%(i))

#Simulation Run
file1.write("time = 0.\n")
file1.write("step_size = 0.01\n")

#Data Container for results
file1.write("#Data Container for results\n")
file1.write("res_time = [] # time steps\n")
file1.write("res_G1_angle = [] # rotor angle of G1 relative to reference machine angle\n")
file1.write("res_G2_angle = [] # rotor angle of G2 relative to reference machine angle\n")
file1.write("res_G1_speed = [] # rotor speed of G1 relative to reference machine angle\n")
file1.write("res_G2_speed = [] # rotor speed of G2 relative to reference machine angle\n")
file1.write("res_Bus9_U= []\n")
file1.write("res_TR_P= []\n")

for i in range(1,33):
    file1.write("res_Bus_U_%i = []\n"%(i))
    file1.write("res_WT_%i_P_%i = []\n"%(i,i))
    file1.write("res_Id_ref_%i = []\n"%(i))
    file1.write("res_Iq_ref_%i = []\n"%(i))
    file1.write("res_I_out_%i = []\n"%(i))
    file1.write("res_State_%i = [] # value of FRT state\n"%(i))
    file1.write("res_CLM_%i = []\n\n"%(i))
    file1.write("res_Vpcc_%i=[]\n"%(i))
    file1.write("res_Vdiff_%i=[]\n"%(i))
    file1.write("res_Vnom_%i=[]\n"%(i))

file1.write("t0=True\n")

#Running Co-sim
file1.write("while ( time < stop_time ):\n")
file1.write("    new_step = True\n")
for i in range(1,33):
    file1.write("    tP_%i = fmuM_%i.integrate( time + step_size) # integrate model\n"%(i,i))

for i in range(1,33):
    file1.write("    tF_%i = fmuF_%i.integrate( time + step_size) # integrate model \n"%(i,i))

file1.write("    status = fmu.doStep( time, step_size, new_step )\n")
file1.write("    assert status == fmipp.fmiOK\n")

# Advance time.
file1.write("    time += step_size\n\n")

for i in range(1,33):
    file1.write("    controllerOut_%i = fmuM_%i.getRealValue('Id_ref')\n"%(i,i))

for i in range(1,33):
    file1.write("    Ppcc_%i = fmu.getRealValue('ElmGenstat.WT_%i.m:Psum:bus1') / Pnom_%i\n"%(i,i,i))
    file1.write("    Vpcc_%i = fmu.getRealValue( 'ElmGenstat.WT_%i.m:u1:bus1')\n"%(i,i))
    file1.write("    Qpcc_%i = fmu.getRealValue('ElmGenstat.WT_%i.m:Q:bus1') / Pnom_%i\n"%(i,i,i))
    file1.write("    iq_out_%i = fmuM_%i.getRealValue('Iq_ref')\n"%(i,i))
    file1.write("    State_%i = fmuF_%i.getRealValue('STATE')\n"%(i,i))
    file1.write("    CLM_%i = fmuF_%i.getRealValue('CLMODE')\n"%(i,i))
    file1.write("    KaRCI_%i = fmuF_%i.getRealValue('KaRCI')\n"%(i,i))
    file1.write("    Rp_%i = fmuF_%i.getRealValue('Rp')\n\n"%(i,i))

for i in range(1,33):
    file1.write("    fmuM_%i.setRealValue('V_pcc_RMS', Vpcc_%i)\n"%(i,i))
    file1.write("    fmuM_%i.setRealValue('Qpcc', Qpcc_%i)\n"%(i,i))
    file1.write("    status%i = fmuF_%i.setRealValue( 'VPCC', Vpcc_%i)\n\n"%(i,i,i))
    file1.write("    Vdef_%i=(Vnom_%i-Vpcc_%i)\n\n"%(i,i,i))

for i in range(1,33):
    file1.write("    print('|'+33*'-'+' t = %5.2f s ' %time + 33*'-' +'|')\n")
    file1.write("    print('terminal voltage of WT_%i = %%s pu' %%Vpcc_%i)\n"%(i,i))
    file1.write("    print('|'+77*'-'+'|')\n")

# Calculations
file1.write("    if time<0.18:\n")
for i in range(1,33):
    file1.write("        Pref_%i=P_0_%i/Pnom_%i\n"%(i,i,i))

file1.write("    else:\n")
for i in range(1,33):
    file1.write("        Pref_%i=P_0_%i/Pnom_%i\n"%(i,i,i))

file1.write("    # current limit mode: limitation priority 1.0: d-priority, 2.0: q-priority\n")
for i in range(1,33):
    file1.write("    fmuM_%i.setRealValue('I_lim', CLM_%i)\n"%(i,i))

file1.write("    # ramping rate from FRT controller to converter controller\n")
for i in range(1,33):
    file1.write("    fmuM_%i.setRealValue('Parameters.Converter_RMS_Controller.Ramp_limitation.Rate_Limiter.RisingSlewLimit', Rp_%i)\n"%(i,i))

file1.write("    # additional reactive current injection gain from FRT controller to convertere controller\n")
for i in range(1,33):
    file1.write("    fmuM_%i.setRealValue('K_aRCI',KaRCI_%i)\n"%(i,i))

for i in range(1,33):
    file1.write("    status%i = fmu.setRealValue( 'EvtParam.WTframe_%i.id_ref_in', controllerOut_%i - i_d_0_%i)\n"%(i,i,i,i))
    file1.write("    assert status%i == fmipp.fmiOK\n"%(i))

for i in range(1,33):
    file1.write("    status%i = fmu.setRealValue( 'EvtParam.WTframe_%i.iq_ref_in', iq_out_%i - i_q_0_%i)\n"%(i,i,i,i))
    file1.write("    assert status%i == fmipp.fmiOK \n"%(i))

file1.write("    # set reference value of active power infeed by static generator\n")
for i in range(1,33):
    file1.write("    fmuM_%i.setRealValue('Parameters.Converter_RMS_Controller.Vdc_ref__V_.Value', Pref_%i)\n"%(i,i))

file1.write("    # set measured value of active power infeed into FMU-ME\n")
for i in range(1,33):
    file1.write("    fmuM_%i.setRealValue('Vdc_pu', Ppcc_%i)\n"%(i,i))

#Getting Simulation Results
file1.write("    # Get simulation results\n")
file1.write("    res_time.append( time )\n")
file1.write("    res_G1_angle.append( fmu.getRealValue( 'ElmSym.G1.s:xphi' )*180.0/3.1415 )\n")
file1.write("    res_G2_angle.append( fmu.getRealValue( 'ElmSym.G2.s:xphi' )*180.0/3.1415 )\n")
file1.write("    res_G1_speed.append( fmu.getRealValue( 'ElmSym.G1.s:xspeed' ))\n")
file1.write("    res_G2_speed.append( fmu.getRealValue( 'ElmSym.G2.s:xspeed' ))\n")
file1.write("    res_Bus9_U.append( fmu.getRealValue( 'ElmTerm.Bus9.m:u' ))\n")
file1.write("    res_TR_P.append( fmu.getRealValue( 'ElmTr2.TWPP.m:Psum:buslv' ))\n")

for i in range(1,33):
    file1.write("    res_WT_%i_P_%i.append( fmu.getRealValue( 'ElmGenstat.WT_%i.m:P:bus1' ) )\n"%(i,i,i))
    file1.write("    res_Bus_U_%i.append( fmu.getRealValue( 'ElmGenstat.WT_%i.m:u1:bus1' ) )\n"%(i,i))
    file1.write("    res_Id_ref_%i.append(controllerOut_%i)\n"%(i,i))
    file1.write("    res_Iq_ref_%i.append(iq_out_%i)\n"%(i,i))
    file1.write("    res_I_out_%i.append(np.sqrt(controllerOut_%i**2 + iq_out_%i**2))\n"%(i,i,i))
    file1.write("    res_State_%i.append(fmuF_%i.getRealValue('STATE'))\n"%(i,i))
    file1.write("    res_CLM_%i.append(fmuF_%i.getRealValue('CLMODE'))\n"%(i,i))
    file1.write("    res_Vdiff_%i.append(Vdef_%i)\n"%(i,i))
    file1.write("    res_Vpcc_%i.append(Vpcc_%i)\n"%(i,i))
    file1.write("    res_Vnom_%i.append(Vnom_%i)\n"%(i,i))

#Writing results
file1.write("# uncomment code below to write simulation results to a csv file\n")
file1.write("with open(EXPname, 'wb') as f:\n")
file1.write("    writer = csv.writer(f)\n")
file1.write("    writer.writerow(res_time)\n")
file1.write("    writer.writerow(res_G1_angle)\n")
file1.write("    writer.writerow(res_G2_angle)\n")
file1.write("    writer.writerow(res_G2_speed)\n")
file1.write("    writer.writerow(res_G1_speed)\n")
file1.write("    writer.writerow(res_Bus9_U)\n")
file1.write("    writer.writerow(res_TR_P)\n")

for i in range(1,33):
    file1.write("    writer.writerow(res_WT_%i_P_%i)\n"%(i,i))
    file1.write("    writer.writerow(res_Id_ref_%i)\n"%(i))
    file1.write("    writer.writerow(res_Iq_ref_%i)\n"%(i))
    file1.write("    writer.writerow(res_I_out_%i)\n"%(i))
    file1.write("    writer.writerow(res_Bus_U_%i)\n"%(i))
    file1.write("    writer.writerow(res_State_%i)\n"%(i))
    file1.write("    writer.writerow(res_CLM_%i)\n"%(i))
    file1.write("    writer.writerow(res_Vdiff_%i)\n"%(i))
    file1.write("    writer.writerow(res_Vpcc_%i)\n"%(i))
    file1.write("    writer.writerow(res_Vnom_%i)\n"%(i))

#Plotting Results
file1.write("# Plot the results.\n")
file1.write("plt.figure(1)\n")
file1.write("plt.plot( res_time, res_G1_angle, 'b-',linewidth=4 )\n")
file1.write("plt.plot( res_time, res_G2_angle, 'r-',linewidth=4 )\n")
file1.write("plt.xlabel( 'simulation time in s' )\n")
file1.write("plt.ylabel( 'relative rotor angle of G1 and G2 in deg' )\n")
file1.write("plt.xlim( 0., stop_time)\n")
file1.write("plt.ylim( -100., 100. )\n")
file1.write('plt.legend(["G1","G2"] )\n')
file1.write(r"plt.savefig(r'C:\Users\LocalAdmin\Desktop\WG-TC1\Upscaledfinal\Upscaled_final Plots\fig1.png')")
file1.write("\n")

file1.write("plt.figure(2)\n")
file1.write("plt.plot( res_time, res_G1_speed, 'b-',linewidth=4 )\n")
file1.write("plt.plot( res_time, res_G2_speed, 'r-',linewidth=4 )\n")
file1.write("plt.xlabel( 'simulation time in s' )\n")
file1.write("plt.ylabel( 'rotor speed deviation of G1 and G2 in pu' )\n")
file1.write("plt.xlim( 0., stop_time)\n")
file1.write("plt.ylim( 0.95 , 1.05 )\n")
file1.write('plt.legend(["G1","G2"] )\n')
file1.write(r"plt.savefig(r'C:\Users\LocalAdmin\Desktop\WG-TC1\Upscaledfinal\Upscaled_final Plots\fig2.png')")
file1.write("\n")

count = 3
for i in range(1,33):
    file1.write("plt.figure(%i)\n"%(count))
    file1.write("plt.plot( res_time, res_WT_%i_P_%i, 'b-',linewidth=4 )\n"%(i,i))
    file1.write("plt.xlabel( 'simulation time in s' )\n")
    file1.write("plt.ylabel( 'wind turbine %i output power' )\n"%(i))
    file1.write("plt.xlim( 0., stop_time)\n")
    #file1.write("plt.ylim( 0., 140. )\n")
    file1.write(r"plt.savefig(r'C:\Users\LocalAdmin\Desktop\WG-TC1\Upscaledfinal\Upscaled_final Plots\fig%i.png')"%(count))
    file1.write("\n")
    count+=1

    file1.write("plt.figure(%i)\n"%(count))
    file1.write("plt.plot( res_time, res_Bus_U_%i, 'r-',linewidth=4)\n"%(i))
    file1.write("plt.xlabel( 'simulation time in s' )\n")
    file1.write("plt.ylabel( 'voltage at Bus GEN (WT_%i) in p.u.' )\n"%(i))
    #file1.write("plt.ylim( 0., 1.5 )\n")
    file1.write("plt.xlim( 0., stop_time)\n")
    file1.write(r"plt.savefig(r'C:\Users\LocalAdmin\Desktop\WG-TC1\Upscaledfinal\Upscaled_final Plots\fig%i.png')"%(count))
    file1.write("\n")
    count+=1

    file1.write("plt.figure(%i)\n"%(count))
    file1.write("plt.plot( res_time, res_Id_ref_%i, 'r-',linewidth=4)\n"%(i))
    file1.write("plt.plot( res_time, res_Iq_ref_%i, 'b-',linewidth=4)\n"%(i))
    file1.write("plt.plot( res_time, res_I_out_%i, 'k-',linewidth=4)\n"%(i))
    file1.write("plt.xlabel( 'simulation time in s' )\n")
    file1.write("plt.ylabel( 'WT_%i Currents in p.u.' )\n"%(i))
    file1.write("plt.xlim( 0., stop_time)\n")
    file1.write('plt.legend(["Id","Iq","Iout"] )\n')
    file1.write(r"plt.savefig(r'C:\Users\LocalAdmin\Desktop\WG-TC1\Upscaledfinal\Upscaled_final Plots\fig%i.png')"%(count))
    file1.write("\n")
    count+=1

    file1.write("plt.figure(%i)\n"%(count))
    file1.write("plt.plot( res_time, res_State_%i, 'b-',linewidth=4 )\n"%(i))
    file1.write("plt.xlabel( 'simulation time in s' )\n")
    file1.write("plt.ylabel( 'converter FRT state of WT_%i' )\n"%(i))
    file1.write("plt.xlim( 0., stop_time)\n")
    #file1.write("plt.ylim( -1., 5. )\n")
    file1.write(r"plt.savefig(r'C:\Users\LocalAdmin\Desktop\WG-TC1\Upscaledfinal\Upscaled_final Plots\fig%i.png')"%(count))
    file1.write("\n")
    count+=1

    file1.write("plt.figure(%i)\n"%(count))
    file1.write("plt.plot( res_time, res_CLM_%i, 'r-',linewidth=4)\n"%(i))
    file1.write("plt.xlabel( 'simulation time in s' )\n")
    file1.write("plt.ylabel( 'converter current limiting mode of WT_%i' )\n"%(i))
    file1.write("plt.xlim( 0., stop_time)\n")
    file1.write(r"plt.savefig(r'C:\Users\LocalAdmin\Desktop\WG-TC1\Upscaledfinal\Upscaled_final Plots\fig%i.png')"%(count))
    file1.write("\n")
    count+=1

    file1.write("plt.figure(%i)\n"%(count))
    file1.write("plt.plot( res_time, res_Vdiff_%i, 'r-',linewidth=4)\n"%(i))
    file1.write("plt.plot( res_time, res_Vpcc_%i, 'b-',linewidth=4)\n"%(i))
    file1.write("plt.plot( res_time, res_Vnom_%i, 'k-',linewidth=4)\n"%(i))
    file1.write("plt.xlabel( 'simulation time in s' )\n")
    file1.write("plt.ylabel( 'Voltages of WT_%i' )\n"%(i))
    file1.write("plt.xlim( 0., stop_time)\n")
    file1.write('plt.legend(["Vdiff","Vpcc","Vnom"] )\n')
    file1.write(r"plt.savefig(r'C:\Users\LocalAdmin\Desktop\WG-TC1\Upscaledfinal\Upscaled_final Plots\fig%i.png')"%(count))
    file1.write("\n")
    count+=1

#file1.write("plt.show()\n")

file1.close()
