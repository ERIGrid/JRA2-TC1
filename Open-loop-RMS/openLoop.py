# Import FMI++ Python library.
import fmipp
import os
import sys
import matplotlib.pyplot as plt


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
# F M U  P A R A M E T E R S 
#------------------------------------------------------------------------------


work_dir=os.getcwd()
logging_on = False


#------------------------------------------------------------------------------
# the matlab controller
#------------------------------------------------------------------------------

model_name_M='RmsConverterController_R2014b_sf'
stop_before_event = False
event_search_precision = 1e-10
integrator_type = fmipp.eu

path_to_fmu_M = os.path.join(work_dir, model_name_M + '.fmu')
# Extract FMU and retrieve URI to directory.
uri_to_extracted_fmu_M= fmipp.extractFMU( path_to_fmu_M, work_dir )
# using the FMI 2.0 specification
fmuM = fmipp.FMUModelExchangeV2(uri_to_extracted_fmu_M, model_name_M, logging_on, stop_before_event, event_search_precision, integrator_type )
# Instantiate the FMU.
status1 = fmuM.instantiate( "my_RMS_controller" ) # instantiate model


assert status1 == fmipp.fmiOK
# Initialize the FMU.
status1 = fmuM.initialize() # initialize model
assert status1 == fmipp.fmiOK




# Initialize the FMU.
stop_time = 20.
stop_time_defined = True

# status = fmu.initialize( start_time, stop_time_defined, stop_time )
# assert status == fmipp.fmiOK


# Run a simulation, changing the inputs at every synchronization step. Also, save outputs for plotting.
time = 0.
step_size = 0.05

# data containers for results
res_time = [] # time steps
res_Id_ref = [] # rotor angle of G1 relative to reference machine angle
res_Iq_ref = []

# inputs

# set the FRT control 
fmuM.setRealValue("K_aRCI",0.0)
fmuM.setRealValue("R_on",0.0)
fmuM.setRealValue("R_p", 10.0)
fmuM.setRealValue("I_lim", 1.1)
fmuM.setRealValue("Vd", 1.0)
fmuM.setRealValue("Vq", 0.0)
fmuM.setRealValue("V_pcc_RMS", 1.0)
fmuM.setRealValue("Qref_pu", 0.0)
fmuM.setRealValue("Vdc_pu", 1.0)



# outputs

Id_ref = fmuM.getRealValue("Id_ref")
Iq_ref = fmuM.getRealValue("Iq_ref")

print "Id_ref = ", Id_ref
print "Iq_ref = ", Iq_ref

t0=True

while ( time < stop_time ):
    # Make co-simulation step.
    new_step = True
    tP = fmuM.integrate( time + step_size) # integrate model
    # status = fmuM.doStep( time, step_size, new_step )
    # assert status == fmipp.fmiOK
    
    # Advance time.
    time += step_size
    print('t = %s s' %time)

    if time<1.0:
        Vpcc=1.0
        vd=1.0
        #status = fmu.setRealValue( 'EvtParam.VREF-SLOT.vrefin', 0.0)
    else:
        Vpcc=1.00
        vd=0.1
        #status = fmu.setRealValue( 'EvtParam.VREF-SLOT.vrefin', 0.01)

    #status = fmuM.setRealValue( 'V_pcc_RMS', Vpcc)        
    status = fmuM.setRealValue( 'Vd', vd)
    assert status == fmipp.fmiOK

    # Get simulation results
    res_time.append( time )
    res_Id_ref.append(fmuM.getRealValue("Id_ref"))
    res_Iq_ref.append(fmuM.getRealValue("Iq_ref"))    

# import ipdb; ipdb.set_trace()
    
# Plot the results.
plt.plot( res_time, res_Id_ref, 'b-',linewidth=4 )
plt.xlabel( 'simulation time in s' )
plt.ylabel( 'd-axis current reference in pu' )
plt.xlim( 0., stop_time)
plt.ylim( -1., 1. )
plt.show()


plt.plot( res_time, res_Id_ref, 'r-',linewidth=4)
plt.xlabel( 'simulation time in s' )
plt.ylabel( 'q-axis reference current in p.u.' )
plt.xlim( 0., stop_time)
plt.show()

# Done.
