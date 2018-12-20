'''This is a simple module that can serve as a mosaik simulator to manipulate the
data that is exchanged between two simulators. Specifically allows to modify received
data with a given value and operator. Usable e.g. for unit conversion.'''
import itertools
import mosaik_api

meta = {
    'models': {
        'Modifier': {
            'public': True,
            'attrs': ['input', 'output'],
            'params': ['mod_val',   # Value that is used to modify the input
            'operator']             # Operator that is used to modify the input...
        }                           # ... as string: 'add', 'sub', 'mul' or 'div'
    }
}

class ModComp(mosaik_api.Simulator):
    '''The module structures follows that standard mosaik interface.'''
    def __init__(self):
        super(ModComp, self).__init__(meta)
        self.sid = None

        self.cache = None
        self._entities = {}
        self.eid_counters = {}
        self._entities = {}

    def init(self, sid, step_size=1):
        self.sid = sid
        self.step_size = step_size

        return self.meta

    def create(self, num, model, **model_params):
        counter = self.eid_counters.setdefault(model, itertools.count())

        entities = []

        for i in range(num):
            eid = '%s_%s' % (model, next(counter))

            self._entities[eid] = model_params

            entities.append({'eid': eid, 'type': model, 'rel': []})

        return entities

    def step(self, t, inputs):
        self.cache = {}
        for eid, attrs in inputs.items():
            for attr, vals in attrs.items():
                # Input is modified based on specified value and operator:
                val = list(vals.values())[0]
                mod = self._entities[eid]
                if mod['operator'] == 'add':
                    self.cache[eid] = val + mod['mod_val']
                elif mod['operator'] == 'sub':
                    self.cache[eid] = val - mod['mod_val']
                elif mod['operator'] == 'mul':
                    self.cache[eid] = val * mod['mod_val']
                elif mod['operator'] == 'div':
                    self.cache[eid] = val / mod['mod_val']

        return t + self.step_size

    def get_data(self, outputs):
        data = {}
        for eid, attrs in outputs.items():
            data[eid] = {}
            for attr in attrs:
                data[eid][attr] = self.cache[eid]

        return data
