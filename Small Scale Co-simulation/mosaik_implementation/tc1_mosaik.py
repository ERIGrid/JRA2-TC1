import mosaik

# Employed simulators
sim_config = {
    'FMUME': {
        'python': 'mosaik_fmume_test.mosaik_fmi:FmuMeAdapter',
    },
    'FMUCS': {
        'python': 'mosaik_fmume_test.mosaik_fmi_cs:FmuCsAdapter',
    },
    'fault': {
        'python': 'fault_sim:FaultSim'
    },
    'modif': {
        'python': 'modif_comp:ModComp'
    },
    'DB': {
        'cmd': 'mosaik-hdf5 %(addr)s',
    }
}

mosaik_config = {
    'addr': ('127.0.0.1', 5555),
    'start_timeout': 30,
    'stop_timeout': 30,
}

END = 1000

# Working directories for FMUs to be set by the user!
WORK_DIR_RMS = None
MODEL_NAME_RMS = 'RmsConverterController_AAvdM_R2014b_sf'
INSTANCE_NAME_RMS = 'RmsConverterController_AAvdM_R2014b_sf'

WORK_DIR_PF = None
MODEL_NAME_PF = 'IEEEWPP'
INSTANCE_NAME_PF = 'IEEEWPP'

def main():
    world = mosaik.World(sim_config, mosaik_config=mosaik_config)
    create_scenario(world)
    world.run(until=END)

