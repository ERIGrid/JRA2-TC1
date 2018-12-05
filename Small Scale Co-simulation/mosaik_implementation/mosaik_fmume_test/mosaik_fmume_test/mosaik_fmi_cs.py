'''Adapter to allow the integration of arbitrary FMUs 
(for Co-Simulation) as simulators into mosaik.'''
import itertools
import os
import mosaik_api
import fmipp
import mosaik_fmume_test.parse_xml

meta = {
    'models': {},
    'extra_methods': [
        'fmi_set', 'fmi_get'
    ]
}

# The user can specify the variables of the model by using
# this structure, but the adapter can read alternatively
# read it from the XML file.
'''
var_table = {
    'parameter': {
        'a': 'Real',
        'b': 'Integer',
        'c': 'Boolean',
        'd': 'String'
    },
    'input': {
        'x': 'Real',
        ...
    },
    'output': {
        ...
    }
}
'''

class FmuCsAdapter(mosaik_api.Simulator):
    def __init__(self):
        super(FmuCsAdapter, self).__init__(meta)
        self.sid = None

        self._entities = {}
        self.eid_counters = {}

        self.work_dir = None
        self.model_name = None
        self.instance_name = None
        self.var_table = None
        self.translation_table = None
        self.step_size = None
        self.logging_on = False
        self.time_diff_resolution = 1e-9
        self.interactive = False
        self.visible = False
        self.start_time = 0
        self.stop_time = 10000
        self.stop_time_defined = False
        self.uri_to_extracted_fmu = None
        self.step_factor = None

    def init(self, sid, work_dir=None, model_name=None, instance_name=None, var_table=None, step_size=1, logging_on=False,
             time_diff_resolution=1e-9, interactive=False, visible=False, stop_time_defined=False, step_factor=1,
             stop_time=10000):
        self.sid = sid
        # Set simulator parameters needed mostly for the FMU:
        self.work_dir = work_dir
        self.model_name = model_name
        self.instance_name = instance_name
        self.step_size = step_size
        self.step_factor = step_factor
        self.logging_on = logging_on
        self.time_diff_resolution =time_diff_resolution
        self.interactive = interactive
        self.visible = visible
        self.stop_time_defined = stop_time_defined
        self.stop_time = stop_time

        # Extract the module from the FMU:
        path_to_fmu = os.path.join(self.work_dir, self.model_name + '.fmu')
        self.uri_to_extracted_fmu = fmipp.extractFMU(path_to_fmu, self.work_dir)
        # Get the model description and use it if the user did not specify the variables:
        xmlfile = os.path.join(self.work_dir, self.model_name, 'modelDescription.xml')
        if var_table is None:
            self.var_table, self.translation_table = mosaik_fmume_test.parse_xml.get_var_table(xmlfile)
        else:
            self.var_table = var_table
            self.translation_table = {}

        self.adjust_var_table()
        self.adjust_meta()

        return self.meta

    def create(self, num, model, **model_params):
        counter = self.eid_counters.setdefault(model, itertools.count())

        entities = []

        for i in range(num):
            eid = '%s_%s' % (model, next(counter))

            fmu = fmipp.FMUCoSimulation(self.uri_to_extracted_fmu, self.model_name, self.logging_on,
                                        self.time_diff_resolution)

            self._entities[eid] = fmu
            inst_stat = self._entities[eid].instantiate(self.instance_name, self.start_time, self.visible,
                                                        self.interactive)
            assert inst_stat == fmipp.fmiOK
            # Set parameter values and initialize:
            self.set_values(eid, model_params, 'parameter')
            init_stat = self._entities[eid].initialize(self.start_time, self.stop_time_defined, self.stop_time)
            assert init_stat == fmipp.fmiOK

            entities.append({'eid': eid, 'type': model, 'rel': []})

        return entities

    def step(self, t, inputs=None):
        # Step simulator if no input is required:
        if inputs is None or inputs == {}:
            for fmu in self._entities.values():
                step_stat = fmu.doStep(t * self.step_factor, self.step_size * self.step_factor, True)
                assert step_stat == fmipp.fmiOK
        # Step simulator with input:
        else:
            for eid, attrs in inputs.items():
                for attr, vals in attrs.items():
                    for val in vals.values():
                        self.set_values(eid, {attr: val}, 'input')

                step_stat = self._entities[eid].doStep(t * self.step_factor, self.step_size * self.step_factor, True)
                assert step_stat == fmipp.fmiOK

        return t + self.step_size

    def get_data(self, outputs):
        data = {}
        for eid, attrs in outputs.items():
            data[eid] = {}
            for attr in attrs:
                data[eid][attr] = self.get_value(eid, attr)

        return data

    def adjust_var_table(self):
        '''Help function for variable name management.'''
        self.var_table.setdefault('parameter', {})
        self.var_table.setdefault('input', {})
        self.var_table.setdefault('output', {})

        self.translation_table.setdefault('parameter', {})
        self.translation_table.setdefault('input', {})
        self.translation_table.setdefault('output', {})

    def adjust_meta(self):
        '''Help function to provide variable info to mosaik.'''
        attr_list = list(self.translation_table['input'].keys())
        out_list = list(self.translation_table['output'].keys())
        attr_list.extend(out_list)

        self.meta['models'][self.instance_name] = {
            'public': True,
            'params': list(self.translation_table['parameter'].keys()),
            'attrs': attr_list
        }

    def set_values(self, eid, val_dict, var_type):
        '''Help function to set values to the FMU.'''
        for alt_name, val in val_dict.items():
            # Translation may be needed if variables have different names for FMU and mosaik:
            name = self.translation_table[var_type][alt_name]
            set_func = getattr(self._entities[eid], 'set' + self.var_table[var_type][name] + 'Value')
            set_stat = set_func(name, val)
            assert set_stat == fmipp.fmiOK

    def get_value(self, eid, alt_attr):
        '''Help function to get values from the FMU.'''
        # Translation may be needed if variables have different names for FMU and mosaik:
        attr = self.translation_table['output'][alt_attr]
        get_func = getattr(self._entities[eid], 'get' + self.var_table['output'][attr] + 'Value')
        val = get_func(attr)
        return val

    def fmi_set(self, entity, var_name, value, var_type='input'):
        var_dict = {var_name: value}
        self.set_values(entity.eid, var_dict, var_type)

    def fmi_get(self, entity, var_name):
        val = self.get_value(entity.eid, var_name)
        return val