# Establishing the simulation scenario:
def create_scenario(world):
    # Help simulators in Python to allow the introduction and manipulation of a fault:
    faultsim = world.start('fault')
    faultmod = faultsim.Fault(rp=100, postrp=100.0, time_thresh=1.18)
    prefsim = world.start('fault')

    # Help simulators in Python that allow data aggregation and conversion between the FMUs:
    mod_from_pf = world.start('modif')
    mod_from_rms = world.start('modif')
    ppcc_mod = mod_from_pf.Modifier(mod_val=120.0, operator='div')

    # Controller simulator from FMU:
    rms_sim = world.start('FMUME', work_dir=WORK_DIR_RMS, model_name=MODEL_NAME_RMS, instance_name=INSTANCE_NAME_RMS,
                          step_size=1, step_factor=0.01, fmi_me_version=2, integrator='dp',
                          automated_initialization=False)
    maxCurrent = 1.1
    KiV = 10
    Kv = 0.0
    RP = 100
    KBOOST = 1.0
    Iprio = 2
    rmscon = rms_sim.RmsConverterController_AAvdM_R2014b_sf(
        Parameters_Converter_RMS_Controller_Saturation_UpperLimit=maxCurrent,
        Parameters_Converter_RMS_Controller_Saturation_LowerLimit=-maxCurrent,
        Parameters_Converter_RMS_Controller_PID_Controller_Saturate_UpperLimit=maxCurrent,
        Parameters_Converter_RMS_Controller_PID_Controller_Saturate_LowerLimit=-maxCurrent,
        Parameters_Converter_RMS_Controller_PID_Controller_Clamping_circuit_DeadZone_LowerValue=-maxCurrent,
        Parameters_Converter_RMS_Controller_PID_Controller_Clamping_circuit_DeadZone_UpperValue=maxCurrent,
        Parameters_Converter_RMS_Controller_PID_Controller1_Saturate_UpperLimit=maxCurrent,
        Parameters_Converter_RMS_Controller_PID_Controller1_Saturate_LowerLimit=-maxCurrent,
        Parameters_Converter_RMS_Controller_PID_Controller1_Clamping_circuit_DeadZone_LowerValue=-maxCurrent,
        Parameters_Converter_RMS_Controller_PID_Controller1_Clamping_circuit_DeadZone_UpperValue=maxCurrent,
        Parameters_Converter_RMS_Controller_Riferimento_Q1_Saturation_UpperLimit=maxCurrent,
        Parameters_Converter_RMS_Controller_Riferimento_Q1_Saturation_LowerLimit=-maxCurrent,
        Parameters_Converter_RMS_Controller_PID_Controller_Integral_Gain_Gain=1,
        Parameters_Converter_RMS_Controller_PID_Controller_Proportional_Gain_Gain=0.0,
        Parameters_Converter_RMS_Controller_PID_Controller1_Integral_Gain_Gain=KiV,
        Parameters_Converter_RMS_Controller_PID_Controller1_Proportional_Gain_Gain=Kv,
        Parameters_Converter_RMS_Controller_Ramp_limitation_Rate_Limiter_RisingSlewLimit=RP,
        R_on=1.0, K_aRCI=KBOOST, R_p=10.0, I_lim=Iprio, Vd=1.0, Vq=0.0, V_pcc_RMS=1.0,
        Qref_pu=0.0, Vdc_pu=1.0)

    # Power system simulator from FMU:
    pf_sim = world.start('FMUCS', work_dir=WORK_DIR_PF, model_name=MODEL_NAME_PF, instance_name=INSTANCE_NAME_PF,
                          step_size=1, step_factor=0.01, stop_time=10, stop_time_defined=True)

    pf_mod = pf_sim.IEEEWPP()
    P_0 = pf_sim.fmi_get(pf_mod, 'ElmGenstat_WPP_m:P:bus1')
    Q_0 = pf_sim.fmi_get(pf_mod, 'ElmGenstat_WPP_m:Q:bus1')
    V_0 = pf_sim.fmi_get(pf_mod, 'ElmGenstat_WPP_m:u1:bus1')
    Pnom = pf_sim.fmi_get(pf_mod, 'ElmGenstat_WPP_e:Pnom')
    i_d_0 = P_0 / Pnom / V_0
    i_q_0 = - Q_0 / Pnom / V_0

    # Further instantiation of conversion and fault modules:
    controller_mod = mod_from_rms.Modifier(mod_val=i_d_0, operator='sub')
    iq_mod = mod_from_rms.Modifier(mod_val=i_q_0, operator='sub')
    pref_mod = prefsim.Fault(rp=P_0/Pnom, postrp=P_0/Pnom, time_thresh=100.0)

    # Initialization of controller simulator:
    rms_sim.fmi_set(rmscon, 'Parameters_Converter_RMS_Controller_PID_Controller_Integrator_InitialCondition', i_d_0)
    rms_sim.fmi_set(rmscon, 'Parameters_Converter_RMS_Controller_PID_Controller1_Integrator_InitialCondition', i_q_0)
    rms_sim.fmi_initialize()

    # Connections between simulators (and help modules)
    world.connect(pf_mod, rmscon, ('ElmGenstat_WPP_m:u1:bus1', 'Vd'), time_shifted=True,
                  initial_data={'ElmGenstat_WPP_m:u1:bus1': None})
    world.connect(pf_mod, rmscon, ('ElmGenstat_WPP_m:u1:bus1', 'V_pcc_RMS'), time_shifted=True,
                  initial_data={'ElmGenstat_WPP_m:u1:bus1': None})
    world.connect(rmscon, controller_mod, ('Id_ref', 'input'))
    world.connect(rmscon, iq_mod, ('Iq_ref', 'input'))
    world.connect(pf_mod, ppcc_mod, ('ElmGenstat_WPP_m:Psum:bus1', 'input'))
    world.connect(controller_mod, pf_mod, ('output', 'EvtParam_id_ref_slot_id_ref_in'), time_shifted=True,
                  initial_data={'output': None})
    world.connect(iq_mod, pf_mod, ('output', 'EvtParam_iq_ref_slot_iq_ref_in'), time_shifted=True,
                  initial_data={'output': None})
    world.connect(ppcc_mod, rmscon, ('output', 'Vdc_pu'), time_shifted=True, initial_data={'output': None})
    world.connect(faultmod, rmscon, ('output',
                                     'Parameters_Converter_RMS_Controller_Ramp_limitation_Rate_Limiter_RisingSlewLimit'),
                  time_shifted=True, initial_data={'output': None})
    world.connect(pref_mod, rmscon, ('output', 'Parameters_Converter_RMS_Controller_Vdc_ref__V__Value'),
                  time_shifted=True, initial_data={'output': None})

    # Integration of hdf5 database for output data storage:
    db = world.start('DB', step_size=1, duration=END)
    hdf5 = db.Database(filename='tc1_case1.hdf5')
    world.connect(pf_mod, hdf5, 'ElmGenstat_WPP_m:P:bus1', 'ElmGenstat_WPP_m:u1:bus1', 'ElmSym_G1_s:xphi',
                  'ElmSym_G2_s:xphi', 'ElmSym_G1_s:xspeed', 'ElmSym_G2_s:xspeed')
    world.connect(rmscon, hdf5, 'Id_ref', 'Iq_ref')
    


if __name__ == '__main__':
    main()